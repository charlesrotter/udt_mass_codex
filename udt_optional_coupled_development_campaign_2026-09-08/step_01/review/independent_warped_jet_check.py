"""Post-exposure direct CD1 check: exact metric jets and covariant K derivatives.

Reuses an inspected, pinned previous reviewer geometry utility; no CD1 author
code/result import. Finite diagnostics, not Picard-Lindelof or PDE proofs.
"""
import ast
from fractions import Fraction as F
import hashlib
import json
import pathlib
import platform

old = pathlib.Path('udt_source_metric_connection_campaign_2026-09-08/step_03/review/independent_interface_check.py')
raw = old.read_bytes()
pin = '06c96d1df44bc67f697ebbe9a6100cdc0f281e20d681e61fdb7ed7c423cb8071'
assert hashlib.sha256(raw).hexdigest() == pin
# Reuse only the two inspected pure geometry functions, without old test runs.
tree = ast.parse(raw)
definitions = [node for node in tree.body if isinstance(node, ast.FunctionDef)
               and node.name in ('zeros', 'curvature')]
assert len(definitions) == 2
exec(compile(ast.Module(body=definitions, type_ignores=[]), str(old), 'exec'))

checks, red, records = [], [], []
def check(name, actual, expected=F(0)):
    assert actual == expected, (name, actual, expected)
    checks.append(name)
def reject(name, residual):
    try:
        assert residual == 0
    except AssertionError:
        red.append({'name':name, 'residual':str(residual), 'guard':'RED'})
    else:
        raise AssertionError('false pass: '+name)

def projections(a, ap, app, A, B, Aprime, Bprime):
    ginv = [[F(-1 if i == 0 else 1) if i==j else F(0)
             for j in range(4)] for i in range(4)]
    ginv[2][2] = ginv[3][3] = 1/(a*a)
    first, second = zeros(4,4,4), zeros(4,4,4,4)
    kv = [A, a*a*B, a*a*B]
    kprime = [Aprime, 2*a*ap*B+a*a*Bprime, 2*a*ap*B+a*a*Bprime]
    for i in range(1,4):
        first[0][i][i] = -2*kv[i-1]
        second[0][1][i][i] = second[1][0][i][i] = -2*kprime[i-1]
        second[0][0][i][i] = F(2*i+1, 7)  # arbitrary unclaimed normal acceleration
    for i in (2,3):
        first[1][i][i] = 2*a*ap
        second[1][1][i][i] = 2*(ap*ap+a*app)
    _, r4, s4 = curvature(ginv, first, second)
    i3 = [[ginv[i+1][j+1] for j in range(3)] for i in range(3)]
    d3 = [[[first[k+1][i+1][j+1] for j in range(3)] for i in range(3)] for k in range(3)]
    dd3 = [[[[second[k+1][l+1][i+1][j+1] for j in range(3)] for i in range(3)] for l in range(3)] for k in range(3)]
    conn, r3, scalar = curvature(i3, d3, dd3)
    K = [[kv[i] if i==j else F(0) for j in range(3)] for i in range(3)]
    DK = zeros(3,3,3)
    for k in range(3):
        for i in range(3):
            for j in range(3):
                DK[k][i][j] = (kprime[i] if k==0 and i==j else F(0)) - sum(
                    conn[e][k][i]*K[e][j]+conn[e][k][j]*K[i][e] for e in range(3))
    M = [sum(i3[j][k]*(DK[j][k][i]-DK[i][j][k]) for j in range(3) for k in range(3)) for i in range(3)]
    tr = sum(i3[i][j]*K[i][j] for i in range(3) for j in range(3))
    norm = sum(i3[i][j]*i3[k][l]*K[i][k]*K[j][l] for i in range(3) for j in range(3) for k in range(3) for l in range(3))
    H = scalar+tr*tr-norm
    return scalar, H, M, r4[0][0]+s4/2, r4[0][1:]

for number, data in enumerate([
    (F(2,3), F(9,4), F(2,5), F(-1,3), F(5,3), F(-4,7), F(0), F(7,5)),
    (F(5,4), F(16,25), F(-3,7), F(2,9), F(3,2), F(5,8), F(-2), F(-3,4)),
    (F(1), F(2), F(0), F(1,5), F(4,3), F(-1), F(3,2), F(1)),
    (F(3,2), F(4,9), F(1,2), F(-7,8), F(2), F(3,5), F(5,11), F(-2)),
]):
    a, rho, rp, rpp, E, beta, lam, B = data
    s0 = rho*a*a
    h = -rp/(2*rho)
    ap = a*h
    app = a*(3*rp*rp/(4*rho*rho)-rpp/(2*rho))
    T = beta*rho*E*E
    R = -4*app/a-2*h*h
    A = (2*lam+2*T-R-2*B*B)/(4*B)
    Bprime = h*(A-B)-T/2
    scalar, H, M, Gnn, Rni = projections(a,ap,app,A,B,F(17,13),Bprime)
    prefix = 'jet_'+str(number)+'_'
    check(prefix+'intrinsic_scalar', scalar,R)
    check(prefix+'full_H',H,2*lam+2*T)
    for i in range(3):
        check(prefix+'full_M_'+str(i), M[i], T if i==0 else F(0))
        check(prefix+'negative_K_Gauss_Codazzi_'+str(i), M[i],-Rni[i])
    check(prefix+'normal_Gauss_Codazzi',H,2*Gnn)
    check(prefix+'fixed_product',rho*a*a,s0)
    check(prefix+'phase_flux',rho*E*a*a,s0*E)
    records.append({'rho':str(rho),'rho_prime':str(rp),'rho_second':str(rpp),
                    's0':str(s0),'E':str(E),'beta':str(beta),'Lambda':str(lam),
                    'A':str(A),'B':str(B),'Bprime':str(Bprime),'R3':str(scalar),
                    'H':str(H),'M':list(map(str,M))})
    if number==0:
        wrong = projections(a,ap,app,A,B,F(17,13),h*(A-B)+T/2)
        reject('reversed_momentum_sign',wrong[2][0]-T)
        reject('dropped_warp_connection',-2*Bprime-T)
        badA=(2*lam+2*T+R-2*B*B)/(4*B)
        wrong=projections(a,ap,app,badA,B,F(17,13),h*(badA-B)-T/2)
        reject('wrong_scalar_sign_in_elimination',wrong[1]-2*lam-2*T)
        reject('dropped_phase_from_product',s0*E-s0)

# Nondivided chart control: gamma flat, T constant!=0, Lambda=-T,
# B(x)=-T*x/2, A(x)=-B(x)/2 solves constraints THROUGH B=0.
# This verifies that the candidate's B!=0 exclusion is a method-chart limit.
T=F(3,2)
for x in (F(-1,5),F(0),F(2,7)):
    B=-T*x/2
    scalar,H,M,Gnn,Rni=projections(F(1),F(0),F(0),-B/2,B,T/4,-T/2)
    check('crossing_H_'+str(x),H,F(0))
    check('crossing_Mx_'+str(x),M[0],T)
    check('crossing_My_'+str(x),M[1])
    check('crossing_Mz_'+str(x),M[2])
print(json.dumps({'python':platform.python_version(),'arithmetic':'fractions.Fraction exact',
                  'geometry_utility':str(old),'geometry_utility_sha256':pin,
                  'checks_passed':len(checks),'checks':checks,'red':red,'jets':records,
                  'scope':'finite original-equation metric-jet diagnostics; no ODE/PDE existence proof'},indent=2))
