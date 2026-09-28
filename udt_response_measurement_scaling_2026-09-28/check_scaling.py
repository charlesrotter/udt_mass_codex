#!/usr/bin/env python3
"""Exact scoped RMS1 checks. No source/field equation or physical light model."""
import hashlib
import itertools
import json
from pathlib import Path
import platform
import sys
import sympy as s

t,x,y,z=s.symbols('t x y z',real=True)
coords=(t,x,y,z); point={v:0 for v in coords}
ell=s.symbols('ell',positive=True)
checks=[]; outputs={}
sm=lambda q:s.factor(s.cancel(s.expand(q)))

def eq(name,a,b=0):
    dif=list(s.Matrix(a)-s.Matrix(b)) if isinstance(a,s.MatrixBase) else [a-b]
    vals=[sm(q) for q in dif]
    assert all(q==0 for q in vals),(name,vals)
    checks.append({'name':name,'pass':True,'residual':list(map(str,vals))})

def neq(name,a,b=0):
    dif=list(s.Matrix(a)-s.Matrix(b)) if isinstance(a,s.MatrixBase) else [a-b]
    vals=[sm(q) for q in dif]
    assert any(q!=0 for q in vals),name
    checks.append({'name':name,'pass':True,'nonzero':list(map(str,[q for q in vals if q!=0]))})

def geom_jet(gfield,ufield):
    g=gfield.subs(point); inv=g.inv(); U=ufield.subs(point)
    dg=[gfield.diff(v).subs(point) for v in coords]
    ddg=[[gfield.diff(v,w).subs(point) for w in coords] for v in coords]
    du=[ufield.diff(v).subs(point) for v in coords]
    ddu=[[ufield.diff(v,w).subs(point) for w in coords] for v in coords]
    dinv=[-inv*gg*inv for gg in dg]
    G=[[[sm(sum(inv[a,d]*(dg[b][d,c]+dg[c][d,b]-dg[d][b,c])
             for d in range(4))/2) for c in range(4)] for b in range(4)] for a in range(4)]
    dG=[[[[sm(sum(dinv[e][a,d]*(dg[b][d,c]+dg[c][d,b]-dg[d][b,c])
               +inv[a,d]*(ddg[e][b][d,c]+ddg[e][c][d,b]-ddg[e][d][b,c])
               for d in range(4))/2) for c in range(4)] for b in range(4)]
               for a in range(4)] for e in range(4)]
    Ric=s.Matrix(4,4,lambda a,b:sm(sum(dG[c][c][a][b]-dG[b][c][a][c]
        +sum(G[c][c][d]*G[d][a][b]-G[c][b][d]*G[d][a][c] for d in range(4)) for c in range(4))))
    M=s.Matrix(4,4,lambda a,b:sm(du[b][a]+sum(G[a][b][c]*U[c] for c in range(4))))
    dM=[s.Matrix(4,4,lambda a,b:sm(ddu[e][b][a]+sum(
        dG[e][a][b][c]*U[c]+G[a][b][c]*du[e][c] for c in range(4)))) for e in range(4)]
    theta=s.trace(M); dt=[s.trace(mm) for mm in dM]
    acc=M*U
    dacc=[dM[e]*U+M*du[e] for e in range(4)]
    divacc=sm(sum(dacc[a][a]+sum(G[a][a][c]*acc[c] for c in range(4)) for a in range(4)))
    ul=g*U; h=g+ul*ul.T; P=s.eye(4)+ul*U.T
    B=g*M; spatial=P*B*P.T
    sigma=(spatial+spatial.T)/2-theta*h/3
    twist=(spatial-spatial.T)/2
    norm=lambda B:sm(sum(inv[a,c]*inv[b,d]*B[a,b]*B[c,d]
                          for a,b,c,d in itertools.product(range(4),repeat=4)))
    return {'g':g,'inv':inv,'U':U,'Ric':Ric,'B':B,'theta':theta,
       'dotm':sm(-sum(U[a]*dt[a] for a in range(4))/3),'A':divacc,
       'W':norm(twist),'sigma2':norm(sigma),'acc':acc,
       'ricUU':sm((U.T*Ric*U)[0])}

