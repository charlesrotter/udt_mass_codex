# G248 exact derivation — metric regular-branch measure ownership

## Landing

`METRIC_OWNS_ORDERED_REGULAR_INCIDENCE_COAREA_DENSITY_R_OVER_A__SKY_PHASE_COUNTING_AND_INCIDENCE_MEASURES_ARE_DISTINCT_TYPED_OBJECTS__CSP4_COMPOSITION_LEAVES_REAL_CHARACTER_FAMILY_R_TO_ALPHA__UNIVERSAL_PHYSICAL_BRANCH_MEASURE_SOURCE_POPULATION_AND_CRITICAL_COMPLETION_REMAIN_OPEN`

This is alternative B from the preregistration. The result is metric-led and outcome-blind.

## 1. Bounded geometric setting

Let \((M,g)\) be a time-oriented Lorentzian four-manifold and let \(z_A,z_B\) be future unit-timelike
observer worldlines with proper times \(\tau_A,\tau_B\). G245 supplies the celestial sphere and the
source-clock-normalized future-null germ

\[
 -g(U_A,N_A)=1.
\]

On the regular domain define the source-cone map

\[
 C_A(\tau_A,n,s)=\operatorname{Exp}_{z_A(\tau_A)}(sN_A(\tau_A,n)),
 \qquad n\in S_A^2.
\]

The ordered incidence relation is the fiber product

\[
 \mathcal I_{AB}
 =\{(\tau_A,n,s,\tau_B):C_A(\tau_A,n,s)=z_B(\tau_B)\}.
\]

This derivation is restricted to a locally finite, noncaustic, transverse regular stratum: the
incidence difference map has rank four and the two-dimensional Jacobi position block is invertible.
No source population, detector, observational outcome, `X_max`, or critical completion is used.

## 2. The canonical ordered incidence coarea density

The metric and the two proper-clock calibrations supply the product density

\[
 d\lambda_X=d\tau_A\,d\Omega_A\,ds\,d\tau_B
\]

on \(X=I_A\times S_A^2\times\mathbb R_+\times I_B\), together with the spacetime density
\(|\operatorname{vol}_g|\). On a transverse fiber, the density exact sequence defines the coarea
density \(d\mu_{AB}\) by dividing the domain density by the normal Jacobian of the incidence map.

Choose orthonormal angular coordinates at the source. At the target let

\[
 J_i=\frac{\partial C_A}{\partial n^i},\qquad K=\frac{\partial C_A}{\partial s}
\]

and let \(U_B\) be the target clock. If \(\mathcal D\) is the G244 Jacobi screen map—equivalently
the G226 upper-right phase block \(B\)—then

\[
 A_{AB}=|\det\mathcal D|>0.
\]

In a target orthonormal frame,

\[
 K=\omega_B(U_B+e_3),
\]

while null-gauge additions \(J_i\mapsto J_i+\gamma_iK\) do not alter the determinant. Therefore

\[
 \left|\operatorname{vol}_g(J_1,J_2,K,U_B)\right|
 =\omega_B A_{AB}.
\]

G216/G226 give

\[
 r_{AB}=\frac{\omega_A}{\omega_B}=\frac{d\tau_B}{d\tau_A}.
\]

The source normalization is \(\omega_A=1\), hence \(\omega_B=r_{AB}^{-1}\). Evaluating the density
exact sequence on a branch tangent normalized by \(d\tau_A=1\) gives

\[
 \boxed{d\mu_{AB}=\frac{r_{AB}}{A_{AB}}\,d\tau_A.}
\]

This is an ordered geometric incidence density: in flat space it has the familiar inverse-area
dimension. It is not, by itself, a probability, luminosity law, source number density, or detector
response.

The formula is invariant under endpoint \(O(2)\) screen changes, under orientation reversal after
the absolute determinant is taken, and under additions of multiples of \(K\) to the Jacobi fields.
The source-clock normalization removes arbitrary affine scale. Equivalently, under an unnormalized
affine rescaling the changes in \(ds\) and \(K\) cancel in the density quotient.

## 3. Reversal is typed, not a scalar symmetry claim

Write the G226 phase map as

\[
 M=\begin{pmatrix}A&B\\C&D\end{pmatrix},
 \qquad M^T\Omega M=r\Omega.
\]

Then

\[
 M^{-1}=\frac1r
 \begin{pmatrix}D^T&-B^T\\-C^T&A^T\end{pmatrix}.
\]

Consequently,

\[
 B_{BA}=-r^{-1}B_{AB}^T,
 \qquad A_{BA}=\frac{A_{AB}}{r^2},
 \qquad r_{BA}=r^{-1}.
\]

The inverse-query coefficient is therefore

\[
 \frac{r_{BA}}{A_{BA}}=\frac rA.
\]

But it multiplies \(d\tau_B\), not \(d\tau_A\). Since \(d\tau_B=r\,d\tau_A\), the two complete
ordered densities are not generally identical. G248 derives lawful reversal of the typed query; it
does not impose an additional exchange-even physical weighting.

## 4. Other canonical measures are different objects

The same metric geometry supplies several measures with different domains:

1. \(d\Omega_A\): solid angle on one observer's celestial sphere;
2. phase volume \(\nu\): for the full G226 phase map,
   \[
   M^*\nu_B=r^2\nu_A,\qquad M_*\nu_A=r^{-2}\nu_B;
   \]
3. unit counting on a finite branch fiber, after the G240 all-image query is chosen;
4. the ordered incidence coarea density \((r/A)d\tau_A\).

They cannot be identified merely because all are metric-natural on their typed domains.

## 5. Composition does not select a universal weight

Every positive conformal-symplectic map can be written uniquely as

\[
 M=\sqrt r\,S,\qquad S\in\operatorname{Sp}(4,\mathbb R).
\]

The connected semisimple group \(\operatorname{Sp}(4,\mathbb R)\) has no nontrivial continuous
positive real character. Every continuous positive character of
\(\operatorname{CSp}^+(4,\mathbb R)\) therefore factors through the multiplier:

\[
 \boxed{\chi_\alpha(M)=r(M)^\alpha,\qquad \alpha\in\mathbb R.}
\]

Composition proves multiplicativity for every \(\alpha\); it does not select one exponent.

Matched incidence coarea densities may be multiplied on a declared fiber-product chain. That
matched-chain density must not be identified with a direct edge: the composed Jacobi position
block is the full phase-block expression, not generally \(B_2B_1\).

## 6. Caustic boundary and conclusion ceiling

At \(A=0\), the regular incidence Jacobian vanishes and \((r/A)d\tau_A\) leaves its domain. The
full phase map remains invertible because \(\det M=r^2>0\). G248 does not prescribe branch merger,
critical measure, wave uniformization, or aggregation across the caustic.

Thus the metric owns a nontrivial ordered geometric incidence density on the stated regular query.
It does not select a universal physical branch probability or populate sources. The exact result is
a narrowing of the missing bridge, not closure of source or observational semantics.
