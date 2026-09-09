"""Freeze/table/source-address audit; semantic assessment is in DIRECT_REVIEW.md."""
import csv
import hashlib
import json
import pathlib
import platform
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]
PACKAGE = ROOT / 'udt_gr_filter_authority_audit_2026-09-09'
BASE = '4a699eec12b656a9487fa41f5ebad5993ef7adc5'
FROZEN = {
    'INITIAL_AUDIT.md': 'eb5fcd6b279e463f9a0e96cbf3cc32f1a15f08f27cf9d4f8e01415c0216d03b9',
    'AUTHORITY_MAP.tsv': 'bd24957354f8c4d0c4dd5ce54a00df7fc8af792ccdf67c79b1e162ee40d7569e',
    'DEPENDENCY_IMPACT.tsv': '13c7e57784f2470db762d3ae01f6bde0e9f6b012cb001a54f0a2e4133188559e',
}
def digest(data):
    return hashlib.sha256(data).hexdigest()

for name, expected in FROZEN.items():
    assert digest((PACKAGE / name).read_bytes()) == expected, ('freeze_changed', name)

address_records = []
table_records = []
for name, field in [('AUTHORITY_MAP.tsv', 'exact_source'),
                    ('DEPENDENCY_IMPACT.tsv', 'controlling_statement_source')]:
    with (PACKAGE / name).open() as stream:
        rows = list(csv.DictReader(stream, delimiter='\t'))
    assert len({row['id'] for row in rows}) == len(rows), ('duplicate_id', name)
    for row in rows:
        assert None not in row and None not in row.values(), ('ragged_row', name, row['id'])
        source_names = re.findall(r'[A-Za-z0-9_./-]+\.(?:md|tsv)', row[field])
        assert source_names, ('missing_source_address', name, row['id'])
        first = pathlib.Path(source_names[0])
        for address in source_names:
            path = pathlib.Path(address)
            if not (ROOT / path).exists() and len(path.parts) == 1:
                path = first.parent / path
            assert (ROOT / path).is_file(), ('missing_source_file', name, row['id'], str(path))
            raw = (ROOT / path).read_bytes()
            old = subprocess.check_output(
                ['git', '-c', 'core.preloadIndex=false', '-c', 'index.threads=1',
                 'show', BASE + ':' + str(path)], cwd=ROOT)
            # OTHER_DESCENDANTS uses a current navigation page explicitly, not proof.
            mutable_navigation = row['id'] == 'OTHER_DESCENDANTS'
            assert raw == old or mutable_navigation, ('changed_proof_source', str(path))
            address_records.append(dict(table=name, id=row['id'], path=str(path),
                                        sha256=digest(raw), unchanged=raw == old,
                                        navigation_only=mutable_navigation))
    table_records.append(dict(path=name, rows=len(rows)))

print(json.dumps(dict(evidence_kind='FREEZE_AND_SOURCE_ADDRESS_CORRESPONDENCE_ONLY',
                      python=platform.python_version(), baseline=BASE,
                      frozen_hashes=FROZEN, tables=table_records,
                      source_addresses=address_records), indent=2))
