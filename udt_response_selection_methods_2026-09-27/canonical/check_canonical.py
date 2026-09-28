#!/usr/bin/env python3
"""Exact local controls; author context, not independent scientific review.

CPU only, no physical parameter values, no grid and no floating tolerances.
Run with timeout 120s. The analytic proof is in CONSTRUCTION.md.
"""
import json
import platform
from pathlib import Path
import sympy as S

ROOT = Path(__file__).resolve().parent
A, B, C, D = S.symbols('A B C D', real=True)  # FREE method coefficients
x, y, z = coords = S.symbols('x y z', real=True)
slots = [(0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2)]
checks = {}
details = {}

def record(name, result):
    checks[name] = bool(result)
    assert checks[name], name

def symmat(values):
    out = S.zeros(3)
    for (i, j), value in zip(slots, values):
        out[i, j] = out[j, i] = value
    return out

def contraction(left, right):
    return sum(left[i, j] * right[i, j] for i in range(3) for j in range(3))

# Full six-variable kinetic/volume differentiation; non-diagonal SPD evaluation.
hs, ps = S.symbols('h0:6'), S.symbols('p0:6')
H, P = symmat(hs), symmat(ps)
H0 = S.Matrix([[4, 1, 1], [1, 3, 1], [1, 1, 2]])
P0 = S.Matrix([[2, -1, 3], [-1, 4, 2], [3, 2, -2]])
subs = {hs[k]: H0[i, j] for k, (i, j) in enumerate(slots)}
subs.update({ps[k]: P0[i, j] for k, (i, j) in enumerate(slots)})
s = S.sqrt(H.det())
p = contraction(H, P)
q = A * contraction(P, H * P * H) + B * p**2
s0, p0 = S.sqrt(H0.det()), contraction(H0, P0)
q0 = q.subs(subs)
h_expected = (2*A*P0*H0*P0 + 2*B*p0*P0 - H0.inv()*q0/2)/s0
pi_expected = 2*(A*H0*P0*H0+B*p0*H0)/s0
for k, (i, j) in enumerate(slots):
    factor = 1 if i == j else 2
    record(f'kinetic_h_derivative_{i}{j}',
           S.simplify(S.diff(q/s, hs[k]).subs(subs)-factor*h_expected[i,j]) == 0)
    record(f'kinetic_pi_derivative_{i}{j}',
           S.simplify(S.diff(q/s, ps[k]).subs(subs)-factor*pi_expected[i,j]) == 0)
    record(f'volume_h_derivative_{i}{j}',
           S.simplify(S.diff(D*s, hs[k]).subs(subs)-factor*D*s0*H0.inv()[i,j]/2) == 0)
record('catch_missing_offdiagonal_factor',
       S.simplify(S.diff(q/s, hs[3]).subs(subs)-h_expected[0,1]) != 0)
details['positive_metric_leading_minors'] = [4, 11, int(H0.det())]

# Linearized scalar curvature from Christoffel definition, all six perturbations.
k = symmat([S.Function(f'k{a}')(x,y,z) for a in range(6)])
gamma1 = [[[sum(S.KroneckerDelta(a,l) *
              (S.diff(k[l,c],coords[b])+S.diff(k[l,b],coords[c])-S.diff(k[b,c],coords[l]))
              for l in range(3))/2 for c in range(3)] for b in range(3)] for a in range(3)]
linear_R = sum(S.diff(gamma1[a][i][i],coords[a])-S.diff(gamma1[a][i][a],coords[i])
               for a in range(3) for i in range(3))
claimed_linear_R = sum(S.diff(k[i,j],coords[i],coords[j]) for i in range(3) for j in range(3)) \
                 - sum(S.diff(S.trace(k), c, 2) for c in coords)
record('all_component_curvature_linearization', S.simplify(linear_R-claimed_linear_R) == 0)

# Jet independence: 18 free first derivatives -> momentum divergence + trace gradient.
jets = S.symbols('jet0:18')
pj = [symmat(jets[6*d:6*(d+1)]) for d in range(3)]
div = S.Matrix([sum(pj[i][i,j] for i in range(3)) for j in range(3)])
gradtrace = S.Matrix([S.trace(pj[j]) for j in range(3)])
jetmap = S.Matrix.vstack(div, gradtrace).jacobian(jets)
details['jet_map_shape'] = list(jetmap.shape)
details['jet_map_rank'] = int(jetmap.rank())
record('divergence_and_trace_gradient_independent', jetmap.rank() == 6)

# Exact polynomial IBP control on [-1,1]^3: N,M and first derivatives vanish on faces.
# This is a boundary-vanishing analytic control, not a globally smooth bump claim.
N = (1-x*x)**2*(1-y*y)**2*(1-z*z)**2
M = (x+2*y+z*z)*N
Pfield = S.Matrix([[x+2*y, x*y+x*x, y*z+x],
                   [x*y+x*x, 3*x+z, x*z+y],
                   [y*z+x, x*z+y, x*x+2*x+3*z]])
ptrace = S.trace(Pfield)
w = [S.expand(N*S.diff(M,c)-M*S.diff(N,c)) for c in coords]
lapN, lapM = sum(S.diff(N,c,2) for c in coords), sum(S.diff(M,c,2) for c in coords)
direct_A = sum(Pfield[i,j]*(M*S.diff(N,coords[i],coords[j])-N*S.diff(M,coords[i],coords[j]))
               for i in range(3) for j in range(3))
