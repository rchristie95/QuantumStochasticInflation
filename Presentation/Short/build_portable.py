"""Package the rendered talk for offline browser playback, without Python setup."""
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent


def main():
    slides = json.loads((ROOT / 'slides/QuantumStochasticShort.json').read_text())['slides']
    target = ROOT / 'Portable'
    (target / 'clips').mkdir(parents=True, exist_ok=True)
    playlist = []
    for i, slide in enumerate(slides, 1):
        entry = {}
        for key, suffix in [('file', ''), ('rev_file', '-reverse')]:
            source = ROOT / slide[key]
            filename = f'clips/{i:03}{suffix}.mp4'
            shutil.copy2(source, target / filename)
            entry[key] = filename
        playlist.append(entry)
    template = (ROOT / 'portable_player.html').read_text(encoding='utf-8')
    (target / 'index.html').write_text(template.replace('__PLAYLIST__', json.dumps(playlist)), encoding='utf-8')
    print(f'Packaged {len(slides)} reveals with forward/reverse clips in {target}')


if __name__ == '__main__':
    main()
