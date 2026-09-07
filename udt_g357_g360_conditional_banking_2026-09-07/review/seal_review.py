"""Seal top-level authored review/capture files; leave ephemeral fixture trees."""
import hashlib
import json
import pathlib

root = pathlib.Path(__file__).resolve().parent
manifest = root / 'REVIEW_SHA256SUMS'
archive = root / 'ARCHIVE_FILES.txt'
assert not manifest.exists() and not archive.exists(), 'refuse seal overwrite'
payloads = sorted(path.name for path in root.iterdir() if path.is_file())
archive_names = sorted(payloads + ['ARCHIVE_FILES.txt', 'REVIEW_SHA256SUMS'])
archive.write_text(''.join(name + '\n' for name in archive_names))
payloads = sorted(payloads + ['ARCHIVE_FILES.txt'])
lines = [hashlib.sha256((root / name).read_bytes()).hexdigest() + '  ' + name + '\n'
         for name in payloads]
manifest.write_text(''.join(lines))
print(json.dumps({'archive_files': len(archive_names), 'manifest_payloads': len(payloads),
                  'manifest_sha256': hashlib.sha256(manifest.read_bytes()).hexdigest(),
                  'final_review_sha256': hashlib.sha256((root / 'FINAL_FIDELITY_REVIEW.md').read_bytes()).hexdigest(),
                  'omitted_ephemeral_directories': sorted(path.name for path in root.iterdir() if path.is_dir())},
                 indent=2))
