# W7 — THE SYMPHONY: the ensemble solve on the fold quotient. Results

Date: 2026-06-13. Driver: Claude (W7 Symphony agent). Declaration: W7
section of w_stiffness_push_declaration.md (binding). Mode: UNCOVER +
SOLVE (algebraic/solution-space), the orchestra principle made literal.
The single-cell resonator template is RETIRED; this push solves the
COUPLED, FOLDED, TIME-ON system for a discrete spectrum emerging from
the COMPOSITION of sectors.

Scripts (all assert-laden, pre-registered failure criteria, namespace
w7_*): w7_a_mirror_bc.py (7/7), w7_b_pt_spectrum.py (12/12),
w7_c_kappa_wwave.py (5/5), w7_d_verifier.py (5/5 ADVERSARIAL). Reuses
committed machinery (w6_arm1_lib geometry/jets; the harvested closed
forms of w_alg_*; the W6 mirror-fold geometry) WITHOUT editing any
committed file. Logs: /tmp/w7_*.log.

## SYMPHONY VERDICT (grading branch (i), earned by closed form +
## independent eigensolve; aimed-hardest skepticism applied):
## THE ENSEMBLE QUANTIZES INTO A DISCRETE CLOSED-FORM LADDER.
## Scale autonomy is PARTIAL (shape invariant, scale still inherited).

