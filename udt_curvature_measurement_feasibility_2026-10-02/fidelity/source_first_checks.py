"""Independent finite rational controls; no candidate code imports or physics fit."""
from fractions import Fraction as Q
from itertools import product
import json, math, platform

checks = []
def check(name, condition, evidence):
    checks.append(dict(name=name, passed=bool(condition), evidence=evidence))
    if not condition:
        raise AssertionError(name)

def bilinear(a, x, y):
    return sum(a[i][j]*x[i]*y[j] for i,j in product(range(4), repeat=2))

def rank(a):
    a=[list(map(Q,row)) for row in a]
    r=0
    for j in range(len(a[0])):
        p=next((i for i in range(r,len(a)) if a[i][j]),None)
        if p is None: continue
        a[r],a[p]=a[p],a[r]
        pivot=a[r][j]
        a[r]=[x/pivot for x in a[r]]
        for i in range(len(a)):
            if i!=r:
                q=a[i][j]
                a[i]=[x-q*y for x,y in zip(a[i],a[r])]
        r+=1
    return r

g=[[Q((-1 if i==0 else 1) if i==j else 0) for j in range(4)] for i in range(4)]
basis=[[Q(i==j) for i in range(4)] for j in range(4)]
frames=[basis[0]]
for i in range(1,4):
    for s in [-1,1]:
        frames.append([Q(5,4) if j==0 else Q(s*3,4) if j==i else Q(0) for j in range(4)])
check('all seven frames unit timelike',all(bilinear(g,u,u)==-1 for u in frames),frames)
weights=[-Q(28,3)]+[Q(8,9)]*6
indices=[(i,j) for i in range(4) for j in range(i,4)]
design=[[u[i]*u[j]*(1 if i==j else 2) for i,j in indices] for u in frames]
check('seven-frame design rank',rank(design)==7,rank(design))
for i,j in indices:
    a=[[Q((k,l)==(i,j) or (k,l)==(j,i)) for l in range(4)] for k in range(4)]
    recovered=sum(w*bilinear(a,u,u) for w,u in zip(weights,frames))
    true=-a[0][0]+sum(a[k][k] for k in range(1,4))
    check('scalar basis component '+str((i,j)),recovered==true,dict(recovered=recovered,true=true))
invisible=[[Q((i,j) in [(1,2),(2,1)]) for j in range(4)] for i in range(4)]
check('spatial off-diagonal tensor invisible',all(bilinear(invisible,u,u)==0 for u in frames),invisible)
check('worst-case scalar amplification',sum(map(abs,weights))==Q(44,3),sum(map(abs,weights)))

# Change the orthonormal tetrad with another rational boost, and verify that
# contractions against the transformed arbitrary tensor recover the same scalar.
lorentz=[row[:] for row in basis]
lorentz[0]=[Q(5,3),Q(4,3),Q(0),Q(0)]
lorentz[1]=[Q(4,3),Q(5,3),Q(0),Q(0)]
check('independent boost orthonormal',all(bilinear(g,x,y)==g[i][j] for i,x in enumerate(lorentz) for j,y in enumerate(lorentz)),lorentz)
ric=[[Q(i+j+1 if i!=j else (i+1)**2) for j in range(4)] for i in range(4)]
new_ric=[[bilinear(ric,x,y) for y in lorentz] for x in lorentz]
old_scalar=-ric[0][0]+sum(ric[i][i] for i in range(1,4))
new_scalar=sum(w*bilinear(new_ric,u,u) for w,u in zip(weights,frames))
check('scalar is tetrad independent in rational control',old_scalar==new_scalar,dict(old=old_scalar,new=new_scalar))

# Direct coordinate Ricci reconstruction from the metric jet diag(-1,b,b,b),
# b=1+2t, g'=diag(0,2,2,2), g''=0. No field-equation or supplied Ricci formula.
def curvature_control(t):
    b=1+2*t
    gd=[Q(-1),b,b,b]; inv=[1/x for x in gd]; deriv=[Q(0),Q(2),Q(2),Q(2)]
    def dg(a,i,j):return deriv[i] if a==0 and i==j else Q(0)
    gamma=[[[Q(1,2)*inv[a]*(dg(c,a,d)+dg(d,a,c)-dg(a,c,d)) for d in range(4)] for c in range(4)] for a in range(4)]
    def dgamma(k,a,c,d):
        if k: return Q(0)
        return -deriv[a]*inv[a]*gamma[a][c][d]
    ric=[]
    for m in range(4):
        row=[]
        for n in range(4):
            x=sum(dgamma(a,a,m,n)-dgamma(n,a,m,a) for a in range(4))
            x+=sum(gamma[a][a][bb]*gamma[bb][m][n]-gamma[a][n][bb]*gamma[bb][m][a] for a,bb in product(range(4),repeat=2))
            row.append(x)
        ric.append(row)
    scalar=sum(inv[a]*ric[a][a] for a in range(4))
    return scalar,ric
for t in [Q(0),Q(1,2),Q(3,2)]:
    scalar,tensor=curvature_control(t)
    check('trace false-pass control at '+str(t),scalar==0 and tensor[0][0]>0,dict(R=scalar,Ric00=tensor[0][0]))

# Finite difference bias/noise constants, independently assembled binomial weights.
for order in [2,4,5]:
    w=[Q((-1)**(order-j)*math.comb(order,j),math.factorial(order)) for j in range(order+1)]
    for power in range(order):
        check('finite difference vanishing '+str((order,power)),sum(wj*j**power for j,wj in enumerate(w))==0,power)
    check('finite difference unit '+str(order),sum(wj*j**order for j,wj in enumerate(w))==1,w)
    check('next Taylor monomial bias '+str(order),sum(wj*j**(order+1) for j,wj in enumerate(w))==Q(order*(order+1),2),sum(wj*j**(order+1) for j,wj in enumerate(w)))
    check('finite difference noise norm '+str(order),sum(map(abs,w))==Q(2**order,math.factorial(order)),sum(map(abs,w)))

# The quadratic trace is R=6 alpha X+4 Lambda, X=Box R. These are arbitrary
# exact diagnostic pairs, not synthetic observations or native geometries.
alpha=Q(2,3); lam=Q(-5,7)
points=[(x,6*alpha*x+4*lam) for x in [Q(-2),Q(0),Q(3)]]
a=(points[1][1]-points[0][1])/(6*(points[1][0]-points[0][0]))
l=(points[0][1]-6*a*points[0][0])/4
check('affine trace recovery with independent third-point check',a==alpha and l==lam and points[2][1]==6*a*points[2][0]+4*l,dict(alpha=a,Lambda=l,points=points))
check('distinct R does not imply identifiable fit',Q(2)-Q(1)!=0 and Q(3)-Q(3)==0,'Same Box R=3, distinct R=1,2 is incompatible with every finite alpha.')

out=dict(status='PASS',checks=len(checks),python=platform.python_version(),library='Python stdlib Fraction only',controls=checks)
print(json.dumps(out,indent=2,default=str))
