# Derivation notes — c_eff crux (trivial vs profound). LEAD / UNBANKED.

Date 2026-08-06. Branch grok. Mode: OBSERVE (report what is there). Exact sympy, float-free.
Scope stamp on EVERYTHING below: reciprocal-lock metric class, static representative,
free-kinematic level (no law selected). Not a general theorem. See PREREGISTRATION.md.

Metric (SUPPLIED, canon C-2026-06-18-1):
  ds^2 = -e^{-2 phi(x)} c^2 dt^2 + e^{2 phi(x)}(dx^2 + dy^2 + dz^2),  phi = phi(x).
Field pair (SUPPLIED, CHOSE/foundational): (g, u), u = d_t / sqrt(-g_tt), the copresence
"now" direction, PROMOTED to an independent physical field (not assumed metric-determined).
  u^mu = (e^{phi}/c, 0, 0, 0),  u_mu = (-e^{-phi} c, 0, 0, 0),  u^mu u_mu = -1.  [verified]

Compute scripts: compute_kinematics.py (4D, full congruence), compute_invariants.py (2D core,
static reduction + curvature contraction). Both exact; outputs transcribed below verbatim.

--------------------------------------------------------------------------------
## 1. u-congruence kinematics (DERIVED, exact)  [compute_kinematics.py]

