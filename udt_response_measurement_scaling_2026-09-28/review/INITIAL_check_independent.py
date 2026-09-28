#!/usr/bin/env python3
"""RMS1 source-first exact checks. No imports from producer or predecessor code.

Geometry: supplied local polynomial Lorentz metric near origin, unit observer
along coordinate t. All arithmetic is exact. Metric jets are differentiated
directly; inverse derivatives follow the inverse identity. This is a witness
and implementation check, not the proof of general homothety or physical access.
"""
import datetime
import hashlib
import json
import platform
from pathlib import Path
import sympy as s

checks = []
rejections = []
def equal(name, lhs, rhs):
    diff = lhs-rhs
    vals = list(diff) if isinstance(diff, s.MatrixBase) else [diff]
    residuals = [s.simplify(z) for z in vals]
    assert all(z == 0 for z in residuals), (name,residuals)
    checks.append(name)

def reject(name, lhs, rhs):
    diff = lhs-rhs
    vals = list(diff) if isinstance(diff,s.MatrixBase) else [diff]
    residuals = [s.simplify(z) for z in vals]
    assert any(z != 0 for z in residuals), name
    rejections.append({'name':name,'nonzero_residuals':[str(z) for z in residuals if z!=0]})

t,x,y,z=s.symbols('t x y z',real=True)
coords=[t,x,y,z]
origin=dict.fromkeys(coords,s.S.Zero)
eta=s.diag(-1,1,1,1)
# Free-and-explored metric jet; g(0)=eta gives a regular Lorentz neighborhood.
base=s.Matrix([
 [-1+t+2*x+x*x+y*z, x+2*y+t*x, -x+z+t*y, y+t*z],
 [x+2*y+t*x, 1+2*t+t*t+x*y, z+t*x, x+t*y],
 [-x+z+t*y, z+t*x, 1+3*t+2*t*t+y*y, x+y+t*z],
 [y+t*z, x+t*y, x+y+t*z, 1-t+3*t*t+z*z]
])

def geometry(scale):
    g=scale**2*base
    gp=g.subs(origin)
    inv=gp.inv()
    dg=[g.diff(c).subs(origin) for c in coords]
    ddg=[[g.diff(a,b).subs(origin) for b in coords] for a in coords]
    dinv=[-inv*di*inv for di in dg]
    C=[[[sum(inv[a,d]*(dg[b][d,c]+dg[c][d,b]-dg[d][b,c]) for d in range(4))/2
          for c in range(4)] for b in range(4)] for a in range(4)]
    dC=[[[[sum(dinv[e][a,d]*(dg[b][d,c]+dg[c][d,b]-dg[d][b,c])
             +inv[a,d]*(ddg[e][b][d,c]+ddg[e][c][d,b]-ddg[e][d][b,c])
             for d in range(4))/2
           for c in range(4)] for b in range(4)] for a in range(4)] for e in range(4)]
    R=[[[[s.simplify(dC[c][a][d][b]-dC[d][a][c][b]
         +sum(C[a][c][e]*C[e][d][b]-C[a][d][e]*C[e][c][b] for e in range(4)))
         for d in range(4)] for c in range(4)] for b in range(4)] for a in range(4)]
    Ric=s.Matrix(4,4,lambda b,d:sum(R[a][b][a][d] for a in range(4)))
    scalar=s.trace(inv*Ric)
    U=s.Matrix([1/s.sqrt(-g[0,0]),0,0,0])
    up=U.subs(origin)
    du=[U.diff(c).subs(origin) for c in coords]
    ddu=[[U.diff(c,d).subs(origin) for d in coords] for c in coords]
    M=s.Matrix(4,4,lambda a,b:du[b][a]+sum(C[a][b][c]*up[c] for c in range(4)))
    dM=[s.Matrix(4,4,lambda a,b:ddu[e][b][a]+sum(
        dC[e][a][b][c]*up[c]+C[a][b][c]*du[e][c] for c in range(4))) for e in range(4)]
    accel=M*up
    daccel=[dM[e]*up+M*du[e] for e in range(4)]
    divaccel=sum(daccel[a][a]+sum(C[a][a][b]*accel[b] for b in range(4)) for a in range(4))
    theta=s.trace(M)
    dtheta=sum(up[e]*s.trace(dM[e]) for e in range(4))
    lower=gp*M # lower[a,b]=nabla_b U_a; reversing slots changes twist sign only.
    spatial=s.Matrix(3,3,lambda a,b:lower[a+1,b+1]/scale**2)
    sym=(spatial+spatial.T)/2
    twist=(spatial-spatial.T)/2
    sigma=sym-s.trace(sym)*s.eye(3)/3
    shear2=s.trace(sigma.T*sigma)
    twist2=s.trace(twist.T*twist)
    m=-theta/3
    mdot=-dtheta/3
    V=s.Rational(2,15)*shear2
    target=(up.T*Ric*up)[0]
    equal('unit observer '+str(scale),(up.T*gp*up)[0],-1)
    equal('Ricci symmetry '+str(scale),Ric,Ric.T)
    equal('direct curvature vs DCI1 '+str(scale),target,3*mdot-3*m*m-s.Rational(15,2)*V+divaccel+twist2)
    equal('trace observer deformation '+str(scale),s.trace(sym),theta)
    return dict(g=gp,inv=inv,C=C,R=R,Ric=Ric,scalar=scalar,U=up,M=M,
                acceleration=accel,m=m,mdot=mdot,V=V,A=divaccel,W=twist2,
                target=target,sigma=sigma,spatial=spatial)

