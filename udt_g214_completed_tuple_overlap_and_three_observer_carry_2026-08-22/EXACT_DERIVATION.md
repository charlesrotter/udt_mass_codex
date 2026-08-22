# G214 exact derivation — completed-tuple overlap and three-observer carry

Date: 2026-08-22

## Bounded landing

```text
THE_DENSITY_COMPLETED_TUPLE_IS_A_NATURAL_CHANGE_OF_VARIABLES_ON_POSITIVE_CALIBRATED_PAIR_CHARTS
__THE_POSITIVE_DENSITY_CARRIES_THE_TRANSITION_DETERMINANT
__THE_NORMALIZED_METRIC_CARRIES_AN_INDUCED_SL2_CONGRUENCE
__THE_INDUCED_TRANSITIONS_OBEY_THE_EXACT_TRIPLE_OVERLAP_COCYCLE
__G130_COMPATIBLE_FULL_PULLBACK_DESCENT_THEREFORE_TRANSFERS_WITHOUT_DENSITY_LOSS
__PURE_RULER_REPARAMETERIZATION_IS_ABSORBED_BY_THE_DENSITY
__GENERAL_RECHARTING_IS_EQUIVARIANT_NOT_INVARIANT
__ORIENTATION_REVERSAL_REQUIRES_THE_RETAINED_RULER_ORIENTATION
__DISTINCT_AB_BC_AC_PAIR_SURFACES_HAVE_NO_AUTOMATIC_FULL_TUPLE_PRODUCT
__MATCHED_INCIDENCE_SCALARS_TELESCOPE_AND_THE_G171_UNMATCHED_DEFECT_SURVIVES
__NO_GERM_POPULATION_NETWORK_VALUES_OR_HISTORY_EVOLUTION_DERIVED
```

Status: `DERIVED_CONDITIONAL__INDEPENDENTLY_VERIFIED__EXTERNALLY_REVIEWED_WITH_CAVEATS`.

## 1. Domain

Let \(h_i\) be the matrix of one supplied regular Lorentzian pair pullback in a calibrated pair
chart \(i\), with

\[
(h_i)_{00}<0,\qquad \det h_i<0.
\]

The G176 working clarification defines

\[
m_i=\sqrt{-\det h_i}>0,
\qquad
J_i=\operatorname{diag}(1,m_i),
\qquad
h_{s,i}=J_i^{-T}h_iJ_i^{-1}.
\]

Therefore \(\det h_{s,i}=-1\), and G213 gives the exact inverse

\[
h_i=J_i^Th_{s,i}J_i.
\]

The calibrated germ and ruler orientation remain part of the type. The following theorem concerns
only the regular order-zero pair tensor. It does not include derivatives, connections, holonomy,
caustics, or singular charts.

## 2. Positive calibrated overlap theorem

Let charts \(i\) and \(j\) overlap with a smooth time- and ruler-orientation-preserving calibrated
Jacobian

\[
P_{ij}=
\begin{pmatrix}
a&n\\
0&d
\end{pmatrix},
\qquad a,d>0,
\]

and convention

\[
h_j=P_{ij}^Th_iP_{ij}.
\]

Taking determinants gives

\[
-\det h_j=(\det P_{ij})^2(-\det h_i).
\]

Positivity removes the absolute-value ambiguity, so

\[
\boxed{m_j=(\det P_{ij})m_i=ad\,m_i.}
\]

Define the induced completed transition

\[
\boxed{C_{ij}=J_iP_{ij}J_j^{-1}.}
\]

Its determinant is

\[
\det C_{ij}
=\frac{m_i\det P_{ij}}{m_j}
=1.
\]

Thus \(C_{ij}\in SL(2,\mathbb R)\). Direct substitution gives

\[
\boxed{h_{s,j}=C_{ij}^Th_{s,i}C_{ij}.}
\]

For the displayed triangular transition,

\[
\boxed{
C_{ij}=
\begin{pmatrix}
a&n/(ad\,m_i)\\
0&a^{-1}
\end{pmatrix}.}
\]

The spatial scale \(d\) is absorbed into the density. Clock rescaling \(a\) and clock-ruler shear
\(n\) remain as a reciprocal determinant-one congruence of the normalized metric.

This is the precise sense in which completion commutes with recharting: the tuple is equivariant.
Except on a smaller subgroup, \(h_s\) is not invariant by itself.

## 3. Reconstruction commutes with the overlap

Starting from the completed tuple in chart \(j\),

\[
\begin{aligned}
J_j^Th_{s,j}J_j
&=J_j^TC_{ij}^Th_{s,i}C_{ij}J_j\\
&=P_{ij}^TJ_i^Th_{s,i}J_iP_{ij}\\
&=P_{ij}^Th_iP_{ij}\\
&=h_j.
\end{aligned}
\]

Therefore the square commutes exactly:

\[
\boxed{
\begin{array}{ccc}
h_i&\longleftrightarrow&(m_i,h_{s,i})\\
\downarrow P_{ij}&&\downarrow(\det P_{ij},C_{ij})\\
h_j&\longleftrightarrow&(m_j,h_{s,j}).
\end{array}}
\]

