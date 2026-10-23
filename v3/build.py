"""Build the v3 presentation data snapshot and self-contained offline page.

No network calls and no third-party dependencies. Python 3.9+.
"""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'v3'
SOURCE=ROOT/'studies/fifth_freedom_bj_sn/outputs/evidence.json'
GENERATED=('data/evidence.json','data/evidence.js','offline.html','build-audit.json')

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

def build(output_dir=SITE,template_dir=SITE,source=SOURCE):
    evidence=json.loads(source.read_text(encoding='utf-8-sig'))
    validate(evidence)
    compact=json.dumps(evidence,ensure_ascii=False,indent=2)+'\n'
    _write(output_dir/'data/evidence.json',compact)
    _write(output_dir/'data/evidence.js','window.AERORISK_EVIDENCE = '+json.dumps(evidence,ensure_ascii=False,separators=(',',':'))+';\n')
    html=(template_dir/'index.html').read_text(encoding='utf-8')
    css=(template_dir/'styles.css').read_text(encoding='utf-8')
    app=(template_dir/'app.js').read_text(encoding='utf-8')
    data_js=(output_dir/'data/evidence.js').read_text(encoding='utf-8')
    offline=html.replace('<link rel="stylesheet" href="styles.css">','<style>\n'+css+'\n</style>')
    offline=offline.replace('<script src="data/evidence.js"></script>','<script>\n'+data_js+'\n</script>')
    offline=offline.replace('<script src="app.js"></script>','<script>\n'+app+'\n</script>')
    offline=offline.replace('href="data/evidence.json" download','href="#evidence"').replace('href="offline.html" download','href="#top"').replace('href="README.md"','href="#method"')
    _write(output_dir/'offline.html',offline)
    artifacts={name:_sha((output_dir/name).read_bytes()) for name in GENERATED if name!='build-audit.json'}
    audit={'source':str(source.relative_to(ROOT)).replace('\\','/'),'source_sha256':_sha(source.read_bytes()),'artifacts':artifacts,'guardrail':'Kenya Airways specific permit and local paid carriage remain UNKNOWN'}
    _write(output_dir/'build-audit.json',json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'site':'v3','counts':evidence['counts'],'generated':list(GENERATED)},ensure_ascii=False))
    return evidence

if __name__=='__main__':
    build()
