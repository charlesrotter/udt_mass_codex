"""Full metric/Jacobian/product controls; analytic argument owns persistence."""
import argparse
from itertools import product
import json
import sys
import sympy as s
ap=argparse.ArgumentParser()
ap.add_argument('--mutant',choices=('omit_area','omit_normal_flux','past_phase','ignore_product'))
mode=ap.parse_args().mutant
guards=[]
def zero(x): return s.simplify(x)==0
def check(name,ok):
    if not ok:
        print(json.dumps(dict(status='FAIL',guard=name,mutant=mode,passed=guards)))
        raise SystemExit(1)
    guards.append(name)
# Generic positive metric via its positive screen block and positive Schur gap.
p,r,T=s.symbols('p r T',positive=True); a,m,n=s.symbols('a m n',real=True)
C=s.Matrix([[p*p,p*a],[p*a,a*a+r*r]])
cross=s.Matrix([m,n]); scalar=T*T+(cross.T*C.inv()*cross)[0]
gam=s.Matrix([[scalar,m,n],[m,C[0,0],C[0,1]],[n,C[1,0],C[1,1]]])
check('generic_full_schur_coarea',zero(gam.det()-T*T*p*p*r*r)
      and zero(gam.inv()[0,0]-1/(T*T)))
check('nonorthogonal_phase_labels_retained',gam[0,1]==m and gam[0,2]==n)
# Actual spacetime graph map in the harmonic-chart metric. H remains symbolic:
# these geometric identities do not require its field equation.
u,v,x,y=s.symbols('u v x y',real=True)
H=s.Function('H')(u,x,y); kappa=s.symbols('kappa',positive=True)
c,A,B,Lshear=s.symbols('c A B Lshear',real=True)
h=s.symbols('h',real=True) # independent event H value for exact pullbacks
g=s.Matrix([[h,-1,0,0],[-1,0,0,0],[0,0,1,0],[0,0,0,1]])
L=h+2*c-A*A-B*B
ell=s.Matrix([0,1,0,0])
normal=s.Matrix([1,h+c,A,B])/s.sqrt(L)
basis=s.Matrix([[1,0,0],[-c,A,B],[0,1,0],[0,0,1]])
gamma=s.simplify(basis.T*g*basis)
check('complete_sloped_spacelike_graph',zero(gamma.det()-L)
      and all(zero(a) for a in basis.T*g*normal)
      and zero((normal.T*g*normal)[0]+1))
f=1/s.sqrt(L)
check('positive_initial_flux_factor',zero(-(ell.T*g*normal)[0]-f))
k=s.Matrix([-kappa,0,0,0])
if mode=='past_phase': k=-k
check('full_future_phase_normalization',zero((k.T*g.inv()*k)[0])
      and zero((k.T*normal)[0]+kappa*f)
      and all(zero(a) for a in g.inv()*k-kappa*ell))
# Nonlinear positive label x=z1^2, y=z2+Lshear*z1; phase theta=-kappa*u.
z1=s.symbols('z1',positive=True)
M=s.Matrix([[-1/kappa,0,0],[0,2*z1,0],[0,Lshear,1]])
gamma_phase=s.simplify(M.T*gamma*M)
J2=2*z1
if mode=='omit_area': J2=s.S.One
check('full_phase_label_volume_coarea',
      zero(gamma_phase.det()-L*J2**2/kappa**2))
check('nonlinear_screen_area',zero(gamma_phase[1:,1:].det()-J2*J2))
# Full four-dimensional flow chart: v=s-c*u+A*x+B*y, x=z1^2,
# y=z2+Lshear*z1. V=partial_s. No slope is discarded.
full=s.Matrix([[0,-1/kappa,0,0],
               [1,c/kappa,2*A*z1+B*Lshear,B],
               [0,0,2*z1,0],[0,0,Lshear,1]])
pull=s.simplify(full.T*g*full)
check('full_flow_volume',zero(pull.det()+4*z1*z1/(kappa*kappa)))
w,Delta=s.symbols('w Delta',positive=True)
J3=2*z1*s.sqrt(L)/kappa
flux=w*f*J3
if mode=='omit_normal_flux': flux=w*J3
check('current_flux_matches_quotient',zero(flux-w*J2/kappa))
# A fixed-phase graph cut can have arbitrary V-direction slopes.
tx,ty=s.symbols('tx ty',real=True)
cut=s.Matrix([[0,0],[tx,ty],[2*z1,0],[Lshear,1]])
screen=s.simplify(cut.T*g*cut)
check('arbitrary_cut_graph_area',zero(screen.det()-J2*J2))
au=s.symbols('au',positive=True); px,py=s.symbols('px py',real=True)
U=s.Matrix([au,(1+h*au*au+px*px+py*py)/(2*au),px,py])
check('full_future_unit_observer',zero((U.T*g*U)[0]+1)
      and zero(-(U.T*g*ell)[0]-au))
omega=-(k.T*U)[0]; sigma=Delta*w*J2/kappa
Gamma=omega*sigma/(Delta*J2)
check('original_clock_readout_equals_current',zero(Gamma+(U.T*g*(w*ell))[0]))
# Initial product eligibility is independent of flow conservation. These are
# smooth quotient-density controls, NOT asserted arbitrary curvature recipes.
theta,z2,flow=s.symbols('theta z2 flow',real=True)
good=1+z1*z1+z2*z2; bad=s.exp(theta*z1)
def some_fixed_product(density):
    return True if mode=='ignore_product' else zero(s.diff(density,theta))
check('positive_initial_product',some_fixed_product(good))
check('conserved_nonproduct_rejected',not some_fixed_product(bad)
      and s.diff(bad,flow)==0 and s.diff(bad,theta)!=0)
rebuilt=Delta*bad
check('phase_dependent_measure_is_not_fixed_mu',s.diff(rebuilt,theta)!=0)
scale=s.symbols('scale',positive=True)
check('common_affine_phase_spacing_gauge',zero((scale*omega)/(scale*Delta)-omega/Delta))
print(json.dumps(dict(status='PASS',mutant=mode,guards=guards,guard_count=len(guards),
    gamma_graph=str(gamma),gamma_phase=str(gamma_phase),
    initial_flux=str(flux),J2=str(J2),J3=str(J3),Gamma=str(Gamma),
    nonproduct_derivative=str(s.diff(bad,theta)),python=sys.version,sympy=s.__version__,
    scope='exact full-coordinate/coarea/readout and measure controls, not proof of local flow/PDE or physical identification'),
    indent=2,sort_keys=True))
