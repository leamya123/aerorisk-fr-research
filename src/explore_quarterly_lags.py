"""EXPLORATORY quarter-to-quarter correlations; deliberately not causal 2SLS.

Question: do policy-level changes coincide with *observed bank loan-rate changes*?
Uses only first differences, no p values and no claims of identification.
The pre-analysis audit explicitly labels 2025Q1 high cross-vintage discrepancy.
For loan-rate comparisons, exclude 2025Q1 and 2025Q2 differences because
2025Q2 delta includes the controversial 2025Q1 lending observation.
For central-bank policy-only comparison, do not exclude these periods.
Lag k correlates current outcome ΔY_t with prior explanatory ΔX_(t-k).
"""
import csv
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PANEL=ROOT/"data/processed/quarterly_policy_lending_panel_v1.csv"

def load():
    with PANEL.open("r", encoding="utf-8", newline="") as f:
        records=list(csv.DictReader(f))
    if len(records)!=26:
        raise ValueError("Expected 26 quarterly observations.")
    return records

def lag_correlation(rows,outcome,explanatory,lag=0,exclude_revision=True):
    if not 0 <= lag <= 4:
        raise ValueError("Valid exploratory lags: 0 to 4 quarters")
    if explanatory not in rows[0] or outcome not in rows[0]:
        raise ValueError("Unknown variables")
    pairs=[]
    for t in range(1+lag,len(rows)):
        # 2025Q1 and Q2 have lending first differences exposed to the
        # unresolved 2025Q1 vintage discrepancy. Exclude both for lending.
        if exclude_revision and rows[t]["quarter"] in ("2025-Q1","2025-Q2"):
            continue
        a=rows[t][outcome]
        b=rows[t-lag][explanatory]
        if a=="" or b=="":
            continue
        pairs.append((float(a),float(b)))
    if len(pairs)<12:
        return {"lag_quarters":lag,"n":len(pairs),"pearson_r":None}
    a_mean=sum(p[0] for p in pairs)/len(pairs)
    b_mean=sum(p[1] for p in pairs)/len(pairs)
    cov=sum((p[0]-a_mean)*(p[1]-b_mean) for p in pairs)
    v1=sum((p[0]-a_mean)**2 for p in pairs)
    v2=sum((p[1]-b_mean)**2 for p in pairs)
    r=(cov/math.sqrt(v1*v2)) if v1>0 and v2>0 else None
    return {"lag_quarters":lag,"n":len(pairs),
            "pearson_r":None if r is None else round(r,3)}

def run():
    rows=load()
    pairs=[
        ("Policy ECB → BCEAO","delta_bceao_tms_pp","delta_ecb_dfr_pp",False),
        ("BCEAO → UEMOA lending","delta_uemoa_lending_pp","delta_bceao_tms_pp",True),
        ("BCEAO → Côte d'Ivoire lending","delta_cote_divoire_lending_pp","delta_bceao_tms_pp",True),
        ("BCEAO → Senegal lending","delta_senegal_lending_pp","delta_bceao_tms_pp",True)
    ]
    result={}
    for label,y,x,exclude in pairs:
        result[label]=[lag_correlation(rows,y,x,k,exclude) for k in (0,1,2)]
    return result

if __name__=="__main__":
    print("EXPORATORY ONLY: raw Pearson coefficients, no p values / causal interpretation")
    print("Loans exclude 2025Q1 and 2025Q2 changes due to vintage uncertainty.")
    for name,arr in run().items():
        print(name)
        for entry in arr:
            print(f"  lag {entry['lag_quarters']}q: r={entry['pearson_r']} (n={entry['n']})")
