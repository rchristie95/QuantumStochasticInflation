"""Presentation content: classical."""
from presentation_common import *


class ClassicalSection:
    def starobinsky(self):
        self.step("Phase-space Langevin equations", "These are the paper's original field and comoving momentum-density equations, before its retained canonical pair is introduced. Noise terms come from differentiating the cutoff.")
        self.section(1,"Starobinsky's formulation")
        drift_label = text_line("Classical drift", 24, BULK).move_to([-2,2,0])
        noise_label = text_line("Crossing-shell noise", 24, SHELL).move_to([3,2,0])
        phi = equation(r"\frac{d\phi}{dN}=",r"\frac{\pi}{Ha^3}","+",r"\xi_\phi",size=46).move_to([0,.9,0])
        mom = equation(r"\frac{d\pi}{dN}=",r"-\frac{a^3m^2}{H}\phi","+",r"\xi_\pi",size=46).move_to([0,-.5,0])
        for obj in [phi,mom]:
            obj[1].set_color(BULK); obj[3].set_color(SHELL)
        corr=equation(r"\langle\xi_f(N)\xi_g(N')\rangle=D_{fg}(N)\,\delta(N-N')",size=32).move_to([0,-2,0])
        self.play(FadeIn(drift_label),FadeIn(noise_label),Write(phi))
        self.hold()
        self.step("The momentum-density Langevin equation", "Now add the conjugate phase-space equation. Its bulk mass force and its boundary noise have the same colour convention as the field equation.")
        self.play(Write(mom));self.hold()
        self.step("Specify the boundary-noise correlations", "The shell supplies correlated white-noise sources in e-fold time. The diffusion matrix describes both phase-space components.")
        self.play(Write(corr));self.hold()

        self.step("Slow-roll reduction", "Use m much smaller than H, sigma much smaller than one, and the overdamped attractor. The amplitude H/(2 pi) is specific to this limit.")
        self.clear_content()
        conditions=equation(r"m\ll H,\qquad\sigma\ll1,\qquad\text{slow-roll attractor}",size=34).move_to([0,1.9,0])
        self.sde=equation(r"d\phi=",r"-\frac{m^2\phi}{3H^2}\,dN","+",r"\frac{H}{2\pi}\,dW_N",size=48).move_to([0,.4,0])
        self.sde[1].set_color(BULK);self.sde[3].set_color(SHELL)
        brownian=equation(r"\mathbb E[dW_N]=0,\qquad\mathbb E[dW_N^2]=dN",size=32).move_to([0,-1.1,0])
        self.play(Write(conditions));self.hold()
        self.step("Keep the slow-roll drift", "Use the overdamped light-field attractor to obtain the deterministic decay term. The boundary noise is revealed next.")
        self.play(Write(self.sde[0]),Write(self.sde[1]));self.hold()
        self.step("Add the light-field stochastic increment", "In the stated light-field, super-Hubble limit, the noise coefficient is H/(2 pi). This amplitude is not asserted outside that limit.")
        self.play(Write(self.sde[2]),Write(self.sde[3]));self.hold()
        self.step("Normalize the Wiener increment", "The increment has zero mean and variance dN. This normalization fixes the meaning of the noise amplitude in the preceding equation.")
        self.play(Write(brownian));self.hold()

