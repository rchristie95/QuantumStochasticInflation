"""Foreground furniture survives cached clips and static/moving partitioning."""
import unittest
import numpy as np
from manim import Scene,Rectangle,Dot,tempconfig
from presentation_common import BG,PlotCamera,CachedRenderer


class ForegroundTests(unittest.TestCase):
    def test_foreground_is_composited_once_after_a_skipped_clip(self):
        with tempconfig({'pixel_width':160,'pixel_height':90,'background_color':BG,'dry_run':True}):
            renderer=CachedRenderer(camera_class=PlotCamera)
            scene=Scene(renderer=renderer)
            static=Dot([-2,0,0],color='#66B7FF')
            moving=Dot([2,0,0],color='#FFB569')
            furniture=Rectangle(width=9,height=.4,fill_color='#EDF3FA',fill_opacity=.4,stroke_width=0).shift([0,3,0])
            scene.add(static,moving)
            scene.add_foreground_mobject(furniture)
            renderer.skip_animations=True
            renderer.save_static_frame_data(scene,[static,furniture])
            renderer.update_frame(scene,mobjects=[moving])
            renderer.skip_animations=False
            renderer.save_static_frame_data(scene,[static,furniture])
            # Include the foreground twice through its family and its root, as
            # Manim can do during a reveal; it must still be painted once.
            renderer.update_frame(scene,mobjects=[moving,*furniture.get_family()])
            reference=PlotCamera()
            reference.capture_mobjects([static,moving,furniture])
            np.testing.assert_array_equal(renderer.get_frame(),reference.pixel_array)


if __name__=='__main__': unittest.main()
