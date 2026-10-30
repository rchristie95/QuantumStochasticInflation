"""Presentation content: massive."""
from presentation_common import *
from hashlib import sha256

WIGNER_END=10.
MASS_EXAMPLES=(1.,1.5,2.)


def _nice_limit(value):
    power=10.**np.floor(np.log10(value))
    return float(np.ceil(value/power)*power)


def field_wigner_model(mass,sigma=.1):
    """Exact Gaussian GKLS covariance, converted to physical canonical Q,P."""
    times,covs,purities,stationary,drift,diffusion,*_=massive_covariances(mass,sigma,times=np.linspace(0,WIGNER_END,401))
    volume=6*np.pi**2/sigma**3
    inverse=np.diag([1/np.sqrt(mass*volume),np.sqrt(mass*volume)])
    physical=np.array([inverse@cov@inverse.T for cov in covs])
    return dict(mass=mass,times=times,covs=physical,purities=purities,
                stationary=stationary,drift=drift,inverse=inverse,
                qlim=_nice_limit(4.3*np.sqrt(physical[:,0,0].max())),
                plim=_nice_limit(4.3*np.sqrt(physical[:,1,1].max())))


def field_covariance(model,time):
    prop=expm(model['drift']*time)
    cov=model['stationary']+prop@(.5*np.eye(2)-model['stationary'])@prop.T
    return model['inverse']@cov@model['inverse'].T


WIGNER_MIN=1e-5
WIGNER_MAX=1/np.pi
WIGNER_PALETTE=np.array([[16,24,36],[38,73,129],[79,151,208],[143,209,179],[255,235,167]],dtype=float)


def wigner_rgb(values):
    """One shared, quantitatively labelled logarithmic colour map."""
    level=np.clip(np.log(np.maximum(values,WIGNER_MIN)/WIGNER_MIN)/np.log(WIGNER_MAX/WIGNER_MIN),0,1)
    rgb=np.stack([np.interp(level,np.linspace(0,1,len(WIGNER_PALETTE)),WIGNER_PALETTE[:,k]) for k in range(3)],axis=-1)
    return np.rint(rgb).astype(np.uint8)


def gaussian_wigner(cov,q,p):
    determinant=float(np.linalg.det(cov))
    exponent=(cov[1,1]*q*q-2*cov[0,1]*q*p+cov[0,0]*p*p)/(2*determinant)
    return np.exp(-exponent)/(2*np.pi*np.sqrt(determinant))


