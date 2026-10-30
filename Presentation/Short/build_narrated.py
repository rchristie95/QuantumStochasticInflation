"""Export the continuous short talk with action-synchronized synthetic narration."""
import argparse
import asyncio
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import textwrap

import edge_tts

ROOT=Path(__file__).resolve().parent
CACHE=ROOT/'media/narration'
OUTPUT=ROOT/'Narrated'
ACTION_COUNT=json.loads((ROOT/'reveal_plan.json').read_text())['expected_steps']
FPS=30
SAMPLE_RATE=48000
PRE=.5
POST=2.5
NAME='Short presentation - AI narrated'


def run(command):
    result=subprocess.run(command,capture_output=True,text=True)
    if result.returncode:
        raise RuntimeError(result.stderr[-5000:])
    return result.stdout


def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def key(data):
    return hashlib.sha256(json.dumps(data,sort_keys=True).encode()).hexdigest()[:20]


def write_json(path,data):
    temporary=path.with_suffix(path.suffix+'.tmp')
    temporary.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    temporary.replace(path)


def spoken_text(text):
    # Spell out scientific initialisms without altering the authored script.
    for original,replacement in [('GKLS','G K L S'),('SSE','S S E'),('POVM','P O V M'),
                                 ('QFT','Q F T'),('dN','d N'),('dW','d W')]:
        text=re.sub(r'\b'+original+r'\b',replacement,text)
    return text.replace('W n prime joint','W sub n prime joint').replace('W n joint','W sub n joint')


async def synthesize(action,voice,rate,semaphore):
    speech_key=key([voice,rate,action['spoken'],edge_tts.__version__])
    audio=CACHE/f'{speech_key}.mp3';metadata=CACHE/f'{speech_key}.json'
    if audio.is_file() and metadata.is_file():
        saved=json.loads(metadata.read_text(encoding='utf-8'))
        if saved['audio_sha256']==digest(audio):
            return dict(action,audio=str(audio),speech_seconds=saved['seconds'],boundaries=saved['boundaries'])
    async with semaphore:
        for attempt in range(3):
            try:
                boundaries=[];temporary=audio.with_suffix('.tmp.mp3')
                communicate=edge_tts.Communicate(action['spoken'],voice=voice,rate=rate,boundary='WordBoundary')
                with temporary.open('wb') as stream:
                    async for chunk in communicate.stream():
                        if chunk['type']=='audio':stream.write(chunk['data'])
                        elif chunk['type']=='WordBoundary':boundaries.append(chunk)
                seconds=float(probe(temporary)['format']['duration'])
                assert seconds>0 and boundaries,'Speech service returned incomplete audio.'
                assert boundaries[-1]['offset']/1e7<seconds+.5,'Invalid speech timestamps.'
                temporary.replace(audio)
                write_json(metadata,{'voice':voice,'rate':rate,'spoken':action['spoken'],'seconds':seconds,
                                     'audio_sha256':digest(audio),'boundaries':boundaries})
                print(f'Speech {action["action"]:02}/{ACTION_COUNT}: {seconds:.1f}s — {action["title"]}',flush=True)
                return dict(action,audio=str(audio),speech_seconds=seconds,boundaries=boundaries)
            except Exception:
                if attempt==2:raise
                await asyncio.sleep(2**attempt)


def choose_encoder(requested):
    if requested=='cpu':return 'libx264'
    test=subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','color=size=1920x1080:rate=30:duration=0.1',
                         '-an','-c:v','h264_nvenc','-preset','p4','-f','null','-'],capture_output=True)
    if test.returncode==0:return 'h264_nvenc'
    if requested=='nvenc':raise RuntimeError(test.stderr.decode(errors='replace'))
    return 'libx264'


