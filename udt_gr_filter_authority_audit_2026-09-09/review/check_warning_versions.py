"""Authenticate the repaired warning and explicitly reconstructed earlier page."""
import csv
import hashlib
import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]
HERE = pathlib.Path(__file__).resolve().parent
def sha(data):
    return hashlib.sha256(data).hexdigest()
def pins(name):
    return {r['path']: r['sha256'] for r in csv.DictReader((HERE / name).open(), delimiter='\t')}
initial = pins('INITIAL_WARNING_PINS.tsv')
final = pins('FINAL_WARNING_PINS.tsv')
assert initial.keys() == final.keys()
for path, expected in final.items():
    assert sha((ROOT / path).read_bytes()) == expected, ('warning_version_changed', path)
changed = [path for path in initial if initial[path] != final[path]]
assert changed == ['CURRENT_SCIENTIFIC_PREMISES.md'], changed
old = (HERE / 'RECONSTRUCTED_INITIAL_PREMISES.md').read_bytes()
assert sha(old) == initial[changed[0]], 'reconstruction_hash_mismatch'
new = (ROOT / changed[0]).read_text()
reconstructed = new.replace('not automatically signal speed.', 'not signal speed.')
reconstructed = reconstructed.replace(
    'Pullbacks plus the bivector area bilinear can recover `g`; scalar data stop at its positive conformal class.',
    'Pullbacks and bivector area recover `g`; scalar data stop at its positive conformal class.')
reconstructed = reconstructed.replace(
    "Scopes/assumptions/positivity/recipes/reviews control; tables aren't proofs.",
    'Source scopes/assumptions/positivity/recipes/reviews control; tables navigate, not prove.')
assert reconstructed.encode() == old, 'reconstruction_recipe_mismatch'
diff = subprocess.check_output(
    ['git', '-c', 'core.preloadIndex=false', '-c', 'index.threads=1', 'diff',
     '4a699eec12b656a9487fa41f5ebad5993ef7adc5', '--'] + list(final), cwd=ROOT)
assert diff == (HERE / 'FINAL_WARNING_DIFF.patch').read_bytes(), 'saved_final_diff_mismatch'
for line in (HERE / 'SOURCE_FIRST_SHA256SUMS').read_text().splitlines():
    expected, path = line.split('  ', 1)
    assert sha((ROOT / path).read_bytes()) == expected, ('source_first_seal_changed', path)
print(json.dumps(dict(status='PASS_WARNING_BYTE_CORRESPONDENCE', final_warning_hashes=final,
                      changed_in_focused_repair=changed,
                      reconstruction='POST_HOC; matches independently observed initial digest; not an original capture',
                      reconstructed_sha256=sha(old), source_first_seal_unchanged=True,
                      semantic_assessment='DIRECT_REVIEW.md; hashes do not prove fidelity'), indent=2))
