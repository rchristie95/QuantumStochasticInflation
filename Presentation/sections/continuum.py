"""The retained QFT mode in a moving sharp Fourier window."""
from presentation_common import *


class ContinuumSection:
    def continuum_connection(self):
        self.step("The retained QFT mode", "Use quantum field operators throughout. Evaluate at the representative patch centre. The sharp Fourier window selects the averaged field; the full infrared sector still contains more than this one retained collective mode.")
        self.section(3,"A moving Fourier window selects the field mode")
        q=equation(r"\hat Q_N=\int\frac{d^3k}{(2\pi)^3}\,\Theta(k_\sigma-k)\hat\Phi_{\mathbf k}(N)",size=39,color=BULK).move_to([0,1.65,0])
        p=equation(r"\hat P_N=V_{\rm com}\int\frac{d^3k}{(2\pi)^3}\,\Theta(k_\sigma-k)\hat\Pi_{\mathbf k}(N)",size=39,color=SHELL).move_to([0,.15,0])
        norm=equation(r"V_{\rm com}=\frac{6\pi^2}{k_\sigma^3},\qquad[\hat Q_N,\hat P_N]=i",size=37,color=GREEN).move_to([0,-1.35,0])
        caption=text_line("One canonical collective mode of the infrared quantum field",24,MUTED).move_to([0,-2.65,0])
        self.play(Write(q));self.hold()
        self.step("Select the total field momentum", "Apply the same Fourier window to the canonical momentum density, including the effective-volume factor in the total momentum from the beginning.")
        self.play(Write(p));self.hold()
        self.step("Normalize the retained QFT mode", "Parseval fixes the effective volume for the sharp Fourier window. The retained quantum field and total momentum are a canonical pair.")
        self.play(Write(norm),FadeIn(caption));self.hold()
