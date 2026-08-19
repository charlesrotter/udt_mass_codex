# G179 exact derivation — complete-coframe completed-pair extension

Date: 2026-08-19

## 1. Domain and premise boundary

Let a supplied smooth Lorentzian metric be represented at one event by any invertible coframe

\[
g=E^T\eta_4E,
\qquad
\eta_4=\operatorname{diag}(-1,1,1,1),
\]

and let a supplied ordered observer-pair germ have rank-two tangent matrix (J). The complete pair
coframe and pair metric are

\[
V=EJ,
\qquad
\boxed{h=J^TE^T\eta_4EJ=V^T\eta_4V}.
\]

The local regular stratum is

\[
h_{00}<0,
\qquad
\det h<0.
\]

The metric and germ are supplied. G179 does not select events, observers, or a global history. Its
only nonidentity physical premise is Charles's provisional `WORKING_FOUNDATIONAL_CLARIFICATION`:
Dual Reciprocity is applied to the completed observer-pair pullback after all metric channels have
entered.

## 2. The arbitrary-coframe theorem

Write the auxiliary pair metric in its unique positive shifted form,

\[
h_\sigma=-T^2(dy^0+\beta\,d\sigma)^2+L_\sigma^2d\sigma^2.
\]

Directly from the three entries of (h),

\[
T^2=-h_{00},
\qquad
\beta=\frac{h_{01}}{h_{00}},
\qquad
L_\sigma^2=h_{11}-\frac{h_{01}^2}{h_{00}},
\]

and

\[
T^2L_\sigma^2=-\det h.
\]

Let the physical ruler coordinate obey (ds=m,d\sigma), (m>0). Then

\[
T_s=T,
\qquad
L_s=\frac{L_\sigma}{m},
\qquad
\beta_s=\frac{\beta}{m}.
\]

Completed-pair Dual Reciprocity is (T_sL_s=1). Positivity gives one and only one solution:

\[
\boxed{m=T L_\sigma=\sqrt{-\det h}}.
\]

Consequently,

\[
\det h_s=-1,
\qquad
L_s=T^{-1},
\qquad
\boxed{\Phi=-\log T=-\frac12\log(-h_{00})}.
\]

No feature of this proof depends on a spherical chart, block-diagonal ambient metric, zero shift,
invertible base projection, static history, or scalar mixing coefficient. Once (h) is the full
pullback, no additional scalar remains.

The older arbitrary-calibration readout

\[
\phi_{\rm arbitrary}
=\frac14\log\frac{-\det h}{h_{00}^2}
\]

is a valid control on the supplied auxiliary ruler coordinate. It is not the completed physical
reciprocal kernel after (m) has been fixed. In completed coordinates (-\det h_s=1), so the same
triangular formula reduces exactly to (Phi=-\tfrac12\log(-h_{00})).

## 3. Explicit complete-coframe specialization

In the conditional complete (2+2) chart,

\[
E=
\begin{pmatrix}
B&0\\
QS&Q
\end{pmatrix},
\qquad
J=\begin{pmatrix}Y\\Z\end{pmatrix},
\]

where (B,Q\in GL(2,\mathbb R)) and (S,Y,Z\in\operatorname{Mat}(2,\mathbb R)). Direct
multiplication gives

\[
\boxed{
h=Y^TB^T\eta_2BY+(SY+Z)^TQ^TQ(SY+Z).
}
\]

This identity uses no (Y^{-1}). It retains:

- the clock/ruler block (B);
- nonspherical screen scale and shape (Q);
- all four base-to-screen mixing components in (S);
- both supplied pair-tangent blocks (Y,Z).

Every term enters before (T,L_\sigma,\beta,m,Phi) are read. The chart is an explicit diagnostic
of provenance; the arbitrary-coframe theorem itself requires only (E,J), not this block form.

## 4. Exact full-sector witnesses

The production witness is

\[
B=\begin{pmatrix}2&-2\\2&1\end{pmatrix},\quad
Q=\begin{pmatrix}1&2\\2&3\end{pmatrix},\quad
S=\begin{pmatrix}-1&1\\-1&-1\end{pmatrix},
\]

\[
Y=\begin{pmatrix}3&2\\-3&1\end{pmatrix},\quad
Z=\begin{pmatrix}1&-2\\2&-3\end{pmatrix}.
\]

All four (S) entries, nonspherical (Q), and (Z) are active. The exact pullback is

\[
h=\begin{pmatrix}-118&102\\102&822\end{pmatrix},
\qquad
\det h=-107400.
\]

