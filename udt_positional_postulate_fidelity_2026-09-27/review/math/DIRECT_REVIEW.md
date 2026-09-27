# Direct mathematical fidelity review

Initial verdict: **VERIFIED-WITH-CAVEATS** for the source-relative candidate at
SHA-256 `84ced7b9a9f483c4caee3b1e3eff246b429688a9f64596a0c386328e4c485961`.
One orientation definition and one authorization/interpretation clarification
are requested below. No incorrect displayed curvature formula, hidden adopted
GR equation, or native source promotion was found. This verdict does not certify
all UDT, endorse a new physical premise, or upgrade any source grade.

## Exposure and independence

The immutable source-first freeze predates candidate exposure. It includes the
reviewer's own Christoffel-to-Ricci-to-Einstein implementation and 20 exact checks.
Only after reporting that freeze did this context read the pinned CANDIDATE.md,
REPAIR_LOG.md, parent check_geometry.py and GEOMETRY_CHECKS.json. Source-first
argument independence and later candidate exposure are separate stages.

Reviewer `/root/postulate_math`; fresh separate context, inherited model with
exact variant unavailable; different-model independence UNTESTED. Source-first
implementation uses no repository scientific implementation. Parent and reviewer
independently chose the same standard connection-to-curvature route; this is
independent implementation of a common mathematical method, not an unrelated
argument or independently validated symbolic engine. Both use SymPy 1.13.1.

After exposure, G220/G265/G269/G301 exact source arguments were also read directly
to check the candidate's new load-bearing passages. The original source-first
pins are unchanged; DIRECT_REVIEW_PINS.json records these additional sources and
the actual candidate/code/output versions inspected. No protected payload was read.

## Adversarial findings

### R1: make the redshift-depth orientation self-contained

Section 2 writes 1+z=exp(delta_z) and chi_z=tanh(delta_z), while other passages use
directed delta. G220 defines delta_AB=-log(r_AB) with r_AB=omega_A/omega_B.
For A=source and B=observer, standard 1+z=r_AB, hence

    delta_z=log(1+z)=-delta_source_to_observer
           =V(source)-V(observer)     [matched static calibration].

The candidate's use of a separate subscript is compatible with this, so the
display is not itself false. But it does not define that subscript, leaving a
reader able to identify opposite orientations accidentally. Smallest repair:
state the equation above beside the table or in a short convention sentence.
Survivor: nonlinear redshift and directed clock depth are exactly compatible
once orientation and signal-query scope are retained. The independent supplemental
check explicitly confirms the lapse-ratio sign.

### R2: distinguish native deduction from authorized counterfactual exploration

The candidate's statements that a "specific ... requirement from positional
dilation" is needed before the next construction correctly guard a claim of
native derivation. They should not be read as forbidding all openly chosen,
unadopted modified-GR exploration until such a requirement has already been
derived. The owner's current direction permits considering modifications;
AGENTS explicitly allows authorized counterfactual exploration with declared
premises, resources and stops.

Smallest repair: in the candidate or accompanying lay decision brief, distinguish
(a) deriving a consequence of current postulates, from (b) evaluating an explicitly
chosen, motivated counterfactual change under a bounded work order. The latter
must disclose assumptions and retain postulate fidelity, causality, full-metric
and applicable consistency checks; passing them does not establish native
derivation, adoption or empirical truth. The present work order still excludes
choosing an actual correction tensor, so no such selection is required now.
Survivor: the placeholder H and three conceptual routes are valid scoping tools.

### No required mathematical repair to the primary/normalization distinction

The positive regular static spherical areal domain makes

    G^r_r-G^t_t=(log(AB))'/(r B)

exactly equivalent to AB constant on a connected interval. Constant time
rescaling sets that positive constant to one as a coordinate normalization;
fixed operational reference calibration must remain visible when comparing
readouts. A general radius regrading also changes the sphere coefficient,
so W1 pair completion is not equivalent to preserving the primary areal form.
This is a bounded geometric observation, not a universal covariant ansatz or
a new UDT equation. The candidate says so explicitly.

The full Einstein components, G=3a I for f=1+a r²+b/r, and the positive quartic
control's diagonal (5q,5q,10q,10q) are correct. The latter is not an Einstein
metric when epsilon,L,r are positive, but is not asserted to satisfy full DDR.
It therefore separates the ansatz from the Einstein condition without making
an all-postulates countermodel. The candidate retains this essential ceiling.

### No required repair to the flat-rate/finite-duration control

On the declared flat static matched query, equal clock rates give zero directed
depth and contrast, while positive separation and c_E give positive travel time.
This refutes only an added rate-mismatch-equals-duration claim, which the candidate
does not attribute to Charles. Its stronger editorial point also survives:
the scalar alone omits the calibrated dimensionful/null background carried by
the full metric and W4. No contradiction with the founding postulate, no need
to derive numerical c_E, no physical flat-universe admission, and no W5-to-proper-
distance identification follow. The revised paragraph explicitly preserves them.

### G301 and divergence distinctions are correct

For the specified G301 class, TF(a Ric+b Rg)=a TF(Ric). With nonzero a and DDR,
the vacuum metric condition is TF(Ric)=0 independently of b. Changing coefficients
can change a residual operator without changing that vacuum solution class.
The precision repair recorded in REPAIR_LOG.md is therefore justified. This
would not be the same statement if the condition were E=0 instead of TF(E)=0;
G301's generic and exceptional E=0 classes remain distinct. The candidate
explicitly retains DDR and avoids that conflation.

For the schematic external equation G+Lambda g+H=kappa T, constant couplings and
separate stress conservation imply divergence(H)=0 on solutions. This alone does
not assert an off-solution tensor identity. The candidate now states exactly
that distinction. No native source, correction, action, scale or response map
has been imported through the placeholder equation.

Current G312 authority remains filter-only. Local Metric Sufficiency does not
choose response order, curvature weight or G301 membership. The candidate
keeps membership unclosed and does not use its compatibility calculations to
restore the historical stronger GR principal-overlap authority.

## Checks actually performed

Before candidate exposure: 20 exact symbolic checks in the source-first script,
including generic A,B full Einstein components, primary specialization, angular
and Bianchi identities, vacuum/trace-balanced families, W1 normalization and
reconstruction, a nonreciprocal areal control, and the vacuous two-dimensional
Einstein tensor. Runtime 1.086 seconds; stdout/stderr and exact command preserved.

After candidate exposure: 8 supplemental exact checks in check_direct.py, runtime
1.182 seconds, using the reviewer's frozen generic tensor for the new quartic
control. The mutual-clock formula was independently obtained by solving the
unit-clock normalization equation, including the carried-screen reversal. The
G301 trace-free identity was checked on a general symbolic symmetric tensor.
The static redshift orientation was checked explicitly. All eight passed.

The parent's code and saved output were inspected: the claimed 29 checks and
full tensor construction correspond to the code. Its script was not rerun here,
because it writes outside this reviewer's allowed directory and the independent
geometry calculation already covers the load-bearing quantity. Parent replay
would be regression evidence, not another independence axis.

No full package replay, fresh external human review, global solution theorem,
time-live extension, empirical test or complete theory-admission check is claimed.
Prior source grades remain controlled by the registry and full original reviews.
The parent's full 406-row premise audit remains an attributed gate, not a check
performed in this context. Concrete R1/R2 repairs should be version-pinned and
checked before a final reviewed-synthesis claim.