The composition {dressed Poschl-Teller radial spine + DERIVED mirror
parity BC + finite-cell outer closure} yields a DISCRETE, closed-form
spectrum that NO single sector shows: the radial sector alone on an
infinite line gives the reflectionless PT CONTINUUM (one bound state +
bands — the retired resonator's bands); the FINITE MIRRORED cell
converts that continuum into a discrete ladder whose SHAPE is set by an
intrinsic invariant. This is discreteness from the cell being FINITE +
MIRRORED (the finite-cell canon), not from a potential well in one
sector — the orchestra effect, realized.

## (i) THE EXPLICIT ENSEMBLE EIGENPROBLEM (operator + DERIVED BC)

Differential spine (radial phi + time — the ONLY differential sector,
per w_alg): on the f ~ 1/r (rho=1) member, the unique exactly-solvable
scaling, the dressed C1 pencil is EXACTLY Poschl-Teller lambda=1
(reflectionless):

    -psi''(z) - 2 theta^2 sech^2(theta z) psi(z) = E psi(z),
    z in [-L, +L],   E = omega^2,   X = theta z.

Algebraic angular web: q*, w enter ALGEBRAICALLY (w_alg closure: the
w-row carries no angular SL well; bands-not-lines stands at the w-row).
They set the dressing scale theta and the cell half-width L PER RAY —
they are PARAMETER-SUPPLIERS, not a separate differential channel.

Fold / mirror boundary (DERIVED, not chosen — w7_a_mirror_bc.py): the
same-minus involution sigma: (a,b)=(g_Tr,g_Ttheta) -> (-a,-b) is a
genuine quotient symmetry (sigma^2=id; det g4 invariant; (f,q,w) and
the (r,theta) sector untouched — A1). The crease residual
rho := (b - f q a) is ODD under sigma (rho -> -rho; det g4 ~ rho^2 is
even, which is why the fold is regular — A2). On the W6 same-minus
STATIONARY row (a*=alpha f_T, b*=(f_theta/f_r)a*), sigma IS f_T -> -f_T
— sigma is TIME REVERSAL on the crease (B1). Hence the DERIVED parity
dichotomy of the fluctuation fields across the crease:

    sigma-EVEN sector (static shape, f_T=0) -> NEUMANN at crease
    sigma-ODD  sector (f_T-driven amplitude) -> DIRICHLET at crease

The outer cell edge closes the FINITE cell with Dirichlet at z=+-L
(canon: no spatial infinity). REDUCTION CHECK (A4): on the static
fixed slice a=b=0, sigma is trivial (rho=0, no transverse direction)
and imposes NOTHING — consistent with W4/W5 finding bands on the static
slice. Quantization is carried ONLY by the f_T-driven (time-on) sector
where sigma acts nontrivially — exactly registry #30's f_T-driven
reopening. THE BC IS DERIVED FROM sigma, NOT PICKED — the central
hypothesis-discipline gate, passed.

## (ii) THE HARVESTED CLOSED FORMS (written down, not just classified)

Poschl-Teller lambda=1 full solution set (each verified by substitution
to identity, w7_b PART A; random-point reverified to 1e-6, w7_d D3):
  - single bound state: psi0 = sech(theta z), E0 = -theta^2 (A1);
  - reflectionless scattering tower: psi_k = (theta tanh(theta z)-ik)
    e^{ikz}, E=+k^2, transmission 1 (A2);
  - zero-energy pair: even 1-(theta z)tanh(theta z), odd tanh(theta z)
    (A3/A4; the even mode is exactly the w_alg D2a marginal Dirichlet
    mode at the fold).
General-E real parity solutions on the cell (A1/B-series):
  u_c(z) = theta tanh(theta z) cos(kz) + k sin(kz)   -> ODD  (u_c(0)=0)
  u_s(z) = theta tanh(theta z) sin(kz) - k cos(kz)   -> EVEN (u_s'(0)=0)
  (parity DERIVED from the geometry: tanh is odd; the towers match the
  sigma-odd/sigma-even sectors AUTOMATICALLY — the crease BC SELECTS a
  tower, it does NOT quantize; the OUTER finite-cell Dirichlet does.)

Liouville / Tzitzeica per-ray sources (carried from w_alg, written
down): OFF = Liouville general solution e^{-2V} = -/+4 F'G'/(F+G)^2
(F,G arbitrary chiral, both branches); the dressing background is
v = ln[(sqrt(Phi)/theta) cosh(theta(m-m0))], Phi = p b/(8 kappa);
ON = Tzitzeica/DBM exponent pair (+1,-2). Gelfand-Bratu fold identity
G* = 8 s*^2 sech^2 s*, s* root of s tanh s = 1.

THE CLOSED-FORM QUANTIZATION CONDITIONS (the ensemble notes, B5),
s := theta L the dimensionless cell DEPTH:
    ODD  tower (sigma-odd, f_T):    tan(kL) = -(s tanh s)/kL
    EVEN tower (sigma-even, shape): tan(kL) = +kL/(s tanh s)
Transcendental but DISCRETE: a countable {k_n L} per tower. The
dressing factor (s tanh s) is exactly the w_alg fold invariant
(s tanh s = 1 at the saddle-node).

## (iii) THE SYMPHONY SPECTRUM + SCALE-AUTONOMY (the decisive grading)

DISCRETE LADDER, verified two independent ways:
  - closed-form transcendental roots (w7_b PART C);
  - INDEPENDENT full-cell parity-classified eigensolve (torch float64,
    V100, N=8000, Dirichlet outer ends; w7_d D4): ODD k = 2.67137,
    6.06288, 9.27949; EVEN k = 4.41398, 7.67898, 10.8713 (at s=1.5,
    L=1); both towers match the closed form to ~3e-6 (O(h^2)); exactly
    ONE bound state (the PT single bound level, cell-shifted to
    E=-1.153). The ladder is real, discrete, self-adjoint, complete.

SCALE-AUTONOMY (banked classifier, applied honestly — w7_b C1/C2/C3):
  - the ODD fundamental kL_1 MOVES by 1.32 across depth s in [0.3, 8]
    (3.11 -> 1.79): the dressing genuinely participates; NOT pinned to
    a bare-box value (the triviality attack, w7_d D1, REPELLED — dressed
    spectrum differs from the theta=0 box and moves with depth);
  - the overtone ratio omega_2/omega_1 (manifestly L-INDEPENDENT) VARIES
    with s (2.01 at s=0.3 -> 2.96 at s=8): a pure dimensionless SHAPE
    INVARIANT of the cell, set by s = theta L alone. The cell's spectrum
    has a SHAPE no box length can set.
  HONEST VERDICT: the SHAPE (overtone ratios, ladder structure) is a
  depth-controlled INVARIANT; but the ABSOLUTE omega = kL_n(s)/L still
  carries 1/L. There is no absolute note without theta (the dressing
  length) fixing the scale. FULL scale autonomy is NOT achieved at this
  order: theta is still an INPUT, inherited from the member's dressing
  length. This is the finite-cell canon — the depth-to-dressing ratio s
  owns the SHAPE, theta owns the SCALE.

## (iv) THE kappa / W_wave SETTLEMENT (the watched import thread)

w7_c, deliverable (iii) of the declaration. kappa enters the dressing
ONLY through Phi = p b/(8 kappa) (A1); theta = theta(kappa, L) via the
seal condition s sech s = sqrt(Phi) L. Result:
  - the fold quotient + mirror BC do NOT determine an absolute kappa;
  - they DO fix (a) the RATIO kappa_s/kappa_c = 2 pi^2/(3 G*) =
    1.87252511385 (theorem, member-independent — w_alg D3), and (b) a
    kappa THRESHOLD (saddle-node fold): below kappa_fold NO dressed cell
    exists (two depths above, none below — B1); the threshold scales
    with the member's p b L^2 (member sets scale, metric fixes the
    dimensionless fold structure — C2);
  - W_wave is FORCED-AS-REQUIRED, not refuted: kappa=0 sends Phi -> inf,
    the Liouville dressing degenerates (no finite PT well, no notes),
    and the w-sector loses its only curvature term (registry #21/#22:
    W_wave the single forced object). The discrete notes EXIST ONLY for
    kappa != 0 above the fold threshold. The import thread settles:
    W_wave is forced; kappa is a free dial above a DERIVED threshold,
    with the fold RATIO fixed exactly. (Settlement by derivation, not
    assumption — clean, branch iii-b/iii-c blend.)

## (v) SCRIPTS + COUNTS

  w7_a_mirror_bc.py   7/7   the DERIVED mirror/parity BC (sigma = time
                            reversal; even->Neumann, odd->Dirichlet)
  w7_b_pt_spectrum.py 12/12 PT lambda=1 closed forms + the ensemble
                            quantization conditions + scale-autonomy
  w7_c_kappa_wwave.py 5/5   the kappa/W_wave settlement
  w7_d_verifier.py    5/5   ADVERSARIAL self-verifier (GPU eigensolve)

## (vi) VERIFIER ATTACK LIST + WHAT IT FOUND (w7_d_verifier.py)

The adversarial pass (hardest skepticism at the program-confirming
outcome, per hypothesis discipline) ran five attacks and FOUND TWO REAL
BUGS — both in the verifier scaffolding, NEITHER in the physics:
  D1 TRIVIALITY ("box did everything, any finite SL is discrete"):
     REPELLED — the PT dressing shifts the spectrum vs the bare box and
     moves with depth (load-bearing voice).
  D2 BC-PROVENANCE ("BC chosen to quantize"): REPELLED — the two parity
     towers interlace and strictly ALTERNATE (odd,even,odd,...) with the
     ODD tower lowest: the textbook signature of ONE symmetric operator
     parity-split; the crease BC relabels, the outer Dirichlet quantizes.
     [BUG FOUND + FIXED: the first version asserted ground=EVEN; for
     outer-Dirichlet ends the ODD (Dirichlet-Dirichlet) mode is lowest —
     a wrong assertion, corrected; physics unchanged.]
  D3 REFLECTIONLESS-CONSISTENCY: PASS (200 random points, residual 9e-6).
  D4 SPECTRUM-EXISTENCE (independent eigensolve): PASS after FIX.
     [BUG FOUND + FIXED: the first version's Neumann ghost-node FD was
     wrong (returned the odd answer for the even tower); replaced with a
     full-cell Dirichlet eigensolve + parity classification — BC-
     discretization-free — which reproduces BOTH towers to ~3e-6 and
     exactly one bound state. The bug was a discretization error, not a
     spectrum error: the closed form was right all along.]
  D5 ORCHESTRA-NECESSITY (honest scope, no overclaim): LOAD-BEARING =
     {radial phi spine -> PT well; finite cell -> discretization;
     fold/mirror -> crease parity + inner BC}. The angular web is a
     PARAMETER-SUPPLIER (no differential channel — the w_alg bands-not-
     lines w-row theorem stands); the time row's role is to make the
     crease REGULAR (fold not edge) and FIX THE PARITY (sigma = time
     reversal), not to add a propagating mode.

KEY SCOPE / HONESTY FLAG (the standing-hunch caveat): discreteness IS
realized from composition, but the mechanism is phi-SPINE x FINITE-
MIRROR, NOT the phi-ANGULAR differential coupling that is Charles's
named suspect for the discreteness gap. The angular sector composes
ALGEBRAICALLY (sets theta, L), not as a co-oscillator at this order.
The orchestra plays; the specific instrument pairing in the standing
hunch is not yet the source of the notes. All kappa != 0 / time-
dependent physics remains HYPOTHESIS-GRADE pending Charles canonization.

## PREMISE SET (binding on every W7 claim)

f ~ 1/r flat-weight (rho=1) member (the unique exactly-solvable
scaling; all rho!=1 collapse to one non-solvable Emden-Fowler class —
w_alg E2); C=0 class; the W6 same-minus stationary time row (a*~f_T);
the differential spine restricted to radial phi + time (angular
algebraic); the mirror BC derived from the same-minus involution sigma;
the outer finite-cell Dirichlet from canon (no spatial infinity). The
closed-form PT spectrum and quantization conditions are THEOREM-GRADE
on this member; the kappa-threshold and the discreteness verdict carry
this premise set; full scale autonomy is OPEN (theta inherited).

## VERIFIER AMENDMENT — DOWNGRADE (2026-06-13, independent main-loop pass)

Independent blind verifier (agent a98f2e9f2d10e132e, own free-box-
calibrated machinery, w7_verifier_boxsep.py 12/12 + w7_verifier_bcprov.py
5/5; shared no machinery with the arm) — the branch-(i) headline
("THE ENSEMBLE QUANTIZES INTO A DISCRETE CLOSED-FORM LADDER / gap
addressed") is OVERCLAIMED and is DOWNGRADED. The arm's mathematics is
correct and every sub-claim is independently confirmed (below), but the
DISCRETENESS ITSELF is the outer finite-cell Dirichlet BOX (registry
#1), not native discreteness from the ensemble.

DECISIVE box-vs-mirror separation (holding theta = the inherited
dressing length fixed, varying cell size L): omega_1 = kL_1/L -> 0 as
exactly 1/L, with kL_1 BOUNDED in [pi/2, pi] (1.5957 -> 1.5723 at
L = 64 -> 1024) — i.e. omega_1 * L ~ box constant: this IS registry #1
("omega ~ 1/R_max", "omega1*Rmax ~ const") verbatim. Wall-off test
(L -> infinity at fixed theta): the ladder spacing collapses as ~pi/L
(1.745 at L=2 -> 0.0247 at L=128) -> CONTINUUM; only the single PT
bound state survives (E0 = -theta^2, imaginary omega, not a propagating
note). Outer wall Dirichlet<->Neumann moves eigenvalues drastically
(the OUTER wall quantizes); the crease BC only swaps odd<->even towers
(the mirror LABELS, it does not quantize). The ONLY depth-invariant is
the overtone RATIO omega_2/omega_1 (the Gelfand-Bratu shape factor,
2.04 -> 2.96 across s); NO L-independent absolute note exists.

CONFIRMED verbatim (these stand): the dressed spine is exactly
Poschl-Teller lambda=1 reflectionless, one bound state; the closed-form
quantization conditions and the s*tanh s = Gelfand-Bratu connection
(G* = 3.51383072); the mirror BC is genuinely DERIVED from the
same-minus involution sigma:(a,b)->(-a,-b) (= time reversal on the
stationary row; rho=(b-fqa) odd; parity dichotomy real, NOT a smuggled
quantizing BC); the two arm-verifier bugs were scaffolding-only;
W_wave FORCED-AS-REQUIRED (kappa=0 => no dressing => no notes); the
fold + BC do NOT fix absolute kappa (saddle-node threshold + free dial;
ratio kappa_s/kappa_c = 2pi^2/(3G*) exact).

HONEST OBJECT (what W7 actually delivered): a finite-cell box spectrum
(absolute omega ~ 1/L = registry #1 box-control) carrying (a) a
depth-invariant Gelfand-Bratu OVERTONE RATIO (shape invariant) and
(b) same-minus-derived PARITY labeling. Real and non-trivial; NOT
native discreteness; the discreteness gap is NOT closed.

SCOPE (Charles-relevant): the posed operator is 1D in z (radial-phi +
time); the ANGULAR sector enters ALGEBRAICALLY (theta, L scalar
parameter-suppliers), NOT as a phi-angular DIFFERENTIAL co-oscillator.
Charles's named discreteness-gap suspect (the phi-angular interaction)
is explicitly NOT the mechanism here; the orchestra that plays is
phi-spine x finite-box-boundary, with the angular instrument not
co-oscillating. The standing hunch remains OPEN and unrealized.
