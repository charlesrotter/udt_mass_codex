# Source-first expectation — nonlinear Cartan/Bianchi ensemble

Frozen by the fresh adversarial context before it read
`derive_cartan_ensemble.py` or any generated production table.

Original `/tmp` artifact SHA-256:
`6e197767abf3e4efc8da01fe9eba6d237effd036c246c6c1c9118405008b6569`.
The text below preserves its scientific content; only repository-relative
wording and formatting are normalized.

## Convention-sensitive predictions

With `e01=theta0 wedge theta1`, `p_i=s_i/2-a_i`, and
`q_i=s_i/2+a_i`, direct differentiation of the stated coframe must give

```text
d theta0 = u1 e01
d theta1 = u0 e01
d theta2 = f2 e01 + p0 e02 + p1 e12 + h0 e03 + h1 e13
d theta3 = f3 e01 + q0 e03 + q1 e13.
```

For `K=dD D^-1`, the right Maurer-Cartan identity has sign
`dK-K wedge K=0`, not `dK+K wedge K=0`. In the anholonomic base,
`[E0,E1]=-u1 E0-u0 E1`, so scalar mixed jets obey
`E0(v1)-E1(v0)+u1 v0+u0 v1=0`.

The Levi-Civita slots must be uniquely determined from these structure
coefficients by the Koszul formula. Curvature uses
`Omega^a_b=d omega^a_b+omega^a_c wedge omega^c_b`; after lowering the first
index it must satisfy pair antisymmetry, pair exchange, and first Bianchi once
the explicit coframe-integrability identities are imposed. The second Bianchi
identity is differential consistency, not an equation of motion.

## Nonlinear family expectation

Curvature should contain derivatives of all six registered families and
nonlinear quadratic couplings. The full graph is expected to be connected
through angular common/shape/shear families. A direct
`PHI_ANHOLONOMY--CONNECTION_CURVATURE_1/2` quadratic edge is not expected: in
the phi-plus-F slice the apparent `u_i f_A` terms from differentiating the
coframe cancel against spin-connection products. Phi can couple indirectly to
`f2/f3` through `sigma/alpha/k`, while nonzero `f` curvature cannot honestly
be called a matter force or source.

The ten channels are complete only for the stated torus-invariant
upper-triangular regular chart. Individual `a,h,f2,f3` components are
basis/chart dependent; only tensorial curvature or properly transformed,
lattice-aware statements can be global/invariant.

## Completion and ontology expectation

Exactly twelve completion rows are required. FC01-FC10 and FC12 may admit the
local formula on regular toric patches subject to boundary, cap, gluing,
monodromy, orientation, and rank conditions. FC11 is not globally covered by
a toric fibration chart and must be an explicit scope failure. None of the
twelve rows is a complete on-shell universe or global coverage theorem.

No torsion equation, Maurer-Cartan identity, Riemann symmetry, or Bianchi
identity supplies the missing response one-form, action, source, density law,
selector, or dynamics. The maximum admissible result is an exact local
nonlinear geometric atlas plus a scoped applicability map.

## Independent route

1. Rebuild structure coefficients from the coframe.
2. Reconstruct the connection with the Koszul formula.
3. Build curvature with the noncoordinate-frame component formula.
4. Cross-check against a coordinate-metric Christoffel/Riemann calculation.
5. Contract curvature and compare the neutral specialization with the banked
   parent formula.
6. Parse production rows only after these expectations are frozen.
