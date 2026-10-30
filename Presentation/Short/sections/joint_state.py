"""Presentation content: joint state."""
from presentation_common import *
from hashlib import sha256


WIGNER_DENSITY_MAX=1/np.pi
WIGNER_PALETTE=np.array([[16,24,36],[38,73,129],[79,151,208],[143,209,179],[255,235,167]],dtype=float)


def gaussian_marginal(covariance,x,y):
    """Exact normalized 2D marginal of the zero-mean Gaussian Wigner density."""
    inverse=np.linalg.inv(covariance)
    exponent=inverse[0,0]*x*x+2*inverse[0,1]*x*y+inverse[1,1]*y*y
    return np.exp(-exponent/2)/(2*np.pi*np.sqrt(np.linalg.det(covariance)))


def density_pixels(density):
    """One absolute linear density scale for every panel and animation frame."""
    level=np.clip(density/WIGNER_DENSITY_MAX,0,1)
    rgb=np.stack([np.interp(level,np.linspace(0,1,len(WIGNER_PALETTE)),WIGNER_PALETTE[:,k]) for k in range(3)],axis=-1)
    alpha=np.full((*level.shape,1),255,dtype=np.uint8)
    return np.concatenate([np.rint(rgb).astype(np.uint8),alpha],axis=-1)


def refresh_density_digest(image):
    # Manim excludes pixel arrays from animation hashes.
    image.asset_content_digest=sha256(image.pixel_array.tobytes()+Path(__file__).read_bytes()).hexdigest()


def density_axes(center):
    return Axes(x_range=[-3,3,1],y_range=[-3,3,1],x_length=4,y_length=2.3,tips=False,
                axis_config={'include_numbers':True,'numbers_to_include':[-3,3],
                             'font_size':16,'stroke_width':1.2,'stroke_opacity':.6}).move_to(center).set_z_index(2)


