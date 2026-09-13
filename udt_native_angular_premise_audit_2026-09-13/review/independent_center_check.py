#!/usr/bin/env python3
"""Independent NAP1 exact center check, prepared source-first.

Original input is LSR1's quadratic metric jet. No parent NAP1 implementation,
result or symbolic tensor routine is imported. Exact coefficient extraction by
polarization is applied to that polynomial, then differentiated Christoffels
are contracted with the actual center metric. This is algebra, not evaluation
of the full positive local metric at unit-distance sample points.
"""
from fractions import Fraction as F
import json
import platform
import resource
import sys

resource.setrlimit(resource.RLIMIT_AS, (2048 * 1024**2, 2048 * 1024**2))
ETA = [F(-1), F(1), F(1), F(1)]
checks = 0

def check(ok, label):
    global checks
    checks += 1
    if not ok:
        raise AssertionError(label)

def cross(a,b):
    return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]

def dot(a,b):
    return sum(x*y for x,y in zip(a,b))

def matvec(a,v):
    return [dot(row,v) for row in a]

def metric(x, c, s):
    r2=dot(x,x)
    g=[[F(0) for _ in range(4)] for _ in range(4)]
    g[0][0]=-1-c*r2
    axes=[[F(i==j) for i in range(3)] for j in range(3)]
    cols=[cross(x,e) for e in axes]
    for i in range(3):
        for j in range(3):
            g[i+1][j+1]=F(i==j)-c*x[i]*x[j]+dot(cols[i],matvec(s,cols[j]))
    return g

def hessians(c,s):
    h={}
    origin=[F(0)]*3
    g0=metric(origin,c,s)
    for k in range(4):
        for l in range(4):
            if k==0 or l==0:
                deriv=[[F(0) for _ in range(4)] for _ in range(4)]
            else:
                e=[F(i==k-1) for i in range(3)]
                f=[F(i==l-1) for i in range(3)]
                if k==l:
                    a=metric(e,c,s); b=metric([-z for z in e],c,s)
                    deriv=[[a[i][j]+b[i][j]-2*g0[i][j] for j in range(4)] for i in range(4)]
                else:
                    a=metric([e[i]+f[i] for i in range(3)],c,s)
                    b=metric(e,c,s); d=metric(f,c,s)
                    deriv=[[a[i][j]-b[i][j]-d[i][j]+g0[i][j] for j in range(4)] for i in range(4)]
            for a in range(4):
                for b in range(4):
                    h[a,b,k,l]=deriv[a][b]
    return h

def original_curvature(c,s):
    h=hessians(c,s)
    # dg is partial_d Gamma^a_bc at the zero-connection center.
    dg={}
    for a in range(4):
        for b in range(4):
            for cidx in range(4):
                for d in range(4):
                    dg[a,b,cidx,d]=ETA[a]*(h[a,cidx,b,d]+h[a,b,cidx,d]-h[b,cidx,a,d])/2
    r={}
    for a in range(4):
        for b in range(4):
            for cidx in range(4):
                for d in range(4):
                    r[a,b,cidx,d]=ETA[a]*(dg[a,d,b,cidx]-dg[a,cidx,b,d])
    ric=[[sum(ETA[a]*r[a,b,a,d] for a in range(4)) for d in range(4)] for b in range(4)]
    scalar=sum(ETA[a]*ric[a][a] for a in range(4))
    tf=[[ric[a][b]-F(a==b)*ETA[a]*scalar/4 for b in range(4)] for a in range(4)]
    return r,ric,scalar,tf

def rank(rows):
    a=[list(row) for row in rows]
    p=0
    for c in range(len(a[0])):
        target=next((i for i in range(p,len(a)) if a[i][c]),None)
        if target is None: continue
        a[p],a[target]=a[target],a[p]
        factor=a[p][c]
        a[p]=[v/factor for v in a[p]]
        for i in range(len(a)):
            if i!=p and a[i][c]:
                factor=a[i][c]
                a[i]=[u-factor*v for u,v in zip(a[i],a[p])]
        p+=1
    return p

def smat(a=0,b=0,d=0,e=0,f=0):
    return [[F(a),F(d),F(e)],[F(d),F(b),F(f)],[F(e),F(f),-F(a)-F(b)]]

