import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'v3'))
from build import SITE, SOURCE, FINANCE_SOURCE, GENERATED, build, validate

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

    def test_finance_snapshot_preserves_source_values_and_metadata(self):
        import csv
        with FINANCE_SOURCE.open(encoding='utf-8-sig',newline='') as stream:
            expected=list(csv.DictReader(stream))
        script=(SITE/'data/finance.js').read_text(encoding='utf-8')
        snapshot=json.loads(script.removeprefix('window.AERORISK_FINANCE = ').rstrip().removesuffix(';'))
        self.assertEqual(snapshot['rows'],expected)
        chart=(SITE/'data/airline-financials.svg').read_text(encoding='utf-8')
        for row in expected:
            for field in ('revenue_billion_xof','net_income_billion_xof'):
                self.assertIn(row['fiscal_year']+' '+field+': '+row[field],chart)
        audit=json.loads((SITE/'build-audit.json').read_text(encoding='utf-8'))
        import hashlib
        self.assertEqual(audit['financial_source_sha256'],hashlib.sha256(FINANCE_SOURCE.read_bytes()).hexdigest())

    def test_offline_page_is_self_contained(self):
        page=(SITE/'offline.html').read_text(encoding='utf-8')
        self.assertIn('window.AERORISK_EVIDENCE',page)
        self.assertNotIn('src="data/evidence.js"',page)
        self.assertNotIn('href="styles.css"',page)
        self.assertIn('window.AERORISK_FINANCE',page)
        self.assertIn('Air Côte d’Ivoire revenue and net income',page)
        self.assertNotIn('src="data/finance.js"',page)
        self.assertNotIn('src="data/airline-financials.svg"',page)

if __name__=='__main__':unittest.main()