class JointStateSection:
    def gaussian_density_plot(self,covariance,axes):
        x,y=np.meshgrid(np.linspace(-3,3,480),np.linspace(3,-3,276))
        pixels=density_pixels(gaussian_marginal(covariance,x,y))
        image=ImageMobject(pixels).stretch_to_fit_width(4).stretch_to_fit_height(2.3).move_to(axes.c2p(0,0))
        refresh_density_digest(image)
        return image,x,y


    def joint_wigner_example(self):
        self.step("Product inputs become entangled outputs", "Worked example n=1, retaining general-index coordinate names throughout. Start with independent Q_n,P_n and q_{n+1},p_{n+1}, in differently squeezed pure Gaussian states. The input covariance in the displayed order Q_n,q_{n+1},P_n,p_{n+1} is diag(1,1/4,1/4,1). W_n^joint is pi^-2 exp[-Q_n^2/2-2q_{n+1}^2-2P_n^2-p_{n+1}^2/2]. The plots evaluate the exact normalized position and momentum marginals of this 4D Wigner density, integrating over the other pair of coordinates. One absolute linear density colour scale, zero to 1/pi, is fixed across both panels and the reduced density. Animate the canonical coordinate transformation; the full covariance determinant stays 1/16 and joint purity stays one. W_n prime joint denotes the same Wigner function in output coordinates, not a new state. The initial fixed parity reflection leaves the even incoming squeezed vacuum unchanged. Outputs are Q_{n+1},Q^perp_{n+1},P_{n+1},P^perp_{n+1}. Position cross covariance is 3/8 and momentum cross covariance is -3/8. For these pure inputs, the output factors are entangled. Both output modes remain present until the partial trace.")
        self.section(2,"Independent inputs become entangled outputs")
        sigma0=np.diag([1,.25,.25,1])
        w=equation(r"W_n^{\mathrm{joint}}(Q_n,q_{n+1},P_n,p_{n+1})=\frac1{\pi^2}e^{-Q_n^2/2-2q_{n+1}^2-2P_n^2-p_{n+1}^2/2}",size=30).move_to([0,2.23,0])
        cov=equation(r"n=1:\qquad\Sigma_{\rm in}=\operatorname{diag}(1,1/4,1/4,1)",size=29).move_to([0,1.38,0])
        axes=[];labels=[];shapes=[]
        tracker=ValueTracker(0)
        for x,indices,names,color in [(-3.3,[0,1],(r"Q_n",r"q_{n+1}"),BULK),(3.3,[3,2],(r"p_{n+1}",r"P_n"),SHELL)]:
            ax=density_axes([x,-.65,0])
            labels.append(VGroup(equation(names[0],size=22,color=color).next_to(ax.x_axis,RIGHT,buff=.12),equation(names[1],size=22,color=color).next_to(ax.y_axis,UP,buff=.12)).set_z_index(3))
            image,xx,yy=self.gaussian_density_plot(sigma0[np.ix_(indices,indices)],ax)
            def update_density(image,indices=indices,xx=xx,yy=yy):
                mapping=canonical_map(1,tracker.get_value())
                covariance=mapping@sigma0@mapping.T
                image.pixel_array=density_pixels(gaussian_marginal(covariance[np.ix_(indices,indices)],xx,yy))
            image.add_updater(update_density)
            shapes.append(image);axes.append(ax)
        description=text_line("Exact position and momentum marginals of the joint Wigner density",21,MUTED).move_to([0,-2.05,0])
        bar=ImageMobject(density_pixels(np.linspace(WIGNER_DENSITY_MAX,0,276)[:,None])).stretch_to_fit_width(.16).stretch_to_fit_height(2.3).move_to([6.15,-.65,0])
        refresh_density_digest(bar)
        bar_labels=VGroup(text_line('Density',17,MUTED).move_to([6.3,.92,0]),
                          equation(r'1/\pi',size=17).move_to([6.65,.5,0]),
                          equation('0',size=17).move_to([6.65,-1.8,0]))
        purity=equation(r"\rho_n\otimes\rho_{\rm in}\xrightarrow{\ U_{A_n}\ }\rho_{\rm joint},\qquad\Tr\rho_{\rm joint}^2=1",size=31,color=GREEN).move_to([0,-2.7,0])
        self.play(Write(w));self.hold()
        self.step("Specify the pure Gaussian input covariance", "Use n=1 and perpendicular pure squeezing. The four-dimensional covariance refers to the full factorized input state.")
        self.play(Write(cov));self.hold()
        self.step("Inspect the input position and momentum marginals", "W_n^joint denotes the full 4D Wigner density. The two heatmaps are its exact normalized position-position and momentum-momentum marginals, not schematic ellipses or 2D slices. Integrate over the other two coordinates. Both use the fixed density colour scale zero to 1/pi. Initially the two input modes are independent.")
        self.play(*[Create(a) for a in axes],*[FadeIn(l) for l in labels],*[FadeIn(s) for s in shapes],FadeIn(description),FadeIn(bar),FadeIn(bar_labels));self.hold()
        transformed=equation(r"W_n^{\prime,\mathrm{joint}}(Q_{n+1},Q^\perp_{n+1},P_{n+1},P^\perp_{n+1})",size=33).move_to(w)
        new_description=text_line("Same joint Wigner function in new coordinates; exact marginals",21,MUTED).move_to(description)
        entanglement=equation(r"n=1:\qquad Q_{n+1}\ \text{and}\ Q^\perp_{n+1}\ \text{are entangled}",size=29,color=MIX).move_to(cov)
        new_labels=[]
        for ax,names in zip(axes,[(r"Q_{n+1}",r"Q^\perp_{n+1}"),(r"P^\perp_{n+1}",r"P_{n+1}")]):
            new_labels.append(VGroup(equation(names[0],size=22).next_to(ax.x_axis,RIGHT,buff=.12),equation(names[1],size=22).next_to(ax.y_axis,UP,buff=.12)).set_z_index(3))
        self.step("Redefine the two output modes", "Apply the reversible canonical coordinate redefinition. W_n prime joint is W_n joint expressed in the output coordinates, with no Jacobian factor because the full map is symplectic. At every animation frame, evaluate the exact normalized 2D marginals from S Sigma_in S transpose. Watch their correlations change on the same colour scale; both output factors remain present.")
        self.play(tracker.animate.set_value(1),Transform(w,transformed),Transform(cov,entanglement),Transform(description,new_description),*[Transform(a,b) for a,b in zip(labels,new_labels)],run_time=3)
        for shape in shapes:
            shape.clear_updaters()
            refresh_density_digest(shape)
        self.hold()
        retained=text_line("Both output modes are still retained",20,MIX).move_to([0,-3.17,0])
        self.step("The entangled joint output is still pure", "Write the actual transformed Gaussian for n=1: pi^-2 exp[-(5/2)Q^2+(3/2)Q Qperp-(5/8)Qperp^2-(5/8)P^2-(3/2)P Pperp-(5/2)Pperp^2], with all output labels carrying n+1. It is the same Wigner function in the new coordinates. The full operation is unitary, so the joint purity remains one. Both output modes are still present.")
        explicit_joint=equation(
            r"\begin{aligned}n=1:\quad W_n^{\prime,\mathrm{joint}}"
            r"&=\frac1{\pi^2}\exp\!\Bigl[-\frac52 Q_{n+1}^2"
            r"+\frac32 Q_{n+1}Q^\perp_{n+1}-\frac58(Q^\perp_{n+1})^2"
            r"\\[-2pt]&\hspace{2.7em}-\frac58 P_{n+1}^2"
            r"-\frac32 P_{n+1}P^\perp_{n+1}-\frac52(P^\perp_{n+1})^2\Bigr]\end{aligned}",
            size=29).move_to([0,2.03,0])
        self.play(Transform(w,explicit_joint),FadeOut(cov),Write(purity),FadeIn(retained));self.hold()


        self.step("Tracing the collective complement", "Keep the same exact position and momentum marginals on screen. Define W_{n+1}^traced by integrating W_n prime joint over Qperp and Pperp, and evaluate it explicitly for n=1: 4/(5 pi) exp[-(8/5)Q_{n+1}^2-(2/5)P_{n+1}^2]. The analytic result is visible now; the next press animates this integral by merging the retained axes. Both output modes remain plotted until then.")
        integral=equation(
            r"\begin{aligned}W_{n+1}^{\mathrm{traced}}(Q_{n+1},P_{n+1})"
            r"&=\int dQ^\perp_{n+1}\,dP^\perp_{n+1}\;W_n^{\prime,\mathrm{joint}}"
            r"\\&=\frac4{5\pi}\exp\!\left[-\frac85Q_{n+1}^2-\frac25P_{n+1}^2\right]"
            r"\qquad(n=1)\end{aligned}",size=29).move_to([0,2.03,0])
        self.play(Transform(w,integral),run_time=1)
        self.hold()
        self.step("Trace out the complementary oscillator", "Integrate over the complementary position and momentum. The two exact marginal density maps move together: retained Q supplies the horizontal axis and retained P supplies the vertical axis. Contracting the integrated directions is a visual cue for integration; the two plots are not multiplied. The final heatmap evaluates the actual normalized reduced Q,P Wigner density with covariance diag(5/16,5/4), using the same absolute colour scale. The complementary mode has been traced out.")
        self.set_chrome(2,"Trace out the complementary oscillator")
        mapping=canonical_map(1);covariance=mapping@sigma0@mapping.T
        target=density_axes([0,-.65,0])
        qlabel=equation(r"Q_{n+1}",size=22).next_to(target.x_axis,RIGHT,buff=.12)
        plabel=equation(r"P_{n+1}",size=22).next_to(target.y_axis,UP,buff=.12)
        reduced,_,_=self.gaussian_density_plot(covariance[np.ix_([0,2],[0,2])],target)
        trace=equation(r"\rho_{n+1}=\Tr_{\perp}\rho_{\rm joint}",size=31).move_to(purity)
        traced=text_line("Complementary mode traced out",20,SHELL).move_to(retained)
        # Contract only the integrated directions, keeping retained Q and P scales.
        q_projection=shapes[0].copy().stretch(.015,1).move_to(target.c2p(0,0))
        p_projection=shapes[1].copy().stretch(.015,0).move_to(target.c2p(0,0))
        self.play(FadeOut(description),FadeOut(purity),FadeOut(retained),
                  FadeOut(labels[0][1]),FadeOut(labels[1][0]),
                  FadeOut(axes[0].y_axis),FadeOut(axes[1].x_axis),run_time=.6)
        self.play(Transform(axes[0].x_axis,target.x_axis),Transform(axes[1].y_axis,target.y_axis),
                  Transform(labels[0][0],qlabel),Transform(labels[1][1],plabel),
                  Transform(shapes[0],q_projection),Transform(shapes[1],p_projection),run_time=2.2)
        self.play(FadeOut(shapes[0]),FadeOut(shapes[1]),FadeIn(reduced),Write(trace),FadeIn(traced),run_time=1.2)
        self.hold()
        self.step("The retained oscillator is mixed", "The retained covariance is diagonal, with entries five sixteenths and five quarters. Its determinant is twenty-five sixty-fourths, giving purity four fifths. The global state was pure; the reduced state is mixed because the output modes were entangled.")
        result=equation(r"n=1:\quad\Sigma_{n+1}=\operatorname{diag}(5/16,5/4),\qquad\mu_{n+1}=\frac1{2\sqrt{\det\Sigma_{n+1}}}=\frac45",size=29,color=MIX).move_to([0,-2.12,0])
        self.play(Write(result),trace.animate.move_to([-3.15,-3.05,0]),traced.animate.move_to([3.15,-3.05,0]));self.hold()
