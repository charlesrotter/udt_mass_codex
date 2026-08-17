# G145 exact derivation — relation/history descent equivalence

Date: 2026-08-17

## 1. The object being tested

A regular co-present relation atlas consists of two nested structures:

1. a full-dimensional regular base cover `U_i` with transition maps `f_ji`;
2. over each base chart, a rank-complete labelled family of pair differentials and regular pair
   sheets `F_alpha:Sigma_alpha->M` with complete pullbacks `h_alpha=F_alpha^*g`;
3. branch-resolved two-dimensional maps `psi_beta_alpha=F_beta^-1 o F_alpha` only where two pair
   sheets represent one immersed relation patch;
4. calibrated endpoint factors and the adopted signed position readout within each declared
   composition-compatible relation family;
5. time orientation and the metric causal cones; and
6. separately typed path transport when a query owns a route.

This is not one universal scalar field. Different pair families can have different terminal
reciprocal readouts because the complete angular, screen, mixing, and immersion data enter before
`phi_pair`. Cross-family composition is required only when the middle state and relation type match.

## 2. Descent theorem

At a point let the declared pair differentials be

\[
A_a:\mathbb R^2\longrightarrow T_pM,
\qquad h_a=A_a^TgA_a.
\]

The linear restriction map is

\[
\mathcal M_A(k)=\{A_a^TkA_a\}_a.
\]

If `rank(M_A)=10`, the full four-dimensional symmetric bilinear form is uniquely reconstructed.
The six ruler directions

\[
e_1,e_2,e_3,e_1+e_2,e_1+e_3,e_2+e_3
\]

give exact rank ten.

On a full-dimensional base-chart overlap,

\[
g_i=f_{ji}^*g_j,
\qquad
Df_{ki}=Df_{kj}Df_{ji}.
\]

Therefore the uniquely reconstructed local metrics obey the same tensor transition law and descend
to one Lorentz metric on the supplied regular Hausdorff second-countable base quotient. Conversely, one
Lorentz metric plus a supplied labelled rank-complete query atlas produces exactly these pullbacks
and overlap identities.

G144's two-dimensional pair-sheet overlap is a different level: it supplies presentation carry
inside an already typed common relation patch. Pair sheets alone do not form a four-dimensional
manifold atlas, and their overlap is not used here as a substitute for base-chart descent.

Hence, modulo atlas reparameterization,

\[
\boxed{
\text{coherent rank-complete valued relation atlas}
\quad\longleftrightarrow\quad
(\text{Lorentz metric history},\text{supplied labelled query atlas}) .
}
\]

This is an equivalence of presentations after numerical values and query data are supplied. It is
not a derivation of those values or of the physical query population.

## 3. Position and carry add no second history field

For endpoint reciprocal factors

\[
R_i=\operatorname{diag}(e^{-\Phi_i},e^{+\Phi_i}),
\]

the calibrated comparison is

\[
C_{ji}=R_jR_i^{-1}=D(\Phi_j-\Phi_i).
\]

It obeys

\[
C_{kj}C_{ji}=C_{ki},
\qquad C_{ji}^{-1}=C_{ij},
\]

and every matched triangle has zero reciprocal period. The adopted position constitution then gives

\[
\xi_{ji}=\tanh(\Phi_j-\Phi_i),
\qquad
\xi_{ki}=\frac{\xi_{ji}+\xi_{kj}}{1+\xi_{ji}\xi_{kj}}.
\]

On a reparameterized or overlapping sheet, G142--G144 replace identity carry by the covariant total
`C=R_j M_ji R_i^-1`; no new physical field is created. Path-labelled angular transport can remain
nontrivial while the endpoint positional cycle closes.

The cycle condition is nonidentity on independently supplied edge values. But choosing a coherent
endpoint-factor family leaves every smooth assignment `Phi_i` free. Composition constrains the
form of the values, not their numerical profile.

## 4. Continuous inequivalent survivor family

Consider the complete four-dimensional metric family

\[
g_\Phi=-e^{-2\Phi(r)}c_E^2dt^2+e^{2\Phi(r)}dr^2+dy^2+dz^2,
\qquad c_E>0.
\]

Its determinant and inverse clock norm are

