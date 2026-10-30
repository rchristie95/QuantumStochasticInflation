"""Synchronize authored narration with the published action order and clip timings."""
from pathlib import Path
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parent


def main():
    plan = json.loads((ROOT / 'reveal_plan.json').read_text())
    titles = [title for anchor in plan['original_topic_order']
              for title in plan['reveal_sequences'][anchor]]
    narration = json.loads((ROOT / 'speaker_narration.json').read_text(encoding='utf-8'))
    assert set(titles) == set(narration), 'Narration and storyboard differ'
    steps = json.loads((ROOT / 'media/opening_steps.json').read_text())
    slides = json.loads((ROOT / 'slides/QuantumStochasticOpening.json').read_text())['slides']
    assert titles == [step['title'] for step in steps]
    assert len(slides) == len(titles) == plan['expected_steps']
    durations = []
    for slide in slides:
        result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries',
            'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1',
            str(ROOT / slide['file'])], capture_output=True, text=True, check=True)
        durations.append(float(result.stdout))
    words = [len(re.findall(r"\b[\w'-]+\b", narration[t])) for t in titles]
    # Speak during animation; reserve three seconds per action for pointing/reading.
    def estimate(rate):
        return sum(max(w * 60 / rate, d) + 3 for w, d in zip(words, durations))
    def clock(seconds):
        return f'{int(seconds)//60:02}:{int(seconds)%60:02}'
    lines = ['QUANTUM STOCHASTIC INFLATION — SPEAKING SCRIPT',
        'Robson Christie | Pusan National University, South Korea', '',
        f'{len(titles)} actions; {sum(words):,} spoken words.',
        f'Estimated delivery: {estimate(135)/60:.1f}–{estimate(110)/60:.1f} minutes, excluding questions.',
        'Allow approximately 30–35 minutes in the programme, including brief pauses.',
        'Timestamps below use 125 words/minute, speaking during animations, plus',
        'three seconds per action for pointing, equation reading and advancing.',
        'Action 1 is the opening state. Press Right once for each subsequent action.',
        'Read only the quoted prose aloud; headings and timestamps are cues.',
        'Pause longer where needed; the audience controls no automatic timer.', '',
        'The removed momentum/velocity action shifts old actions 75–125 down by one.',
        'Trace preparation is action 42; merging/trace is 43; reduced purity is 44.', '']
    elapsed = 0
    for i, (title, count, duration) in enumerate(zip(titles, words, durations), 1):
        seconds = max(count * 60 / 125, duration) + 3
        lines += [f'ACTION {i:03} | {clock(elapsed)}–{clock(elapsed+seconds)} | {title}',
                  f'"{narration[title]}"', '']
        elapsed += seconds
    (ROOT / 'Speaking script.txt').write_text('\n'.join(lines), encoding='utf-8')
    print(f'Validated {len(titles)} actions; {sum(words)} words; '
          f'{estimate(135)/60:.1f}–{estimate(110)/60:.1f} minutes.')


if __name__ == '__main__':
    main()
