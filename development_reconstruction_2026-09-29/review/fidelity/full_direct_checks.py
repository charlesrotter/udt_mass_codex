"""Bounded independent sign and correspondence checks for frozen full review."""
import csv,hashlib,json
from fractions import Fraction as F
from pathlib import Path

base=Path('development_reconstruction_2026-09-29')
checks=[]
def ck(name,truth):
    assert truth,name
    checks.append(name)
def outer(a,b):return [[x*y for y in b] for x in a]
def add(a,b):return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def scale(t,a):return [[t*x for x in r] for r in a]
C,S=F(5,4),F(3,4)
u,n=[-C,S],[-S,C]
e0,e1=[F(-1),F(0)],[F(0),F(1)]
half=add(outer(u,u),outer(n,n))
basehalf=add(outer(e0,e0),outer(e1,e1))
delta=add(half,scale(-(C*C+S*S),basehalf))
odot=add(outer(e0,e1),outer(e1,e0))
ck('boost_lowered_covector_positive_coefficient',delta==scale(2*C*S,odot))
ck('boost_coordinate_components_negative',delta[0][1]==delta[1][0]==F(-15,8))
ck('old_covector_basis_sign_rejected',delta!=scale(-2*C*S,odot))
freeze=json.loads((base/'FULL_CANDIDATE_FREEZE.json').read_text())
for p,h in freeze['files'].items():
    ck('pin:'+p,hashlib.sha256((base/p).read_bytes()).hexdigest()==h)
r=list(csv.DictReader((base/'CLAIM_DISPOSITIONS.tsv').open(),delimiter='\t'))
registry=list(csv.DictReader(open('CURRENT_SCIENTIFIC_PREMISES.tsv'),delimiter='\t'))
ck('registry_ids_exactly_once',len(r)==406 and len({x['premise_id'] for x in r})==406 and {x['premise_id'] for x in r}=={x['premise_id'] for x in registry})
print(json.dumps({'scope':'one independently lowered boost plus exact frozen bytes/ID coverage; not generic proof','count':len(checks),'checks':checks,'boost_half_tangent_difference':[[str(x) for x in row] for row in delta]},indent=2))
