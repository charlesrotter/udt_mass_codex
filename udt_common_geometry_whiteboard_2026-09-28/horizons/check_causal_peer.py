import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[name]='2'
import resource
resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
import sympy as s
import json,platform
from pathlib import Path

checks={}
def z(name,expr):
    r=s.simplify(expr)
    checks[name]={'residual':str(r),'pass':r==0}

a=s.symbols('a',positive=True)
b,lam=s.symbols('b lam',real=True)
u=a+b*lam
raw=lam/(a*(a+b*lam))
normalized=a*raw
z('raw_conformal_affine',s.diff(raw,lam)-u**-2)
z('observer_frequency_normalized_affine',s.diff(normalized,lam)-a/u**2)
z('normalized_initial_affine_derivative',s.diff(normalized,lam).subs(lam,0)-1/a)

t,r,k,L=s.symbols('t r k L',real=True)
U=1+k*(-t*t+r*r)/2
uo=U.subs(r,0)
ue=U.subs({t:t-L,r:L})
redshift=ue/uo
beam=L/ue
z('one_cone_u',ue.subs(t,0)-1)
z('proper_drift', (uo*s.diff(redshift,t)).subs(t,0)-k*L)
z('screen_drift',(uo*s.diff(beam,t)).subs(t,0)+k*L**2)
z('all_epoch_product',redshift*beam-L/uo)

# Independent conformal-Ricci formula in n=4, derived from the connection difference:
# Ric_hat_ij = 2 u^-1 Hess_ij(u) + [u^-1 Box(u)-3u^-2|du|^2] eta_ij.
# Here Hess=k eta, Box=4k, |du|^2=k^2(-t^2+r^2).
ricci_coefficient=6*k/U-3*k*k*(-t*t+r*r)/U**2
z('quadratic_conformal_Ricci',ricci_coefficient-6*k/U**2)
z('quadratic_scalar',4*U**2*ricci_coefficient-24*k)

# Actual distinct future legs, central emission at coordinate T, source reflection T+L,
# central reception T+2L. Incidence derivatives all equal 1; proper intervals divide by u.
u_start=U.subs(r,0)
u_mid=U.subs({t:t+L,r:L})
u_end=U.subs({t:t+2*L,r:0})
forward=u_start/u_mid
backward=u_mid/u_end
z('future_echo_chain',forward*backward-u_start/u_end)
z('zero_epoch_forward',forward.subs(t,0)-1)
z('zero_epoch_later_return',backward.subs(t,0)-1/(1-2*k*L**2))

out={'kind':'PEER_INDEPENDENT_SMALL_SYMBOLIC_REDERIVATION_NOT_FRESH_REVIEW','python':platform.python_version(),'sympy':s.__version__,'checks':checks,'count':len(checks),'status':'PASS' if all(v['pass'] for v in checks.values()) else 'FAIL','future_return_result':str(s.factor(backward.subs(t,0))),'scope':'positive finite segments; no source tensor utility imported'}
p=Path(__file__).with_name('PEER_CHECK_RESULT.json');p.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
raise SystemExit(0 if out['status']=='PASS' else 1)
