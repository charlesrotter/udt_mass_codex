# G340 exact derivation — finite-separated normal-observer relations

Date: 2026-09-03
Grade: `EXTERNALLY_ACCEPTED_DERIVED_CONDITIONAL_BOUNDED`

## Bounded landing

```text
METRIC_NULL_GEOMETRY_CLOSES_A_PATH_LABELLED_FINITE_NORMAL_PAIR_FAMILY
__NO_PHENOMENOLOGICAL_LIGHT_MODEL_REQUIRED
__SLICE_DISTANCE_NULL_EXCHANGE_RADAR_AND_PROJECTIVE_READOUT_ARE_RELATED_NOT_IDENTICAL
__COMPACT_WINDINGS_REMAIN_DISTINCT_BRANCHES
__NO_PHYSICAL_PROTOCOL_POPULATION_SCALE_OR_XMAX_SELECTED
```

G340 selects preregistered alternative A. It uses null geometry as a mathematical consequence of
the supplied metric. It does not import electromagnetism, photon propagation, luminosity, opacity,
or a transfer law. An ideal two-leg radar reflection is a declared operational control, not a UDT
distance postulate.

## 1. Fixed spacetime and observers

Use the exact conditional G323/G324/G338/G339 spacetime

\[
 g=-dT^2+a_X(T)^2dX^2+a_\perp(T)^2(dy^2+dz^2),
\]

\[
 a_X=C_XT^{-1/3},\qquad a_\perp=C_\perp T^{2/3},\qquad T>0.
\tag{1}
\]

The supplied normal observers are the fixed spatial-label curves, with tangent `n=partial_T`.
Their geometric proper-clock length is `T`; if proper time is recorded in time units, then
`tau=T/c_E`. No observer population is selected by (1).

Let `Gamma` be the supplied compact translation lattice. Two spatial labels have lift differences

\[
 q_\ell=\Delta x+\ell,\qquad \ell\in\Gamma.
\tag{2}
\]

Every `ell` is a distinct path/homotopy label until an explicit quotient identification is made.

## 2. Same-slice distance

Each constant-`T` slice is flat with the time-dependent quadratic form

\[
 \gamma_T(q,q)=C_X^2T^{-2/3}q_X^2
 +C_\perp^2T^{4/3}(q_y^2+q_z^2).
\tag{3}
\]

The length of the straight lifted slice geodesic is

\[
 D_\ell(T)=\sqrt{\gamma_T(q_\ell,q_\ell)},
\tag{4}
\]

and the shortest distance in this supplied normal slicing is

\[
 \boxed{D_{\rm slice}(T)=\min_{\ell\in\Gamma}D_\ell(T)}.
\tag{5}
\]

This is an exact finite-separation extension of G338/G339's connecting-field length. It is tied to
the supplied normal slice and is not automatically radar, affine, optical, or projective distance.
For a mixed direction the minimizing lattice lift can change with `T`, producing an ordinary flat-
torus cut-locus switch rather than a spacetime singularity.

## 3. Metric-null propagation without a light model

For an affinely parametrized null curve, translation symmetry makes the three covariant spatial
momenta constant:

\[
 p_X=a_X^2\dot X,\qquad p_y=a_\perp^2\dot y,\qquad
 p_z=a_\perp^2\dot z.
\tag{6}
\]

The null Hamiltonian is

\[
 0=2\mathcal H=-p_T^2
 +\frac{p_X^2T^{2/3}}{C_X^2}
 +\frac{(p_y^2+p_z^2)T^{-4/3}}{C_\perp^2}.
\tag{7}
\]

For the future branch, the frequency measured by a normal observer is

\[
 \omega(T)=-g(k,n)=\dot T
 =\sqrt{\frac{p_X^2T^{2/3}}{C_X^2}
 +\frac{p_\perp^2T^{-4/3}}{C_\perp^2}}.
\tag{8}
\]

Therefore every supplied regular momentum/path branch has the exact endpoint quadrature

\[
 q_\ell^i=\int_{T_e}^{T_r}
 \frac{\gamma^{ij}(T)p_j}{\omega(T)}\,dT.
\tag{9}
\]

Multiplying all `p_i` by one positive constant changes the affine scale but not (9). Equation (9)
is the general nonprincipal answer. Solving its boundary-value inverse can be multivalued and is
not classified here, but no phenomenological propagation model is missing: the metric completely
specifies the equation and every supplied solution branch.

## 4. Exact principal-axis arrivals

For a longitudinal lift of coordinate length `q>0`, equation (9) gives

\[
 q=\frac{3}{4C_X}\left(T_r^{4/3}-T_e^{4/3}\right),
\]

\[
 \boxed{T_r=\left(T_e^{4/3}+\frac{4C_Xq}{3}\right)^{3/4}}.
\tag{10}
\]

For either transverse principal direction,

\[
 q=\frac{3}{C_\perp}\left(T_r^{1/3}-T_e^{1/3}\right),
\]

\[
 \boxed{T_r=\left(T_e^{1/3}+\frac{C_\perp q}{3}\right)^3}.
\tag{11}
\]

Both maps are strictly increasing in `q`; every nonzero winding arrives later than a shorter lift
when compared within the same principal family and emission event.

## 5. Frequency, reciprocal depth, and projective readout

On a regular directed leg G298 defines

\[
 r=\frac{\omega_e}{\omega_r}=\frac{d\tau_r}{d\tau_e},
 \qquad \delta=-\log r.
\tag{12}
\]

Equations (8), (10), and (11) give

\[
 r_X=\left(\frac{T_e}{T_r}\right)^{1/3},\qquad
 \delta_X=\frac13\log\frac{T_r}{T_e},
\tag{13}
\]

