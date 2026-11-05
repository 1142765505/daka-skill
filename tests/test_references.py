import sys
from pathlib import Path
import tempfile
import unittest
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from prepare_references import prepare

class ReferenceTests(unittest.TestCase):
    @unittest.skipUnless((ROOT/"references/private/identities/401/1-ref-1.png").is_file(),"Run build_library.py first")
    def test_selected_identity_supplement(self):
        with tempfile.TemporaryDirectory() as tmp:
            files=prepare("401",[1,4],Path(tmp)/"selected")
            self.assertEqual(len(files),2)
            for file in files:
                with Image.open(file) as im:
                    self.assertEqual(im.size,(640,400))
            # Other people must not accidentally inherit the 1/4 supplemental views.
            files=prepare("401",[2],Path(tmp)/"other")
            self.assertEqual(len(files),1)
            with Image.open(files[0]) as im:
                self.assertEqual(im.size,(320,400))

    @unittest.skipUnless((ROOT/"references/private/identities/401/9-ref-2.png").is_file(),"Run build_library.py first")
    def test_nine_has_two_supplemental_views(self):
        with tempfile.TemporaryDirectory() as tmp:
            files=prepare("401",[9],tmp)
            self.assertEqual(len(files),2)
            with Image.open(files[0]) as im:self.assertEqual(im.size,(320,400))
            with Image.open(files[1]) as im:self.assertEqual(im.size,(640,400))

if __name__=="__main__":unittest.main()
