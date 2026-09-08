"""Exact RT2 density/full-metric diagnostics; reuse sound RT1 author calculus."""
import contextlib
import hashlib
import io
import itertools
import json
from pathlib import Path
import runpy
import sympy as s

pkg=Path(__file__).resolve().parent.parent
captured=io.StringIO()
with contextlib.redirect_stdout(captured):
    ns=runpy.run_path(str(pkg/'step_01/check_reconstruction.py'))
rt1_replay=captured.getvalue().encode()
assert rt1_replay==(pkg/'step_01/author_checks_initial.stdout').read_bytes()
metric_calculus=ns['metric_calculus']; exterior=ns['exterior']; zero=ns['zero']
u,r,x,y=coords=ns['coords']
q=s.Matrix([1,0,0,0]); a=1+u**2; B=2+y
checks={}
def check(name,value):
    checks[name]=bool(value)
    assert value,name
def assert_zero(value,reason):
    assert zero(value),reason
def pp(H):
    return s.Matrix([[H,1,0,0],[1,0,0,0],[0,0,1,0],[0,0,0,1]])

# Separable actual metric, restricted B>0. beta=1 is fixed, not calibrated.
sigma=a*a*B
g=pp(-sigma*x*x)
inv,connection,ric,R,div=metric_calculus(g)
ell=inv*q
check('separable_metric_full_Ricci', R==0 and zero(ric-sigma*q*q.T))
check('separable_reference_conservation', div(sigma*ell)==0)
check('mixed_density_criterion_zero', zero(s.diff(s.diff(s.log(sigma),u),y)))
check('prescribed_B_measure_ratio_phase_only', zero(sigma/B-a*a) and s.diff(sigma/B,y)==0)
qmatch=a*q; nmatch=B; jmatch=nmatch*inv*qmatch
check('matched_exact_phase_full_covector', zero(qmatch-s.Matrix([s.diff(u+u**3/3,z) for z in coords])))
check('matched_full_tensor_and_product', zero(nmatch*qmatch*qmatch.T-ric) and nmatch==B)
check('matched_current_conservation', div(jmatch)==0)
b=a*s.sqrt(B)*q
check('metric_square_root_and_fixed_data_formula', zero(b*b.T-ric) and zero(b/s.sqrt(B)-qmatch)
      and zero(s.sqrt(B)*inv*b-jmatch))
kc=s.Matrix([-1,g[0,0]/2,0,0]); U=(ell+kc)/s.sqrt(2)
check('fixed_query_unit_and_future', zero((U.T*g*U)[0]+1) and (q.T*U)[0]==-1/s.sqrt(2))
Gamma=-(U.T*g*jmatch)[0]
omega_over_delta=-(U.T*qmatch)[0]
check('matched_G352_and_current_readout', zero(Gamma-omega_over_delta*B)
      and zero(Gamma+s.sqrt(B)*(b.T*U)[0]))

# Full ambient closure cannot be replaced by closure on a null cut.
qwrong=b  # supplied measure s_fixed=1 forces this covector, not the matched one
dwrong=exterior(qwrong)
check('wrong_fixed_measure_full_covector_nonclosed', zero(dwrong[3,0]-a/(2*s.sqrt(B))) and not zero(dwrong))
check('same_wrong_covector_cut_restriction_vacuously_closed', all(dwrong[i,j]==0 for i in (1,2,3) for j in (1,2,3)))
for c in (s.Rational(2),s.Rational(3,2)):
    qc=c*qmatch; nc=B/c**2
    check(f'free_measure_constant_family_full_tensor:{c}', zero(nc*qc*qc.T-ric))
    check(f'free_measure_current_not_gauge:{c}', zero(nc*inv*qc-jmatch/c) and not zero(nc*inv*qc-jmatch))

