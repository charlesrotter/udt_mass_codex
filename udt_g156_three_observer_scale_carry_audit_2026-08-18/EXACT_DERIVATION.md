# G156 exact derivation — the pair metric owns a half-density; a supplied carry owns its character

## 1. The intrinsic common-scale carrier

Let \(V_i\) be the oriented two-dimensional carrier of one supplied regular calibrated pair metric

\[
h_i=-T_i^2(dy_i^0+\beta_i dy_i^1)^2+L_i^2(dy_i^1)^2,
\qquad T_i,L_i>0.
\]

Every such carrier has the one-dimensional half-density vector line

\[
\mathcal L_i=|\Lambda^2V_i^*|^{1/2}
\]

and its positive ray \(\mathcal L_i^+\). The line belongs to the typed pair plane; the metric
supplies its canonical section in that positive ray,

\[
\ell_i=\nu_{h_i}^{1/2}
=(-\det h_i)^{1/4}|dy_i^0\wedge dy_i^1|^{1/2}
=\sqrt{T_iL_i}\,|dy_i^0\wedge dy_i^1|^{1/2}.
\]

Since \(T_iL_i=e^{2\kappa_i}\), its coefficient in the calibrated chart is \(e^{\kappa_i}\).
This is the exact geometric home of the local common-scale readout.

Under an orientation-preserving reparameterization with Jacobian \(J\),

\[
h_i'=J^Th_iJ,
\qquad
-\det h_i'=(\det J)^2(-\det h_i).
\]

Therefore the coefficient transforms by \((\det J)^{1/2}\), exactly as a half-density. The section
\(\ell_i\) is intrinsic, while the displayed coefficient \(e^{\kappa_i}\), and hence \(\kappa_i\)
itself, depends on the chosen density trivialization. This does not make common scale gauge: two
different metric sections are still different supplied metric data.

## 2. The scale character of a typed comparison

Let

\[
R_i=\begin{pmatrix}T_i&T_i\beta_i\\0&L_i\end{pmatrix}:V_i\to W
\]

be the positive triangular terminal factor, and let
\(M_{BA}:V_A\to V_B\) be a supplied orientation-preserving physical or query carry. The fully typed
model-space comparison is the G142 transition

\[
C_{BA}=R_BM_{BA}R_A^{-1}.
\]

Its common-scale character is

\[
\boxed{
\sigma_{BA}=\frac12\log|\det C_{BA}|
=\kappa_B-\kappa_A+\frac12\log|\det M_{BA}|.
}
\]

Equivalently, the pullback of the metric half-density satisfies

\[
\boxed{M_{BA}^*\ell_B=e^{\sigma_{BA}}\ell_A.}
\]

This equation is coordinate-natural and makes no reference to an external volume postulate.

Under independent endpoint carrier gauges

\[
R_i'=R_iP_i,
\qquad
M_{BA}'=P_B^{-1}M_{BA}P_A,
\]

the total transition is unchanged:

\[
C_{BA}'=C_{BA}.
\]

Consequently \(\sigma_{BA}\) is invariant even though the endpoint coefficients \(\kappa_i\) and
the determinant grading of \(M_{BA}\) separately move between the endpoint factors and the carry.
The invariant object is the complete joined comparison.

## 3. Three-observer composition

For \(A\to B\to C\), define

\[
\Omega^{\rm sc}_{ABC}
=\sigma_{BA}+\sigma_{CB}-\sigma_{CA}.
\]

The endpoint metric factors cancel exactly:

\[
\boxed{
\Omega^{\rm sc}_{ABC}
=\frac12\log\left|
\det\bigl(M_{CB}M_{BA}M_{CA}^{-1}\bigr)
\right|.
}
\]

Thus the scale defect does **not** test the local values of \(\kappa_A,\kappa_B,\kappa_C\). It tests
the determinant part of the carry triangle.

If the full carries compose,

\[
M_{CB}M_{BA}=M_{CA},
\]

