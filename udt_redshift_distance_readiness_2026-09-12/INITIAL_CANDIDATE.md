# ZDR1 initial conditional checkpoint — UNPROMOTED, review pending

Snapshot: grok at892546169db5a63f39244c7388bde7e72e667017. Source pins and
FRAME_AND_EXPOSURE control provenance. This is a bounded synthesis/application,
not a claim of new geometric mathematics or a new physical light law.

## 1. Landing and what has advanced

The newer results close more of the geometric evaluation, but do not yet provide
a native numerical redshift–distance curve. They support a useful conditional
comparison between redshift, forward/reverse beam areas and brightness, and a
precise local-to-finite-duration gate. Neither relation singles out expansion
or UDT. No observational fit is run or proposed as already ready.

| Accepted source | Contribution to this checkpoint | Remaining boundary |
|---|---|---|
| G280/G281 | Depth/projective state can agree while beam area differs; earlier SNe work is reconstruction/calibration and conditional cross-release checking | No independently predicted physical distance curve |
| G348 | Forward/reverse infinitesimal metric areas have exact frequency reciprocity for arbitrary supplied smooth Lorentz geometry | Physical optical interpretation, observers, path and history remain supplied |
| G349 | Finite null-map sheet area can be calculated with multiplicity and rank strata | Sheet area is not finite-source flux or an unresolved-image detector rule |
| G351/G352 | Conserved label density and the chosen continuous clock-rate product are precisely typed | Neither identifies energy flux, light or a supernova envelope |
| G402/NCI1 | Exact criterion for compressing all local null-clock ratios into one endpoint scalar | The criterion does not choose a history, require compression, or imply non-expansion |
| G220 | Exact proper-clock arrival derivative on a supplied regular null correspondence | Physical feature transport and a stable source-clock standard remain additional |

G348/G349 remove a former restriction to special geometry and local area bookkeeping;
they do not remove the need for complete geometry. G402 shows why replacing every
directional null query by one endpoint depth is itself a substantive restriction.
These are advances relevant to the main metric/kernel roadmap even if no catalog
comparison follows now.

## 2. Sign, path and area conventions

Use emitter e and observer o, future affine tangent k and future metric-unit U:

    omega_i = -g(U_i,k_i)>0,    Z = omega_e/omega_o = 1+z.

The Z identification with a measured spectral redshift is a supplied optical
identification. G220's ordered null-query depth is

    delta_eo = log(omega_o/omega_e) = -log Z.

Do not silently replace that by the historical catalog-oriented positive depth.
For NCI1's static control N=exp(-phi), Z=N_o/N_e=exp(phi_e-phi_o).
For its conformal-time control g=a(eta)^2 eta_flat with comoving U,
Z=a_o/a_e. Both can admit an endpoint potential. General supplied histories need
not: NCI1's all-short-null-directions scalar property holds precisely when
exp(-Psi)U is conformal Killing, equivalently zero shear and exact
alpha=a_flat-(div U/3)U_flat. Local closedness and global exactness remain distinct.

On one regular branch with rank-two Jacobi position block B, let

    A_oe = dA_o/dOmega_e,    A_eo = dA_e/dOmega_o.

These are directional infinitesimal metric-area Jacobians, not yet measured
distances. In orthonormal quotient frames G348 gives

    A_oe = omega_e^2 |det B|,
    A_eo = omega_o^2 |det B|,
    A_oe = Z^2 A_eo.                                      (1)

The metric density factors restore the same result in general screen coordinates.
Common affine normalization cancels. At conjugate rank loss both areas vanish;
the division-free equality survives, while their ratio and positive-distance
chart are not defined. Full symplectic propagation is retained. Different path
labels, observers or unresolved-image sums are not silently mixed.
The reversed area is an endpoint-map comparison, not backward causal signalling.

## 3. The conditional brightness bridge and the missing energy factor

