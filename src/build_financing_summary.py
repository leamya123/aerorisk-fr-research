"""Rebuild strictly descriptive BCEAO financing statistics from transcribed official tables.

Source: BCEAO Bulletin Trimestriel des Statistiques, T1 2026, pp. 4 & 12.
No regressions, causal claims, invented asset-level observations or interpolation.
Python >=3.9, standard library only.
"""
import csv
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUCTIONS = ROOT/"data/official/bceao_weekly_auction_monthly.csv"
BANKS = ROOT/"data/official/bceao_bank_lending_quarterly.csv"
POLICY = ROOT/"data/processed/central_bank_policy_monthly_v1.csv"
OUT = ROOT/"data/processed/financing_descriptives_v1.json"

NOTE = ("Descriptive endpoint differences, not monetary policy causal effects, "
        "exchange rate pass-through or aircraft leasing rates.")

def _read(path):
    with path.open(encoding="utf-8-sig",newline="") as f:
        rows=list(csv.DictReader(f))
    if not rows:
        raise ValueError("Missing source rows: "+str(path))
    return rows

def _months_between(start, end):
    y,m=map(int,start.split("-"))
    ey,em=map(int,end.split("-"))
    ret=[]
    while (y,m)<=(ey,em):
        ret.append(f"{y:04d}-{m:02d}")
        m+=1
        if m==13:y+=1;m=1
    return ret

def build(out=OUT):
    auction=_read(AUCTIONS)
    bank=_read(BANKS)
    policy=_read(POLICY)
    am={r["month"]:r for r in auction}
    bm={r["quarter"]:r for r in bank}
    pm={r["month_end"][:7]:r for r in policy}
    months=_months_between("2024-07","2026-03")
    quarters=["2024-Q4","2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1"]
    if list(am)!=months or list(bm)!=quarters:
        raise ValueError("Unexpected periods or missing data; never interpolate missing values.")
    if not set(months).issubset(pm):
        raise ValueError("Missing policy-month matches.")
    for r in auction+bank:
        if not r["source_url"].startswith("https://www.bceao.int/"):
            raise ValueError("Untraceable BCEAO record.")
        for key,value in r.items():
            if key.endswith("_pct") and not 0<=float(value)<=30:
                raise ValueError("Financing rate outside plausible published range.")

    def auction_rate(month):
        return float(am[month]["one_week_auction_weighted_average_pct"])
    def min_bid(month):
        return float(pm[month]["bceao_minimum_bid_pct"])
    def bank_rate(q,key):
        return float(bm[q][key])

    output={
        "auction_count":len(auction),
        "bank_lending_quarter_count":len(bank),
        "auction_2024_07_rate_pct":auction_rate("2024-07"),
        "auction_2026_03_rate_pct":auction_rate("2026-03"),
        "auction_change_2024_07_to_2026_03_bp":round((auction_rate("2026-03")-auction_rate("2024-07"))*100,1),
        "policy_bceao_2024_07_pct":min_bid("2024-07"),
        "policy_bceao_2026_03_pct":min_bid("2026-03"),
        "policy_change_bp":int(round((min_bid("2026-03")-min_bid("2024-07"))*100)),
        "auction_minus_policy_spread_2024_07_bp":int(round((auction_rate("2024-07")-min_bid("2024-07"))*100)),
        "auction_minus_policy_spread_2026_03_bp":round((auction_rate("2026-03")-min_bid("2026-03"))*100,1),
        "bank_uemoa_2024_q4_pct":bank_rate("2024-Q4","uemoa_avg_bank_lending_pct"),
        "bank_uemoa_2026_q1_pct":bank_rate("2026-Q1","uemoa_avg_bank_lending_pct"),
        "bank_uemoa_change_2024q4_to_2026q1_bp":int(round((bank_rate("2026-Q1","uemoa_avg_bank_lending_pct")-bank_rate("2024-Q4","uemoa_avg_bank_lending_pct"))*100)),
        "bank_senegal_2025_q3_pct":bank_rate("2025-Q3","senegal_avg_bank_lending_pct"),
        "bank_senegal_2025_q4_pct":bank_rate("2025-Q4","senegal_avg_bank_lending_pct"),
        "bank_cote_divoire_2025_q3_pct":bank_rate("2025-Q3","cote_divoire_avg_bank_lending_pct"),
        "bank_cote_divoire_2025_q4_pct":bank_rate("2025-Q4","cote_divoire_avg_bank_lending_pct"),
        "note":NOTE
    }
    out.parent.mkdir(exist_ok=True,parents=True)
    out.write_text(json.dumps(output,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"Verified {len(auction)} monthly auction observations and {len(bank)} quarters. Saved {out}")
    return output

if __name__=="__main__":
    build()