Thus

\[
\beta=-\frac{51}{59},
\qquad
L_\sigma^2=\frac{53700}{59},
\qquad
m^2=107400,
\qquad
\Phi=-\frac12\log 118.
\]

The shift is not erased. It becomes (eta_s=\beta/m).

A second exact witness has

\[
Y=\begin{pmatrix}-8&0\\2&0\end{pmatrix},
\qquad
Z=\begin{pmatrix}-6&3\\-6&-6\end{pmatrix}.
\]

Here (det Y=0), while (operatorname{rank}J=2) and

\[
h=\begin{pmatrix}-124&-132\\-132&225\end{pmatrix},
\qquad
\det h=-45324.
\]

The theorem therefore does not hide the obsolete invertible-(Y) compression.

## 5. Where the orchestra is heard

At the generic full-sector witness, independent one-entry variations give:

| sector | varied entry | (d\Phi) | (d(m^2)) |
| --- | ---: | ---: | ---: |
| (B) | (0,0) | (-18/59) | (52120) |
| (Q) | (0,0) | (5/118) | (18312) |
| (S) | (0,0) | (-27/118) | (-27576) |
| (Y) | (0,0) | (5/118) | (26664) |
| (Z) | (0,0) | (-9/118) | (1944) |

So the completed scalar is not blind to the orchestra in a generic pair. The more precise rule is:

- any contribution changing (h_{00}) changes (Phi);
- contributions changing (h_{01}) or (h_{11}) change the physical ruler density and shift;
- a channel that is spatial-only for one special germ may move the tape without changing its
  endpoint depth on that germ;
- no additive angular score or scalar `mu` is attached afterward.

## 6. Covariance and reversal boundary

For a Lorentz coframe gauge change (E\mapsto\Lambda E),

\[
\Lambda^T\eta_4\Lambda=\eta_4
\quad\Longrightarrow\quad
h\mapsto h.
\]

For a matched ambient basis change (E\mapsto EK^{-1}), (J\mapsto KJ), the complete pair
coframe (EJ) and (h) are unchanged. The exact test uses a non-block transformed coframe, so the
result is not confined to the lower-block chart.

Under (sigma=k\widetilde\sigma),

\[
h_{01}\mapsto k h_{01},
\qquad
h_{11}\mapsto k^2h_{11},
\qquad
m\mapsto |k|m.
\]

The scalar is invariant. For (k<0), the directed ruler one-form and shift reverse orientation
while the positive density and determinant magnitude do not. This is spatial-coordinate reversal,
not observer-pair reversal. G170--G171 separately own the bounded same-pair endpoint-reversal
theorem.

## 7. Time-live scope

For any supplied smooth parameter family,

\[
\dot g=\dot E^T\eta_4E+E^T\eta_4\dot E,
\]

\[
\boxed{
\dot h
=\dot J^TgJ+J^T\dot gJ+J^Tg\dot J.
}
\]

The completed depth derivative is then

\[
\dot\Phi=-\frac12\frac{\dot h_{00}}{h_{00}}.
\]

This is exact query-live kinematics. It shows that time dependence of every supplied coframe and
pair-tangent channel is retained. It does not select those histories or create an evolution law.

## 8. Independent replay and mutation gates

The standalone standard-library verifier imports no production functions and passes 20,000 exact
`Fraction` witnesses. Every trial checks the block and direct pullbacks, shifted reconstruction,
unique reciprocal density, Lorentz-coframe gauge, matched ambient coordinate covariance, signed
auxiliary-ruler reparameterization, and live product rule.

Thirty mutation and semantic catches reject deletion of (Q,S,Z), scalarization of (S), freezing
of (Y), shift erasure, arclength substitution, arbitrary-calibration substitution, `X_max`, path,
transport, fit, source, action, matter, bootstrap, and observer-selection imports.

## 9. Landing and ceiling

The preregistered landing is

```text
GENERAL_COMPLETE_COFRAME_PULLBACK_EXTENDS_COMPLETED_PAIR_KERNEL_WITHOUT_EXTRA_SCALAR
```

Status: `DERIVED_CONDITIONAL__VERIFIED_WITH_CAVEATS_PENDING_FRESH_ADVERSARIAL_REVIEW`.

The theorem is local to supplied smooth regular rank-two completed pair germs and conditional on
the working completed-pair clarification. Event/germ realization, null and degenerate strata,
global completion, non-scalar transport, `X_max`, observations, radiative transfer, dynamics,
action, source, matter, mass, bootstrap, and signalling remain open or outside scope.