direct_trace = ptrace*(M*lapN-N*lapM)
def cube_integral(expr):
    total = 0
    for powers, coeff in S.Poly(S.expand(expr), *coords).terms():
        if all(power % 2 == 0 for power in powers):
            total += coeff*S.prod(S.Rational(2,power+1) for power in powers)
    return S.factor(total)

direct = 2*C*(A*cube_integral(direct_A)-(A+2*B)*cube_integral(direct_trace))
momentum_div = [sum(S.diff(Pfield[i,j],coords[i]) for i in range(3)) for j in range(3)]
Dvalue = -2*cube_integral(sum(w[j]*momentum_div[j] for j in range(3)))
Jvalue = cube_integral(sum(w[j]*S.diff(ptrace,coords[j]) for j in range(3)))
after_IBP = -A*C*Dvalue-2*C*(A+2*B)*Jvalue
record('exact_smeared_bracket_vs_direct_hessian', S.expand(direct-after_IBP) == 0)
record('control_momentum_and_trace_both_nonzero', Dvalue != 0 and Jvalue != 0)
record('catch_wrong_momentum_bracket_sign', S.expand(direct-(A*C*Dvalue-2*C*(A+2*B)*Jvalue)) != 0)
record('catch_wrong_trace_coefficient', S.expand(direct-(-A*C*Dvalue-2*C*(A+B)*Jvalue)) != 0)
record('normalized_closure_control', S.simplify((direct-Dvalue).subs({B:-A/2,C:-1/A})) == 0)
details['cube_Dw'] = str(Dvalue)
details['cube_trace_gradient_integral'] = str(Jvalue)
details['cube_direct_bracket'] = str(S.factor(direct))

# Actual weak-closure witness. Direct Christoffel and Ricci, not inserted curvature.
f = S.Function('f')(x)
qfun = S.Function('q')(x)
g = S.diag(1,f**2,1)
ginv = g.inv()
gp = S.diag(0,0,f*qfun)  # weight-one contravariant momentum
Gamma = [[[S.simplify(sum(ginv[a,l]*(S.diff(g[l,c],coords[b])+S.diff(g[l,b],coords[c])
                      -S.diff(g[b,c],coords[l])) for l in range(3))/2)
           for c in range(3)] for b in range(3)] for a in range(3)]
Ric = S.Matrix(3,3, lambda i,j: S.simplify(sum(
    S.diff(Gamma[k][i][j],coords[k])-S.diff(Gamma[k][i][k],coords[j])
    +sum(Gamma[k][k][l]*Gamma[l][i][j]-Gamma[k][j][l]*Gamma[l][i][k] for l in range(3))
    for k in range(3))))
R = S.simplify(contraction(ginv,Ric))
# Compute density covariant derivative with all slots before cancellation.
divdensity = [S.simplify(sum(S.diff(gp[i,j],coords[i])
    +sum(Gamma[i][i][l]*gp[l,j]+Gamma[j][i][l]*gp[i,l]-Gamma[l][l][i]*gp[i,j]
         for l in range(3)) for i in range(3))) for j in range(3)]
trace_density = contraction(g,gp)
grad_density = [S.simplify(S.diff(trace_density,coords[i])
    -sum(Gamma[l][l][i] for l in range(3))*trace_density) for i in range(3)]
Qwarp = A*contraction(gp,g*gp*g)+B*trace_density**2
Hscalar = S.simplify(Qwarp/f**2+C*R+D)
record('witness_curvature_direct', S.simplify(R+2*S.diff(f,x,2)/f) == 0)
record('witness_momentum_constraint_direct', divdensity == [0,0,0])
record('witness_density_trace_gradient_direct', grad_density == [f*S.diff(qfun,x),0,0])
record('witness_H_scalar_direct', S.simplify(Hscalar-((A+B)*qfun**2-2*C*S.diff(f,x,2)/f+D)) == 0)
ode = ((A+B)*x*x+D)*f/(2*C)
record('witness_H_zero_after_ODE', S.simplify(Hscalar.subs(qfun,x).subs(S.diff(f,x,2),ode)) == 0)
record('catch_omitted_weight_one_connection',
       S.simplify(S.diff(trace_density,x)-grad_density[0]) != 0)
details['witness_scalar_curvature'] = str(R)
details['witness_momentum_divergence'] = list(map(str,divdensity))
details['witness_covariant_trace_gradient'] = list(map(str,grad_density))
details['witness_H_over_sqrt_h'] = str(Hscalar)

# Exact Legendre identities at the same non-diagonal metric, all K components free.
K = symmat(S.symbols('K0:6'))
Ktrace = S.trace(H0.inv()*K)
Kraised = H0.inv()*K*H0.inv()
canonical_P = s0*(Kraised-Ktrace*H0.inv())/A
canonical_trace = contraction(H0,canonical_P)
record('legendre_velocity_inversion', all(S.simplify(v)==0 for v in
    (A*(H0*canonical_P*H0-canonical_trace*H0/2)/s0-K)))
kinetic_H = A*(contraction(canonical_P,H0*canonical_P*H0)-canonical_trace**2/2)/s0
legendre_kinetic = 2*contraction(canonical_P,K)-kinetic_H
record('legendre_kinetic_identity', S.simplify(legendre_kinetic-s0*(contraction(K,Kraised)-Ktrace**2)/A)==0)

out = {'status':'PASS', 'evidence':'exact symbolic author controls; not fresh review',
       'python':platform.python_version(), 'sympy':S.__version__,
       'checks':checks, 'check_count':len(checks), 'details':details}
(ROOT/'CHECK_RESULT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,indent=2,sort_keys=True))