one=geometry(s.Integer(1))
for scale in [s.Integer(2),s.Integer(3)]:
    hat=geometry(scale)
    equal('Ricci weight zero '+str(scale),hat['Ric'],one['Ric'])
    equal('scalar weight -2 '+str(scale),hat['scalar'],one['scalar']/scale**2)
    equal('observer weight -1 '+str(scale),hat['U'],one['U']/scale)
    equal('deformation weight -1 '+str(scale),hat['M'],one['M']/scale)
    equal('acceleration coordinate vector weight -2 '+str(scale),hat['acceleration'],one['acceleration']/scale**2)
    equal('mean weight -1 '+str(scale),hat['m'],one['m']/scale)
    for k in ['mdot','V','A','W','target']:
        equal(k+' weight -2 '+str(scale),hat[k],one[k]/scale**2)
    flatC=lambda v:s.Matrix([v[a][b][c] for a in range(4) for b in range(4) for c in range(4)])
    equal('connection unchanged '+str(scale),flatC(hat['C']),flatC(one['C']))
    flatR=lambda v:s.Matrix([v[a][b][c][d] for a in range(4) for b in range(4) for c in range(4) for d in range(4)])
    equal('mixed curvature unchanged '+str(scale),flatR(hat['R']),flatR(one['R']))
    reject('wrong scalar weight zero '+str(scale),hat['target'],one['target'])
    reject('wrong covariant Ricci weight -2 '+str(scale),hat['Ric'],one['Ric']/scale**2)

for key in ['mdot','V','A','W']:
    reject('active channel '+key,one[key],0)
reject('omit motion channels',one['target'],3*one['mdot']-3*one['m']**2-s.Rational(15,2)*one['V'])
reject('half vorticity norm',one['target'],3*one['mdot']-3*one['m']**2-s.Rational(15,2)*one['V']+one['A']+one['W']/2)

# Exact ten-query polarization from rational future-unit timelike vectors.
# Three signed axis boosts give 1+6 records. Three two-axis boosts add 3.
C,S=s.Rational(5,3),s.Rational(4,3)
vectors=[s.Matrix([1,0,0,0])]
for i in range(1,4):
    for sign in [-1,1]:
        v=s.Matrix([C,0,0,0]);v[i]=sign*S;vectors.append(v)
for i,j in [(1,2),(1,3),(2,3)]:
    v=s.Matrix([3,0,0,0]);v[i]=2;v[j]=2;vectors.append(v)
slots=[(a,b) for a in range(4) for b in range(a,4)]
design=s.Matrix([[v[a]*v[b]*(1 if a==b else 2) for a,b in slots] for v in vectors])
for j,v in enumerate(vectors):equal('timelike query '+str(j),(v.T*eta*v)[0],-1)
equal('ten-query rank',design.rank(),10)
unknown=s.Matrix(4,4,lambda a,b: s.Rational((min(a,b)+2)*11+(max(a,b)+1)*7,13))
record=s.Matrix([(v.T*unknown*v)[0] for v in vectors])
recovered=design.inv()*record
equal('quadratic-form reconstruction',recovered,s.Matrix([unknown[a,b] for a,b in slots]))
equal('actual Ricci reconstruction',design.inv()*s.Matrix([(v.T*one['Ric']*v)[0] for v in vectors]),s.Matrix([one['Ric'][a,b] for a,b in slots]))
for scale in [s.Integer(2),s.Integer(3)]:
    hat_design=design/scale**2
    equal('scaled tensor reconstruction '+str(scale),hat_design.inv()*(record/scale**2),recovered)
    reject('raw unit records held fixed '+str(scale),hat_design.inv()*record,recovered)
wrong=s.Matrix([[v[a]*v[b] for a,b in slots] for v in vectors])
reject('omit polarization cross factor',wrong.inv()*record,recovered)

# Raw G176 pullback and chosen G352 readout transformations, symbolic positive.
c,N,L,b,Delta,mu,J1,J2,w1,w2=s.symbols('c N L b Delta mu J1 J2 w1 w2',positive=True)
h=s.Matrix([[-N*N,-N*N*b],[-N*N*b,L*L-N*N*b*b]])
equal('pair determinant',h.det(),-N*N*L*L)
equal('raw pair homothety',h.subs({N:c*N,L:c*L},simultaneous=True),c*c*h)
m=N*L
equal('tape density weight +2',(c*N)*(c*L),c*c*m)
reject('tape mistaken for metric arclength',(c*N)*(c*L),c*m)
equal('recalibrated ruler weight -1',(c*L)/((c*N)*(c*L)),(L/m)/c)
Gamma1=w1*mu/(Delta*J1)
Gamma2=w2*mu/(Delta*J2)
hat1=Gamma1.subs({w1:w1/c,J1:c*c*J1},simultaneous=True)
hat2=Gamma2.subs({w2:w2/c,J2:c*c*J2},simultaneous=True)
equal('chosen readout weight -3',hat1,Gamma1/c**3)
equal('transfer ratio invariant',hat2/hat1,Gamma2/Gamma1)
equal('area ratio invariant',(c*c*J2)/(c*c*J1),J2/J1)
reject('area ratio mistaken for absolute area',(c*c*J2)/(c*c*J1),c*c*J2/J1)

report={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'python':platform.python_version(),'sympy':s.__version__,'arithmetic':'exact symbolic/rational; no tolerance',
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'checks':checks,'rejection_controls':rejections,
 'metric':str(base),'event':[0,0,0,0],'Ricci':str(one['Ric']),
 'DCI1_channels':{k:str(one[k]) for k in ['m','mdot','V','A','W','target']},
 'query_vectors':[list(map(str,v)) for v in vectors],'design_determinant':str(design.det()),
 'scope':'supplied local metric jet and exact algebra; not physical E identification or instrument access'}
print(json.dumps(report,indent=2))
