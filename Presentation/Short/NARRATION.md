# Narrated short presentation

The generated video, audio-only version, subtitles and measured action timings
are in `Narrated/`, together with `Narrated script.txt` using the video's actual
action timings. The narration is synthetic British English male speech
(`en-GB-RyanNeural`), generated from `speaker_narration.json`.

From this folder:

```powershell
uv pip install --python ../../.manim-venv/Scripts/python.exe -r requirements-narration.txt
../../.manim-venv/Scripts/python.exe build_narrated.py
```

The export uses the published forward clips from the single continuous scene.
It preserves animation speed and pads each action with its held final frame.
Narration begins half a second into the action and leaves 2.5 seconds afterward.
Video holds and PCM audio are matched exactly at 30 frames / 48,000 samples per
second before one final audio encode. Chapters and subtitles use the same clock.

Voice, pace and encoder can be changed with `--voice`, `--rate=-20%`, and
`--encoder auto|nvenc|cpu`. The default encoder uses NVIDIA hardware if available
and otherwise falls back to CPU. Speech and action video caches are kept in
`media/narration/`; unchanged text is not sent to the speech service again.

This optional export uses Microsoft's online neural speech service through
[edge-tts](https://github.com/rany2/edge-tts). It does not clone the presenter's
voice. The original speaking script and interactive decks are preserved.
