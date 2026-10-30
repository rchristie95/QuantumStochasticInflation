"""An introductory, keyboard-controlled scene for paper_v2.tex."""

from manim import *
from manim_slides import Slide


class CoarseGraining(Slide):
    def construct(self):
        title = Text("Quantum Stochastic Inflation", font_size=46)
        subtitle = Text("From a quantum field to a coarse-grained patch", font_size=25)
        subtitle.next_to(title, DOWN, buff=0.4)
        self.play(FadeIn(title, shift=UP * 0.2), FadeIn(subtitle))
        self.next_slide()

        heading = Text("A moving cutoff", font_size=34).to_edge(UP)
        cutoff = MathTex(r"k_\sigma(N)", "=", r"\sigma a(N)H", font_size=56)
        self.play(FadeOut(title), FadeOut(subtitle), FadeIn(heading), Write(cutoff))
        self.next_slide()

        window = MathTex(
            r"\Theta_\sigma(N,k)", "=", r"\Theta\!\left(k_\sigma(N)-k\right)",
            font_size=48,
        ).next_to(cutoff, DOWN, buff=0.65)
        note = Text("Modes below the cutoff enter the patch", font_size=26, color=BLUE_B)
        note.next_to(window, DOWN, buff=0.45)
        self.play(Write(window), FadeIn(note))
        self.next_slide()

        q = MathTex(
            r"\hat Q_N(\mathbf x)", "=",
            r"\int\!\frac{d^3k}{(2\pi)^3}\,"
            r"\Theta_\sigma(N,k)\hat\Phi_{\mathbf k}(N)e^{i\mathbf k\cdot\mathbf x}",
            font_size=37,
        )
        p = MathTex(
            r"\hat P_N(\mathbf x)", "=",
            r"\mathtt{vol}_{\rm com}(N)\!\int\!\frac{d^3k}{(2\pi)^3}\,"
            r"\Theta_\sigma(N,k)\hat\Pi_{\mathbf k}(N)e^{i\mathbf k\cdot\mathbf x}",
            font_size=37,
        )
        equations = VGroup(q, p).arrange(DOWN, aligned_edge=LEFT, buff=0.55)
        new_heading = Text("The coarse-grained patch", font_size=34).to_edge(UP)
        self.play(FadeOut(cutoff), FadeOut(window), FadeOut(note),
                  Transform(heading, new_heading))
        self.play(Write(q))
        self.next_slide()
        self.play(Write(p))
        self.next_slide()

        commutator = MathTex(r"[\hat Q_N,\hat P_N]=i", font_size=48, color=YELLOW)
        commutator.next_to(equations, DOWN, buff=0.65)
        self.play(Write(commutator))
        self.next_slide()
