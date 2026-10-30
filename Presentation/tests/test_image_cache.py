"""Replacing pixels at the same asset path must invalidate animation hashes."""
from pathlib import Path
import tempfile
import unittest
from PIL import Image
from manim import Camera
from manim.utils.hashing import get_hash_from_play_call
from sections.trajectories import wigner_image


class ImageCacheTests(unittest.TestCase):
    def test_same_path_with_new_pixels_changes_clip_hash(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/"plot.png"
            def clip_hash(color):
                Image.new("RGBA",(16,16),color).save(path)
                image=wigner_image(path)
                return get_hash_from_play_call(object(),Camera(pixel_width=32,pixel_height=32),[],[image])
            red=clip_hash("red")
            self.assertEqual(red,clip_hash("red"))
            self.assertNotEqual(red,clip_hash("blue"))


if __name__=="__main__": unittest.main()
