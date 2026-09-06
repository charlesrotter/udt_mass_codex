"""Independent byte/membership checks; no scientific reconstruction."""
import hashlib
import json
import pathlib
import subprocess

root = pathlib.Path('/home/udt-admin/udt_mass_codex')
bank = root / 'udt_g353_g356_conditional_banking_2026-09-06'
snapshot = 'c92588ad31f3fd79868378e6e3a318af2de1235f'
def digest(data):
    return hashlib.sha256(data).hexdigest()
def git_bytes(path):
    return subprocess.run(['git', 'show', snapshot + ':' + path], cwd=root,
                          check=True, capture_output=True).stdout
pin = bank / 'INTEGRATION_CANDIDATE_SHA256SUMS'
candidate_rows = []
for line in pin.read_text().splitlines():
    expected, path = line.split(maxsplit=1)
    data = (root / path).read_bytes()
    assert digest(data) == expected, ('candidate changed', path)
    candidate_rows.append(dict(path=path, sha256=expected, bytes=len(data)))
assert len(candidate_rows) == 14
new_ids = {b'G353', b'G354', b'G355', b'G356'}
live = (root / 'CURRENT_SCIENTIFIC_PREMISES.tsv').read_bytes()
lines = live.splitlines(keepends=True)
old = b''.join(line for line in lines if line.split(b'\t', 1)[0] not in new_ids)
frozen = git_bytes('CURRENT_SCIENTIFIC_PREMISES.tsv')
assert old == frozen
assert len(lines) == 340 and len(frozen.splitlines()) == 336
additions = [line.split(b'\t', 1)[0] for line in lines if line.split(b'\t', 1)[0] in new_ids]
assert len(additions) == 4 and set(additions) == new_ids
campaign = root / 'udt_g351_g352_content_bridge_campaign_2026-09-06'
manifest = campaign / 'ARTIFACT_SHA256SUMS'
assert digest(manifest.read_bytes()) == '048e2870eb229943d029c8383ae82c5609a0d3e1e77c4d910916e4b3ece87dcb'
paths = []
for line in manifest.read_text().splitlines():
    expected, name = line.split(maxsplit=1)
    assert digest((campaign / name).read_bytes()) == expected, name
    paths.append(pathlib.PurePosixPath(name).as_posix())
assert len(paths) == len(set(paths)) == 350
actual = {p.relative_to(campaign).as_posix() for p in campaign.rglob('*') if p.is_file()}
assert actual == set(paths) | {'ARTIFACT_SHA256SUMS'}, ('campaign membership', actual - set(paths))
integration = bank / 'integration'
im = integration / 'SHA256SUMS'
assert digest(im.read_bytes()) == 'bd9f541b4b84ef457c7250a954ab8d006176b8ef677acd116118689b08bc534e'
evidence_names = []
for line in im.read_text().splitlines():
    expected, name = line.split(maxsplit=1)
    assert digest((integration / name).read_bytes()) == expected, name
    evidence_names.append(name)
assert len(evidence_names) == 9
assert {p.name for p in integration.iterdir() if p.is_file()} == set(evidence_names) | {'SHA256SUMS'}
preserved = []
for name in ('UDT_METRIC_KERNEL_DEVELOPMENT.md', 'UDT_METRIC_KERNEL_COVERAGE.tsv',
             'CANON.md', 'verify_metric_kernel_account.py', 'update_metric_kernel_account.py'):
    data = (root / name).read_bytes()
    assert data == git_bytes(name), ('fixed file changed', name)
    preserved.append(dict(path=name, sha256=digest(data)))
print(json.dumps(dict(verdict='PASS_BYTE_CORRESPONDENCE_ONLY', snapshot=snapshot,
                     pin_sha256=digest(pin.read_bytes()), candidates=candidate_rows,
                     old_registry_sha256=digest(old), old_data_rows=335, new_data_rows=339,
                     added_ids=sorted(x.decode() for x in additions),
                     campaign_payload_hashes=350, exact_campaign_membership=351,
                     integration_payload_hashes=9, exact_integration_membership=10,
                     preserved_fixed_files=preserved, full_premise_audit_run=False), indent=2))