then

\[
C_{CB}C_{BA}=C_{CA},
\qquad
\Omega^{\rm sc}_{ABC}=0.
\]

The converse is false. With

\[
M_{BA}=M_{CB}=I,
\qquad
M_{CA}=\begin{pmatrix}1&1\\0&1\end{pmatrix},
\]

the scalar scale defect vanishes because all determinants equal one, but the matrix carry triangle
does not close. In the declared positive-triangular arena, the scale character has kernel
\(B^+(2)\cap SL(2)\); reciprocal and shear information can remain there. No broader
\(GL^+(2)\) classification is needed for this result.

This is the main three-observer classification: scale closure is necessary under full carry closure,
but it is strictly weaker than closure of the complete observer comparison.

## 4. Which existing regimes own flat scale carry?

### One supplied calibrated query chart

If one chart spans the three parameter points, its identity presentation owns the carry. After a
rechart with endpoint Jacobians \(J_i\),

\[
M_{BA}=J_BJ_A^{-1},
\qquad
(J_CJ_B^{-1})(J_BJ_A^{-1})=J_CJ_A^{-1}.
\]

The scale character is endpoint-exact and every chart loop has zero scale defect. This is a
presentation theorem, not a physical force.

### Genuine cross-query overlap

When two pair realizations are proved to be charts of the same relation patch, the overlap
differential supplies the carry. Pullback naturality makes the total transition Lorentz isometric.
It therefore has \(|\det C|=1\), so \(\sigma=0\). In the positive triangular gauge the total overlap
transition is exactly the identity.

Shared endpoint observers without an open relation overlap do not supply such a differential.

### Levi-Civita transport

The pair metric's Levi-Civita connection satisfies

\[
\nabla^{h}\nu_h=0,
\qquad
\nabla^{h}\ell_h=0.
\]

Its parallel transport is isometric and therefore has zero determinant scale character relative to
the endpoint metric half-densities. It may retain Lorentz or path holonomy, but it cannot manufacture
a nonisometric common-scale response.

### A supplied nonisometric carry triangle

Independently supplied physical/query carries can have a nonzero determinant triangle defect. For
example, if
the composite route carries are identity but the direct supplied carry is
\(M_{CA}=\operatorname{diag}(2,1)\), then

\[
\exp(2\Omega^{\rm sc}_{ABC})=\frac12,
\qquad
\Omega^{\rm sc}_{ABC}=-\frac12\log2.
\]

This is an algebraic admissible witness, not holonomy unless a path/loop functor is separately
declared, and not evidence that the metric selects that carry.

## 5. Landing

The preregistered outcome class is

`CONDITIONAL_FLAT_SCALE_CARRY`.

The primary qualified landing is:

`PAIR_METRIC_CANONICALLY_SUPPLIES_POSITIVE_HALF_DENSITY_SECTION__ANY_SUPPLIED_TYPED_CARRY_INDUCES_GAUGE_INVARIANT_LOG_DETERMINANT_CHARACTER__FULL_CLOSURE_IMPLIES_BUT_IS_NOT_IMPLIED_BY_SCALE_CLOSURE__OWNED_CHART_OVERLAP_AND_LEVI_CIVITA_CARRIES_ARE_SCALE_FLAT__ARBITRARY_SUPPLIED_NONISOMETRIC_CARRIES_NEED_NOT_BE_FLAT__NO_METRIC_OWNED_CROSS_QUERY_CARRY_OR_KAPPA_HISTORY`.

G156 therefore resolves the carrier question raised by G155: no additional local scale line has to
be invented. What remains open is not the existence of the carrier or its scalar character. It is
which nonisometric relations, if any, Nature realizes between otherwise unglued query sheets, and
what nonidentity law restricts or evolves the metric section \(\ell_h\), equivalently the common-scale
history represented locally by \(\kappa\).

No action, history selector, observational law, \(X_{\max}\) value, or canonization follows.
