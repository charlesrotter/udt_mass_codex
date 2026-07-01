import sympy as sp
import random

coords = sp.symbols('x0 x1 x2 x3')
Th = sp.Function('Theta')(*coords)
Ph = sp.Function('Phi')(*coords)
n = sp.Matrix([sp.sin(Th)*sp.cos(Ph), sp.sin(Th)*sp.sin(Ph), sp.cos(Th)])
assert sp.simplify((n.T*n)[0]-1)==0
dn=[sp.Matrix([sp.diff(c,coords[m]) for c in n]) for m in range(4)]
for m in range(4): assert sp.simplify((n.T*dn[m])[0])==0
print("[0,1] |n|=1 and n.d_m n=0 identically: OK")
def cross(a,b): return sp.Matrix([a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]])
S=[[cross(dn[m],dn[k]) for k in range(4)] for m in range(4)]
F=[[(n.T*cross(dn[m],dn[k]))[0] for k in range(4)] for m in range(4)]

# Claim A symbolic, all 256 pairs
allok=True; cnt=0
for m in range(4):
  for k in range(4):
    for p in range(4):
      for q in range(4):
        d=sp.simplify((S[m][k].T*S[p][q])[0]-F[m][k]*F[p][q])
        cnt+=1
        if d!=0: allok=False; print("MISMATCH",(m,k,p,q),d)
print(f"[2] CLAIM A S.S==FF all {cnt} pairs:",allok)

# Metric contraction: prove via random NUMERIC substitution (field derivs as
# free symbols) for BOTH UDT-diagonal and a random symmetric NON-DIAGONAL g.
# Build numeric lambdified arrays. Replace the 8 first-derivatives of Theta,Phi
# (d_m Theta, d_m Phi) and Theta,Phi themselves with random reals.
syms=[Th,Ph]+[sp.diff(Th,coords[m]) for m in range(4)]+[sp.diff(Ph,coords[m]) for m in range(4)]
def randsub():
    return {s: random.uniform(-2,2) for s in syms}

def num(expr,sub):
    return float(expr.subs(sub).evalf())

# UDT inverse metric numeric (random phi,c,r,theta)
def check_metric(ginv_num, label):
    worst=0
    for _ in range(6):
        sub=randsub()
        Fn=[[num(F[m][k],sub) for k in range(4)] for m in range(4)]
        Sn=[[ [num(S[m][k][i],sub) for i in range(3)] for k in range(4)] for m in range(4)]
        g=ginv_num()
        tF=tS=0.0
        for m in range(4):
          for k in range(4):
            for p in range(4):
              for q in range(4):
                w=g[m][p]*g[k][q]
                tF+=w*Fn[m][k]*Fn[p][q]
                tS+=w*sum(Sn[m][k][i]*Sn[p][q][i] for i in range(3))
        worst=max(worst,abs(tF-tS))
    print(f"[{label}] max|g.gFF - g.gSS| over random fields = {worst:.2e}")

import math
def udt_ginv():
    phi=random.uniform(-3,3); c=random.uniform(0.5,2); r=random.uniform(0.5,3); th=random.uniform(0.3,2.8)
    return [[-math.exp(2*phi)/c**2,0,0,0],[0,math.exp(-2*phi),0,0],[0,0,1/r**2,0],[0,0,0,1/(r**2*math.sin(th)**2)]]
def nondiag_ginv():
    M=[[random.uniform(-1,1) for _ in range(4)] for _ in range(4)]
    return [[ (M[i][j]+M[j][i]) for j in range(4)] for i in range(4)]  # symmetric

check_metric(udt_ginv,"3 UDT-diag")
check_metric(nondiag_ginv,"4 NON-diag")
print("Normalization note: 1/4 vs 1/2 vs 1/32 only rescales kappa => native-vs-not unaffected.")