N=1+2*x+3*x*x+5*y*y
clock=s.Matrix([1,-y,x,0])
gfield=-N**2*clock*clock.T+s.diag(0,s.exp(2*t+t*t),s.exp(4*t-t*t),s.exp(-2*t+2*t*t))
ufield=s.Matrix([1/N,0,0,0])
eq('unit_observer_as_field',(ufield.T*gfield*ufield)[0],-1)
base=geom_jet(gfield,ufield); scaled=geom_jet(ell**2*gfield,ufield/ell)
eq('regular_Lorentz_metric_at_event',base['g'],s.diag(-1,1,1,1))
ns=s.symbols('n1 n2 n3',real=True)

def mean(poly):
    ans=0
    for powers,coeff in s.Poly(s.expand(poly),*ns).terms():
        if any(p%2 for p in powers):continue
        ans+=coeff*s.prod(s.factorial2(p-1) for p in powers)/s.factorial2(sum(powers)+1)
    return sm(ans)

for label,data,scale in [('base',base,s.Integer(1)),('scaled',scaled,ell)]:
    k=data['U']+s.Matrix([0,*ns])/scale
    q=sm(-(k.T*data['B']*k)[0])
    m=mean(q); even=sm((q+q.subs(dict(zip(ns,[-n for n in ns])),simultaneous=True))/2)
    V=mean((even-m)**2)
    data.update(q=q,m=m,V=V)
    eq(label+'_angular_mean',m,-data['theta']/3)
    eq(label+'_even_variance',V,2*data['sigma2']/15)
    target=3*data['dotm']-3*m*m-s.Rational(15,2)*V+data['A']+data['W']
    eq(label+'_DCI1_vs_original_Ricci',target,data['ricUU'])
    outputs[label]={key:str(data[key]) for key in ['Ric','q','m','V','dotm','A','W','ricUU']}
for key,weight in [('q',-1),('m',-1),('V',-2),('dotm',-2),('A',-2),('W',-2),('ricUU',-2)]:
    eq('actual_homothety_'+key,scaled[key],ell**weight*base[key])
eq('covariant_Ricci_weight_zero',scaled['Ric'],base['Ric'])
for key in ['A','W','sigma2','dotm']:
    neq('nonzero_channel_'+key,base[key])
neq('reject_missing_acceleration',base['ricUU']-base['A'],base['ricUU'])
neq('reject_missing_twist',base['ricUU']-base['W'],base['ricUU'])
neq('reject_opposite_Ricci_sign',base['ricUU'],-base['ricUU'])
neq('reject_fixed_observer_normalization',(base['U'].T*scaled['g']*base['U'])[0],-1)

# Original complete shifted pair: both variation conventions, no action.
T,L=s.symbols('T L',positive=True); beta,eps=s.symbols('beta eps',real=True)
h=s.Matrix([[-T*T,-T*T*beta],[-T*T*beta,L*L-T*T*beta*beta]])
m=T*L; C=s.diag(1,1/m); hs=C.T*h*C
eq('complete_pair_calibrated_determinant',hs.det(),-1)
eq('raw_pair_density_homothety',s.sqrt(-(ell**2*h).det()),ell**2*m)
K=s.Matrix([1,0]); U=K/T
v00,v01,v11=s.symbols('v00 v01 v11'); v=s.Matrix([[v00,v01],[v01,v11]])
phi=lambda gg:-s.log(-(K.T*gg*K)[0])/2
eq('kernel_covariant_variation',s.diff(phi(h+eps*v),eps).subs(eps,0),(U.T*v*U)[0]/2)
inverse_var=(h.inv()+eps*v).inv()
eq('kernel_inverse_variation',s.diff(phi(inverse_var),eps).subs(eps,0),-(U.T*h*v*h*U)[0]/2)
eq('kernel_covariant_coefficient_weight_plus_two',
   -(ell**2*h*(U/ell))*(ell**2*h*(U/ell)).T/2,ell**2*(-(h*U)*(h*U).T/2))
eq('co_normalized_clock_T_squared',-((K/ell).T*(ell**2*h)*(K/ell))[0],T*T)

# Ten exact ideal observer readings. Tensor is free test data, not a field law.
eta=s.diag(-1,1,1,1); frame=[s.eye(4)[:,i] for i in range(4)]
units=[frame[0]]
C,S=s.Rational(5,3),s.Rational(4,3)
for i in range(1,4):units.extend([C*frame[0]+S*frame[i],C*frame[0]-S*frame[i]])
for i,j in [(1,2),(1,3),(2,3)]:
    units.append(C*frame[0]+S*(s.Rational(3,5)*frame[i]+s.Rational(4,5)*frame[j]))
