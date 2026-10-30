# Active presentation checks

Run from the `Presentation` folder:

```powershell
..\.manim-venv\Scripts\python.exe tests\run_checks.py
..\.manim-venv\Scripts\python.exe tests\run_checks.py --edition long
..\.manim-venv\Scripts\python.exe tests\run_checks.py --edition short
```

The shared suite retains:

- `verify_physics.py`: canonical normalization, symplectic maps, exact Gaussian
  expressions, Wigner normalization/purity, Fock/position conditioning and massive
  field covariance. It imports the selected edition's actual numerical helpers.
- `verify_unravellings.py`: counting/homodyne normalization and ensemble GKLS
  identities. This edition-independent operator-algebra check runs once.
- `test_image_cache.py`: changing a raster at the same asset path invalidates
  its animation hash.
- `test_foreground.py`: slide furniture survives cached/static frame composition.

Full rendered-deck review remains with each edition: `Long/review_render.py`
and `Short/review_short.py`. These inspect their own video exports and notes.

The retired section-assembly builder, its tests, installation demo and redundant
standalone preview launcher are archived under `Long/Archive/retired-tools`.
They are not part of this suite or either active build. The duplicate short
physics-check file is archived; the shared runner checks both editions instead.
Retired executables have disabled `.txt` suffixes and are excluded from test discovery.
