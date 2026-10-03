"""Independent stdlib exact recomputation from saved observable coefficients."""
from pathlib import Path
from fractions import Fraction as Q
import json,hashlib,platform
B=Path(__file__).resolve().parent; p=B/'EXACT_RESULT.json';d=json.loads(p.read_text());out=[]
for row in d['saved_clock_jets']:
 b3,b4,b5=(Q(row[n]) for n in ['b3','b4','b5'])
 alpha=-b3/(120*(b5-Q(12,5)*b4*b4/b3));beta=-alpha*b4/(27*b3*b3);P0=36*b3
 assert alpha==Q(row['alpha']);assert beta==Q(row['beta']);assert P0==Q(row['P0'])
 # Original homogeneous spatial equation at constant and linear proper time.
 d0=-144*alpha*b4-3888*beta*b3*b3
 d1=-720*alpha*b5-77760*beta*b3*b4-6*b3
 assert d0==0,d0;assert d1==0,d1
 assert Q(row['flat_M2'])==1/(6*alpha)
 quadratic_only_b5=-b3/(120*alpha)
 out.append({'name':row['name'],'recovered_alpha':str(alpha),'recovered_beta':str(beta),'recovered_P0':str(P0),'original_spatial_constant':str(d0),'original_spatial_linear':str(d1),'quadratic_clock_test_defect':str(b5-quadratic_only_b5)})
assert Q(out[1]['quadratic_clock_test_defect'])!=0
result={'status':'PASS','source':str(p.relative_to(B.parent)),'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'python':platform.python_version(),'results':out,'limits':'Exposed rational saved-coefficient check, no independent observation or full interval certification.'}
with (B/'SAVED_JET_RESULT.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps(result,indent=2))