Acceleration   a_mu = u^nu ∇_nu u_mu = (0, -phi', 0, 0)
               a^mu = (0, -e^{-2phi} phi', 0, 0)
               a^mu a_mu = e^{-2phi} (phi')^2          NONZERO iff phi' != 0
Expansion      theta = ∇_mu u^mu = 0                    VANISHES
Shear          sigma_{mu nu} = 0                        VANISHES
Twist/vortic.  omega_{mu nu} = 0                        VANISHES
               sigma^2 = 0,  omega^2 = 0

Reading: u is a RIGID, NON-ROTATING, NON-EXPANDING, ACCELERATING congruence. The only
surviving first-derivative datum is the acceleration a_mu, pointing "downhill" in phi
(magnitude e^{-phi}|phi'|). This is the static-observer 4-acceleration ("what holds you
in place against the depth gradient"). All shear/expansion/twist zero because ∂_t is a
hypersurface-orthogonal Killing vector.

--------------------------------------------------------------------------------
## 2. Is u the unique timelike Killing direction? (DERIVED)  [compute_invariants.py]

The metric is static: xi = d_t is a Killing vector, hypersurface-orthogonal (no dt·dx
cross term). For phi' != 0 the spatial slices are inhomogeneous along x, so there is NO
extra timelike Killing symmetry; xi is the UNIQUE timelike Killing direction up to constant
scale. Therefore u = xi / |xi| is fully METRIC-DETERMINED in this metric class.

Consequence, made explicit and verified exactly:
  Let V^2 = -g(xi,xi) = -g_tt = c^2 e^{-2phi}  (the Killing NORM; a coordinate-invariant
  scalar because xi is invariantly singled out by g). Then
        a_mu = ∇_mu ln V                                [verified: a_mu - grad ln V = 0]
        a^mu a_mu = | ∇ ln V |^2 = e^{-2phi}(phi')^2    [verified: grad2 - a2 = 0]
  Scale ambiguity xi -> lambda*xi shifts ln V by a constant, leaving a_mu untouched, so
  even the Killing scale does not enter. a_mu carries ZERO information beyond g.

Curvature contraction (verified):
        R_{mu nu} u^mu u^nu = (2 phi'^2 - phi'') e^{-2phi}
  and via Raychaudhuri with theta=sigma=omega=0 this equals ∇_mu a^mu = box(ln V) — again
  a pure-metric scalar. Ricci scalar R = 2(phi'' - 2phi'^2) e^{-2phi} (2D core).

Every scalar we can form from (g,u) up to first derivative of u — a^2, theta, sigma^2,
omega^2, R_{mu nu}u^mu u^nu, u^mu ∂_mu(any g-scalar) — is a function of phi, phi', phi''
i.e. a PURE-METRIC invariant. u contributes no independent scalar.

--------------------------------------------------------------------------------
## Q1 VERDICT (STATIC): NO static (g,u)-invariant exceeds the g-invariants.

Reason (load-bearing): u is built from the UNIQUE hypersurface-orthogonal timelike
Killing vector, which is metric-determined; hence a_mu = ∇_mu ln(Killing norm) and every
(g,u)-scalar is a g-scalar. u is statically a RELABEL — no invariant distinguishes (g,u)
from g alone. This is the honest TRIVIAL answer at the static, exhibited-invariant level,
and it is given full derivational care (F-STEER guard: not deflated, it is computed).

--------------------------------------------------------------------------------
## 3. Moving frame / off-alignment (Q2, structural — no magnitude)

Model a system moving at velocity w relative to copresence: boost u along e_x (the unit
spatial x-vector, e_x^mu = (0, e^{-phi}, 0, 0)):
        u'^mu = u^mu cosh w + e_x^mu sinh w,   u'·u' = -1.
Two candidate "GR-lacks-this" invariants and their honest fate IN THIS METRIC CLASS:

(a) Contractions on the boosted vector, e.g. R_{mu nu} u'^mu u'^nu, DO depend on w. But
    this is NOT a distinction from GR: pure-metric GR permits evaluating curvature
    contractions on ANY chosen timelike vector; a w-dependent number is not an invariant
    property of the theory, it is a chosen probe direction. Calling it a distinction fires
    F-GAUGE/F-CIRCULAR. -> NOT a difference.

(b) The absolute-velocity scalar gamma = -g(U_sys, u) (Lorentz factor of a system's
    4-velocity U_sys relative to copresence u). In a theory with a genuinely independent u
    this IS an invariant GR has no analog of (GR has no preferred u, so no absolute
    velocity). BUT in THIS metric class u = xi/|xi|, so
        gamma = -g(U_sys, xi)/|xi| = E / |xi|,   E = -g(U_sys, xi) = Killing energy.
    i.e. "velocity relative to copresence" collapses to the STANDARD GR conserved Killing
    energy of the system in the static frame — a pure-metric quantity. -> NOT a difference
    in this metric class, BECAUSE u is pinned to the metric's Killing vector.

Q2 verdict (this metric class, free-kinematic): NO FORCED invariant that GR lacks. Every
"relative-to-u" quantity reduces to a Killing-frame (metric) quantity while u stays pinned
to xi. The absolute-velocity invariant gamma is STRUCTURALLY available ONLY IF u carries
data beyond xi (u NOT metric-determined) — which this static class does not supply. The
distinction is contingent, not exhibited here. (Magnitude of any effect is law-dependent:
F-LAWCLAIM — unclaimed.)

--------------------------------------------------------------------------------
## 4. Lovelock premise (Q3, field-content structural statement)

Statement about FIELD CONTENT, not a new theorem: Lovelock's uniqueness (the only
divergence-free symmetric 2-tensor built from g and its first two derivatives in 4D is
a G_{mu nu} + b g_{mu nu}) has as its HYPOTHESIS "built from the metric ALONE." Promoting
u to an INDEPENDENT unit timelike vector field adds a field the action/EL-tensor may
depend on: one can now build divergence-free 2-tensors from u (u_mu u_nu, ∇u terms, ...).
So the (g,u) theory's admissible response-law space is genuinely LARGER than metric-only,
and it lies OUTSIDE Lovelock's hypothesis. This is the textbook Einstein-aether / Horava
situation: adding a unit timelike vector is precisely how those theories evade GR
uniqueness and become empirically distinct (different PPN, GW speed, etc.). The claim is
NON-CIRCULAR: it does not assume u "physical" to get a specific measurable; it states a
proven fact about what laws the enlarged field content admits.

CRUX CAVEAT (the honest tension, both directions surfaced):
- The ENLARGEMENT is a property of the THEORY (field content). It is real.
- This metric class's STATIC SOLUTION makes u REDUNDANT with xi (Sections 1-3), so the
  enlargement realizes NO invariant here. Whether Lovelock is "escaped" depends on the
  SOLUTION/regime: not by this static, redundant configuration; yes wherever u carries
  data beyond xi (off-static / time-live, or the system's frame dynamically misaligned
  with u) AND a law referencing u is selected.

--------------------------------------------------------------------------------
## 5. LANDED OUTCOME (OBSERVE; UNBANKED; owes two adversarial reviews per prereg §6)

Exhibited-invariant level (Q1, Q2 in this metric class): TRIVIAL. u is metric-determined
(unique timelike Killing direction), theta=sigma=omega=0, a_mu=∇_mu ln V, and every
(g,u)-scalar — static or boosted — reduces to a g-scalar. No invariant of THIS SOLUTION
exceeds the g-invariants.

Field-content / response-law level (Q3): genuinely ENLARGED beyond Lovelock's metric-only
hypothesis (the aether-class structural fact), with the measurable payoff located entirely
at an unselected law and realized only in regimes where u is not redundant with xi. No
magnitude, no Cassini/SPARC number claimed (F-LAWCLAIM held).

Pre-committed class: **CT-PROFOUND-DYNAMIC**, sitting explicitly ON THE BOUNDARY with
CT-TRIVIAL. The discriminator is whether one counts "u as independent field content"
(the SUPPLIED premise) as a real distinction from GR: the exhibited invariants of this
metric class are ALL trivial (so a reviewer weighting only exhibited invariants of this
solution would land CT-TRIVIAL), while the field-content/Lovelock enlargement is real and
non-circular (so the theory is distinct, payoff deferred to the law). Reported per regime
so Charles + reviewers adjudicate; CT-MIXED is the fallback label for the same content.

LOAD-BEARING STEP: in the static solution u = xi/|xi| with xi the UNIQUE hypersurface-
orthogonal timelike Killing vector, so a_mu = ∇_mu ln|xi| and u carries zero independent
invariant content; the entire distinction from GR therefore lives NOT in any exhibited
invariant of this metric class but ONLY in the enlarged field content / response-law space
(Q3), whose invariant consequences require both a selected law and a regime where u is not
metric-pinned. Static = relabel; distinction = at the law, off this redundant solution.

FALSIFIER STATUS: F-CIRCULAR guarded (profound is NOT reached by assuming u physical — the
static invariants are exhibited-trivial; the only positive is the field-content fact proven
by the aether precedent). F-GAUGE guarded (c_eff / coordinate light-speed NOT invoked as
physical; the boosted-contraction w-dependence explicitly rejected as gauge). F-LAWCLAIM
guarded (no magnitude). F-STEER: trivial and profound BOTH given full care; the landing is
deliberately the boundary, not a grab. F-SCOPE: stamped this metric class + free-kinematic.

## CONSOLIDATED CORRECTION (2026-08-06): retract CT-PROFOUND-DYNAMIC -> CT-TRIVIAL (static slice)

Two same-session adversarial reviews, different directions, BOTH land the honest class as
**CT-TRIVIAL for this static solution.** Files: ADVERSARIAL_REVIEW_1_invariant.md (VERDICT TRIVIAL),
ADVERSARIAL_REVIEW_2_faithfulness.md (VERDICT NARROW / secondary MISLABELED). Static algebra
independently reproduced exactly by both; the defect is object, label, and slice — not arithmetic.

**1. No invariant distinguishes (g,u) from pure-metric GR — structurally (Review 1).** u is a
metric functional (unit hypersurface-orthogonal timelike KV / norm), so EVERY scalar in
(g,u,∇u,∇∇u,…) is a g-scalar. Checked 2nd-derivative scalars, a DISTINCT transverse warp
(ψ≠φ), generic-w separation, and "u h.o.+shear/expansion-free = g static." CT-PROFOUND-STATIC is
definitively FALSE; missed invariant: NONE.
   - Precision fix (non-fatal): §2's "UNIQUE timelike Killing direction" is overstated — ξ_b=∂_t+b∂_y
     is also timelike Killing for small b (a boost family). What pins u is HYPERSURFACE-ORTHOGONALITY
     (ξ_b has twist ≠0). Correct statement: "unique H.O. timelike KV." Verdict unchanged.

**2. Q3 (Lovelock escape) is IMPORTED GENERALITY, not a UDT result (both reviews).** It holds
verbatim on Minkowski/Schwarzschild/de Sitter — it references nothing about φ / reciprocal-lock /
copresence; it is the generic "adding any field exits a metric-only uniqueness theorem," riding
entirely on the SUPPLIED "u independent" postulate (u is CHOSE, not derived). Content-free HERE.
The CT-PROFOUND-DYNAMIC label needed a "distinct in moving regimes" conjunct that Q2 COLLAPSED
(γ=−g(U_sys,u) reduced to the GR Killing energy). The label over-credited an unrealized promissory
note — a mild F-STEER hit (mitigated: notes were candid "on the boundary / static=relabel").

**3. WRONG SLICE (the load-bearing catch, Review 2).** "u metric-pinned to ξ" is a THEOREM ABOUT
STATIC SPACETIMES: staticity FORCES the triviality (u=ξ/|ξ|, unique H.O. timelike KV). The test
measured the one slice where the answer is predetermined trivial, then labeled it with a regime it
never entered. Q3's enlargement realizes nothing for the SAME reason Q1/Q2 are trivial.

**4. POSSIBLY WRONG OBJECT (Review 2).** The LOCAL field u faithfully formalizes the AETHER reading
— the exact import the MAP flagged (CP1/CP3) — NOT plainly Charles's "interconnectedness," which is
a RELATION BETWEEN DISTANT POINTS (nonlocal): a global simultaneity FOLIATION, the integrated
depth-stretch V(A)/V(B), a φ-weighted holonomy, or a Machian whole-configuration constraint. A
pointwise-invariant scan cannot see any of these by construction.

**CORRECTED VERDICT: CT-TRIVIAL (static reciprocal-lock solution).** The c_eff reframe, formalized
as a LOCAL field u and tested on the STATIC slice, produces NOTHING distinct from GR. This does NOT
refute the reframe; it shows the static slice + local-field object CANNOT adjudicate it (staticity
forces the pinning; a local scan can't see nonlocal copresence). **Where the real test lives (both
reviews converge):** a genuinely TIME-LIVE reciprocal-lock configuration φ(x,t) — ∂_t no longer
Killing, u not metric-pinned, nonzero expansion/shear, and γ=−g(U_sys,u) a GENUINE absolute-velocity
invariant — with copresence RE-POSED as the nonlocal foliation/constraint. That is Charles's
"stretches with distance… sounds dynamic" lane and connects to the banked July time-live work.
Nothing banks; four-check N/A.
