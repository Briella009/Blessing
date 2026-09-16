from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]


def read_csv(path):
    with path.open(encoding='utf-8', newline='') as handle:
        return list(csv.DictReader(handle))


def test_version_metadata_is_synchronized():
    version = (ROOT / 'VERSION').read_text(encoding='utf-8').strip()
    citation = (ROOT / 'CITATION.cff').read_text(encoding='utf-8')
    changelog = (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8')
    readme = (ROOT / 'README.md').read_text(encoding='utf-8')
    assert f'version: "{version}"' in citation
    assert f'## {version} ' in changelog
    assert f'v{version}' in readme


def test_v020_has_19_core_records_and_promoted_operational_cases():
    version = (ROOT / 'VERSION').read_text(encoding='utf-8').strip()
    core = read_csv(ROOT / 'data' / 'incidents.csv')
    assert version == '0.2.0'
    assert len(core) == 19
    ids = {row['incident_id'] for row in core}
    assert {'AAIO-0018', 'AAIO-0019'} <= ids


def test_material_promotions_have_history_entries():
    history = read_csv(ROOT / 'data' / 'record_history.csv')
    by_incident = {row['incident_id'] for row in history if row['change_type'] == 'promotion'}
    assert {'AAIO-0018', 'AAIO-0019'} <= by_incident


def test_promoted_operational_rows_link_back_to_core():
    core = {row['incident_id'] for row in read_csv(ROOT / 'data' / 'incidents.csv')}
    operational = read_csv(ROOT / 'data' / 'operational_incidents.csv')
    promoted = [row for row in operational if row['core_promotion_status'] == 'promoted_to_core']
    assert len(promoted) >= 2
    for row in promoted:
        assert row['promoted_core_id'] in core
        assert row['promoted_in_release'] == '0.2.0'
