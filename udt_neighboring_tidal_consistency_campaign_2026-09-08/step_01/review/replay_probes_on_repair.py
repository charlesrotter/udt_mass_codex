"""Reapply the unchanged original corruption rules to the separately frozen repair."""
from pathlib import Path
original_probe=Path(__file__).with_name('run_author_probe.py')
source=original_probe.read_text()
old="/'check_nt1.py'"
new="/'check_nt1_repaired.py'"
assert source.count(old)==1
exec(compile(source.replace(old,new),str(original_probe),'exec'),
     {'__file__':str(original_probe),'__name__':'__main__'})
