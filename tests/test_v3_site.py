import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'v3'))
from build import SITE, SOURCE, GENERATED, build, validate

class V3PresentationTests(unittest.TestCase):
    def test_contract_and_kq_guardrail(self):
        evidence=json.loads(SOURCE.read_text(encoding='utf-8-sig'))
        validate(evidence)
        kq=next(row for row in evidence['data']['chains'] if row['chain_id']=='CH01')
        self.assertEqual(kq['specific_permit'],'UNKNOWN')
        self.assertEqual(kq['local_paid_carriage'],'UNKNOWN')

    def test_page_has_four_required_sections_and_no_approval_claim(self):
        html=(SITE/'index.html').read_text(encoding='utf-8')
        for section in ('id="method"','id="legal"','id="evidence"','id="case"'):
            self.assertIn(section,html)
        self.assertIn('不可标为“许可已批准”',html)
        self.assertNotIn('class="good">许可已批准',html)

    def test_generated_site_is_reproducible(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)
            build(output_dir=out)
            for name in GENERATED:
                self.assertEqual((out/name).read_bytes(),(SITE/name).read_bytes(),name)

    def test_offline_page_is_self_contained(self):
        page=(SITE/'offline.html').read_text(encoding='utf-8')
        self.assertIn('window.AERORISK_EVIDENCE',page)
        self.assertNotIn('src="data/evidence.js"',page)
        self.assertNotIn('href="styles.css"',page)

if __name__=='__main__':unittest.main()
