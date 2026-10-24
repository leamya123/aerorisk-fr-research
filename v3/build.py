"""Build the v3 presentation data snapshot and self-contained offline page.

No network calls and no third-party dependencies. Python 3.9+.
"""
import csv
import html
import hashlib
import json
from urllib.parse import quote
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'v3'
SOURCE=ROOT/'studies/fifth_freedom_bj_sn/outputs/evidence.json'
FINANCE_SOURCE=ROOT/'data/official/airline_financials_candidate_v1.csv'
GENERATED=('data/evidence.json','data/evidence.js','data/finance.js','data/airline-financials.svg','offline.html','build-audit.json')

def _write(path,text):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(text.replace('\r\n','\n').encode('utf-8'))

def _sha(payload):
    return hashlib.sha256(payload).hexdigest()

def validate(evidence):
    required={'sources','events','routes','literature','articles','chains'}
    if set(evidence.get('counts',{}))!=required or set(evidence.get('data',{}))!=required:
        raise ValueError('Unexpected evidence contract')
    sources={row['document_id']:row for row in evidence['data']['sources']}
    if any(not row['official_url'].startswith('https://') for row in sources.values()):
        raise ValueError('Every presentation source requires an HTTPS official URL')
    for row in evidence['data']['articles']:
        if row['source_id'] not in sources:
            raise ValueError('Unresolved legal source '+row['source_id'])
    kq=next((row for row in evidence['data']['chains'] if row['chain_id']=='CH01'),None)
    if not kq or kq['specific_permit']!='UNKNOWN' or kq['local_paid_carriage']!='UNKNOWN':
        raise ValueError('KQ permit and local carriage must remain UNKNOWN until evidence is obtained')
    return sources

def financial_chart(rows):
    """A common zero-based numeric scale; exact amounts remain in the table."""
    from decimal import Decimal
    def y(value):
        return 405-(float(value)+40)/180*340
    svg=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 470" role="img" aria-labelledby="title desc">',
         '<title id="title">Air Côte d’Ivoire revenue and net income, 2019–2023</title>',
         '<desc id="desc">Billion nominal XOF. Paired bars on a common scale from -40 to 140. Source: DGPE state portfolio report, printed page 151. See accompanying exact-value table and precision notes.</desc>',
         '<rect width="1000" height="470" fill="#ffffff"/>',
         '<g font-family="sans-serif" font-size="16" fill="#102c38">',
         '<text x="20" y="26">Billion nominal XOF</text>',
         '<rect x="550" y="13" width="16" height="16" fill="#0b766f"/><text x="575" y="27">Revenue</text>',
         '<rect x="735" y="13" width="16" height="16" fill="#ffffff" stroke="#80571f" stroke-width="2"/><text x="760" y="27">Net income</text>']
    for tick in range(-40,141,20):
        yy=y(tick)
        svg.append(f'<line x1="75" x2="960" y1="{yy:.2f}" y2="{yy:.2f}" stroke="{("#60747b" if tick==0 else "#dce5e2")}"/><text x="60" y="{yy+5:.2f}" text-anchor="end">{tick}</text>')
    svg.append('<line x1="75" x2="75" y1="65" y2="405" stroke="#60747b"/>')
    for i,row in enumerate(rows):
        x=155+i*170
        for field,offset,color,fill in [('revenue_billion_xof',-46,'#0b766f','#0b766f'),('net_income_billion_xof',4,'#80571f','#ffffff')]:
            value=Decimal(row[field]); yy=y(value); zero=y(0)
            label=format(value.quantize(Decimal('0.01')),'f')
            label_y=yy-10 if value>=0 else yy+22
            svg.append(f'<rect x="{x+offset}" y="{min(yy,zero):.2f}" width="36" height="{abs(yy-zero):.2f}" fill="{fill}" stroke="{color}" stroke-width="2"><title>{html.escape(row["fiscal_year"]+" "+field+": "+row[field])}</title></rect>')
            svg.append(f'<text x="{x+offset+18}" y="{label_y:.2f}" text-anchor="middle">{label}</text>')
        svg.append(f'<text x="{x}" y="440" text-anchor="middle">{html.escape(row["fiscal_year"])}</text>')
    svg.append('</g></svg>')
    return ''.join(svg)+'\n'


def build(output_dir=SITE,template_dir=SITE,source=SOURCE):
    evidence=json.loads(source.read_text(encoding='utf-8-sig'))
    validate(evidence)
    with FINANCE_SOURCE.open(encoding='utf-8-sig',newline='') as stream:
        rows=list(csv.DictReader(stream))
    if [row['fiscal_year'] for row in rows]!=['2019','2020','2021','2022','2023']:
        raise ValueError('Financial coverage changed; review the presentation and DS contract before building')
    finance={'source':str(FINANCE_SOURCE.relative_to(ROOT)).replace('\\','/'), 'rows':rows}
    _write(output_dir/'data/finance.js','window.AERORISK_FINANCE = '+json.dumps(finance,ensure_ascii=False,separators=(',',':'))+';\n')
    chart=financial_chart(rows)
    _write(output_dir/'data/airline-financials.svg',chart)
    compact=json.dumps(evidence,ensure_ascii=False,indent=2)+'\n'
    _write(output_dir/'data/evidence.json',compact)
    _write(output_dir/'data/evidence.js','window.AERORISK_EVIDENCE = '+json.dumps(evidence,ensure_ascii=False,separators=(',',':'))+';\n')
    html=(template_dir/'index.html').read_text(encoding='utf-8')
    css=(template_dir/'styles.css').read_text(encoding='utf-8')
    app=(template_dir/'app.js').read_text(encoding='utf-8')
    data_js=(output_dir/'data/evidence.js').read_text(encoding='utf-8')
    offline=html.replace('<link rel="stylesheet" href="styles.css">','<style>\n'+css+'\n</style>')
    offline=offline.replace('<script src="data/evidence.js"></script>','<script>\n'+data_js+'\n</script>')
    offline=offline.replace('<script src="data/finance.js"></script>','<script>\n'+(output_dir/'data/finance.js').read_text(encoding='utf-8')+'\n</script>')
    import re
    offline=re.sub(r'<img class="finance-chart"[^>]*>', '<div class="finance-chart">'+chart+'</div>', offline)
    offline=offline.replace('<script src="app.js"></script>','<script>\n'+app+'\n</script>')
    # Offline controls must perform the action their label promises.
    offline=offline.replace('href="data/evidence.json" download',
                            'href="data:application/json;charset=utf-8,'+quote(compact,safe='')+'" download="evidence.json"')
    offline=offline.replace('href="offline.html" download>下载离线单页', 'href="#top">返回页首')
    offline=offline.replace('href="README.md">查看操作说明', 'href="#offline-help">查看离线说明')
    _write(output_dir/'offline.html',offline)
    artifacts={name:_sha((output_dir/name).read_bytes()) for name in GENERATED if name!='build-audit.json'}
    audit={'source':str(source.relative_to(ROOT)).replace('\\','/'),'source_sha256':_sha(source.read_bytes()),'financial_source':str(FINANCE_SOURCE.relative_to(ROOT)).replace('\\','/'),'financial_source_sha256':_sha(FINANCE_SOURCE.read_bytes()),'artifacts':artifacts,'guardrail':'Kenya Airways specific permit and local paid carriage remain UNKNOWN'}
    _write(output_dir/'build-audit.json',json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'site':'v3','counts':evidence['counts'],'generated':list(GENERATED)},ensure_ascii=False))
    return evidence

if __name__=='__main__':
    build()
