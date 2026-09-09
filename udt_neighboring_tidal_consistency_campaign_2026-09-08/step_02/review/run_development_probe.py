"""Actual isolated NT2 corruptions; reuse NT1's source-exec probe mechanism.

Original author files remain unchanged. Every replacement and source hash is
printed unbuffered before execution. These are implementation sensitivity
tests, not proposed scientific data repairs or new premises.
"""
import hashlib
import json
from pathlib import Path
import sys

path=Path(__file__).resolve().parents[1]/'check_development.py'
source=path.read_text()
probe=sys.argv[1]
replacements={
 'freeze_profiles':[("A=s.Function('A')(u);F=s.Function('F')(u)","A=-a*u;F=-b*u")],
 'reverse_normal_and_K':[
   ('n=s.Matrix([1,H+2,0,0])/s.sqrt(S)','n=-s.Matrix([1,H+2,0,0])/s.sqrt(S)'),
   ('Kdirect=s.Matrix(3,3,lambda i,j:-sum(', 'Kdirect=s.Matrix(3,3,lambda i,j:sum('),
   ('K=s.Matrix([[s.diff(H,u),s.diff(H,x),s.diff(H,y)]', 'K=-s.Matrix([[s.diff(H,u),s.diff(H,x),s.diff(H,y)]')
 ],
}
modified=source
for old,new in replacements[probe]:
    assert modified.count(old)==1,(probe,old)
    modified=modified.replace(old,new)
print(json.dumps({'probe':probe,'source':str(path),
   'source_sha256':hashlib.sha256(source.encode()).hexdigest(),
   'replacements':replacements[probe],
   'modified_sha256':hashlib.sha256(modified.encode()).hexdigest(),
   'classification':'actual corruption, original source unchanged'}),flush=True)
sys.argv=[str(path)]
exec(compile(modified,str(path),'exec'),{'__file__':str(path),'__name__':'__main__'})
