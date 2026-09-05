# G352 exact derivation — clock-rate carried-measure readout

Date: 2026-09-05
Status: `REPAIRED_DERIVED_CONDITIONAL_BOUNDED_PENDING_EXTERNAL_FOLLOWUP`

## 1. Exact premise and domain

Charles provisionally adopted:

> On a supplied conserved sequence of causal phase/event crossings, the local clock-rate readout is
> crossings per observer proper time per metric sheet area.

Use one explicitly chosen continuous phase-intensity realization of that premise. Let `Lambda` be
the transverse label space and let `Theta` be a supplied dimensionless phase with nonzero
future-raised null gradient on the retained family. With signature `(-,+,+,+)`, choose

\[
 k_a=\nabla_a\Theta,
 \qquad g^{ab}k_ak_b=0,
 \qquad \omega_i=-u_i^ak_a>0.
\tag{1}
\]

Then `dTheta/dtau_i=-omega_i`. For one fixed supplied spacing `DeltaTheta>0`, define the continuous
total-phase count coordinate by `dN_cont=|dTheta|/DeltaTheta`. Its positive local intensity is
therefore

\[
 \rho_i={dN_{\rm cont}\over d\tau_i}
        ={|d\Theta/d\tau_i|\over\Delta\Theta}
          ={\omega_i\over\Delta\Theta}.
\tag{2}
\]

Equation (2) uses metric proper time and metric-measured frequency. It is not the ordinary
instantaneous derivative of a literal atomic crossing count or discrete step-count. A literal
sequence of fixed levels has
the atomic counting measure `sum_n delta_(Theta_n)` and no everywhere-smooth instantaneous rate
unless an averaging, random-offset, interpolation, or coarse-graining premise is added. That atomic
branch remains distinct and open.

The existence, normalization, and population of the phase object are supplied; the metric does not
generate them. An endpoint observer tangent fixes the local intensity for a worldline extension
with that tangent. It does not supply a global worldline or guarantee that every phase level lies in
the worldline's range.

For this bounded calculation, choose the nonnegative product measure

\[
 d\Xi={|d\Theta|\over\Delta\Theta}\otimes d\mu,
\tag{3}
\]

on the explicitly supplied product measurable space of phase and transverse labels. Here `mu` is
G351's supplied finite nonnegative countably additive transverse label measure, the same on
source-free cuts. The common fixed spacing, the same `mu` on every phase slice, phase-independent
support and weight, no phase--label correlation, label preservation across the compared cuts, and
measurable cut/frequency maps are a `CHOSE_BOUNDED_MATHEMATICAL_REALIZATION` / supplied query
condition. They are not derived from G351 or the metric and are not a new owner or canonical
physical premise. A phase-dependent measure family would replace the product form and remains open.

## 2. Regular-cut clock-rate density

On a regular label chart, decompose the absolutely continuous part of `mu` as

\[
 d\mu_{\rm ac}=s(\lambda)d\lambda,
 \qquad dA_i=J_i(\lambda)d\lambda,
 \qquad J_i>0.
\tag{4}
\]

G351 gives the observer-neutral density

\[
 n_i={d\mu_{\rm ac}\over dA_i}={s\over J_i}.
\tag{5}
\]

The adopted clock-rate readout, in this chosen continuous realization, is the amount in (5) carried
per unit observer proper time:

\[
 \boxed{\Gamma_i={\omega_i\over\Delta\Theta}{s\over J_i}.}
\tag{6}
\]

For the same nonzero absolutely continuous component at two regular cuts,

\[
 {\Gamma_j\over\Gamma_i}
 ={\omega_j\over\omega_i}{J_i\over J_j}
 =R_{ji}A_{ji}^{-1}.
\tag{7}
\]

Thus this specific readout has the G350 character weights

\[
 \boxed{(p,q)=(1,-1),\qquad T_{\rm clock}=RA^{-1}.}
\tag{8}
\]

The area weight was already fixed conditionally by G351. G352 fixes `p=1` only because the adopted
readout is realized here as a continuous total-phase rate per observer proper time. It makes no
smooth-rate statement about the literal atomic crossing branch.

## 3. Bounded uniqueness and non-universality

Inside G350's declared full independent positive character domain, compare a general character
`R^a A^q` to (7). Equality for every independent positive `(R,A)` gives

\[
 R^{a-1}A^{q+1}=1.
\tag{9}
\]

