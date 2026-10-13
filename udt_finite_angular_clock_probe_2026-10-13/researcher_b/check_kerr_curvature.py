"""Exact pointwise curvature from original Kerr metric, not Weyl formula."""
import hashlib,itertools,json,time
from pathlib import Path
import sympy as s

started=time.monotonic()
t,r,y,phi,M,a=s.symbols('t r y phi M a',real=True)
coords=[t,r,y,phi]
Sigma=r*r+a*a*y*y
Delta=r*r-2*M*r+a*a
g=s.zeros(4)
g[0,0]=-(1-2*M*r/Sigma)
g[0,3]=g[3,0]=-2*M*a*r*(1-y*y)/Sigma
g[1,1]=Sigma/Delta
g[2,2]=Sigma/(1-y*y)
g[3,3]=(r*r+a*a+2*M*a*a*r*(1-y*y)/Sigma)*(1-y*y)
pairs=list(itertools.combinations(range(4),2))
def simp(x):return s.simplify(x)

cases=[('schwarzschild',s.Integer(0),s.Integer(3),s.Rational(3,5)),
       ('extremal_pure_magnetic',s.Integer(1),s.sqrt(s.Rational(3,2)),1/s.sqrt(2)),
       ('nonextremal_pure_magnetic',s.sqrt(15)/4,s.Rational(3,2),2/s.sqrt(5)),
       ('nonextremal_outside_ergosphere',s.sqrt(15)/4,s.Rational(31,20),2/s.sqrt(5))]
results=[]
for name,av,rv,yv in cases:
    point={M:s.Integer(1),a:av,r:rv,y:yv}
    at=lambda expr:simp(expr.subs(point))
    g0=g.applyfunc(at);gi=g0.inv().applyfunc(simp)
    d=[g.diff(c).applyfunc(at) for c in coords]
    dd=[[g.diff(c1,c2).applyfunc(at) for c2 in coords] for c1 in coords]
    gl=[[[simp((d[b][aa,c]+d[c][aa,b]-d[aa][b,c])/2)
          for c in range(4)] for b in range(4)] for aa in range(4)]
    R6=s.zeros(6)
    for pi,(aa,b) in enumerate(pairs):
        for qi,(c,ddx) in enumerate(pairs):
            linear=(dd[b][c][aa,ddx]+dd[aa][ddx][b,c]-dd[b][ddx][aa,c]-dd[aa][c][b,ddx])/2
            quadratic=sum(gi[e,f]*(gl[e][b][c]*gl[f][aa][ddx]-gl[e][b][ddx]*gl[f][aa][c])
                          for e in range(4) for f in range(4))
            R6[pi,qi]=simp(linear+quadratic)
    sigma=at(Sigma);delta=at(Delta)
    co=s.zeros(4)
    co[0,0]=s.sqrt(delta/sigma)
    co[0,3]=-av*(1-yv*yv)*s.sqrt(delta/sigma)
    co[1,1]=s.sqrt(sigma/delta)
    co[2,2]=s.sqrt(sigma/(1-yv*yv))
    co[3,0]=-av*s.sqrt((1-yv*yv)/sigma)
    co[3,3]=(rv*rv+av*av)*s.sqrt((1-yv*yv)/sigma)
    frame=co.inv().applyfunc(simp)
    eta=s.diag(-1,1,1,1)
    assert (frame.T*g0*frame-eta).applyfunc(simp)==s.zeros(4)
    P=s.zeros(6)
    for ii,(aa,b) in enumerate(pairs):
        for jj,(c,ddx) in enumerate(pairs):
            P[ii,jj]=simp(frame[aa,c]*frame[b,ddx]-frame[aa,ddx]*frame[b,c])
    Rh=(P.T*R6*P).applyfunc(simp)
    def rc(aa,b,c,ddx):
        if aa==b or c==ddx:return s.Integer(0)
        sign=1
        if aa>b:aa,b=b,aa;sign=-sign
        if c>ddx:c,ddx=ddx,c;sign=-sign
        return sign*Rh[pairs.index((aa,b)),pairs.index((c,ddx))]
    Ric=s.Matrix(4,4,lambda b,ddx:simp(sum(eta[aa,aa]*rc(aa,b,aa,ddx) for aa in range(4))))
    assert Ric==s.zeros(4),('RICCI_NONZERO',name,Ric)
    E=s.Matrix(3,3,lambda i,j:rc(0,i+1,0,j+1)).applyfunc(simp)
    cyc=[(2,3),(3,1),(1,2)]
    B=s.Matrix(3,3,lambda i,j:rc(0,i+1,*cyc[j])).applyfunc(simp)
    assert E==E.T and B==B.T and s.trace(E)==0 and s.trace(B)==0
    e=at(M*r*(r*r-3*a*a*y*y)/Sigma**3)
    h=at(-M*a*y*(3*r*r-a*a*y*y)/Sigma**3)
    diagonal=s.diag(-2,1,1)
    assert (E-e*diagonal).applyfunc(simp)==s.zeros(3),('E_MISMATCH',name,E,e)
    assert ((B-h*diagonal).applyfunc(simp)==s.zeros(3) or
            (B+h*diagonal).applyfunc(simp)==s.zeros(3)),('B_MISMATCH',name,B,h)
    E2=simp(s.trace(E*E));B2=simp(s.trace(B*B))
    assert simp(E2-6*e*e)==0 and simp(B2-6*h*h)==0
    kretsch=simp(sum(eta[aa,aa]*eta[b,b]*eta[c,c]*eta[ddx,ddx]*rc(aa,b,c,ddx)**2
                      for aa in range(4) for b in range(4) for c in range(4) for ddx in range(4)))
    assert simp(kretsch-8*(E2-B2))==0
    rplus=1+s.sqrt(1-av*av)
    assert simp(rv-rplus)>0
    if 'pure_magnetic' in name:assert E==s.zeros(3) and B2>0
    if name=='nonextremal_outside_ergosphere':assert g0[0,0]<0 and 4*E2-3*B2<0
    result=dict(name=name,a=str(av),r=str(rv),cos_theta=str(yv),Sigma=str(sigma),Delta=str(delta),
                outer_horizon=str(rplus),gtt=str(g0[0,0]),E=str(E),B=str(B),
                E2=str(E2),B2=str(B2),Kretschmann=str(kretsch),
                proposed_quartic_expression_ONLY_not_clock_theorem=str(simp((4*E2-3*B2)/360)),
                ricci_zero=True,orthonormal_frame=True)
    results.append(result)
    print(json.dumps(result),flush=True)
print(json.dumps(dict(status='PASS_EXACT_ORIGINAL_KERR_CURVATURE_POINTS',
                      cases=len(results),duration_seconds=time.monotonic()-started,
                      sympy=s.__version__,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())),flush=True)
