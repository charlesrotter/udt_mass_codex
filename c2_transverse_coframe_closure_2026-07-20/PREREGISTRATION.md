# Transverse-coframe closure audit — preregistration

Date: 2026-07-20

Base: `f214dba92109b7e6d9ecdd5e68b11113b5368e81`

Branch: `codex/c2-transverse-coframe-closure-2026-07-20`

Mode: CPU-only exact symbolic derivation plus independent automatic-differentiation witnesses

## Whole question

The intrinsic-angular product audit showed that scalar Gaussian curvature changes the conditional
`C2` background and twist equations but does not select the remaining reciprocal cubic family. It
also exposed directional screen-connection dependence.

This audit asks the smallest next metric-led question:

> When the local toric transverse area, shear, and gauge-complete twist connection are restored, do
> their equations add a local selector for the product Bach family, or does selection remain a
> global boundary/bootstrap problem?

This is `METRIC_LED` and `OBSERVING`. It does not target a favorable coefficient, particle, carrier,
topology, or boundary.

## Whole frame and bounded sector

The local coframe is

```text
e0 = sqrt(y(r)) dt,
e1 = dr/sqrt(y(r)),
e2 = a(r) exp(+s(r)) d theta,
e3 = a(r) exp(-s(r)) F(theta)
     [d psi + A_r(r,theta) dr + A_theta(r,theta) d theta],

y>0, a>0, F>0,
F_second + K F = 0.
```

The connection obeys the exact local coordinate gauge law

```text
psi -> psi - lambda(r,theta),
A -> A + d lambda,
H = dA.
```

Only after recording that law, the toric radial control fixes local radial gauge

```text
A_r=0, A_theta=epsilon*u(r), H=u_first dr wedge dtheta.
```

This gauge does not remove global holonomy, periods, caps, or boundary data. Constant `u` must be a
local pure-gauge zero mode.

`a(r)` is the transverse area-radius mode and `s(r)` is diagonal shear. The product audit is the
exact control `a=1,s=0`. The constant-curvature `F` seed remains a bounded angular control: its sign
and `K` are free, but its general shape, topology, and variation are not supplied.

## Premise ledger

| Object | Classification |
|---|---|
| The metric is the theory | `pinned-by-THEORY` |
| Reciprocal clock/radial block | `DERIVED-CONDITIONAL` under inherited sign, unit, representative, and slot premises |
| Four-dimensional conformal-Lorentzian readout | `INHERITED / CONDITIONAL` |
| Metric-only local `C2` bulk | `UNIQUE-CONDITIONAL` only in the frozen pre-scale action class |
| `y(r)>0` | `free-and-varied` |
| transverse area `a(r)>0` | `free-and-varied` |
| transverse shear `s(r)` | `free-and-varied` |
| local connection `A` and curvature `H=dA` | `free-and-varied`; radial gauge used only after gauge law is explicit |
| intrinsic curvature `K` | `free-and-explored`, including both signs and zero |
| constant-curvature toric seed `F` | `pinned-by-HABIT / BOUNDED CONTROL` |
| static radial dependence of `y,a,s,u` | `pinned-by-HABIT / BOUNDED CONTROL` |
| unrestricted angular metric and nontoric modes | `OMITTED / OPEN` |
| cap, period, topology, finite-cell seal, boundary functional, bootstrap | `OPEN / EXCLUDED` |
| carrier, `S2`, `L2+L4`, source, scale, mass | `OPEN / EXCLUDED` |
| exact algebra and float64 AD | category-A methods |

## Frozen calculations

1. Derive the exact connection gauge law and identify the invariant `H`; distinguish local radial
   gauge from global holonomy.
2. Construct the complete background metric and `sqrt(-g) C2` action density with arbitrary
   `y,a,s` and constant-curvature `F`.
3. Derive the reduced radial Euler expressions and all endpoint-current coefficients for variations
   of `y,a,s`. These are ansatz projections and must not be renamed the unrestricted metric equation.