The density is essential. Removing it destroys the inverse horizontal arrows and reproduces the
G213 positive spatial-rescaling blind family.

## 4. Triple-overlap cocycle

On a triple overlap let

\[
P_{ik}=P_{ij}P_{jk}.
\]

Then the density transformations multiply:

\[
m_k=(\det P_{jk})m_j
=(\det P_{ij})(\det P_{jk})m_i
=(\det P_{ik})m_i.
\]

The completed transitions obey

\[
\begin{aligned}
C_{ij}C_{jk}
&=(J_iP_{ij}J_j^{-1})(J_jP_{jk}J_k^{-1})\\
&=J_iP_{ij}P_{jk}J_k^{-1}\\
&=C_{ik}.
\end{aligned}
\]

Thus the density-completion map is a faithful change of variables on the supplied calibrated
pair-chart groupoid. It does not merely pass pairwise overlaps; it preserves the exact cocycle
order.

## 5. Pure ruler reparameterization

For

\[
P=\operatorname{diag}(1,k),\qquad k>0,
\]

one has \(m'=km\) and

\[
C=JPJ'^{-1}=I.
\]

Therefore

\[
\boxed{h_s'=h_s.}
\]

This recovers G176/G180: the one-dimensional ruler reparameterization is absorbed entirely by the
positive density. Under a general calibrated rechart, however, \(C\ne I\) in general.

## 6. Orientation and the two different reversals

The positive-overlap theorem assumed \(\det P>0\). For a spatial orientation reversal

\[
R=\operatorname{diag}(1,-1),
\]

the positive magnitude \(m\) is unchanged, the retained ruler orientation changes sign, and

\[
h_s' = R^Th_sR.
\]

The clock-ruler shift changes sign. This is a pair-chart orientation operation, not observer-pair
endpoint reversal.

Same-pair endpoint reversal instead swaps the same two completed incidence readouts. G170 then
continues to give

\[
\delta_{BA}=-\delta_{AB}.
\]

Conflating these two reversals would erase the shift or falsely negate a local endpoint density.

## 7. Transfer of the G130 representation theorem

G130 requires known calibrated embeddings, their complete pullbacks, and lawful overlap descent.
Sections 2--4 show that every full-pullback transition has one exact density-completed transition,
and Section 3 reconstructs the original pullback on every chart. Consequently,

\[
\boxed{
\text{smooth compatible full-pullback valuation}
\longleftrightarrow
\text{smooth compatible typed }(m,h_s)\text{ valuation}.}
\]

The G129/G213 rank-ten finite witness is therefore not merely pointwise faithful: on any supplied
compatible regular cover, it can be expressed with density-completed tuples without changing the
reconstructed metric or its overlap law.

This is still reconstructive. It does not assign the numerical values, select the cover, or prove
that Nature populates the rank-complete germ family.

## 8. Three observers are not one chart overlap

Let independently supplied pair germs `AB`, `BC`, and `AC` have endpoint-incidence scalars

\[
\Phi_{A|AB},\ \Phi_{B|AB},\ \Phi_{B|BC},\ \Phi_{C|BC},\
\Phi_{A|AC},\ \Phi_{C|AC}.
\]

Their exact G171 defect is

\[
\begin{aligned}
\Omega_{ABC}
={}&\delta_{AB}+\delta_{BC}-\delta_{AC}\\
={}&(\Phi_{B|AB}-\Phi_{B|BC})
+(\Phi_{C|BC}-\Phi_{C|AC})
+(\Phi_{A|AC}-\Phi_{A|AB}).
\end{aligned}
\]

Tuple completion does not set these three incidence mismatches to zero. A shared observer label is
not a chart transition between two distinct pair planes. Moreover, two symmetric Lorentz pair
metrics do not possess a geometrically typed matrix product; ordinary matrix multiplication need
not even remain symmetric.

If explicit incidence identifications place all incident tuples into the same calibrated state,
then the endpoint scalars match and telescope. Such maps are sufficient compatibility data. They
may be supplied by one common pair family or a later global query construction. They are not
generated by the local completion algebra.

Therefore:

\[
\boxed{
\text{chart-overlap descent closes}
\quad\not\Rightarrow\quad
\text{arbitrary three-observer full-tuple composition}.}
\]

## 9. Status ceiling

- `DERIVED_CONDITIONAL`: density weight, induced determinant-one transition, reconstruction square,
  and triple-overlap cocycle on the supplied positive calibrated pair-chart groupoid.
- `DERIVED_BOUNDED`: pure ruler reparameterization invariance and oriented reversal congruence.
- `DERIVED_CONDITIONAL`: G130 compatible-cover reconstruction transfers to typed completed tuples
  without density loss.
- `RETAINED`: G170 same-pair reversal and G171 exact three-pair incidence defect.
- `OPEN`: cross-pair incidence owner, physical germ population, numerical network valuation,
  singular/global strata, and history evolution.

No fit, transfer law, `X_max`, source, action, matter, mass, bootstrap, observation, signalling, or
canon claim follows.
