# G121 exact derivation — co-present reciprocal/causal history consistency

Date: 2026-08-16

## 1. The proposed principle contains two different networks

The phrase

> globally reciprocal, composable, and compatible with causality

does not describe one kind of arrow.

The reversible co-present comparison of two calibrated observer states belongs to an observer-pair
relation groupoid. If a unique physical comparison is assigned to every ordered pair, its natural
abstract home is the pair groupoid. Reversing an ordered comparison is legal.

A future-directed ray or other causal propagation belongs instead to a causal path category. A
future-directed signal generally has no future-directed inverse. Reversing the observational
comparison is not the same operation as sending the physical carrier backward in time.

This type separation is essential. The metric supplies the local cones and evaluates both
structures once their observer/query/branch data are supplied. The current founding does not yet
derive the map that joins every co-present pair arrow to its causal realization(s).

## 2. Generic pair cone

On the preregistered regular spherical pair patch, write

\[
h=-T^2(d\tau+\beta dR)^2+L^2dR^2,
\qquad T,L>0.
\]

The orbit matrix and determinant are

\[
h_{ab}=
\begin{pmatrix}
-T^2&-T^2\beta\\
-T^2\beta&L^2-T^2\beta^2
\end{pmatrix},
\qquad
\det h=-T^2L^2.
\]

The dual orthonormal frame is

\[
e_0=T^{-1}\partial_\tau,
\qquad
e_1=-\frac{\beta}{L}\partial_\tau+\frac1L\partial_R.
\]

Therefore

\[
K_\pm=e_0\pm e_1,
\qquad h(K_\pm,K_\pm)=0
\]

exactly for every positive `T,L` and every `beta`. The complete shifted cone is informative about a
supplied history, but the existence of that cone does not choose the functions `T,L,beta`.

For the null Hamiltonian

\[
H(x,p)=\frac12g^{ab}(x)p_ap_b,
\]

Hamilton's equations give

\[
\frac{dH}{d\lambda}
=\partial_aH\,\frac{\partial H}{\partial p_a}
-\frac{\partial H}{\partial p_a}\,\partial_aH=0.
\]

Thus a null covector remains null under affine metric propagation on either frozen witness. This is
a metric-compatibility identity, not a history equation.

## 3. Frequency reciprocity and composition

For one carried null covector and calibrated observer clocks,

\[
\omega_i=-g(k,U_i)>0,
\qquad Z_{ij}=\frac{\omega_i}{\omega_j}.
\]

Then

\[
Z_{ij}Z_{jk}=Z_{ik},
\qquad Z_{ji}=Z_{ij}^{-1}.
\]

The exact rational witness uses frequencies

\[
(\omega_A,\omega_B,\omega_C)=(1,1/2,3/2)
\]

and returns zero triangle and reversal residuals. This holds because the same carried calibration is
used at the middle observer. It does not select the metric history.

## 4. Reciprocal descent: the genuine nonidentity fork

Start with a connected complete observer graph and let every oriented edge carry an antisymmetric
scalar 1-cochain `delta_ij`. Reversal alone says

\[
\delta_{ji}=-\delta_{ij}.
\]

It does not force triangle closure. The exact independent-edge witness

\[
\delta_{AB}=1/3,
\quad\delta_{BC}=2/5,
\quad\delta_{CA}=1/7
\]

obeys reversal after defining the opposite edges, but has the nonzero loop period

\[
\Omega_{ABC}^{\rm rec}
=\delta_{AB}+\delta_{BC}+\delta_{CA}
=\frac{92}{105}.
\]

Now impose zero oriented-triangle periods,

\[
\Omega_{ABC}^{\rm rec}=0
\]

for every observer triangle. This condition holds if and only if there is a vertex potential with

\[
\delta_{ij}=\Phi_j-\Phi_i
\]

on each connected component. The forward implication telescopes. Conversely, choose a base vertex
`o`, set `Phi_i=delta_oi`, and use the zero period on `(o,i,j)` to recover
`delta_ij=Phi_j-Phi_i`. The potential is unique up to one additive constant per component.

Only after this closure has been proved does the 1-cochain descend to an additive scalar functor on
the pair groupoid. Thus global pair-scalar descent is a real nonidentity restriction on
independently supplied pair data; it is not hidden in antisymmetry alone.

It is not yet a restriction on `g` alone. To become one, the metric must first own the physical
pair-relation family whose terminal readouts produce the `delta_ij`. The present metric/query
evaluator does not universally own that assignment.

## 5. The angular and Jacobi channels must not be flattened

The full Jacobi phase carrier composes as

\[
P_{CA}=P_{CB}P_{BA},
\qquad
P^{-1}_{AB}=P_{BA}
\]

on matched paths and middle phase states. Its symplectic form is preserved:

\[
P^T\Omega P=\Omega.
\]

