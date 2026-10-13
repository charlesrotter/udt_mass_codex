# GRC1 researcher B — evolving exploration record

UNADOPTED conditional research, not a new maintained scientific summary. Parent owns
the campaign notebook and central integration. No physical adoption or source grade
change occurs here.

## Context and independent formation

Parent startup and synchronization are attributed, not repeated by this scoped
researcher. Independently verified branch `grok`, HEAD
`89b4b473bed869f5ca296e9bfc67559a3c9ceaff`. Existing unrelated untracked names
were seen only in status/BASELINE and excluded from inspection, hashing and edits.
Read AGENTS, CLAUDE required sections, triggered no-shortcuts/completeness-map,
GRC1 WORK_ORDER and BASELINE. All writes are confined to this directory.

Initial idea was independently formed before exposure to researcher A or a
coordinator hypothesis: promote additive ordered comparisons to route-independent
scalar calibration on a supplied clock network, then derive geometric integrability.
The parent flagged NCI1 as closest prior; central R18 and G402 confirm that this
exact strong condition already has the conformal-Killing criterion. It is retained
as a tool, not claimed novel or rederived as the campaign result. The physical
network/scalar assumption is not native F3. Primary-source search independently
found Dirmeier/Plaue/Scherfner (2008), arXiv:0802.3642, with the same local
kinematic theorem; source qualifications do not replace NCI1's global-period
qualification. No other researcher's ideas have been read at this stage.

## Question B2: universal sign rather than universal magnitude

The failed novelty of B1 motivates a different test, independent of a preferred
clock congruence: can an extra positional clock effect keep the same slowing sign
in every physically matched freely falling laboratory, while its magnitude varies?
PCC1 already tested all-frame *equality* of a leading coefficient. B2 deliberately
weakens equality to a sign inequality. This is not inferred from no preferred
observer or ordinary clocks.

Supply two smooth Lorentz4 metrics g,g0 and a time-oriented tangent isometry I
at matched events, as in PCC1. Use PSW1's actual parallel-prepared released clocks,
matched initial proper L, unit frame, units, and regular null branch. For each fixed
future unit U and unit n perpendicular to U, define

    D = A_g - I* A_g0,
    C(U,n) = lim_(L->0) 2 log(p_L/p0_L)/L^2 = -D(n,U,U,n).

A(X,Y,Z,W)=g(R(X,Y)Z,W) and R=[nabla_X,nabla_Y]-nabla_[X,Y]. D is an algebraic
curvature tensor, not a second physical field. The reference and I are supplied
comparison data. PSW1's local remainders are at fixed U,n; no uniform domain over
arbitrarily boosted laboratories is presumed.

**B2-S (unadopted physical trial):** C(U,n)>=0 for every such U,n. Interpretation:
the matched leading additional positional effect never blueshifts this preparation.
The choice of this preparation, nonzero L^2 interpretation and universal sign are
new physical hypotheses being investigated, not owner-adopted consequences.
Strict positivity can later exclude the zero contribution; the weak version makes
the closure and boundary cases transparent.

First test: boost U toward a null direction while keeping transverse n. Since this
is an algebraic limit *after* taking the fixed-laboratory L->0 coefficient, it does
not interchange a finite-clock asymptotic with infinite boost. The implication is
that D(n,k,k,n)<=0 for every null k and screen n. Therefore Delta Ric(k,k)<=0.
This is a prospective clock-to-optics restriction, not a GR matter/energy condition.

**B2-N (optional, unadopted optical trial):** Delta Ric(k,k)=0 for every null k.
Meaning: preserve the reference's infinitesimal null area-focusing coefficient,
with the same tangent/affine normalization. This is a physically motivated minimal
optical-change option, not implied by GR recovery, conformal equivalence, W4 or DDR.
It does not assert identical finite lensing or identical null paths. Preliminary
argument: B2-S makes each null screen tidal difference negative semidefinite;
B2-N makes its trace zero, hence the full screen difference vanishes. Algebraic
null-curvature rigidity then gives D=kappa B_g with kappa>=0. This recovers PCC1's
isotropic difference from sign plus optical neutrality, rather than assuming its
all-frame equality. Need exact proof, adverse controls and review before return.

## Choices, resources and maximum conclusion

Before the first check, B2-N was weakened to **B2-F**: Delta Ric(k,k)>=0
for all null k (no additional local null defocusing). B2-S itself supplies the
opposite sign, so B2-F entails B2-N within this candidate. This optical inequality
is a genuinely new, oppositely directed physical restriction. Existing UDT
commitments do not supply it; recovery of finite tested GR behavior does not
imply exact zero or nonnegative curvature difference. Its investigatory purpose
is to test whether universal extra clock slowing can coexist with leaving null
area convergence unchanged or more focusing. It is not adopted to force a desired
equation. The sign-only family remains a valid candidate when B2-F is dropped.

