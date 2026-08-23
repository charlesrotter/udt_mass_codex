# G235 exact derivation — rank-complete matched-network nonselection

Date: 2026-08-23

## Landing

```text
RANK_COMPLETE_MATCHED_COMPLETION_IS_RECONSTRUCTIVE_NOT_SELECTIVE
__EXISTENCE_CONDITION_ACCEPTS_G233_INVARIANT_TWINS
__NO_CANDIDATE
```

This is a bounded negative for the exact G234 candidate tested here. It is not a no-go for a
different genuinely global UDT relation law.

## 1. The quantified condition

The tested condition is

\[
P_{\rm net}[g]:
\quad
\exists\,\mathscr N
\text{ smooth, compatible, rank-complete, incidence-matched, and G176-completed over }g.
\]

It must not be silently replaced by the stronger statement that every conceivable observer germ
is physically populated or that all independently calibrated timelike directions share one
endpoint scalar. Current UDT does not own those quantifiers.

## 2. Rank completeness with one common clock

At one regular event choose a common timelike clock vector `e0` and a spatial basis
`e1,e2,e3`. Use ruler directions

\[
e_1,\ e_2,\ e_3,\ e_1+e_2,\ e_1+e_3,\ e_2+e_3.
\]

Each clock--ruler plane returns

\[
g(e_0,e_0),\qquad g(e_0,v),\qquad g(v,v).
\]

The first three directions give `g00`, all `g0i`, and all `gii`. The sum directions give

\[
g_{ij}=\frac12\{g(e_i+e_j,e_i+e_j)-g_{ii}-g_{jj}\}.
\]

Thus the restriction design has rank ten. The exact production and independent implementations
recover rank `10`; deleting one sum direction drops it to `9`. Sharing one clock vector therefore
does not prevent full metric reconstruction.

This is a sufficiency construction. It does not declare these six planes to be Nature's preferred
observer population.

## 3. Completed reciprocity is fiberwise

For any one regular pullback

\[
h_\sigma=
\begin{pmatrix}
-T^2&-T^2\beta\\
-T^2\beta&L_\sigma^2-T^2\beta^2
\end{pmatrix},
\]

G176 gives

\[
m=T L_\sigma=\sqrt{-\det h_\sigma},
\qquad
h_s=J^{-T}h_\sigma J^{-1},
\qquad
J=\operatorname{diag}(1,m).
\]

Then

\[
\det h_s=-1,
\qquad
h_\sigma=J^T h_s J,
\qquad
\Phi=-\log T=-\frac12\log(-h_{00}).
\]

The tuple `(m,h_s)` is therefore exactly reconstructive. The normalization creates no equation
between pullbacks at different events.

## 4. Matched incidence supplies an arbitrary endpoint potential

When all pair germs incident at an event use the same calibrated clock vector `U`, their clock
entry is the same:

\[
(h_a)_{00}=g(U,U).
\]

Hence every incident completed pair has

\[
\Phi_a(p)=-\frac12\log[-g(U,U)]\equiv\Phi(p),
\]

independently of its ruler direction. Explicit incidence matching then gives

\[
\delta_{pq}=\Phi(q)-\Phi(p).
\]

Consequently,

\[
\delta_{qp}=-\delta_{pq},
\qquad
\delta_{pq}+\delta_{qr}=\delta_{pr}.
\]

Every smooth function `Phi` satisfies these equations. Corrupting one edge by an additive unit
breaks the executable composition check, so the positive test is not vacuous. Composition reduces
edge values to a vertex potential but does not determine the potential.

## 5. Smooth covered primary-network construction

On a regular static-spherical annular region use the primary metric

\[
g_\phi=-e^{-2\phi(r)}dt^2+e^{2\phi(r)}dr^2+r^2d\Omega^2.
\]

Take the global static clock \(U=\partial_t\). In each regular spatial coordinate chart, use the six
coordinate ruler combinations above. The clock commutes with the spatial coordinate fields, so
their local clock--ruler surfaces are regular integral surfaces. Multiple angular charts cover the
sphere, and G214 transports their supplied completed tuples on overlaps.

For every ruler `v`, the pullback is time-orthogonal with

\[
h_{00}=-e^{-2\phi},
\qquad
h_{11}=g(v,v)>0.
\]

Completion gives

\[
m_v^2=e^{-2\phi}g(v,v),
\qquad
(h_{s,v})_{11}=e^{2\phi},
\qquad
\det h_{s,v}=-1,
\qquad
\Phi=\phi.
\]

Thus every smooth primary profile on the regular annulus admits the tested completed, matched,
rank-complete network. Angular geometry enters each density `m_v`; it has not been deleted or added
after readout.

## 6. Preregistered invariant twins

Set

\[
s=(r-3)/3,
\qquad
\phi_b=s^3+2s^4+b s^5.
\]

The `b=0` and `b=7` metrics are smooth and Lorentzian on the declared annulus. At `r=3` their
profile derivatives through order four agree, while

\[
\Delta\phi^{(5)}=840.
\]

G233 supplies the coordinate-independent separator

\[
\Delta[(\nabla^3\mathcal R)(n,n,n)]
=\frac{240\Delta b}{r_0^5}
=\frac{560}{81}.
\]

They are therefore invariantly distinct. Nevertheless, the production derivation constructs all
six completed primary pair types separately for each profile and verifies rank, determinant,
reconstruction, matched composition, and reversal for both. The independent exact replay reaches
the same result over 5,000 rational trials and 540,005 assertions after the externally
preregistered profile-by-profile completion strengthening.

The candidate does not reject its preregistered control.

## 7. Why each ingredient is nonselective

| Ingredient | What it does | Why it does not cut the profile |
|---|---|---|
| Rank ten | reconstructs all metric components | rank depends on the query design, not their values |
| G176 completion | normalizes each supplied pair | it is an invertible change of variables when `m` is retained |
| Matched incidence | identifies one endpoint calibration | every smooth endpoint potential is allowed |
| Reversal/composition | makes edge depth exact | exactness does not determine the potential |
| G214 overlap | transports supplied tuples | it preserves rather than generates values |
| Global covered existence | supplies one coherent network | both invariantly distinct twins possess one |

The full combination is therefore reconstructive and compositional but remains an identity on the
declared supplied-metric arena.

G214 also blocks one apparent escape: completed pair metrics on distinct `AB`, `BC`, and `AC`
surfaces are not typed linear arrows and have no native matrix product. Demanding a path-independent
full-tuple product would require a newly defined cross-pair transport and incidence law. It is not
content already hidden in completed Dual Reciprocity.

## 8. The stronger statement not tested

Demanding equality across all independently calibrated timelike germs, prescribed holonomy,
all-germ curvature isotropy, or another cross-sector global invariant could be nonidentity. Those
are additional conditions. G212 already shows that full all-germ two-jet isotropy forces a
space-form only conditionally and is not UDT-owned.

The negative result cannot be evaded by silently strengthening `exists one matched rank-complete
network` into an unowned universal population premise.

## Maximum conclusion

The literal completed-pair/matched-incidence/rank-complete existence candidate fails the G234
nonidentity gate. Current completed reciprocity still evaluates and faithfully reconstructs a
supplied metric; it does not select the primary profile. The remaining live architectures are an
independently owned invariant smaller-family cut or a genuinely stronger global relation law whose
condition is stated before its desired survivor is known.