4. Evaluate those projections on the exact product family
   `a=1,s=0,y=A r^3+B r^2+C r+D,B^2=3AC+K^2`.
5. Compare with every full Bach component already derived at the product point. Determine whether
   freeing area or shear adds a condition on that family.
6. Expand the complete `sqrt(-g) C2` action through quadratic order in the gauge curvature
   `A_theta=epsilon*u(r)`, retaining arbitrary `y,a,s` where computationally exact.
7. Derive the twist Jacobi operator and both radial endpoint channels. Verify dependence on `u`
   occurs only through derivatives and recover the product result exactly.
8. Test the mixed quadratic blocks between reflection-even area/shear variations and the
   reflection-odd twist. A symmetry proof must be accompanied by an explicit algebraic or AD check.
9. Independently reconstruct registered action-density and projection witnesses with a separate
   Torch coordinate implementation.

If the exact unrestricted `a,s` twist expression is computationally intractable, stop and return
`COFRAME_CONTROL_INCONCLUSIVE`; do not freeze profiles or drop terms to force completion.

## Frozen independent witnesses

```text
y = 2 + r/3 + r^2/5 - r^3/7,
a = 1 + r/5 + r^2/10,
s = r/7 - r^2/11,
u = 2r/5 - r^2/4 + r^3/6,
r = -1/3, 1/5.

K=+1: F=sin(theta),  theta=0.7
K= 0: F=1,           theta=0.4
K=-1: F=cosh(theta), theta=0.6
```

Product controls use `a=1,s=0` and the exact full-Bach witness
`K=1,y=r^3-r/3+2`. Nonzero comparisons require relative `1e-8`; zero and mixed-block controls
require absolute `1e-9` in float64.

## Frozen outcome classes

1. `LOCAL_TRANSVERSE_COFRAME_SELECTS_PRODUCT_SUBFAMILY` — area/shear/full-connection equations add
   a nonredundant local condition on the product Bach family.
2. `PRODUCT_BACH_FAMILY_REMAINS_FULL_METRIC_STATIONARY` — freeing the registered coframe modes adds
   no local background condition at the product point.
3. `TWIST_HESSIAN_MIXES_WITH_AREA_OR_SHEAR` — a nonzero quadratic mixed block survives after gauge
   completion.
4. `TWIST_HESSIAN_BLOCK_DIAGONAL_BY_REFLECTION` — all registered twist/even-sector mixed Hessian
   blocks vanish while the pure twist block remains.
5. `TRANSVERSE_COFRAME_CHANGES_TWIST_OPERATOR` — nonconstant area/shear add exact terms to the pure
   twist operator.
6. `COFRAME_CONTROL_INCONCLUSIVE` — exact derivation, product recovery, or independent verification
   fails.

Multiple classes may apply. None may be renamed global bootstrap closure, carrier emergence,
stability, or a complete action.

## Falsification and stop line

- Dropping `sqrt(-g)`, connection components before showing gauge covariance, area/shear derivative
  terms, full Bach components, endpoint currents, or zero strata fails the audit.
- Reduced ansatz stationarity cannot add authority beyond the full Bach tensor.
- A constant-`u` response fails local gauge completion.
- Failure to recover the product action and branch equations exactly is conclusive failure.
- Any registered independent mismatch above tolerance yields `COFRAME_CONTROL_INCONCLUSIVE`.
- The result must retain unrestricted angular geometry, global boundary/topology, time dependence,
  bootstrap, carrier, source, and scale as open.

Maximum positive conclusion:

`CONDITIONAL_LOCAL_C2_TRANSVERSE_COFRAME_CLOSURE_CHARACTERIZED`.

No startup-control edit, `CANON.md` edit, GPU work, physical boundary choice, carrier adoption,
repository reorganization, or mass claim is authorized.