Supply the following ordinary optical model only as a comparison contract:
the measured rays and spectral frequencies realize the same null geometry;
emission is locally isotropic with known bolometric source luminosity L_e per
source proper time; transported quanta are conserved on this branch; their energy
ratio obeys E_o/E_e=omega_o/omega_e=1/Z; and the detector measures bolometric
energy per observer proper time per transverse area. Wave, absorption, finite-size,
bandpass, anisotropic-emission and multi-image corrections must be separately
justified before empirical use. No numerical bound for them is supplied here.

G220 supplies d tau_o/d tau_e=Z for the chosen correspondence. Direct accounting
for a small emitted solid angle gives

    dN_e = (L_e/E_e) d tau_e dOmega_e/(4pi),
    F_o = (dN_e E_o)/(d tau_o dA_o)
        = L_e/(4pi Z^2 A_oe)
        = L_e/(4pi Z^4 A_eo).                             (2)

If the optical angular-distance definition is independently justified as
d_A^2=A_eo, and luminosity distance is defined by F_o=L_e/(4pi d_L^2),

    d_L = Z^2 d_A.                                       (3)

The geometric part of the earlier imported relation is now available at G348's
general metric scope. The physical assumptions in (2) remain supplied. This is
the familiar transparent-optics distance relation, not a UDT-specific prediction
or a derivation of physical light. No Einstein equation or expansion law enters.

G352 alone cannot supply (2). Its chosen continuous readout scales as frequency
once per metric sheet area; it supplies no per-crossing energy law. In the
separately supplied quantum picture, number arrival rate contributes one factor
1/Z and energy contributes a second. Dropping the latter would give a different
observable and the wrong luminosity power. A G352 phase count cannot be relabeled
bolometric flux to recover the historical one-factor shortcut.

## 4. What remains testable after calibration

One conditional observable target is

    C_i = log(4pi F_i d_A,i^2 Z_i^4/L_i) = 0.              (4)

Its inputs must be attached to compatible branch/observer/optical definitions.
The angular-distance information must come independently of solving (3) from the
same brightness data. L_i must have independent source-standard calibration or a
frozen common standardized model with nuisance support. Estimating a single common
normalization from designated training data can leave held-out contrasts; giving
each target its own freely fitted luminosity does not. Indeed any positive triple
(F_i,d_A,i,Z_i) fits identically after choosing
L_i=4pi F_i d_A,i^2 Z_i^4. Arbitrary target-specific attenuation or calibration can
likewise absorb departures and must be independently controlled.

If justified hard logarithmic bounds exist, then measurement/transfer perturbations
obey the triangle bound

    |C_measured-C_true|
      <= u_F + 2u_A + 4u_Z + u_L + u_transfer,             (5)

where u_A bounds log d_A, not log area. Correlations are not assumed absent;
this is a conservative deterministic bound. Standard deviations cannot be used
as these hard bounds without an appropriate statistical treatment. Training and
shared calibration errors belong in the applicable budget and covariance model.
Equation(5) is conditional algebra, not an error certification of any dataset.

No eligible paired luminosity/angular-distance dataset is identified or loaded
here. A supernova brightness–redshift catalog alone does not supply an independent
d_A for (4). Building d_A from that same catalog using (3) merely checks the
reconstruction. A future qualified comparison would constrain this joint optical
contract; it would not by itself distinguish UDT, a nonexpanding history and an
expanding history that share the contract.

## 5. Complementary duration: exact correspondence and finite-event support

Let s be emitter proper time, and supply a C1 unique regular null correspondence
tau_o=f(s) over one whole event interval [s0,s1], with Z(s)>0. G220 applies at
each paired event, so

    f'(s)=Z(s),
    Delta tau_o = integral_[s0,s1] Z(s) ds.                (6)

This is an exact geometric endpoint-interval relation. For any fixed positive
reference Z0 and a supplied uniform bound |Z(s)/Z0-1|<=epsilon on that interval,

    |Delta tau_o/(Z0 Delta s)-1|<=epsilon.                 (7)

