"""Finite exact anchors; not the proof or independent review of SM1."""
import json
import platform
import sympy as S

checks = {}
def check(name, condition):
    checks[name] = bool(condition)
    assert checks[name], name

H,A,B,p,q,t = S.symbols('H A B p q t', real=True)
g = S.Matrix([[0,1,0,0],[1,H,A,B],[0,A,p,q],[0,B,q,t]])
check('full_adapted_determinant', S.expand(g.det()) == -(p*t-q*q))
check('full_covector_inverse', g*S.Matrix([1,0,0,0]) == S.Matrix([0,1,0,0]))
# Generic adapted geometry, not claimed to solve a metric field equation.
r,phi,theta = S.symbols('r phi theta', positive=True)
s,D,a = S.symbols('s D a', positive=True)
J = r**2*S.sin(theta)  # Flat outgoing null coordinates, 0<theta<pi, r>0.
n = s/J
check('expanding_flat_tube_conservation', S.simplify(S.diff(J*n,r)/J) == 0)
wrong = S.simplify(S.diff(J*s,r)/J)
check('mutation_missing_area_rejected', wrong == 2*s/r and wrong != 0)
# In outgoing coordinates g=2dr dphi-dphi^2+r^2 dOmega^2,
# static future unit U has (U^r,U^phi)=(0,-1); ell=(1,0).
g2 = S.Matrix([[0,1],[1,-1]])
U,ell = S.Matrix([0,-1]), S.Matrix([1,0])
check('observer_unit', (U.T*g2*U)[0] == -1)
Gamma = s/J
check('observer_readout', S.simplify(-(U.T*g2*(n*ell))[0]-Gamma) == 0)
check('mutation_readout_sign_rejected', S.simplify((U.T*g2*(n*ell))[0]-Gamma) != 0)
# k scales with Theta, whereas ell=k/Delta is invariant under admitted gauge.
k = D*ell
check('phase_spacing_gauge', S.simplify(a*k/(a*D)-k/D) == S.zeros(2,1))
check('mutation_missing_spacing_rejected', S.simplify(a*k-k) != S.zeros(2,1))
Sphase = 2+S.sin(phi)
check('conserved_phase_dependent_counterexample', S.diff(Sphase,r) == 0 and S.diff(Sphase,phi) != 0)
check('measure_rescaling_not_gauge', S.simplify(3*n-n) != 0)
z = S.symbols('z', positive=True)
check('positive_label_jacobian_ratio', S.simplify((s*z)/(J*z)-n) == 0)
check('negative_chart_jacobian_ratio', S.simplify((s*S.Abs(-z))/(J*S.Abs(-z))-n) == 0)
# Four linearly independent future unit timelike vectors in a Minkowski frame.
obs = S.Matrix([[1,0,0,0],[S.Rational(5,3),S.Rational(4,3),0,0],
                [S.Rational(5,3),0,S.Rational(4,3),0],
                [S.Rational(5,3),0,0,S.Rational(4,3)]])
check('observer_span_anchor', obs.det() != 0)
print(json.dumps({'kind':'same-author finite exact anchors, not independent proof',
                  'python':platform.python_version(),'sympy':S.__version__,
                  'checks':checks,'passed':len(checks)}, sort_keys=True, indent=2))
