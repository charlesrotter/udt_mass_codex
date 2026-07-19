# Reciprocal Clock–Optical–Scale Selector

## Result

`RECIPROCAL_CLOCK_OPTICAL_LINK_DERIVED_SCALE_REALIZATION_AND_MASS_OPEN`

The owner's intuition is substantially right in the reciprocal static sector:

> Time dilation, redshift, ruler dilation, and effective optical speed are different operational readings of one dilation field.

They are not universally or numerically identical. Time dilation supplies the clock factor; UDT Reciprocity supplies the paired ruler factor. Both are needed to obtain the effective coordinate slope.

## The basic distinction

Write a static radial metric as

\[
ds^2=-N^2c_0^2dt^2+B^2dr^2.
\]

For the supplied static worldlines and their orthogonal radial slice,

\[
d\tau=Ndt,
\qquad
dL_{\rm prop}=B|dr|,
\]

and a metric-null curve obeys

\[
\left|\frac{dr}{dt}\right|=c_0\frac{N}{B}.
\]

A metric-normalized orthonormal observer assigns

\[
\left|\frac{dL_{\rm prop}}{d\tau}\right|=c_0.
\]

Thus `N` alone does not determine an effective coordinate speed. The relative clock-to-ruler response `N/B` does.

## Why Reciprocity matters

Three metrics can have the same clock factor `N` and different ruler factors:

| Ruler response | `B` | Coordinate slope | Optical stretch `B/N` |
|---|---:|---:|---:|
| Time only | `1` | `c0 N` | `1/N` |
| Common scale | `N` | `c0` | `1` |
| UDT reciprocal | `1/N` | `c0 N^2` | `1/N^2` |

These are distinct response functions and give distinct numerical slopes for nontrivial `N!=1`; at the neutral anchor `N=1` they coincide. This is an exact counterexample to the universal statement “time dilation equals a change in light speed.” A common clock-and-ruler dilation changes both proper units but leaves the coordinate null slope unchanged. Under CSN it is precisely the pointwise ratio that survives.

UDT's conditional reciprocal representative instead has

\[
N=e^{-\phi},
\qquad
B=e^{+\phi}=N^{-1},
\]

so

\[
c_{\rm eff}=c_0N^2=c_0e^{-2\phi},
\qquad
q_{\rm opt}=\frac{B}{N}=N^{-2}=e^{2\phi},
\qquad
c_{\rm eff}q_{\rm opt}=c_0.
\]

The apparent speed change is therefore the squared clock effect because the ruler changes reciprocally at the same time.

## Redshift is linked, not identical

For static Killing observers at emitter `e` and observer `o`, the locally measured frequency is inversely proportional to the lapse. Therefore

\[
1+z=\frac{\omega_e}{\omega_o}=\frac{N_o}{N_e},
\qquad
\frac{d\tau_e}{d\tau_o}=\frac{N_e}{N_o}=(1+z)^{-1}.
\]

For general independent rulers,

\[
\frac{c_{{\rm eff},e}}{c_{{\rm eff},o}}
=\frac{N_e}{N_o}\frac{B_o}{B_e}.
\]

Under UDT Reciprocity, `B=1/N`, so

\[
\boxed{
\frac{c_{{\rm eff},e}}{c_{{\rm eff},o}}=(1+z)^{-2}
}
\]

and

\[
\boxed{
\frac{q_{{\rm opt},e}}{q_{{\rm opt},o}}=(1+z)^2.
}
\]

These two boxed component ratios require one pinned adapted `NB=1` representative with the same specified reciprocal radial coordinate standard and Killing normalization at emitter and observer. Under a radial reparameterization with endpoint Jacobians `J_e` and `J_o`, the slope ratio acquires `J_o/J_e` and the optical-component ratio acquires `J_e/J_o`. Integrated optical length remains invariant when flow, path, and normalization are fixed.

There is also a CSN representative gate. `NB=1` is not preserved by a radial reparameterization, a time normalization change, or a local common rescaling. An endpoint-dependent common rescaling changes the lapse ratio by `Omega_o/Omega_e`. Physical redshift therefore requires either a selected post-scale representative or a derived transformation/coupling rule for material emitter and receiver clocks. Before that selection, the formulas are conditional metric/Killing readouts rather than CSN-class physical-redshift theorems.

If a scale label is introduced, emitter and observer must also use the same operational scale `sigma`, or UDT must supply an explicit `sigma_e`/`sigma_o` comparison and coupling rule.

With those pins, this is the precise content behind “redshift, time dilation, and effective speed are the same thing”: they share `N`, but clocks carry one power while reciprocal optical propagation carries two. They are linked but not numerically identical.

These are static-sector identities. An expanding cosmology generally has no global timelike Killing generator, so the CMB and cosmological redshift require a time-live derivation rather than direct promotion of this formula.

## What happens to mass

The kinematics do not derive a local mass increase—and they do not derive native invariant-mass constancy either. As a standard fixed-mass comparison branch, assume a constant local rest parameter `m`, standard `hbar`, and conventional local matter-clock coupling. Then

