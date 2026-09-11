#!/usr/bin/env python3
"""TI3 source-exposed reviewer check, independently written from metric derivatives.

Solve original spatial Ricci=0 and its X/T derivatives for normal metric jets.
Compute all-lower Riemann and its T derivative, all Ricci entries, Weyl,
Lorentzian first-pair Hodge and differentiated complete contraction.
No author scientific implementation or compact rate formula is imported.
"""
import itertools as it
import ast
import json
import platform
from pathlib import Path
import sys
import sympy as S

I = range(4)
PAIRS = [(a,b) for a in range(1,4) for b in range(a,4)]
IDX4 = list(it.product(I,repeat=4))
ZERO = S.Integer(0)
ETA = [-1,1,1,1]
checks = []

def require(name, values):
    values = list(values)
    residuals = [S.factor(v) for v in values]
    bad = [(i,str(v)) for i,v in enumerate(residuals) if v != 0]
    checks.append({'name':name,'components':len(values),'failures':bad})
    if bad:
        raise AssertionError((name,bad[:5]))

class Jets:
    def __init__(self):
        self.data = {}
        for a in I:
            self.put(a,a,(),S.Integer(ETA[a]))
    def put(self,a,b,ds,value):
        self.data[(min(a,b),max(a,b),tuple(sorted(ds)))] = S.sympify(value)
    def g(self,a,b,*ds):
        return self.data.get((min(a,b),max(a,b),tuple(sorted(ds))),ZERO)

def geometry(j,der=None):
    g=j.g
    inv=S.diag(*ETA)
    A={(a,b,c):(g(a,b,c)+g(a,c,b)-g(b,c,a))/2
       for a,b,c in it.product(I,repeat=3)}
    if der is not None:
        invd=-inv*S.Matrix(4,4,lambda a,b:g(a,b,der))*inv
        Ad={(a,b,c):(g(a,b,c,der)+g(a,c,b,der)-g(b,c,a,der))/2
            for a,b,c in it.product(I,repeat=3)}
    R={}
    Rd={}
    for a,b,c,d in IDX4:
        val=(g(a,d,b,c)+g(b,c,a,d)-g(a,c,b,d)-g(b,d,a,c))/2
        for e in I:
            val+=ETA[e]*(A[e,b,c]*A[e,a,d]-A[e,b,d]*A[e,a,c])
        R[a,b,c,d]=S.expand(val)
        if der is not None:
            vd=(g(a,d,b,c,der)+g(b,c,a,d,der)-g(a,c,b,d,der)-g(b,d,a,c,der))/2
            for e in I:
                vd+=ETA[e]*(Ad[e,b,c]*A[e,a,d]+A[e,b,c]*Ad[e,a,d]
                            -Ad[e,b,d]*A[e,a,c]-A[e,b,d]*Ad[e,a,c])
                for f in I:
                    vd+=invd[e,f]*(A[e,b,c]*A[f,a,d]-A[e,b,d]*A[f,a,c])
            Rd[a,b,c,d]=S.expand(vd)
    Ric=S.Matrix(4,4,lambda b,d:sum(ETA[a]*R[a,b,a,d] for a in I))
    if der is None:
        return R,Ric
    Ricd=S.Matrix(4,4,lambda b,d:sum(ETA[a]*Rd[a,b,a,d] for a in I)
                   +sum(invd[a,c]*R[a,b,c,d] for a in I for c in I))
    return R,Ric,Rd,Ricd

def solve_normal(j,derivatives,name):
    unknowns=S.symbols('u0:6')
    for (a,b),u in zip(PAIRS,unknowns):
        j.put(a,b,derivatives,u)
    if len(derivatives)==2:
        _,ric=geometry(j)
    else:
        _,_,_,ric=geometry(j,derivatives[-1])
    eqs=[ric[a,b] for a,b in PAIRS]
    mat,rhs=S.linear_eq_to_matrix(eqs,unknowns)
    require(name+'_normal_coefficient', [mat.det()-S.Rational(1,64)])
    solved=mat.inv()*rhs
    for (a,b),v in zip(PAIRS,solved):
        j.put(a,b,derivatives,S.factor(v))

def star(C):
    return {(a,b,c,d):S.expand(sum(S.LeviCivita(a,b,e,f)*ETA[e]*ETA[f]*C[e,f,c,d]/2
                  for e in I for f in I)) for a,b,c,d in IDX4}

def star_derivative(j,C,Ct):
    inv=S.diag(*ETA)
    invt=-inv*S.Matrix(4,4,lambda a,b:j.g(a,b,0))*inv
    volume_rate=sum(ETA[a]*j.g(a,a,0) for a in I)/2
    out={}
    for a,b,c,d in IDX4:
        v=ZERO
        for e in I:
            for f in I:
                ep=S.LeviCivita(a,b,e,f)
                if ep==0:
                    continue
                v+=ep*ETA[e]*ETA[f]*(Ct[e,f,c,d]+volume_rate*C[e,f,c,d])/2
                for h in I:
                    v+=ep*(invt[e,h]*ETA[f]*C[h,f,c,d]+ETA[e]*invt[f,h]*C[e,h,c,d])/2
        out[a,b,c,d]=S.expand(v)
    return out

