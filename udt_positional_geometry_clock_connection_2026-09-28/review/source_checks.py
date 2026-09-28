"""Independent source-first exact checks. No author implementation imported."""
import json
import platform
import sympy as sp

checks = {}
def zero(name, value):
    residual = sp.simplify(value)
    checks[name] = {"residual": str(residual), "pass": residual == 0}
    if residual != 0:
        raise RuntimeError((name, residual))

t, L, a0, d = sp.symbols("t L a0 d", real=True, nonzero=True)
tB = ((a0 + d*t)*sp.exp(d*L)-a0)/d
zero("time_live_incidence_chord", (a0+d*tB)-(a0+d*t)*sp.exp(d*L))
zero("time_live_received_clock_slope", sp.diff(tB,t)-sp.exp(d*L))
zero("flat_constant_delay_zero_shift", sp.diff(t+L,t)-1)
zero("time_live_flat_limit", sp.limit(tB,d,0)-(t+a0*L))

NA, NB = sp.symbols("NA NB", positive=True)
proper_static_slope = NB/NA
zero("static_return_reciprocal", proper_static_slope*(NA/NB)-1)
delta = sp.symbols("delta", real=True)
zero("even_candidate_differs_from_signed_arrow",
     (sp.exp(-delta)-2/(sp.exp(delta)+sp.exp(-delta)))
     -((sp.exp(-2*delta)-1)/(sp.exp(delta)+sp.exp(-delta))))

# Independent endpoint incidence in Minkowski spacetime: A at x=0,
# B at x=L+v t, proper clocks tau_A=t_A and tau_B=sqrt(1-v^2)t_B.
v = sp.Rational(3,5)
tauB = sp.sqrt(1-v*v)*(L+t)/(1-v)
zero("fixed_velocity_nearby_slope_is_two", sp.diff(tauB,t)-2)
zero("zero_distance_does_not_remove_fixed_velocity_shift", sp.limit(sp.diff(tauB,t),L,0)-2)

# At one orthonormal event U=(1,0,0,0), k=(1,n), omega=1.
# Unit normalization gives nabla_a U_0=0. Antisymmetry cancels vorticity.
H, ax, ay, az, s1, s2, s12, s13, s23, w12, w13, w23 = sp.symbols(
    "H ax ay az s1 s2 s12 s13 s23 w12 w13 w23", real=True)
nx,ny,nz = sp.symbols("nx ny nz", real=True)
n = sp.Matrix([nx,ny,nz]); a=sp.Matrix([ax,ay,az])
sigma=sp.Matrix([[s1,s12,s13],[s12,s2,s23],[s13,s23,-s1-s2]])
w=sp.Matrix([[0,w12,w13],[-w12,0,w23],[-w13,-w23,0]])
Du=sp.zeros(4)
for j in range(3):
    Du[0,j+1]=a[j]
for i in range(3):
    for j in range(3):
        Du[i+1,j+1]=(H*sp.eye(3)+sigma+w)[i,j]
k=sp.Matrix([1,nx,ny,nz])
contraction=(k.T*Du*k)[0]
K=H+(a.T*n)[0]+(n.T*sigma*n)[0]
zero("clock_slope_kinematic_decomposition_on_unit_sphere",
     contraction-K-H*((n.T*n)[0]-1))
zero("opposite_direction_even_channel",
     K+K.xreplace({nx:-nx,ny:-ny,nz:-nz})-2*(H+(n.T*sigma*n)[0]))

print(json.dumps({
    "classification":"independent exact symbolic arithmetic supporting source-first analysis",
    "python":platform.python_version(), "sympy":sp.__version__,
    "shape":"one 4x4 local derivative matrix; scalar exact checks; no grid",
    "checks":checks, "all_pass":all(x["pass"] for x in checks.values()),
    "limits":"No physical metric, observer population, signal content, scale or native value law is selected."
},indent=2))
