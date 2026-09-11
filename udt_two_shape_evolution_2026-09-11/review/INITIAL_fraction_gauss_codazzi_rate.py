#!/usr/bin/env python3
"""Post-exposure independent-library full tensor check, no author/scientific imports."""
from fractions import Fraction as F
from itertools import product,permutations
import json,platform

n=range(3); four=range(4); inds=list(product(four,repeat=4))
def zmat(): return [[F(0) for j in n] for i in n]
def tr(A): return sum(A[i][i] for i in n)
def mul(A,B): return [[sum(A[i][k]*B[k][j] for k in n) for j in n] for i in n]
def combo(*terms): return [[sum(f*A[i][j] for f,A in terms) for j in n] for i in n]
def lev(t):
 if len(set(t))<len(t): return 0
 return (-1)**sum(t[i]>t[j] for i in range(len(t)) for j in range(i+1,len(t)))
def eps(a,b,c,d): return lev((a,b,c,d))
def tensor(E,M,Spa):
 # Antisymmetric pairs 0i or ij; E[i,j]=R[i0j0], M[i,j,k]=R[ij k0].
 Q={q:F(0) for q in inds}
 def put(a,b,c,d,v):
  for aa,bb,sg in [(a,b,1),(b,a,-1)]:
   for cc,dd,tg in [(c,d,1),(d,c,-1)]:
    Q[aa,bb,cc,dd]=Q[cc,dd,aa,bb]=sg*tg*v
 for i,j in product(n,repeat=2): put(i+1,0,j+1,0,E[i][j])
 for i,j,k in product(n,repeat=3):
  if i<j: put(i+1,j+1,k+1,0,M[i,j,k])
 for i,j,k,l in product(n,repeat=4):
  if i<j and k<l: put(i+1,j+1,k+1,l+1,Spa[i,j,k,l])
 return Q

def build(p,r,px,rx,pxx,rxx,s):
 d=p*p+r*r; kk=(d-s*s)/(2*s)
 K=[[kk,F(0),F(0)],[F(0),s-p,-r],[F(0),-r,s+p]]
 Kx=[[(p*px+r*rx)/s,F(0),F(0)],[F(0),-px,-rx],[F(0),-rx,px]]
 Kxx=[[(px*px+p*pxx+rx*rx+r*rxx)/s,F(0),F(0)],[F(0),-pxx,-rxx],[F(0),-rxx,pxx]]
 tau=tr(K); taux=tr(Kx); K2=mul(K,K); K3=mul(K2,K)
 Kt=combo((tau,K),(-2,K2))
 Ktx=combo((taux,K),(tau,Kx),(-2,mul(Kx,K)),(-2,mul(K,Kx)))
 Rt=zmat(); Rt[1][1]=-pxx;Rt[1][2]=Rt[2][1]=-rxx;Rt[2][2]=pxx
 E=combo((tau,K),(-1,K2)); Et=combo((1,Rt),(2*tau*tau,K),(-4*tau,K2),(2,K3))
 Ex=combo((taux,K),(tau,Kx),(-1,mul(Kx,K)),(-1,mul(K,Kx)))
 def Dx(A,der,i,j): return A[i][j] if der==0 else F(0)
 def Gt(a,b,c): return -Dx(Kx,b,a,c)-Dx(Kx,c,a,b)+Dx(Kx,a,b,c)
 def Cod(A,i,j,k): return Dx(A,j,i,k)-Dx(A,i,j,k)
 M={(i,j,k):Cod(Kx,i,j,k) for i,j,k in product(n,repeat=3)}
 Mx={(i,j,k):Cod(Kxx,i,j,k) for i,j,k in product(n,repeat=3)}
 Mt={(i,j,k):Cod(Ktx,i,j,k)+sum(-Gt(a,j,k)*K[i][a]+Gt(a,i,k)*K[j][a] for a in n) for i,j,k in product(n,repeat=3)}
 def second(i,j,a,b): return -2*Kxx[i][j] if a==b==0 else F(0)
 Spa={};Spat={};Spax={}
 for i,j,k,l in product(n,repeat=4):
  Spa[i,j,k,l]=K[i][k]*K[j][l]-K[i][l]*K[j][k]
  Spax[i,j,k,l]=Kx[i][k]*K[j][l]+K[i][k]*Kx[j][l]-Kx[i][l]*K[j][k]-K[i][l]*Kx[j][k]
  curvature_t=(second(i,l,j,k)+second(j,k,i,l)-second(i,k,j,l)-second(j,l,i,k))/2
  Spat[i,j,k,l]=curvature_t+Kt[i][k]*K[j][l]+K[i][k]*Kt[j][l]-Kt[i][l]*K[j][k]-K[i][l]*Kt[j][k]
 R=tensor(E,M,Spa);RD=tensor(Et,Mt,Spat);RX=tensor(Ex,Mx,Spax)
 return K,Kx,Kxx,tau,R,RD,RX