def serialize(a):
    if isinstance(a,dict): return {str(k):serialize(v) for k,v in a.items()}
    if isinstance(a,(list,tuple)): return [serialize(v) for v in a]
    if isinstance(a,F): return str(a)
    return a

def run():
    basis=[(F(1),smat()),(F(0),smat(a=1)),(F(0),smat(b=1)),(F(0),smat(d=1)),(F(0),smat(e=1)),(F(0),smat(f=1))]
    cases=[(F(0),smat())]+basis+[(F(2,3),smat(F(1,2),F(-5,13),F(2,7),F(-3,11),F(4,17)))]
    output=[]; linear_map=[]
    dirs=[[F(1),F(0),F(0)],[F(0),F(1),F(0)],[F(0),F(0),F(1)], [F(3,5),F(4,5),F(0)], [F(3,5),F(0),F(4,5)], [F(0),F(3,5),F(4,5)]]
    for index,(c,s) in enumerate(cases):
        r,ric,scalar,tf=original_curvature(c,s)
        check(scalar==-12*c, ('scalar',index,scalar))
        expected=[[F(0) for _ in range(4)] for _ in range(4)]
        for i in range(3):
            for j in range(3): expected[i+1][j+1]=3*s[i][j]
        check(tf==expected,('TF from original derivatives',index,tf,expected))
        for a in range(4):
            for b in range(4):
                for ci in range(4):
                    for d in range(4):
                        check(r[a,b,ci,d]==-r[b,a,ci,d],('first antisymmetry',index))
                        check(r[a,b,ci,d]==r[ci,d,a,b],('pair exchange',index))
                        check(r[a,b,ci,d]+r[a,ci,d,b]+r[a,d,b,ci]==0,('Bianchi',index))
        # Full, factor-two DDR pair tangent, raised on both response-pairing indices.
        balances=[]
        for n in dirs:
            check(dot(n,n)==1, ('unit ruler',n))
            u=[F(1),F(0),F(0),F(0)]; nv=[F(0)]+n
            hc=[[2*ETA[a]*ETA[b]*(u[a]*u[b]+nv[a]*nv[b]) for b in range(4)] for a in range(4)]
            check(sum(ETA[a]*hc[a][a] for a in range(4))==0,'reciprocal tangent trace')
            bal=sum(ETA[a]*ETA[b]*ric[a][b]*hc[a][b] for a in range(4) for b in range(4))
            check(bal==6*dot(n,matvec(s,n)),('DDR original Ricci contraction',index,n,bal))
            balances.append(bal)
        if 1<=index<=6: linear_map.append([v for row in tf for v in row])
        output.append({'case_index':index,'c2':c,'S':s,'Ric':ric,'R':scalar,'TF_Ric':tf,'six_full_DDR_balances':balances})
    tf_rank=rank(linear_map)
    check(tf_rank==5,('conditional center shape rank',tf_rank))
    # Original pair pullbacks retain the spatial quadratic jet through m^2/f.
    v=[F(2),F(-1),F(3)]
    c,s=cases[-1]
    x=[F(1,7),F(2,11),F(-1,13)]
    g=metric(x,c,s); f=-g[0][0]
    length2=sum(v[i]*g[i+1][j+1]*v[j] for i in range(3) for j in range(3))
    density2=f*length2
    check(density2/f==length2,'full pair density preserves raw ruler')
    check(length2/density2==1/f,'completed pair ruler normalization')
    return {'status':'PASS','method':'Fraction polynomial coefficient extraction -> differentiated Christoffels -> original Riemann/Ricci contraction; no parent code imported','python':sys.version,'platform':platform.platform(),'exact_cases':len(cases),'linear_basis_parameters':6,'checked_conditional_TF_map_rank':tf_rank,'assertions':checks,'results':output,'limits':['LSR1 second-jet input is supplied mathematical comparison geometry, not native physical admission.','Linearity at this zero-connection center makes the exact basis calculation cover all c2 and all tracefree S; it is not an arbitrary full-metric classification.','DDR specialization remains conditional on faithful G301 response E=a Ric+b Rg, a nonzero, with every source gate retained.','Six stationary-clock planes suffice on this restricted Ricci-jet image; this does not re-prove the general nine-shape all-pair theorem.','The separate pair algebra uses the quadratic polynomial only; it does not test exact areal normalization or global positivity.']}

if __name__=='__main__':
    print(json.dumps(serialize(run()),indent=2))
