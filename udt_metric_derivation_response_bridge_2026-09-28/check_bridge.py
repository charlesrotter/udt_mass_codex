"""Exact construction controls; mathematical probes, no physical law adoption."""
import json
import platform
import time
import sympy as s

start = time.monotonic()
checks = {}


def eq(name, actual, expected=0):
    residual = s.simplify(s.expand(actual - expected))
    if residual != 0:
        raise AssertionError((name, residual))
    checks[name] = {"residual": str(residual)}


def nonzero(name, value):
    value = s.simplify(value)
    if value == 0:
        raise AssertionError((name, value))
    checks[name] = {"nonzero_control": str(value)}


t, r, theta, az = s.symbols("t r theta az", real=True)
f, N = s.Function("f")(r), s.Function("N")(r)
x = [t, r, theta, az]
g = s.diag(-N**2 * f, 1/f, r**2, r**2 * s.sin(theta)**2)
inverse = g.inv()
Gamma = [[[s.simplify(sum(inverse[i, k] * (
    s.diff(g[k, j], x[l]) + s.diff(g[k, l], x[j]) - s.diff(g[j, l], x[k])
) for k in range(4))/2) for l in range(4)] for j in range(4)] for i in range(4)]
Ric = s.Matrix(4, 4, lambda i, j: s.simplify(sum(
    s.diff(Gamma[k][i][j], x[k]) - s.diff(Gamma[k][i][k], x[j])
    + sum(Gamma[k][k][l]*Gamma[l][i][j] - Gamma[k][j][l]*Gamma[l][i][k]
          for l in range(4)) for k in range(4))))
mixed = s.simplify(inverse * Ric)
R = s.simplify(s.trace(mixed))
R_expected = (-s.diff(f, r, 2) - 4*s.diff(f, r)/r + 2*(1-f)/r**2
              - 2*f*s.diff(N, r, 2)/N - 3*s.diff(f, r)*s.diff(N, r)/N
              - 4*f*s.diff(N, r)/(r*N))
eq("full_4d_scalar_with_independent_N", R, R_expected)
for i in range(4):
    for j in range(4):
        if i != j:
            eq(f"off_diagonal_Ric_{i}{j}", mixed[i,j])
eq("full_metric_determinant", g.det(), -N**2*r**4*s.sin(theta)**2)
primary = lambda value: s.simplify(value.subs(N, 1).doit())
Rf = primary(R)
U = -s.diff(f,r,2)/2-s.diff(f,r)/r
V = (1-f-r*s.diff(f,r))/r**2
for i, expected in enumerate([U,U,V,V]):
    eq(f"primary_Ric_{i}", primary(mixed[i,i]), expected)
eq("primary_scalar", Rf, 2*(U+V))

a,b,P,Q,Z = s.symbols("a b P Q Z", real=True)
response = [a*U+b*Rf,a*U+b*Rf,a*V+b*Rf]
v = s.Matrix([[1,-1],[-1,-1],[0,1]])
pair_matrix = v.T*s.diag(1,1,2)
eq("fixed_volume_directions_1", (s.Matrix([[1,1,2]])*v)[0,0])
eq("fixed_volume_directions_2", (s.Matrix([[1,1,2]])*v)[0,1])
eq("static_tracefree_pairing_rank", pair_matrix.rank(), 2)
eq("pairing_kernel_dimension", len(pair_matrix.nullspace()), 1)
eq("kernel_equal_entries", sum((pair_matrix*s.ones(3,1))[i]**2 for i in range(2)))
eq("generic_founded_tangent_pairing", (pair_matrix*s.Matrix([P,Q,Z]))[0], P-Q)
eq("G301_founded_tangent_annihilates_all_coefficients", (pair_matrix*s.Matrix(response))[0])
eq("complementary_probe", (pair_matrix*s.Matrix(response))[1], 2*a*(V-U))
eq("complementary_Euler_equation", V-U, s.diff(f,r,2)/2-(f-1)/r**2)
c2, cm1 = s.symbols("c2 cm1", real=True)
family = 1+c2*r**2+cm1/r
eq("known_Einstein_family_complement", (V-U).subs(f,family).doit())
eq("known_Einstein_family_scalar", Rf.subs(f,family).doit(), -12*c2)

