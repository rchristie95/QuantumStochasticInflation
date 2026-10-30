# 25-minute version

The presentation and speaking script use 27 slide/topic numbers. Successive
reveals on the same canvas keep the same number; Right-arrow pauses remain.
`slide_numbering.py` defines the shared boundaries. The speaking script has one
heading and time range per slide, with no separate reveal cues. Script backups
are retained in `script_backups/`; generation still writes a separate candidate.

This is an independent 63-action edition. The original presentation, launcher,
124-action storyboard, and `../Long/Speaking script.txt` remain the long version.

Start this edition with `../Start short presentation.lnk` or
`Launch presentation.cmd`. Its script is `Speaking script - short.txt`.
Short actions have their own continuous numbering. `action_map.json` and the
script give the corresponding long-version action numbers.

The 2,420-word script estimates to about 23 minutes at 120 words/minute,
including three seconds per action for pointing and advancing while speaking
during animations. At 110 words/minute it estimates to 25.1 minutes.

The speaking script contains manually edited prose. The script builder preserves
that file and writes `Speaking script - short.generated.txt` for review instead.
The recovered original edited copy is in `Backups/`.

The short edition retains the cutoff sweep, canonical toy model, exact joint
Wigner densities, explicit transformed and traced Gaussians, trace-out merge,
paper POVM figure, recorded purity, two oscillator additions, field boundary
channel, GKLS equation, quadrature unravelling, and massive Wigner/purity plots.
It cites the classical sources beside their equations and condenses canonical
algebra and field derivations; omits
later oscillator additions, the full field counting equation and separate
mean-motion plots; and summarizes the Kraus/block calculation.

The oscillator additions remain separate button presses: n=1, then n=2, then
n=3. The full position and Fock Wigner assets are computed from the same
wavefunctions as the long version. No skipped addition is presented as a single
step of the short animation.

From this directory:

```powershell
..\..\.manim-venv\Scripts\python.exe build_presentation.py --draft
..\..\.manim-venv\Scripts\python.exe build_presentation.py
..\..\.manim-venv\Scripts\python.exe build_speaking_script.py
..\..\.manim-venv\Scripts\python.exe review_short.py
..\..\.manim-venv\Scripts\python.exe ..\tests\run_checks.py --edition short
```

The final render remains one continuous live Manim scene. Forward/reverse clips
and presenter notes are published only after the full scene succeeds. Caching
stays enabled. Generated media and slides remain local and are ignored by Git.

`sections/condensed.py` contains the short summary canvases. The other modules
are a separate editable source snapshot of the long talk, with the short route
declared in `deck.py`. Changes here do not edit the long talk. Numerical Wigner
and Gaussian assets retain their content digests for Manim caching.

The final Wigner/purity animation covers N=0 through N=10 e-folds.

Mass examples are m/H=1 (light), 1.5 (critical) and 2 (heavy).
