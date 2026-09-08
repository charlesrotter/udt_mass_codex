"""Independent byte/inventory check for disposition-only CD banking.

No parent banking checker imports; no scientific proof or protected payload.
"""
import hashlib
import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]
BASE = '180c1a114bf80f953752c8d6e8ecabcf61626ee9'
CAMPAIGN = 'udt_optional_coupled_development_campaign_2026-09-08/'
NEW = {b'G372', b'G373'}


def git(*args):
    return subprocess.check_output(
        ['git', '-c', 'core.packedGitLimit=32m', '-c',
         'core.packedGitWindowSize=1m', *args], cwd=ROOT)


def original_rows_only(current, baseline):
    lines = current.splitlines(keepends=True)
    ids = [line.split(b'\t', 1)[0] for line in lines[1:]]
    assert len(ids) == len(set(ids)), 'duplicate registry ID'
    assert len(ids) == 356, 'wrong registry count'
    assert all(ids.count(key) == 1 for key in NEW), 'missing or repeated additions'
    restored = b''.join(line for line in lines if line.split(b'\t', 1)[0] not in NEW)
    assert restored == baseline, 'earlier registry bytes changed'


def blob_identity(payload, oid):
    actual = hashlib.sha1(b'blob ' + str(len(payload)).encode() + b'\0' + payload).hexdigest()
    assert actual == oid, 'original campaign byte change'


def rejects(call, message):
    try:
        call()
    except AssertionError as error:
        assert message in str(error), (message, str(error))
        return {'caught': message}
    raise AssertionError('false-pass: ' + message)


baseline = git('show', BASE + ':CURRENT_SCIENTIFIC_PREMISES.tsv')
assert hashlib.sha256(baseline).hexdigest() == '1bbb790281fec94a57d63f101f0bd2b909022348587473864190b6965aa17900'
assert len(baseline.splitlines()) == 355
current = (ROOT / 'CURRENT_SCIENTIFIC_PREMISES.tsv').read_bytes()
original_rows_only(current, baseline)

entries = git('ls-tree', '-rz', BASE, '--', CAMPAIGN).split(b'\0')
inventory = {}
for entry in entries:
    if not entry:
        continue
    meta, name = entry.split(b'\t', 1)
    mode, kind, oid = meta.split()
    assert kind == b'blob' and mode == b'100644', 'unexpected original file kind'
    path = name.decode()
    assert path.startswith(CAMPAIGN)
    inventory[path] = oid.decode()
assert len(inventory) == 81
tracked = set(git('ls-files', '-z', '--', CAMPAIGN).decode().split('\0')) - {''}
assert tracked == set(inventory), 'original tracked inventory changed'
for path, oid in inventory.items():
    blob_identity((ROOT / path).read_bytes(), oid)

# Reintroduce byte/ID errors IN MEMORY through the exact guards above.
old_lines = current.splitlines(keepends=True)
prior_index = next(i for i, line in enumerate(old_lines)
                   if i > 0 and line.split(b'\t', 1)[0] not in NEW)
old_lines[prior_index] = old_lines[prior_index].replace(b'\t', b'\tBROKEN_', 1)
first_source = next(iter(inventory))
first_payload = (ROOT / first_source).read_bytes()
catches = {
    'old_row_modified': rejects(
        lambda: original_rows_only(b''.join(old_lines), baseline),
        'earlier registry bytes changed'),
    'new_row_duplicated': rejects(
        lambda: original_rows_only(current + current.splitlines(keepends=True)[1], baseline),
        'duplicate registry ID'),
    'source_payload_modified': rejects(
        lambda: blob_identity(first_payload + b'\nBROKEN', inventory[first_source]),
        'original campaign byte change'),
}
print(json.dumps({
    'verdict': 'PASS_BYTE_CORRESPONDENCE_NOT_SCIENTIFIC_PROOF',
    'baseline': BASE,
    'original_campaign_files': len(inventory),
    'prior_registry_rows_unchanged': 354,
    'only_added_registry_ids': sorted(key.decode() for key in NEW),
    'registry_current_sha256': hashlib.sha256(current).hexdigest(),
    'in_memory_guard_catches': catches,
    'protected_payloads_accessed': False,
}, indent=2, sort_keys=True))
