from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]


def read_csv(path):
    with path.open(encoding='utf-8', newline='') as handle:
        return list(csv.DictReader(handle))


def semver_tuple(value):
    return tuple(int(part) for part in value.split('.'))


def test_version_metadata_is_synchronized():
    version = (ROOT / 'VERSION').read_text(encoding='utf-8').strip()
    citation = (ROOT / 'CITATION.cff').read_text(encoding='utf-8')
    changelog = (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8')
    readme = (ROOT / 'README.md').read_text(encoding='utf-8')
    assert f'version: "{version}"' in citation
    assert f'## {version} ' in changelog
    assert f'v{version}' in readme


def test_v02x_preserves_operational_core_expansion():
    version = (ROOT / 'VERSION').read_text(encoding='utf-8').strip()
    core = read_csv(ROOT / 'data' / 'incidents.csv')
    assert semver_tuple(version) >= (0, 2, 0)
    assert len(core) >= 19
    ids = {row['incident_id'] for row in core}
    assert {'AAIO-0018', 'AAIO-0019'} <= ids


def test_material_promotions_have_history_entries():
    history = read_csv(ROOT / 'data' / 'record_history.csv')
    by_incident = {row['incident_id'] for row in history if row['change_type'] == 'promotion'}
    assert {'AAIO-0018', 'AAIO-0019'} <= by_incident


def test_promoted_operational_rows_link_back_to_core_and_original_release():
    current = semver_tuple((ROOT / 'VERSION').read_text(encoding='utf-8').strip())
    core = {row['incident_id'] for row in read_csv(ROOT / 'data' / 'incidents.csv')}
    operational = read_csv(ROOT / 'data' / 'operational_incidents.csv')
    promoted = [row for row in operational if row['core_promotion_status'] == 'promoted_to_core']
    assert len(promoted) >= 2
    for row in promoted:
        assert row['promoted_core_id'] in core
        assert row['promoted_in_release']
        assert semver_tuple(row['promoted_in_release']) <= current


def test_v020_promotions_keep_historical_release_value():
    operational = read_csv(ROOT / 'data' / 'operational_incidents.csv')
    promoted = {row['incident_id']: row for row in operational if row['core_promotion_status'] == 'promoted_to_core'}
    assert promoted['AAIO-OP-0001']['promoted_in_release'] == '0.2.0'
    assert promoted['AAIO-OP-0002']['promoted_in_release'] == '0.2.0'
