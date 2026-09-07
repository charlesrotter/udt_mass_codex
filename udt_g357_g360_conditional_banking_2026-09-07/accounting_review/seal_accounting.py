"""Seal this bounded accounting report and actual capture files only."""
import hashlib
import json
import pathlib

root = pathlib.Path(__file__).resolve().parent
manifest = root / 'REVIEW_SHA256SUMS'
archive = root / 'ARCHIVE_FILES.txt'
assert not manifest.exists() and not archive.exists()
payloads = sorted(path.name for path in root.iterdir() if path.is_file())
names = sorted(payloads + ['ARCHIVE_FILES.txt', 'REVIEW_SHA256SUMS'])
archive.write_text(''.join(name + '\n' for name in names))
payloads = sorted(payloads + ['ARCHIVE_FILES.txt'])
manifest.write_text(''.join(hashlib.sha256((root / name).read_bytes()).hexdigest() + '  ' + name + '\n'
                            for name in payloads))
print(json.dumps({'archive_files': len(names), 'manifest_payloads': len(payloads),
                  'manifest_sha256': hashlib.sha256(manifest.read_bytes()).hexdigest(),
                  'report_sha256': hashlib.sha256((root / 'FOCUSED_ACCOUNTING_REVIEW.md').read_bytes()).hexdigest()}, indent=2))
