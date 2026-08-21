# G207 map — G205 trace-free screen time-live robustness

Date: 2026-08-21

## Whole question

Starting from any exact G205 metric

\[
g_0=-f(r)dt^2+h_0,
\qquad
h_0=\frac{dr^2}{f}+r^2d\Omega^2,
\]

turn on the smallest nonconformal angular instrument. On `r>0`, let `S` be a smooth
`h0`-self-adjoint endomorphism that annihilates the radial direction and is trace-free on the
two-dimensional spherical screen. Require `S` to extend smoothly through the Cartesian center.
Put

\[
A=e^S,
\qquad
h_S(v,w)=h_0(Av,Aw),
\qquad
g_S=-fdt^2+h_S.
\]

Classify exactly what signature, volume, causal/global, null-affine, and completed-pair properties
follow from this supplied deformation class.

## Frame

- **Metric-led:** `S` changes the complete metric before any pair pullback or scalar readout.
- **Observing, not targeting:** classify static, compact-time-live, and unrestricted smooth
  time-live screen shears, including explicit survivor and failure strata.
- **One tile:** common conformal scale is held at its G205 value; radial-screen mixing and shift are
  omitted rather than silently frozen into a universal claim.
- **No physical selector:** `S` and its witness axis/profile are `FREE_AND_EXPLORED` or
  `CHOSE_CONTROL`, never promoted to the UDT history.

## Exact premise ledger

| Item | Provenance | Role |
|---|---|---|
| G205 `g0,f,h0` | `DERIVED_CONDITIONAL` | supplied complete base |
| radial/spherical screen on `r>0` | `PINNED_BY_DECLARED_G205_REALIZATION` | screen type |
| smooth center extension of `S` | `PINNED_BY_REGULARITY` | retain declared manifold |
| `S*=S`, `S radial=0`, `tr_screen S=0` | `CHOSE_EXTENSION_CLASS` | pure trace-free screen shear |
| `A=exp(S)` | `DERIVED_FROM_CLASS` | positive determinant-one screen map |
| completed-pair Dual Reciprocity | `WORKING_FOUNDATIONAL_CLARIFICATION` | terminal scalar after pullback |
| axis/time profiles in witnesses | `CHOSE_CONTROLS` | coexistence and counterexample only |
| circular-null radius in failure witness | `DERIVED_CONDITIONAL_FROM_G205_SUPERCRITICAL_STRATUM` | exact test orbit |
| action/source/transfer/observations/`X_max` | `OMITTED_OPEN` | forbidden inputs |

## Maximum conclusion

At most: a conditional tensorial theorem for the supplied pure-screen deformation class, with exact
global-causal, null-affine, ambient-volume, and completed-pair strata. No physical `S`, axis,
amplitude, profile, parameter, history, transfer rule, or `X_max` may be selected.
