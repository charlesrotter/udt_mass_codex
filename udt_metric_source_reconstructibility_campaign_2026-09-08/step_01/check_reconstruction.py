"""Exact diagnostic recomputation from metric components; not general proof."""
import json
import sympy as s

u, r, x, y = coords = s.symbols('u r x y', real=True)
checks = {}
def check(name, value):
    checks[name] = bool(value)
    assert value, name
def zero(value):
    return all(s.simplify(v) == 0 for v in value) if isinstance(value, s.MatrixBase) else s.simplify(value) == 0
def metric_calculus(g):
    inv = g.inv()
    gamma = [[[s.simplify(sum(inv[a,d]*(s.diff(g[d,c],coords[b])
        +s.diff(g[d,b],coords[c])-s.diff(g[b,c],coords[d])) for d in range(4))/2)
        for c in range(4)] for b in range(4)] for a in range(4)]
    ric = s.zeros(4)
    for a in range(4):
        for b in range(4):
            ric[a,b] = s.simplify(sum(s.diff(gamma[c][a][b],coords[c])
                -s.diff(gamma[c][a][c],coords[b])
                +sum(gamma[c][c][d]*gamma[d][a][b]-gamma[c][b][d]*gamma[d][a][c]
                     for d in range(4)) for c in range(4)))
    scalar = s.simplify(s.trace(inv*ric))
    def div(v):
        return s.simplify(sum(s.diff(v[a],coords[a])
            +sum(gamma[a][a][b]*v[b] for b in range(4)) for a in range(4)))
    return inv, gamma, ric, scalar, div
def exterior(b):
    return s.Matrix(4,4,lambda i,j:s.diff(b[j],coords[i])-s.diff(b[i],coords[j]))
def frobenius(b):
    db=exterior(b)
    return [s.simplify(b[i]*db[j,k]+b[j]*db[k,i]+b[k]*db[i,j])
            for i in range(4) for j in range(i+1,4) for k in range(j+1,4)]
def assert_zero(value, reason):
    assert zero(value), reason

# Pointwise Ricci algebra: all trace powers vanish but full square/rank fails.
eta=s.diag(-1,1,1,1)
q0=s.Matrix([-1,0,0,1]); e=s.Matrix([0,1,0,0])
T=q0*e.T+e*q0.T; B=eta*T
check('rank_two_tracefree_fixture', T.rank()==2 and s.trace(B)==0)
check('all_positive_trace_powers_nilpotent', all(s.trace(B**k)==0 for k in range(1,5)) and zero(B**3))
check('full_square_is_nonzero', not zero(B**2) and zero(B**2-(eta*q0)*q0.T))
K=lambda a,b,c,d:(eta[a,c]*T[b,d]+eta[b,d]*T[a,c]-eta[a,d]*T[b,c]-eta[b,c]*T[a,d])/2
KR=s.Matrix(4,4,lambda b,d:sum(eta[a,c]*K(a,b,c,d) for a in range(4) for c in range(4)))
check('pointwise_curvature_Ricci_contracts_to_fixture', zero(KR-T))

for rho in (s.Rational(1),s.Rational(-2),s.Rational(9,4)):
    S0=rho*q0*q0.T; epsilon=s.sign(rho)
    roots=[]
    for U in (s.Matrix([1,0,0,0]),s.Matrix([s.Rational(5,3),s.Rational(4,3),0,0])):
        amplitude=(U.T*S0*U)[0]
        b=-epsilon*S0*U/s.sqrt(abs(amplitude))
        roots.append(b)
        check(f'root_future_and_full_factor:{rho}:{U[0]}', (eta*b)[0]>0 and zero(epsilon*b*b.T-S0))
    check(f'auxiliary_observer_independence:{rho}', zero(roots[0]-roots[1]))