Lambda = s.symbols("Lambda", real=True)
L = N*r**2*(R-2*Lambda)
boundary = -N*r**2*s.diff(f,r)-2*f*r**2*s.diff(N,r)
bulk = 2*N*(1-f-r*s.diff(f,r)-Lambda*r**2)
eq("Hilbert_boundary_identity", L, s.diff(boundary,r)+bulk)


def EL(density, field):
    return s.simplify(s.diff(density,field)
        - s.diff(s.diff(density,s.diff(field,r)),r)
        + s.diff(s.diff(density,s.diff(field,r,2)),r,2))


eq("full_N_variation", EL(L,N), 2*(1-f-r*s.diff(f,r)-Lambda*r**2))
eq("full_f_variation", EL(L,f), 2*r*s.diff(N,r))
eq("bulk_N_variation", EL(bulk,N), EL(L,N))
eq("bulk_f_variation", EL(bulk,f), EL(L,f))
eq("primary_density_total_derivative", primary(L), 2-s.diff(r**2*f,r,2)-2*Lambda*r**2)
eq("primary_Hilbert_EL_zero", EL(primary(L),f))
eq("retained_N_variation_is_full_tt_equation", EL(L,N), -2*r**2*(primary(mixed[0,0]-R/2)+Lambda))
eq("fixed_Lambda_solution", EL(L,N).subs(f,1+cm1/r-Lambda*r**2/3).doit())

epsilon = s.symbols("epsilon", positive=True)
control = 1+epsilon*r**4
control_sub = lambda expr: s.simplify(expr.subs(f,control).doit())
eq("positive_profile_R", control_sub(Rf), -30*epsilon*r**2)
nonzero("missing_angular_equation_detected", control_sub(V-U))
nonzero("missing_N_equation_detected", control_sub(EL(L,N)).subs(Lambda,0))
eq("wrong_profile_still_passes_primary_Hilbert_variation", control_sub(EL(primary(L),f)))
nonzero("catch_wrong_sum_in_tangent_projection", control_sub(2*U))
nonzero("catch_discarded_angular_second_derivative", control_sub(s.diff(f,r,2)/2))

# Existing unadopted higher-order response: do not add a new term or physical alpha.
alpha = s.symbols("alpha", nonzero=True, real=True)
F = 1+2*alpha*Rf
Hess = s.Matrix(4,4,lambda i,j: s.simplify(s.diff(F,x[i],x[j])
    - sum(primary(Gamma[k][i][j])*s.diff(F,x[k]) for k in range(4))))
primary_inverse = inverse.applyfunc(primary)
boxF = s.simplify(s.trace(primary_inverse*Hess))
R2response = s.simplify(F*mixed.applyfunc(primary)
    -(Rf+alpha*Rf**2)*s.eye(4)/2+boxF*s.eye(4)-primary_inverse*Hess)
eq("R2_full_response_t_minus_r", R2response[0,0]-R2response[1,1], 2*alpha*f*s.diff(Rf,r,2))
L2 = r**2*(Rf+alpha*Rf**2)
eq("R2_restricted_variation", EL(L2,f), -2*alpha*r**2*s.diff(Rf,r,2))
eq("R2_projected_full_equals_restricted_variation", EL(L2,f), -r**2*(R2response[0,0]-R2response[1,1])/f)
nonzero("R2_control_survives_projection", control_sub(EL(L2,f)))
eq("R2_fourth_radial_derivative_coefficient", s.diff(EL(L2,f),s.diff(f,r,4)), 2*alpha*r**2)

print(json.dumps({"status":"PASS","count":len(checks),"checks":checks,
    "python":platform.python_version(),"sympy":s.__version__,
    "elapsed_seconds":time.monotonic()-start,
    "derived_scalar":str(R),"founded_tangent_projection":"P-Q",
    "complementary_projection":"2 a (V-U)",
    "Hilbert_primary_EL":str(EL(primary(L),f)),
    "limits":"Exact static spherical projection/variation diagnostic; not native action, full dynamics, universal postulate insufficiency, or an adopted extension."},indent=2))
