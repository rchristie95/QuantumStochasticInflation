"""Presentation content: connection."""
from presentation_common import *


class ConnectionSection:
    def measurement_connection(self):
        self.step("Back to the boundary channel", "Apply the earlier oscillator Fock/position readout comparison to the field model. The measured factor is the decoupled canonical mode. Its partial trace yields GKLS; efficient rank-one monitoring defines conditional trajectories for pure joint trajectories. Their ensemble mean is the reduced state. A suitable readout and the appropriate limits connect conditional centres to the Starobinsky Langevin equation.")
        self.clear_content()
        pair=self.figure_pair().shift(UP*.35)
        trace_title=text_line("Partial trace",27,MIX).move_to([-3,-.65,0])
        readout_title=text_line("Recorded rank-one readout",27,GREEN).move_to([3,-.65,0])
        master=equation(r"\rho_N=\Tr_\perp\rho_{\parallel\perp}",size=35).move_to([-3,-1.45,0])
        trajectory=equation(r"\rho_{c,r}=\ket{\psi_{c,r}}\bra{\psi_{c,r}}",size=35).move_to([3,-1.45,0])
        identity=equation(r"\mathbb E_r[\rho_{c,r}]=\rho",size=44,color=GREEN).move_to([0,-2.55,0])
        qualification=text_line("Pure joint trajectories; efficient rank-one readout",18,MUTED).move_to([0,-3.12,0])
        self.play(FadeIn(pair),FadeIn(trace_title),Write(master));self.hold()
        self.step("Follow a conditional quantum trajectory", "Efficient rank-one monitoring of pure joint trajectories gives a pure retained conditional state. Keep its outcome record, as in the oscillator example.")
        self.play(FadeIn(readout_title),Write(trajectory),FadeIn(qualification));self.hold()
        self.step("Average the conditional trajectories", "Average over the complete outcome ensemble. This recovers the reduced GKLS state; two selected sample records alone do not form that ensemble.")
        self.play(Write(identity));self.hold()
        self.field_counting_equation()
        self.field_homodyne_sse()

    def field_counting_equation(self):
        self.step("Field POVM: count the decoupled quanta", "Paper Appendix, Jump unravelling, CountingPOVMApp through JumpSMEApp. Display the Fock effects of the complete counting POVM. Vacuum and one-count outcomes suffice through order dN. Every occurrence of the paper's jump operator is explicitly replaced by sqrt(3) A_N. The fixed overall phase drops out of counting dynamics.")
        self.section(3,"Fock readout gives quantum jumps")
        povm=equation(r"\Pi_j=\ket j_\perp\bra j,\quad j=0,1,\ldots",size=35,color=SHELL).move_to([0,2.05,0])
        rate=equation(r"\nu_c=3\langle A_N^\dagger A_N\rangle_c,\qquad"
                      r"\mathbb E[dJ\mid\rho_c]=\nu_c\,dN,\quad(dJ)^2=dJ",size=31).move_to([0,.95,0])
        drift=equation(r"d\rho_c=\left(-i[K_{\rm eff},\rho_c]-\frac32\{A_N^\dagger A_N,\rho_c\}"
                       r"+\nu_c\rho_c\right)dN",size=32).move_to([0,-.35,0])
        jump=equation(r"\hspace{1cm}+\left(\frac{A_N\rho_c A_N^\dagger}{\langle A_N^\dagger A_N\rangle_c}"
                      r"-\rho_c\right)dJ",size=34,color=GREEN).move_to([0,-1.7,0])
        caption=text_line("No count: normalized drift. Count: a recorded state update.",23,MUTED).move_to([0,-2.85,0])
        self.play(Write(povm));self.hold()
        self.step("The conditional count rate", "Define nu_c as the conditional intensity, not a new operator. dJ is zero or one and has conditional expectation nu_c dN. When the intensity is zero no count occurs; the normalized jump expression is used only on a nonzero-probability branch.")
        self.play(Write(rate));self.hold()
        self.step("Evolve between recorded counts", "First reveal the normalized deterministic part of the paper's JumpSMEApp: Hamiltonian drift, no-count anticommutator and the state-dependent normalization correction. The stochastic count update follows on the next press.")
        self.play(Write(drift));self.hold()
        self.step("Apply the recorded quantum jump", "Complete JumpSMEApp with the count update. Efficient Fock readout preserves conditional purity for pure joint input. Substituting E[dJ|rho_c]=3<A_N-dagger A_N>_c dN recovers the same unconditional GKLS generator after ensemble averaging.")
        self.play(Write(jump),FadeIn(caption));self.hold()

    def field_homodyne_sse(self):
        self.step("Field POVM: read one decoupled quadrature", "Paper Appendix Homodyne unravelling, HomodyneRecordPOVMApp and homodyneSSEshort. The quadrature's rank-one spectral measure defines a continuous POVM. The phase chi selects the read quadrature; choose a fixed phase convention for A_N. The paper's phase-rotated jump operator is explicitly sqrt(3) exp(i chi) A_N throughout this slide.")
        self.section(3,"Quadrature readout gives a diffusive SSE")
        povm=equation(r"\Pi_\chi(y)\,dy=\ket{y;\chi}_\perp\bra{y;\chi}\,dy,\qquad"
                      r"\int\Pi_\chi(y)\,dy=I",size=29,color=SHELL).move_to([0,2.1,0])
        mean=equation(r"x_c=\sqrt3\,\langle e^{i\chi}A_N+e^{-i\chi}A_N^\dagger\rangle_c",size=31).move_to([0,1.15,0])
        record=equation(r"dY_\chi=x_c\,dN+dW_\chi,\qquad(dW_\chi)^2=dN",size=31,color=GREEN).move_to([0,.2,0])
        drift=equation(r"d\ket{\psi_c}=\left[-iK_{\rm eff}-\frac32 A_N^\dagger A_N"
                       r"+\frac{\sqrt3}{2}x_c e^{i\chi}A_N-\frac{x_c^2}{8}\right]\ket{\psi_c}\,dN",size=31).move_to([0,-1.05,0])
        noise=equation(r"\hspace{1cm}+\left(\sqrt3 e^{i\chi}A_N-\frac{x_c}{2}\right)"
                       r"\ket{\psi_c}\,dW_\chi",size=33,color=GREEN).move_to([0,-2.05,0])
        average=equation(r"\mathbb E[\ket{\psi_c}\bra{\psi_c}]=\rho_N",size=28).move_to([0,-2.95,0])
        self.play(Write(povm),Write(mean));self.hold()
        self.step("A quadrature record has a Wiener innovation", "y denotes the dimensionless eigenvalue of the signed decoupled quadrature, with y=dY_chi/sqrt(dN), as in the paper. x_c is its conditional bulk signal, not an independent dynamical variable. dW_chi is the innovations Wiener increment.")
        self.play(Write(record));self.hold()
        self.step("The normalized stochastic Schrodinger drift", "The normalized pure-state homodyne SSE from homodyneSSEshort, with L_chi replaced everywhere by sqrt(3) exp(i chi) A_N: -iK_eff -(3/2)A_N-dagger A_N +(sqrt(3)/2)x_c exp(i chi) A_N -x_c squared/8. The scalar terms ensure norm preservation together with the Ito noise correction.")
        self.play(Write(drift));self.hold()
        self.step("Complete the diffusive pure-state equation", "Add (sqrt(3) exp(i chi) A_N - x_c/2)|psi_c> dW_chi. This is the efficient rank-one, recorded-quadrature unravelling of the same GKLS evolution. It preserves pure conditional states for pure input, and the complete ensemble average returns rho_N. No physical detector is asserted as part of the inflationary theory.")
        self.play(Write(noise),Write(average));self.hold()