First calculation declaration: `check_clock_optics.py` checks the exact finite
linear space of algebraic curvature tensors under Bianchi and a sufficient finite
set of null-screen equalities; an exact rational boosted Weyl control; direct
coordinate curvature of a positive-cosh supplied metric; and a vertex Jacobi
Taylor determinant coefficient. Python/SymPy exact arithmetic, no float dtype,
no statistical or interval claim. These identities support but do not replace
the analytic all-frame proof. 2 GiB virtual, one BLAS, one CPU process; no grid,
no time cutoff, small stdout/stderr/JSON under `checks/algebra_01.*`.

Metric-led exact tangent algebra; Lorentz4, signature -+++, smooth fixed metrics,
ordinary proper clocks and conditional null interface. U,n and allowed curvature
differences are free-and-explored; physical protocol is supplied as PSW1, not
pinned-by-theory selection. The sign/null-neutrality assumptions are explicitly
unadopted. No action, E=Ric, source law, preferred observer, fitted scale, X_max,
light microphysics or accepted premise is added. No GPU. Exact symbolic checks
will use one CPU process at a time, one BLAS thread, 2 GiB address-space limit,
existing TPS1 capture.py, small JSON/stdout artifacts. No elapsed-time kill.
Checks concern finite exact identities and controls; all-frame claims require
analytic arguments. Maximum result is a reviewed conditional geometric restriction
and a discriminating consequence, with the physical joining assumptions still open.

## Exact sources inspected so far

- UDT_DEVELOPMENT D1, R1-R7, PSW1, ACI1, PCC1, R9, selected R17/R18.
- Three owner statements linked from D1 (positional geometry, ordinary local clocks,
  shared additional effect), directly read. Their intended interpretation is kept.
- PSW1 INITIAL_CANDIDATE.md and REPAIR.md, directly read for the prepared formula
  and differentiated-remainder qualification.
- PCC1 INITIAL_DERIVATION.md, directly read for matched curvature difference,
  algebraic convention and regional Bianchi caveat.
- G402 exact registry row; NCI1 exact source to be inspected before relying further.

## Primary literature inspected and access limits

1. A. Dirmeier, M. Plaue, M. Scherfner, *On Conformal Vector Fields Parallel to
   the Observer Field* (2008), https://arxiv.org/pdf/0802.3642 . Read abstract,
   smooth Lorentz4/unit observer conventions, Proposition 3.1 and nearby redshift
   equivalence via the web PDF text. This is credit for the abandoned B1 avenue,
   not evidence that UDT adopts an endpoint scalar. Global exactness remains an
   explicit requirement in NCI1.
2. S. Harris, *A Triangle Comparison Theorem for Lorentz Manifolds*, Indiana
   Univ. Math. J.31 (1982),289-308,
   https://doi.org/10.1512/iumj.1982.31.31026 . Official DOI target was inaccessible.
   Author-hosted ResearchGate PDF search text exposed Proposition2.3 and its
   orthonormal-triple proof: zero null sectional curvature implies pointwise
   constant sectional curvature in dimension>=3. PDF:
   https://www.researchgate.net/profile/Stacey-Harris-3/publication/265423248_A_triangle_comparison_theorem_for_Lorentz_manifolds/links/6112ea010c2bfa282a373479/A-triangle-comparison-theorem-for-Lorentz-manifolds.pdf .
   Open succeeded but text extraction returned zero lines; screenshot requests
   produced tool references without model-visible page images. Access is therefore
   partial, not a claim to have checked the full paper. Our proof will be explicit.
3. S.B. Alexander, R.L. Bishop, *Lorentz and Semi-Riemannian Spaces with Alexandrov
   Curvature Bounds* (2008), https://arxiv.org/pdf/0804.2493 . Inspected introduction
   pp.1-3, theorem1.1 hypotheses and section6 null curvature definition/proposition6.3.
   Used to distinguish one-sided timelike bounds from bounded curvature on all
   nondegenerate planes. No triangle-comparison theorem is yet used in B2.

## B3 development after cross-exposure

Parent later exposed researcher A's spherical radial affine-neutrality (NAR)
proposal. This was the first exposure to another researcher's scientific idea;
B1/B2 formation and B2.1/B2.2 were prior. We exchanged the distinction between
radial null optical neutrality and all-null optical neutrality. For reciprocal
spherical comparison metrics I independently derived the complete all-timelike
plane sign test beta>=0, alpha>=beta, beta>=gamma, then the profile inequalities
for delta f=-r²q. A independently confirmed the translation and noted its
no-exact-switch-off consequence. That portion is collaborative, not blind.

The quartic delta f=-lambda r^4 was chosen as a simple algebraic witness in this
cone, not inferred native or fitted to a target curve. It leads to a finite released
radial clock experiment inside its regular static patch. The same metric gives
outward tidal acceleration; the exact lapse-times-Doppler factor explains the
received ratio. No ordinary GR/motion contribution was removed. lambda and the
launch radius ratio1/4 are free demonstration choices, not theory-pinned values.