\[
 r_\perp=\left(\frac{T_r}{T_e}\right)^{2/3},\qquad
 \delta_\perp=-\frac23\log\frac{T_r}{T_e}.
\tag{14}
\]

A principal null route remains in its `1+1` plane, so the transported screen mismatch is zero.
The existing completed transported-source projective readout is consequently

\[
 \boxed{\chi=\tanh\delta=\frac{1-r^2}{1+r^2}},\qquad
 \boxed{M=\operatorname{sech}\delta=\frac{2r}{1+r^2}}.
\tag{15}
\]

The positive route length `q` has not become negative in (14). The sign of `delta` and `chi` records
the ordered clock/frequency response of an expanding or contracting principal direction. It is not
the sign of physical distance. Mathematical path reversal, a later physical return leg, and a
positive slice length remain three different operations.

## 6. Two-leg radar as a supplied protocol

Let normal observer A emit at `T_-`, normal observer B reflect at `T_B`, and A receive at `T_+`.
Give the outgoing and return principal lifts independent positive lengths `q_-` and `q_+`. For the
longitudinal family,

\[
 T_-^{4/3}=T_B^{4/3}-\frac{4C_Xq_-}{3},\qquad
 T_+^{4/3}=T_B^{4/3}+\frac{4C_Xq_+}{3}.
\tag{16}
\]

For the transverse family,

\[
 T_-^{1/3}=T_B^{1/3}-\frac{C_\perp q_-}{3},\qquad
 T_+^{1/3}=T_B^{1/3}+\frac{C_\perp q_+}{3}.
\tag{17}
\]

The A-centred convention assigns

\[
 T_A^{\rm rad}=\frac{T_-+T_+}{2},\qquad
 D_A^{\rm rad}=\frac{T_+-T_-}{2}
 =\frac{c_E}{2}(\tau_+-\tau_-).
\tag{18}
\]

Thus `c_E` merely converts the clock record to length and cancels after `T=c_E tau`; it neither
selects the metric history nor fixes an independent absolute scale.

For fixed route lengths, the exact first-germ clock-correspondence rates are

\[
 \boxed{
 R_X=\frac{2}{(T_B/T_-)^{1/3}+(T_B/T_+)^{1/3}}
 },
\tag{19}
\]

\[
 \boxed{
 R_\perp=\frac{2}{(T_-/T_B)^{2/3}+(T_+/T_B)^{2/3}}
 }.
\tag{20}
\]

When `q_-=q_+=q`, the reflection event is the midpoint in the appropriate conformal power,

\[
 T_B^{4/3}=\frac{T_-^{4/3}+T_+^{4/3}}2
 \quad\hbox{or}\quad
 T_B^{1/3}=\frac{T_-^{1/3}+T_+^{1/3}}2,
\tag{21}
\]

but generally not the arithmetic radar midpoint. This is the exact finite-time version of G297's
warning that radar midpoint is a convention on a causal diamond, not co-presence or the whole pair
relation.

## 7. The four notions do not collapse

Take `C_X=C_perp=1`, `T_B=2`, and equal principal lift lengths `q=0.8`. Direct evaluation gives

```text
longitudinal: T_-=1.3235444627, T_+=2.6061770888
              D_radar=0.6413163131, D_slice(T_B)=0.6349604208
transverse:   T_-=0.9798993528, T_+=3.5576669618
              D_radar=1.2888838045, D_slice(T_B)=1.2699208416
```

The differences are exact nonlinear effects, not numerical noise. Projective `chi` is dimensionless
and belongs to each directed leg; it cannot equal either length without a separately typed scale.
The null relation is the full pair of endpoint events plus a route label, not its travel-time
number alone.

## 8. Compact winding and first arrival

On a split principal circle of period `L`, every lift has

\[
 q_n=|\Delta x+nL|,\qquad n\in\mathbb Z.
\tag{22}
\]

Substituting `q_n` into (10) or (11) produces a distinct path-labelled arrival branch. The smallest
`q_n` gives the earliest arrival in that principal family. At a half-period separation two lifts tie,
so even earliest arrival can be branch-multiple. The later winding arrivals remain lawful metric
solutions; G340 does not discard them or claim that a physical source excites them.

For a general lattice and mixed route, equations (2), (8), and (9) retain the same branch-labelled
structure. Slice minimization, earliest causal arrival, and choosing a physical detected route are
different operations.

## 9. Causality and ownership

Every future-null result above has `T_r>T_e` and lies on the metric light cone. Nothing in G340
models or exploits an instantaneous substrate signal. The founding “infinite c” intuition can be
an interpretation behind the emergent metric response, but the operational equations here are
ordinary causal null geometry.

No Maxwell field is needed to answer *when a metric-null route reaches an observer* or *what
normal-observer frequency ratio that route has*. A field/source/detector model would be required to
predict whether a signal is emitted, its intensity, polarization, spectrum, absorption, or
detection. Those questions are outside G340.

Production passed `3868/3868` nonlinear analytic and quadrature checks. An implementation-distinct
direct four-metric reconstruction using Gauss--Legendre integration and bisection, importing no
production code or result, passed `5988/5988` checks. This is implementation-distinct, not
premise-distinct.

A fresh sealed external `gpt-5.4` review authenticated all 35 manifest payloads, independently
rederived the bounded metric-null chain, replayed the registered checks, and returned
`ACCEPT_G340_BOUNDED_FINITE_PAIR_RELATION_CLASSIFICATION` with no finding at any severity and no
required repair.

The metric, reciprocal kernel, angular sector, and provisional equation are unchanged. No physical
distance protocol, observer/path population, occupancy, scale, `X_max`, or canon is selected.
