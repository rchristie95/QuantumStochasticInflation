"""Presentation content: canonical."""
from presentation_common import *


class CanonicalSection:
    def canonical_derivation(self):
        self.step("The spectator Lagrangian", "Begin the quantum derivation in 3+1 dimensions, c=hbar=1, dimensionless a and length-valued comoving coordinates. Fixed de Sitter geometry; spectator backreaction is neglected.")
        self.section(3,"From the field Lagrangian to its canonical algebra")
        metric=equation(r"ds^2=-dt^2+a^2(t)d\mathbf x^2,\quad a=e^{Ht},\quad N=Ht",size=35).move_to([0,2,0])
        lag=equation(r"\mathcal L_\Phi=-\frac12g^{\mu\nu}\partial_\mu\Phi\partial_\nu\Phi-\frac12m^2\Phi^2",size=39).move_to([0,.65,0])
        action=equation(r"S=\int dt\,d^3x\,a^3\left[\frac12\dot\Phi^2-\frac{(\nabla\Phi)^2}{2a^2}-\frac12m^2\Phi^2\right]",size=35).move_to([0,-.85,0])
        assumption=text_line("Free spectator field; fixed background",25,MUTED).move_to([0,-2.4,0])
        self.play(Write(metric));self.hold()
        self.step("Choose the free spectator Lagrangian", "On the fixed de Sitter geometry, introduce the covariant kinetic and mass terms. The spectator does not backreact on the background.")
        self.play(Write(lag));self.hold()
        self.step("Write the action in cosmological time", "Insert the metric and the volume element a^3. Identify the time-derivative term before taking its canonical derivative.")
        self.play(Write(action),FadeIn(assumption));self.hold()

        self.step("Canonical quantisation", "Differentiate the coordinate Lagrangian density a^3 L, not L alone. Pi is the canonical momentum density with respect to comoving coordinate volume.")
        self.section(3,"Quantise the field and its momentum density")
        pi=equation(r"\Pi=\frac{\partial(a^3\mathcal L_\Phi)}{\partial\dot\Phi}=a^3\dot\Phi",size=44,color=SHELL).move_to([0,1.7,0])
        ham=equation(r"\mathcal H=\frac{\Pi^2}{2a^3}+\frac a2(\nabla\Phi)^2+\frac{a^3m^2}{2}\Phi^2",size=39).move_to([0,.15,0])
        comm=equation(r"[\hat\Phi(\mathbf x),\hat\Pi(\mathbf y)]=i\delta^{(3)}(\mathbf x-\mathbf y)",size=38).move_to([0,-1.45,0])
        self.play(Write(pi));self.hold()
        self.step("Legendre transform to the Hamiltonian density", "Express the kinetic term using the comoving canonical momentum density. Keep the gradient and mass terms.")
        self.play(Write(ham));self.hold()
        self.step("Impose the equal-time field commutator", "Quantize the field and its canonical momentum density. The delta function carries inverse coordinate-volume dimensions.")
        self.play(Write(comm));self.hold()


        self.step("Canonical coarse-grained field variables", "Define the QFT variables directly: the field is averaged, while P_N is the total canonical momentum of the effective patch. V_com is the inverse squared-kernel norm. There is no trial averaged momentum and no discrete oscillator recap.")
        self.section(3,"Field average and total canonical momentum")
        norm=equation(r"\int d^3y\,W_N=1,\qquad V_{\rm com}^{-1}=\int d^3y\,W_N^2",size=35).move_to([0,1.95,0])
        q=equation(r"\hat Q_N=\int d^3y\,W_N(\mathbf y)\hat\Phi(\mathbf y)",size=40,color=BULK).move_to([0,.65,0])
        p=equation(r"\hat P_N=V_{\rm com}\int d^3y\,W_N(\mathbf y)\hat\Pi(\mathbf y)",size=40,color=SHELL).move_to([0,-.65,0])
        roles=text_line("Averaged field; total momentum of the effective patch",25,GREEN).move_to([0,-2.3,0])
        self.play(Write(norm));self.hold()
        self.step("Define the averaged quantum field", "Smear the quantum field over the normalized real kernel.")
        self.play(Write(q));self.hold()
        self.step("Define the total canonical field momentum", "Define P_N correctly from the outset as V_com times the smeared canonical momentum density. For a real-space top-hat this is the momentum integral; for the sharp Fourier window V_com is the effective smearing volume.")
        self.play(Write(p),FadeIn(roles));self.hold()

        self.step("The normalized smeared field algebra", "Use the equal-time QFT commutator with the correctly normalized total momentum. The same factor V_com appears throughout, so this calculation never introduces a noncanonical trial momentum.")
        self.section(3,"Smearing preserves the canonical field algebra")
        integral=equation(r"[\hat Q_N,\hat P_N]=iV_{\rm com}\!\int d^3y\,d^3z\,W_N(\mathbf y)W_N(\mathbf z)\delta^{(3)}(\mathbf y-\mathbf z)",size=32).move_to([0,1.65,0])
        reduced=equation(r"=iV_{\rm com}\int d^3y\,W_N^2=i",size=43,color=GREEN).move_to([0,.15,0])
        dims=equation(r"[\hat Q_N,\hat P_N]=i,\qquad [Q]=M,\quad[P]=M^{-1}",size=36).move_to([0,-1.55,0])
        self.play(Write(integral));self.hold()
        self.step("Collapse the field delta function", "The squared-kernel norm cancels the effective volume in the total momentum.")
        self.play(Write(reduced));self.hold()
        self.step("Read the canonical field dimensions", "With hbar=1 the canonical commutator is dimensionless. Q has mass dimension one and its conjugate total field momentum has mass dimension minus one.")
        self.play(Write(dims));self.hold()

        self.step("The homogeneous patch Hamiltonian", "For a sharp Fourier window, Parseval fixes the effective comoving volume. It is not a literal real-space top-hat volume. The physical effective volume is constant. The homogeneous bulk Hamiltonian below describes pre-existing modes at leading super-Hubble order; the moving-boundary redefinition is added separately.")
        self.section(3,"The coarse-grained field Hamiltonian")
        vol=equation(r"V_{\rm com}=\left(\int W_N^2d^3y\right)^{-1}=\frac{6\pi^2}{k_\sigma^3},\quad V_{\rm phys}=a^3V_{\rm com}=\frac{6\pi^2}{\sigma^3H^3}",size=32).move_to([0,1.9,0])
        bulk=equation(r"K_{\rm IR}^\parallel=\frac{\hat P^2}{2HV_{\rm phys}}+\frac{m^2V_{\rm phys}}{2H}\hat Q^2",size=38).move_to([0,.1,0])
        label=text_line("One canonical collective mode, with a changing microscopic embedding",24,MUTED).move_to([0,-2.4,0])
        self.play(Write(vol));self.hold()
        self.step("Obtain the collective bulk Hamiltonian", "Substitute the canonical pair into the homogeneous bulk energy and divide by H to evolve in e-fold time. This is one canonical oscillator with a changing embedding.")
        self.play(Write(bulk),FadeIn(label));self.hold()

