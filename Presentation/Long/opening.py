"""Continuous scene entry point; build_presentation.py retains animation caching."""
from presentation_common import *
from deck import SECTIONS
from sections.intro import IntroSection
from sections.collective import CollectiveSection
from sections.joint_state import JointStateSection
from sections.readout import ReadoutSection
from sections.trajectories import TrajectoriesSection
from sections.history import HistorySection
from sections.classical import ClassicalSection
from sections.canonical import CanonicalSection
from sections.continuum import ContinuumSection
from sections.boundary import BoundarySection
from sections.connection import ConnectionSection
from sections.massive import MassiveSection


class QuantumStochasticOpening(IntroSection,CollectiveSection,JointStateSection,ReadoutSection,TrajectoriesSection,HistorySection,ClassicalSection,CanonicalSection,ContinuumSection,BoundarySection,ConnectionSection,MassiveSection,PresentationBase):
    def construct(self):
        self.camera.background_color=ManimColor(BG)
        self.step_number=0
        self.step_log=[]
        self.chrome=VGroup()
        self.chrome_state=None
        only=os.environ.get("QSI_ONLY_SECTION")
        if context_file:=os.environ.get("QSI_CONTEXT_FILE"):
            self.restore_canvas(json.loads(Path(context_file).read_text()))
        selected=[section for section in SECTIONS if not only or section.id==only]
        for section in selected:
            self.active_section=section.id
            if section.chapter:
                self.title_page(*section.chapter)
            for method in (() if os.environ.get("QSI_DIVIDER_ONLY")=="1" else section.methods):
                getattr(self,method)()
        if selected[-1].id==SECTIONS[-1].id:
            self.wait(.3)
        self.step_log[-1]["end_animation"]=self.renderer.num_plays
        if result_file:=os.environ.get("QSI_RESULT_FILE"):
            Path(result_file).write_text(json.dumps({"steps":self.step_log,"chrome":self.chrome_state},indent=2))
        elif not os.environ.get("QSI_BUILD"):
            Path("media").mkdir(exist_ok=True)
            Path("media/opening_steps.json").write_text(json.dumps(self.step_log,indent=2))

    def collective(self):
        """Compatibility helper for isolated oscillator previews."""
        self.collective_definitions()
        self.joint_wigner_example()
        self.collective_povms()
        self.oscillator_trajectories()
