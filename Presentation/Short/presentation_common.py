"""Keyboard-controlled opening for paper_v2.tex (Manim 0.19 / Manim Slides 5.7).

Render from this Presentation directory. See README.md.
"""
import os
from pathlib import Path
import json

import numpy as np
from manim import *
from manim_slides import Slide
from manim.renderer.cairo_renderer import CairoRenderer
from manim.scene.scene_file_writer import SceneFileWriter
import mpmath as mp
import qrcode
from PIL import Image as PILImage
from scipy.linalg import expm, solve_continuous_lyapunov
from oscillator_states import canonical_map, make_assets


BG = "#101824"
INK = "#EDF3FA"
MUTED = "#A9B7CB"
BULK = "#66B7FF"
SHELL = "#FFB569"
MIX = "#B8A1EF"
GREEN = "#80DDB5"
ASSET_DIR = Path(__file__).resolve().parent / "assets"
PAPER_URL = "https://arxiv.org/abs/2606.12636"
from deck import CHAPTERS
from slide_numbering import slide_map, SLIDE_STARTS

TEMPLATE = TexTemplate()
TEMPLATE.add_to_preamble(r"\newcommand{\ket}[1]{\lvert #1\rangle}"
                         r"\newcommand{\bra}[1]{\langle #1\rvert}"
                         r"\newcommand{\Tr}{\operatorname{Tr}}")


def text_line(s, size=26, color=INK, width=12):
    obj = Text(s, font="DejaVu Sans", font_size=size, color=color)
    if obj.width > width:
        obj.scale_to_fit_width(width)
    return obj


def equation(*parts, size=37, color=INK, width=12):
    obj = MathTex(*parts, font_size=size, color=color, tex_template=TEMPLATE)
    if obj.width > width:
        obj.scale_to_fit_width(width)
    return obj


def simulated_paths(seed=1986, paths=120, steps=120, duration=6, alpha=0.03):
    """Dimensionless light-field OU illustration; first path is reused verbatim."""
    rng = np.random.default_rng(seed)
    dt = duration / steps
    dw = rng.normal(0, np.sqrt(dt), (paths, steps))
    values = np.zeros((paths, steps + 1))
    for j in range(steps):
        values[:, j + 1] = values[:, j] * (1 - alpha * dt) + dw[:, j]
    return np.linspace(0, duration, steps + 1), values, dw


def massive_covariances(mass, sigma=.1, times=None):
    """Paper's exact de Sitter coefficients, H=1, N=0, canonical scaled axes.

    X=sqrt(m Vphys) Q, Y=P/sqrt(m Vphys). Initial covariance I/2 is the
    ground state of the bulk Hamiltonian without its redefinition term.
    """
    times = np.linspace(0,40,161) if times is None else np.asarray(times)
    with mp.workdps(40):
        nu=mp.sqrt(mp.mpf('2.25')-mass**2)
        phase=mp.exp(1j*mp.pi*(2*nu+1)/4)
        phi=complex(mp.sqrt(mp.pi)/2*phase*mp.hankel1(nu,sigma))
        pi=complex(-mp.sqrt(mp.pi)/2*phase*(sigma*mp.hankel1(nu-1,sigma)+(mp.mpf('1.5')-nu)*mp.hankel1(nu,sigma)))
    volume=6*np.pi**2/sigma**3
    scale=np.diag([np.sqrt(mass*volume),1/np.sqrt(mass*volume)])
    diffusion=scale@(3*np.array([[abs(phi)**2/volume,np.real(np.conj(phi)*pi)],
                                [np.real(np.conj(phi)*pi),volume*abs(pi)**2]]))@scale.T
    drift=np.array([[0,mass],[-mass,-3.]])
    stationary=solve_continuous_lyapunov(drift,-diffusion)
    stationary=(stationary+stationary.T)/2
    covariances=np.array([stationary+expm(drift*t)@(.5*np.eye(2)-stationary)@expm(drift.T*t) for t in times])
    purity=1/(2*np.sqrt(np.linalg.det(covariances)))
    return times,covariances,purity,stationary,drift,diffusion,phi,pi


def collective_map(n):
    """Average coordinate / total momentum, plus a canonical relative pair.

    Order: (Q_n, q_new, P_n, p_new). Positions transform with A;
    momenta transform with A^{-T}, not with the same Euclidean rotation.
    """
    a=np.array([[n/(n+1),1/(n+1)],[1.,-1.]])
    b=np.linalg.inv(a).T
    return np.block([[a,np.zeros((2,2))],[np.zeros((2,2)),b]])


