"""Exact normalization repair of the frozen ACI1 controls; equations unchanged."""
from pathlib import Path
import hashlib
p=Path('udt_asymptotic_curvature_implication_2026-10-04/check_controls.py')
assert hashlib.sha256(p.read_bytes()).hexdigest()=='4db3dadcc9f8162677359b6f7a8e3fa02d04bbb0dd1dccc7b592cd3b71780582'
source=p.read_text()
replacements={
    'r=s.simplify(value)':
        'r=s.simplify(s.expand_trig(value).rewrite(s.exp))',
    "    details.append({'family':label":
        "    scalar,ric2,riem2=[s.simplify(s.expand_trig(v).rewrite(s.exp)) for v in (scalar,ric2,riem2)]\n    details.append({'family':label",
}
for old,new in replacements.items():
    assert source.count(old)==1,old
    source=source.replace(old,new,1)
exec(compile(source,str(p)+' [exact normalization repair]','exec'))
