"""Run unchanged candidate capture-runner code against controlled scratch children.

Only __file__ is redirected to the scratch stub directory. The original runner
source is read and compiled verbatim. This is an explicit operational probe,
not a mutation of candidate science or a claim about its normal baseline.
"""
from pathlib import Path
original = Path('/home/udt-admin/udt_mass_codex/udt_g349_normalized_cone_phase_extension_candidate_2026-09-06/run_checks.py')
scratch_runner_identity = '/tmp/udt-cone-review-0WvbvE/runner_probe/run_checks.py'
namespace = {'__name__':'__main__', '__file__':scratch_runner_identity}
exec(compile(original.read_text(), str(original), 'exec'), namespace)
