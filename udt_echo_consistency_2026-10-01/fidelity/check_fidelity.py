"""ECS1 exact fidelity checks; independent endpoint contractions, no producer imports."""
import hashlib
import json
import platform
from pathlib import Path
import sympy as S

L = S.Symbol('L', real=True)
t, x, y, z = S.symbols('t x y z', real=True)
checks = []
def equal(name, actual, wanted=0):
    difference = S.trigsimp(S.expand_trig(S.simplify(actual-wanted)))
    if difference != 0:
        raise AssertionError((name, str(difference)))
    checks.append(name)
def require(name, condition):
    if not condition:
        raise AssertionError(name)
    checks.append(name)
def trunc(expr):
    return S.series(expr, L, 0, 5).removeO().expand()
def expr(text):
    return S.sympify(text, locals={'L': L})

source = Path('udt_finite_positional_clock_test_2026-10-01/math/kasner_higher.stdout')
raw = source.read_bytes()
saved = json.loads(raw)
require('saved_source_status', saved['status'] == 'PASS')
results = []
for row in saved['controls']:
    r = S.Rational(row['p'])
    tb = 1+expr(row['tb_minus_one'])
    ta = 1+expr(row['ta_minus_one'])
    C = expr(row['C'])
    ab = trunc(tb**r)
    aa = trunc(ta**r)
    gamma = trunc(S.sqrt(1+C*C/ab**2))
    # At each endpoint use k^mu=(1/a, +/-1/a^2), U_B=(gamma,C/a^2).
    # Covariant metric diag(-1,a^2); normalize outgoing coordinate momentum to1.
    gb = S.diag(-1, trunc(ab**2))
    ub = S.Matrix([gamma, trunc(C/ab**2)])
    kout = S.Matrix([trunc(1/ab), trunc(1/ab**2)])
    kin = S.Matrix([trunc(1/ab), -trunc(1/ab**2)])
    omega_b_out = trunc(-(ub.T*gb*kout)[0])
    omega_b_in = trunc(-(ub.T*gb*kin)[0])
    # A is comoving, with outgoing frequency1 and received incoming frequency1/a_a.
    p = trunc(1/omega_b_out)
    q = trunc(omega_b_in*aa)
    lp, lq = trunc(S.log(p)), trunc(S.log(q))
    equal(f'{r}: reconstructed_log_outgoing', lp, expr(row['log_outgoing']))
    equal(f'{r}: reconstructed_log_return', lq, expr(row['log_return']))
    predicted_q = trunc(p/(2-p*p))
    residual = trunc(q-predicted_q)
    log_residual = trunc(S.log(q)-S.log(predicted_q))
    # Independent desired cubic coefficients frozen in SOURCE_FIRST.md.
    expected_cubic = {S.Rational(-1,3): -S.Rational(16,27),
                      S.Rational(2,3): S.Rational(8,27), S.Integer(0):0, S.Integer(1):0}[r]
    equal(f'{r}: actual_echo_residual_L2', residual.coeff(L,2))
    equal(f'{r}: actual_echo_residual_L3', residual.coeff(L,3), expected_cubic)
    equal(f'{r}: log_echo_residual_L3', log_residual.coeff(L,3), expected_cubic)
    if r in (0,1):
        equal(f'{r}: flat_control_p', p, 1)
        equal(f'{r}: flat_control_q', q, 1)
    else:
        # Mistaking a whole-echo derivative for q changes a nonzero quadratic term.
        wrong_q = trunc(p*q)
        require(f'{r}: q_vs_pq_mutant_detected', trunc(wrong_q-q).coeff(L,2) != 0)
    results.append({'axis_r':str(r), 'p':str(p), 'q':str(q),
                    'q_minus_discriminator':str(residual), 'log_residual':str(log_residual)})

# Shared double-angle identity checks are explicitly algebraic regression, not independent flights.
rational = []
for C0 in [S.Rational(5,3), S.Integer(1), S.Rational(4,5)]:
    p0=1/C0
    q0=C0/(2*C0*C0-1)
    require(f'C={C0}: regular_echo_domain', bool(0<p0 and p0*p0<2))
    equal(f'C={C0}: elimination', q0, p0/(2-p0*p0))
    equal(f'C={C0}: whole_echo', p0*q0, p0*p0/(2-p0*p0))
    if p0!=1:
        require(f'C={C0}: mislabeled_pq_detected', p0*q0!=q0)
    rational.append({'C':str(C0),'p':str(p0),'q':str(q0),'pq':str(p0*q0)})
Cbad=S.Rational(3,5)
pbad=1/Cbad
qbad=Cbad/(2*Cbad*Cbad-1)
require('formal_continuation_domain_rejected', bool(pbad*pbad>2 and qbad<0))

# Original coordinate metric/connection/Ricci computation, not inserting scalar formulas.
def geometry(name, g, expected_R, split):
    coord=[t,x,y,z]
    inv=g.inv()
    Gamma=[[[S.simplify(sum(inv[i,l]*(S.diff(g[l,k],coord[j])+S.diff(g[l,j],coord[k])-S.diff(g[j,k],coord[l])) for l in range(4))/2)
             for k in range(4)] for j in range(4)] for i in range(4)]
    Ric=S.zeros(4)
    for j in range(4):
        for k in range(4):
            Ric[j,k]=S.simplify(sum(S.diff(Gamma[i][j][k],coord[i])-S.diff(Gamma[i][j][i],coord[k])
              +sum(Gamma[i][i][m]*Gamma[m][j][k]-Gamma[i][k][m]*Gamma[m][j][i] for m in range(4)) for i in range(4)))
    scalar=S.simplify(sum(inv[j,k]*Ric[j,k] for j in range(4) for k in range(4)))
    equal(name+': scalar_invariant',scalar,expected_R)
    for i in range(4):
        for j in range(4):
            for k in range(4):
                if len({i in split,j in split,k in split})>1:
                    equal(f'{name}: product_connection_{i}{j}{k}',Gamma[i][j][k])
    # At coordinate origin compare with the full4D space form or flat metric.
    at0={x:0,y:0}
    normalized=[S.simplify(Ric[i,i]/g[i,i]).subs(at0) for i in range(4)]
    require(name+': not_an_Einstein_metric',len(set(normalized))>1)
    return {'metric':str(g),'Ricci':str(Ric),'scalar':str(scalar),
            'normalized_diagonal_Ricci_at_origin':[str(v) for v in normalized]}

geometries={
    'positive_plane_flat_transverse': geometry('positive',S.diag(-S.cos(x)**2,1,1,1),2,{0,1}),
    'negative_plane_flat_transverse': geometry('negative',S.diag(-S.cosh(x)**2,1,1,1),-2,{0,1}),
    'flat_plane_positive_transverse': geometry('flat_plane',S.diag(-1,1,1,S.cos(y)**2),2,{0,1})
}
print(json.dumps({'status':'PASS','check_count':len(checks),'checks':checks,
 'source_sha256':hashlib.sha256(raw).hexdigest(),'source':str(source),
 'kasner_endpoint_reconstruction':results,'rational_controls':rational,
 'inadmissible_continuation':{'p':str(pbad),'formal_q':str(qbad)},'product_metrics':geometries,
 'python':platform.python_version(),'sympy':S.__version__,
 'scope':'Exact finite symbolic checks. Product connection proof owns continuum planar mimic; no independent arrival ODE, global classification, field-sector or native admission.'},indent=2))
