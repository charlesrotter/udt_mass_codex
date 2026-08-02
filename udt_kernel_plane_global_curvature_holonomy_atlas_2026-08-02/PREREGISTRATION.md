# Preregistration — global kernel-plane curvature and finite-loop holonomy atlas

Date: 2026-08-02  
Branch: `grok`  
Base: `f6aaabe5a8da518bf56d9b21b883ba57472df3b9`

## Whole question

On the unchanged stationary, off-shell, complete `R x S3` ensemble, determine the global zero and
singular structure of the metric-anchored kernel-plane curvature

```text
omega_E=g(n,nabla T),
Omega_E=d omega_E
```

on the continued domain `M=S3 minus D`, and evaluate a fixed finite-loop family that probes all six
regular graph edges and both six-puncture pole links. Determine which pointwise branch distinctions
persist globally. Do not ask whether the result resembles charge, matter, a carrier, or a desired
universe.

This is metric-led. It is not a field-equation, action, source, stability, density, or observation
test.

## Frozen candidate universe

`CANDIDATE_UNIVERSE.tsv` retains all 18 parent candidates.

- Global curvature owners: `C04,C08,C09,C10`.
- Exact twist-scaling controls: `C16,C17`; they share `C08` screen data and have `a=4,5`.
- Nine intrinsic-zero, two projector-blocked, and one metric-degenerate candidates remain controls
  and may not acquire a connection or curvature.

No profile, `lambda`, shear, twist, topology, point, loop, radius, pole shell, or acceptance rule may
be changed after outcomes are seen.

## Exact global domain and algebraic route

The prior package fixes

```text
D=C03 union C13 union C23,
C03: q1=q2=0,
C13: q0=q2=0,
C23: q0=q1=0,
M=S3 minus D.
```

Stereographic coordinates

```text
q0=(1-x^2-y^2-z^2)/(1+x^2+y^2+z^2),
(q1,q2,q3)=2(x,y,z)/(1+x^2+y^2+z^2)
```

cover all of `M` because the omitted sphere point belongs to `D`. The exact test is whether the
full metric expression reduces to

```text
eta=f13 sigma1+f23 sigma2,
S=u f12^2+F[(b f13-r f23)^2+f13^2/r^2],
P=u S,
omega_E=-a eta/sqrt(P),
Omega_E=-a[2P d eta-dP wedge eta]/(2 P^(3/2)).
```

This is a preregistered identity to prove or refute, not an accepted input. Every `u,F,r` is positive
on the registered nondegenerate candidates. `S=0` must be proved equivalent to `D`; otherwise the
singular-set claim narrows.

For each of `C04,C08,C09,C10`, clear only proved-positive/nonzero denominators from the three
stereographic components of

```text
B=2P d eta-dP wedge eta.
```

Record primitive polynomial numerators and denominator factorizations. Saturate the numerator ideal
away from the defect polynomial using an auxiliary inverse equation. A Gröbner basis equal to one
may certify an empty complex zero set on `M`. Any nontrivial ideal must be retained and classified;
numerical searching may locate components but cannot certify completeness. A global nonzero claim
requires exact saturation, exact real-algebraic decomposition, or an equivalent fail-closed proof.

## Frozen finite-loop universe

`LOOP_FAMILY_UNIVERSE.tsv` freezes six regular-edge and ten pole-link families.

### Regular-edge meridians

Use the exact stereographic parameterizations in that table at radii

```text
rho in {1/100,1/20,1/10}.
```

All six graph edges are evaluated. `R01` through `R05` are the registered five-meridian homology
basis; `R06` retains the dependent sixth edge. No equality of holonomy on homologous loops is
assumed because `Omega_E` need not vanish.

### Pole-link meridians

At pole sign `s=+1,-1`, use

```text
q=(delta v0,delta v1,delta v2,s sqrt(1-delta^2)),
delta in {1/20,1/10},
epsilon_link=1/10.
```

The five `v(theta)` puncture loops in the table surround `+e0,-e0,+e1,-e1,+e2`; the omitted `-e2`
is the dependent sixth puncture. Both pole signs are retained. These loops probe the pole-link
stratum only; they are not boundary conditions or carrier spheres.

The fixed census is:

```text
18 regular geometric loops + 20 pole-link geometric loops = 38,
38 x 4 independent configurations = 152 primary integrals,
38 x 2 twist controls = 76 exact scaling checks,
total = 228 registered evaluations.
```

## Numerical certification for finite integrals

Finite integrals need not have elementary closed forms. The primary route uses at least 90-decimal
periodic high-precision quadrature with fixed panel refinement. The independent route must use a
separate implementation and quadrature family. Record raw integrals, convergence differences,
orientation, path, and parameters. A nonzero finite value is `OBSERVED_HIGH_PRECISION` unless a
rigorous interval excludes zero. No retuning, rounding-to-pattern, or equality claim may use a
decimal threshold without a preregistered error bound.

For `SO+(1,1)`, report the signed rapidity integral `H=integral omega_E`; the group element is the
corresponding boost. Do not call it a `U(1)` phase. Reversing loop orientation must negate `H`.

## Controls and invariance

The audit must test:

1. exact reconstruction of `omega_E` from the registered metric, including the canceled
   acceleration term `n(phi)=0`;
2. exact positivity/singularity denominators and full defect exclusion;
3. exact `C16=4 C08`, `C17=5 C08` scaling for curvature and every loop integral;
4. consistent screen-`O(2)` component changes versus arbitrary `SO(1,1)` frame-gauge changes;
5. loop orientation reversal;
6. all six edge and both pole strata; and
7. zero, blocked, and degenerate controls remaining unassigned.

## Certification and maximum conclusion

Required before banking:

- source blobs frozen after this preregistration and before production;
- every object in `OBJECT_UNIVERSE.tsv` receives the exact same ID/name in the status table;
- every mutation in `FALSIFICATION_CONTRACT.tsv` changes real evidence/state and is caught;
- independent zero-set and finite-integral implementations share no production functions;
- fresh read-only adversarial review reconstructs the load-bearing factorization, global algebraic
  certificate, and representative loop values;
- six frozen manifests, current paths/frontier, premise guards, links, and tests replay.

Maximum conclusion: a verified or honestly incomplete global curvature/singularity and finite-loop
atlas for the frozen stationary metric family. No charge, quantization, carrier, Hopf section,
particle, force, substrate ontology, physical branch, action, source, boundary, density/bootstrap
value, `X_max`, matter, mass, stability, phenomenology, dynamics, or canonization may follow.
