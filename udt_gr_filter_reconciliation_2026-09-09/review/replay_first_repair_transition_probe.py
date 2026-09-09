"""POST-HOC reconstruction and execution, never a contemporaneous old run."""
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile

R = Path(__file__).resolve().parent
P = R.parent
ROOT = P.parent
BASE = 'a9896cb190e9c4aa8fd8a317cfaaa942d64e0a19'
OLD_SHA = '917800b0d2011b2f5c5aa5b282dd1c4316894a6d0bc34c1270f1aca2f49a7f7c'
GIT = ['git', '-c', 'core.preloadIndex=false', '-c', 'index.threads=1',
       '-c', 'core.packedGitWindowSize=16m', '-c', 'core.packedGitLimit=64m']
patch_data = (P / 'REPAIRED_IMPLEMENTATION.patch').read_bytes()
assert hashlib.sha256(patch_data).hexdigest() == \
    '9ac4e0858334e95e3f1d8da1706dd69a413a4fef5354bae37fef240026267fd9'
marker = b'diff --git a/verify_current_scientific_premises.py b/verify_current_scientific_premises.py\n'
assert patch_data.count(marker) == 1
verifier_patch = marker + patch_data.split(marker, 1)[1].split(b'\ndiff --git ', 1)[0]
with tempfile.TemporaryDirectory(prefix='udt-gr-first-repair-reconstruction-') as temporary:
    scratch = Path(temporary)
    source = scratch / 'verify_current_scientific_premises.py'
    baseline = subprocess.run(GIT + ['show', BASE + ':verify_current_scientific_premises.py'],
        cwd=ROOT, capture_output=True, check=True, timeout=10).stdout
    source.write_bytes(baseline)
    subprocess.run(GIT + ['apply', '--check', '-'], input=verifier_patch,
        cwd=scratch, capture_output=True, check=True, timeout=10)
    subprocess.run(GIT + ['apply', '-'], input=verifier_patch,
        cwd=scratch, capture_output=True, check=True, timeout=10)
    assert hashlib.sha256(source.read_bytes()).hexdigest() == OLD_SHA
    spec = importlib.util.spec_from_file_location('verify_current_scientific_premises', source)
    module = importlib.util.module_from_spec(spec)
    sys.modules['verify_current_scientific_premises'] = module
    spec.loader.exec_module(module)
    module.ROOT = ROOT  # Real source repository for the unchanged scoped fixture/history readers.
    stream = io.StringIO()
    code = 0
    with contextlib.redirect_stdout(stream):
        try:
            runpy.run_path(str(R / 'probe_transition_snapshot.py'), run_name='__main__')
        except SystemExit as error:
            code = error.code
    result = json.loads(stream.getvalue())
    print(json.dumps({'chronology': 'POST_HOC_FIRST_REPAIR_RECONSTRUCTION_AND_EXECUTION',
        'baseline': BASE, 'reconstructed_verifier_sha256': OLD_SHA,
        'first_repair_patch_sha256': hashlib.sha256(patch_data).hexdigest(),
        'shared_fixture': 'Current final author fixture; startup copy helper unchanged by repair',
        'source_root_override': 'module.ROOT points to real frozen source root; root arguments remain scratch',
        'probe': result}, indent=2))
    raise SystemExit(code)
