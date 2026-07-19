# Metric-wide Cartan/Holonomy Audit

Date: 2026-07-19

Base: `ec24c135212d3121e2d5903a29ec669f0b8a982a`

Status: `VERIFIED-WITH-CAVEATS`; preregistered bounded CPU-only metric audit, not canonization

## Result first

The zoomed-out idea was worth testing. Cartan geometry is the cleanest native language yet found for
holding the reciprocal and angular sectors of the UDT metric in one object. Once a nondegenerate
metric representative is supplied, its torsion-free metric-compatible connection, curvature, and
infinitesimal holonomy are derived from that metric. They are not imported GR field equations.

But the audit finds a sharp limit:

> **Cartan geometry faithfully describes a chosen metric's local curvature and transport; it does not choose which complete metric the universe realizes.**

Three exact results make that distinction load-bearing:

1. A full transverse twist comparison family has identical chosen endpoint jets but continuously
   different interior curvature and local loop transport, while satisfying the Cartan and Bianchi
   identities exactly. Thus the identities plus those equal boundary data do not select the
   interior. Current UDT supplies no stronger transverse-twist boundary law.
2. In the historical *chosen single-axis metric* candidate, a rank-one angular texture has vanishing
   pullback area form but nonzero Weyl-squared curvature. The proposed shortcut from metric `C^2` to
   an area-only `F^2` carrier functional is therefore false in this tested class.
3. `C^2` and EH do share one Cartan-curvature origin, but they use different contractions and have
   different scale weights, variation domains, and boundary problems. Common origin is not a derived
   two-stage bridge.

The audit does **not** derive matter from holonomy, a native phi-angular equation, a lightlike phi
branch, a uniquely repeated curvature direction, or a complete action. For the holonomy/bridge route,
it identifies one candidate open gate more precisely: a global metric admissibility, reduction, or
soldering rule that includes variation and boundary content. That is a route-scoped description,
not a claim of uniqueness and not a new postulate.

## Lay picture

Think of the metric as a fabric containing both clock/ruler dilation and angular orientation. Cartan's
method tells us how a tiny measuring frame turns when carried through that fabric. Curvature is the
failure to return unchanged around a tiny loop; holonomy is the accumulated turn around a finite
loop.

That is exactly the right bookkeeping for the hunch that matter might be a persistent global twist
of the geometry. The difficulty is that *every* curved geometry has some such turning. Merely naming
the turn does not tell us which turns are physical particles, which whole-universe geometry is
allowed, or why one global pattern is selected. For this route, another local connection is not the
missing piece: the metric already supplies it. A still-missing piece is a rule that distinguishes an
admissible, self-closing global pattern from other geometries.

This makes the problem simpler, but not closed. It redirects work away from random local equations
or GPU grinding and toward the global selection/variation/boundary seam.

## Whole metric map

For a local `2+2` split, the audit retains

\[
 ds^2=g_{ij}(x,y)dx^idx^j+
 q_{AB}(x,y)\bigl(dy^A+A^A{}_i dx^i\bigr)
                  \bigl(dy^B+A^B{}_j dx^j\bigr).
\]

The reciprocal temporal/radial realization can live in `g_ij`. The positive transverse block
`q_AB` carries its own area, shear, and zweibein rotation. The shifts `A^A_i` carry non-integrable
twist. The resulting Cartan curvature contains base curvature, transverse curvature, mixed
derivatives, shear/expansion, twist curvature, and algebraic cross terms.

No current UDT premise sets `A^A_i=0`, diagonalizes `q_AB`, removes transverse shear, or makes the
screen integrable. Those are useful comparison subfamilies, not consequences. This is why the audit
does not repeat the earlier error of setting an angular sector to zero before asking how it interacts
with phi.

## What the Cartan equations do and do not say

For an orthonormal coframe `e^I`, the torsion-free Levi-Civita connection obeys

\[
 T^I=de^I+\omega^I{}_J\wedge e^J=0,
 \qquad
 \Omega^I{}_J=d\omega^I{}_J+
 \omega^I{}_K\wedge\omega^K{}_J.
\]

