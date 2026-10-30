# Presentation authoring workflow

- Edit the relevant content module in `sections/`. Shared visual helpers live in
  `presentation_common.py`; section order/dependencies are declared in `deck.py`.
- Use `..\.manim-venv\Scripts\python.exe build_presentation.py` for revisions.
  The user explicitly requested a single continuous scene on 2026-10-29 because
  separately rendered sections caused transition problems. Source remains in
  section modules, but the default builder renders one live object graph without
  frozen incoming frames. Do not switch back to section assembly by default.
- Manim animation caching remains enabled; never routinely use --disable_caching.
  An unchanged build launches no renderer. Keep `media/` to retain clip caches.
- The user explicitly requested restoring slide numbers. A foreground counter
  numbers each reveal. Keep it out of clear_content fades and native plot rasters.
- Keep `Start presentation.lnk` and `Launch presentation.cmd` working as before.
  Preserve final forward/reverse playback and presenter pauses.
- Manim omits image pixel arrays from clip hashes. Use the content-digested
  `wigner_image` factory for numerical rasters and update the digest after image
  transforms. Incoming frozen frames already carry their immutable image hash.
- Keep a separate Right-arrow pause between definitions, operations, intermediate
  results, and interpretations. Keep prior equations visible on the same canvas.
  Treat `reveal_plan.json` as the pacing storyboard and update it when adding or
  removing reveals. Preserve one press per oscillator addition in the Wigner demo.