slots=[(i,j) for i in range(4) for j in range(i,4)]
row=lambda u:[u[i]*u[j]*(1 if i==j else 2) for i,j in slots]
R=s.Matrix([row(u) for u in units])
for i,u in enumerate(units):eq('unit_tomography_observer_'+str(i),(u.T*eta*u)[0],-1)
eq('timelike_tomography_rank',R.rank(),10)
bvec=s.Matrix([2,-3,5,7,11,-13,17,19,23,-29]); readings=R*bvec
eq('timelike_tensor_reconstruction',R.inv()*readings,bvec)
eq('weight_zero_from_reading_minus_two',(R/ell**2).inv()*(readings/ell**2),bvec)
neq('one_observer_not_complete',s.Matrix([row(units[0])]).rank(),10)

# Independent exact finite certificate of the analytically proved null ambiguity.
directions=[sgn*frame[i] for i in range(1,4) for sgn in [-1,1]]
directions += [s.Rational(3,5)*frame[i]+s.Rational(4,5)*frame[j] for i,j in [(1,2),(1,3),(2,3)]]
RN=s.Matrix([row(frame[0]+n) for n in directions])
eq('null_readout_rank',RN.rank(),9)
metric_vec=s.Matrix([eta[i,j] for i,j in slots])
eq('null_trace_blindness',RN*metric_vec,s.zeros(9,1))
eq('null_one_dimensional_ambiguity',len(RN.nullspace()),1)

# Weight-zero trace-free response need not make full response weight zero.
B=s.Matrix(4,4,lambda i,j:bvec[slots.index((min(i,j),max(i,j)))])
tf=lambda B,g:B-g*s.trace(g.inv()*B)/4
shape=tf(B,eta)
eq('tracefree_projection_under_homothety',tf(B,ell**2*eta),tf(B,eta))
eq('shape_ignores_weight_two_trace',tf(shape+ell**2*eta,ell**2*eta),shape)
neq('reject_full_response_weight_inference',shape+ell**2*eta,shape+eta)

# Chosen G352 supplied-data protocol: absolute rates vs ratios.
wi,wj,Ji,Jj,dtheta,density=s.symbols('wi wj Ji Jj dtheta density',positive=True)
Gi=wi*density/(dtheta*Ji); Gj=wj*density/(dtheta*Jj)
Ghat=(wi/ell)*density/(dtheta*(ell**2*Ji))
eq('absolute_Gamma_weight_minus_three',Ghat,Gi/ell**3)
eq('endpoint_rate_ratio_invariant',(Gj/ell**3)/(Gi/ell**3),Gj/Gi)
eq('area_ratio_invariant',(ell**2*Jj)/(ell**2*Ji),Jj/Ji)
neq('reject_area_ratio_weight_two',(ell**2*Jj)/(ell**2*Ji),ell**2*Jj/Ji)
factor=s.symbols('measure_factor',positive=True)
eq('supplied_measure_rescaling_visible',Ghat.subs(density,factor*density),factor*Gi/ell**3)

# Gamma=e^-v cannot be a fixed quadratic tensor on an open boost interval.
boosts=[s.Integer(i) for i in (1,2,3,4)] # r=e^v>0, exact rational boosts
matrix=s.Matrix([[(r+1/r)**2/4,(r+1/r)*(r-1/r)/2,(r-1/r)**2/4] for r in boosts])
values=s.Matrix([1/r for r in boosts])
eq('quadratic_boost_design_rank',matrix.rank(),3)
eq('linear_readout_augmented_rank',matrix.row_join(values).rank(),4)

result={'status':'PASS','checks':checks,'count':len(checks),'outputs':outputs,
    'versions':{'python':platform.python_version(),'sympy':s.__version__},
    'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'scope':'exact event jets, algebraic reconstruction and protocol controls; analytic arguments own generic statements',
    'not_established':['native E identification','physical record accessibility','light/source law','physical scale symmetry']}
with Path(sys.argv[1]).open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({'status':'PASS','count':len(checks),'metric_channels':outputs,'output':sys.argv[1]}))
