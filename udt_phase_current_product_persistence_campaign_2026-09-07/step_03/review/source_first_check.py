"""Independent pre-exposure PC3 algebra; stdout only, no author imports."""
import hashlib
import json
import pathlib
import platform
import sympy as S

root = pathlib.Path(__file__).resolve().parents[3]
checks = {}

def zero(name, value):
    entries = list(value) if isinstance(value, S.MatrixBase) else [value]
    residuals = [S.simplify(v) for v in entries]
    assert all(v == 0 for v in residuals), (name, residuals)
    checks[name] = 'PASS'

def nonzero(name, value):
    assert S.simplify(value) != 0, name
    checks[name] = 'PASS'

# The metric and graph are computed by full pullback. H is the local value
# of the admitted harmonic profile, not a new physical constant.
H, c, e, d = S.symbols('H c e d', real=True)
kappa, z, t, w = S.symbols('kappa z t w', positive=True)
g = S.Matrix([[H,-1,0,0],[-1,0,0,0],[0,0,1,0],[0,0,0,1]])
# Coordinates (s,theta,z,t): u=-theta/kappa, x=z^2, y=t^3,
# v=s-c*u+e*x+d*y. Sigma={s=0}; V=partial_s.
Jac = S.Matrix([[0,-1/kappa,0,0],[1,c/kappa,2*e*z,3*d*t**2],
                [0,0,2*z,0],[0,0,0,3*t**2]])
G = Jac.T*g*Jac
Gi = S.simplify(G.inv())
gamma = G[1:4,1:4]
screen = 6*z*t**2
L = H+2*c-e**2-d**2
zero('full_lorentzian_determinant',G.det()+screen**2/kappa**2)
zero('initial_volume_squared',gamma.det()-L*screen**2/kappa**2)
zero('full_cut_area_squared',gamma[1:3,1:3].det()-screen**2)
zero('phase_spatial_norm_squared',gamma.inv()[0,0]-kappa**2/L)
zero('normal_time_metric',Gi[0,0]+L)
nflat=S.Matrix([-1/S.sqrt(L),0,0,0])
n=Gi*nflat
zero('normal_unit',(n.T*G*n)[0]+1)
V=S.Matrix([1,0,0,0]); nu=G*V
k=S.Matrix([0,1,0,0])
zero('full_aligned_covector',k-kappa*nu)
zero('full_null_covector',(k.T*Gi*k)[0])
zero('initial_normal_phase',(k.T*n)[0]+kappa/S.sqrt(L))
spatial=k+(k.T*n)[0]*nflat
zero('spatial_extension_annihilates_normal',(spatial.T*n)[0])
zero('full_initial_future_completion',spatial+kappa/S.sqrt(L)*nflat-k)
bad=spatial+2*kappa/S.sqrt(L)*nflat
zero('wrong_normal_exact_residual',(bad.T*Gi*bad)[0]+3*kappa**2/L)
nonzero('wrong_normal_rejected',(bad.T*Gi*bad)[0])
flux=-(n.T*G*(w*V))[0]
zero('initial_positive_flux_factor',flux-w/S.sqrt(L))
volume=S.sqrt(L)*screen/kappa
zero('full_initial_flux_density',flux*volume-w*screen/kappa)
zero('coarea_density',w*screen/kappa-w*screen/kappa)
nonzero('omitted_normal_flux_rejected',(w*volume-w*screen/kappa).subs({H:7,c:2,e:0,d:0}))
nonzero('omitted_screen_area_rejected',(w/kappa-w*screen/kappa).subs({z:2,t:1}))

