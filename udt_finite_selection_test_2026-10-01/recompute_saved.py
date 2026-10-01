"""Exposed saved-output recomputation; independent implementation, shared inputs."""
from fractions import Fraction as Q
from pathlib import Path
import json,hashlib
b=Path(__file__).parent;s=b/'math/exact.stdout';j=json.loads(s.read_text());v=list(map(Q,j['common_nullspace'][0]));pairs=[(i,k) for i in range(4) for k in range(i,4)];E=[[Q(0) for _ in range(4)]for _ in range(4)]
for value,(i,k) in zip(v,pairs):E[i][k]=E[k][i]=value
checks=0
# Conjugate saved tensor by new rational boosts in each spatial direction.
for direction in [1,2,3]:
 B=[[Q(i==k) for k in range(4)]for i in range(4)];B[0][0]=B[direction][direction]=Q(13,5);B[0][direction]=B[direction][0]=Q(12,5)
 for i in range(4):
  for k in range(4):
   z=sum(B[a][i]*E[a][c]*B[c][k] for a in range(4) for c in range(4));assert z==E[i][k];checks+=1
for row in j['curvature_rows']:
 k=Q(row['kappa']);R=Q(row['R']);Ric00=Q(row['Ric00']);assert R==-4*Ric00;checks+=1;assert R/12==k;checks+=1
r=j['contrast'];p=Q(r['p']);p0=Q(r['p0']);assert p/p0==Q(r['p_ratio']);checks+=1;assert p0<p<1;checks+=1
# Reciprocal cosh inputs inferred from saved clock ratios retain exact duplication.
assert 1/p0==2*(1/p)**2-1;checks+=1
print(json.dumps({'status':'PASS','assertions':checks,'input_sha256':hashlib.sha256(s.read_bytes()).hexdigest(),'scope':'Saved invariant tensor, curvature contractions and clock ratio/duplication; no independent worldline or rank reconstruction.'},indent=2))
