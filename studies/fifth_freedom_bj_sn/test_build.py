import copy
import tempfile
import unittest
import shutil
from pathlib import Path
from build import ROOT, TABLES, load, validate, build

class EvidenceIntegrityTests(unittest.TestCase):
    def test_missing_source_is_rejected(self):
        data=load(); data['events'][0]['source_id']='MISSING'
        with self.assertRaises(ValueError): validate(data)

    def test_zero_does_not_replace_unknown_status(self):
        data=load(); data['events'][0]['authorization_evidence']='0'
        with self.assertRaises(ValueError): validate(data)

    def test_validation_preserves_unknown_and_dates(self):
        data=load(); before=copy.deepcopy(data); validate(data)
        self.assertEqual(data,before)

    def test_build_is_reproducible(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for name,_ in TABLES.values(): shutil.copyfile(ROOT/name,root/name)
            build(root)
            first={p.name:p.read_bytes() for p in (root/'outputs').iterdir()}
            build(root)
            self.assertEqual(first,{p.name:p.read_bytes() for p in (root/'outputs').iterdir()})

if __name__=='__main__': unittest.main()
