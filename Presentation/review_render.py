"""Extract every segment's held frame and contact sheets for visual review."""
from pathlib import Path
import json
import subprocess
from PIL import Image, ImageDraw
import numpy as np
import zxingcpp
from deck import CHAPTERS


def main():
    data=json.loads(Path("slides/QuantumStochasticOpening.json").read_text())
    notes=json.loads(Path("media/opening_steps.json").read_text())
    slides=data["slides"]
    plan=json.loads(Path("reveal_plan.json").read_text())
    assert len(slides)==len(notes)==plan["expected_steps"], (len(slides),len(notes))
    assert [entry["step"] for entry in notes]==list(range(1,len(notes)+1))
    chapters=[entry["title"].removesuffix(" / chapter") for entry in notes if entry["title"].endswith(" / chapter")]
    assert chapters==CHAPTERS,chapters
    titles=[entry["title"] for entry in notes]
    assert titles[:2]==["Title page","Talk outline"],titles[:2]
    anchors=plan["original_topic_order"]
    positions=[titles.index(title) for title in anchors]
    assert positions==sorted(set(positions)), "Topics must follow the chapter outline"
    for anchor,sequence in plan["reveal_sequences"].items():
        i=anchors.index(anchor)
        end=titles.index(anchors[i+1]) if i+1<len(anchors) else len(titles)
        assert titles[titles.index(anchor):end]==sequence, (anchor,titles[titles.index(anchor):end])
    assert not any(t in titles for t in ["Qubit toy model / chapter","Entangled spins","Gaussian purity and area","Pure inputs, mixed retained output","Equal covariances","Taking the partial trace","Rank-one Z readout","Recorded outcomes","Averaging the records"])
    assert 'Why stochastic inflation matters' not in titles
    assert titles.index("Origins")<titles.index("What stochastic inflation does")<titles.index("Gradients and separate regions")<titles.index("Phase-space Langevin equations")<titles.index("Many oscillators, one collective mode")<titles.index("The spectator Lagrangian")
    assert titles.index("The spectator Lagrangian")<titles.index("The retained QFT mode")<titles.index("Bulk and boundary shell")<titles.index("Back to the boundary channel")<titles.index("Massive spectator dynamics")
    out=Path("media/opening-review")
    out.mkdir(exist_ok=True)
    frames=[]
    dimensions=set()
    duration=0
    for i,slide in enumerate(slides):
        assert slide["notes"]==notes[i]["notes"] and slide["notes"].strip(), f"Incorrect notes for {i+1}"
        assert not slide["loop"] and not slide["auto_next"]
        for key in ("file","rev_file"):
            assert Path(slide[key]).is_file(), slide[key]
            meta=json.loads(subprocess.run(["ffprobe","-v","error","-select_streams","v:0",
                "-show_entries","stream=width,height,r_frame_rate:format=duration","-of","json",slide[key]],
                capture_output=True,text=True,check=True).stdout)
            stream=meta["streams"][0]
            dimensions.add((stream["width"],stream["height"],stream["r_frame_rate"]))
            assert float(meta["format"]["duration"])>0
            if key=="file":
                duration+=float(meta["format"]["duration"])
        target=out/f"step-{i+1:02}.png"
        subprocess.run(["ffmpeg","-v","error","-y","-sseof","-0.12","-i",slide["file"],
                        "-frames:v","1",str(target)],check=True,capture_output=True)
        pixels=np.asarray(Image.open(target).convert("RGB"),dtype=float)
        foreground=np.max(np.abs(pixels-np.array([16,24,36])),axis=2)>30
        h,w=foreground.shape
        corner=notes[i]['title'] in ['What stochastic inflation does','The sharp Fourier window','Cutoff sweep: boundary kicks']
        left,right=(.86,.98) if corner else (.43,.57)
        top,bottom=(.02,.09) if corner else (.94,.99)
        assert foreground[int(top*h):int(bottom*h),int(left*w):int(right*w)].sum()>30, f"Missing reveal counter: step {i+1}"
        if i==0:
            qr=zxingcpp.read_barcode(Image.open(target))
            assert qr and qr.text=="https://arxiv.org/abs/2606.12636", "Cover QR must decode to the paper"
        if i>=2 and not notes[i]["title"].endswith(" / chapter"):
            assert foreground[:int(.13*len(pixels))].sum()>50, f"Missing heading: step {i+1}"
            assert foreground[int(.91*len(pixels)):].sum()>30, f"Missing footer: step {i+1}"
        frames.append(target)
    for start in range(0,len(frames),6):
        sheet=Image.new("RGB",(1280,3*390),"#101824")
        draw=ImageDraw.Draw(sheet)
        for j,path in enumerate(frames[start:start+6]):
            frame=Image.open(path).convert("RGB").resize((640,360))
            x=(j%2)*640;y=(j//2)*390
            sheet.paste(frame,(x,y))
            draw.text((x+12,y+365),f"{start+j+1:02}  {notes[start+j]['title']}",fill="white")
        sheet.save(out/f"contact-{start//6+1}.jpg",quality=93)
    assert len(dimensions)==1, dimensions
    report={"segments":len(slides),"chapters":chapters,"all_video_dimensions":list(dimensions),
            "animation_seconds":round(duration,2),"notes_verified":True,"reverse_files_verified":True,"cover_qr_verified":True,"slide_counter_removed":True,"logical_reveal_order_verified":True,
            "review_folder":str(out)}
    report.pop("slide_counter_removed",None)
    report["slide_numbers_verified"]=True
    (out/"report.json").write_text(json.dumps(report,indent=2))
    print(json.dumps(report))


if __name__ == "__main__":
    main()