Thus a single spectral redshift predicts the finite clock-interval factor only
with support for its variation over the event. A pointwise frequency or local
phase period does not alone provide that finite bound. Equation(7) follows by
integrating the pointwise inequalities; no probability model or chosen cosmic
timescale is imported.

For a supernova width to instantiate these clock intervals, the emitted feature
definition and its population/calibration must be stable, observed bands must be
matched, and propagation/detection must preserve that feature with bounded shape
distortion. Even an affine arrival map cannot prevent a time-varying amplitude
transfer from changing a light-curve width or moving its peaks. G352's phase-
independent product readout supplies neither a varying source envelope nor such
feature transport. It is therefore not a ready supernova clock model.

An exact actual-metric control illustrates why the finite clause matters. In
Minkowski g=-dt^2+dx^2+dy^2+dz^2, emit from (t,x)=(s,0), 0<=s<=T.
Choose Z0>=1, epsilon>=0, T,D>0 and a receiving worldline parametrized by s:

    Z(s)=Z0(1+epsilon s/T),
    u=t-x=s,
    v=t+x=2D+Z0^2(s+epsilon s^2/T+epsilon^2 s^3/(3T^2)).

It is future timelike, x>0, and its proper-time derivative is
d tau_o/ds=sqrt((dt/ds)^2-(dx/ds)^2)=Z(s). Each emission and reception is joined
by the outgoing null branch. Contracting k=(1,1,0,0) with its normalized tangent
gives omega_o=1/Z(s), while omega_e=1. Consequently

    Delta tau_o=Z0 T(1+epsilon/2),                         (8)

although the initial spectral ratio is Z0. Z0=2, epsilon=1/5, T=D=1 gives
Delta tau_o=11/5 instead of2, within the epsilon bound. This is a supplied
accelerating observer control in flat geometry, not a cosmic mechanism, source
model or counterexample to G220. It establishes no physical supernova mismatch.

## 6. DES comparator and observational readiness

The already exposed White et al. v2 duration paper is a useful methods comparator,
not a UDT test. Its first procedure searches a dilation exponent; its precise
second estimate is explicitly a consistency check using a dilation-built reference.
Wavelength matching, peak normalization, population variation and selection remain
part of its measurement contract; sources/DES_METHOD_FACTS.md pins the distinctions.
The paper's reported outcome is not fresh confirmation for this checkpoint and
does not uniquely identify the physical origin of a redshift.

This checkpoint has no new SNe prediction score, calibrated cosmic distance,
Hubble parameter, preferred scale or physically selected nonexpanding history.
The G278 resolution-sensitive lead is not repaired by these identities. Its
data cannot become untouched holdout data again through a new label.

## 7. Roadmap return and maximum conclusion

The useful addition is a connected, explicitly conditional observation interface:
the same complete metric/query must supply spectral Z, both Jacobi areas and
the event-arrival map. Brightness and event width then require distinct physical
source/transfer/calibration support. Retaining full geometry exposes those inputs;
compressing it to one scalar depth does not recover them automatically.

The present return is the precise missing connection for a new redshift–distance
curve, together with the conditional target (4) and finite-duration gate (7).
To use a declared metric family for comparison, independently freeze its geometry,
observer/branch data and the remaining optical assumptions before examining test
outcomes. Such a conditional family need not select the whole universe. A native
prediction has the additional native-history/physical-selection boundary stated
by G281. No complete census or universal nonexistence is claimed here.

Recommend returning to metric/kernel expansion and attaching these three outputs
to the next separately authorized family question when practical. Do not start a
new profile fit, second survey, global cosmology solve or automatic followup.
This reviewed checkpoint, if accepted by its reviewer, remains UNPROMOTED and does
not upgrade sources, adopt standard optics or establish new physical identification.
