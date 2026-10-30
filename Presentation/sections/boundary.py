"""Presentation content: boundary."""
from presentation_common import *

ADAPTED_MODE = (r"A_N=i\left[\frac{\phi_{k_\sigma}^*}{\sqrt{V_{\rm com}}}\hat P_N"
                r"-\sqrt{V_{\rm com}}\,\pi_{k_\sigma}^*\hat Q_N\right]")


class BoundarySection:
    def formulation(self):
        if os.environ.get("QSI_BOUNDARY_BLOCK_ONLY")=="1":
            self.kraus_block_trace()
            return
        if os.environ.get("QSI_GKLS_FIRST_ONLY")=="1":
            self.gkls_channel()
            return
        self.step("Bulk and boundary shell", "Three minutes. Figure 1 is reconstructed using editable Manim objects. The full IR Fock space contains a collective factor and a complement. Only the collective bulk and one active collective shell input enter this diagram.")
        self.section(3,"The quantum boundary map")
        factor=equation(r"\mathcal F_N=\mathcal F_N^\parallel\otimes\mathcal F_N^\perp",size=35).move_to([0,2.15,0])
        bulk=self.mode_card(-3,.5,BULK,"Incoming bulk",r"\rho_N")
        shell=self.mode_card(3,.5,SHELL,"Incoming vacuum shell",r"\ket0_\Delta")
        product=equation(r"\rho_N\otimes\ket0_\Delta\bra0",size=38).move_to([0,-1.7,0])
        self.play(Write(factor));self.hold()
        if os.environ.get("QSI_BOUNDARY_INPUT_ONLY")=="1":return
        self.step("Select the collective bulk and shell inputs", "The full infrared sector has more degrees of freedom than its retained collective oscillator. The diagram now selects that oscillator and the active collective shell input.")
        self.play(FadeIn(bulk),FadeIn(shell));self.hold()
        self.step("Prepare a product with the vacuum shell", "Before evolution and redefinition, the retained bulk and fresh vacuum shell form the displayed product state.")
        self.play(Write(product));self.hold()

        self.step("Incoming-bulk evolution", "First evolve the already retained bulk. This internal unitary precedes the addition and redefinition of the shell.")
        unitary=equation(r"U_{\rm bulk}=e^{-iK_{\rm IR}^{\parallel}dN}",size=35).move_to([0,1.35,0])
        evolved=equation(r"U_{\rm bulk}\rho_NU_{\rm bulk}^\dagger\otimes\ket0_\Delta\bra0",size=36).move_to(product)
        phase_marker=Dot(bulk[0].get_center()+RIGHT*.57,radius=.05,color=BULK)
        self.play(Write(unitary));self.hold()
        self.step("Apply the incoming-bulk unitary", "Conjugate only the retained bulk state. The fresh shell is still in its incoming vacuum state.")
        self.play(FadeIn(phase_marker),Transform(product,evolved))
        self.play(Rotate(phase_marker,angle=PI/3,about_point=bulk[0].get_center()),run_time=1)
        self.hold()

        self.step("Entangling redefinition", "The complete V includes incoming-bulk dynamics and the redefinition. In general the two outgoing factors are entangled. Decoupled refers to the mode factor, not statistical independence.")
        pair=self.figure_pair()
        mapping=equation(r"\mathcal F_N^\parallel\otimes\mathcal F_\Delta^\parallel"
                        r"\xrightarrow{\ V_{N+dN}\ }\mathcal F_{N+dN}^\parallel\otimes\mathcal F_{N+dN}^{\mathrm d,\perp}",size=32).move_to([0,-1.3,0])
        self.play(FadeOut(factor),FadeOut(unitary),FadeOut(product),FadeOut(phase_marker),
                  Transform(bulk,pair[0]),Transform(shell,pair[1]),
                  GrowFromCenter(pair[2]),FadeIn(pair[3]),run_time=1.6)
        self.remove(bulk,shell,pair[2],pair[3])
        self.add(pair)
        self.hold()
        self.step("Identify the redefined Hilbert-space factors", "The complete V maps the incoming collective factors to the retained collective factor and decoupled output factor. Decoupled does not mean statistically independent.")
        self.play(Write(mapping));self.hold()

        self.step("Tracing the decoupled mode", "Non-unitarity appears in the reduced description when the decoupled output is traced. This is not tracing away the incoming shell before the redefinition.")
        trace=equation(r"\rho_{N+dN}=\Tr_{\mathrm d,\perp}\!\left[V_{N+dN}"
                       r"(\rho_N\otimes\ket0_\Delta\bra0)V_{N+dN}^\dagger\right]",size=33).move_to([0,-2.2,0])
        self.play(pair[1].animate.set_opacity(.3),pair[2].animate.set_opacity(.2),pair[3].animate.set_opacity(.2),Write(trace))
        self.play(Indicate(pair[0],color=MIX));self.hold()

        self.step("The single boundary-adapted channel", "Only one collective vacuum shell input couples to the retained homogeneous pair. Its mode functions define the adapted annihilation operator; the Wronskian and the normalized commutator give [A,A-dagger]=1.")
        self.clear_content()
        adapted=equation(ADAPTED_MODE,size=38).move_to([0,1.3,0])
        wronskian=equation(r"\phi_k\pi_k^*-\phi_k^*\pi_k=i\quad\Longrightarrow\quad[A_N,A_N^\dagger]=1",size=35).move_to([0,-.2,0])
        lindblad=equation(r"\text{Channel strength: }\sqrt3\,A_N",size=38,color=SHELL).move_to([0,-1.65,0])
        self.play(Write(adapted));self.hold()
        self.step("Normalize the boundary-adapted oscillator", "Use the mode-function Wronskian and the normalized Q,P algebra. Together they give the annihilator commutator equal to one.")
        self.play(Write(wronskian));self.hold()
        self.step("Identify the single Lindblad operator", "The one active vacuum shell oscillator defines one non-Hermitian channel. Coefficients are identified here without deriving their detailed mode dependence.")
        self.play(Write(lindblad));self.hold()

        self.step("From the short-time map to GKLS", "Expand the vacuum-input map in zero- and one-quantum Kraus operators to first order in dN. The no-event term contains the normalization correction; combining both terms yields the dissipator. These Kraus labels are an algebraic expansion, not a claim that a detector has been installed.")
        self.clear_content()
        kraus=equation(r"M_0=I-\left(iK_{\rm eff}+\frac32A_N^\dagger A_N\right)dN,",r"\qquad M_1=-\sqrt{3\,dN}\,A_N",size=34).move_to([0,1.45,0])
        complete=equation(r"\sum_r M_r^\dagger M_r=I+O(dN^2)",size=36).move_to([0,.05,0])
        evolution=equation(r"\rho_{N+dN}=\sum_rM_r\rho_NM_r^\dagger=\rho_N+dN\,\mathcal L(\rho_N)+O(dN^2)",size=33).move_to([0,-1.45,0])
        self.play(Write(kraus[0]));self.hold()
        self.step("Include the one-quantum Kraus contribution", "The second Kraus term is order square root of dN, so its density-matrix contribution is first order in dN. These algebraic labels do not assert a physical detector.")
        self.play(Write(kraus[1]));self.hold()
        self.step("Check trace preservation to first order", "The no-event normalization correction and the one-quantum contribution cancel in the Kraus completeness relation at order dN.")
        self.play(Write(complete));self.hold()
        self.kraus_block_trace()
        self.gkls_channel()

        self.step("A different treatment of the output", "Recall the earlier oscillator Fock and position readouts. Instead of discarding the record, condition on a rank-one measurement of the decoupled mode. The measurement is an unravelling, not an extra detector asserted by the theory.")
        self.clear_content()
        pair=self.figure_pair()
        discard=text_line("Discard output information",25,MUTED).move_to([-3,-1.4,0])
        record=text_line("Keep a measurement record",25,GREEN).move_to([3,-1.4,0])
        unconditional=equation(r"\rho=\Tr_\perp\rho_{\parallel\perp}",size=34).move_to([-3,-2.25,0])
        conditional=equation(r"\rho_{c,r}\quad\text{given outcome }r",size=34).move_to([3,-2.25,0])
        self.play(FadeIn(pair));self.hold()
        self.step("Discard the output information", "Tracing over the output gives the unconditional retained state. No measurement record is kept in this description.")
        self.play(FadeIn(discard),Write(unconditional));self.hold()
        self.step("Alternatively retain an output record", "On a monitored branch, condition on the rank-one measurement outcome. The readout selects an unravelling of the same reduced dynamics.")
        self.play(FadeIn(record),Write(conditional));self.hold()


    def kraus_block_trace(self):
        self.step("Resolve the decoupled vacuum and one-quantum blocks", "Represent the joint output in the boundary-adapted output basis |0>_perp, |1>_perp. Block rs is M_r rho_N M_s-dagger and acts on the retained field mode. This is the vacuum/one-quantum sector relevant to the reduced map through order dN: higher diagonal populations are order dN squared. Higher-sector coherences can be order dN but vanish under the output trace; the entire joint state is not being claimed accurate to order dN squared after discarding those coherences. No detector or recorded outcome is assumed.")
        self.clear_content()
        block=Matrix([[r"M_0\rho_NM_0^\dagger",r"M_0\rho_NM_1^\dagger"],
                      [r"M_1\rho_NM_0^\dagger",r"M_1\rho_NM_1^\dagger"]],
                     h_buff=4.3,v_buff=1.25,element_to_mobject=lambda s:equation(s,size=31)).move_to([.25,.45,0])
        entries=block.get_entries()
        entries[0].set_color(GREEN);entries[3].set_color(GREEN)
        entries[1].set_color(MIX);entries[2].set_color(MIX)
        rows,cols=self.block_basis(block)
        label=text_line("Joint output in the decoupled-mode basis",22,MUTED).move_to([0,2.62,0])
        truncation=text_line("Vacuum / one-quantum sector",19,MUTED).move_to([0,-1.13,0])
        delta=equation(r"\Tr_\perp\!\left(\ket r_\perp\bra s\right)=\delta_{rs}",size=35).move_to([0,-2.15,0])
        summed=equation(r"\rho_{N+dN}=M_0\rho_NM_0^\dagger+M_1\rho_NM_1^\dagger"
                        r"=\rho_N+dN\,\mathcal L(\rho_N)+O(dN^2)",size=29).move_to([0,-2.85,0])
        self.play(FadeIn(label),Write(block),FadeIn(rows),FadeIn(cols),FadeIn(truncation));self.hold()
        self.step("Expand the joint blocks in the boundary operator", "Substitute M0 and M1 before taking the output trace, using the paper's minus sign for M1. In block 00 the bulk Hamiltonian is included: rho_N - i[K_eff,rho_N]dN - (3/2){A_N-dagger A_N,rho_N}dN. The off-diagonal blocks are -sqrt(3 dN) rho_N A_N-dagger and its adjoint; block 11 is 3 dN A_N rho_N A_N-dagger. Displayed entries keep the terms needed at Ito order. Higher-sector coherences do not contribute under the trace.")
        expanded=Matrix([[r"\begin{gathered}\rho_N-i[K_{\rm eff},\rho_N]dN\\[-2pt]-\frac32\{A_N^\dagger A_N,\rho_N\}dN\end{gathered}",
                          r"-\sqrt{3\,dN}\,\rho_N A_N^\dagger"],
                         [r"-\sqrt{3\,dN}\,A_N\rho_N",r"3\,dN\,A_N\rho_N A_N^\dagger"]],
                        h_buff=5.4,v_buff=1.65,element_to_mobject=lambda s:equation(s,size=27)).move_to([.25,.25,0])
        expanded_entries=expanded.get_entries()
        for i in (0,3):expanded_entries[i].set_color(GREEN)
        for i in (1,2):expanded_entries[i].set_color(MIX)
        newrows,newcols=self.block_basis(expanded)
        # The complete matrix and its basis labels transform together, before
        # any entry is removed by the following, separately triggered trace.
        self.play(ReplacementTransform(block,expanded),Transform(rows,newrows),Transform(cols,newcols),
                  truncation.animate.move_to([0,-1.57,0]),run_time=1.5)
        entries=expanded_entries
        self.hold()
        self.step("The partial trace removes the off-diagonal blocks", "Trace over the decoupled output only. Tr_perp(|r><s|)=delta_rs removes blocks 01 and 10 and leaves blocks 00 and 11. This is a sum of retained-mode operators, not the scalar trace of each retained-mode block. The full joint state is not projected onto a particular outcome.")
        self.play(entries[1].animate.set_opacity(.15),entries[2].animate.set_opacity(.15),
                  Circumscribe(entries[0],color=GREEN),Circumscribe(entries[3],color=GREEN),Write(delta));self.hold()
        self.step("Sum the diagonal blocks", "The two surviving blocks give M0 rho M0-dagger plus M1 rho M1-dagger. The normalization correction supplies -(3/2){A_N-dagger A_N,rho_N}; the one-quantum population supplies 3 A_N rho_N A_N-dagger. Together with the effective Hamiltonian this gives the GKLS generator.")
        self.play(Write(summed));self.hold()

    def block_basis(self,block):
        """Align basis labels outside the full matrix, even for unequal entries."""
        rows=VGroup(*[equation(fr"\ket{{{r}}}_\perp",size=27,color=SHELL).move_to(
            [block.get_left()[0]-.55,block.get_rows()[r].get_center()[1],0]) for r in range(2)])
        cols=VGroup(*[equation(fr"{{}}_\perp\bra{{{r}}}",size=27,color=SHELL).move_to(
            [block.get_columns()[r].get_center()[0],block.get_top()[1]+.36,0]) for r in range(2)])
        return rows,cols


    def gkls_channel(self):
        self.step("One quantum channel", "The continuous limit gives one non-Hermitian Lindblad operator. The effective Hamiltonian includes the redefinition term. Diffusion and damping originate in this same boundary map.")
        self.clear_content()
        gkls=equation(r"\frac{d\rho_N}{dN}=-i[K_{\rm eff},\rho_N]+3A_N\rho_N A_N^\dagger-\frac32\{A_N^\dagger A_N,\rho_N\}",size=36).move_to([0,1.9,0])
        ham=equation(r"K_{\rm eff}=\frac{\hat P_N^2}{2HV_{\rm phys}}+\frac{m^2V_{\rm phys}}{2H}\hat Q_N^2+\frac34\{\hat Q_N,\hat P_N\}",size=33).move_to([0,.55,0])
        jump=equation(ADAPTED_MODE,size=34,color=SHELL).move_to([0,-.9,0])
        comm=equation(r"[A_N,A_N^\dagger]=1",size=28,color=SHELL).move_to([0,-1.85,0])
        channel=text_line("One non-Hermitian channel: damping and diffusion",25,MIX).move_to([0,-2.7,0])
        self.play(Write(gkls));self.hold()
        if os.environ.get("QSI_GKLS_FIRST_ONLY")=="1":return
        self.step("Identify the effective Hamiltonian", "Separate the bulk oscillator terms from the anticommutator term generated by the redefinition.")
        self.play(Write(ham));self.hold()
        self.step("One non-Hermitian channel supplies damping and diffusion", "The single boundary-adapted annihilator gives the Lindblad operator already normalized above. Both effects follow from the same reduced map.")
        self.play(Write(jump),Write(comm),FadeIn(channel));self.hold()