def full_scalar(K,tau,R,RD,scales=(F(1),F(1),F(1),F(1)),freeze_volume=False):
 gi=[F(-1)/(scales[0]**2)]+[1/(scales[i]**2) for i in (1,2,3)]
 gid=[[F(0) for j in four] for i in four]
 for i,j in product(n,repeat=2): gid[i+1][j+1]=2*K[i][j]/(scales[i+1]*scales[j+1])
 vol=scales[0]*scales[1]*scales[2]*scales[3]
 RR={q:R[q]*scales[q[0]]*scales[q[1]]*scales[q[2]]*scales[q[3]] for q in inds}
 RT={q:RD[q]*scales[q[0]]*scales[q[1]]*scales[q[2]]*scales[q[3]] for q in inds}
 star={}; stard={}
 for a,b,c,h in inds:
  star[a,b,c,h]=sum(F(eps(a,b,e,f),2)*vol*gi[e]*gi[f]*RR[e,f,c,h] for e,f in product(four,repeat=2))
  stard[a,b,c,h]=sum(F(eps(a,b,e,f),2)*vol*gi[e]*gi[f]*RT[e,f,c,h] for e,f in product(four,repeat=2))
  if not freeze_volume: stard[a,b,c,h]-=tau*star[a,b,c,h]
  stard[a,b,c,h]+=sum(F(eps(a,b,e,f),2)*vol*(gid[e][m]*gi[f]*RR[m,f,c,h]+gi[e]*gid[f][m]*RR[e,m,c,h]) for e,f,m in product(four,repeat=3))
 P=sum(gi[a]*gi[b]*gi[c]*gi[h]*RR[a,b,c,h]*star[a,b,c,h] for a,b,c,h in inds)
 PD=sum(gi[a]*gi[b]*gi[c]*gi[h]*(RT[a,b,c,h]*star[a,b,c,h]+RR[a,b,c,h]*stard[a,b,c,h]) for a,b,c,h in inds)
 for q in inds:
  for pos in four:
   factor=F(1)
   for j in four:
    if j!=pos:factor*=gi[q[j]]
   for m in four:
    alt=list(q);alt[pos]=m
    PD+=factor*gid[q[pos]][m]*RR[q]*star[tuple(alt)]
 return P,PD

def run(name,datum):
 p,r,px,rx,pxx,rxx,s=datum
 K,Kx,Kxx,tau,R,RD,RX=build(*datum)
 signs=[-1,1,1,1];giD=[[F(0) for j in four] for i in four]
 for i,j in product(n,repeat=2):giD[i+1][j+1]=2*K[i][j]
 ric=[sum(signs[a]*R[a,b,a,d] for a in four) for b,d in product(four,repeat=2)]
 ricd=[sum(signs[a]*RD[a,b,a,d] for a in four)+sum(giD[a][c]*R[a,b,c,d] for a,c in product(four,repeat=2)) for b,d in product(four,repeat=2)]
 assert all(x==0 for x in ric+ricd),(name,'Ric/Ric_T')
 def Gamma(a,b,c):
  if a==0 and b and c: return -K[b-1][c-1]
  if a and b==0 and c: return -K[a-1][c-1]
  if a and c==0 and b: return -K[a-1][b-1]
  return F(0)
 cov={}
 for der in four:
  for q in inds:
   value=RD[q] if der==0 else RX[q] if der==1 else F(0)
   for pos in four:
    for m in four:
     alt=list(q);alt[pos]=m
     value-=Gamma(m,der,q[pos])*R[tuple(alt)]
   cov[der,*q]=value
 bianchi=[cov[a,b,c,d,e]+cov[b,c,a,d,e]+cov[c,a,b,d,e] for a,b,c,d,e in product(four,repeat=5)]
 assert all(x==0 for x in bianchi),(name,'differential Bianchi')
 actual=full_scalar(K,tau,R,RD)
 W=p*rx-r*px;d=p*p+r*r
 formula=(-16*W*(d-s*s)/s,-8*W*(5*d*d+6*d*s*s-11*s**4)/(s*s)-32*(pxx*rx-px*rxx))
 assert actual==formula,(name,actual,formula)
 changed=full_scalar(K,tau,R,RD,(F(1),F(2),F(3),F(5)))
 assert changed==actual,(name,'constant chart scaling')
 frozen_volume=full_scalar(K,tau,R,RD,freeze_volume=True)
 # Six records reconstructed using an exact six-by-six linear solve, not source polarization.
 directions=[(1,0,0),(0,1,0),(0,0,1),(1,1,0),(1,0,1),(0,1,1)]
 def recover(A):
  rows=[]
  for x,y,z in directions:
   v=(x,y,z);q=-2*sum(F(v[i]*v[j])*A[i][j] for i,j in product(n,repeat=2))
   rows.append([F(x*x),F(y*y),F(z*z),F(2*x*y),F(2*x*z),F(2*y*z),-q/2])
  for j in range(6):
   k=next(k for k in range(j,6) if rows[k][j]);rows[j],rows[k]=rows[k],rows[j]
   div=rows[j][j];rows[j]=[x/div for x in rows[j]]
   for k in range(6):
    if k!=j:
     fac=rows[k][j];rows[k]=[rows[k][l]-fac*rows[j][l] for l in range(7)]
  a,b,c,h,i,j=[row[-1] for row in rows]
  return [[a,h,i],[h,b,j],[i,j,c]]
 assert recover(K)==K and recover(Kx)==Kx and recover(Kxx)==Kxx
 return {'name':name,'datum':list(map(str,datum)),'P':str(actual[0]),'U_P':str(actual[1]),
  'checks':{'Ricci_components':16,'Ricci_rate_components':16,'differential_Bianchi_components':1024,
    'full_Hodge_contraction_and_rate':True,'positive_nonorthonormal_chart':True,'six_record_exact_elimination_K_KX_KXX':True},
  'frozen_volume_rate_error':str(frozen_volume[1]-actual[1])}

data=[('safe_harmonic',(F(1,8),F(1,12),-F(1,10),F(1,7),-F(1,8),-F(1,12),-F(2,3))),
 ('initial_cancellation',(F(2,3),F(0),F(0),F(2,3),-F(2,3),F(0),F(2,3)))]
print(json.dumps({'status':'PASS','python':platform.python_version(),'arithmetic':'standard fractions only',
 'exposure':'POST_STAGE_A_AND_AUTHOR_CODE_EXPOSURE; no source scientific implementation imported',
 'checks':[run(name,datum) for name,datum in data]},indent=2))
