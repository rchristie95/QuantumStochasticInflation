"""Check the short edition's exports and render held frames for visual review."""
import argparse
import json
from pathlib import Path
import subprocess
from PIL import Image,ImageDraw
import numpy as np
import zxingcpp
from continuous_build import validate_storyboard


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--draft',action='store_true')
    args=parser.parse_args()
    suffix='-preview' if args.draft else ''
    slides=json.loads(Path(f'slides/QuantumStochasticShort{suffix}.json').read_text())['slides']
    steps=json.loads(Path('media/preview_steps.json' if args.draft else 'media/opening_steps.json').read_text())
    validate_storyboard(steps)
    assert len(slides)==len(steps)==json.loads(Path('reveal_plan.json').read_text())['expected_steps']
    out=Path('media/review-draft' if args.draft else 'media/review-final');out.mkdir(exist_ok=True)
    dimensions=set();duration=0;frames=[]
    for i,(slide,step) in enumerate(zip(slides,steps),1):
        assert step['step']==i and slide['notes']==step['notes'] and step['notes'].strip()
        assert not slide['loop'] and not slide['auto_next']
        for key in ('file','rev_file'):
            assert Path(slide[key]).is_file()
            meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height,r_frame_rate','-show_entries','format=duration','-of','json',slide[key]]))
            stream=meta['streams'][0];dimensions.add((stream['width'],stream['height'],stream['r_frame_rate']))
            if key=='file':duration+=float(meta['format']['duration'])
        frame=out/f'step-{i:02}.png'
        subprocess.run(['ffmpeg','-v','error','-y','-sseof','-0.3','-i',slide['file'],'-frames:v','1',str(frame)],capture_output=True,check=True)
        pixels=np.asarray(Image.open(frame).convert('RGB'),dtype=float)
        foreground=np.max(np.abs(pixels-[16,24,36]),axis=2)>30;h,w=foreground.shape
        corner=step['title'] in ['What stochastic inflation does','The sharp Fourier window','Cutoff sweep: boundary kicks']
        left,right,top,bottom=(.86,.98,.02,.09) if corner else (.43,.57,.94,.99)
        assert foreground[int(top*h):int(bottom*h),int(left*w):int(right*w)].sum()>30,f'Missing counter at {i}'
        if i==1:
            code=zxingcpp.read_barcode(Image.open(frame))
            assert code and code.text=='https://arxiv.org/abs/2606.12636'
        frames.append(frame)
    expected=(854,480,'15/1') if args.draft else (1920,1080,'30/1')
    assert dimensions=={expected},dimensions
    selected=[4,5,7,8,10,11,13,14,15,16,25,26,27,32,33,34,46,47,58,59]
    for start in range(0,len(selected),8):
        sheet=Image.new('RGB',(1280,4*390),'#101824');draw=ImageDraw.Draw(sheet)
        for j,n in enumerate(selected[start:start+8]):
            x=(j%2)*640;y=(j//2)*390
            sheet.paste(Image.open(frames[n-1]).convert('RGB').resize((640,360)),(x,y))
            draw.text((x+8,y+365),f'{n}: {steps[n-1]["title"]}',fill='white')
        sheet.save(out/f'condensed-{start//8+1}.jpg',quality=93)
    report=dict(actions=len(slides),dimensions=list(expected),animation_seconds=round(duration,2),
                notes_verified=True,forward_reverse_verified=True,counters_verified=True,qr_verified=True,storyboard_verified=True)
    (out/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))


if __name__=='__main__':main()
