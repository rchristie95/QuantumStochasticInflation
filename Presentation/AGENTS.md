# Presentation authoring workflow

- Long and short materials live in `Long/` and `Short/`. Work inside the intended
  edition; edit `sections/`, `presentation_common.py`, and `deck.py` there.
- Speaking scripts can contain the user's manual edits. Treat their current prose
  as authoritative. Preserve a backup before changing a script, merge only the
  requested changes, and generate candidates separately instead of overwriting
  an existing authored script. Action renumbering must preserve the user's prose.
- From an edition folder use
  `..\..\.manim-venv\Scripts\python.exe build_presentation.py` for revisions.
  The user explicitly requested a single continuous scene on 2026-10-29 because
  separately rendered sections caused transition problems. Source remains in
  section modules, but the default builder renders one live object graph without
  frozen incoming frames. Do not switch back to section assembly by default.
- Manim animation caching remains enabled; never routinely use --disable_caching.
  An unchanged build launches no renderer. Keep `media/` to retain clip caches.
- The user explicitly requested restoring slide numbers. A foreground counter
  numbers each reveal. Keep it out of clear_content fades and native plot rasters.
  For the Short edition, the user subsequently requested one number per slide/topic,
  held fixed through its reveals. Use Short/slide_numbering.py for these boundaries
  in both the presentation and script. The short script has slide cues only.
- Keep `Start long presentation.lnk` and `Start short presentation.lnk` in the
  top-level Presentation folder. Each edition has its own `Launch presentation.cmd`.
  Preserve final forward/reverse playback and presenter pauses.
- Manim omits image pixel arrays from clip hashes. Use the content-digested
  `wigner_image` factory for numerical rasters and update the digest after image
  transforms. Incoming frozen frames already carry their immutable image hash.
- Keep a separate Right-arrow pause between definitions, operations, intermediate
  results, and interpretations. Keep prior equations visible on the same canvas.
  Treat `reveal_plan.json` as the pacing storyboard and update it when adding or
  removing reveals. Preserve one press per oscillator addition in the Wigner demo.
- Active shared checks live in `tests/`; run them with
  `..\.manim-venv\Scripts\python.exe tests\run_checks.py` from Presentation.
  `Long/Archive/retired-tools` is historical and is not an active build or test suite.