The Bianchi identities are

\[
 \Omega^I{}_J\wedge e^J=0,
 \qquad D\Omega^I{}_J=0.
\]

These statements are `DERIVED_PER_REPRESENTATIVE`. They determine how connection and curvature are
computed from a supplied metric. They are identities, not Euler--Lagrange equations: they do not set
the Ricci tensor, Weyl tensor, Bach tensor, or any source expression to a prescribed value.

A local Lorentz rotation changes coframe and connection components while leaving the metric and
curvature/holonomy conjugacy class invariant. Consequently a component-level angular direction is
not physical until a gauge-invariant global reduction or section has been selected.

## Exact chosen-boundary-equal twist counterfamily

The exact comparison coframe is

\[
 e^0=dt,\quad e^1=dr,\quad e^2=dx,\quad
 e^3=dy+u(r)dx,
\]

with `q=u_r`. Its nonzero connection forms are

\[
 \omega_{12}=-\frac q2e^3,\qquad
 \omega_{13}=-\frac q2e^2,\qquad
 \omega_{23}= \frac q2e^1.
\]

Direct exterior algebra gives

\[
\begin{aligned}
 \Omega_{12}&=-\frac{3q^2}{4}e^1\wedge e^2
              -\frac{q'}2e^1\wedge e^3,\\
 \Omega_{13}&=-\frac{q'}2e^1\wedge e^2
              +\frac{q^2}{4}e^1\wedge e^3,\\
 \Omega_{23}&= \frac{q^2}{4}e^2\wedge e^3.
\end{aligned}
\]

Torsion, first Bianchi, and second Bianchi all vanish exactly while these curvature forms need not.
Choose the finite-cell bump

\[
 u_\lambda(r)=\lambda(1-r^2)^3,\qquad -1\le r\le1.
\]

Every member has `u=q=q'=0` at both boundaries. The `lambda=0` member is flat. At
`r=1/2, lambda=1`, however,

\[
 q=-\frac{27}{16},\qquad q'=\frac98,
\]

so the curvature and infinitesimal local loop transport are nonzero. This is an exact family, not a
linearized perturbation. It proves that Cartan identities plus the chosen equal endpoint jets do not
determine the interior twist or local transport. Current UDT registers limited phi seal data and no
stronger transverse-twist endpoint law, but these tiles are not complete-bootstrap solution
countermodels. The tile sets `phi=0` only to isolate transverse freedom. Embedding the same twist in
a fixed nontrivial reciprocal coframe changes the connection and curvature and was not calculated
here.

## Holonomy does not yet equal matter

Even before dynamics, holonomy fixed sets are not generically unique. An identity rotation fixes all
three directions; a single nontrivial spatial rotation fixes one axis; two rotations about
nonparallel axes have no common nonzero fixed direction. A one-dimensional fixed set therefore
signals a special reduction, not a generic consequence of having holonomy.

To turn “matter is holonomy” into a derivation would require, at minimum:

- the selected global bundle/sector and topology;
- a gauge-invariant object that identifies the matter degree of freedom;
- a functional or complete-solution rule selecting it;
- a native source/coupling interpretation;
- boundary completion and a stability statement.

Current C0/C1, Reciprocity, CSN, and bootstrap do not yet supply that chain. The July-15 reciprocal
loop document suggested the hypothesis, but it grades itself provisional/unbanked with independent
verification open. It supplies a candidate and test target, not controlling current authority. The
preregistration's mistaken pre-July classification is preserved and corrected explicitly in
`PREREGISTRATION_CORRECTION.md`.

## Exact challenge to the single-axis `F^2` shortcut

The historical candidate chose a spatial single-axis metric

\[
 h=I+(a-1)n\otimes n,\qquad a=e^{2\phi}.
\]

This is not derived by the current foundation; it is retained only as a stringent comparison. Take

\[
 n=(\cos x,\sin x,0)
\]

and form the direct product of its two-dimensional `(x,y)` metric with flat constant time and a flat
third spatial direction. At `x=0, a=4`, direct Christoffel/Riemann calculation gives

\[
 K=-\frac34,\qquad R=-\frac32,\qquad
 C_{abcd}C^{abcd}=\frac34.
\]

But `n` varies in only one coordinate, so

\[
 F_{xy}=n\cdot(\partial_xn\times\partial_yn)=0.
\]

Thus `F^2=0` while metric `C^2` is nonzero. The metric is invariant under `n -> -n`, so the result is
not a sign-lift artifact. It disappears at `a=1`, confirming that the curvature is the anisotropic
axis cost. The conclusion is bounded but decisive: within this chosen metric, `C^2` contains
rank-one orientation-gradient curvature density not captured by the area-only form. The two
functionals cannot be identified generally. No global numerical ordering is claimed.

This does not rule out every possible geometric carrier functional. It rules out the tested elegant
shortcut.

## `C^2`, EH, and the possible two-stage bridge

Both conditional actions are made from the curvature just derived from the metric, so their common
geometric origin is real. In four dimensions, however, under a constant common rescaling
`g -> s^2 g`,

\[
 \sqrt{|g|}\,C^2\longrightarrow \sqrt{|g|}\,C^2,
 \qquad
 \sqrt{|g|}\,R\longrightarrow s^2\sqrt{|g|}\,R.
\]

The pre-scale `C^2` route is `UNIQUE-CONDITIONAL` under its locality/covariance/fourth-order and
variation-before-scale premises. The post-scale EH route is `CONDITIONAL` after a physical metric
representative is selected and the minimal second-order premise is adopted. They also require
different variation and boundary completions. No Cartan or Bianchi identity maps the Bach equation
to the Einstein equation.

A two-stage story remains logically possible: a conformal/pre-scale stage could select a physical
representative, followed by a post-scale stage. What remains absent is the native rule that performs
that selection and shows that the second variational problem follows from the first. Calling both
stages “curvature” does not supply the bridge.

## Adjudication of the armchair lead

The lead was productive, but it does not justify another narrowing chase yet.

- `DERIVED_PER_REPRESENTATIVE`: Levi-Civita connection, curvature, Cartan identities, infinitesimal
  holonomy.
- `DERIVED_GEOMETRY`: reciprocal, transverse, shear, twist, and mixed sectors all interact in the
  full curvature.
- `UNDERDETERMINED`: the holonomy/reduction selected by current finite-cell and bootstrap premises.
- `REFUTED_IN_TESTED_CLASS`: the conditional single-axis metric `C^2 = area-only F^2` shortcut.
- `OPEN`: metric holonomy as matter, the native phi-angular law, complete action/source/boundary,
  and the `C^2`-to-EH bridge.

The clean next question is not “which local component should be zero?” It is whether current UDT has
an unrecognized **global admissibility condition**—expressible solely in metric, finite-cell,
Reciprocity, CSN, and bootstrap data—that selects a holonomy reduction or a physical representative
and comes with a legitimate variation/boundary domain. This audit did not find such a condition.

GPU mapping is not indicated by this result. Sampling more local geometries would exhibit more
holonomies but would not provide the missing selection rule. A future numerical solve becomes useful
only after a specific global functional or admissibility equation is derived and preregistered.

## Scope and four evidence gates

1. **Preregistered:** yes; commit `98a7c31` predates derivation output.
2. **Full space or bounded scope justified:** bounded exact sector map plus two exact countertiles;
   not a classification of all four-metrics or all global holonomy groups.
3. **Independently verified:** independent coordinate-basis recomputation and fresh adversarial review
   are recorded in this package.
4. **Every premise audited:** yes in `CARTAN_SECTOR_LEDGER.tsv`; open/conditional choices remain
   explicit.

Accordingly the package is `VERIFIED-WITH-CAVEATS`, not `PROVED`, `SETTLED`, `CANON`, or a complete
UDT action result.
