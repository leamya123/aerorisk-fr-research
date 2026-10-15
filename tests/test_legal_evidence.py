"""LEGAL registry guardrails: official rules must never be typed as observed repossession."""
import csv
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
EVIDENCE=ROOT/"legal/evidence_registry_v1.csv"
CONTROLS=ROOT/"data/official/control_variable_source_registry_v1.csv"

def load(path):
    with path.open("r",encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))

class LegalResearchIntegrityTests(unittest.TestCase):
    def test_country_declaration_units_are_not_conflated(self):
        rows=load(EVIDENCE)
        by={row["record_id"]:row for row in rows}
        self.assertEqual(by["OHADA-AUVE-2024"]["rule_effective_date"],"2024-02-16")
        self.assertEqual(by["SEN-PROTOCOL-X-DE"]["deadline_unit"],"calendar_days")
        self.assertEqual(by["CIV-PROTOCOL-X-DE"]["deadline_unit"],"working_days")
        self.assertEqual(by["CIV-PROTOCOL-X-DE"]["rule_effective_date"],"2020-01-01")
        self.assertEqual(len(rows),5)

    def test_statutory_limits_are_never_observed_case_durations(self):
        for r in load(EVIDENCE):
            self.assertEqual(r["observed_case_days"],"",
                             "No aircraft case-level recovery times have been established")
            self.assertIn(r["record_type"],("treaty_declaration","enacted_rule"))
            self.assertTrue(r["source_url"].startswith("https://"))
        with (ROOT/"legal/case_coding_template_v1.csv").open("r",encoding="utf-8") as f:
            self.assertEqual(len(f.readlines()),1,
                             "A case record requires a verified court decision first")

    def test_controls_are_source_plans_not_collected_observations(self):
        controls=load(CONTROLS)
        self.assertGreaterEqual(len(controls),6)
        for r in controls:
            self.assertIn(r["status"],("to_collect","source_discovery"))
            self.assertTrue(r["official_source_url"].startswith("https://"))
if __name__=="__main__":
    unittest.main()
