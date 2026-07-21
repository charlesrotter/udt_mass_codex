# Transverse-coframe closure audit

Date: 2026-07-20  
Base: `f214dba92109b7e6d9ecdd5e68b11113b5368e81`  
Preregistration commit: `384d558`  
Compute: CPU-only exact SymPy and independent Torch forward-AD  
Status: **VERIFIED-WITH-CAVEATS / PARTIAL** — the background, gauge, variation-domain, and mixed
Hessian rulings are verified; the arbitrary-area/shear pure-twist operator is `INCONCLUSIVE`.

## Result first

Restoring radial transverse area and shear does **not** provide a legitimate new local selector for
the reciprocal product family.

It initially appears to. If the angular profile, caps, periods, and coordinate domain are frozen
while the two angular leg lengths are varied only with radius, the restricted shear projection gives

```text
Euler_s | full product Bach = (8/3) K (y_second - 2K).
```

Setting this to zero would select `y_second=2K` when `K` is nonzero. But that is a false promotion of
a restricted ansatz equation. The exact product Bach system also admits

```text
y_second = -2K,
y_third = y_fourth = 0,
```

the constant-curvature Einstein product branch. Its full Bach tensor vanishes, while the restricted
shear projection is

```text
-32 K^2/3.
```

Therefore the restricted shear equation is detecting the frozen angular completion—cap regularity,
cone angle, period, or boundary—not an additional pointwise field equation. It cannot discard the
Einstein branch or select the physical reciprocal branch.

The exact local connection result is cleaner. For

```text
e3 = a exp(-s) F(theta) [d psi + A],
psi -> psi-lambda,
A -> A+d lambda,
H = dA,
```

the determinant is independent of `A`, constant radial-gauge `A_theta` is a local zero mode, and
reflection `psi -> -psi` makes the action even in `A`. Hence the quadratic twist/even-sector mixed
blocks with area and shear vanish exactly about `A=0`. Independent AD found both mixed blocks exactly
zero at all six registered witnesses while the pure twist block was nonzero.

The exact arbitrary-`a(r),s(r)` pure-twist contraction did not complete within the registered
ten-minute CPU window and was stopped without simplifying the metric. It is `INCONCLUSIVE`, not a
negative result.

Registered outcomes:

```text
PRODUCT_BACH_FAMILY_REMAINS_FULL_METRIC_STATIONARY
TWIST_HESSIAN_BLOCK_DIAGONAL_BY_REFLECTION
COFRAME_CONTROL_INCONCLUSIVE.
```

Maximum banked conclusion:

`CONDITIONAL_LOCAL_C2_TRANSVERSE_COFRAME_CLOSURE_PARTIALLY_CHARACTERIZED`.

## Lay reading

We let the angular screen breathe, stretch in one direction, shrink in the other, and carry a proper
geometric twist connection.

One equation looked as though it finally picked the desired clock curve. But it did so only because
we held the ends and identifications of the angular surface fixed while deforming it. That is like
changing the shape of a globe while refusing to let its poles or longitude spacing adjust, then
mistaking the resulting strain for a new law of nature.

The decisive counterexample is an ordinary exact branch of the full metric equation. The tempting
reduced equation rejects it even though the full pointwise curvature equation says it is valid. So
the reduced “selector” is not trustworthy.

What this teaches us is more useful: the local radial and angular equations cannot be separated from
the global angular completion. The cap, period, regularity, and finite-cell data are now demonstrably
load-bearing—not optional finishing details.

## Exact background action

Use the two positive transverse leg radii

```text
b = a exp(s),
c = a exp(-s).
```

The complete local metric is

```text
ds^2 = -y dt^2 + dr^2/y + b^2 dtheta^2 + c^2 F(theta)^2 dpsi^2,
F_second + K F = 0.
```

`BACKGROUND_CLOSURE.json` records the exact `sqrt(-g)C2` density, all three second-order radial
Euler-density projections for `y,b,c`, and both endpoint coefficients for each field. The general
density carries inequivalent angular weights proportional to `F` and `F_first^2/F`. Therefore there
is no valid general division by an angular volume factor. A radial equation exists only after the
angular domain and regularity data have been selected and integrated.

