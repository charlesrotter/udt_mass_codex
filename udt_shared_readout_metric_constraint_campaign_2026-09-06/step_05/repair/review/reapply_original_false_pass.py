"""Focus-only author-code mutation; not an independent scientific implementation."""
import pathlib
import sys

path=pathlib.Path('/home/udt-admin/udt_mass_codex/udt_shared_readout_metric_constraint_campaign_2026-09-06/step_05/repair/check_exact.py')
source=path.read_text()
anchor='def construct(z, e):\n'
assert source.count(anchor)==1
source=source.replace(anchor,anchor+'    if any(z):\n        return None\n')
sys.argv=[str(path)]
exec(compile(source,str(path)+':reviewer_original_overreject','exec'),{'__name__':'__main__'})