\[
E_{\rm rest,local}=mc_0^2,
\qquad
\omega_C=\frac{mc_0^2}{\hbar}
\]

are the comparison-branch local metric-frame values. This is not yet native UDT matter physics.

For a static rest worldline at the emitter, the energy conjugate to coordinate time is

\[
E_K=N_e mc_0^2.
\]

Relative to the observer's normalized clock, the corresponding remote assignment is

\[
E_o=\frac{E_K}{N_o}
=mc_0^2\frac{N_e}{N_o}
=\frac{mc_0^2}{1+z}.
\]

A null covector with conserved Killing frequency obeys the same static redshift relation,

\[
E_{\gamma,o}=\frac{E_{\gamma,e}}{1+z}.
\]

Calling this a physically received photon energy additionally assumes emission, propagation, and detection couple to the selected metric cone—an open material-coupling theorem. Multiplying such a received energy by `(1+z)` reconstructs the comparison source-frame energy; it does not show that the source's invariant rest mass increased.

The honest mass ruling is therefore symmetric: neither mass increase nor invariant mass constancy is derived. Rest, inertial, and gravitational mass dependencies all remain open to a specified native action, source, carrier coupling, or operational inference rule.

## Position is not resolution scale

The previous WR-L result concerned position `r`. The owner's new clarification concerns separation or probe scale `sigma`. Proper radial length is denoted `L_prop`; none of `r`, `L_prop`, and `sigma` may be silently identified.

At one spacetime event, an ordinary local metric `g_mu_nu(x)` has one null cone. If different probe scales at that same event have literally different cones, additional multiscale, Finsler, constitutive, bilocal, or effective geometry would be required, for example

\[
g_{\mu\nu}(x;\sigma).
\]

That is not the unique architecture. Effective scale-dependent optics might instead arise from a single metric plus a scale-dependent observer/line/readout or a nonlocal travel-time/constitutive kernel, without literal multiple local cones. UDT must say operationally what selects `sigma`, what geometric or readout law uses it, and—if physical universality is claimed—why matter and signals couple to that law consistently.

Conditionally, if

\[
N(x;\sigma)=e^{-\phi(x;\sigma)},
\qquad
B(x;\sigma)=e^{+\phi(x;\sigma)},
\]

then the owner's three regimes are kinematically coherent:

- UV, under a specified operational ordering of `sigma`: `phi(x;sigma)<0`, giving an adapted coordinate slope `c_eff>c0`;
- ordinary region: `phi(x;sigma) approximately 0`, giving `c_eff approximately c0`;
- IR/cosmological, under that ordering: `phi(x;sigma)>0`, giving an adapted coordinate slope `c_eff<c0`.

If paired scales obey

\[
\phi(x;\sigma^\vee)=-\phi(x;\sigma),
\]

then

\[
c_{\rm eff}(x;\sigma)c_{\rm eff}(x;\sigma^\vee)=c_0^2.
\]

This is a clean candidate for scale Reciprocity. Genuine scale Reciprocity additionally needs an operational involution and domain, a consistent event/observer frame, any fixed point or pivot, and a coupling rule. None is selected.

## GR-like middle regime

The executable algebra proves only the exact neutral anchor `phi=0`, where `N=B=1`, `c_eff=c0`, and normalized optical stretch is one. A broad `phi approximately 0` plateau is an owner hypothesis whose breadth, thresholds, and error bounds were not tested. Such a plateau would be necessary for the proposed GR overlap, but not sufficient. Matching GR at those scales also requires the correct field equations, matter coupling, equivalence behavior, and precision limits. This derivation supplies no such phenomenological proof.

## The one-sided fallback

If the UV branch never exceeds `c0`, then in the reciprocal one-sided domain `phi>=0`,

\[
c_{\rm eff}=c_0e^{-2\phi}\le c_0,
\qquad
q_{\rm opt}=e^{2\phi}\ge1.
\]

In that pinned adapted-coordinate language, `c0` is the **coordinate-slope ceiling**, not the speed floor. Unity is the floor of the pinned optical-density normalization. Neither is an invariant material signal-speed ceiling or scalar optical floor. Conversely, an adapted coordinate value `c_eff>c0` by itself does not imply superluminal signalling. A genuinely widened material cone would require hyperbolicity, a common causal order, coupling, and intervention-level no-signalling proof.

## Adjudication

The conditional static reciprocal representative has a reciprocal square law. Extending it to relational scale or cosmology is an open owner hypothesis, not a result of the static calculation.

No unique smallest architecture has been selected. The conditional obligation set is:

1. retain the still-open clock flow, parallel line, post-scale representative, and normalization selectors;
2. define an operational relational scale `sigma`;
3. derive the geometric or readout law—single-metric/nonlocal or genuinely multiscale—that uses it;
4. define the same-scale endpoint comparison or a cross-scale coupling rule;
5. if universal material propagation is claimed, derive matter/signal coupling and causal compatibility.

Only after those obligations are met is it meaningful to choose a UV/IR profile or decide whether the UV infinity represents a coordinate optical effect, a controllable signal cone, or a pregeometric limit. Observable superluminal signalling remains unauthorized.
