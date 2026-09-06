"""Phase B author-code mutation: test coverage, not an independent proof."""
import pathlib
import sys

path = pathlib.Path('/home/udt-admin/udt_mass_codex/udt_shared_readout_metric_constraint_campaign_2026-09-06/step_05/check_exact.py')
source = path.read_text()
anchor = 'def construct(z, e):\n'
assert source.count(anchor) == 1
changed = source.replace(anchor, anchor + '    if any(z):\n        return None\n')
sys.argv = [str(path)]
exec(compile(changed, str(path) + ':reviewer_overreject_nonzero', 'exec'), {'__name__': '__main__'})
