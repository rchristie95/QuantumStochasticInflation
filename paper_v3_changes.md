# paper_v3 revision notes

The new draft retains the existing article's structure and prose. `2424` of the `2474` original source lines remain verbatim. `paper_v2.tex`, its bibliography and its figures are unchanged.

## Substantive additions

- Section 4 retains the full spatial-gradient hierarchy, orthonormalises its canonical partners, and gives the finite-projection single-input GKLS generator and complete-positivity identity.
- Eliminating the complementary radial modes gives a memory equation, including correlated shell noise and initial patch/complement correlations. The paper distinguishes evolution from a specified full band state from a universal channel on an arbitrary patch state.
- A Hankel-function propagator evolves each incoming shell with its redshifting physical momentum. This gives exact window covariances without a finite hierarchy truncation.
- The massless check includes both momentum and mixed moments, the gradient-force variance balance, an explicit infrared prescription and the late-time Gaussian purity.
- Section 5.4 compares the full stationary covariance and purity against the homogeneous model, including the noncommuting stationary and massless limits.

## Targeted corrections

The abstract, introduction, bulk approximation, summary and appendices now distinguish exact canonical/shell statements from homogeneous closure. The light-shell QP and PP diffusion coefficients were corrected to the paper's canonical normalization. Existing heatmaps remain homogeneous-model results; the caption's statement that field variance diverges as the cutoff decreases at fixed positive mass was corrected. Critical/heavy limiting purities survive the comparison, but finite-cutoff corrections and homogeneous relaxation rates are scoped accordingly.

## Verification

Run from the repository root:

```bash
python3 codes_stochastic_inflation/validate_paper_v3_gradients.py
python3 codes_stochastic_inflation/validate_paper_v3_propagator.py
latexmk -pdf -interaction=nonstopmode -halt-on-error paper_v3.tex
```

The scripts require NumPy, SciPy, SymPy and mpmath. Results are saved in `codes_stochastic_inflation/paper_v3_gradient_validation.json`.

- Exact symbolic checks: five orthonormal polynomial modes, canonical commutator balance, and massless PP/QP/gradient-force integrals.
- Nine massive cases: 40-digit mode integration versus independent ODE propagation of all three covariance entries. Maximum relative discrepancy: `1.9e-13`. Homogeneous purities also use 40-digit covariance arithmetic to handle determinant cancellation.
- Eighteen explicit Hankel propagator checks, for real and imaginary orders: maximum relative matrix discrepancy `5.23e-11`.
- Three finite-time massless covariance checks: maximum relative discrepancy `5.54e-14`.
- LaTeX compilation and bibliography resolved; no undefined references/citations or overfull boxes. The PDF was rendered and visually inspected.

The numerical tail in the independent ODE check drops the exponentially small gradient coefficient after 20 e-folds and repeats at 24; the direct mode integral is independent of that approximation. No finite polynomial truncation is used for the reported full-window predictions. Its accuracy is not inferred from complete positivity.

Original `paper_v2.tex` SHA-256: `7f5900806c9ca4bc23bcd01049c702c7eb8fbae4e331f366e6bf8a0e84868198`.
