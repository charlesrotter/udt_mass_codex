# UDT metric-orchestra common-domain rehearsal

Date: 2026-07-25  
Grade: `VERIFIED-WITH-CAVEATS`
Maximum conclusion: `EXACT_TYPED_PARTIAL_R_GEOM_AND_COMMON_DOMAIN_CROSS_RESPONSE_ATLAS_ONLY`

## Result first

The proposed geometric instruments can be placed consistently on one common
conditional finite-cell coframe domain.  They do not remain isolated there.
At the neutral two-jet point, the complete Ricci-component response graph in
the declared chart connects all eight amplitudes:

```text
phi -- {sigma,alpha,k} -- {S10,S11,S20,S21},
```

with additional shape/connection and connection/connection edges.  There is
no direct `phi-S` first-rate edge at that point; angular area and shape are the
exact bridge.  This is the first bounded calculation in this line of work to
put reciprocal clock/ruler depth, angular area, angular shape, and horizontal-
vertical mixing into one complete response census rather than testing one
instrument at a time.

The one-number scalar curvature sees only 16 nonzero upper-triangle first-rate
pairs and four nonzero pure second jets.  The ten-component Ricci tensor sees
59 and 17 respectively.  The discrepancy is exact trace cancellation, not
missing sector response.

This establishes a coupling grammar, not a tuning law.  Registered
Reciprocity, `c_E`, CSN, finite-cell structure, seal data, topology, and the
current bootstrap wording still supply no reverse admissibility map that
chooses a profile, boundary functional, action, matter source, density, or
physical branch.

## Exact common-domain structure

The preregistered coframe uses `x0=c_E t` and a bounded `(x0,x)` base with a
conditional torus fiber.  Its eight amplitudes are

```text
phi, sigma, alpha, k, S10, S11, S20, S21.
```

Only `phi` is founded as reciprocal clock/ruler depth.  `sigma` is the angular
common log-area direction; `(alpha,k)` give a complete pointwise positive
determinant-one angular two-metric chart; the four `S` components are a torus
connection.  These seven completing directions are mathematically complete
for this coframe chart but remain physically unselected.

Exact identities include:

- `det(E)=exp(sigma)` and `det(g)=-exp(2 sigma)`;
- four-volume `exp(sigma) dx0 dx dy dz`, so reciprocal `phi` cancels exactly;
- observer-rest spatial volume `exp(phi+sigma)`;
- `x`-boundary induced volume `exp(-phi+sigma)`;
- `G_ang=exp(sigma)H`, with `det(H)=1` and no `sigma` dependence;
- connection curvatures `F1=d0S11-d1S10` and `F2=d0S21-d1S20`;
- an exact general covector norm involving all eight sectors;
- exact torus-invariant `dphi` norm
  `-exp(2phi)phi_0^2+exp(-2phi)phi_1^2`.

See `EXACT_DERIVATION.md` for the complete formulas.

## The trace-hidden ensemble

The scalar trace organizes into reciprocal base combinations, angular shape
rates, and the two connection field strengths.  On its own it suggests a
nearly block-separated system.  That suggestion is false for the underlying
Ricci response in the tested chart:

- `phi` has direct first-rate response edges to `sigma`, `alpha`, and `k`;
- every `S` component has a direct edge to one or more of `sigma,alpha,k`;
- the four `S` components also cross-couple among themselves;
- the complete family graph is connected even with self-edges removed;
- the Ricci second jets separate into base, angular diagonal, angular shear,
  and mixed base/angular channels.

This component graph is a typed local response result in the declared coframe
chart.  It is not promoted to a new frame-independent invariant.  The tensor
itself is covariant; this specific graph records how the preregistered chart
amplitudes enter its components at one regular point.

## Independent verification

Production used exact SymPy 1.14.0 metric two-jets and passed 25 algebraic
checks.  A separately implemented mpmath 1.3.0 route evaluated the full
coframe metric directly at 70 digits, constructed fourth-order finite-
difference metric jets, and reconstructed:

- all 256 scalar-Hessian entries;
- all 2,560 Ricci-Hessian component entries;
- all 24 scalar second-jet responses; and
- all 240 Ricci second-jet component entries.

At step `h=0.001`, maximum absolute errors were approximately
`1.53e-11` for the scalar Hessian, `5.34e-6` for the Ricci Hessians,
`1.34e-12` for scalar second jets, and `6.67e-13` for Ricci second jets.
All errors decreased by more than the verifier's required factor of three.
Pure-gauge
connection jets gave zero curvature, while one unit field-strength control
gave scalar curvature `1/2`.

The independent result's 20 checks comprise 15 numerical reconstruction or
geometric controls and five schema/source/artifact-integrity checks.  The
latter are regression guards, not additional independent physics evidence.

A fresh source-first reviewer froze expectations before seeing any production
artifact (`ADVERSARIAL_PRERULING.md`, SHA-256
`36a02a336120397f4092c1199ca53e59c2de9795ea5ac78b1b14595152ea6a49`).
A separate SymPy `diffgeom` library route then reproduced eight load-bearing
first-rate Ricci controls and all 240 pure-second-jet Ricci entries exactly.
After exact connection-gauge reduction, the raw four `S` amplitudes collapse
to the two curvature channels `(F1,F2)`.  The resulting six-node graph
`{phi,sigma,alpha,k,F1,F2}` remains connected and retains no direct `phi-F`
edge.  See `INDEPENDENT_REVIEW.md` and `GAUGE_REDUCED_RICCI_GRAPH.tsv`.

## Reverse-arrow audit

`A_ARROW_AUDIT.tsv` keeps the directions separate:

```text
metric/coframe amplitudes -> geometric outputs        derived here in part
complete outputs -> admissible/realized amplitudes    still open
```

`c_E` calibrates the time coordinate.  Reciprocity fixes the founded
clock/ruler relation.  CSN identifies an equivalence layer but does not choose
a representative.  A finite cell requires boundary/gluing data but does not
derive a boundary functional.  Current bootstrap is on-shell admissibility,
not an instantiated same-branch feedback operator.  None supplies the missing
reverse arrow.

## Scope and caveats

The audit is exhaustive only for the preregistered eight-amplitude,
torus-invariant, neutral-point first/two-jet census plus the exact general
local covector norm.  It does not cover arbitrary angular dependence of the
curvature, non-neutral nonlinear profiles, all four-dimensional coframes,
the complete Riemann/Weyl response, global cap/quotient descent, an on-shell
branch, or dynamics.

No action, field equation, carrier, source, density, mass, energy, boundary
charge, or topology is selected.  No GPU work or numerical solution search
was run.  The result cannot be called matter emergence or bootstrap closure.

Repository preservation gates pass: six frozen manifests retain 127 entries
and 133 tracked paths; all 1,114 current artifact paths and 306 frontier rows
resolve; tests remain 70 passed and one expected xfail; and the protected
55-path dirty checkout retains its recorded metadata with contents unread.

## Next justified step

The next metric-led audit is the nonlinear Cartan/Bianchi ensemble map on the
same coframe, followed across complete finite-cell branches.  It asks whether
metric identities preserve or reduce the newly visible tensor network away
from the neutral point.  Density tuning and time-live/GPU solves remain
premature until a native equation or operational admissibility arrow exists.
