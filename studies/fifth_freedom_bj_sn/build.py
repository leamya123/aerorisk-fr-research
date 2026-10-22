"""Build inspectable midterm evidence tables using only Python's standard library.

Structural validation is not legal verification. No network calls or imputed facts.
"""
import csv
import hashlib
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
TABLES = {
    'sources': ('official_source_registry.csv', 'document_id'),
    'events': ('policy_events.csv', 'event_id'),
    'routes': ('route_evidence_audit.csv', 'route_id'),
    'literature': ('literature_gap_matrix.csv', 'literature_id'),
    'articles': ('legal_article_matrix.csv', 'row_id'),
    'chains': ('evidence_chain_and_gaps.csv', 'chain_id'),
}

def load(root=ROOT):
    data = {}
    for key, (filename, primary_key) in TABLES.items():
        with (root / filename).open(encoding='utf-8-sig', newline='') as stream:
            data[key] = list(csv.DictReader(stream))
        ids = [row[primary_key] for row in data[key]]
        if not all(ids) or len(set(ids)) != len(ids):
            raise ValueError(f'{key}: empty or duplicate identifier')
    return data

def validate(data):
    ids = {row['document_id'] for row in data['sources']}
    for key in ('events', 'routes', 'articles'):
        for row in data[key]:
            if row['source_id'] not in ids:
                raise ValueError(f'{key}: unresolved source {row["source_id"]}')
    for row in data['chains']:
        if not set(row['source_ids'].split(';')) <= ids:
            raise ValueError('chains: unresolved source')
    for row in data['sources']:
        if urlparse(row['official_url']).scheme not in ('http', 'https'):
            raise ValueError('sources: invalid URL format')
    statuses = {'DIRECT','REPORTED','SECONDARY','PLANNED','UNKNOWN','EXPLICIT_NOT_IMPLEMENTED','NA'}
    for row in data['events']:
        for key in ('legal_commitment','domestic_measure','authorization_evidence','operational_evidence'):
            if row[key] not in statuses:
                raise ValueError(f'events: invalid status {row[key]}')
    return {key: len(rows) for key, rows in data.items()}

def table(rows, fields):
    def cell(value):
        return str(value).replace('|', '\\|').replace('\n', ' ')
    lines = ['| ' + ' | '.join(fields) + ' |', '| ' + ' | '.join('---' for _ in fields) + ' |']
    return '\n'.join(lines + ['| ' + ' | '.join(cell(row.get(f,'')) for f in fields) + ' |' for row in rows])

def build(root=ROOT):
    data = load(root)
    counts = validate(data)
    output = root / 'outputs'
    output.mkdir(exist_ok=True)
    snapshot = {'evidence_cutoff':'2026-10-19','packaging_date':'2026-10-22',
                'decision':'CONDITIONAL GO; scope B', 'counts':counts, 'data':data}
    (output/'evidence.json').write_text(json.dumps(snapshot, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    for name,key,fields in [
        ('legal_comparison.md','articles',['row_id','country','article','paired_article','comparative_finding','interpretation_boundary','source_id','source_locator']),
        ('route_gaps.md','chains',['chain_id','carrier','candidate_foreign_segment','specific_ASA_terms','specific_permit','operation','gap']),
        ('source_index.md','sources',['document_id','original_title','verification_status','official_url','relevant_page_or_article'])]:
        (output/name).write_text('# '+name.removesuffix('.md')+'\n\n'+table(data[key],fields)+'\n',encoding='utf-8')
    hashes = {name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name,_ in TABLES.values()}
    (output/'audit.json').write_text(json.dumps({'counts':counts,'input_sha256':hashes,
        'checks':'IDs, references, URL syntax, status vocabulary',
        'not_checked':'URL availability, current legal validity, independent translation, novelty, real route operation'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(counts,ensure_ascii=False))
    return counts

if __name__ == '__main__':
    build()