def contraction_and_rate(j,C,Ct):
    D=star(C)
    Dt=star_derivative(j,C,Ct)
    inv=S.diag(*ETA)
    invt=-inv*S.Matrix(4,4,lambda a,b:j.g(a,b,0))*inv
    p=ZERO
    pt=ZERO
    contraction_term=ZERO
    for inds in IDX4:
        sig=S.prod(ETA[a] for a in inds)
        p+=sig*C[inds]*D[inds]
        pt+=sig*(Ct[inds]*D[inds]+C[inds]*Dt[inds])
        for slot,a in enumerate(inds):
            other_sig=S.prod(ETA[inds[k]] for k in range(4) if k!=slot)
            for b in I:
                replace=list(inds)
                replace[slot]=b
                contraction_term+=other_sig*invt[a,b]*C[inds]*D[tuple(replace)]
    return S.factor(p),S.factor(pt+contraction_term),S.factor(contraction_term)

def anchor(lam):
    x=S.symbols('x',real=True)
    a=b=S.Rational(1,100)
    s=-S.Rational(2,3)
    p=a*(1+lam*(1-S.cos(x)))
    r=b*S.sin(x)
    kap=(p*p+r*r-s*s)/(2*s)
    K=S.Matrix([[kap,0,0],[0,s-p,-r],[0,-r,s+p]])
    Ks=[K.diff(x,k).subs(x,0) for k in range(3)]
    j=Jets()
    for ai in range(3):
        for bi in range(ai,3):
            for k in range(3):
                j.put(ai+1,bi+1,(0,)+(1,)*k,-2*Ks[k][ai,bi])
    # Sequentially solve the complete original spatial equations and their derivatives.
    solve_normal(j,(0,0),f'lambda{lam}_Ricij')
    solve_normal(j,(0,0,1),f'lambda{lam}_Ricij_X')
    solve_normal(j,(0,0,0),f'lambda{lam}_Ricij_T')
    R,Ric,Rt,Rict=geometry(j,0)
    _,_,_,Ricx=geometry(j,1)
    require(f'lambda{lam}_all_Ricci',Ric)
    require(f'lambda{lam}_all_Ricci_T',Rict)
    require(f'lambda{lam}_all_Ricci_X',Ricx)
    require(f'lambda{lam}_Riemann_symmetries',
            (v for aa,bb,cc,dd in IDX4 for v in
             (R[aa,bb,cc,dd]+R[bb,aa,cc,dd],R[aa,bb,cc,dd]+R[aa,bb,dd,cc],
              R[aa,bb,cc,dd]-R[cc,dd,aa,bb],
              R[aa,bb,cc,dd]+R[aa,cc,dd,bb]+R[aa,dd,bb,cc])))
    # Full Ricci and its derivative vanish, hence Weyl=Riemann to this order.
    twice=star(star(R))
    require(f'lambda{lam}_Lorentzian_star_squared', (twice[q]+R[q] for q in IDX4))
    P,Pt,term=contraction_and_rate(j,R,Rt)
    expectedP=-S.Rational(39991,37500000)
    expectedPt=S.Rational(3519567919,900000000000)-S.Rational(32,10000)*lam
    require(f'lambda{lam}_candidate_correspondence',[P-expectedP,Pt-expectedPt])
    # Unlike P_t, the point records through second total order must coincide.
    dirs=[S.Matrix(v) for v in [(1,0,0),(0,1,0),(0,0,1),(1,1,0),(1,0,1),(0,1,1)]]
    records={}
    for vi,v in enumerate(dirs):
        for order in range(4):
            for ds in it.combinations_with_replacement(I,order):
                records[str((vi,ds))]=sum(v[ai]*v[bi]*j.g(ai+1,bi+1,*ds)
                                          for ai in range(3) for bi in range(3))
    return {'lambda':lam,'P':P,'U_P':Pt,'inverse_contraction_term':term,
            'metric_jets':j.data,'records':records,'Riemann':R,'Riemann_T':Rt,
            'Ricci':list(Ric),'Ricci_T':list(Rict),'Ricci_X':list(Ricx)}

def encode(v):
    if isinstance(v,dict):
        return {str(k):encode(w) for k,w in v.items()}
    if isinstance(v,list):
        return [encode(w) for w in v]
    if isinstance(v,(int,float,str,bool)) or v is None:
        return v
    return str(v)

out=[anchor(0),anchor(2)]
for kind in ['metric_jets','records']:
    if kind=='metric_jets':
        keys=[(a,b,ds) for a in I for b in range(a,4) for order in range(3)
              for ds in it.combinations_with_replacement(I,order)]
    else:
        keys=[k for k in out[0][kind] if len(ast.literal_eval(k)[1])<=2]
    require(kind+'_complete_second_order_equality',
            [out[0][kind].get(k,ZERO)-out[1][kind].get(k,ZERO) for k in keys])
require('rate_difference', [out[1]['U_P']-out[0]['U_P']+S.Rational(64,10000)])
third_difference=out[1]['metric_jets'][(2,2,(0,1,1))]-out[0]['metric_jets'][(2,2,(0,1,1))]
require('third_jet_difference',[third_difference-S.Rational(1,25)])
result={'verdict':'PASS','implementation':'independent direct lower-Riemann metric-jet equation solve',
        'python':platform.python_version(),'sympy':S.__version__,
        'source_exposed':True,'author_science_imports':[],
        'check_groups':len(checks),'components':sum(c['components'] for c in checks),
        'checks':checks,'anchors':out,'third_jet_yy_TXX_difference':third_difference}
path=Path(sys.argv[1])
with path.open('x') as f:
    json.dump(encode(result),f,indent=2)
    f.write('\n')
print(json.dumps({k:encode(v) for k,v in result.items() if k!='anchors'},indent=2))
for a in out:
    print('lambda',a['lambda'],'P',a['P'],'U(P)',a['U_P'],'inverse contraction',a['inverse_contraction_term'])
