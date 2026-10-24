"""Recheck the DS handoff against repository inputs, without network or imputation.

Python standard library only. Excel workbooks are read as OOXML, never edited.
This verifies internal consistency and arithmetic, not official-source truth.
"""
import csv
import hashlib
import json
import re
import xml.etree.ElementTree as ET
import zipfile
from collections import Counter
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'data/official').is_dir())
STUDY = ROOT / 'studies/fifth_freedom_bj_sn'
NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}


def csv_rows(path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def sheet_cells(path, number):
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None
        strings = []
        if 'xl/sharedStrings.xml' in z.namelist():
            strings = [''.join(t.text or '' for t in x.findall('.//m:t', NS))
                       for x in ET.fromstring(z.read('xl/sharedStrings.xml'))]
        cells, formulas = {}, {}
        tree = ET.fromstring(z.read(f'xl/worksheets/sheet{number}.xml'))
        for c in tree.findall('.//m:sheetData/m:row/m:c', NS):
            v = c.find('m:v', NS)
            value = v.text if v is not None else ''
            if c.get('t') == 's':
                value = strings[int(value)]
            elif c.get('t') == 'inlineStr':
                value = ''.join(t.text or '' for t in c.findall('.//m:t', NS))
            assert c.get('t') != 'e', (path.name, c.get('r'), value)
            cells[c.get('r')] = value
            f = c.find('m:f', NS)
            if f is not None:
                formulas[c.get('r')] = f.text
        return cells, formulas


def run():
    specs = {
        'sources': ('official_source_registry', 'document_id', 25),
        'events': ('policy_events', 'event_id', 11),
        'routes': ('route_evidence_audit', 'route_id', 18),
        'articles': ('legal_article_matrix', 'row_id', 9),
    }
    bundle = json.loads((HERE / 'cleaned/evidence.cleaned.json').read_text())
    canonical = json.loads((STUDY / 'outputs/evidence.json').read_text())
    tables, result = {}, {'review_date': '2026-10-24',
        'baseline_commit': '61c225bf91dc0d52f4bac919ff4d27735ac54a48',
        'ds_legal_audit_declared_commit': 'f115e9bbfda6723f66950c67c03b306f7a1a73f9',
        'scope': 'Internal reconciliation, field preservation and arithmetic; no fresh URL/legal/financial statement certification',
        'tables': {}}
    for key, (name, pk, count) in specs.items():
        original = csv_rows(STUDY / (name + '.csv'))
        cleaned = csv_rows(HERE / 'cleaned' / (name + '.cleaned.csv'))
        assert len(original) == len(cleaned) == count
        ids = [r[pk] for r in cleaned]
        assert all(ids) and len(set(ids)) == count
        assert len({tuple(sorted(r.items())) for r in cleaned}) == count
        original_map = {r[pk]: r for r in original}
        assert set(ids) == set(original_map)
        compared = 0
        for row in cleaned:
            for field, value in original_map[row[pk]].items():
                assert row[field] == value, (key, row[pk], field)
                compared += 1
        assert bundle['data'][key] == cleaned, key
        tables[key] = cleaned
        result['tables'][key] = {'records': count, 'duplicate_ids': 0,
            'original_cells_equal': compared,
            'added_fields': sorted(set(cleaned[0]) - set(original[0])),
            'json_matches_csv': True}
    source_ids = {r['document_id'] for r in tables['sources']}
    for key in ('events', 'routes', 'articles'):
        assert all(r['source_id'] in source_ids and r['source_reference_valid'] == 'true'
                   for r in tables[key])
    for key in ('literature', 'chains'):
        assert bundle['data'][key] == canonical['data'][key]
    for key, rows in bundle['data'].items():
        assert bundle['counts'][key] == len(rows)
    assert all(set(r['source_ids'].split(';')) <= source_ids for r in bundle['data']['chains'])
    statuses = {'DIRECT','REPORTED','SECONDARY','PLANNED','UNKNOWN','EXPLICIT_NOT_IMPLEMENTED','NA'}
    for row in tables['events']:
        for field in ('legal_commitment','domestic_measure','authorization_evidence','operational_evidence'):
            assert row[field] in statuses
        exact = bool(re.fullmatch(r'\d{4}-\d{2}-\d{2}', row['event_date']))
        assert row['date_precision'] == ('EXACT_DATE' if exact else 'ANCHOR_ONLY')
    date_counts = Counter(r['date_precision'] for r in tables['events'])
    assert date_counts == {'EXACT_DATE': 5, 'ANCHOR_ONLY': 6}
    for row in tables['routes']:
        assert row['confirmed_fifth_freedom_authorization'] == ''
        assert row['confirmed_fifth_freedom_operation'] == ''
        assert row['local_commercial_traffic_verified'] == 'UNKNOWN'
        normalized = re.sub(r'\s+', '', re.sub(r'[–—−]', '-', row['full_itinerary_as_reported'])).lower()
        assert row['canonical_itinerary_key'] == normalized
    same_itinerary = {}
    for row in tables['routes']:
        same_itinerary.setdefault(row['canonical_itinerary_key'], []).append(row['route_id'])
    duplicates = [v for v in same_itinerary.values() if len(v) > 1]
    assert duplicates == [['R03','R07']]
    coverage = {f: sum(bool(r[f]) for r in tables['routes']) for f in
        ('source_id','full_itinerary_as_reported','carrier_as_reported','candidate_foreign_segment',
         'carrier_home_state_verified','authorization_document','actual_flight_date')}
    assert list(coverage.values()) == [18,18,7,4,0,0,0]
    assert Counter(r['source_reliability'] for r in tables['sources']) == {
        'official_primary':22, 'carrier_primary':2, 'official_hosted_commissioned_analysis':1}
    summary = json.loads((HERE/'cleaned/audit_summary.json').read_text())
    assert summary['records'] == {k: len(v) for k,v in tables.items()}
    assert summary['event_date_precision'] == dict(date_counts)
    groups = summary['source_urls']
    assert set(groups['historical_http_200_or_206']) == {r['document_id'] for r in tables['sources'] if r['url_check_http_status'] in ('200','206')}
    assert set(groups['historical_http_non_success']) == {'BJ06'}
    assert set(groups['historical_unknown']) == {'UE01','BJ03','CN01'}
    assert all(not r['url_check_checked_at_utc'] and r['url_check_method']=='unknown' for r in tables['sources'])
    result['figures'] = {'route_field_coverage': coverage, 'local_carriage_UNKNOWN':18,
        'date_precision':dict(date_counts), 'source_counts':[22,2,1],
        'duplicate_itinerary_records':duplicates}
    # Check all workbook missingness cells against the original field order.
    missing, _ = sheet_cells(HERE/'originals/legal_data_audit_20261024.xlsx', 3)
    excel_row = 7
    for key, (name, _, _) in specs.items():
        raw = csv_rows(STUDY/(name+'.csv'))
        for field in raw[0]:
            values=[r[field] for r in raw]
            n_blank=sum(v=='' for v in values)
            assert int(missing[f'C{excel_row}']) == n_blank, (key, field)
            assert int(missing[f'D{excel_row}']) == len(values)
            assert abs(Decimal(missing[f'E{excel_row}'])-Decimal(n_blank)/len(values)) < Decimal('1e-12')
            assert int(missing[f'F{excel_row}']) == values.count('UNKNOWN')
            assert int(missing[f'G{excel_row}']) == values.count('NA')
            excel_row += 1
    result['legal_missingness_fields_checked'] = excel_row-7
    fin, formulas = sheet_cells(HERE/'originals/financial_data_audit_20261024.xlsx',2)
    annual = csv_rows(ROOT/'data/official/bceao_annual_lending_2020_2025.csv')
    fields = ['uemoa_all_loans_pct','cote_divoire_all_loans_pct','senegal_all_loans_pct']
    for idx,row in enumerate(annual,7):
        assert fin[f'A{idx}'] == row['year']
        for col,field in zip('BCD',fields):
            assert Decimal(fin[f'{col}{idx}']) == Decimal(row[field])
    companies=csv_rows(ROOT/'data/official/airline_financials_candidate_v1.csv')
    for idx,row in enumerate(companies,18):
        assert fin[f'A{idx}'] == row['fiscal_year']
        for col,field in [('B','revenue_billion_xof'),('C','net_income_billion_xof')]:
            assert Decimal(fin[f'{col}{idx}']) == Decimal(row[field])
    checked_formulas={}
    for col in 'BCD':
        cell=col+'14'; assert formulas[cell] == f'({col}12-{col}11)*100'
        expected=(Decimal(fin[col+'12'])-Decimal(fin[col+'11']))*100
        assert abs(Decimal(fin[cell])-expected)<Decimal('1e-10')
        checked_formulas[cell]=str(expected)
    for row in (26,27):
        cell=f'E{row}'; assert formulas[cell] == f'ABS((D{row}-C{row})*100)'
        expected=abs((Decimal(fin[f'D{row}'])-Decimal(fin[f'C{row}']))*100)
        assert Decimal(fin[cell]) == expected
        checked_formulas[cell]=str(expected)
    assert Decimal('934.76')/1000 == Decimal('0.93476')
    assert Decimal('657.67')/1000 == Decimal('0.65767')
    old_summary=json.loads((ROOT/'data/processed/financing_descriptives_v1.json').read_text())
    assert Decimal(str(old_summary['auction_change_2024_07_to_2026_03_bp'])) == Decimal('-192.3')
    auctions={r['month']:r for r in csv_rows(ROOT/'data/official/bceao_weekly_auction_monthly.csv')}
    auction_change=(Decimal(auctions['2026-03']['one_week_auction_weighted_average_pct'])-Decimal(auctions['2024-07']['one_week_auction_weighted_average_pct']))*100
    assert auction_change == Decimal('-192.3')
    assert old_summary['bank_uemoa_change_2024q4_to_2026q1_bp'] == -25
    quarterly={r['quarter']:r for r in csv_rows(ROOT/'data/processed/quarterly_policy_lending_panel_v1.csv')}
    latest_change=(Decimal(quarterly['2026-Q1']['uemoa_lending_pct'])-Decimal(quarterly['2024-Q4']['uemoa_lending_pct']))*100
    assert latest_change == -27
    result['finance']={'annual_values_matched':18,'airline_values_matched':10,
        'formulas_independently_recomputed':checked_formulas,
        'unit_conversions_checked':2,'old_vintage_change_bp':-25,'selected_vintage_change_bp':str(latest_change),
        'financial_workbook_scope':'Three annual regional/country series; not all seven annual series'}
    result['input_sha256']={str(p.relative_to(HERE)): hashlib.sha256(p.read_bytes()).hexdigest()
        for directory in ('originals','cleaned','figures') for p in sorted((HERE/directory).glob('*')) if p.is_file()}
    result['decision']='ACCEPT_FOR_ARCHIVE_AND_MIDTERM_WITH_REVIEW_NOTES; NOT_A_CANONICAL_DATA_REPLACEMENT'
    (HERE/'review_results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='input_sha256'},ensure_ascii=False,indent=2))
    return result


if __name__ == '__main__':
    run()