def render_action(action,encoder):
    render_key=key(['narrated-v1',digest(action['video']),digest(action['audio']),
                    action['frames'],PRE,POST,encoder])
    video=CACHE/f'{render_key}.mp4';audio=CACHE/f'{render_key}.wav';metadata=CACHE/f'{render_key}.render.json'
    if video.is_file() and audio.is_file() and metadata.is_file():
        return dict(action,rendered_video=str(video),rendered_audio=str(audio))
    video_temp=video.with_suffix('.tmp.mp4');audio_temp=audio.with_suffix('.tmp.wav')
    extra=max(0,action['seconds']-action['video_seconds'])
    samples=action['frames']*(SAMPLE_RATE//FPS)
    filters=(f'[0:v]tpad=stop_mode=clone:stop_duration={extra+1:.6f},'
             f'trim=duration={action["seconds"]:.9f},setpts=PTS-STARTPTS,setsar=1[v];'
             f'[1:a]aresample={SAMPLE_RATE},adelay={round(PRE*SAMPLE_RATE)}S,'
             f'apad,atrim=end_sample={samples},asetpts=PTS-STARTPTS[a]')
    codec=['-c:v',encoder,'-pix_fmt','yuv420p','-r',str(FPS),'-g','60','-bf','0']
    codec+=['-preset','p4','-rc','vbr','-cq','19','-b:v','0'] if encoder=='h264_nvenc' else ['-preset','veryfast','-crf','19','-threads','4']
    run(['ffmpeg','-v','error','-y','-i',action['video'],'-i',action['audio'],
         '-filter_complex',filters,'-map','[v]','-an',*codec,'-frames:v',str(action['frames']),str(video_temp),
         '-map','[a]','-vn','-c:a','pcm_s16le','-ar',str(SAMPLE_RATE),'-ac','1',str(audio_temp)])
    v=probe(video_temp)['streams'][0];a=probe(audio_temp)['streams'][0]
    assert (v['width'],v['height'],v['r_frame_rate'])==(1920,1080,'30/1')
    assert int(v['nb_frames'])==action['frames']
    assert int(a['duration_ts'])==samples
    video_temp.replace(video);audio_temp.replace(audio)
    write_json(metadata,{'action':action['action'],'frames':action['frames'],'samples':samples})
    print(f'Video {action["action"]:02}/{ACTION_COUNT}: {action["seconds"]:.1f}s — {action["title"]}',flush=True)
    return dict(action,rendered_video=str(video),rendered_audio=str(audio))


def concat_file(path,actions,field):
    def quote(value):return Path(value).as_posix().replace("'","'\\''")
    path.write_text('ffconcat version 1.0\n'+''.join(f"file '{quote(a[field])}'\n" for a in actions),encoding='utf-8')


def srt_clock(seconds):
    ms=round(seconds*1000);hours,ms=divmod(ms,3600000);minutes,ms=divmod(ms,60000);seconds,ms=divmod(ms,1000)
    return f'{hours:02}:{minutes:02}:{seconds:02},{ms:03}'


def write_subtitles(actions,path):
    cues=[]
    for action in actions:
        words=[]
        def flush():
            if not words:return
            text=' '.join(w['text'] for w in words)
            text=text.replace('G K L S','GKLS').replace('P O V M','POVM').replace('S S E','SSE').replace('d N','dN').replace('W sub n','W n')
            start=action['start']+PRE+words[0]['offset']/1e7
            end=action['start']+PRE+(words[-1]['offset']+words[-1]['duration'])/1e7
            cues.append((start,min(end+.15,action['end']),textwrap.fill(text,width=48)))
            words.clear()
        for word in action['boundaries']:
            if words and (len(words)>=12 or len(' '.join(w['text'] for w in words))+len(word['text'])>88):flush()
            words.append(word)
        flush()
    path.write_text('\n\n'.join(f'{i}\n{srt_clock(s)} --> {srt_clock(e)}\n{t}' for i,(s,e,t) in enumerate(cues,1))+'\n',encoding='utf-8')
    return len(cues)


def export(actions,voice,rate,encoder):
    videos=CACHE/'videos.ffconcat';audios=CACHE/'audio.ffconcat'
    concat_file(videos,actions,'rendered_video');concat_file(audios,actions,'rendered_audio')
    subtitles=OUTPUT/f'{NAME}.srt';cue_count=write_subtitles(actions,subtitles)
    chapters=CACHE/'chapters.ffmetadata'
    def escape(text):return text.replace('\\','\\\\').replace('=','\\=').replace(';','\\;').replace('#','\\#').replace('\n',' ')
    metadata=[';FFMETADATA1','title=Quantum Stochastic Inflation — AI-narrated short presentation',
              'artist=Robson Christie','comment=AI-generated British English male narration; '+voice]
    for action in actions:
        metadata+=['[CHAPTER]','TIMEBASE=1/1000',f'START={round(action["start"]*1000)}',
                   f'END={round(action["end"]*1000)}',f'title={action["action"]:02} — {escape(action["title"])}']
    chapters.write_text('\n'.join(metadata)+'\n',encoding='utf-8')
    final=OUTPUT/f'{NAME}.mp4';temporary=OUTPUT/f'{NAME}.tmp.mp4'
    run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(videos),
         '-f','concat','-safe','0','-i',str(audios),'-i',str(subtitles),'-i',str(chapters),
         '-map','0:v:0','-map','1:a:0','-map','2:0','-map_metadata','3','-map_chapters','3',
         '-c:v','copy','-c:a','aac','-b:a','128k','-c:s','mov_text','-metadata:s:s:0','language=eng',
         '-disposition:s:0','0','-t',str(actions[-1]['end']),'-movflags','+faststart',str(temporary)])
    temporary.replace(final)
    audio_only=OUTPUT/f'{NAME}.m4a'
    run(['ffmpeg','-v','error','-y','-i',str(final),'-map','0:a:0','-c:a','copy','-map_metadata','0','-map_chapters','0','-vn',str(audio_only)])
    manifest={
        'voice':voice,'rate':rate,'engine':'Microsoft Edge neural text-to-speech via edge-tts '+edge_tts.__version__,
        'ai_generated_narration':True,'encoder':encoder,'duration_seconds':actions[-1]['end'],
        'actions':[{k:v for k,v in a.items() if k not in ('boundaries','rendered_video','rendered_audio','audio','video')} for a in actions],
        'subtitle_cues':cue_count,'video':str(final),'audio':str(audio_only),'subtitles':str(subtitles),
        'script_sha256':digest(ROOT/'speaker_narration.json'),'slides_sha256':digest(ROOT/'slides/QuantumStochasticShort.json')}
    write_json(OUTPUT/'action_timing.json',manifest)
    def stamp(seconds):
        seconds=round(seconds)
        return f'{seconds//60:02}:{seconds%60:02}'
    transcript=['AI-NARRATED SHORT PRESENTATION — TIMED TRANSCRIPT',
                f'British English male synthetic voice; {voice}.',
                f'Running time: {stamp(actions[-1]["end"])}.','']
    for action in actions:
        transcript += [f'ACTION {action["action"]:03} | {stamp(action["start"])}–{stamp(action["end"])} | {action["title"]}',action['text'],'']
    (OUTPUT/'Narrated script.txt').write_text('\n'.join(transcript),encoding='utf-8')
    # One video frame = exactly 1,600 audio samples throughout the padded master.
    info=probe(final);video=next(s for s in info['streams'] if s['codec_type']=='video')
    audio=next(s for s in info['streams'] if s['codec_type']=='audio')
    assert (video['width'],video['height'])==(1920,1080)
    assert abs(float(video['duration'])-actions[-1]['end'])<.05
    assert abs(float(audio['duration'])-float(video['duration']))<.05
    chapter_info=json.loads(run(['ffprobe','-v','error','-show_chapters','-of','json',str(final)]))
    assert len(chapter_info['chapters'])==len(actions)
    print(f'Complete: {final}\nDuration: {actions[-1]["end"]/60:.2f} minutes; {len(actions)} chapters; {cue_count} subtitle cues.',flush=True)
    return manifest


