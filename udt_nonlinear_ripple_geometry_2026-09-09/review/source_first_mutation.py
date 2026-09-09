"""Actual in-memory mutation of reviewer code; frozen source stays unchanged."""
from pathlib import Path
path=Path(__file__).with_name('source_first_tensor.py')
original=path.read_text()
old='lt=t*(pt*pt+b*b*px*px)'
new='lt=0*(pt*pt+b*b*px*px)'
assert original.count(old)==1
print('MUTATION: delete required time constraint response; expect original_Ricci failure.',flush=True)
exec(compile(original.replace(old,new),str(path)+'[delete_response]', 'exec'))
