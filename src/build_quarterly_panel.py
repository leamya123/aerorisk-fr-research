"""Reproduce mixed-vintage BCEAO quarterly lending and quarter-end policy data.

Data sources are in data/official/. No forward filling of lending observations.
ECB/BCEAO *policy rates* are observed quarter-end levels, not quarterly means.
This script is descriptive and does not identify causal or structural effects.
Python 3.9+ / standard library only.
"""
import calendar
import csv
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOANS = ROOT / "data/official/bceao_lending_quarterly_2020q1_2026q2_selected_vintages.csv"
POLICY = ROOT / "data/processed/central_bank_policy_monthly_v1.csv"
OUTPUT = ROOT / "data/processed/quarterly_policy_lending_panel_v1.csv"
RATE_FIELDS = [
    "uemoa_lending_pct", "cote_divoire_lending_pct", "senegal_lending_pct",
    "ecb_dfr_quarter_end_pct", "bceao_tms_quarter_end_pct"
]
OUTPUT_FIELDS = [
    "quarter", *RATE_FIELDS,
    "delta_uemoa_lending_pp", "delta_cote_divoire_lending_pp",
    "delta_senegal_lending_pp", "delta_ecb_dfr_pp", "delta_bceao_tms_pp",
    "source_vintage", "quality_flag", "source_url", "source_printed_page"
]

def _load(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def _quarters():
    return [f"{y}-Q{q}" for y in range(2020, 2027)
            for q in range(1, 5) if y < 2026 or q <= 2]

def _end_date(quarter):
    year = int(quarter[:4])
    q = int(quarter[-1])
    month = 3*q
    return date(year, month, calendar.monthrange(year, month)[1]).isoformat()

def build(output=OUTPUT):
    loans = _load(LOANS)
    if [r["quarter"] for r in loans] != _quarters():
        raise ValueError("Expected 26 unique and consecutive quarters from 2020Q1 to 2026Q2")
    policy_months = _load(POLICY)
    policy = {r["month_end"]: r for r in policy_months}
    output_rows = []
    previous = None
    for loan in loans:
        if not loan["source_url"].startswith("https://"):
            raise ValueError("Every lending quarter requires a verifiable source URL")
        if loan["source_table"] != "3.1" or not loan["source_vintage"]:
            raise ValueError("Missing lending source vintage or table")
        p = policy.get(_end_date(loan["quarter"]))
        if p is None:
            raise ValueError("Missing policy level at " + loan["quarter"])
        numbers = {
            "uemoa_lending_pct":float(loan["uemoa_lending_pct"]),
            "cote_divoire_lending_pct":float(loan["cote_divoire_lending_pct"]),
            "senegal_lending_pct":float(loan["senegal_lending_pct"]),
            "ecb_dfr_quarter_end_pct":float(p["ecb_deposit_facility_pct"]),
            "bceao_tms_quarter_end_pct":float(p["bceao_minimum_bid_pct"]),
        }
        if any(not -5 <= v <= 30 for v in numbers.values()):
            raise ValueError("Rate outside validation range at " + loan["quarter"])
        output_record = {"quarter":loan["quarter"]}
        for key in RATE_FIELDS:
            output_record[key] = f"{numbers[key]:.2f}"
        for name,key in [
            ("delta_uemoa_lending_pp","uemoa_lending_pct"),
            ("delta_cote_divoire_lending_pp","cote_divoire_lending_pct"),
            ("delta_senegal_lending_pp","senegal_lending_pct"),
            ("delta_ecb_dfr_pp","ecb_dfr_quarter_end_pct"),
            ("delta_bceao_tms_pp","bceao_tms_quarter_end_pct")
        ]:
            output_record[name] = "" if previous is None else f"{numbers[key]-previous[key]:.2f}"
        for col in ["source_vintage","quality_flag","source_url","source_printed_page"]:
            output_record[col]=loan[col]
        output_rows.append(output_record)
        previous=numbers
    output.parent.mkdir(exist_ok=True,parents=True)
    with output.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(output_rows)
    print(f"Wrote {len(output_rows)} source-audited quarter-end observations to {output}")
    return output_rows

if __name__ == "__main__":
    build()
