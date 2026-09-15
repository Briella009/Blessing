from pathlib import Path
import csv
import json
import subprocess
import sys
from datetime import date

ROOT = Path(__file__).resolve().parents[1]


def core_rows():
    with (ROOT / 'data' / 'incidents.csv').open(encoding='utf-8', newline='') as handle:
        return list(csv.DictReader(handle))


def test_core_has_multiple_countries_sources_and_verification_dates():
    rows = core_rows()
    assert len(rows) == 19
    assert len({row['country'] for row in rows}) >= 8
    assert all(row['source_1_url'].startswith('https://') for row in rows)

    verification_dates = [date.fromisoformat(row['last_verified']) for row in rows]
    assert all(value <= date(2026, 9, 15) for value in verification_dates)
    assert min(verification_dates) >= date(2026, 9, 8)


def test_watchlist_is_separate():
    core = {row['incident_id'] for row in core_rows()}
    with (ROOT / 'data' / 'watchlist.csv').open(encoding='utf-8', newline='') as handle:
        watch = list(csv.DictReader(handle))
    assert watch
    assert all(row['watch_id'] not in core for row in watch)


def test_json_export_matches_csv_ids(tmp_path):
    subprocess.run(
        [sys.executable, str(ROOT / 'scripts' / 'export_json.py')],
        check=True,
        cwd=ROOT,
    )
    rows = core_rows()
    generated = ROOT / 'data' / 'incidents.generated.json'
    with generated.open(encoding='utf-8') as handle:
        data = json.load(handle)
    assert [row['incident_id'] for row in rows] == [row['incident_id'] for row in data]
    generated.unlink()
