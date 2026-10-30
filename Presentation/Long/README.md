# Long presentation

This is the preserved 124-action edition. Start it with
`../Start long presentation.lnk`, or use `Launch presentation.cmd` here.
The synchronized narration is `Speaking script.txt`; its estimate is about
30Ã¢â‚¬â€œ35 minutes. The separate 25-minute edition is in `../Short/`.

All long-version sources, assets, slides, videos, notes and animation caches
are contained in this folder. The shared environment is `../../.manim-venv`.
Edit `sections/`; `deck.py` declares the order and dependencies.

From this directory in PowerShell:

```powershell
# Reuse caches to render one continuous 1080p scene
..\..\.manim-venv\Scripts\python.exe build_presentation.py

# Check whether a render is needed
..\..\.manim-venv\Scripts\python.exe build_presentation.py --status

# Isolated 480p section preview; final talk stays untouched
..\..\.manim-venv\Scripts\python.exe build_presentation.py --preview boundary
..\..\.manim-venv\Scripts\manim-slides.exe present QuantumStochasticOpening-preview

# Update the speaking script after changing and rendering the deck
..\..\.manim-venv\Scripts\python.exe build_speaking_script.py

# Shared scientific and rendering regression checks
..\..\.manim-venv\Scripts\python.exe ..\tests\run_checks.py --edition long

# Review the actual rendered slides, notes, counters, QR and reverse clips
..\..\.manim-venv\Scripts\python.exe review_render.py
```

The final talk is one live Manim scene, not an assembly of section renders.
Keep `media/` to preserve animation and forward/reverse clip caches. Published
presenter configuration is `slides/QuantumStochasticOpening.json`; notes are
`media/opening_steps.json`. Logs and the current build manifest are in
`media/build/continuous/final/`. `build_utils.py` supplies atomic publication.
A failed render leaves the published deck usable.

| Key | Action |
| --- | --- |
| Right | Advance or resume the current animation |
| Left | Previous segment, played forward |
| V | Play the previous transition in reverse |
| R | Replay the current segment |
| Space | Pause/resume |
| F | Full screen |
| Q | Quit |

Each action holds until advanced. To include presenter notes, use:

```powershell
..\..\.manim-venv\Scripts\manim-slides.exe present --show-info-window QuantumStochasticOpening
```

The Wigner plots are computed normalized densities. Their physical conventions,
references and assumptions are documented in `sources.md`. The original paper
is `../../paper_v2.tex`; the POVM figure wrapper uses its original TikZ source.

Active tests live once in `../tests/`, including checks for canonical maps,
Wigner purity/normalization, unravelling algebra, image cache invalidation and
foreground rendering. Obsolete section-assembly tests, the retired builder,
installation demo and redundant standalone preview are in `Archive/retired-tools`;
they are not part of the active build or test suite.

The final Wigner/purity animation covers N=0 through N=10 e-folds.

Mass examples are m/H=1 (light), 1.5 (critical) and 2 (heavy).
