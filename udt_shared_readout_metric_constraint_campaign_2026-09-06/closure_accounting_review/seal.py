import hashlib
import json
import pathlib

root = pathlib.Path('/tmp/tri_closure_accounting.4rsNkG')
manifest = root / 'REVIEW_SHA256SUMS'
assert not manifest.exists()
files = sorted(root.iterdir())
assert all(path.is_file() for path in files)
rows = [(hashlib.sha256(path.read_bytes()).hexdigest(), path.name) for path in files]
with manifest.open('x') as stream:
    stream.write(''.join(digest + '  ' + name + '\n' for digest, name in rows))
for digest, name in rows:
    assert hashlib.sha256((root / name).read_bytes()).hexdigest() == digest
print(json.dumps(dict(result='PASS', payload_count=len(rows),
                      manifest_sha256=hashlib.sha256(manifest.read_bytes()).hexdigest(),
                      report_sha256=hashlib.sha256((root / 'ACCOUNTING_ADDENDUM.md').read_bytes()).hexdigest()), sort_keys=True))
