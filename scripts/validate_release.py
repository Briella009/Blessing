#!/usr/bin/env python3
from pathlib import Path
import csv
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SEMVER = re.compile(r'\d+\.\d+\.\d+')


def fail(errors, message):
    errors.append(message)


def version_tuple(value):
    if not SEMVER.fullmatch(value):
        raise ValueError(value)
    return tuple(int(part) for part in value.split('.'))


def main():
    errors = []
    version = (ROOT / 'VERSION').read_text(encoding='utf-8').strip()
    if not SEMVER.fullmatch(version):
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
            promoted_release = row.get('promoted_in_release', '')
            if not SEMVER.fullmatch(promoted_release):
                fail(errors, f"{row['incident_id']} has invalid promotion release {promoted_release!r}")
            else:
                if SEMVER.fullmatch(version) and version_tuple(promoted_release) > version_tuple(version):
                    fail(errors, f"{row['incident_id']} promotion release {promoted_release} is newer than VERSION {version}")
                if f'## {promoted_release} ' not in changelog:
                    fail(errors, f"{row['incident_id']} promotion release {promoted_release} is missing from CHANGELOG.md")

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
        release = row.get('release', '')
        if release:
            if not SEMVER.fullmatch(release):
                fail(errors, f'{cid} has invalid release metadata')
            elif SEMVER.fullmatch(version) and version_tuple(release) > version_tuple(version):
                fail(errors, f'{cid} history release {release} is newer than VERSION {version}')

    if version_tuple(version) >= (0, 2, 0) and len(core) < 19:
        fail(errors, f'v{version} must preserve at least the 19 core records established in v0.2.0; found {len(core)}')

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
