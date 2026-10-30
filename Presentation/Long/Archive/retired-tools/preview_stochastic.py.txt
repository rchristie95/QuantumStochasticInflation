"""Isolated preview of the production cutoff canvas, including its explanation pauses."""
from presentation_common import *
from sections.history import HistorySection, validate_model


class CutoffDraft(HistorySection,PresentationBase):
    def __init__(self,*args,**kwargs):
        config.tex_dir=str(ASSET_DIR.parent/'media'/'Tex')
        config.text_dir=str(ASSET_DIR.parent/'media'/'texts')
        kwargs.setdefault('output_folder',ASSET_DIR.parent/'previews'/'stochastic'/'slides')
        kwargs.setdefault('renderer',CachedRenderer(camera_class=PlotCamera))
        super().__init__(*args,**kwargs)

    def construct(self):
        self.camera.background_color=ManimColor(BG)
        self.chrome=VGroup();self.chrome_state=None;self.step_log=[];self.step_number=0
        self.cutoff_only=False
        self.motivation()
