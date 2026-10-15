"""Reproducible descriptive calculations on BCEAO annual lending rates.

Source: BCEAO 2025 annual banking-conditions report (pp. 23, 34, 46, 62).
Six annual observations (2020-2025); never interpret changes as a causal pass-through.
No third-party dependencies.
"""
import csv
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
INPUT=ROOT/"data/official/bceao_annual_lending_2020_2025.csv"
OUTPUT=ROOT/"data/processed/annual_lending_descriptives_v1.json"
SERIES={
 "uemoa_all_loans_pct":"UEMOA average: all lending",
 "cote_divoire_all_loans_pct":"Cote d'Ivoire average: all lending",
 "senegal_all_loans_pct":"Senegal average: all lending",
 "uemoa_nonfinancial_corporate_pct":"UEMOA: nonfinancial corporations",
 "uemoa_export_loans_pct":"UEMOA: export lending",
 "uemoa_equipment_loans_pct":"UEMOA: equipment lending",
 "uemoa_working_capital_loans_pct":"UEMOA: working-capital lending",
}

def compute():
    with INPUT.open("r",encoding="utf-8-sig",newline="") as f:
        records=list(csv.DictReader(f))
    years=[int(r["year"]) for r in records]
    if years!=list(range(2020,2026)):
        raise ValueError("Expected six strictly ordered annual observations (2020-2025)")
    for r in records:
        if "Rapport%20annuel%20Conditions%20de%20banque" not in r["source_url"]:
            raise ValueError("Wrong BCEAO source or missing citation")
        for k in SERIES:
            if not 0<float(r[k])<30:
                raise ValueError(f"Implausible percent rate: {k} for {r['year']}")
    before,after=records[-2:]
    return {
        "source_table":"BCEAO annual banking conditions report 2025; appendix 2020-2025",
        "start_year":2020,
        "end_year":2025,
        "n_annual_observations":len(records),
        "statistics": {
            k:{
                "description":label,
                "value_2024_pct":float(before[k]),
                "value_2025_pct":float(after[k]),
                "change_2024_to_2025_bp":round((float(after[k])-float(before[k]))*100)
            } for k,label in SERIES.items()
        },
        "interpretation_guardrail":"Annual descriptive group averages with varying composition. Do not use as asset-level lease price evidence or causal estimates."
    }

def write_report(out=OUTPUT):
    x=compute()
    out.parent.mkdir(exist_ok=True,parents=True)
    out.write_text(json.dumps(x,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"Wrote 2020-2025 annual rates summary to {out}")
    return x

if __name__=="__main__":
    write_report()
