from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'data' / 'operational_incidents.csv'


def rows():
    with PATH.open(encoding='utf-8', newline='') as handle:
        return list(csv.DictReader(handle))


def core_rows():
    with (ROOT / 'data' / 'incidents.csv').open(encoding='utf-8', newline='') as handle:
        return list(csv.DictReader(handle))


def test_operational_register_has_multiple_sectors():
    data = rows()
    assert len(data) >= 2
    assert len({row['sector'] for row in data}) >= 2


def test_healthcare_case_preserves_patient_harm_boundary():
    case = next(row for row in rows() if row['incident_id'] == 'AAIO-OP-0001')
    summary = case['summary'].lower()
    assert '115' in summary
    assert '67' in summary or 'sixty-seven' in summary
    assert 'does not infer patient injury' in summary
    assert case['evidence_confidence'] == 'A'
    assert 'nature.com' in case['source_1_url']
    assert 'pubmed.ncbi.nlm.nih.gov' in case['source_2_url']


def test_legal_case_has_direct_ai_linkage_and_primary_sources():
    case = next(row for row in rows() if row['incident_id'] == 'AAIO-OP-0002')
    assert case['ai_system_or_tool'] == 'ChatGPT'
    assert case['evidence_confidence'] == 'A'
    assert 'lawlibrary.org.za' in case['source_1_url']
    assert 'saflii.org' in case['source_2_url']


def test_promoted_operational_records_resolve_to_core_records():
    core = {row['incident_id']: row for row in core_rows()}
    promoted = [row for row in rows() if row['core_promotion_status'] == 'promoted_to_core']
    assert len(promoted) >= 2
    for row in promoted:
        core_id = row['promoted_core_id']
        assert core_id in core
        assert row['promoted_in_release'] == '0.2.0'
        assert core[core_id]['title'] == row['title']
        assert core[core_id]['evidence_confidence'] == row['evidence_confidence']
        assert core[core_id]['source_1_url'] == row['source_1_url']


def test_core_eligible_records_are_high_confidence_and_source_traceable():
    for row in rows():
        if row['core_promotion_status'] in {'eligible_for_core', 'promoted_to_core'}:
            assert row['evidence_confidence'] in {'A', 'B'}
            assert row['source_1_url'].startswith('https://')
            assert row['source_2_url'].startswith('https://')
            assert len(row['qualification_basis']) >= 80
            assert len(row['notes']) >= 80


def test_operational_ids_do_not_collide_with_versioned_core_ids():
    core_ids = {row['incident_id'] for row in core_rows()}
    operational_ids = {row['incident_id'] for row in rows()}
    assert core_ids.isdisjoint(operational_ids)