class PlotCamera(Camera):
    """Axis-aligned scientific raster plots, compatible with pinned Manim/Pillow.

    Manim 0.19 constructs a float zero array with mode RGBA, unsupported by
    Pillow 13. A real transparent RGBA canvas keeps the installed pins intact.
    """
    def display_image_mobject(self,image_mobject,pixel_array):
        ul,ur,dl,_=self.points_to_pixel_coords(image_mobject,image_mobject.points)
        if abs(ur[1]-ul[1])>1 or abs(dl[0]-ul[0])>1:
            raise ValueError("Scientific plot images must remain axis-aligned")
        size=(max(int(np.linalg.norm(ur-ul)),1),max(int(np.linalg.norm(dl-ul)),1))
        image=PILImage.fromarray(image_mobject.get_pixel_array()).resize(size,resample=image_mobject.resampling_algorithm)
        canvas=PILImage.new('RGBA',(self.pixel_width,self.pixel_height),(0,0,0,0))
        canvas.paste(image,tuple(np.rint(ul).astype(int)))
        self.overlay_PIL_image(pixel_array,canvas)


class SectionFileWriter(SceneFileWriter):
    def finish(self):
        # Slides exports its own forward/reverse clips from the partial movies.
        # A second, monolithic movie is unused by the presenter. Besides adding
        # work, Manim 0.19's redundant concat can fail on valid cached timestamps.
        pass


class CachedRenderer(CairoRenderer):
    """Cached/skipped clips need final object states, not static raster paints."""
    def __init__(self,*args,**kwargs):
        kwargs.setdefault("file_writer_class",SceneFileWriter if os.environ.get("QSI_CONTINUOUS")=="1" else SectionFileWriter)
        super().__init__(*args,**kwargs)

    def save_static_frame_data(self,scene,static_mobjects):
        if self.skip_animations:
            self.static_image=None
            # The camera creates its dispatch table lazily on the first paint.
            # Initialize the same table without painting, so skipping the first
            # cached clip does not change the camera hash of the second clip.
            if not hasattr(self.camera,"display_funcs"):
                self.camera.type_or_raise(Mobject())
            return None
        # Foreground furniture must be composited once after the moving layer.
        # In particular it must never be baked into a static image that Cairo
        # may replace while a cached animation is skipped.
        foreground={id(m) for root in scene.foreground_mobjects for m in root.get_family()}
        static_mobjects=[m for m in static_mobjects if id(m) not in foreground]
        self.static_image=None
        if static_mobjects:
            super().update_frame(scene,mobjects=static_mobjects)
            self.static_image=self.get_frame()
        return self.static_image

    def update_frame(self,scene,mobjects=None,**kwargs):
        if not self.skip_animations:
            foreground={id(m) for root in scene.foreground_mobjects for m in root.get_family()}
            moving=list(mobjects) if mobjects else list(scene.mobjects)
            moving=[m for m in moving if id(m) not in foreground]
            moving.extend(scene.foreground_mobjects)
            return super().update_frame(scene,mobjects=moving,**kwargs)


