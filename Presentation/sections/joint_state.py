"""Presentation content: joint state."""
from presentation_common import *


class JointStateSection:
    def gaussian_projection(self,covariance,axes,color):
        vals,vecs=np.linalg.eigh(covariance)
        a=np.linspace(0,TAU,121)
        points=2*(vecs@np.diag(np.sqrt(vals))@vecs.T)@np.array([np.cos(a),np.sin(a)])
        return VMobject(color=color,fill_color=color,fill_opacity=.18,stroke_width=3).set_points_as_corners([axes.c2p(x,y) for x,y in points.T])


    def joint_wigner_example(self):
        if os.environ.get("QSI_TRACE_ONLY")=="1":
            self.trace_collective_complement()
            return
        self.step("Product inputs become entangled outputs", "Worked example n=1, retaining general-index coordinate names throughout. Start with independent Q_n,P_n and q_{n+1},p_{n+1}, in differently squeezed pure Gaussian states. The input covariance in the displayed order Q_n,q_{n+1},P_n,p_{n+1} is diag(1,1/4,1/4,1). Its 4D Wigner function is pi^-2 exp[-Q_n^2/2-2q_{n+1}^2-2P_n^2-p_{n+1}^2/2]. The two ellipses are position and momentum marginals of that one 4D Wigner function. Animate the same canonical transformation as before; the full covariance determinant stays 1/16 and the joint purity stays one. The initial fixed parity reflection leaves the even incoming squeezed vacuum unchanged. The outputs are Q_{n+1},Q^perp_{n+1},P_{n+1},P^perp_{n+1}. Their position cross covariance is 3/8 and momentum cross covariance is -3/8. For these chosen pure inputs, the joint state is entangled between Q_{n+1} and Q^perp_{n+1}. Animate rho_n tensor rho_in becoming rho_joint under U_{A_n}. Both output modes remain present. Hold here; the next reveal presents both output portraits before a further Right-arrow press performs the partial trace.")
        self.section(2,"Independent inputs become entangled outputs")
        sigma0=np.diag([1,.25,.25,1])
        w=equation(r"W_{\rm in}(Q_n,q_{n+1},P_n,p_{n+1})=\frac1{\pi^2}e^{-Q_n^2/2-2q_{n+1}^2-2P_n^2-p_{n+1}^2/2}",size=30).move_to([0,2.23,0])
        cov=equation(r"n=1:\qquad\Sigma_{\rm in}=\operatorname{diag}(1,1/4,1/4,1)",size=29).move_to([0,1.38,0])
        axes=[];labels=[];shapes=[]
        tracker=ValueTracker(0)
        for x,indices,names,color in [(-3.3,[0,1],(r"Q_n",r"q_{n+1}"),BULK),(3.3,[2,3],(r"P_n",r"p_{n+1}"),SHELL)]:
            ax=Axes(x_range=[-3,3,1],y_range=[-3,3,1],x_length=4,y_length=2.3,tips=False).move_to([x,-.65,0])
            labels.append(VGroup(equation(names[0],size=22).next_to(ax.x_axis,RIGHT,buff=.12),equation(names[1],size=22).next_to(ax.y_axis,UP,buff=.12)))
            def projection(ax=ax,indices=indices,color=color):
                mapping=canonical_map(1,tracker.get_value())
                covariance=mapping@sigma0@mapping.T
                return self.gaussian_projection(covariance[np.ix_(indices,indices)],ax,color)
            shapes.append(always_redraw(projection));axes.append(ax)
        description=text_line("Position and momentum marginals of one 4D Wigner function",22,MUTED).move_to([0,-2.05,0])
        purity=equation(r"\rho_n\otimes\rho_{\rm in}\xrightarrow{\ U_{A_n}\ }\rho_{\rm joint},\qquad\Tr\rho_{\rm joint}^2=1",size=31,color=GREEN).move_to([0,-2.7,0])
        self.play(Write(w));self.hold()
        self.step("Specify the pure Gaussian input covariance", "Use n=1 and perpendicular pure squeezing. The four-dimensional covariance refers to the full factorized input state.")
        self.play(Write(cov));self.hold()
        self.step("Inspect the input position and momentum marginals", "These two contours are projections of one four-dimensional Wigner function. Initially the two input modes are independent.")
        self.play(*[Create(a) for a in axes],*[FadeIn(l) for l in labels],*[FadeIn(s) for s in shapes],FadeIn(description));self.hold()
        transformed=equation(r"W_{\rm out}(Q_{n+1},Q^\perp_{n+1},P_{n+1},P^\perp_{n+1})",size=33).move_to(w)
        entanglement=equation(r"n=1:\qquad Q_{n+1}\ \text{and}\ Q^\perp_{n+1}\ \text{are entangled}",size=29,color=MIX).move_to(cov)
        new_labels=[]
        for ax,names in zip(axes,[(r"Q_{n+1}",r"Q^\perp_{n+1}"),(r"P_{n+1}",r"P^\perp_{n+1}")]):
            new_labels.append(VGroup(equation(names[0],size=22).next_to(ax.x_axis,RIGHT,buff=.12),equation(names[1],size=22).next_to(ax.y_axis,UP,buff=.12)))
        self.step("Redefine the two output modes", "Apply the reversible coordinate redefinition. Watch correlations appear in the position and momentum marginals; both output factors are retained.")
        self.play(tracker.animate.set_value(1),Transform(w,transformed),Transform(cov,entanglement),*[Transform(a,b) for a,b in zip(labels,new_labels)],run_time=3)
        for shape in shapes: shape.clear_updaters()
        self.hold()
        retained=text_line("Both output modes are still retained",20,MIX).move_to([0,-3.17,0])
        self.step("The entangled joint output is still pure", "The full operation is unitary, so the joint purity remains one. Hold both output modes here. The next Right-arrow press presents the two portraits; the subsequent Right-arrow press performs the partial trace.")
        self.play(Write(purity),FadeIn(retained));self.hold()

        self.trace_collective_complement()

    def trace_collective_complement(self):
        sigma0=np.diag([1,.25,.25,1])
        self.step("Tracing the collective complement", "Prepare the trace without executing it. Hold both portraits and joint purity one on this canvas. Only the NEXT separate Right-arrow press starts tracing. Discard the whole complementary oscillator Q^perp_{n+1},P^perp_{n+1}, retaining Q_{n+1},P_{n+1}. Show rho_{n+1}=Tr_{Q^perp_{n+1}} rho_joint; the trace subscript labels the entire complementary Hilbert-space factor. In phase space the fully labelled operation is W_{n+1}(Q_{n+1},P_{n+1})=integral dQ^perp_{n+1} dP^perp_{n+1} W_out(Q_{n+1},Q^perp_{n+1},P_{n+1},P^perp_{n+1}). For the chosen n=1 example the retained covariance is diag(5/16,5/4), determinant 25/64 and purity 4/5. The portraits are marginals of the joint state; the correlation arrow represents the cross-mode correlations. The full unmeasured joint state remains pure, while its retained reduced state is mixed.")
        self.section(2,"Two entangled modes before the partial trace")
        mapping=canonical_map(1);covariance=mapping@sigma0@mapping.T
        portraits=[]
        for x,idx,names,color in [(-3.3,[0,2],(r"Q_{n+1}",r"P_{n+1}"),MIX),(3.3,[1,3],(r"Q^\perp_{n+1}",r"P^\perp_{n+1}"),SHELL)]:
            ax=Axes(x_range=[-3,3,1],y_range=[-3,3,1],x_length=3.4,y_length=2.6,tips=False).move_to([x,.45,0])
            labels=VGroup(equation(names[0],size=23).next_to(ax.x_axis,RIGHT,buff=.1),equation(names[1],size=23).next_to(ax.y_axis,UP,buff=.1))
            portraits.append(VGroup(ax,labels,self.gaussian_projection(covariance[np.ix_(idx,idx)],ax,color)))
        link=DoubleArrow([-.6,.45,0],[1.3,.45,0],color=MIX,buff=.1,stroke_width=2.5,tip_length=.16)
        label=text_line("correlated",20,MIX).move_to([.35,.95,0])
        discarded=equation(r"\text{Discard }(Q^\perp_{n+1},P^\perp_{n+1})",size=24,color=SHELL,width=5.8).move_to([3.3,-1.1,0])
        trace=equation(r"\rho_{n+1}=\Tr_{Q^\perp_{n+1}}\rho_{\rm joint}",size=40).move_to([0,-1.85,0])
        result=equation(r"n=1:\quad\Sigma_{n+1}=\operatorname{diag}(5/16,5/4),\quad\mu_{n+1}=\frac1{2\sqrt{\det\Sigma_{n+1}}}=\frac45",size=31,color=MIX).move_to([0,-2.8,0])
        joint_purity=equation(r"\Tr\rho_{\rm joint}^2=1",size=33,color=GREEN).move_to([0,-1.85,0])
        retained_note=text_line("Both output modes are retained",23,MIX).move_to([0,-2.8,0])
        self.play(*[FadeIn(p) for p in portraits],GrowArrow(link),FadeIn(label),Write(joint_purity),FadeIn(retained_note));self.hold()
        self.step("Trace out the complementary oscillator", "The two portraits have now held on screen with joint purity one. THIS separate Right-arrow press starts discarding the entire complementary pair (Q^perp_{n+1},P^perp_{n+1}). The retained reduced state is rho_{n+1}=Tr_{Q^perp_{n+1}} rho_joint. The following press reveals its covariance and purity.")
        self.set_chrome(2,"Trace out the complementary oscillator")
        self.play(FadeOut(joint_purity),FadeOut(retained_note),FadeOut(portraits[1]),FadeOut(link),FadeOut(label),FadeIn(discarded),Write(trace),run_time=1.8);self.hold()
        self.step("The retained oscillator is mixed", "Only after the trace, evaluate the retained covariance and its determinant. Its purity is 4/5 even though the unmeasured joint state was pure.")
        self.play(Write(result));self.hold()