Further source reads: NCI1 INITIAL_CANDIDATE/REPAIR directly inspected; G348's
screen/Jacobi result read through central R13 (exact source to be checked before
final banking). Beran, Kunzinger, Ohanyan, Rott, *The equivalence of smooth and
synthetic notions of timelike sectional curvature bounds* (2024),
https://arxiv.org/html/2403.18077v2 , inspected sections1.1,2.1 and introduction.
Its convention agrees with ours; one-sided timelike bounds are distinguished from
semi-Riemannian bounds. Strong causality belongs to its comparison theorems; none
of those theorems is being imported into the present pointwise calculation.

Second calculation declaration: exact original-coordinate curvature of the
generic reciprocal spherical metric, adapted with attribution from PCC1's sound
coordinate check (not claimed a different implementation); direct contraction of
the quartic difference; bivector identity; exact free-clock/null frequency factors,
interception-bound constants and small-epsilon coefficients. Python/SymPy exact
arithmetic, all parameters symbolic except transparent rational controls. No grid,
floating-point fit, scan, finite-data confidence interval or long solve. Same
2 GiB/one-BLAS/one-CPU capture limits. Output `checks/spherical_01.*`.

Both exact checks returned0 with empty stderr; read their saved stdout. The first
used Python3.10.12/SymPy1.13.1, rank20/21 and the rational -11/16 boosted control.
The second recovered the generic spherical curvature from original Christoffels,
quartic null screens (0,0) radial and(-4,-1)lambda*r² tangential, parallel
preparation, exact ratios and the3/2,5/2 quartic coefficients. These are author
checks, not fresh adversarial review.

Third check declaration: independently integrate the quartic metric's coordinate-
time timelike geodesic equation and actual outgoing/incoming null arrival maps,
then differentiate the saved proper-arrival data by centered finite differences.
Use lambda=1,r0=1/4, ordinary proper-clock normalization, float64 DOP853,
rtol/atol(1e-11,1e-13) then(1e-12,1e-14), max stepsizes0.002 then0.001,
finite emission/relay differencing h=1e-4 then5e-5, integration stop t=0.75
for B and at most1.5 for null legs. These stops bound a finite diagnostic and
are not elapsed-time process kills. Compare p/q to the exact endpoint formula
only AFTER the arrival derivative has been obtained. Record raw arrivals,
energy/normalization residuals and changes; this floating-point agreement is
not interval certification or the proof of sign. One CPU/BLAS,2GiB capture,
small JSON stdout; preserve any failure. Output `checks/arrival_01.*`.

Further cross-exposure: coordinator supplied a tentative conformal-only/Weyl
obstruction, and A proposed a rational q completion witness. Neither is an input
to B2/B3 proofs here; A owns checking its new witness. The parent owns any
integration of those separate candidate chains.

Coordinator subsequently suggested a mean-only quiet-sector route. I corrected
that S alone does not force Weyl neutrality, then developed B4: for a Ricci-flat
reference the PSW1 angular mean is -Ric(U,U)/3 independent of reference matching.
Universal nonnegative mean plus nonnegative physical null Ricci gives Ric=Lambda g,
Lambda>=0 and constant regionally. This deliberately retains Weyl and is separated
from directional S by the exact boosted control. It overlaps FE1/PSW1's old
Einstein-class endpoint but uses separately unadopted operational inequalities,
not an unidentified-response equivalence. No new computation was necessary for
the elementary symmetric-null-cone/Bianchi proof.

The arrival-map check returned0/empty stderr. Read saved stdout: tighter p and q
are1.005909819619 and1.009917278384, endpoint discrepancies below3e-12, changes
below8e-12. The two solves differentiate actual arrivals and do not insert p=E+v
to produce them. Sampled energy conservation is a trajectory diagnostic; the
normalization residual is explicitly algebraic. No rigorous floating-point
certificate or physical validation is inferred. G348 exact source sections1-2
were directly read for the quotient-screen/Jacobi convention after central R13.

## Pre-freeze self-audit and return

Found and corrected one notation defect before freeze: early section2 prose used
Q (defined as a curvature DIFFERENCE) in the actual Jacobi evolution equation and
vertex expansion. Actual beams evolve with their respective total T_g and T_0;
only the initial Taylor-coefficient difference is Q. The corrected candidate now
states that distinction and does not claim a propagated difference solves a
homogeneous Jacobi equation. The screen algebra, sign theorem, exact check and
finite clock witness are unchanged. No unresolved numerical issue or known proof
gap remains in the stated conditional results; their unadopted physical joins
and untested global/stability/empirical questions remain explicit.

Parent accepted this as a decision-ready early-review checkpoint under the work
order. Further decorative examples would not sharpen this choice. Freeze the
current candidate, notes, checks and exact sources; await actual fresh separate
reviews. The researcher is the same inherited AI model, not a human specialist;
author symbolic/arrival checks do not constitute independent reviewer contexts.

