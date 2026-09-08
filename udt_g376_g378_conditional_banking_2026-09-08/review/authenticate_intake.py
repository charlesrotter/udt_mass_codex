"""Read-only correspondence check for this proportional banking review."""
import csv
import hashlib
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path('/home/udt-admin/udt_mass_codex')
BANK = ROOT / 'udt_g376_g378_conditional_banking_2026-09-08'
receipt_name = sys.argv[1] if len(sys.argv) > 1 else 'prebank_358'
assert receipt_name in {'prebank_358', 'postbank_361', 'final_361'}
expected_count = 358 if receipt_name == 'prebank_358' else 361
receipt_path = BANK / (receipt_name + '.json')
receipt = json.loads(receipt_path.read_text())
assert receipt['command'] == ['python3', '-B', 'verify_current_scientific_premises.py']
assert receipt['cwd'] == str(ROOT)
assert receipt['returncode'] == 0 and receipt['timeout'] is False
for kind in ('stdout', 'stderr'):
    assert receipt[kind].encode() == (BANK / (receipt_name + '.' + kind)).read_bytes()
assert f'PASS: {expected_count}-row premise registry' in receipt['stdout']
assert receipt['stderr'] == ''

expected_sources = {
    'G310': 'udt_g310_differential_dual_reciprocity_tracefree_ownership_2026-08-31/AUDIT_REPORT.md',
    'G312': 'udt_g312_quiet_gr_response_constitution_discriminator_2026-09-01/AUDIT_REPORT.md',
    'G315': 'udt_g315_conditional_cauchy_characteristic_data_interface_2026-09-01/AUDIT_REPORT.md',
    'G330': 'udt_g330_berger_hopf_eigenline_local_persistence_2026-09-02/AUDIT_REPORT.md',
    'G332': 'udt_g332_weighted_contact_vacuum_constraint_embedding_2026-09-03/AUDIT_REPORT.md',
    'G337': 'udt_g337_double_silent_third_normal_ownership_2026-09-03/AUDIT_REPORT.md',
}
registry = ROOT / 'CURRENT_SCIENTIFIC_PREMISES.tsv'
with registry.open(newline='') as stream:
    rows = {r['premise_id']: r for r in csv.DictReader(stream, delimiter='\t')}
out_rows = {}
for key, source in expected_sources.items():
    row = rows[key]
    assert row['controlling_source'] == source
    assert (ROOT / source).is_file()
    if key in ('G310', 'G312'):
        assert 'OWNER' in row['current_status'] and 'PROVISIONAL' in row['current_status']
        assert 'NOT_CANON' in row['current_status']
    else:
        assert row['current_status'].startswith('EXTERNALLY_ACCEPTED')
    out_rows[key] = dict(row)

paths = [receipt_path, BANK / (receipt_name + '.stdout'), BANK / (receipt_name + '.stderr'), registry,
         ROOT / 'verify_current_scientific_premises.py']
result = {
    'scope': 'receipt/stream/row/source correspondence only; no scientific rerun',
    'python': sys.version,
    'head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
    'branch': subprocess.check_output(['git', 'branch', '--show-current'], cwd=ROOT, text=True).strip(),
    'parent_receipt_reused_not_replayed': receipt,
    'current_registry_row_count': len(rows),
    'exact_relevant_rows': out_rows,
    'sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
    'verdict': 'PASS',
}
print(json.dumps(result, indent=2, sort_keys=True))