The production witness uses two noncommuting exact rational symplectic maps; both factors and their
composite pass exactly.

Path-labelled screen transport similarly composes group-valuedly. The exact orthogonal loop

\[
U_{\rm loop}=
\begin{pmatrix}0&-1\\1&0\end{pmatrix}
\neq I
\]

has determinant `+1` and is a lawful oriented `SO(2)` screen rotation. Consequently, global
reciprocal scalar descent does **not** imply zero screen holonomy. Separately, G121 verifies
phase-map symplectic composition; it does not construct a closed nonidentity Jacobi-phase loop.
G114 conditionally types such phase-loop holonomy through source junctions. Requiring every direct
route to equal every composite route would add flatness and
erase legitimate curvature memory. That is a stronger premise, not Reciprocity.

## 6. Two inequivalent histories survive

The frozen witnesses are

\[
H_0:\quad T=L=1,\quad\beta=0,
\]

and

\[
H_1:\quad
T=e^{\tau R^2/5},\quad
L=e^{-\tau R^2/7},\quad
\beta=\tau R/11
\]

on `|tau|<=1`, `0<=R<=1`.

They are centrally regular and Lorentzian. They are invariantly distinct in areal gauge because

\[
g^{-1}(dR,dR)=L^{-2}
\]

is `1` for `H0` and `exp(2 tau R^2/7)` for `H1`.

Both preserve the null Hamiltonian exactly. Both patches also admit `tau` as a time function. For
`H1`, throughout the declared patch,

\[
g^{-1}(d\tau,d\tau)
\le -e^{-2/5}+\frac{e^{2/7}}{121}
\approx-0.6593<0.
\]

Therefore adding ordinary local cone consistency—and even this bounded time-function condition—does
not distinguish the two histories.

## 7. What global causality can and cannot do

Global chronology, causality, stable causality, and global hyperbolicity are progressively stronger
nonlocal restrictions on a Lorentzian history. They can exclude histories that have the same local
cone algebra. None is derived merely by:

- the reciprocal `c_E` character;
- local cone existence;
- null-geodesic preservation;
- matched observer composition; or
- co-presence understood only as membership in one complete solution.

Moreover, reciprocal comparison reversal must not be identified with reversal of a future causal
arrow. A global causal condition can be adopted and tested, but it would remain a declared
completion premise until derived from stronger UDT structure.

## 8. The useful joint exposed by the negative

The proposed physical-history idea is not empty. It becomes a sharply typed joint condition:

1. one complete metric history supplies the cone/Jacobi/transport evaluator;
2. one physical co-present observer-pair family supplies reversible pair arrows;
3. the reciprocal scalar on those arrows descends globally (`Omega_rec=0`);
4. causal observation paths remain directed and retain lawful phase/screen holonomy;
5. on every realized observation, the causal and co-present evaluations agree through the same
   complete metric construction.

Items 1 and the conditional evaluation in 4 are owned. Item 3 is a mathematically exact closure
condition once the pair family is supplied. The unowned joint is the metric-native assignment in
item 2 and its compatibility map in item 5.

The smallest next calculation is therefore a mixed commuting-square test. For one source and two
observers, compare:

- the causal carried edge `P_B^{-1} C_{BA} P_A` from G114; and
- the direct co-present pair edge obtained from one complete pair immersion.

These maps are not currently known to act on one common carrier: the first is a four-dimensional
Jacobi phase map, while the second starts as a tangent/pair differential. The next gate must first
derive a canonical common carrier, inclusion, quotient, or comparison diagram. A multiplicative
matrix defect is not defined before that typing succeeds. The eventual comparison must retain the
full Jacobi phase, terminal pair block, middle calibration, and angular holonomy. At scalar order
its local reduction must reproduce G116 rather than impose
`zeta=phi_pair` outside the pure stationary reciprocal branch.

## 9. Bounded landing

```text
LOCAL_CAUSAL_COMPOSITION_IDENTITIES_ONLY
__PAIR_SCALAR_DESCENT_IS_A_CONDITIONAL_NONIDENTITY_CLOSURE_ON_SUPPLIED_PAIR_DATA
__RECIPROCAL_SCALAR_DESCENT_DOES_NOT_REQUIRE_ZERO_SCREEN_HOLONOMY
__TWO_INEQUIVALENT_REGULAR_TIME_ORIENTED_HISTORIES_SURVIVE
__GLOBAL_CAUSAL_COMPLETION_IS_NOT_DERIVED_BY_LOCAL_CONES_OR_RECIPROCITY
__NO_METRIC_ONLY_HISTORY_SELECTOR
__TYPED_MIXED_CAUSAL_PAIR_MAP_REMAINS_OPEN
```

No native radiation, source, matter, signalling, action, bootstrap, `X_max`, SNe, BAO, or CMB result
follows.
