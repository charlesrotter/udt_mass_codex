"""Source-first exact jet diagnostic: constrained data -> harmonic full Ricci.

No CD2 author code/results. Reuse only two inspected prior REVIEWER pure
geometry functions through AST selection; do not execute its old tests.
All first/second derivatives are coordinate metric derivatives at one event.
Finite jets do not establish a PDE existence theorem.
"""
import ast
from copy import deepcopy
from fractions import Fraction as F
import hashlib
import json
import pathlib
import platform

root = pathlib.Path(__file__).resolve().parents[3]
utility = root / 'udt_source_metric_connection_campaign_2026-09-08/step_03/review/independent_interface_check.py'
expected = '06c96d1df44bc67f697ebbe9a6100cdc0f281e20d681e61fdb7ed7c423cb8071'
blob = utility.read_bytes()
assert hashlib.sha256(blob).hexdigest() == expected
tree = ast.parse(blob)
selected = ast.Module(body=[node for node in tree.body
                           if isinstance(node, ast.FunctionDef)
                           and node.name in ('zeros', 'curvature')], type_ignores=[])
namespace = {'F': F}
exec(compile(selected, str(utility), 'exec'), namespace)
zeros, curvature = namespace['zeros'], namespace['curvature']

checks, reds, values = [], [], {}


def flat(value):
    return [z for v in value for z in flat(v)] if isinstance(value, list) else [value]


def accept_zero(value):
    assert all(v == 0 for v in flat(value)), str(value)


def check(name, value):
    accept_zero(value)
    checks.append(name)


def red(name, value):
    try:
        accept_zero(value)
    except AssertionError:
        reds.append({'name': name, 'status': 'RED', 'residual': list(map(str, flat(value)))})
    else:
        raise AssertionError('mutant unexpectedly passed: ' + name)


def diagonal(entries):
    return [[value if i == j else F(0) for j in range(len(entries))]
            for i, value in enumerate(entries)]


def harmonic(g, gi, dg, ddg):
    """Contract the expanded metric derivative formula, not curvature's loops."""
    di = [[[-sum(gi[a][i]*dg[k][i][j]*gi[j][b] for i in range(4) for j in range(4))
            for b in range(4)] for a in range(4)] for k in range(4)]
    H = [sum(gi[a][b]*gi[c][d]*(dg[c][d][b]-dg[b][c][d]/2)
             for b in range(4) for c in range(4) for d in range(4)) for a in range(4)]
    dH = [[sum((di[k][a][b]*gi[c][d]+gi[a][b]*di[k][c][d])
                *(dg[c][d][b]-dg[b][c][d]/2)
                +gi[a][b]*gi[c][d]*(ddg[k][c][d][b]-ddg[k][b][c][d]/2)
                for b in range(4) for c in range(4) for d in range(4))
            for a in range(4)] for k in range(4)]
    conn, ric, scalar = curvature(gi, dg, ddg)
    # On H=0, Ric^H = Ric - g_(a|c| partial_b) H^c.
    reduced = [[ric[a][b]-sum(g[a][c]*dH[b][c]+g[b][c]*dH[a][c]
                             for c in range(4))/2 for b in range(4)] for a in range(4)]
    return H, dH, reduced, ric, scalar, conn, di


def case(a, ap, app, B, E, Ep, s, beta, lam, Aprime, wrong_momentum=False):
    h = ap/a
    n = s/a**2
    T = beta*n*E**2
    R3 = -4*app/a-2*h**2
    A = (2*lam+2*T-R3-2*B**2)/(4*B)
    Bp = h*(A-B)+(T/2 if wrong_momentum else -T/2)
    g, gi = diagonal([F(-1), F(1), a*a, a*a]), diagonal([F(-1), F(1), a**-2, a**-2])
    dg, ddg = zeros(4, 4, 4), zeros(4, 4, 4, 4)
    dg[0][0][0] = 2*(A+2*B)
    dg[0][0][1] = dg[0][1][0] = -2*h
    dg[0][1][1] = -2*A
    for z in (2, 3):
        dg[0][z][z] = -2*a*a*B
        dg[1][z][z] = 2*a*ap
        ddg[1][1][z][z] = 2*(ap*ap+a*app)
        ddg[0][1][z][z] = ddg[1][0][z][z] = -2*(2*a*ap*B+a*a*Bp)
    ddg[0][1][0][0] = ddg[1][0][0][0] = 2*(Aprime+2*Bp)
    for c, d in ((0, 1), (1, 0)):
        ddg[0][1][c][d] = ddg[1][0][c][d] = -2*(app/a-h*h)
    ddg[0][1][1][1] = ddg[1][0][1][1] = -2*Aprime
    initial = harmonic(g, gi, dg, ddg)
    q = [-E, E, F(0), F(0)]
    source = [[lam*g[c][d]+beta*n*q[c]*q[d] for d in range(4)] for c in range(4)]
    for c in range(4):
        for d in range(4):
            ddg[0][0][c][d] = 2*(source[c][d]-initial[2][c][d])
    out = harmonic(g, gi, dg, ddg)
    return dict(g=g, gi=gi, dg=dg, ddg=ddg, q=q, n=n, A=A, B=B, Bp=Bp,
                E=E, Ep=Ep, h=h, T=T, source=source, initial=initial, out=out)


