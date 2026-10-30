"""Exercise cache invalidation and safe publication without rendering video."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import incremental_build as build
from deck import Section


class IncrementalBuildTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.sections=(Section("a",("first",)),Section("b",("second",)))
        for name in build.SHARED+("sections/a.py","sections/b.py"):
            path=self.root/name
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text("original")
        for name,value in (("ROOT",self.root),("SECTIONS",self.sections)):
            replacement=patch.object(build,name,value)
            replacement.start();self.addCleanup(replacement.stop)
        # main() changes cwd, so restore it before TemporaryDirectory cleanup.
        import os
        cwd=Path.cwd()
        self.addCleanup(os.chdir,cwd)
        self.rendered=[]

    def worker(self,section,profile,folder,context):
        self.rendered.append(section.id)
        # End frames remain unchanged when only an earlier caption is edited.
        frame=self.root/f"{profile}-{section.id}.png"
        frame.write_bytes(b"end frame")
        movie=self.root/f"{profile}-{section.id}.mp4"
        movie.write_bytes(b"clip")
        step={"title":section.id,"notes":section.id,"step":1}
        record={"fingerprint":build.fingerprint(section,profile),"incoming":context,
                "frame":frame.name,"chrome":None,"steps":[step],
                "slides":[{"file":movie.name,"rev_file":movie.name,"notes":section.id}]}
        return record,{"section":section.id}

    def run_build(self,*args):
        with patch.object(build,"render_section",side_effect=self.worker),contextlib.redirect_stdout(io.StringIO()):
            build.main(list(args))

    def test_local_edit_noop_and_deleted_output(self):
        self.run_build()
        self.assertEqual(self.rendered,["a","b"])
        self.rendered.clear()
        self.run_build()
        self.assertEqual(self.rendered,[])
        (self.root/"sections/a.py").write_text("changed caption")
        self.run_build()
        self.assertEqual(self.rendered,["a"])
        self.rendered.clear()
        (self.root/"final-b.mp4").unlink()
        self.run_build()
        self.assertEqual(self.rendered,["b"])

    def test_shared_change_invalidates_both_sections(self):
        self.run_build();self.rendered.clear()
        (self.root/"presentation_common.py").write_text("new style")
        self.run_build()
        self.assertEqual(self.rendered,["a","b"])

    def test_incoming_frame_change_invalidates_successor(self):
        self.run_build();self.rendered.clear()
        path=self.root/"media/build/final/manifest.json"
        manifest=json.loads(path.read_text())
        (self.root/"new-frame.png").write_bytes(b"new terminal frame")
        manifest["sections"]["a"]["frame"]="new-frame.png"
        build.atomic_json(path,manifest)
        self.run_build()
        self.assertEqual(self.rendered,["b"])

    def test_preview_preserves_final_deck_and_notes(self):
        self.run_build()
        final=self.root/"slides/QuantumStochasticOpening.json"
        notes=self.root/"media/opening_steps.json"
        before=(final.read_bytes(),notes.read_bytes())
        self.rendered.clear()
        self.run_build("--preview","b")
        self.assertEqual(self.rendered,["b"])
        self.assertEqual(before,(final.read_bytes(),notes.read_bytes()))
        self.assertTrue((self.root/"slides/QuantumStochasticOpening-preview.json").is_file())
        self.assertEqual([entry["step"] for entry in json.loads(notes.read_text())],[1,2])

    def test_failed_render_preserves_published_deck(self):
        self.run_build()
        final=self.root/"slides/QuantumStochasticOpening.json"
        before=final.read_bytes()
        with patch.object(build,"render_section",side_effect=RuntimeError("worker failed")),contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(RuntimeError): build.main(["--force"])
        self.assertEqual(before,final.read_bytes())


if __name__=="__main__": unittest.main()
