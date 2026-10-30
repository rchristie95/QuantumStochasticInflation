# Quantum Stochastic Inflation: animated opening

**Double-click `Start presentation` (the Windows shortcut) in this folder.**
It opens the presentation without a terminal window. `Launch presentation.cmd`
is an alternative launcher that uses paths relative to this folder.

The presentation source, slides, videos, review images and notes are all in
this `Presentation` folder. Its Python environment is shared from the project's
adjacent `.manim-venv` folder.

`QuantumStochasticOpening` presents 124 keyboard-controlled reveals as one talk.
History, motivation and the classical Langevin description form the opening
**Classical theory** chapter. **Toy model** follows, then **Quantum stochastic
inflation**. Their equations build over additional Right-arrow presses.
Definitions precede normalization checks,
operations precede their results, and interpretations follow the calculation.
Earlier equations stay visible while the next result is revealed. The measurement
comparison builds the Fock branch, then the position branch, then purity and the
ensemble average. `reveal_plan.json` records the complete pacing storyboard.
A small foreground counter numbers all 124 keyboard-controlled reveals.
The full-height cutoff canvas places its counter in the upper-right corner to
keep the boundary-kick equation clear.
The first two pages are the talk title (Robson Christie, collaborators,
arXiv:2606.12636 and QR code) and outline.
The three outline entries and chapter dividers are Classical theory, Toy model,
and Quantum stochastic inflation. Combining the former history and classical
chapters removes one redundant divider; the equation reveals are preserved.

The averages-versus-averages detour is removed. Toy-model headings identify the
operation on each canvas. The coordinate-matrix canvas includes a native axis
diagram for n=1; the matrix gives the scale factors. The trace stays on the Gaussian-example canvas. A separate press prepares
the integral; the next merges the retained Q and P axes while contracting
the complementary directions. Another press reveals reduced purity.

The toy model uses the average `Q_n = sum(q_j)/n` and total `P_n = sum(p_j)`.
The reversible-redefinition view shows the position matrix A_n and the momentum
coefficients directly. The next view defines U_{A_n} by its coordinate-basis action
and builds all six independent output commutators over separate presses.
The redefinition and Gaussian example use only Q_n, q_{n+1}, P_n, p_{n+1}
and the corresponding collective/complementary output names, without coordinate
aliases or another named transformation matrix.
The Gaussian example starts with an explicit 4D Wigner density and animates its symplectic
basis change through fully labelled, normalized position/momentum density maps.
The same joint function is labelled W_n joint before the coordinate change and
W_n prime joint afterwards. A fixed absolute linear density scale (0 to 1/pi)
is shared by both marginals and the actual reduced Q/P Wigner density. Action 41
expands the transformed joint Gaussian; actions 42 and 43 show the evaluated
trace, labelled W_(n+1) traced, together with its defining integral. The worked
example is n=1, while every coordinate retains its general-index name.
The joint state holds with both output modes retained. **Tracing the output
requires the next Right-arrow press.** Fock and ideal position POVMs follow.
Action 51 shows the original paper POVM figure under the title
"Measuring vs discarding the decoupled mode", with the outcome average below. Action 52 returns to the Fock/position
comparison and states the purity of recorded rank-one outcomes.
The raster is compiled from `assets/paper_povm.tex`, which inputs the paper's
original `../figures/pure_state_povm_tikz.tex` source.

The next continuous canvas compares **Master, Fock and Q** Wigner functions.
Press Right separately for the additions from one to two, three and seven
oscillators. These are computed conditional states, including Fock Wigner
negativity, not Gaussian substitutes. The selected Fock record is `(1,0,1,0,0,0)`;
the selected position record is `(0.8,-0.6,0.5,-0.4,0.3,-0.2)`. Number outcomes show probabilities;
position outcomes show the recorded position. Conditional Wigner functions integrate to one, with a common signed colour scale. Each conditional column carries
its own prior measurement record. All columns share fixed plot and colour scales.
The Master column is the discrete unconditioned reduced map with no free dynamics;
it is not a continuous-time GKLS integration. The former Gaussian-purity and
qubit sequence (old slides 11-19) has been removed.