At the exact product control `b=c=1`, those extra weights collapse and the action returns

```text
sqrt(-g) C2 = F (y_second - 2K)^2/3.
```

The `y` and common-area projections vanish on the complete product Bach equations. The relative-leg
projection produces the obstruction above because it is not an unrestricted compact-support
variation of the curved angular surface with the missing angular data frozen.

## Connection and Hessian structure

The complete local toric connection has two components,

```text
A = A_r dr + A_theta dtheta,
H_rtheta = partial_r A_theta - partial_theta A_r.
```

Local radial gauge sets `A_r=0` and the registered control uses `A_theta=epsilon u(r)`. This does not
remove global Wilson data, periods, caps, or boundary conditions.

The coordinate reflection `psi -> -psi` maps `A -> -A` while leaving `y,a,s,F` even. Any scalar
metric action is consequently even in `A` around the twist-free background. The area–twist and
shear–twist Hessian blocks vanish exactly. This means solving the even linearized coframe modes
cannot renormalize or select the pure twist coefficient at quadratic order.

It does not determine the pure twist block itself for nonconstant `a,s`; that exact contraction is
the portion that timed out.

## Independent verification

A separate Torch coordinate implementation rebuilt the metric, determinant, connection, Riemann,
Ricci, Weyl, Bach, action density, and parameter Hessian.

- general background-density records: `6`;
- maximum scaled background mismatch: `7.751335700394727e-16`;
- Einstein plus conformal Bach components: `32`;
- maximum Bach zero magnitude: `1.0556565501409803e-14`;
- restricted Einstein shear: `-6.8716553305353765`;
- independent expected value: `-6.871655330535371`;
- conformal restricted shear: `-9.928387537893786e-16`;
- area–twist and shear–twist mixed-block maximum: exactly `0.0`;
- smallest pure-twist control magnitude: `0.4239273485225331`;
- constant-connection finite-amplitude difference: `5.551115123125783e-16`.

All registered nonzero comparisons satisfy relative `1e-8`; zero controls satisfy absolute `1e-9`.
The pre-bank corrections and exact timeout are preserved in separate records.

## What is and is not closed

`DERIVED` in this local conditional branch:

- the exact local connection gauge law and curvature `H=dA`;
- connection-independent determinant and constant-connection zero mode;
- reflection block-diagonalization of twist versus area/shear at quadratic order;
- the complete background action density and radial projection/endpoint densities;
- the exact variation-domain obstruction and its Einstein counterexample.

`OPEN` or `INCONCLUSIVE`:

- the exact pure-twist operator with arbitrary nonconstant area and shear;
- the intrinsic angular shape beyond the constant-curvature toric seed;
- admissible caps, periods, topology, finite-cell seal, and boundary action;
- global integration and bootstrap branch selection;
- carrier, matter source, physical scale, time-live stability, and mass.

The `C2` action remains `UNIQUE-CONDITIONAL` only inside the frozen pre-scale action class. No GR
field equation, EH action, `S2` carrier, `L2+L4` matter action, source, scale, or GPU work entered.

## Four banking gates

1. **Preregistered:** yes, commit `384d558`.
2. **Full space or bounded scope:** complete for the declared background/gauge/variation-domain and
   mixed-Hessian questions. The arbitrary-area/shear pure-twist contraction is explicitly
   incomplete.
3. **Independently verified:** yes for every banked load-bearing claim, by a separate Torch tensor
   implementation. No fresh external-model review was authorized.
4. **Every premise audited:** yes; the conditional action, static toric restriction, frozen angular
   seed/domain, boundary, topology, time, carrier, source, and scale are explicit.

Banked grade: **VERIFIED-WITH-CAVEATS / PARTIAL**.

## Scientific decision

Do not impose the restricted radial-shear equation, choose `y_second=2K`, or infer a carrier. The
next conceptual gate is the angular completion itself: determine what the UDT metric and finite-cell
seal require of the angular domain, cap regularity, periods, and admissible compact-support
variations before reducing them to radial equations. Only then can the full coframe legitimately be
tested as a selector.