# Nonseparable actual metric: phase-only changes cannot cure fixed-label product.
sigman=1+u*y  # retained |u|<1, |y|<1/2, hence positive
gn=pp(-x*x*sigman)
inn,cn,rn,Rn,dn=metric_calculus(gn)
jn=sigman*inn*q
check('nonseparable_actual_full_Ricci', Rn==0 and zero(rn-sigman*q*q.T))
check('nonseparable_reference_null_and_conserved', zero((q.T*inn*q)[0]) and dn(jn)==0)
mixed=s.simplify(s.diff(s.diff(s.log(sigman),u),y))
check('nonseparable_mixed_obstruction_exact', zero(mixed-1/sigman**2))
check('obstruction_survives_reference_rephase', zero(s.diff(s.diff(s.log(sigman/a**2),u),y)-mixed))

# Explicitly CHANGED cross-phase labels, not admitted passive product gauge.
Y1=x*sigman/a**2; Y2=y
D=s.Matrix([[s.diff(Y1,x),s.diff(Y1,y)],[s.diff(Y2,x),s.diff(Y2,y)]])
detD=s.factor(D.det())
check('changed_label_jacobian_positive_on_declared_patch', zero(detD-sigman/a**2))
qscreen=D.inv().T*D.inv()
Jnew=a*a/sigman  # positive square root of det(qscreen) on retained patch
check('full_transformed_screen_metric_area', zero(qscreen.det()-Jnew**2))
np=sigman/a**2; qp=a*q; jp=np*inn*qp
check('new_product_unit_density', zero(np*Jnew-1))
check('same_full_source_different_current', zero(np*qp*qp.T-rn) and zero(jp-jn/a))
check('new_current_conserved', dn(jp)==0)
forms=[qp,s.Matrix([s.diff(Y1,z) for z in coords]),s.Matrix([s.diff(Y2,z) for z in coords])]
wedge={}
for triple in itertools.combinations(range(4),3):
    coefficient=s.simplify(s.Matrix([[form[i] for i in triple] for form in forms]).det())
    wedge[str(triple)]=str(coefficient)
    target=sigman/a if triple==(0,2,3) else 0
    check('full_three_form:'+str(triple),zero(coefficient-target))
check('changed_labels_not_phase_independent', not zero(s.diff(Y1,u)))
check('new_unit_measure_pullback_is_phase_dependent', not zero(s.diff(detD,u)))

# Passive phase-INDEPENDENT label changes preserve the fixed-data tests.
k=s.Rational(3)
check('passive_density_ratio_invariance', zero((sigma/k)/(B/k)-sigma/B))
check('passive_mixed_obstruction_invariance', zero(s.diff(s.diff(s.log(sigman/k),u),y)-mixed))

mutants={}
cases=[
 ('wrong_a_power_in_full_source',lambda:assert_zero((sigman/a)*qp*qp.T-rn,'full_source_mismatch')),
 ('fixed_measure_ambient_closure_omitted',lambda:assert_zero(dwrong.subs({u:0,y:0}),'nonclosed_full_covector')),
 ('phase_only_cures_nonseparable_product',lambda:assert_zero(mixed.subs({u:s.Rational(1,2),y:s.Rational(1,4)}),'mixed_obstruction_nonzero')),
 ('new_current_called_unchanged',lambda:assert_zero((jp-jn).subs({u:s.Rational(1,2),y:0}),'current_changed')),
 ('phase_dependent_labels_called_passive_gauge',lambda:assert_zero(s.diff(Y1,u).subs({u:0,x:1,y:s.Rational(1,4)}),'label_phase_dependence')),
]
for name,probe in cases:
    try:
        probe()
    except AssertionError as exc:
        mutants[name]=str(exc)
    else:
        raise AssertionError('uncaught defective substitute:'+name)
print(json.dumps({'kind':'exact RT2 diagnostics, not analytic proof',
 'sympy':s.__version__,'coordinates':['u','r','x','y'],
 'rt1_author_regression_reused':'byte-identical; not independent',
 'rt1_replay_sha256':hashlib.sha256(rt1_replay).hexdigest(),
 'groups':len(checks),'checks':checks,'full_three_form_components':wedge,
 'actual_defective_substitutes_caught':mutants,
 'scope':'local positive patches; optional nonvacuum comparison metrics; changed labels disclosed',
 'physical_instrument_or_source_adoption':'NONE'},indent=2,sort_keys=True))
