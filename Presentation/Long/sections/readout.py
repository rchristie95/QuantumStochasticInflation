"""Presentation content: readout."""
from presentation_common import *
from hashlib import sha256


class ReadoutSection:
    def collective_povms(self):
        self.step("Fock and position readout", "Return to the same pre-trace pure joint output on separate trials. Fock readout is the rank-one number-basis PVM E_m=|m><m| of the dimensionless complementary canonical pair (R,P_R), with annihilator (R+iP_R)/sqrt(2). Position readout is the ideal continuous quadrature PVM density E_r=|r><r|, a generalized rank-one readout: position eigenstates are not normalizable. Its outcome has a probability density, not a finite point probability. The conditional amplitude is the Fock overlap integral or the position slice Psi(Q,r), respectively. Both are pure when the joint input is pure and the ideal outcome record is kept. Summing or integrating all outcomes gives the same reduced state as the partial trace. Finite position bins with discarded sub-bin information need not leave a pure conditional state.")
        self.section(2,"Fock or position readout: keep the outcome")
        heads=VGroup(text_line("Fock POVM",29,SHELL).move_to([-3.2,2.25,0]),text_line("Position POVM",29,GREEN).move_to([3.2,2.25,0]))
        effects=VGroup(equation(r"E_m=|m\rangle_\perp\langle m|",size=36,color=SHELL).move_to([-3.2,1.45,0]),equation(r"E_r=|r\rangle_\perp\langle r|",size=36,color=GREEN).move_to([3.2,1.45,0]))
        complete=VGroup(equation(r"\sum_{m=0}^{\infty}E_m=I_\perp",size=32).move_to([-3.2,.55,0]),equation(r"\int_{\mathbb R}dr\,E_r=I_\perp",size=32).move_to([3.2,.55,0]))
        conditional=VGroup(equation(r"\psi_m(Q)\propto\int dR\,\varphi_m^*(R)\Psi(Q,R)",size=30,width=5.8).move_to([-3.2,-.48,0]),equation(r"\psi_r(Q)\propto\Psi(Q,r)",size=32,width=5.8).move_to([3.2,-.48,0]))
        outcomes=VGroup(text_line("Discrete number outcome m",21,SHELL).move_to([-3.2,-1.1,0]),text_line("Continuous position outcome r",21,GREEN).move_to([3.2,-1.1,0]))
        purity=equation(r"\Tr\rho_{+|m}^2=\Tr\rho_{+|r}^2=1",size=35).move_to([0,-1.87,0])
        average=equation(r"\sum_m p_m\rho_{+|m}=\int dr\,p(r)\rho_{+|r}=\rho_+",size=34,color=MIX).move_to([0,-2.65,0])
        caveat=text_line("Pure joint input; ideal recorded readout. Position kets are generalized.",18,MUTED).move_to([0,-3.18,0])
        self.play(FadeIn(heads),Write(effects[0]));self.hold()
        self.step("Fock effects resolve the identity", "The number eigenstates form a complete orthonormal basis of the complementary oscillator. These rank-one effects are a projective special case of a POVM.")
        self.play(Write(complete[0]));self.hold()
        self.step("Condition on a recorded Fock outcome", "Project the joint wavefunction onto the measured number state. The overlap gives the retained conditional amplitude; the outcome m is discrete.")
        self.play(Write(conditional[0]),FadeIn(outcomes[0]));self.hold()
        self.step("An alternative position readout", "On another copy of the same joint state, use the ideal continuous position PVM. Position eigenkets are generalized, not normalizable states.")
        self.play(Write(effects[1]));self.hold()
        self.step("Position completeness uses an integral", "The continuous effects resolve the identity by integration. A single ideal position outcome is described by a probability density.")
        self.play(Write(complete[1]));self.hold()
        self.step("Condition on a recorded position outcome", "A position readout takes a slice of the joint wavefunction. Compare this with the Fock overlap integral already visible on the left.")
        self.play(Write(conditional[1]),FadeIn(outcomes[1]));self.hold()
        self.step("Measuring vs discarding the decoupled mode", "Original paper figure: paper_v2.tex, Fig. PureStatePOVM, from figures/pure_state_povm_tikz.tex. The same entangling redefinition is followed by efficient rank-one readout of the decoupled mode. For a pure joint trajectory, recording outcome r gives a pure conditioned bulk state. Sum the Fock-conditioned states with their probabilities or integrate the position-conditioned states with their density: both averages equal the reduced state produced by partial tracing.")
        self.section(2,"Measuring vs discarding the decoupled mode")
        path=ASSET_DIR/'paper_povm.png'
        figure=ImageMobject(str(path)).scale_to_fit_width(12.4).move_to([0,.55,0])
        figure.asset_content_digest=sha256(path.read_bytes()).hexdigest()
        average.move_to([0,-2.05,0])
        caption=text_line("Unrecorded outcomes: the decoupled mode is traced out",23,MUTED).move_to([0,-2.83,0])
        self.play(FadeIn(figure),run_time=.8)
        self.play(Write(average),FadeIn(caption));self.hold()
        self.step("Recorded rank-one outcomes preserve purity", "Return to the Fock and position readouts after the paper's POVM comparison. For a pure joint input and ideal efficient rank-one readout, the retained conditional state is pure. Keep the outcome record. Finite unresolved position bins need not preserve purity.")
        self.section(2,"Fock or position readout: keep the outcome")
        self.play(FadeIn(heads),FadeIn(effects),FadeIn(complete),FadeIn(conditional),FadeIn(outcomes),run_time=.6)
        self.play(Write(purity),FadeIn(caveat));self.hold()

