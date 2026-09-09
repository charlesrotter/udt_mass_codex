"""Read-only correspondence and explicit controlling-source audit."""
import hashlib
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
BASE = 'ca6f092dacf240b6f72b92cca33bb774284c3c36'
CAMPAIGN = 'udt_neighboring_tidal_consistency_campaign_2026-09-08'
GIT = ['git', '-c', 'core.packedGitWindowSize=16m', '-c', 'core.packedGitLimit=64m']

def git(*args):
    return subprocess.check_output(GIT + list(args), cwd=ROOT)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def git_blob_hash(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

entries = git('ls-tree', '-r', '-z', BASE, '--', CAMPAIGN).split(b'\0')
correspondence = []
for entry in entries:
    if not entry:
        continue
    metadata, path = entry.split(b'\t', 1)
    mode, kind, expected = metadata.decode().split()
    assert kind == 'blob' and mode == '100644', (path, metadata)
    data = (ROOT / path.decode()).read_bytes()
    assert git_blob_hash(data) == expected, path.decode()
    correspondence.append({'path': path.decode(), 'sha256': sha(data), 'bytes': len(data)})
assert len(correspondence) == 338, len(correspondence)

manifest_results = {}
for manifest in ['SOURCE_SHA256SUMS', 'step_02/SOURCE_SHA256SUMS', 'EVIDENCE_SHA256SUMS']:
    count = 0
    for line in (ROOT / CAMPAIGN / manifest).read_text().splitlines():
        if not line or line.startswith('#'):
            continue
        expected, path = line.split(maxsplit=1)
        path = path.lstrip('*')
        # Historical registry pin is authenticated against the banking base.
        data = git('show', BASE + ':' + path) if path == 'CURRENT_SCIENTIFIC_PREMISES.tsv' else (ROOT / path).read_bytes()
        assert sha(data) == expected, (manifest, path)
        count += 1
    manifest_results[manifest] = count

fixed = {}
for path in ['CANON.md', 'UDT_METRIC_KERNEL_DEVELOPMENT.md', 'UDT_METRIC_KERNEL_COVERAGE.tsv']:
    data = (ROOT / path).read_bytes()
    assert data == git('show', BASE + ':' + path), path
    fixed[path] = sha(data)

print(json.dumps({'status': 'PASS', 'scope': 'source byte fidelity, not scientific reproof',
                  'base': BASE, 'campaign_files': len(correspondence),
                  'manifest_members': manifest_results, 'fixed': fixed,
                  'python': sys.version, 'source_files': correspondence}, indent=2))