async def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--voice',default='en-GB-RyanNeural')
    parser.add_argument('--rate',default='-20%')
    parser.add_argument('--jobs',type=int,default=2,choices=range(1,5))
    parser.add_argument('--encoder',choices=('auto','nvenc','cpu'),default='auto')
    args=parser.parse_args()
    CACHE.mkdir(parents=True,exist_ok=True);OUTPUT.mkdir(exist_ok=True)
    steps=json.loads((ROOT/'media/opening_steps.json').read_text())
    slides=json.loads((ROOT/'slides/QuantumStochasticShort.json').read_text())['slides']
    narration=json.loads((ROOT/'speaker_narration.json').read_text(encoding='utf-8'))
    assert len(steps)==len(slides)==ACTION_COUNT and set(narration)=={s['title'] for s in steps}
    actions=[]
    for step,slide in zip(steps,slides):
        video=(ROOT/slide['file']).resolve();assert video.is_relative_to(ROOT)
        assert slide['notes']==step['notes']
        actions.append(dict(action=step['step'],title=step['title'],text=narration[step['title']],
                            spoken=spoken_text(narration[step['title']]),video=str(video),
                            video_seconds=float(probe(video)['format']['duration'])))
    encoder=choose_encoder(args.encoder);print(f'Voice: {args.voice}; rate: {args.rate}; encoder: {encoder}',flush=True)
    semaphore=asyncio.Semaphore(args.jobs)
    spoken=await asyncio.gather(*(synthesize(a,args.voice,args.rate,semaphore) for a in actions))
    elapsed=0
    for action in spoken:
        frames=math.ceil((max(action['video_seconds'],PRE+action['speech_seconds'])+POST)*FPS)
        action.update(frames=frames,seconds=frames/FPS,start=elapsed,end=elapsed+frames/FPS)
        elapsed+=frames/FPS
    print(f'Measured narrated duration: {elapsed/60:.2f} minutes.',flush=True)
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        rendered=list(pool.map(lambda a:render_action(a,encoder),spoken))
    result=export(rendered,args.voice,args.rate,encoder)
    (OUTPUT/'README.md').write_text(
        f'# AI-narrated short presentation\n\nBritish English male neural voice: {args.voice}. '
        f'Running time: {result["duration_seconds"]/60:.1f} minutes.\n\n'
        f'The MP4 contains {ACTION_COUNT} actions with synchronized AI narration, action chapters, '
        'and an optional English subtitle track. Enable subtitles in your player if wanted. '
        'The M4A is the same narration as audio only; the SRT is provided separately.\n\n'
        'Animations retain their original speed and hold their final frame while narration finishes. '
        'The interactive long and short decks remain unchanged. '
        'See ../NARRATION.md to regenerate after editing the presentation.\n',encoding='utf-8')


if __name__=='__main__':asyncio.run(main())