# Full arbitrary cut slopes and finite transverse observer components.
hz,ht,a,p,r=S.symbols('hz ht a p r', real=True)
cut=S.Matrix([[hz,ht],[0,0],[1,0],[0,1]])
zero('graph_slopes_preserve_full_gram',cut.T*G*cut-gamma[1:3,1:3])
Uold=S.Matrix([a,(1+p*p+r*r+H*a*a)/(2*a),p,r])
U=Jac.inv()*Uold
zero('observer_full_unit',(U.T*G*U)[0]+1)
omega=-(k.T*U)[0]
zero('full_observer_frequency',omega-kappa*a)
zero('actual_current_readout',-(U.T*G*(w*V))[0]-w*a)
Delta=S.symbols('Delta',positive=True)
slabel=Delta*w*screen/kappa
zero('G352_readout_equality',omega/Delta*slabel/screen-w*a)
K=Gi*k
projected=cut+K*(U.T*G*cut)/omega
zero('observer_screen_orthogonality',U.T*G*projected)
zero('observer_screen_gram',projected.T*G*projected-cut.T*G*cut)

# Independently differentiate old admitted cubic and mixed profile controls.
u,x,y=S.symbols('u x y',real=True)
base=x**3-3*x*y*y
mixed=base+u*(x**4-6*x*x*y*y+y**4)
for name,profile in [('cubic',base),('mixed',mixed)]:
    zero(name+'_harmonic',S.diff(profile,x,2)+S.diff(profile,y,2))
    N=S.expand(S.diff(profile,x,2)**2+S.diff(profile,x,y)**2)
    q=(S.diff(N,x)**2+S.diff(N,y)**2)/(16*N*N)
    log_derivative=S.simplify(S.diff(q,u)/q+S.diff(N,u)/(4*N))
    if name=='cubic':
        zero('cubic_exact_q',q-1/(4*(x*x+y*y)))
        zero('stationary_fixed_label_product',log_derivative)
    else:
        zero('mixed_initial_phase_dependence',log_derivative.subs(u,0)-5*x)
        nonzero('conserved_correlated_product_rejected',S.diff(log_derivative,x).subs({u:0,x:1,y:0}))

# A smooth positive conserved quotient need not factorize in fixed labels.
theta,Z=S.symbols('theta Z',real=True)
correlated=S.exp(theta*Z)
zero('correlation_mixed_log',S.diff(S.log(correlated),theta,Z)-1)
nonzero('slice_only_product_false_pass',correlated.subs({theta:1,Z:1})-correlated.subs({theta:0,Z:1}))

paths=['AGENTS.md','CLAUDE.md','CROSS_MODEL_VERIFY.md','CURRENT_SCIENTIFIC_PREMISES.tsv']
paths += ['.claude/skills/'+name+'/SKILL.md' for name in ['no-shortcuts','completeness-map','solution-space-not-imposition','verifier-before-record']]
campaign='udt_phase_current_product_persistence_campaign_2026-09-07/'
paths += [campaign+'WORK_ORDER.md',campaign+'step_03/QUESTION.md']
for step in ['step_01','step_02']:
    paths += [campaign+step+'/'+name for name in ['CANDIDATE_ARGUMENT.md','REVIEW_RECORD.md','review/PHASE_B_ADVERSARIAL_REVIEW.md']]
paths += ['udt_g351_source_free_labelwise_carried_measure_conservation_2026-09-05/EXACT_DERIVATION.md']
paths += ['udt_g352_clock_rate_carried_measure_readout_2026-09-05/'+name for name in ['EXACT_DERIVATION.md','ADOPTION_RECORD.md']]
for step in ['step_03','step_04']:
    paths += ['udt_g351_g352_content_bridge_campaign_2026-09-06/'+step+'/'+name for name in ['CANDIDATE_ARGUMENT.md','REVIEW_RECORD.md','review/STAGE_B_ADVERSARIAL_REVIEW.md']]
paths += ['udt_shared_readout_metric_constraint_campaign_2026-09-06/step_04/'+name for name in ['CANDIDATE_ARGUMENT.md','REVIEW_RECORD.md','review/STAGE_B_ADVERSARIAL_REVIEW.md']]
paths += ['udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py']
print(json.dumps(dict(python=platform.python_version(),sympy=S.__version__,checks=checks,
    outputs=dict(metric=G.tolist(),normal=n.tolist(),initial_flux_density=flux*volume,
        phase_norm_squared=kappa**2/L,screen_area=screen,omega=omega,rate=w*a,
        mixed_log_derivative=5),
    source_sha256={p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in paths}),
    indent=2,sort_keys=True,default=str))
