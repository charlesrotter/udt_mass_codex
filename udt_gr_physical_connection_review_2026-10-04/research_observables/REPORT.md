# GRL1 lane 3: joint observables and the positional connection

**DRAFT SOURCE-FIRST RESEARCH RETURN; not yet adversarially reviewed.**

Joint drift and distance information can separate some kinematic and curvature
contributions in a supplied geometry. Within these four papers and the checked
UDT sources, it does not identify which recovered quantity is the additional
positional contribution or require a particular value/sign of that quantity.
Two conditional leads are retained below. Neither closes that physical join.
This is a bounded finding, not a missing-postulate necessity theorem or a
whole-UDT insufficiency claim.

## Authority, frame and exposure

I independently observed branch `grok`, HEAD
`865a116365f8274c3706f4d3c0a5dfeecf51e4ac`, no tracked modification at entry,
and existing untracked names plus this active package. Parent startup/sync and
the prior normal/57-maintenance/full406 results are attributed to BASELINE.json,
not rerun or independently certified here. I read the on-disk method authority,
triggered skills, work order, bounded central sections and exact sources listed
in SOURCES.json. Old derivations/verdicts were exposed; no sibling report or
parent synthesis was read. The exact deployed model revision is unavailable.

The scientific antecedents are the owner's one-geometry positional meaning,
ordinary local clocks, the additional-effect clarification, W4's working metric
coupling, and the conditional R6/R7 interface. Universality means a common law
with circumstance-dependent comparisons. It does not mean one numerical drift
for every observer. No GR field equation, observer population, photon theory,
flux law, source law or preferred frame is introduced. DDR does not identify
its response with a curvature measurement. c_E remains observed calibration;
X_max remains working/open and inactive locally.

Question and test scope were frozen in TEST_FREEZE.md after exploratory hand
work and before this report. This was mathematical discovery, not blind
preregistration. All examples are supplied off-equation controls, not admitted
UDT histories. No scientific program, fit, GPU work or protected payload access
occurred. Bookkeeping hashes certify source correspondence only.

## Four-paper evidence, with limits