class PresentationBase(Slide):
    """Shared visuals for one continuous scene with numbered reveals."""

    def __init__(self,*args,**kwargs):
        kwargs.setdefault("camera_class",PlotCamera)
        if os.environ.get("QSI_BUILD"):
            kwargs.setdefault("output_folder",Path(os.environ["QSI_OUTPUT_FOLDER"]))
            config.disable_caching=False
            config.tex_dir=str(ASSET_DIR.parent/"media"/"Tex")
            config.text_dir=str(ASSET_DIR.parent/"media"/"texts")
            kwargs.setdefault("renderer",CachedRenderer(camera_class=PlotCamera,skip_animations=kwargs.get("skip_animations",False)))
        self.skip_reversing=os.environ.get("QSI_PREVIEW")=="1"
        super().__init__(*args,**kwargs)

    def step(self,title,note):
        self.next_slide(notes=note)
        if self.step_log:
            self.step_log[-1]["end_animation"]=self.renderer.num_plays
        self.step_number+=1
        if os.environ.get("QSI_CONTINUOUS")=="1":
            if hasattr(self,"slide_counter"):
                self.remove_foreground_mobject(self.slide_counter)
                self.remove(self.slide_counter)
            number=slide_map()[title]
            self.slide_counter=text_line(f"{number} / {len(SLIDE_STARTS)}",17,MUTED).move_to([0,-3.55,0])
            self.add_foreground_mobject(self.slide_counter)
        self.step_log.append({"step":self.step_number,"title":title,"notes":note,
                              "section":getattr(self,"active_section","preview"),
                              "start_animation":self.renderer.num_plays})

    def section(self, number, title):
        self.clear_content()
        self.set_chrome(number,title)

    def set_chrome(self,number,title):
        """Recreate the heading/footer without adding a transition or a step."""
        if len(self.chrome):
            self.remove(self.chrome)
        heading = text_line(title, 34).move_to([0, 3.25, 0])
        rule = Line([-6.3, 2.83, 0], [6.3, 2.83, 0], color=MUTED, stroke_opacity=0.3)
        chapter = text_line(f"{number:02} / {len(CHAPTERS):02}", 17, MUTED).move_to([-5.85, -3.55, 0])
        self.chrome = VGroup(heading, rule, chapter)
        # Keep presentation furniture in the foreground render set. Cairo's
        # static-frame cache can otherwise omit it after cached transforms.
        self.add_foreground_mobject(self.chrome)
        self.chrome_state=[number,title]

    def restore_canvas(self,context):
        """A frozen body plus native furniture preserves the preceding fade."""
        if context.get("chrome"):
            self.set_chrome(*context["chrome"])
        if context.get("frame"):
            pixels=np.array(PILImage.open(context["frame"]).convert("RGBA"))
            if context.get("chrome"):
                # Existing content stays below the rule and above the footer.
                pixels[:round(.17*len(pixels)),:,:3]=[16,24,36]
                pixels[round(.925*len(pixels)):,:,:3]=[16,24,36]
            body=ImageMobject(pixels).stretch_to_fit_width(config.frame_width).stretch_to_fit_height(config.frame_height)
            # Manim intentionally excludes pixel arrays from its hashes. Include
            # the immutable source-frame digest so changed incoming fades rebuild.
            body.source_frame_digest=Path(context["frame"]).stem
            self.add(body)


    def title_page(self, number, title, subtitle):
        self.step(title+" / chapter", subtitle)
        self.clear_content()
        self.remove(self.chrome)
        self.chrome=VGroup()
        self.add(self.chrome)
        self.chrome_state=None
        numeral=text_line(f"0{number}",94,MIX).move_to([0,1.25,0])
        name=text_line(title,46,width=12.4).move_to([0,-.05,0])
        rule=Line([-2.5,-.8,0],[2.5,-.8,0],color=BULK)
        sub=text_line(subtitle,25,MUTED).move_to([0,-1.55,0])
        self.play(FadeIn(numeral,shift=UP*.2),Write(name),Create(rule),FadeIn(sub),run_time=1.3)
        self.hold()


    def clear_content(self):
        current = [m for m in self.mobjects if m is not self.chrome and m is not getattr(self,"slide_counter",None)]
        if current:
            self.play(*[FadeOut(m) for m in current], run_time=0.5)


    def hold(self):
        self.wait(0.35)


    def oscillator(self, x, color, name):
        rail=Line([x-.75,0,0],[x+.75,0,0],color=MUTED)
        bob=Dot([x,0,0],radius=.13,color=color)
        spring=VMobject(color=color).set_points_as_corners([[x-.75,0,0],[x-.6,.1,0],[x-.45,-.1,0],[x-.3,.1,0],[x-.15,-.1,0],[x,0,0]])
        label=equation(name,size=29,color=color).move_to([x,-.55,0])
        return VGroup(rail,spring,bob,label)


    def contour(self, covariance, center, color, scale=1.25):
        vals,vecs=np.linalg.eigh(covariance)
        angles=np.linspace(0,TAU,121)
        # Symmetric square root keeps vertex correspondence consistent across
        # covariance changes (eigenvector ordering otherwise flips the contour).
        pts=(vecs@np.diag(np.sqrt(vals))@vecs.T)@np.array([np.cos(angles),np.sin(angles)])
        shape=VMobject(color=color,fill_color=color,fill_opacity=.13,stroke_width=3)
        shape.set_points_as_corners([np.array(center)+scale*np.array([p[0],p[1],0]) for p in pts.T])
        return shape


    def mode_card(self, x, y, color, label, symbol):
        disk=Circle(radius=.7,color=color,fill_opacity=.16).move_to([x,y,0])
        sym=equation(symbol,size=31,color=color).move_to(disk)
        caption=text_line(label,21,color,width=3.1).move_to([x,y-1.05,0])
        return VGroup(disk,sym,caption)


    def figure_pair(self):
        retained=self.mode_card(-2.4,.8,MIX,"Redefined bulk",r"\parallel")
        decoupled=self.mode_card(2.4,.8,SHELL,"Decoupled mode",r"\perp")
        connector=DoubleArrow(retained[0].get_right(),decoupled[0].get_left(),buff=.12,color=MUTED)
        ent=text_line("entangled",22,MUTED).next_to(connector,UP,buff=.15)
        return VGroup(retained,decoupled,connector,ent)

