"""Finite formula/representation checks, not a fitted astronomical metric."""
from pathlib import Path
import csv, hashlib, json, platform
import sympy as s
import mpmath as m
B=Path('udt_first_astronomical_comparison_2026-10-04')
T=Path('udt_observation_metric_evaluation_2026-10-04/observation/MCP_TABLE1_INPUT.tsv')
assert hashlib.sha256(T.read_bytes()).hexdigest()=='114e4412eed79d088dff9cbfc68890d49dd6a902811b7f0370c085b980554910'
t,c,z0=s.symbols('t c z0',positive=True);a,b=s.symbols('a b',positive=True)
# Numeric-method control: inverse actual arrival for Z(s)=z0*exp(a*s),
# alpha(s)=exp(b*s). Neither is an astronomical geometry or source model.
src=s.log(1+a*t/z0)/a
v=c*(z0*s.exp((a-b)*src)-1)
direct=s.diff(v,t)
chain=c*(a-b)*s.exp(-b*src)
assert s.simplify(direct-chain)==0
assert s.simplify(direct.subs(b,0)-c*a)==0
# A varying common factor contributes, rather than silently cancelling.
w=s.symbols('w');Q=s.Function('Q')(w);Z0=s.Function('Z0')(w)
assert s.simplify(s.diff(Z0*Q,w)/(Z0*Q)-s.diff(Z0,w)/Z0-s.diff(Q,w)/Q)==0
D=s.Rational(5);J1=D*s.eye(2);J2=D*s.diag(2,s.Rational(1,2))
assert J1.det()==J2.det()==D**2
assert J1.T*J1==D**2*s.eye(2) and J2.T*J2!=D**2*s.eye(2)
assert J1*s.Matrix([1,1])!=J2*s.Matrix([1,1])
# Affine scaling and physical receiver replacement are different operations.
omega=s.Rational(2);K=s.Matrix([[3,1],[0,4]]);J=omega*K
for f in [s.Rational(1,3),s.Rational(2),s.Rational(7,2)]:
 assert f*omega*(K/f)==J
 assert (f*J).det()==f**2*J.det()
# Optical drift implementation assessed against direct inverse arrival at 60digits.
m.mp.dps=60;errors=[];wrong_errors=[]
for Z in ['1','1.02392388403580186','2']:
 for A,B,tobs in [('0.01','0','0.3'),('0.02','0.003','2'),('0.02','0.007','10')]:
  zz,aa,bb,tt=map(m.mpf,(Z,A,B,tobs));cc=m.mpf('299792.458')
  inv=lambda x:m.log1p(aa*x/zz)/aa
  vv=lambda x:cc*(zz*m.exp((aa-bb)*inv(x))-1)
  got=m.diff(vv,tt);expected=cc*(aa-bb)*m.exp(-bb*inv(tt))
  errors.append(abs(got-expected));wrong_errors.append(abs(got-expected/zz))
assert max(errors)<m.mpf('1e-50') and max(wrong_errors)>1
# Stable source frame convention, no likelihood or simultaneous region.
row=next(r for r in csv.DictReader(T.open(),delimiter='\t') if r['galaxy']=='CGCG 074-064')
cc=m.mpf('299792.458');vv=m.mpf(row['v_opt_CMB_km_s']);dv=m.mpf(row['v_reported_plus_km_s'])
Z=1+vv/cc;lo=1+(vv-dv)/cc;hi=1+(vv+dv)/cc
d=m.mpf(row['D_Mpc']);dl=d-m.mpf(row['D_minus_Mpc']);dh=d+m.mpf(row['D_plus_Mpc'])
obs={'name':row['galaxy'],'Z_median':str(Z),'Z_marginal':[str(lo),str(hi)],'Phi_clock_median':str(-m.log(Z)),'Phi_clock_marginal':[str(-m.log(hi)),str(-m.log(lo))],'chi_clock_median':str(m.tanh(-m.log(Z))),'chi_clock_marginal':[str(m.tanh(-m.log(hi))),str(m.tanh(-m.log(lo)))],'D_Mpc':[str(dl),str(d),str(dh)],'area_Mpc2':[str(dl**2),str(d**2),str(dh**2)],'retained_scope':'Source-compatible scalar-map readout only; processed systemic frame; separate marginal intervals, no joint statistical test, no native phi_pair assignment'}
# Three synthetic likelihood rows. Arbitrary dimensionless test controls only.
# The independently checked implication is: changing unmeasured accelerations
# must leave likelihood unchanged, while a measured slope changes it.
def likelihood(pred,flags=(1,0,1)):
 values=[s.Rational(1),s.Rational(2),s.Rational(3)]
 return -sum((values[i]-pred[i])**2/s.Integer(2) for i in range(3) if flags[i])
p=[s.Integer(0)]*3;base=likelihood(p);p[1]=s.Integer(999)
assert likelihood(p)==base
wrong=likelihood(p,(1,1,1));assert wrong!=base
p[0]=s.Integer(1);assert likelihood(p)!=base
result={'status':'PASS_FINITE_CONSTRUCTION_CHECKS','scope':'Exact symbolic formulas and nine highprecision accounting controls; observed summary conversion; no metric candidate, fit, empirical validation or full data likelihood replay','versions':{'python':platform.python_version(),'sympy':s.__version__,'mpmath':m.__version__},'symbolic_inverse_arrival_identity':True,'variable_factor_identity':True,'same_area_different_sky_map':True,'affine_and_receiver_scaling_cases':3,'finite_drift_cases':9,'drift_max_abs_error':str(max(errors)),'extra_redshift_division_fault_max_abs_error':str(max(wrong_errors)),'unmeasured_acceleration_fault_rejected':True,'wrong_scalar_map_fault_rejected':True,'CGCG_summary':obs}
print(json.dumps(result,indent=2))
(B/'CONSTRUCTION_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