q=s.Matrix([1,0,0,0]); a=1+u**2
g=s.Matrix([[-(x*x+y*y)/2,1,0,0],[1,0,0,0],[0,0,1,0],[0,0,0,1]])
inv,gamma,ric,R,div=metric_calculus(g)
ell=inv*q
check('pp_full_Ricci_and_scalar', zero(ric-q*q.T) and R==0)
check('pp_metric_nondegenerate_lorentz_block', g.det()==-1 and g[0,1]==1)
check('pp_exact_null_phase_and_conservation', zero((q.T*inv*q)[0]) and div(ell)==0)
qp=a*q; np=1/a**2; jp=np*inv*qp
check('nonlinear_phase_exact_full_covector', zero(qp-s.Matrix([s.diff(u+u**3/3,z) for z in coords])))
check('full_tensor_rephase_invariance', zero(np*qp*qp.T-ric))
check('rephased_current_conserved_but_different', div(jp)==0 and zero(jp-ell/a) and not zero(jp-ell))
kc=s.Matrix([-1,g[0,0]/2,0,0]); U=(ell+kc)/s.sqrt(2)
check('complementary_null_and_unit_observer', zero((kc.T*g*kc)[0]) and (ell.T*g*kc)[0]==-1 and zero((U.T*g*U)[0]+1))
Gamma=-(U.T*g*ell)[0]; Gammap=-(U.T*g*jp)[0]
check('fixed_observer_readout_changes_inverse_rate', zero(Gammap-Gamma/a) and not zero(Gammap-Gamma))
for beta_prime in (s.Rational(2),s.Rational(1,3)):
    nprime=1/(beta_prime*a*a)
    check(f'changed_constant_parameter_exact_factor:{beta_prime}', zero(beta_prime*nprime*qp*qp.T-ric))

# Actual variable-scalar metric: rank one and integrable, but not conserved.
gv=s.Matrix([[u*r*r,1,0,0],[1,0,0,0],[0,0,r*r,0],[0,0,0,r*r]])
iv,cv,rv,Rv,dv=metric_calculus(gv)
Sv=s.simplify(rv-Rv*gv/4)
check('variable_scalar_actual_full_Ricci', zero(rv-3*u*gv-r*q*q.T))
check('variable_scalar_actual_trace_and_factor', Rv==12*u and zero(Sv-r*q*q.T))
check('variable_scalar_full_nilpotence', zero((iv*Sv)**2) and Sv.rank()==1)
check('variable_scalar_no_current_conservation', dv(r*iv*q)==3)
check('variable_scalar_rephase_cannot_repair_divergence', zero(dv((r/a**2)*iv*(a*q))-3/a))
check('Bianchi_actual_metric_residual', zero(s.Matrix([s.diff(Rv,z)/4 for z in coords])-3*q))

# A constant-scalar actual metric with nonclosed canonical square root.
gx=s.Matrix([[-x**4/6,1,0,0],[1,0,0,0],[0,0,1,0],[0,0,0,1]])
ix,cx,rx,Rx,dx=metric_calculus(gx)
b=x*q  # restricted x>0, future orientation partial_r
check('nonclosed_root_actual_metric', Rx==0 and zero(rx-b*b.T))
check('nonclosed_root_integrable_not_exact', any(v!=0 for v in exterior(b)) and all(v==0 for v in frobenius(b)))
check('integrating_factor_recovers_conserved_exact_phase', zero(b/x-q) and dx(x*x*ix*q)==0)
twist=s.Matrix([1,0,0,x])  # one-form method fixture, NOT claimed Ricci line
check('Frobenius_method_detects_twist', frobenius(twist)==[0,0,1,0])
check('Frobenius_rescale_covariance', all(s.simplify(v-a*a*w)==0
      for v,w in zip(frobenius(a*twist),frobenius(twist))))

mutants={}
cases=[
 ('trace_only_factor_false_pass',lambda:assert_zero(B**2,'full_square_nonzero')),
 ('wrong_density_power',lambda:assert_zero((1/a)*qp*qp.T-ric,'wrong_full_tensor')),
 ('drop_scalar_constancy',lambda:assert_zero(dv(r*iv*q),'nonzero_divergence')),
 ('canonical_root_assumed_exact',lambda:assert_zero(exterior(b),'nonzero_exterior_derivative')),
]
for name,probe in cases:
    try:
        probe()
    except AssertionError as exc:
        mutants[name]=str(exc)
    else:
        raise AssertionError('uncaught defective substitute:'+name)
print(json.dumps({'kind':'exact finite diagnostics, not general proof',
 'sympy':s.__version__,'coordinates':['u','r','x','y'],
 'checks':checks,'groups':len(checks),'actual_defective_substitutes_caught':mutants,
 'metric_witness_status':'OPTIONAL_COMPARISON_NOT_ADMITTED_VACUUM',
 'twisting_metric_independence':'NOT_ESTABLISHED; one-form fixture only'},indent=2,sort_keys=True))
