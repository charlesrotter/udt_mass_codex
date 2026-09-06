"""Read-only path adapter for the frozen independent saved-artifact comparison.

It changes exactly two path assignments in memory; no mathematics or checks change.
Use python3 -B. Output is stdout; this launcher writes no files.
"""
import sys
sys.dont_write_bytecode = True
import argparse
import difflib
import hashlib
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--review-dir', required=True, type=Path)
parser.add_argument('--candidate-dir', required=True, type=Path)
parser.add_argument('--show-path-diff', action='store_true')
args = parser.parse_args()
review = args.review_dir.resolve(strict=True)
candidate = args.candidate_dir.resolve(strict=True)
source_path = review/'stage_b_independent_artifacts.py'
source = source_path.read_text()
# Authenticate the archived inputs against their own frozen review manifest.
manifest = {}
for line in (review/'REVIEW_SHA256SUMS').read_text().splitlines():
    digest, name = line.split(maxsplit=1)
    manifest[name] = digest
for name in ('stage_b_independent_artifacts.py', 'stage_a_tensor.py'):
    actual = hashlib.sha256((review/name).read_bytes()).hexdigest()
    if actual != manifest[name]:
        raise RuntimeError(f'Frozen review source hash mismatch: {name}')
replacements = {
    "scratch=pathlib.Path('/tmp/udt-curvature-review-qassiP')":
        f'scratch=pathlib.Path({str(review)!r})',
    "pkg=pathlib.Path('/home/udt-admin/udt_mass_codex/udt_g313_curvature_phase_current_candidate_2026-09-06')":
        f'pkg=pathlib.Path({str(candidate)!r})',
}
adapted = source
for before, after in replacements.items():
    if adapted.count(before) != 1:
        raise RuntimeError('Expected exactly one frozen path assignment: '+before)
    adapted = adapted.replace(before, after, 1)
if args.show_path_diff:
    sys.stdout.writelines(difflib.unified_diff(source.splitlines(keepends=True),
        adapted.splitlines(keepends=True), fromfile='frozen/stage_b_independent_artifacts.py',
        tofile='in-memory/path-adapted-stage_b_independent_artifacts.py'))
else:
    exec(compile(adapted, str(source_path)+' [path-adapted in memory]', 'exec'),
         {'__name__':'__main__', '__file__':str(source_path)})
