# UDT macro–micro conformal matching closure — frozen derivation map

## Hygiene

| Field | Value |
|---|---|
| Date | 2026-07-15 |
| Mode | Final analytic source-free matching test; DATA-BLIND |
| Immediate predecessor | `UDT_WRL_CONFORMAL_CARRIER_SCALE_CLOSURE_DERIVATION_RESULTS.md` |
| Exterior | WR-L `A_L=1-r/X`, retaining its DERIVED macro stamp |
| Core probe | Smooth conformal reciprocal core `A_Q=1-r^2/X^2` or the general smooth quadratic member |
| Action branch | Conditional metric-only `S_C proportional to integral sqrt(-g) C^2` |
| Scope | Static reciprocal spherical matching only; unrestricted full-metric provenance audited separately |
| GPU | Not authorized; exact junction algebra first |
| Stop rule | If no unique source-free match exists, stop inverse-action iteration and state the missing physical principle |
| Banking | None; `LIVE.md` and `CANON.md` remain untouched |

## 1. Question

Does the already selected coefficient-free conformal bulk action admit a smooth, source-free,
stationary junction between a regular reciprocal core and the exact WR-L exterior, and—if so—does
stationarity uniquely fix `R/X`?

## 2. Radial functional

For

\[
ds^2=-A(r)c^2dt^2+A(r)^{-1}dr^2+r^2d\Omega^2,
\]

use the exact invariant

\[
C^2=\frac{W[A]^2}{3r^4},
\qquad
W[A]=r^2A''-2rA'+2(A-1).
\]

After the exact angular/time reduction, irrelevant positive constants aside,

\[
I[A]=\int dr\,\frac{W[A]^2}{r^2}.
\]

This reduced functional is used only after its solutions are checked against the previously derived
full Bach constraint.

## 3. Pre-registered tests

### T1. Exact first variation

Derive

\[
\delta I=\int E[A]\,\delta A\,dr
+\left[P_0\delta A+P_1\delta A'\right]_{\partial I}
\]

directly. Check all signs and powers of `r`. Identify the two fourth-order boundary momenta.

### T2. Source-free junction conditions

For a free internal interface with no interface action, require a metric regular enough that `C^2`
is locally integrable. Derive the continuity requirements on `A,A',P_0,P_1`. Determine whether a
jump in `A'` creates an inadmissible squared distribution.

### T3. General bulk extremal

Solve the radial Euler equation and impose the full Bach constraint. Apply smooth-center conditions
and exact equality with WR-L on an exterior open interval.

### T4. Point matching

Even before analytic continuation, test whether

\[
A_{m in}=1+b r^2
\]

can match both `A` and `A'` to WR-L at any `0<R<X`.

### T5. Moving-interface condition

Derive the generalized radial Hamiltonian/transversality quantity. If both phases have `W=0`, test
whether free-interface stationarity contains any information capable of selecting `R/X`.

### T6. Interface-action counterfamily

Allow a generic local interface primitive `B(A,A',R)` only as a nonuniqueness probe. Show which
jump conditions its derivatives change. Do not choose a coefficient or propose it as UDT physics.

## 4. Acceptance gates

- No thin shell with an unhandled `delta^2` in `C^2`.
- No use of EH/GR junction equations.
- No assumption that reduced tangent variation supplies every full metric equation.
- No inference about nonspherical or time-live solutions from the spherical no-go.
- A selected radius must follow from existing premises, not from imposed matching data.
- If a new interface law is required, state the smallest information it must provide.

## 5. Possible verdicts

1. **UNIQUE SOURCE-FREE MATCH:** a regular stationary junction exists and fixes `R/X`.
2. **SOURCE-FREE MATCH IMPOSSIBLE:** the same bulk action cannot join the two phases smoothly.
3. **MATCH EXISTS BUT RADIUS MODULUS:** junction conditions hold for a continuous set of `R/X`.
4. **ALGEBRA/PROVENANCE UNRESOLVED:** variation or full-equation checks disagree.
