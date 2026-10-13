"""B3 exact anchors. Coordinate curvature adapts PCC1 check_curvature.py."""
import itertools
import json
import platform
import sympy as s

t,r,theta,phi=s.symbols('t r theta phi',real=True)
lam=s.symbols('lambda',positive=True)
mu=s.symbols('mu',real=True)
f=s.Function('f')(r)
coords=(t,r,theta,phi); inds=range(4); eta=(-1,1,1,1)
g=(-f,1/f,r*r,r*r*s.sin(theta)**2)
def simp(z):return s.factor(s.trigsimp(s.expand_trig(s.cancel(z))))
Gamma={}
for a,b,c in itertools.product(inds,repeat=3):
    z=((s.diff(g[a],coords[b]) if a==c else 0)
       +(s.diff(g[a],coords[c]) if a==b else 0)
       -(s.diff(g[b],coords[a]) if b==c else 0))/(2*g[a])
    z=simp(z)
    if z!=0:Gamma[a,b,c]=z
G=lambda a,b,c:Gamma.get((a,b,c),s.S.Zero)
orth={}; coordinates={}
e2=(1/f,f,1/r**2,1/(r*r*s.sin(theta)**2))
for i,j,b,a in itertools.product(inds,repeat=4):
    z=s.diff(G(a,j,b),coords[i])-s.diff(G(a,i,b),coords[j])
    z+=sum(G(a,i,c)*G(c,j,b)-G(a,j,c)*G(c,i,b) for c in inds)
    z=simp(g[a]*z)
    if z!=0:
        idx=(i,j,b,a); coordinates[idx]=z
        counts=[idx.count(q) for q in inds]
        assert all(c%2==0 for c in counts)
        orth[idx]=simp(z*s.prod(e2[q]**(counts[q]//2) for q in inds))
H=lambda idx:orth.get(tuple(idx),s.S.Zero)
six_idx=[(1,0,0,1),(2,0,0,2),(3,0,0,3),(1,2,2,1),(1,3,3,1),(2,3,3,2)]
six_expected=[s.diff(f,r,2)/2,s.diff(f,r)/(2*r),s.diff(f,r)/(2*r),
              -s.diff(f,r)/(2*r),-s.diff(f,r)/(2*r),(1-f)/r**2]
assert all(simp(H(idx)-z)==0 for idx,z in zip(six_idx,six_expected))
f0=1-2*mu/r; fq=f0-lam*r**4
delta={idx:simp(z.subs(f,fq).doit()-z.subs(f,f0).doit()) for idx,z in orth.items()}
def con(tensor,X,Y,Z,W):
    return s.expand(sum(z*X[i]*Y[j]*Z[k]*W[l] for (i,j,k,l),z in tensor.items()))
U=s.Matrix(s.symbols('u0:4')); n=s.Matrix(s.symbols('n0:4'))
b=U[0]*n[1:4,0]-n[0]*U[1:4,0]
m=U[1:4,0].cross(n[1:4,0])
alpha,beta,gamma=6*lam*r*r,2*lam*r*r,lam*r*r
raw=-con(delta,n,U,U,n)
assert s.expand(raw-beta*(b.dot(b)-m.dot(m))-(alpha-beta)*b[0]**2-(beta-gamma)*m[0]**2)==0
dot=lambda x,y:sum(eta[i]*x[i]*y[i] for i in inds)
assert s.expand(b.dot(b)-m.dot(m)+dot(U,U)*dot(n,n)-dot(U,n)**2)==0
assert s.expand(b.dot(m))==0
e=[s.eye(4)[:,i] for i in inds]
radial=[con(delta,e[i],e[0]+e[1],e[0]+e[1],e[i]) for i in (2,3)]
tangential=[con(delta,e[i],e[0]+e[2],e[0]+e[2],e[i]) for i in (1,3)]
assert radial==[0,0]
assert tangential==[-4*lam*r*r,-lam*r*r]
q=s.Function('q')(r); df=-r*r*q
aa,bb,cc=-s.diff(df,r,2)/2,-s.diff(df,r)/(2*r),-df/r**2
assert simp(bb-cc-r*s.diff(q,r)/2)==0
assert simp(aa-bb-s.diff(r**3*s.diff(q,r),r)/(2*r))==0

# Static-frame parallel preparation and exact frequency factors.
assert simp(s.diff(f**(-s.Rational(1,2)),r)+G(0,1,0)*f**(-s.Rational(1,2)))==0
E,v,ray_energy=s.symbols('E v ray_energy',positive=True)
ff=E*E-v*v
ut=E/ff; ur=v
kt=ray_energy/ff
omega_out=ff*kt*ut-ray_energy*ur/ff
omega_in=ff*kt*ut+ray_energy*ur/ff
assert s.factor(ray_energy/omega_out-(E+v))==0
assert s.factor(omega_in/ray_energy-1/(E-v))==0
assert s.factor((E/ (ff*v)-1/ff)-1/(v*(E+v)))==0
assert s.factor((E+v)/(E-v)-((E+v)/s.sqrt(ff))**2)==0
Ev=s.sqrt(255)/16
assert Ev>s.Rational(1,2)
gap=s.Rational(1,3)-s.Rational(64,255)
assert gap==s.Rational(7,85)>0
threshold_bound=-1+1/(2*Ev*(1+Ev))
assert threshold_bound<0

# Rescaled first-order receiver/ray incidence, solved before clock expansion.
eps,S=s.symbols('epsilon S')
c=s.symbols('c')
Sarr=1+c*eps
RB=1+eps*Sarr**2
TB=Sarr*(1+eps/2)
Tnull=RB+eps*RB**5/5
incidence=s.series(TB-Tnull,eps,0,2).removeO().expand()
cval=s.solve(incidence.coeff(eps),c)[0]
assert cval==s.Rational(7,10)
Eseries=1-eps/2
varr=2*eps*Sarr.subs(c,cval)
logp=s.series(s.log(Eseries+varr),eps,0,2).removeO()
logq=s.series(-s.log(Eseries-varr),eps,0,2).removeO()
assert logp==s.Rational(3,2)*eps
assert logq==s.Rational(5,2)*eps

print(json.dumps({
 'kind':'exact symbolic coordinate/geodesic anchors, not physical adoption',
 'python':platform.python_version(),'sympy':s.__version__,
 'generic_spherical_curvature':{str(idx):str(H(idx)) for idx in six_idx},
 'quartic_difference_six':{str(idx):str(delta[idx]) for idx in six_idx},
 'all_plane_bivector_identity':True,'normalization_and_simplicity':True,
 'radial_screen':list(map(str,radial)), 'tangential_screen':list(map(str,tangential)),
 'profile_identities':True,'parallel_preparation':True,
 'first_tick_ratio':'E+v','return_tick_ratio':'1/(E-v)',
 'interception_horizon_gap_lower_bound_in_rh_units':str(gap),
 'p_equals_one_threshold_F_upper_bound_in_r0_units':str(threshold_bound),
 'rescaled_proper_arrival_coefficient':str(cval),
 'log_p_first_epsilon_coefficient':str(logp/eps),
 'log_q_first_epsilon_coefficient':str(logq/eps),
 'all_assertions_passed':True,
 'limits':'Exact identities/bound constants. Analytic inequalities, regularity and physical interpretation are in CANDIDATE.md; no empirical or global stability claim.'
},indent=2))
