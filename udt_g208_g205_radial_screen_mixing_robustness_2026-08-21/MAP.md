# G208 map — G205 radial-screen mixing robustness

Date: 2026-08-21

## Whole question

Starting from any exact G205 metric

\[
g_0=-f(r)dt^2+h_0,
\qquad
h_0=\frac{dr^2}{f}+r^2d\Omega^2,
\]

turn on the smallest spatial instrument not covered by G207: a smooth `h0`-self-adjoint
endomorphism `C` which is purely off-diagonal between the radial line and angular screen. On
`r>0`, with `e_r` the `h0`-unit radial vector and `W` a screen vector,

\[
C(v)=h_0(W,v)e_r+h_0(e_r,v)W.
\]

Require the tensor, rather than a normalized screen frame, to extend smoothly through the
Cartesian center. Put

\[
A=e^C,
\qquad
h_C(v,w)=h_0(Av,Aw),
\qquad
g_C=-fdt^2+h_C.
\]

Classify what signature, volume, radial causality, global hyperbolicity, null-affine completeness,
and completed-pair response follow for this supplied mixing class.

## Dependency decision

The combined common-scale/screen case does not need to precede this tile. For every already
supplied spatial deformation `A` and smooth real `Omega`,

\[
\widehat g=e^{2\Omega}g_A
\]

has the same unparametrized null paths as `g_A`, affine density
`d lambda_hat=e^(2 Omega)d lambda_A`, pair pullback `h_hat=e^(2 omega)h_A`, and completed depth
`Phi_hat=Phi_A-omega`, where `omega=Omega composed F`. Common scale therefore composes exactly
with G207; it creates no order ambiguity. This is a composition lemma, not a selected combined
history.

## Frame

- **Metric-led:** `C` enters the spatial metric before any observer-pair pullback or scalar readout.
- **Observing, not targeting:** retain both globally complete and incomplete strata.
- **Whole declared mixing tile:** exact local algebra for every smooth pure radial-screen mixer;
  global survivor and failure theorems carry their explicit growth hypotheses.
- **No physical selector:** `C`, its screen direction, amplitude, and profiles are controls, never
  promoted to the physical UDT history.

## Premise ledger

| Item | Provenance | Role |
|---|---|---|
| G205 `g0,f,h0` | `DERIVED_CONDITIONAL` | supplied complete base |
| radial/screen split on `r>0` | `PINNED_BY_DECLARED_G205_REALIZATION` | mixing type |
| smooth tensorial center extension | `PINNED_BY_REGULARITY` | retain declared manifold |
| `C*=C` and pure radial-screen off-diagonal form | `CHOSE_EXTENSION_CLASS` | one configuration-space tile |
| `A=exp(C)` | `DERIVED_FROM_CLASS` | positive determinant-one spatial map |
| profiles and axis used in witnesses | `CHOSE_CONTROLS` | survivor/failure demonstrations only |
| Levi-Civita, optical metric, Hopf-Rinow | `STANDARD_GEOMETRIC_EVALUATOR` | causal/affine classification |
| completed-pair Dual Reciprocity | `WORKING_FOUNDATIONAL_CLARIFICATION` | scalar only after full pullback |
| action/source/transfer/observations/`X_max` | `OMITTED_OPEN` | forbidden inputs |

## Omitted scope

Trace-changing spatial modes, time-space shift, arbitrary full spatial endomorphisms, timelike and
spacelike completeness, field/history equations, physical observer population, maximal extension,
transfer, observations, matter, and `X_max` remain outside this one tile.

## Maximum conclusion

At most: a conditional tensorial classification of the supplied pure radial-screen mixing class,
including exact growth-controlled survivor and smooth failure strata and its completed-pair
response. No physical mixer, direction, amplitude, profile, parameter, history, or `X_max` may be
selected.
