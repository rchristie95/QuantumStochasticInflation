# Sources and mathematical conventions

## History

- A. A. Starobinsky (1986), *Stochastic de Sitter (inflationary) stage in the early Universe*, Lect. Notes Phys. 246, 107–126. [Original text](https://inspirehep.net/files/21cef7e2d2ef50ab5ee95967bf608911), [DOI](https://doi.org/10.1007/3-540-16452-9_6).
- Y. Nambu and M. Sasaki (1988), *Stochastic Stage of an Inflationary Universe Model*, Phys. Lett. B 205, 441–446. [DOI](https://doi.org/10.1016/0370-2693(88)90974-4).
- A. A. Starobinsky and J. Yokoyama (1994), *Equilibrium state of a self-interacting scalar field in the de Sitter background*, Phys. Rev. D 50, 6357–6368. [Preprint](https://arxiv.org/abs/astro-ph/9407016), [DOI](https://doi.org/10.1103/PhysRevD.50.6357).

This short timeline follows the active paper's introduction and bibliography.
It is selective, not an exhaustive priority history. Interactions occur in the
historical context; the paper's construction here concerns a free spectator.

Each milestone has one contribution bullet rather than a citation count or portrait:

- Starobinsky (1986): quantum noise drives the large-scale Langevin evolution.
- Nambu–Sasaki (1988): phase-space analysis of relaxation toward slow roll in a
  new-inflation model with a Higgs-type potential. The statement is subject to
  the initial-condition assumptions of that paper, whose publisher abstract is
  also preserved in the [bibliographic record](https://inspirehep.net/literature/251873).
- Starobinsky–Yokoyama (1994): an equilibrium distribution for a self-interacting
  scalar field in de Sitter.

## Opening pages and motivation

The first page identifies Robson Christie as presenter and names collaborators
Jaewoo Joo, Greg Kaplanek, Vincent Vennin and David Wands, matching the local
paper and the [arXiv record](https://arxiv.org/abs/2606.12636). The QR code points
to that abstract page and is decoded during render verification. The second page
is the talk outline, not a separate collaborators page.

The method schematic describes effective stochastic dynamics for coarse-grained
long-wavelength fields; the Gaussian distribution is an illustration, not a
claim that every model has Gaussian statistics. Motivation sources are:

- Vennin & Starobinsky (2015), *Correlation Functions in Stochastic Inflation*, [arXiv:1506.04732](https://arxiv.org/abs/1506.04732): non-perturbative perturbation statistics and the classical limit.
- Starobinsky & Yokoyama (1994), above: long-time equilibrium of interacting light scalar fields in de Sitter.
- Pattison, Vennin, Assadullahi & Wands (2017), *Quantum diffusion during inflation and primordial black holes*, [arXiv:1707.00537](https://arxiv.org/abs/1707.00537): full fluctuation PDFs and applications to primordial-black-hole abundances.

The motivation slide does not assert that stochastic corrections are large in
all models or on all observed CMB scales.

## Active paper

`../../paper_v2.tex` is the authoritative source. The presentation uses its
introduction's phase-space Langevin equations, its light-field slow-roll limit,
the canonical smearing definitions in section 2, the boundary-map and effective
Hamiltonian in section 3, and the measurement discussion in Appendix B.
Figure 1 is reconstructed from `../../figures/GKLS_tikz.tex`.

Only the retained collective mode is represented as one oscillator; the entire
infrared sector is not identified with a single Fourier mode. The incoming shell
and incoming bulk are independent before the redefinition. The output that is
traced or measured is the **decoupled mode after the redefinition**.

## Collective oscillator, joint Wigner density and measurements

Presentation slides 7-10 retain the full input/output coordinate names throughout:
Q_n, q_{n+1}, P_n, p_{n+1}, Q_{n+1}, Q^perp_{n+1}, P_{n+1}, P^perp_{n+1}.
The numerical example remains n=1; its coordinate labels are not replaced by
numeric indices. The joint-state unitary is defined directly from A_n:
U_{A_n}|Q_n,q_{n+1}>=|Q_{n+1},Q^perp_{n+1}>. Because |det A_n|=1,
this basis action has no additional Jacobian normalization factor. Its wavefunction
action is Psi(Q_{n+1}+Q^perp_{n+1}/(n+1),Q_{n+1}-n Q^perp_{n+1}/(n+1)).
All six independent output commutators are displayed. Separate canonical modes
can share an entangled joint state. The partial trace on the next Right-arrow
step discards the whole oscillator (Q^perp_{n+1},P^perp_{n+1}). The fully labelled
Wigner integration is included in presenter notes. Later measurement slides and
the numerical implementation retain their shorter internal variable names.


Reference: `C:\Users\robso\Downloads\collective oscillator (2).pdf`.
The toy model retains its canonical mixing construction and Gaussian example,
using **Q_n=(sum q_j)/n, P_n=sum p_j**, with hbar=1. Averaging both gives i/n;
fixing Q as an average requires the total P for [Q,P]=i.

Adding one oscillator gives Q_plus=(n Q_n+q)/(n+1), P_plus=P_n+p.
The complement is R=Q_n-q, P_R=(P_n-n p)/(n+1).
Positions transform with A=[[n/(n+1),1/(n+1)],[1,-1]], momenta with
B=(A inverse)^T=[[1,1],[1/(n+1),-n/(n+1)]]. Thus A B^T=I and S=diag(A,B)
is symplectic. **A is not orthogonal in average/total coordinates.** Balanced
quadratures (sqrt(n) Q_n,q) and (P_n/sqrt(n),p) mix with the orthogonal
R_n=[[sqrt(n),1],[1,-sqrt(n)]]/sqrt(n+1), followed by canonical rescaling.
The corresponding joint-state unitary obeys U-dagger z U=S z; its dagger does
not replace the inverse transpose of A.

For n=1, z=(Q1,q2,P1,p2), Sigma0=diag(1,1/4,1/4,1), and
W_in=pi^-2 exp(-Q1^2/2-2q2^2-2P1^2-p2^2/2). The displayed position and
momentum ellipses are **2D marginals of one 4D Wigner density**, not four-dimensional
pictures or separate mode states. The animated symplectic path preserves the
full determinant 1/16 and purity one. Its initial fixed parity reflection acts
on an even incoming squeezed vacuum, leaving the initial state unchanged.
The final cross-mode covariance is diag(3/8,-3/8); the pure output is entangled.
A separate Right-arrow step integrates both R and P_R out of the joint Wigner
function. Retained covariance diag(5/16,5/4) has purity 4/5.

The Fock readout consists of E_m=|m><m|, m=0,1,..., for the dimensionless pair
(R,P_R), with annihilator (R+i P_R)/sqrt(2). The ideal position readout has
effect density E_r=|r><r|, integrated with dr. These are alternative PVMs and
therefore special cases of POVMs. Position eigenstates are generalized,
not normalizable rank-one vectors. Recorded outcomes are described by a density
p(r); a single exact continuous outcome does not have a finite probability.
Averaging unresolved finite bins can give mixed states. See Silva, Glancy &
Vasconcelos, *Quadrature histograms in maximum-likelihood quantum state tomography*,
Phys. Rev. A 98, 022325 (2018),
[primary article](https://pmc.ncbi.nlm.nih.gov/articles/PMC6463478/), on ideal
quadrature projectors, probability densities, and integrated finite-bin effects.

`oscillator_states.py` performs the actual amplitude transformation
Psi(Q,R)=psi_n(Q+R/(n+1)) chi(Q-nR/(n+1)). Its absolute coordinate Jacobian is one.
Each fresh chi has Var(q)=1/4, Var(p)=1; initially Var(Q1)=1, Var(P1)=1/4.
Fock conditioning integrates Psi against Hermite functions. Position conditioning
takes a slice Psi(Q,r). The selected records are m=(1,0,1) and r=(0.8,-0.6,0.5),
with each branch conditioned on its own preceding record. These are possible
illustrative histories, not typical histories or probability-weighted ensembles.
Both recorded columns remain pure. Master denotes the exact addition-only
reduced map, with covariance diag((1+(n-1)/4)/n^2,1/4+n-1); no free Hamiltonian
or continuous GKLS time discretization is included in this toy comparison.
Averaging **all** histories of either complete readout recovers that master state;
two selected histories alone do not constitute its ensemble average.

Pure Wigner functions are Fourier transforms of the full density kernels,
W(q,p)=pi^-1 integral dy exp(2ipy) psi(q-y) psi*(q+y). The computational Q grid
is [-6,6], 301 points; the relative grid is [-8,8], 801 points; the Fourier
padding is 2048. Forty-eight Fock components capture more than 0.99999 of the
probability at every selected step. Display windows are fixed at Q=[-3,3],
P=[-8,8], with a common signed colour limit +/-1/pi. Blue is positive W,
orange negative W. Display-window truncation does not enter the normalization
and purity checks on the full numerical domain. Wigner frames are interpolated
only as visual transitions between discrete additions, not as an asserted
continuous dynamics during an addition.

## Stochastic illustration

The fixed seed is 1986. In x=2 pi phi/H coordinates, use dx=-0.03 x dN+dW,
corresponding to m/H=0.30 within the displayed approximate slow-roll equation.
Euler–Maruyama uses 120 steps over six e-folds and 120 paths. The highlighted
path is exactly the first ensemble realization; 40 additional paths are shown
and all 120 terminal values enter the histogram. This illustrates the limiting
equation, not an exact finite-mass simulation of the paper's full quantum map.

## Canonical derivation and dimensions

The derivation uses 3+1 dimensions, c=hbar=1, a dimensionless scale factor and
length-valued comoving coordinates. Differentiate the coordinate Lagrangian
density a^3 L to obtain Pi=a^3 Phi-dot. For a real normalized window, the averaged
field and averaged density obey [Q,Pi-bar]=i integral(W^2)=i/Vcom. The integral
of W equals one; its squared norm generally does not. A real-space top-hat
illustrates the inverse volume; the actual sharp Fourier kernel instead gives
Vcom=6 pi^2/k_sigma^3 by Parseval.

Mass dimensions are [Q]=M, [Pi-bar]=M^2, [Vcom]=M^-3, [P]=M^-1. Keeping Q as the
physical averaged field motivates P=Vcom Pi-bar, which gives [Q,P]=i. This is a
canonical field momentum, not a particle's spatial momentum. Multiplying Q or
splitting the factor between Q and P is possible, with a consistent canonical
description. The paper itself discusses such alternative parametrizations.

The homogeneous bulk Hamiltonian excludes the moving-boundary redefinition.
That redefinition supplies the additional anticommutator in K_eff and the
single adapted channel L. The short-time M0/M1 expansion gives the GKLS generator
to first order in dN, as in the paper's boundary-map derivation.

## Massive spectator results

The final chapter uses the active paper's drift, diffusion and exact covariance
solution in section 4. Set H=1, sigma=0.1 and m/H=1,1.5,2. Evaluate the
Bunch-Davies Hankel functions at N=0, retaining the complex-index normalization
phase for heavy fields. Initial covariance is I/2 in canonical coordinates
X=sqrt(m Vphys)Q, Y=P/sqrt(m Vphys), the pure ground state of the bulk Hamiltonian
without its anticommutator term. Evolve to N=40 with the matrix-exponential
solution and solve the stationary Lyapunov equation independently of the paper's
closed-form components. Numerical checks compare those two stationary solutions,
the mode Wronskian and the uncertainty bound throughout evolution.

Contours use a separate fixed display scale in each panel, stated on screen.
Purity curves share axes and the same physical time parameter as the contours.
Displayed stationary numbers are rounded finite-sigma results, not exact
asymptotic constants; the heavy-field value can round to 1.000 without being
exactly pure. The strict m=0 case is excluded from the stationary comparison.


## Field POVM equations used on the presentation canvases

Source: `../../paper_v2.tex`, Appendix �POVM unravellings�. The counting canvas uses
CountingPOVMApp, JumpRateApp and JumpSMEApp. The quadrature canvas uses
HomodyneRecordPOVMApp and homodyneSSEshort. The original paper's jump operator
is substituted everywhere by sqrt(3) A_N, with an arbitrary fixed phase chosen
as zero; a homodyne readout then explicitly includes exp(i chi).

The counting intensity is nu_c=3<A_N-dagger A_N>_c. At a count the retained
state updates to A_N rho_c A_N-dagger / <A_N-dagger A_N>_c. The no-count drift
includes its state-dependent normalization term. The homodyne signal is
x_c=sqrt(3)<exp(i chi)A_N+exp(-i chi)A_N-dagger>_c; dY_chi=x_c dN+dW_chi.
The ket SSE follows the paper verbatim algebraically after that substitution,
including the -x_c^2/8 normalization term. x_c is a conditional expectation,
not another canonical coordinate.

The displayed expanded joint block includes the Hamiltonian in its vacuum
entry, as in FullBlockRJPOVMApp. Off-diagonal entries have the paper's negative
sqrt(3 dN) convention. Terms shown suffice for the reduced dynamics through
order dN; higher-sector coherences vanish under the decoupled-mode trace.
The field slides do not claim the entire outgoing oscillator is two-dimensional.