Setting `A=1` and varying `R` forces `a=1`; setting `R=1` and varying `A` forces `q=-1`. This is
uniqueness for the adopted clock-rate readout inside that bounded class, not selection of one
universal observer weight.

In particular:

- `n_i=s/J_i` remains the distinct observer-neutral density with `p=0`;
- a different declared observer-weighted quantity can still have another `p`;
- no energy or per-crossing value law has been supplied, so no energy-like weight follows.

## 4. Phase normalization and observer covariance

Under a common positive phase-coordinate rescaling

\[
 \Theta\mapsto b\Theta,
 \quad k\mapsto bk,
 \quad \omega_i\mapsto b\omega_i,
 \quad \Delta\Theta\mapsto b\Delta\Theta,
\tag{10}
\]

both `omega_i/DeltaTheta` and `Gamma_i` are invariant. A common phase translation is also harmless.
A general nonlinear reparameterization does not preserve fixed increments and is not covered. No
phase unit or absolute physical scale is selected.

Under an independent finite change of endpoint observer at cut `i`, G347 gives
`omega_i -> D_i omega_i` with `D_i>0`, while the intrinsic labelled sheet area is unchanged. Hence

\[
 \Gamma_i\mapsto D_i\Gamma_i,
 \qquad
 T_{ji}\mapsto {D_j\over D_i}T_{ji}.
\tag{11}
\]

This is observer covariance of weight one. It selects no preferred observer.

## 5. Identity, reversal, and sewing

Because frequency and area ratios are multiplicative,

\[
 R_{ki}=R_{kj}R_{ji},\qquad A_{ki}=A_{kj}A_{ji},
\tag{12}
\]

equation (8) gives exact sewing

\[
 T_{ki}=T_{kj}T_{ji}.
\tag{13}
\]

At identity `T=1`; comparison reversal gives `T_ij=T_ji^{-1}`. This algebraic reversal is not
backward causal propagation: the supplied sheets and observers remain future-directed.

## 6. Measure-valued rank-loss statement

At cut `i`, define the positive continuous-intensity measure on the endpoint image by

\[
 \nu_i(B)=\int_{X_i^{-1}(B)}{\omega_i(\lambda)\over\Delta\Theta}\,d\mu(\lambda).
\tag{14}
\]

If the measurable weight `omega_i/DeltaTheta` is integrable against finite `mu` on the retained
patch, `nu_i` is finite.
Equation (14) remains meaningful when `X_i` loses rank or is many-to-one. On a regular sheet its
absolutely continuous density is exactly (6). At a caustic that ordinary area density can diverge
or become singular even though (14) remains finite.

Pushforward preimage accounting is mathematical additivity of the supplied measure. It is not a
detector rule, physical incoherent sum, cancellation, or interference law.

## 7. Sources and physical ceiling

If `mu=0`, both `Xi` and every `nu_i` vanish. The readout cannot create a phase object, populate
labels, or determine a source magnitude or time profile. A varying phase-sheet measure, literal
atomic crossings, sources or sinks, absorption, and cross-label interactions require distinct or
additional premises.

The exact bounded landing is:

```text
OWNER_PROVISIONAL_CLOCK_RATE_READOUT
__CHOSE_CONTINUOUS_TOTAL_PHASE_INTENSITY_AND_PHASE_INDEPENDENT_LABEL_PRODUCT
__P_EQUALS_ONE_AND_Q_EQUALS_MINUS_ONE_ONLY_FOR_THIS_READOUT
__T_CLOCK_EQUALS_R_A_INVERSE
__PHASE_NORMALIZATION_OBSERVER_COVARIANCE_SEWING_AND_REVERSAL_CLOSE
__INTEGRABLE_RATE_MEASURE_SURVIVES_CAUSTIC_RANK_LOSS_WHILE_DENSITY_NEED_NOT
__LITERAL_ATOMIC_CROSSING_COUNT_P_ZERO_DENSITY_AND_OTHER_READOUT_WEIGHTS_REMAIN_DISTINCT
__NO_LIGHT_ENERGY_DETECTOR_DISTANCE_HISTORY_SCALE_XMAX_MATTER_MASS_OR_CANON
```

This is not a native light, photon, energy, brightness, flux, luminosity, distance, detector,
source, population, history, matter, mass, scale, `X_max`, or canonical law. It is conditional on
the explicit continuous product realization as well as Charles's provisional readout premise. The
metric, reciprocal kernel, angular sector, and owner-provisional vacuum response equation are
unchanged.
