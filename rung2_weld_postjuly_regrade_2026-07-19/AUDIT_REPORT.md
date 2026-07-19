# Rung-2 Phi–Angular Weld — Post-July Regrade and Rederivation

Date: 2026-07-19

Base: `d0b5d824432e1ac621d5e198e9ac490b265d2ea6`

Status: `VERIFIED-WITH-CAVEATS`; bounded CPU-only provenance/operator audit, not canonization

## Result first

The June-10 “rung-2 weld” was not one native UDT equation. It joined three different things under
one name:

1. a real **metric-derived mixed-curvature expression** in a chosen linearized spherical ansatz;
2. an **Einstein/source equation** obtained by setting that expression equal to
   `8 pi G T^t_theta`; and
3. a different **algebraic equation** obtained by varying a June-10 scalar action that is not in the
   current post-July C0/C1 action ledger.

The first survives as exact geometric bookkeeping within its declared ansatz. The second is an
imported GR comparison equation. The third is a correctly reproduced historical conditional, but
not a current native UDT equation. Neither relation forces a lightlike `d phi` branch or a uniquely
repeated Weyl principal null direction.

The maximum current conclusion is therefore:

> `RAW_MIXED_CURVATURE_OPERATOR_METRIC_DERIVED; DIFFERENTIAL_WELD_EINSTEIN_SOURCE_CONDITIONAL; DISTINCT_ALGEBRAIC_WELD_HISTORICAL_PRE_NATIVE_ACTION_CONDITIONAL; NO_CURRENT_NATIVE_RUNG2_SELECTOR_DERIVED`.

`CANON.md` was not edited. Entry `C-2026-06-10-3` remains historical canon text, but its description
of the weld as a “derived, CMB-data-tested dynamical phi-angular coupling” does not pass the current
July-1 provenance firewall. Charles alone decides whether and how to revise that entry.

## What was independently rederived

### 1. The linear metric operator

The historical reproduction tile uses

\[
ds_0^2=-f(r)dt^2+f(r)^{-1}dr^2+r^2d\Omega^2,
\qquad f=e^{-2\phi_0},
\]

and the even-parity first variation

\[
\delta g_{tt}=2f\,pY,\quad
\delta g_{rr}=2f^{-1}pY,\quad
\delta g_{tr}=H_1Y,\quad
\delta g_{AB}=r^2K Y\,\gamma_{AB},
\]

where `p=delta phi`. Starting from the connection definition and differentiating the inverse metric
analytically, the independent implementation obtains

\[
\boxed{
\delta G^t{}_{\theta}
=\frac{1}{f}
\left[-\frac12\partial_r(fH_1)+\partial_t p+\frac12\partial_tK\right]
\partial_{\theta}Y .}
\]

This exactly matches the historical code, including the sign and the `K_t/2` coefficient. That is a
**derived curvature component**, not a dynamical equation. The metric tells us how to calculate it;
the metric alone does not say it must vanish or equal a source.

Imposing the comparison equation

\[
\delta G^t{}_{\theta}=8\pi G\,\delta T^t{}_{\theta},
\qquad
\delta T^t{}_{\theta}=\tau\,\partial_\theta Y,
\]

gives

\[
\boxed{
\partial_r(fH_1)=2\partial_t p+\partial_tK-16\pi Gf\tau .}
\]

That second box is the historical differential weld. Its provenance is the Einstein equation plus a
stress/source choice. Setting `tau=0` removes a source term; it does not convert the equation into a
geometric identity or native UDT dynamics.

### 2. The separate algebraic equation

The June-10 implementation also used

\[
S_{\rm old}=-\frac{c_*}{2}\int
e^{-2\phi}g^{ab}\partial_a\phi\partial_b\phi\sqrt{-g}\,d^4x .
\]

An independent exact second variation reproduces its `H1` Euler–Lagrange expression:

\[
\frac{\delta S_{\rm old}^{(2)}}{\delta H_1}
=\frac{c_*}{2}r^2e^{-4\phi_0}\phi_0'
\left(\phi_0'H_1-2e^{2\phi_0}\partial_t p\right).
\]

For `phi0' != 0`, this gives the distinct algebraic relation

\[
\boxed{f\phi_0'H_1=2\partial_t p.}
\]

The algebra is valid **conditional on that functional**. Its old “native C1” label is not valid under
the current ledger: the action was introduced on June 10, its result is now explicitly bannered
pre-native/superseded, the current cold packet says C0/C1 supplies no action or field equation, and
the final native-action adjudication leaves the complete action and off-shell domain open. A later
file location cannot launder its date or premise.

### 3. The exact nonlinear angular interaction

To avoid mistaking the old linear harmonic tile for the whole geometry, the audit also retained two
independent transverse logarithmic scales in a local diagonal chart:

\[
g=\operatorname{diag}
\left(-e^{-2\Phi},e^{2\Phi},e^{2A},e^{2B}\right),
\qquad \Phi,A,B=\Phi,A,B(t,r,\theta).
\]

The exact metric calculation gives

\[
\begin{aligned}
G^t{}_{\theta}=-e^{2\Phi}\big(&A_tB_\theta+A_t\Phi_\theta
-B_tB_\theta-B_t\Phi_\theta-2\Phi_t\Phi_\theta\\
&-B_{t\theta}-\Phi_{t\theta}\big).
\end{aligned}
\]

This is useful: phi and the angular scales really do interact in the metric. But Reciprocity does
not make the expression vanish. For example,

\[
\Phi=t\theta,\qquad A=t^2+r\theta,\qquad B=tr+\theta^2
\]

gives a generically nonzero mixed component. A native action, variation rule, bootstrap feedback
law, or other independently derived selector would still be needed to turn the readout into an
equation. This diagonal calculation deliberately does not claim coverage of the full off-diagonal
metric space.

A geometric coupling is not a law setting the component to zero.

## Why the old `K=0` step does not survive

The historical program itself says its `K=0` result comes from extending a **static** areal/P0 chart
reading to `ell>=2` time-dependent perturbations. It correctly observes that removing `K` while
remaining in its restricted Regge–Wheeler form generates an omitted `g_{r theta}` component. That
shows the restricted chart is not closed under the transformation; it does not prove current UDT
forbids the angular degree of freedom.

The current cold packet says the transverse spatial block and full time-live geometry are
unselected, and the finite-cell static phi parity does not select other-field data. Accordingly this
audit keeps `K`, angular trace, and angular shear free. The old `K=0 FORCED` wording is regraded
`HISTORICAL_CHOICE_OVERSTATED_AS_FORCED`.

## Selector tests

### Null `d phi`

On `f=1`, `K=0`, and zero source, the differential equation is

\[
-\tfrac12H_{1,r}+p_t=0.
\]

All four causal classes of the **perturbation first jet** `dp` satisfy it:

| class | `p_t` | `p_r` | `H1_r` | `-p_t^2+p_r^2` |
|---|---:|---:|---:|---:|
| timelike | 1 | 0 | 2 | -1 |
| spacelike | 0 | 1 | 0 | +1 |
| null | 1 | 1 | 2 | 0 |
| zero | 0 | 0 | 0 | 0 |

The historical algebraic relation also fixes only `H1` relative to `p_t`; the same four perturbation
first-jet classes survive. These rows do not classify the total covector
`d(phi0+epsilon pY)`.

For an explicit total-gradient check, take the historical scalar-action vacuum background

\[
f=1+\frac{C}{r},\qquad \phi_0=-\frac12\log f,\qquad C>0,
\]

with `p=H1=K=tau=0`. It obeys the old background scalar equation
`E0=phi0''+2phi0'/r-2phi0'^2=0`; both weld residuals vanish; and

\[
g^{-1}(d\phi_0,d\phi_0)=f(\phi_0')^2
=\frac{C^2}{4r^3(C+r)}>0.
\]

Thus the total gradient is nonzero spacelike. The exact reciprocal Petrov-I profile below supplies a
second full-gradient spacelike witness while satisfying `G^t_theta=0`. Neither historical weld
selects the lightlike branch.

### One uniquely repeated PND

Use the exact reciprocal completion of a static `ell=2` member of the same broad metric family:

\[
ds^2=-e^{-2\Phi}dt^2+e^{2\Phi}dr^2+r^2d\Omega^2,
\qquad
\Phi=\frac{r}{20}(3\cos^2\theta-1).
\]

Static diagonality makes `G^t_theta=0` identically. At the regular exact point
`r=1`, `cos(theta)=1/sqrt(3)` (where `Phi=0`), the mixed electric-Weyl matrix is

\[
E^i{}_j=
\begin{pmatrix}
-1/75&-\sqrt2/20&0\\
-\sqrt2/20&-7/75&0\\
0&0&8/75
\end{pmatrix}.
\]

Its characteristic discriminant is

\[
\boxed{11913/1250000000\ne0},
\]

so all three electric-Weyl eigenvalues are distinct and the static purely electric spacetime is
Petrov I: four simple PNDs, no repeated one. This is an exact conditional comparison witness, not a
complete UDT universe. It is enough to refute the claimed implication from the mixed zero equation.
The independent generic Kasner comparison gives the same conclusion through a different family,
with PND-quartic discriminant
`1194393600/(13841287201 tau^12)`.

The witness is not a complete UDT universe.

## CSN, Reciprocity, and bootstrap

- **Reciprocity** supplies the determinant-one temporal/radial comparison block under its current
  readout premises. It supplies no derivative operator or field equation.
- **CSN** can give a trace Noether identity only after a specific exactly invariant action and
  variation domain are chosen. A trace identity is not the missing mixed equation.
- **Bootstrap** currently constrains admissible complete global solutions. It supplies no local
  source, feedback functional, or `t-theta` Euler–Lagrange equation.

Therefore the old weld does not close the selector seam identified by the preceding July-19 audit.
It makes the seam sharper: exact metric geometry contains phi–angular coupling, while the rule that
would select one realization of that coupling is still absent.

## CMB and observational language

The old CMB discriminator may be mined as historical comparison or failure evidence only. Its
blackbody, transfer/projection, source, and Einstein-constraint layers predate the native field
equations and are explicitly bannered superseded. Even perfect observational agreement would show
compatibility of the conditional pipeline, not derive the governing operator. No CMB calculation
was rerun here.

In short, observational agreement would show compatibility, not derivation.

## Four evidence gates

1. **Preregistered:** yes, commit `70f74fa`; candidate families, premises, pass conditions, and
   maximum claims were frozen before detailed derivation.
2. **Full space or bounded scope justified:** bounded and explicit. The named historical ansatz,
   exact diagonal angular comparison, causal implication, and one exact in-family Petrov witness are
   covered. The full ten-component nonlinear metric and complete action space are not.
3. **Independently verified on the load-bearing premise:** yes. A fresh read-only reviewer used
   direct full-epsilon curvature and an independent static-lapse/3+1 Weyl calculation, reproduced
   both load-bearing results, and identified two evidence/wording corrections that were applied.
   See `EXTERNAL_ADVERSARIAL_REVIEW.md`.
4. **Every premise audited:** yes for this bounded tile; see `WELD_OBJECT_LEDGER.tsv` and
   `SOURCE_INVENTORY.tsv`.

## Honest scientific status

- reciprocal UDT kinematics: unchanged, `DERIVED` with its readout premises;
- raw rung-2 mixed-curvature operator: `DERIVED_WITHIN_LINEARIZED_HISTORICAL_ANSATZ`;
- differential rung-2 equation: `IMPORTED_EINSTEIN_SOURCE_EQUATION`;
- algebraic rung-2 equation: `HISTORICAL_PRE_NATIVE_ACTION_CONDITIONAL`;
- `K=0`: `HISTORICAL_CHOICE_OVERSTATED_AS_FORCED`;
- current native phi-angular selector: `NOT_DERIVED_FROM_AUDITED_SOURCE_SET`;
- null branch and unique repeated PND from either old weld: `REFUTED_WITHIN_TESTED_TILES`;
- complete native action, source, variation domain, boundary completion, and bootstrap bridge:
  `OPEN`.

## Stop line

This package regrades one historical operator family. It does not edit `CANON.md` or startup
controls, adopt an action or carrier, launch a time-live solve, derive a complete bootstrap bridge,
run GPU work, continue cosmology, or reorganize the repository.
