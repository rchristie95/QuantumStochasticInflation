"""Section-level builds with clip caching and a single assembled presentation.

Each section starts directly in its own scene, using a frozen incoming body for
the existing opening fade. A section's terminal frame is content-addressed: only
real changes to that frame invalidate the next section's incoming transition.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

from deck import SECTIONS

ROOT=Path(__file__).resolve().parent
SCENE="QuantumStochasticOpening"
SCHEMA=4
PROFILES={"final":{"quality":"h","fps":30,"resolution":[1920,1080]},
          "preview":{"quality":"l","fps":15,"resolution":[854,480]}}
SHARED=("opening.py","presentation_common.py","deck.py","sections/__init__.py","requirements.txt")


def atomic_json(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_suffix(path.suffix+".tmp")
    tmp.write_text(json.dumps(value,indent=2),encoding="utf-8")
    tmp.replace(path)


def fingerprint(section,profile):
    digest=hashlib.sha256()
    versions={name:importlib.metadata.version(name) for name in ("manim","manim-slides","numpy","scipy","pillow")}
    digest.update(json.dumps([SCHEMA,PROFILES[profile],versions,sys.version_info[:2]],sort_keys=True).encode())
    files={ROOT/name for name in SHARED};files.add(ROOT/section.source)
    for pattern in section.dependencies:
        matches=list(ROOT.glob(pattern))
        if not matches: digest.update(("missing:"+pattern).encode())
        files.update(matches)
    for path in sorted(files):
        digest.update(path.relative_to(ROOT).as_posix().encode())
        digest.update(path.read_bytes() if path.is_file() else b"missing")
    return digest.hexdigest()


def load_manifest(path):
    try:
        data=json.loads(Path(path).read_text())
        return data if data.get("schema")==SCHEMA else {}
    except (OSError,ValueError):
        return {}


def record_valid(record):
    return bool(record and record.get("slides") and record.get("steps")
                and len(record["slides"])==len(record["steps"])) and all(
        (ROOT/slide[key]).is_file() for slide in record["slides"] for key in ("file","rev_file")) and (ROOT/record["frame"]).is_file()


def context_of(record):
    if not record: return {"frame":None,"chrome":None}
    return {"frame":record["frame"],"chrome":record.get("chrome")}


def needs_build(record,source_hash,context):
    return not record_valid(record) or record.get("fingerprint")!=source_hash or record.get("incoming")!=context


def terminal_frame(folder,slide):
    from PIL import Image
    target=folder/"terminal.tmp.png"
    subprocess.run(["ffmpeg","-v","error","-y","-sseof","-0.12","-i",str(ROOT/slide["file"]),"-frames:v","1",str(target)],check=True)
    with Image.open(target) as image:
        digest=hashlib.sha256(image.convert("RGB").tobytes()).hexdigest()
    dest=folder/"frames"/(digest+".png");dest.parent.mkdir(exist_ok=True)
    if dest.exists(): target.unlink()
    else: target.replace(dest)
    return dest.relative_to(ROOT).as_posix()


def render_section(section,profile,folder,context):
    job=folder/section.id;job.mkdir(parents=True,exist_ok=True)
    context_file=job/"incoming.json"
    render_context={**context,"frame":str(ROOT/context["frame"]) if context["frame"] else None}
    atomic_json(context_file,render_context)
    env=os.environ.copy()
    # A new slide-cache namespace keeps the published deck available while
    # repairing older clips with incomplete foreground compositing.
    exports=job/"exports_v2"
    env.update(QSI_BUILD="1",QSI_OUTPUT_FOLDER=str(exports),QSI_ONLY_SECTION=section.id,
               QSI_CONTEXT_FILE=str(context_file),QSI_RESULT_FILE=str(job/"steps.json"),
               QSI_PREVIEW="1" if profile=="preview" else "0")
    settings=PROFILES[profile]
    # FFmpeg and Manim's stat() still encounter MAX_PATH on Windows. Keep the
    # deep partial_movie_files tree short, while logs/metadata stay descriptive.
    cache_dir=ROOT/"media"/"c"/profile[0]/section.id
    command=[str(Path(sys.executable).with_name("manim-slides.exe")),"render",
             "--quality",settings["quality"],"--fps",str(settings["fps"]),
             "--media_dir",str(cache_dir),"--progress_bar","none","opening.py",SCENE]
    print(f"Rendering {section.id} (clip cache enabled)...",flush=True)
    log_file=job/"render.log"
    with log_file.open("w",encoding="utf-8") as log:
        result=subprocess.run(command,cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT)
    if result.returncode:
        raise RuntimeError(f"Section {section.id} failed; see {log_file}")
    data=json.loads((exports/f"{SCENE}.json").read_text())
    index=json.loads((job/"steps.json").read_text())
    if len(data["slides"])!=len(index["steps"]): raise RuntimeError(f"Step count mismatch in {section.id}")
    for slide,step in zip(data["slides"],index["steps"]):
        if slide["notes"]!=step["notes"]: raise RuntimeError(f"Notes mismatch in {section.id}")
        for key in ("file","rev_file"):
            path=Path(slide[key])
            if not path.is_absolute(): path=ROOT/path
            if not path.is_file(): raise FileNotFoundError(path)
            slide[key]=Path(os.path.relpath(path,ROOT)).as_posix()
    text=log_file.read_text(encoding="utf-8",errors="replace")
    total=index["steps"][-1]["end_animation"]
    # Rich inserts its source-location column between "cached" and "data".
    hits=len(re.findall(r"Animation\s+\d+\s*:\s*Using cached",text))
    frame=terminal_frame(folder,data["slides"][-1])
    record={"fingerprint":fingerprint(section,profile),"incoming":context,"slides":data["slides"],
            "steps":index["steps"],"chrome":index["chrome"],"frame":frame}
    report={"section":section.id,"cached_animations":hits,"new_animations":total-hits,
            "log":str(log_file.relative_to(ROOT))}
    return record,report


def assemble(records):
    slides=[];steps=[]
    for section in SECTIONS:
        record=records[section.id]
        if not record_valid(record): raise RuntimeError(f"Invalid output for {section.id}")
        for slide,entry in zip(record["slides"],record["steps"]):
            if slide["notes"]!=entry["notes"]: raise RuntimeError(f"Notes mismatch in {section.id}")
            slides.append(slide)
            steps.append({**entry,"step":len(steps)+1,"section":section.id})
    return slides,steps


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    ids=[s.id for s in SECTIONS]
    parser.add_argument("--preview",choices=ids,help="Render only this section at 480p; leave the final deck untouched")
    parser.add_argument("--section",action="append",default=[],choices=ids,help="Also check/render this section through its clip cache")
    parser.add_argument("--force",action="store_true",help="Check every section again using clip caches")
    parser.add_argument("--status",action="store_true",help="Show source/dependency changes without rendering")
    parser.add_argument("--list",action="store_true",help="List editable section files")
    args=parser.parse_args(argv)
    os.chdir(ROOT)
    if args.list:
        for section in SECTIONS: print(f"{section.id:14} {section.source}")
        return
    started=time.perf_counter()
    profile="preview" if args.preview else "final"
    folder=ROOT/"media"/"build"/profile
    manifest_path=folder/"manifest.json"
    manifest=load_manifest(manifest_path)
    records=manifest.get("sections",{}).copy()
    hashes={s.id:fingerprint(s,profile) for s in SECTIONS}
    if args.status:
        changed=[s.id for s in SECTIONS if not record_valid(records.get(s.id)) or records[s.id].get("fingerprint")!=hashes[s.id]]
        print("Changed: "+(", ".join(changed) or "none"));return
    folder.mkdir(parents=True,exist_ok=True)
    forced=set(args.section) | (set(ids) if args.force else set())
    reports=[];reused=[]
    previous=None
    for i,section in enumerate(SECTIONS):
        if args.preview and section.id!=args.preview: continue
        if args.preview:
            final=load_manifest(ROOT/"media"/"build"/"final"/"manifest.json").get("sections",{})
            if i and not record_valid(final.get(SECTIONS[i-1].id)):
                raise RuntimeError("Build the final deck once before previewing a later section")
            previous=final.get(SECTIONS[i-1].id) if i else None
        context=context_of(previous)
        old=records.get(section.id)
        if section.id in forced or needs_build(old,hashes[section.id],context):
            record,report=render_section(section,profile,folder,context)
            records[section.id]=record;reports.append(report)
            # Save completed work even if a later render fails. The public
            # presenter manifest is replaced only after the full deck succeeds.
            atomic_json(manifest_path,{"schema":SCHEMA,"profile":profile,"sections":records})
        else:
            reused.append(section.id)
            print(f"Reusing {section.id}",flush=True)
        previous=records[section.id]
    if args.preview:
        record=records[args.preview]
        presentation={"slides":record["slides"],"resolution":PROFILES[profile]["resolution"],"background_color":"#101824"}
        target=ROOT/"slides"/f"{SCENE}-preview.json"
        atomic_json(target,presentation)
        atomic_json(folder/"preview_steps.json",record["steps"])
    elif reports or not (ROOT/"slides"/f"{SCENE}.json").exists():
        slides,steps=assemble(records)
        presentation={"slides":slides,"resolution":PROFILES[profile]["resolution"],"background_color":"#101824"}
        atomic_json(ROOT/"slides"/f"{SCENE}.json",presentation)
        atomic_json(ROOT/"media"/"opening_steps.json",steps)
    atomic_json(manifest_path,{"schema":SCHEMA,"profile":profile,"sections":records})
    report={"rendered_sections":[r["section"] for r in reports],"reused_sections":reused,
            "jobs":reports,"elapsed_seconds":round(time.perf_counter()-started,3)}
    atomic_json(folder/"last-build.json",report)
    print(f"{len(reports)} section(s) checked/rendered, {len(reused)} reused; {report['elapsed_seconds']:.2f}s.")
    if args.preview: print(f"Preview: manim-slides present {SCENE}-preview")


if __name__=="__main__": main()