\[
\det g_\Phi=-c_E^2,
\qquad
g_\Phi^{-1}(dt,dt)=-\frac{e^{2\Phi}}{c_E^2}<0.
\]

Thus it is Lorentzian and `t` is a temporal function on every regular bounded patch. The radial
clock-ruler pair has terminal reciprocal potential `Phi(r)`. Endpoint comparisons are exact
potential differences and therefore obey reversal, composition, cycle closure, and the signed
Mobius position law for every smooth `Phi`.

The scalar curvature, independently reconstructed from the full Christoffel expression, is

\[
\mathcal R[g_\Phi]
=e^{-2\Phi}\left(2\Phi''-4(\Phi')^2\right).
\]

Preregister

\[
\Phi_-(r)=ar,
\qquad
\Phi_+(r)=ar+br^2,
\qquad a>0,\ b>a^2.
\]

At the common marked event `r=0`,

\[
\mathcal R[g_{\Phi_-}]=-4a^2<0,
\qquad
\mathcal R[g_{\Phi_+}]=4b-4a^2>0.
\]

The marked histories are not isometric, yet both pass every declared reciprocal, composition,
position, overlap, rank-completeness, and local causal gate. The arbitrary smooth profile shows that
the survivor space is function-valued, not merely a two-member ambiguity.

## 5. No frozen-orchestra escape

The diagonal display is an exact separating core, not the maximum arena. Introduce the complete
coframe

\[
E=\begin{pmatrix}B&0\\QS&Q\end{pmatrix},
\]

with the base block

\[
B=\begin{pmatrix}T&T\beta\\0&L\end{pmatrix},
\quad T=e^{\kappa-\Phi},\quad L=e^{\kappa+\Phi}.
\]

The production witness uses independent nonconstant cubic germs for `kappa`, base shift `beta`, all
three positive-screen variables in `Q`, and all four mixing variables in `S`. These are all nine
complete-coframe fields beyond the live reciprocal profile. Their metric perturbation has exactly
zero 0-, 1-, and 2-jets at the marked event, while every field is live away from its zero locus.
Consequently the two marked curvature signs remain exact.

More generally, Lorentz signature, a strictly timelike `dt`, and separated curvature signs are open
under sufficiently small smooth perturbations on a compact subpatch. The two survivors therefore
have open neighborhoods with every complete-coframe sector active. Turning on the orchestra changes
the terminal values through the full pullback, but it does not turn compatibility identities into a
numerical history equation.

## 6. What causality contributes

Metric causality supplies a real admissibility cut: non-Lorentzian or time-orientation-incompatible
data fail. It does not choose among the preregistered survivors. Reciprocal observer comparison is
reversible; future-directed causal propagation is not generally invertible. Equating those two
arrow types would be a category error and an extra physical premise.

Stronger global conditions such as global hyperbolicity or a particular completion may cut the
history space, but they are not derived by the active premises and are outside this bounded test.

## 7. Why the observed anchors do not close the profile

The dimension vectors of `c_E` and `G_obs` are

\[
[c_E]=(1,0,-1),
\qquad [G]=(3,-1,-2)
\]

in `(length,mass,time)` exponents. No monomial `c_E^alpha G^beta` has the dimension of length: zero
mass exponent forces `beta=0`, zero time exponent then forces `alpha=0`. More importantly, constants
alone do not supply a differential or global equation for the function `Phi`.

A mass, density, curvature datum, boundary condition, observation, or native global law could add
information. None is currently derived as the missing profile owner. The bootstrap idea remains a
working hypothesis, not a conclusion of this calculation.

## 8. Landing

The preregistered landing is

```text
RELATION_NETWORK_EQUIVALENT_TO_HISTORY__VALUES_OPEN
```

The important simplification is positive: the full-pullback valuation uniquely determines the
metric component on the supplied four-dimensional base atlas. The labelled query atlas,
calibrations, numerical valuation, and physical realization remain supplied or open. What remains
open is not an extra translation mechanism between those full pullbacks and the reconstructed
metric; it is the numerical/global law or physical data that determine which coherent valuation is
realized.

This theorem is restricted to regular time-oriented local/overlap strata. It does not settle
singularities, topology, boundary completion, numerical `X_max`, proper length, dynamics, action,
source, light, bootstrap, matter, mass, or observations.
