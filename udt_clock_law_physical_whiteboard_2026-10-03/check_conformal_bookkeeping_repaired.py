"""CPW1 exact supplied conformal-flat control; not a free-clock limit solve."""
import json,platform
from pathlib import Path
import sympy as s

O=s.symbols('Omega',positive=True)
grad=s.symbols('Ot Ox Oy Oz',real=True)
eta=s.diag(-1,1,1,1);g=eta/O**2;inv=eta*O**2
dg=[-2*eta*grad[i]/O**3 for i in range(4)]
Gamma=[[[s.simplify(sum(inv[a,d]*(dg[b][d,c]+dg[c][d,b]-dg[d][b,c])/2 for d in range(4))) for c in range(4)] for b in range(4)] for a in range(4)]
kb=s.Matrix([5,3,4,0]);assert (kb.T*eta*kb)[0]==0
go=sum(kb[i]*grad[i] for i in range(4))
def acceleration(power):
 k=O**power*kb
 derivative=power*O**(2*power-1)*go*kb
 connection=s.Matrix([sum(Gamma[a][b][c]*k[b]*k[c] for b in range(4) for c in range(4)) for a in range(4)])
 return s.simplify(derivative+connection)
right=acceleration(2);wrong=acceleration(1)
assert right==s.zeros(4,1)
assert (wrong+O*go*kb).applyfunc(s.expand)==s.zeros(4,1) and wrong!=s.zeros(4,1)
rho=s.symbols('rho',real=True)
ub=s.Matrix([s.cosh(rho),s.sinh(rho),0,0]);u=O*ub
ray=s.Matrix([1,1,0,0]);k=O**2*ray
norm=s.simplify((u.T*g*u)[0]);omega=s.simplify(-(u.T*g*k)[0])
assert norm==-1
assert s.simplify(omega.rewrite(s.exp)-O*s.exp(-rho))==0
cancel=s.simplify(omega.rewrite(s.exp).subs(rho,s.log(O)))
assert cancel==1
result={'status':'PASS','python':platform.python_version(),'sympy':s.__version__,'families':3,'assertion_groups':6,'physical_metric':'eta/Omega^2, supplied control','null_vector':[5,3,4,0],'correct_affine_acceleration':[str(x) for x in right],'wrong_affine_acceleration':[str(x) for x in wrong],'proper_norm':str(norm),'frequency':str(s.simplify(omega.rewrite(s.exp))),'divergent_rapidity_frequency':str(cancel),'scope':'Pointwise conformal bookkeeping only; no free-clock asymptotic/physical selection claim.'}
p=Path('udt_clock_law_physical_whiteboard_2026-10-03/PARENT_CHECK_RESULT.json')
with p.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps(result))