class MassiveSection:
    def massive_spectator(self):
        if os.environ.get("QSI_WIGNER_ONLY")=="1":
            self.wigner_relaxation()
            self.thank_you()
            return
        self.step("Massive spectator dynamics", "Apply the derived channel to the free massive spectator. Exact de Sitter, constant H, sharp cutoff, Bunch-Davies incoming vacuum, leading super-Hubble bulk Hamiltonian. The first moments are unconditional; the boundary input changes covariance as well as damping.")
        self.section(3,"Massive spectator field in de Sitter")
        setup=equation(r"a=e^{Ht},\quad k_\sigma=\sigma aH,\quad V_{\rm phys}=\frac{6\pi^2}{\sigma^3H^3}",size=35).move_to([0,1.95,0])
        first=equation(r"\frac{d\langle\hat Q\rangle}{dN}=\frac{\langle\hat P\rangle}{HV_{\rm phys}},",r"\qquad"
                       r"\frac{d\langle\hat P\rangle}{dN}=-3\langle\hat P\rangle-\frac{m^2V_{\rm phys}}{H}\langle\hat Q\rangle",size=33).move_to([0,.45,0])
        second=equation(r"\frac{d^2\langle\hat Q\rangle}{dN^2}+3\frac{d\langle\hat Q\rangle}{dN}+\frac{m^2}{H^2}\langle\hat Q\rangle=0",size=40,color=BULK).move_to([0,-1.15,0])
        label=text_line("The drift of a damped oscillator; fluctuations remain quantum",24,MUTED).move_to([0,-2.5,0])
        self.play(Write(setup));self.hold()
        self.step("Evolve the mean collective field", "The first Hamilton equation relates the mean field velocity in e-fold time to its canonical total momentum.")
        self.play(Write(first[0]));self.hold()
        self.step("Evolve the mean total momentum", "The companion equation contains Hubble damping and the mass restoring force. Together these form the unconditional drift system.")
        self.play(Write(first[1]));self.hold()
        self.step("Eliminate momentum to obtain the damped oscillator", "Combine the coupled first-moment equations. The second-order mean equation does not describe the full quantum covariance or a stochastic realization.")
        self.play(Write(second),FadeIn(label));self.hold()

        self.step("Three mass regimes", "These curves show normalized unconditional mean displacement, initially one with zero derivative, not purity and not a stochastic trajectory. The critical threshold follows from the drift eigenvalues. Light, critical and heavy examples use m/H=1,1.5,2.")
        self.clear_content()
        eigen=equation(r"\lambda_\pm=-\frac32\pm\sqrt{\frac94-\frac{m^2}{H^2}}",size=39).move_to([0,1.95,0])
        self.play(Write(eigen))
        for x,mass,color,name in zip([-4.4,0,4.4],MASS_EXAMPLES,[BULK,MIX,SHELL],["Light: overdamped","Critical","Heavy: underdamped"]):
            self.hold()
            self.step(f"Mean motion: {name.lower()}", f"Show m/H={mass:g} with the same initial displacement and zero velocity. These curves describe unconditional means, not purity or sample trajectories.")
            axes=Axes(x_range=[0,6,2],y_range=[-.2,1.2,.5],x_length=3.3,y_length=2.2,tips=False).move_to([x,-.25,0])
            def mean(n,mass=mass):
                nu=np.sqrt(2.25-mass**2+0j)
                return float(np.real(np.exp(-1.5*n)*((1+1.5*n) if abs(nu)<1e-9 else np.cosh(nu*n)+1.5/nu*np.sinh(nu*n))))
            curve=axes.plot(mean,x_range=[0,6,.04],color=color)
            title=text_line(name,22,color,width=3.8).move_to([x,1.05,0])
            ratio=equation(fr"m/H={mass:g}",size=28,color=color).move_to([x,-1.8,0])
            self.play(Create(axes),FadeIn(title),Write(ratio),Create(curve),run_time=1.2)
        legend=text_line("Mean displacement vs e-folds; identical initial displacement and velocity",22,MUTED).move_to([0,-2.75,0])
        self.play(FadeIn(legend));self.hold()

        self.wigner_relaxation()
        self.thank_you()

    def wigner_relaxation(self):
        self.step("Mass-dependent Wigner dynamics", "Plot the actual normalized Gaussian Wigner density W(Q,P,N)=exp[-r^T Sigma^-1 r/2]/(2 pi sqrt(det Sigma)), from the paper's finite-sigma Bunch-Davies drift and diffusion. Convert the internally scaled covariance back to physical canonical Q,P; H=1 and sigma=0.1. Each panel has a fixed Q/P range that covers its evolution. All panels and times use ONE logarithmic Wigner colour scale, with physical density values on the colourbar. There is no separate peak normalization. Initial covariance is the pure bulk ground state and means are zero.")
        self.section(3,"Wigner evolution of the retained quantum field")
        models=[field_wigner_model(m) for m in MASS_EXAMPLES]
        centres=[-4.4,-.2,4.0];colours=[BULK,MIX,SHELL]
        tracker=ValueTracker(0)
        # One raster for all three densities avoids repeated full-camera overlays.
        height,width=300,1500
        canvas=np.zeros((height,width,4),dtype=np.uint8)
        panel_width=375
        grids=[]
        for centre,model in zip(centres,models):
            q=np.linspace(-model['qlim'],model['qlim'],panel_width)
            p=np.linspace(model['plim'],-model['plim'],height)
            qq,pp=np.meshgrid(q,p)
            start=round((centre-1.5+5.9)/12*width)
            grids.append((start,qq,pp))
        bar_start=round((5.94+5.9)/12*width)
        bar_end=round((6.06+5.9)/12*width)
        bar_values=np.geomspace(WIGNER_MAX,WIGNER_MIN,height)
        canvas[:,bar_start:bar_end,:3]=wigner_rgb(bar_values)[:,None,:]
        canvas[:,bar_start:bar_end,3]=255
        def pixels(time):
            for model,(start,qq,pp) in zip(models,grids):
                density=gaussian_wigner(field_covariance(model,time),qq,pp)
                canvas[:,start:start+panel_width,:3]=wigner_rgb(density)
                canvas[:,start:start+panel_width,3]=255
            return canvas.copy()
        image=ImageMobject(pixels(0)).stretch_to_fit_width(12).stretch_to_fit_height(2.4).move_to([.1,.7,0])
        image.model_digest=sha256(Path(__file__).read_bytes()+b'physical-Q-P-gaussian-Wigner').hexdigest()
        axis_group=VGroup();labels=VGroup()
        for centre,model,colour in zip(centres,models,colours):
            qlim,plim=model['qlim'],model['plim']
            ax=Axes(x_range=[-qlim,qlim,qlim],y_range=[-plim,plim,plim],
                    x_length=3,y_length=2.4,tips=False,axis_config={'stroke_width':1,'stroke_opacity':.5,'color':INK}).move_to([centre,.7,0])
            axis_group.add(ax)
            labels.add(equation('Q',size=21).move_to([centre+1.7,.7,0]),equation('P',size=21).move_to([centre-1.65,2.05,0]))
            for value in [-qlim,0,qlim]:
                labels.add(text_line(f'{value:g}',13,MUTED).move_to([ax.c2p(value,0)[0],-.69,0]))
            for value in [-plim,plim]:
                labels.add(text_line(f'{value:g}',13,MUTED,width=.6).move_to([centre-1.72,ax.c2p(0,value)[1],0]))
            labels.add(equation(fr'm/H={model["mass"]:g}',size=25,color=colour).move_to([centre,2.22,0]))
        labels.add(equation(r'W',size=23).move_to([6,2.16,0]))
        axis_group.add(Rectangle(width=.12,height=2.4,color=MUTED,stroke_width=1).move_to([6,.7,0]))
        for value,tex in [(WIGNER_MIN,r'10^{-5}'),(1e-3,r'10^{-3}'),(.1,r'10^{-1}'),(WIGNER_MAX,r'1/\pi')]:
            y=-.5+2.4*np.log(value/WIGNER_MIN)/np.log(WIGNER_MAX/WIGNER_MIN)
            axis_group.add(Line([6.06,y,0],[6.13,y,0],color=MUTED,stroke_width=1))
            labels.add(equation(tex,size=14,color=MUTED).move_to([6.47,y,0]))
        setup=text_line('Bunch-Davies input; H = 1; sigma = 0.1',20,MUTED).move_to([0,2.56,0])
        purity_axes=Axes(x_range=[0,WIGNER_END,2],y_range=[0,1,.5],x_length=10.3,y_length=1.45,
                         tips=False,axis_config={'include_numbers':True,'font_size':18}).move_to([0,-2.12,0])
        purity_labels=VGroup(equation(r'\gamma',size=25).next_to(purity_axes.y_axis,LEFT,buff=.22),
                             equation('N',size=23).next_to(purity_axes.x_axis,RIGHT,buff=.18))
        scale_note=text_line('Physical Q,P axes; fixed ranges per panel; shared logarithmic W colour scale',17,MUTED,width=12.5).move_to([0,-3.17,0])
        self.play(FadeIn(setup),Create(purity_axes),FadeIn(purity_labels));self.hold()
        self.step("Prepare the initially pure field Wigner functions", "The examples use m/H=1 (light), 1.5 (critical) and 2 (heavy). All three initial Wigner functions integrate to one and have purity one. Q and P are the canonical QFT variables. Axis ranges are fixed individually per mass; the shared colourbar is not rescaled between masses or during evolution. The lower curves will show purity from the same covariance matrices.")
        self.add(image,labels,scale_note)
        self.add_foreground_mobject(axis_group)
        self.hold()
        self.step("Evolve Wigner densities and compare purity", "Evolve the exact Gaussian covariance from N=0 to N=10, update the actual Wigner density, and draw the three corresponding purities. The clock is slowed at early times to resolve the heavy-field transient, then accelerates toward the late-time distribution. The plotted time remains N, not rendered seconds. All Wigner functions retain unit integral on the full plane.")
        image.add_updater(lambda m:setattr(m,'pixel_array',pixels(tracker.get_value())))
        curves=[]
        for model,colour in zip(models,colours):
            def curve(model=model,colour=colour):
                now=tracker.get_value();mask=model['times']<=now
                points=[purity_axes.c2p(t,p) for t,p in zip(model['times'][mask],model['purities'][mask])]
                current=1/(2*np.sqrt(np.linalg.det(field_covariance(model,now))))
                points.append(purity_axes.c2p(now,current))
                if len(points)<2:points.append(points[0]+RIGHT*1e-6)
                return VMobject(color=colour,stroke_width=2.8).set_points_as_corners(points)
            curves.append(always_redraw(curve))
        self.add(*curves)
        self.play(tracker.animate.set_value(WIGNER_END),run_time=10,rate_func=lambda t:np.expm1(3*t)/np.expm1(3))
        image.clear_updaters()
        for curve in curves:curve.clear_updaters()
        self.hold()
        self.remove_foreground_mobject(axis_group)

    def thank_you(self):
        self.step("Thanks for listening", "Thank the audience. Quantum Stochastic Inflation, Robson Christie, Pusan National University, South Korea; collaborators Jaewoo Joo, Greg Kaplanek, Vincent Vennin and David Wands. arXiv:2606.12636; the QR code and URL match the title page.")
        self.clear_content()
        self.remove(self.chrome);self.chrome=VGroup();self.chrome_state=None
        thanks=text_line('Thanks for listening',47).move_to([0,2.8,0])
        paper=text_line('Quantum Stochastic Inflation',34,BULK).move_to([0,1.97,0])
        rule=Line([-6,1.46,0],[6,1.46,0],color=BULK,stroke_opacity=.6)
        presenter=text_line('Robson Christie',32,BULK).move_to([-2,.97,0])
        affiliation=text_line('Pusan National University, South Korea',23,MUTED).move_to([-2,.4,0])
        collaborators=VGroup(text_line('With Jaewoo Joo, Greg Kaplanek,',24,width=7.7),
                             text_line('Vincent Vennin and David Wands',24,width=7.7)).arrange(DOWN,buff=.22).move_to([-2,-.58,0])
        identifier=text_line('arXiv:2606.12636',29,SHELL).move_to([-2,-1.7,0])
        link=text_line(PAPER_URL,20,MUTED,width=7.5).move_to([-2,-2.25,0])
        qr=self.paper_qr().move_to([4.55,-.35,0])
        scan=text_line('Read the paper',21,MUTED).move_to([4.55,-2.12,0])
        self.play(Write(thanks),FadeIn(paper),Create(rule),FadeIn(presenter),FadeIn(affiliation),run_time=1)
        self.play(FadeIn(collaborators),Write(identifier),FadeIn(link),FadeIn(qr),FadeIn(scan));self.hold()