seeds = [tuple(map(F, row)) for row in (
    ('3/2','2/5','-1/7','4/3','5/4','2/9','7/5','-3/2','0','-2/3'),
    ('5/3','-1/4','2/7','-3/5','7/6','-3/11','2','4/7','-2/3','1/5'),
    ('4/5','3/8','1/6','2/9','9/7','5/13','3/2','5/4','3/7','2/5'),
    ('7/4','-2/9','-3/8','-5/6','4/3','-1/7','5/2','-2/3','2','-4/9'),
)]
for index, seed in enumerate(seeds):
    d = case(*seed)
    H, dH, reduced, ric, scalar, conn, di = d['out']
    g, gi, dg, ddg, q = (d[k] for k in ('g', 'gi', 'dg', 'ddg', 'q'))
    E, Ep, n, B, h = (d[k] for k in ('E', 'Ep', 'n', 'B', 'h'))
    check(f'{index}_initial_harmonic', H)
    check(f'{index}_initial_spatial_harmonic_rate', dH[1:])
    check(f'{index}_reduced_metric_equation', [[reduced[c][b]-d['source'][c][b]
                                             for b in range(4)] for c in range(4)])
    check(f'{index}_normal_harmonic_rate_from_constraints', dH[0])
    check(f'{index}_FULL_original_Ricci', [[ric[c][b]-d['source'][c][b]
                                         for b in range(4)] for c in range(4)])
    probe = deepcopy(ddg)
    for c in range(4):
        for b in range(4):
            probe[0][0][c][b] += F((c+b+1)*(c*b+2), 13)
    probe_reduced = harmonic(g, gi, dg, probe)[2]
    check(f'{index}_wave_normal_coefficient_half',
          [[probe_reduced[c][b]-reduced[c][b]-F((c+b+1)*(c*b+2), 26)
            for b in range(4)] for c in range(4)])
    ell = [sum(gi[c][b]*q[b] for b in range(4)) for c in range(4)]
    dq = zeros(4, 4)
    dq[1][0], dq[1][1] = -Ep, Ep
    for b in range(4):
        dq[0][b] = (sum(ell[c]*conn[k][c][b]*q[k] for c in range(4) for k in range(4))
                    -sum(ell[c]*dq[c][b] for c in range(1,4)))/ell[0]
    check(f'{index}_covector_geodesic_normal_form',
          [sum(ell[c]*(dq[c][b]-sum(conn[k][c][b]*q[k] for k in range(4)))
               for c in range(4)) for b in range(4)])
    check(f'{index}_FULL_initial_covector_closure',
          [[dq[c][b]-dq[b][c] for b in range(4)] for c in range(4)])
    check(f'{index}_null_norm_and_derivatives',
          [sum(gi[c][b]*q[c]*q[b] for c in range(4) for b in range(4))]
          +[sum(di[k][c][b]*q[c]*q[b]+2*gi[c][b]*dq[k][c]*q[b]
                for c in range(4) for b in range(4)) for k in range(4)])
    dell = [[sum(di[k][c][b]*q[b]+gi[c][b]*dq[k][b] for b in range(4))
             for c in range(4)] for k in range(4)]
    divell = sum(dell[c][c]+sum(conn[c][c][b]*ell[b] for b in range(4)) for c in range(4))
    nx = -2*h*n
    nt = (-n*divell-ell[1]*nx)/ell[0]
    check(f'{index}_conservation_normal_form', nt*ell[0]+nx*ell[1]+n*divell)
    check(f'{index}_FULL_initial_product_normal_rate', nt-2*B*n)
    values[str(index)] = {'A':str(d['A']), 'Bprime':str(d['Bp']), 'n':str(n),
                          'T':str(d['T']), 'n_time':str(nt), 'q_time':list(map(str,dq[0])),
                          'Ric00':str(ric[0][0]), 'Ric01':str(ric[0][1])}
    if index == 0:
        wrong = case(*seed, wrong_momentum=True)
        red('reverse_negative_K_momentum_guard', wrong['out'][1][0])
        red('reverse_negative_K_FULL_Ricci_guard',
            [[wrong['out'][3][c][b]-wrong['source'][c][b] for b in range(4)] for c in range(4)])
        bad_dg = deepcopy(dg)
        bad_dg[0][0][0] = -dg[0][0][0]
        red('wrong_harmonic_lapse_rate', harmonic(g, gi, bad_dg, ddg)[0])
        red('erase_density_area_evolution', -2*B*n)
        red('drop_spatial_phase_derivative', dq[0][1])

print(json.dumps({'python':platform.python_version(), 'arithmetic':'exact Fraction',
                  'checks_passed':len(checks), 'checks':checks, 'red_paths':reds,
                  'values':values, 'reused_reviewer_utility_sha256':expected}, indent=2, sort_keys=True))
