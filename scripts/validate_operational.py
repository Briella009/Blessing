#!/usr/bin/env python3
from pathlib import Path
import csv, re, sys
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / 'data' / 'operational_incidents.csv'
CORE = ROOT / 'data' / 'incidents.csv'
REQUIRED = {
    'incident_id','title','incident_date','date_precision','country','sector',
    'system_type','ai_system_or_tool','incident_or_hazard','harm_types',
    'affected_parties','summary','response','evidence_confidence',
    'qualification_basis','source_1_name','source_1_url','source_1_type',
    'source_2_name','source_2_url','source_2_type','last_verified','notes',
    'curator','severity_score','severity_band','core_promotion_status',
    'promoted_core_id','promoted_in_release'
}
ALLOWED_STATUS = {'eligible_for_core','promoted_to_core','hold','watchlist'}
ALLOWED_CONFIDENCE = {'A','B','C'}


def valid_url(value):
    parsed = urlparse(value)
    return parsed.scheme in {'http','https'} and bool(parsed.netloc)


def main():
    errors = []
    with CSV.open(encoding='utf-8', newline='') as handle:
        reader = csv.DictReader(handle)
        fields = set(reader.fieldnames or [])
        missing = sorted(REQUIRED - fields)
        if missing:
            errors.append('Missing fields: ' + ', '.join(missing))
        rows = list(reader)

    with CORE.open(encoding='utf-8', newline='') as handle:
        core_ids = {row['incident_id'] for row in csv.DictReader(handle)}

    ids = set()
    sectors = set()
    promoted_ids = set()
    for index, row in enumerate(rows, 1):
        rid = row.get('incident_id', '')
        status = row.get('core_promotion_status', '')
        promoted_core_id = row.get('promoted_core_id', '').strip()
        promoted_release = row.get('promoted_in_release', '').strip()

        if not re.fullmatch(r'AAIO-OP-\d{4}', rid):
            errors.append(f'Record {index}: bad operational ID {rid}')
        if rid in ids:
            errors.append(f'Record {index}: duplicate ID {rid}')
        ids.add(rid)
        sectors.add(row.get('sector', ''))

        if row.get('incident_or_hazard') != 'incident':
            errors.append(f'{rid}: operational register requires realised incidents')
        if row.get('evidence_confidence') not in ALLOWED_CONFIDENCE:
            errors.append(f'{rid}: invalid confidence')
        if status not in ALLOWED_STATUS:
            errors.append(f'{rid}: invalid promotion status')
        if status in {'eligible_for_core', 'promoted_to_core'} and row.get('evidence_confidence') not in {'A','B'}:
            errors.append(f'{rid}: core-eligible/promoted record must have A/B evidence')

        if status == 'promoted_to_core':
            if not re.fullmatch(r'AAIO-\d{4}', promoted_core_id):
                errors.append(f'{rid}: promoted record must declare a valid promoted_core_id')
            elif promoted_core_id not in core_ids:
                errors.append(f'{rid}: promoted_core_id {promoted_core_id} is missing from core data')
            if promoted_core_id in promoted_ids:
                errors.append(f'{rid}: duplicate promoted_core_id {promoted_core_id}')
            promoted_ids.add(promoted_core_id)
            if not re.fullmatch(r'\d+\.\d+\.\d+', promoted_release):
                errors.append(f'{rid}: promoted record must declare promoted_in_release as x.y.z')
        else:
            if promoted_core_id or promoted_release:
                errors.append(f'{rid}: non-promoted record must not declare promotion metadata')

        for field in ('source_1_url','source_2_url'):
            if not valid_url(row.get(field,'')):
                errors.append(f'{rid}: invalid {field}')
        if len(row.get('qualification_basis','').strip()) < 80:
            errors.append(f'{rid}: qualification basis is too thin')
        if len(row.get('notes','').strip()) < 80:
            errors.append(f'{rid}: calibration note is too thin')

    if len(rows) < 2:
        errors.append('Operational expansion must contain at least two independently sourced incidents')
    if not any('Healthcare' in sector for sector in sectors):
        errors.append('Operational expansion must include a healthcare deployment incident')

    if errors:
        print('\n'.join('ERROR: ' + error for error in errors))
        return 1
    print(f'OK: {len(rows)} operational incidents validated with evidence and promotion traceability.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
