"""Post-exposure independent Fraction replay and actual wrong-rule catches."""
from fractions import Fraction as F
import json
from pathlib import Path
out=Path('/home/udt-admin/udt_mass_codex/udt_finite_separation_law_2026-09-28/review')
def mm(a,b):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def mv(a,v):return [sum(x*y for x,y in zip(row,v)) for row in a]
def eye():return [[F(i==j) for j in range(4)]for i in range(4)]
def B(axis,c,s):
 a=eye();a[0][0]=a[axis][axis]=c;a[0][axis]=a[axis][0]=s;return a
def inverse(a):
 sign=[-1,1,1,1];return [[a[j][i]*sign[i]*sign[j] for j in range(4)] for i in range(4)]
def apply(a,n):
 v=mv(a,[F(1),*n]);return v[0],[x/v[0] for x in v[1:]]
def eq(a,b):assert a==b,(a,b)
catches=[]
def rejects(name,fn):
 try:fn()
 except AssertionError:catches.append(name)
 else:raise AssertionError('mutation false pass: '+name)
a=B(1,F(5,4),F(3,4));b=B(2,F(5,3),F(4,3));ab=mm(b,a)
records=[]
for i,n in enumerate([[F(0),F(1),F(0)],[F(1,3),F(2,3),F(2,3)]]):
 f1,n1=apply(a,n);f2,no=apply(b,n1);f,nfull=apply(ab,n)
 eq(f,f1*f2);eq(no,nfull)
 c=mv(ab,[1,0,0,0]);Z=c[0]-sum(x*y for x,y in zip(c[1:],no))
 eq(Z,1/f)
 fi,ni=apply(inverse(ab),no);eq(f*fi,1);eq(ni,n)
 wrong=apply(b,n)[0]*f1
 rejects(f'case{i}_uncarried_composition',lambda:eq(wrong,f))
 rejects(f'case{i}_gamma_as_redshift',lambda:eq(c[0],Z))
 rejects(f'case{i}_uncarried_inverse',lambda:eq(apply(inverse(ab),n)[0]*f,1))
 records.append({'f':str(f),'Z':str(Z),'wrong_frequency':str(wrong),'gamma':str(c[0])})
# Test the precise orientation omission: future orthonormal is not enough for SO+.
reflect=eye();reflect[1][1]=-1
eta=eye();eta[0][0]=-1
transpose=lambda a:list(map(list,zip(*a)))
eq(mm(mm(transpose(reflect),eta),reflect),eta)
eq(mv(reflect,[1,0,0,0]),[1,0,0,0])
rejects('future_frame_alone_forces_positive_determinant',lambda:eq(reflect[1][1],1))
q=F(2);gamma=1+q*q/2;sp=[q*q/2,q,0];Z=gamma-sp[0]
eq(Z,1)
rejects('projective_norm_as_redshift',lambda:eq(gamma,Z))
result={'records':records,'actual_mutations_rejected':catches,'count_mutations':len(catches),'orientation_separator':'diag(1,-1,1,1): future metric-preserving, determinant -1','stage':'author code/results exposed; independently coded Fraction arithmetic; no author imports'}
with(out/'direct_fraction_result.json').open('x')as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps(result,indent=2))
