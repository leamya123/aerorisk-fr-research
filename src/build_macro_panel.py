"""Build documented end-of-month central-bank policy rate levels from event records.

The public CSVs in data/official/ are transcriptions of ECB/BCEAO source tables.
This script preserves policy effective dates and carries forward the policy level;
it does NOT statistically interpolate or estimate unobserved monetary outcomes.
BEAC is intentionally excluded until its entire comparable series is verified.

Usage: python src/build_macro_panel.py
Requirements: Python >= 3.9 standard library.
"""
import csv
import calendar
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ECB = ROOT / "data/official/ecb_policy_events.csv"
BCEAO = ROOT / "data/official/bceao_policy_events.csv"
OUT = ROOT / "data/processed/central_bank_policy_monthly_v1.csv"

def read_events(file_path, value_columns):
    with file_path.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise ValueError(f"No source events: {file_path}")
    prev = None
    result = []
    for row in rows:
        event_date = date.fromisoformat(row["effective_date"])
        if prev is not None and event_date <= prev:
            raise ValueError(f"Effective dates out of order: {file_path}")
        vals = [float(row[c]) for c in value_columns]
        if any(not (-100 < x < 100) for x in vals):
            raise ValueError("Implausible policy rate")
        if not row.get("source_url", "").startswith("https://"):
            raise ValueError("Source URL missing")
        result.append((event_date, *vals))
        prev = event_date
    return result

def lookup(events, cutoff):
    levels = [row[1:] for row in events if row[0] <= cutoff]
    if not levels:
        raise ValueError("Missing initial rate at " + str(cutoff))
    return levels[-1]

def build(start=(2020, 1), end=(2026, 9), output=OUT):
    ecb = read_events(ECB, ["deposit_facility_rate_pct", "main_refinancing_rate_pct"])
    bceao = read_events(BCEAO, ["minimum_bid_rate_pct", "marginal_lending_rate_pct"])
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["month_end", "ecb_deposit_facility_pct", "ecb_mro_pct",
                         "bceao_minimum_bid_pct", "bceao_marginal_lending_pct"])
        count = 0
        for year in range(start[0], end[0] + 1):
            for month in range(1, 13):
                if (year, month) < start or (year, month) > end:
                    continue
                cutoff = date(year, month, calendar.monthrange(year, month)[1])
                writer.writerow([cutoff.isoformat(), *[f"{rate:.2f}" for rate in
                    (*lookup(ecb, cutoff), *lookup(bceao, cutoff))]])
                count += 1
    print(f"Wrote {count} verified end-of-month policy-rate rows to {output}")
    return count

if __name__ == "__main__":
    build()