History leads into a sharp-window definition of Q_N at the patch centre, a
stationary N=0 frame for explaining Theta, and a Right-arrow-triggered continuous
16-second cutoff animation. Ninety-six modes cross from N=0 through N=6,
including both endpoints. Five earlier modes are already retained at the start,
and five later modes remain oscillating outside the cutoff at the end. The
initial long field includes the retained modes. Crossing amplitudes supply the
matching signed kicks below, on a fixed vertical field scale. No spatial argument, plane-wave phase or momentum
variable appears in this definition. The former why-it-matters view is removed.
The old comoving-mode/shell-crossing demonstration and separate single-path
buildup are also removed. The ensemble view introduces its highlighted path
directly in the original draft; the redundant ensemble canvas has now also been removed.
The following canvas reveals the O(sigma^2) gradient suppression, conditions for
local homogeneous evolution, and a patchwork inside today's Hubble volume.
Its scale comparison uses comoving lengths of late-inflation regions; local
evolution allows inherited correlations. Slow roll is identified as an extra
approximation. The history timeline gives one
contribution bullet per paper, with its publication reference; citation-count
labels and portraits are omitted. The final quantum
chapter derives canonical variables from the field Lagrangian and the boundary
channel, connects to conditional output readout, and ends with massive-spectator
covariance and purity evolution. Allow approximately 30-35 minutes with the synchronized script;
presentation pauses control the duration.

`oscillator_states.py` generates `assets/oscillator_wigner/` with actual Wigner
grids, a manifest and the recorded probabilities. Rendering refreshes these
assets if their numerical source changes. `verify_physics.py` checks the canonical
map, full-state purity, Fock completeness, position conditioning and Wigner
normalization/negativity. A local image-camera compatibility class allows the
scientific raster grids with the installed Manim/Pillow versions; dependency
pins are unchanged. See `sources.md` for conventions and assumptions.
Wigner image objects carry content hashes, including after transformations, so
regenerating a PNG at the same path invalidates its affected animation clips.
The paper QR is native vector geometry and is hashed as geometry.

From this `Presentation` folder in PowerShell:

```powershell
# Numerical checks
..\.manim-venv\Scripts\python.exe verify_physics.py
..\.manim-venv\Scripts\python.exe verify_unravellings.py

# List editable sections
..\.manim-venv\Scripts\python.exe build_presentation.py --list

# Render one continuous 1080p scene, reusing Manim animation clips
..\.manim-venv\Scripts\python.exe build_presentation.py

# Quick isolated 480p content preview, leaving the final talk untouched
..\.manim-venv\Scripts\python.exe build_presentation.py --preview boundary
..\.manim-venv\Scripts\manim-slides.exe present QuantumStochasticOpening-preview

# Check whether the continuous scene needs an update
..\.manim-venv\Scripts\python.exe build_presentation.py --status

# Open the final talk (or double-click the same Start presentation shortcut)
..\.manim-venv\Scripts\manim-slides.exe present --hide-info-window QuantumStochasticOpening
```

Edit content in `sections/`; `deck.py` declares the source order. These modules
organize editing, but the final build now runs **one QuantumStochasticOpening
scene in one renderer**. Transitions operate on live Manim objects throughout.
The default build no longer restores saved section frames or assembles separately
rendered sections. The legacy `incremental_build.py` is retained for old review
artifacts and is not the default builder.

Manim still caches individual animation clips, and Manim Slides caches its
forward/reverse exports. An unchanged build starts no renderer. Keep `media/`
to preserve those caches; never routinely use `--disable_caching`. The single
continuous movie is saved under `media/c/one/f/videos/opening/1080p30/`.
The native presenter still uses keyboard-controlled forward/reverse segments.
Changing a number or live object state can invalidate subsequent animations;
this is normal Manim caching, not pixel/frame patching.

`continuous_build.py` validates reveal order and notes before publishing the
existing `slides/QuantumStochasticOpening.json`. A failed render leaves the
previous published deck usable. Logs and metadata are in
`media/build/continuous/final/`. `--force` traverses the full scene using clip
caches; `--list` lists source modules. Isolated previews do not replace the talk.
Dependency pins and both one-click launchers are unchanged.

The boundary matrix first shows Kraus blocks, then expands them directly in
A_N on a separate press, then traces the decoupled basis on another press.
The master equation repeats the full definition of A_N. All Lindblad-channel
expressions use A_N explicitly. The field POVM canvases show the paper's
normalized counting equation and homodyne SSE, with a separate reveal for each
record, drift and noise term. See `sources.md` for the equation labels and the
phase convention.

The installed presenter's default controls are:

| Key | Action |
| --- | --- |
| Right arrow | Advance; if paused mid-animation, resume first |
| Left arrow | Load the previous segment and play it forward |
| V | Play the previous transition in reverse |
| R | Replay the current segment |
| Space | Pause/resume |
| F | Toggle full screen |
| Q | Quit |

The presenter holds the completed animation until you advance. No stochastic
trajectory loops. Left navigation and reverse playback are separate actions.
To customize these bindings, run
`..\.manim-venv\Scripts\manim-slides.exe wizard`.

Each segment includes presenter notes; `media/opening_steps.json` is generated
on a final build with the section titles and notes. See `sources.md` for references
and the assumptions behind the numerical illustrations.

To show the presenter window with notes alongside the audience view:

```powershell
..\.manim-venv\Scripts\manim-slides.exe present --show-info-window QuantumStochasticOpening
```

To extract every held frame, make review contact sheets, and verify all forward
and reversed videos and presenter notes after a render:

```powershell
..\.manim-venv\Scripts\python.exe review_render.py
```

The results are written to `media/opening-review/`.

`CoarseGraining` remains the six-step installation demo:

```powershell
..\.manim-venv\Scripts\manim-slides.exe render -ql coarse_graining.py CoarseGraining
..\.manim-venv\Scripts\manim-slides.exe CoarseGraining
```

## Recreating the environment

```powershell
uv venv --python 3.13 ..\.manim-venv
uv pip install --python ..\.manim-venv\Scripts\python.exe -r requirements.txt
```

FFmpeg, LaTeX, and dvisvgm must be on PATH. The installed Manim 0.19.0 pin avoids
the `write_to_movie` API incompatibility encountered with Manim 0.22.1 and
Manim Slides 5.7.0. Qt Essentials and Addons supply the desktop presenter.

Re-render after changing the source. Generated media and the virtual environment
are ignored by Git. The source paper and the supplied reference PDF are unchanged.

The final classical ensemble canvas is removed. The QFT derivation defines total
momentum directly and uses field variables throughout, with no oscillator recap.
The short-time boundary map resolves vacuum/one-quantum operator blocks before
tracing the output. The final results show actual Wigner densities with physical
Q/P axes and a shared logarithmic colourbar, followed by the paper/contact QR
closing page. The stationary-covariance derivation canvas is removed.

## Possible cuts for a shorter seminar

These are suggestions only; they have not been removed.

- Reveals 64–66: combine the canonical quantisation recap with the Lagrangian canvas. A cosmology
  audience likely needs only Pi=a^3 Phi-dot and the equal-time field commutator.
- Reveals 70–72 and 76–78: compress the smeared-commutator calculation to one reveal, then merge the
  Fourier-window recap into the initial Q/P definitions. Keep the volume factor
  and dimensions because they explain the total momentum.
- Combine the boundary diagram's input preparation and bulk-evolution reveals.
  Preserve the redefinition, expanded block matrix and separate trace press.
- Reveals 100–105: merge “A different treatment of the output” with “Back to the boundary
  channel”; both compare discarding the mode with retaining a record.
- For a shorter toy demonstration, show n=1,2,4,7. The full n=1 through 7 sequence
  remains in this version as requested.
- Reveals 114–121: combine the mean-field evolution and mass-regime canvases. The actual Wigner
  dynamics already shows the three masses and purity comparison.

Keep the history, cutoff/kick animation, average/total canonical pair,
entangled-output trace, POVM contrast, expanded boundary blocks and final
Wigner evolution as the main narrative.

## Speaking script and current revision

`Speaking script.txt` gives spoken narration and timing cues for all 124 actions.
`speaker_narration.json` stores the prose by action title. After a render, run
`..\.manim-venv\Scripts\python.exe build_speaking_script.py` to validate against
the published action order and update timing from actual clip durations.
The estimate assumes speaking during animations and includes brief pauses;
questions are additional.

The title and closing affiliation is Pusan National University, South Korea.
Recurring talk-name footers are removed. The cutoff demonstration has no
heading above its field definition. Action 13 uses circular regions.
Actions 42-44 prepare, execute and interpret the partial trace on one canvas.
The right marginal has complementary momentum horizontally, so retained
momentum becomes the merged vertical axis. The field Hamiltonian defines K
directly without the velocity relation or intermediate H_bulk/H equality.
Removing the velocity relation shifts former actions 75-125 down by one.
