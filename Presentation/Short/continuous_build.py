"""Render the talk in one Manim scene, retaining animation and slide caches.

Section modules organize source only. No saved boundary frames are restored.
The last published presentation remains usable until the new scene succeeds.
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
from build_utils import atomic_json

ROOT=Path(__file__).resolve().parent
SCENE="QuantumStochasticShort"


def source_fingerprint(profile):
    files={ROOT/name for name in ("continuous_build.py","build_presentation.py","opening.py",
           "presentation_common.py","slide_numbering.py","deck.py","reveal_plan.json","manim.cfg","requirements.txt","build_utils.py")}
    for section in SECTIONS:
        files.add(ROOT/section.source)
        for pattern in section.dependencies:files.update(ROOT.glob(pattern))
    versions={name:importlib.metadata.version(name) for name in ("manim","manim-slides","numpy","scipy","pillow")}
    digest=hashlib.sha256(json.dumps([profile,versions,sys.version_info[:2]],sort_keys=True).encode())
    for path in sorted(files):
        digest.update(path.relative_to(ROOT).as_posix().encode());digest.update(path.read_bytes())
    return digest.hexdigest()


def validate_storyboard(steps):
    plan=json.loads((ROOT/"reveal_plan.json").read_text())
    titles=[step["title"] for step in steps]
    expected=[title for anchor in plan["original_topic_order"] for title in plan["reveal_sequences"][anchor]]
    if titles!=expected:raise RuntimeError("Rendered reveals differ from reveal_plan.json")
    if len(steps)!=plan["expected_steps"]:raise RuntimeError("Incorrect reveal count")


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preview",choices=[s.id for s in SECTIONS],help="Isolated 480p content preview; final talk stays untouched")
    parser.add_argument("--draft",action="store_true",help="Continuous 480p draft of all short-talk actions")
    parser.add_argument("--status",action="store_true")
    parser.add_argument("--list",action="store_true")
    parser.add_argument("--force",action="store_true",help="Run the continuous scene again with animation caching enabled")
    args=parser.parse_args(argv)
    os.chdir(ROOT)
    if args.list:
        for section in SECTIONS:print(f"{section.id:14} {section.source}")
        return
    profile="preview" if args.preview or args.draft else "final"
    job=ROOT/"media"/"build"/"continuous"/(args.preview or ("draft" if args.draft else "final"))
    manifest_path=job/"manifest.json"
    target=ROOT/"slides"/(SCENE+("-preview" if profile=="preview" else "")+".json")
    try:previous=json.loads(manifest_path.read_text())
    except (OSError,ValueError):previous={}
    fingerprint=source_fingerprint(profile)
    current=previous.get("fingerprint")==fingerprint and target.is_file()
    if current:
        published=json.loads(target.read_text())
        current=all((ROOT/s[k]).is_file() for s in published["slides"] for k in ("file","rev_file"))
    if args.status:
        print("Continuous scene: "+("up to date" if current else "render required (animation cache enabled)"));return
    if current and not args.force:
        print("Continuous scene unchanged; no renderer launched.");return
    job.mkdir(parents=True,exist_ok=True)
    exports=job/"exports"
    env={k:v for k,v in os.environ.items() if not k.startswith("QSI_")}
    env.update(QSI_BUILD="1",QSI_CONTINUOUS="1",QSI_OUTPUT_FOLDER=str(exports),
               QSI_RESULT_FILE=str(job/"steps.json"),QSI_PREVIEW="1" if profile=="preview" else "0")
    if args.preview:env["QSI_ONLY_SECTION"]=args.preview
    command=[str(Path(sys.executable).with_name("manim-slides.exe")),"render",
             "--quality","l" if profile=="preview" else "h","--fps","15" if profile=="preview" else "30",
             "--media_dir",str(ROOT/"media"/"c"/"one"/(args.preview or ("draft" if args.draft else "f"))),
             "--progress_bar","none","opening.py",SCENE]
    started=time.perf_counter()
    log_path=job/"render.log"
    print(f"Rendering one continuous scene; clip cache enabled. Log: {log_path}",flush=True)
    with log_path.open("w",encoding="utf-8") as log:
        result=subprocess.run(command,cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT)
    if result.returncode:raise RuntimeError(f"Render failed; the previous talk is preserved. See {log_path}")
    data=json.loads((exports/f"{SCENE}.json").read_text())
    steps=json.loads((job/"steps.json").read_text())["steps"]
    if len(data["slides"])!=len(steps):raise RuntimeError("Notes/clip count mismatch")
    if not args.preview:validate_storyboard(steps)
    for slide,step in zip(data["slides"],steps):
        if slide["notes"]!=step["notes"]:raise RuntimeError("Notes mismatch")
        for key in ("file","rev_file"):
            path=Path(slide[key])
            if not path.is_absolute():path=ROOT/path
            if not path.is_file():raise FileNotFoundError(path)
            slide[key]=Path(os.path.relpath(path,ROOT)).as_posix()
    # Publish only a complete, internally checked scene. No section assembly.
    atomic_json(target,data)
    atomic_json(ROOT/"media"/("preview_steps.json" if profile=="preview" else "opening_steps.json"),steps)
    log=log_path.read_text(encoding="utf-8",errors="replace")
    report={"mode":"continuous","fingerprint":source_fingerprint(profile),"steps":len(steps),
            "cached_animations":len(re.findall(r"Animation\s+\d+\s*:\s*Using cached",log)),
            "animations":steps[-1]["end_animation"],"elapsed_seconds":round(time.perf_counter()-started,2),
            "log":str(log_path.relative_to(ROOT)),"frozen_boundary_frames":False,"slide_numbers":True}
    atomic_json(manifest_path,report)
    print(json.dumps(report),flush=True)


if __name__=="__main__":main()
