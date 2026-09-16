#!/usr/bin/env python3
from pathlib import Path
import csv
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def fail(errors, message):
    errors.append(message)


def main():
    errors = []
    version = (ROOT / 'VERSION').read_text(encoding='utf-8').strip()
    if not re.fullmatch(r'\d+\.\d+\.\d+', version):
        fail(errors, f'Invalid VERSION value: {version!r}')

    citation = (ROOT / 'CITATION.cff').read_text(encoding='utf-8')
    if f'version: "{version}"' not in citation:
        fail(errors, 'CITATION.cff version does not match VERSION')

    changelog = (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8')
    if f'## {version} ' not in changelog:
        fail(errors, 'CHANGELOG.md does not contain the current VERSION')

    readme = (ROOT / 'README.md').read_text(encoding='utf-8')
    if f'v{version}' not in readme:
        fail(errors, 'README.md does not mention the current VERSION')

    with (ROOT / 'data' / 'incidents.csv').open(encoding='utf-8', newline='') as handle:
        core = list(csv.DictReader(handle))
    core_ids = {row['incident_id'] for row in core}
    if len(core_ids) != len(core):
        fail(errors, 'Core incident IDs are not unique')

    with (ROOT / 'data' / 'operational_incidents.csv').open(encoding='utf-8', newline='') as handle:
        operational = list(csv.DictReader(handle))
    for row in operational:
        if row.get('core_promotion_status') == 'promoted_to_core':
            target = row.get('promoted_core_id', '')
            if target not in core_ids:
                fail(errors, f"{row['incident_id']} points to missing core ID {target}")
            if row.get('promoted_in_release') != version:
                fail(errors, f"{row['incident_id']} promotion release does not match VERSION")

    history_path = ROOT / 'data' / 'record_history.csv'
    with history_path.open(encoding='utf-8', newline='') as handle:
        history = list(csv.DictReader(handle))
    seen_changes = set()
    for row in history:
        cid = row.get('change_id', '')
        if not re.fullmatch(r'AAIO-CHG-\d{4}', cid):
            fail(errors, f'Invalid change ID: {cid}')
        if cid in seen_changes:
            fail(errors, f'Duplicate change ID: {cid}')
        seen_changes.add(cid)
        incident_id = row.get('incident_id', '')
        if incident_id not in core_ids:
            fail(errors, f'{cid} references missing core incident {incident_id}')
        if not row.get('summary', '').strip():
            fail(errors, f'{cid} has an empty summary')
        if row.get('release') and not re.fullmatch(r'\d+\.\d+\.\d+', row['release']):
            fail(errors, f'{cid} has invalid release metadata')

    if version == '0.2.0' and len(core) != 19:
        fail(errors, f'v0.2.0 must contain exactly 19 core records, found {len(core)}')

    if errors:
        print('\n'.join('ERROR: ' + error for error in errors))
        return 1

    print(
        f'OK: release metadata synchronized for v{version}; '
        f'{len(core)} core records and {len(history)} material history entries validated.'
    )
    return 0


if __name__ == '__main__':
    sys.exit(main())
