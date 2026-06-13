# W6 FLUX-TEST — Phase 0 (invariant character of the Delta_w / D = 0
# surface): Results

Date: 2026-06-12. Driver: Claude (W6 FLUX-TEST agent). Adjudicates
registry #30 / w_alg_results.md HEADLINE 2 — the hypothesis-grade
"insulating wall => discrete angular CELL COUNT" reading of the q*-branch
metric degeneracy D|q* = r^2 W Delta_w^2/P^2 = 0 at the latitude
u*^2 = 1 - a^3 W/(a_u^2 r), where the coordinate signal speeds
c_ang^2 = f/D and c_rad^2 = f^2 r^2 W/D DIVERGE as 1/D.

Governing lens (Charles's reframe, taken as the FIRST question): a
signal speed that diverges in the COORDINATE frame is suspect as a frame
statement before it is physical; and D = r^2 W - f q^2 is a METRIC BLOCK
DETERMINANT, so speeds ~1/D are the textbook coordinate-degeneracy
signature (Schwarzschild-in-Schwarzschild-coordinates). The test is
UNCOVER-FIRST. PHASE 0 was done ALGEBRAICALLY/EXACTLY (sympy + mpmath
80-digit); it settled the question and made Phase 1 unnecessary (see
verdict). Reused, never edited: w6_arm1_lib.build_metric/geom, the C=0
flat shaped member from w_alg_closure.py.

Scripts (all new, namespace w6_flux_*): w6_flux_phase0.py (10 PASS /
1 designed-FAIL = the singularity detector firing), w6_flux_curv.py
(verdict a, 80-digit), w6_flux_curv_generic.py (q*-artifact ruled out),
w6_flux_phase0b.py (5/5, degeneration-vs-singularity). Blind adversarial
verifier (independent machinery, own curvature engine validated against
Schwarzschild K = 48 M^2/r^6 exactly): agent a66894d1a78df7b1a —
CONFIRMED on two further independent backgrounds/latitudes.

## HEADLINE — THE SURFACE IS A CURVATURE SINGULARITY, NOT A WALL AND
## NOT A COORDINATE ARTIFACT (verdict (a), sharpened)

PHASE-0 VERDICT = (a) SINGULARITY, in a specific sharpened form: D = 0
is a CURVATURE SINGULARITY of the 4-metric that COINCIDES EXACTLY with
the metric-degeneration boundary det g_4 -> 0 (signature loss). It is
the EDGE of the ansatz's declared signature-legal domain (D > 0),
reached at FINITE proper distance, where curvature invariants blow up as
any det -> 0 boundary does. This OVERTURNS BOTH the prior (benign
coordinate type-change) AND the hypothesis (interior insulating wall).

THEOREM-GRADE on the tested members (exact + 80-digit, verifier-
confirmed independently):

1. det g_4 = -(r sin theta)^2 D / (1+w)^2 EXACTLY — the FULL metric
   determinant is proportional to D and vanishes (linearly) on D = 0.
   The Lorentzian signature (-,+,+,+) holds for D > 0 and is LOST at
   D = 0 (the spatial (r,theta) block det = D/f -> 0; one spatial
   eigenvalue lam_- ~ D/(f tr h) -> 0). The covariant metric is finite
   and smooth there; only the INVERSE blows up (g^{rr}, g^{thth} ~ 1/D)
   — but that inverse-divergence is the symptom of det -> 0, not a
   benign chart choice.

2. Curvature invariants DIVERGE as clean power laws as D -> 0 (mpmath
   80-digit, RMS of log-log fit < 5e-4; float64 sign-flips near
   D ~ 1e-7 — confirmed catastrophic cancellation, NOT the true
   behavior):
     - GENERIC smooth q crossing D = 0 transversally (D ~ linear):
       Ricci R ~ D^{-2},  Kretschmann K ~ D^{-4}.
     - q* branch (q* = 2 r^2 W f_r f_th/P), which TOUCHES D = 0
       TANGENTIALLY because D|q* = r^2 W Delta_w^2/P^2 is a PERFECT
       SQUARE in Delta_w (D ~ Delta_w^2):
       R ~ D^{-3/2},  K ~ D^{-3}.
   Both diverge => the singularity is a property of the METRIC, NOT an
   artifact of the q* elimination (the brief's NON-NEGOTIABLE concern,
   explicitly tested and cleared). The differing exponents are exactly
   the transversal-vs-tangential approach to the same det -> 0 edge.
   The verifier confirmed the q* exponents are conditional on W=(1+w)^2
   being LIVE (forcing W=1 degenerates q* to R~D^{-1}, K~D^{-2}) — the
   W factor in q* is load-bearing; the result is a property of the full
   (1+w)^2 class.

3. The singular boundary is reached at FINITE proper distance (proper
   length along the degenerating direction ~ Int sqrt(lam_-) ds ~
   Int sqrt(D) ds, finite for a simple zero) — a genuine curvature edge
   BOUNDING the signature-legal region, not an infinitely-distant
   horizon throat and not an interior partition.

RECONCILIATION (the one apparent tension, resolved): the spatial block's
small eigenvalue is lam_- ~ 0.0067 D (first-order in D), so a single
leg-rescaling removes the 1/D from the metric COMPONENTS (w6_flux_phase0
E1/E2). That rescaling is NOT a smooth diffeomorphism — its Jacobian is
unbounded at D = 0 precisely because det g_4 -> 0 — so it cannot
continue across the surface, and the coordinate-INVARIANT curvature
still diverges. "The 1/D in the components dissolves under rescaling"
and "the curvature is invariantly singular" are BOTH true and not in
conflict: the former is a statement about a chart, the latter about the
geometry. The decisive object is the invariant (curvature), and it is
singular.

## WHAT IT MEANS FOR DISCRETENESS (registry #30 adjudicated)

The cell-partition / insulating-wall reading is REFUTED — and refuted
more decisively than the VWALG analytical prior anticipated. VWALG
expected a benign Neumann-like turning surface (g^{thth} = 1/D blows up,
finite energy gives d_theta u -> 0). The truth is stronger: D = 0 is not
an interior surface inside a valid region at all — it is the BOUNDARY of
the metric's signature-legal domain, a curvature edge. An interior
insulating wall partitioning a valid region into dynamically independent
angular cells CANNOT exist on this class, because the locus u* is where
the q* configuration RUNS INTO the edge of the spacetime, not a feature
inside it. The "count of latitudes = deg(Delta_w in u^2)" is a count of
where the q* branch GRAZES its domain boundary (D|q* = r^2 W Delta_w^2/P^2
touches zero), not a count of insulated cells.

Consequence for the program: angular discreteness, if it is real, must
come from GENUINE INVARIANT STRUCTURE (curvature, topology, the integer
arithmetic / the exact-solvability pattern banked in #30), NOT from a
coordinate latitude or a degeneracy surface. The orchestra/finite-cell
discreteness candidate does NOT acquire dynamical support here; the
Delta_w surface is closed as a discreteness mechanism on this class.

CHARLES'S REFRAME — vindicated, in its deeper form. The divergent
coordinate speeds c_ang^2 = f/D, c_rad^2 = f^2 r^2 W/D are indeed a
frame statement ("infinite for the coordinate observer; the local proper
c_eff = f is finite, D-independent" — w6_flux_phase0 B1/D3). But the
correct deeper reading is not "benign coordinate artifact, no problem
anywhere": it is that the diverging coordinate speeds FLAG that the q*
branch is reaching the EDGE of the signature-legal domain (det g -> 0),
where the geometry genuinely ends. The frame quantity is a symptom; the
invariant disease (a curvature edge bounding the ansatz) is real. There
is no interior barrier — but there is a real domain boundary.

## PHASE 1 — NOT RUN (and why)

Per the brief's routing, Phase 1 (the dynamical flux march of the
unreduced 3-field operator across u*) is run ONLY if Phase 0 finds a
GENUINE INVARIANT NULL/CHARACTERISTIC SURFACE (verdict (b)). Phase 0
found (a) a curvature singularity = domain boundary. There is no
interior surface to march a finite-energy packet across; "insulation vs
crossing" is not the right question because the locus is the edge of the
spacetime, not an interior latitude. Marching an evolution INTO a
det g -> 0 curvature edge would measure the breakdown of the chart at
the boundary, not a flux through an interior wall — it cannot decide the
cell-partition question (which is already answered: no interior wall
exists). Phase 1 is therefore unnecessary; the algebraic Phase 0
settles registry #30's hypothesis decisively in the negative.

(The unreduced 3-field operator — w6_arm1_a_operator.py, 11/11 — remains
the right object for the SEPARATE open W6 question, the coupled
bands-vs-lines branch operator AWAY from the degeneracy edge; this
flux-test does not bear on that, and nothing here edits or invalidates
the Arm-1 operator, whose gates pass on the signature-legal interior.)

## SCOPE / PREMISES (binding on this negative, per registry discipline)

- Member: the C = 0 deep-flat shaped representative (f = a/r with a
  banked ell<=2 angular bump) plus, for the generic-q control, a smooth
  non-q* off-diagonal field; w = 0 (static frozen-wave slice) for the
  explicit curvature evaluations. Verifier added f ~ 1/r^2 and live
  w != 0 backgrounds — exponents held.
- Branch: both the q* C1-stationarity branch and a generic transversal
  q. The singularity is established on BOTH (the key generality result).
- The det g_4 = -(r sin)^2 D/(1+w)^2 identity and the proper-distance
  finiteness are class-general (any f,q,w on the declared ansatz).
- NOT yet probed: whether a NON-diagonal-time or same-minus (g_Tr,
  g_Tth) enlargement changes the determinant structure (that class is
  outside the declared three-field block; flagged, not tested). The
  curvature exponents are member-specific numbers; the SIGN of the
  result (divergence, det -> 0) is class-general by the determinant
  identity.

## REGISTRY ACTION (proposed; append to NEGATIVES_REGISTRY.md on commit)

Amend #30 under its CONDITIONS-CHANGED protocol: the W6 DYNAMICAL
FLUX-TEST it called for is SUPERSEDED by an exact Phase-0 invariant
result. The "insulating wall => discrete angular cell count" reading is
now REFUTED at the KINEMATIC/GEOMETRIC level (not merely as a mechanism):
D = 0 is a curvature singularity coinciding with the metric-degeneration
boundary det g_4 -> 0 (R ~ D^{-2}/K ~ D^{-4} generic; R ~ D^{-3/2}/
K ~ D^{-3} on the tangential q* branch; 80-digit clean, independently
verified). It is the EDGE of the signature-legal domain, not an interior
wall; no angular cell partition exists on this class. The Delta_w
surface is closed as a discreteness mechanism. The DETERMINANT identity
det g_4 = -(r sin)^2 D/(1+w)^2 and the curvature-singularity character
of D=0 are theorem-grade on the declared ansatz. Premises as above.

## VERIFIER ATTACK LIST (for the blind pass of record)

1. Re-derive det g_4 = -(r sin)^2 D/(1+w)^2 independently (1 line);
   confirm linear vanishing on D=0. [verifier did: confirmed exactly.]
2. Rebuild the FULL Riemann/Ricci/Kretschmann with an INDEPENDENT engine
   and reproduce a known case (Schwarzschild K = 48 M^2/r^6; flat R=K=0)
   before trusting it. [verifier did: Schwarzschild exact.]
3. The cancellation trap: confirm float64 K SIGN-FLIPS / goes erratic
   near D ~ 1e-7 while mpmath (>=60 dps) is a clean power law. If high
   precision were BOUNDED while float64 diverged, the claim is REFUTED.
   [verifier did: mpmath clean, float64 erratic — confirms genuine.]
4. Generic vs q*: confirm the singularity persists for a GENERIC smooth
   q (rules out the q*-elimination-artifact escape). [done both ways.]
5. Probe the exponents on a DIFFERENT member (f ~ 1/r^2), different
   latitude, live w: confirm R/K exponents stable. [verifier: stable.]
6. Outstanding adversarial angles NOT yet closed (next verifier):
   - Is the curvature divergence possibly an ARTIFACT of evaluating on
     a STATIC w=0 slice of a fundamentally time-dependent metric? (We
     have verifier-confirmed live-w results — strong, but a fully
     T-dependent background curvature check would close it.)
   - Could a NON-diagonal-time (same-minus g_Tr,g_Tth) completion of the
     metric REMOVE the det -> 0 (i.e. is D=0 of the 3-field block lifted
     by the enlarged class)? This is the one class-generality gap worth
     a targeted check before banking the determinant identity as
     fully class-general.
   - Geodesic completeness: confirm a timelike/null geodesic reaches
     D=0 at finite affine parameter (we showed finite PROPER DISTANCE
     along the degenerating direction; a geodesic-integration check
     would upgrade "finite proper distance" to "geodesically
     incomplete = true edge").