1. Heinesen–Korzyński, [2406.06167v1](https://arxiv.org/html/2406.06167v1),
   §§II–IX, Appendix B: a single source/observer congruence, regular null
   optics, a nonrotating reference frame and controlled local series support
   joint inference. Its principal displayed cosmography takes geodesic clocks.
   Equations (25)–(26) give the drift slope; the monopole is
   `m = -Ric(U,U)/3 + sigma_ab sigma^ab/5 + omega_ab omega^ab/3`.
   Section IX uses additional observables to separate these terms. Section VII
   corrects spatial-Ricci signs in the older papers, but its own (26) and IX
   retain the older-looking minus/plus combination. PDF text pp.6,8,9 confirms
   this internal sign tension. I quarantine the disputed quadrupole; the
   monopole and the flat test below do not use it. I have not independently
   rederived the complete second-order expression. No universal convergence or
   unique-spacetime reconstruction is taken from this paper.

2. Heinesen, [2011.10048v1](https://arxiv.org/html/2011.10048v1), §§II–IV,
   equations (1)–(16): (2)–(4) differentiate the actual clock correspondence;
   (6)–(8) express drift as endpoint directional expansion plus a spatial-energy
   contribution. The latter is not generically zero. The multipole calculation
   further supplies an irrotational null congruence. Statistical cancellation in
   §IV has population and sampling hypotheses. These are geometry/kinematics
   methods, not a native selection law. I do not import its averaging model.

3. Heinesen, [2107.08674v2](https://arxiv.org/html/2107.08674v2), §§II–V,
   equations (4), (8)–(18): the exact drift integrand includes position drift,
   acceleration and curvature. The redshift series requires a regular local
   inverse of affine distance versus redshift. Equations (16)–(18) impose the
   geodesic/position-drift-free approximation; it is not a consequence of common
   metric coupling. Section IV.1's positive-drift curvature inference has
   kinematic qualifications; identifying curvature with an energy condition
   adds Einstein dynamics. The spatial-Ricci signs in (10),(17) are expressly
   corrected by the 2024 paper. I use neither disputed coefficient nor its
   survey estimates as UDT input.

4. Heinesen, [2010.06534v2](https://arxiv.org/html/2010.06534v2), §§2,3,5:
   the screen focusing equation (2.14; HTML (14)) is geometric. The next
   equations define bolometric luminosity distance and use conserved photons
   to connect it to angular distance. These are distinct assumptions. The
   local expansion has `d_A=z/H(e)+O(z^2)` where its inverse exists. Section 5
   discusses regularity, peculiar velocities and error limits; finite
   differentiability alone does not control a chosen finite-redshift truncation.
   I use the local inverse-function condition `H(e)!=0`, not the paper's
   stronger wording equating general invertibility with a nowhere-zero
   derivative. Its corrected shear equation is not used in the tests.

These notes are scoped paraphrases; no complete paper was downloaded or copied.
HTML equation numbering differs from section-numbered numbering in the last
paper. SOURCES.json records precisely which pages/sections were accessed and
which were not fully reconstructed.

## Lead O1: joint drift as a corrected curvature diagnostic

**UDT antecedent.** W4 plus ordinary clocks and R6 permits one actual
received-clock ratio for a specified metric, emitter, receiver and regular
null correspondence. Comparing neighboring reception events is then ordinary
differentiation of that ratio. It requires no new light-speed function.

**Bridge.** For a supplied smooth geodesic congruence with regular local
redshift coordinate, let `s(e)=lim_(z->0) (dz/dtau_o)/z`,
`H(e)=theta/3+sigma(e,e)`, and let angle brackets mean the exact uniform
mathematical average over the rest sphere. The above leading-order formula
gives

    M = <H(e)s(e)> - sigma_ab sigma^ab/5 - omega_ab omega^ab/3
      = -Ric(U,U)/3.

This averages the product; averaging drift alone or dividing averaged
quantities is different. Acceleration must vanish in a neighborhood for this
geodesic-congruence formula; setting only its value to zero at one point does
not remove acceleration gradients. A finite survey would additionally need
measured preparation/population, angular coverage, distance calibration,
frame rotation and truncation/error control. Those are not supplied here.

**Conditional geometric consequence.** If the corrected M for this protocol
is positive, then Ric(U,U)<0. A measured M recovers that contraction. Neither
statement selects a geometry, fixes a curvature scale, identifies DDR's
response, or asserts the condition for all timelike U.

**Failed stronger inference, checked directly.** Positive raw redshift drift
does not by itself force negative Ricci, even with geodesic emitters and receiver.
In Minkowski coordinates use the local inertial congruence

    X(t,q)=q+t Bq,   B=diag(2h,h,h), h>0.

Restrict |Bq|<1 and det(I+tB)>0, so its proper velocities are smooth,
single-valued and timelike. Each worldline is straight, hence a=0 and Ric=0.
At the receiver (t,X)=(0,0), expansion gradient is B,
`sigma=diag(2h/3,-h/3,-h/3)`, and vorticity is zero.

Here is an arrival-map check independent of the published curvature expansion.
For a source received at that event from direction n and coordinate emission
distance r, its emission time is -r, label is
`q=(I-rB)^(-1)rn`, and constant velocity is `v=Bq=rBn+O(r^2)`.
The inertial receiver measures

    Z=gamma_v(1+n.v),
    dn/dt_o=(I-nn^T)v/[r(1+n.v)],
    dZ/dt_o=gamma_v |(I-nn^T)v|^2/[r(1+n.v)].

Thus `z=r n.Bn+O(r^2)`, and
`H(n)s(n)=|(I-nn^T)Bn|^2` in the r->0 limit. Spherical moments give

    <H s> = tr(B^2)/3 - [(tr B)^2+2 tr(B^2)]/15
          = tr(sigma^2)/5 = 2h^2/15 > 0,

while M=0 and Ric=0. H(n)=h(1+n_1^2)>0, so the inverse-redshift domain is
regular. This is a local analytic control, not a fitted cosmological profile.
It tests a failure of the raw-sign inference; it does not refute the published
approximation when its position-drift omission is valid.

A second elementary control allows acceleration: an inertial receiver and a
radially receding flat-space emitter of rapidity r(tau_e) have
`Z=exp(r)` and `dZ/dtau_o=dr/dtau_e`. Positive drift can therefore also occur
with zero curvature through acceleration. This does not evade ACI1: its
accumulated-acceleration control would have to be checked separately.

**Physical join and overlap.** Calling M, its sign, or a matched M difference
the positional effect adds the same type of identification left open at PSW/J1.
The owner's asymptotic slowing target is not a local drift-sign statement:
derivatives along observer time, variation of source separation, and a declared
asymptotic family are different quantifiers. PSW already yields a prepared
Ric(U,U) measurement without a cosmic population. O1 supplies a complementary
method for a different preparation, not a new physical restriction. No
PCC all-frame identical contribution follows. **Ceiling: conditional diagnostic;
native attribution OPEN.**

## Lead O2: distance/optical consistency with clock curvature

**UDT antecedent and bridge.** R13/G348 already gives an intrinsic quotient
screen, self-adjoint Jacobi tide and reciprocal metric angular areas. R6 supplies
the endpoint clock-frequency ratio. The optical focusing equation in the fourth
paper is a scalar consequence of that same Jacobi geometry on a regular
twist-free beam. A specified angular-area distance can be used without asserting
that it is a bolometric luminosity distance.

**Consequence and limitation.** Clock, angle and area records must agree with
their common supplied metric and protocol. A measured bundle can constrain
null curvature contractions; suitable timelike clock data can complement them.
These consistency relations hold for arbitrary regular comparison geometries
at their declared scope. Requiring the identities supplies no new restriction
on UDT geometry.

**Hand failure test.** In the constant-curvature algebraic tensor

    R(X,Y)Z=kappa[g(Y,Z)X-g(X,Z)Y],

`R(X,k)k=0` for screen X perpendicular to null k. Also Ric=3kappa g and
Ric(k,k)=0. For a unit timelike U and spatial unit n,
`g(R(n,U)U,n)=-kappa`. Thus the scalar-curvature channel can be absent from
the null screen tide while present in a timelike prepared-clock tide. This is
not a claim that every optical/redshift record of distinct space forms agrees:
endpoint clocks, affine normalization, paths and distance-redshift conversion
matter. It refutes only an attempted determination of that channel from the
null optical curvature contraction alone.

**Additional premises.** Interpreting conserved labels as photons, assigning
per-crossing energy, specifying emission luminosity and converting detector
energy flux to distance are extra physical identifications. G351 provisionally
conserves a supplied label measure; G352's specified continuous clock-rate
readout gives R A^-1, not an energy-flux law. G350 permits distinct observer
weights for distinct quantities. The paper's luminosity duality cannot silently
choose those weights or populate sources. No such physical input is adopted.

**Overlap and ceiling.** R13/R14 already own this boundary. ECS's aligned-sheet
timing ambiguity is not an all-direction optical degeneracy; added transverse
observations may distinguish its mimics. PCC's isotropic curvature difference
is exactly the algebraic channel annihilated by a null-screen contraction at
the matched point, but PCC remains an unadopted all-frame trial. This lane
does not establish full joint-observable uniqueness. **Ceiling: consistency/
measurement method; no new positional restriction.**

## Explicit comparison with earlier joins

| Existing result | What the literature changes here | What remains open |
|---|---|---|
| NCI1 | Direction-resolved drift can probe congruence derivatives; no endpoint factorization was assumed. | Neither joint measurement nor W4 supplies `exp(-Psi)U` conformal Killing, zero shear, or exact alpha. |
| PSW/J1 | O1 is a distinct population/congruence preparation and recovers a related Ricci contraction. | Net or corrected contraction is not automatically the added positional effect. |
| ECS1 | Optical and transverse data enlarge the record beyond the restricted sheet. | No full-metric uniqueness, universal echo condition or native metric is selected. |
| PCC1 | Clock and null-screen channels respond differently to its conditional isotropic difference. | Common laws do not require identical all-frame numerical contribution or supply matching. |
| R13/R14 | Literature luminosity formulas expose photon and energy-flux identifications explicitly. | Conserved abstract content and clock rate do not by themselves provide those identifications. |
| ACI1 | Local drift identities add no controlled global sweep/preparation family. | Asymptotic realization and positional/net assignment remain necessary to use its finite bound physically. |

The smallest next action supported by this lane is to retain the corrected
observable diagnostic and its counterexample during the parent review, while
asking any proposed physical connection to specify which actual family and
which measured or matched coefficient it constrains. There is no supported
reason here to start an observational campaign, impose a Hubble profile, infer
an energy condition, or select another cosmological model. Return for the
authorized synthesis and two fresh adversarial reviews.
