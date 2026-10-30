# Quantum Stochastic Inflation presentations

Use the two shortcuts in this folder:

| Edition | Shortcut | Script | Length |
| --- | --- | --- | --- |
| Long | `Start long presentation.lnk` | `Long/Speaking script.txt` | 124 actions |
| Short | `Start short presentation.lnk` | `Short/Speaking script - short.txt` | 63 actions; about 23 minutes |

Each edition contains its own editable sources, assets, rendered slides, videos,
presenter notes, script and build instructions. Both use the shared Python
environment at `../.manim-venv`. Their native forward/reverse playback and reveal
numbering are independent. The short script maps its actions to the long version.

The numerical and rendering regression checks live once in `tests/`:

```powershell
..\.manim-venv\Scripts\python.exe tests\run_checks.py
```

See `Long/README.md`, `Short/README.md` and `tests/README.md` for details.
Retired tooling is kept outside the active build in `Long/Archive/retired-tools`.
