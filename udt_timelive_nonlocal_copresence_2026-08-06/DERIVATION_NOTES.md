# Derivation notes — time-live nonlocal copresence (Probe 1). LEAD / UNBANKED.

Date 2026-08-06. Branch grok. Mode: OBSERVE (report what is there; TL-TRIVIAL given equal care).
Exact sympy 1.13.1, float-free, no linearization. Author: driver (Opus).

**SCOPE STAMP on EVERYTHING below**: time-live reciprocal-lock metric class, free-kinematic
(NO law, NO matter dynamics, NO magnitude — F-LAWCLAIM held). Not a general theorem.
Contract: `MAP_AND_PROBE1.md` (frozen). Objects per contract: N2 between-points depth
`delta_t = -(1/2)log(lambda_timelike)` of the frame-covariant strain C_A=A^dagA (the FULL-STRAIN
depth — NOT the exact coboundary delta_a, which has identically zero holonomy and is the wrong
object per the 08-05 retraction), and its N3 loop holonomy.

Metric (THEORY, canon C-2026-06-18-1): `ds^2 = -e^{-2phi(t,x)}c^2 dt^2 + e^{2phi(t,x)}dx^2`
(+ isotropic transverse e^{2phi}(dy^2+dz^2) where a question needs 3+1), phi_t != 0 (CHOSE).
Copresence u = d_t/sqrt(-g_tt): u^a=(e^{phi}/c,0,0,0), u_a=(-c e^{-phi},0,0,0), u.u=-1 [verified].

Scripts (all exact, outputs transcribed verbatim): q1_kinematics.py (Killing L_xi g),
q1b_killing.py (full Killing system 1+1), q1c_kinematics.py (3+1 congruence kinematics),
q2q3_boostcurv.py (depth 1-form + boost curvature, general-diagonal + lock), q2b_gamma.py
(gamma, Killing-energy collapse, frame-invariant sectional curvature).

--------------------------------------------------------------------------------
## Q1 — UN-PINNING (DERIVED, exact)

**(a) d_t is NOT Killing time-live.** L_{d_t} g has nonzero diagonal entries, every one carrying
a factor phi_t (q1_kinematics.py):
  (L g)_tt = 2c^2 e^{-2phi} phi_t,  (L g)_xx = (L g)_yy = (L g)_zz = 2 e^{2phi} phi_t.
phi_t != 0  =>  d_t not Killing.

**(b) No stationary timelike KV for generic phi.** Full Killing system, V=P(t,x)d_t+Q(t,x)d_x
(q1b_killing.py), positive prefactors dropped:
  (a) P_t = P phi_t + Q phi_x
  (b) Q_x = -(P phi_t + Q phi_x)
  (c) P_x = (e^{4phi}/c^2) Q_t
On the static branch (phi_t=0) this admits V=d_t (P=1,Q=0) — recovering the static pinning.
Time-live it is over-determined: (a)/(b)/(c) are three first-order PDEs whose integrability
imposes a differential constraint on phi that a generic time-live phi does not satisfy => no
timelike KV. (Non-existence is regime-generic, not proven for every phi; the decisive, phi-free
un-pinning proof is the kinematics below.)

**(c) Congruence kinematics, 3+1 (q1c_kinematics.py, EXACT):**
  acceleration  a_b = (0, -phi_x, -phi_y, -phi_z),  a^2 = e^{-2phi}(grad_space phi)^2   [as static]
  expansion     theta = 3 e^{phi} phi_t / c        <-- NONZERO time-live (was 0 static). TURNS ON.
  shear^2       sigma_ab sigma^ab = 0              <-- stays zero (isotropic spatial stretch)
  twist^2       omega_ab omega^ab = 0              <-- stays zero (u ~ dt gradient: h.o. always)

**DECISIVE un-pinning proof (F-GAUGE-clean, no posit):** a hypersurface-orthogonal timelike
Killing vector forces theta=sigma=omega=0 for its unit congruence. Time-live theta = 3e^{phi}phi_t/c
!= 0, so u is provably NOT the unit vector of any h.o. timelike KV. The static pinning theorem
(u = xi/|xi|, the load-bearing cause of CT-TRIVIAL) DOES NOT APPLY time-live.

**What turns on:** expansion only (isotropic "dynamic stretch", Charles's picture); shear and twist
stay zero. So copresence is irrotational and shear-free but EXPANDING — a genuinely non-static
congruence.

**Is copresence still metric-determined?** As a DIRECTION, u = unit normal to t=const is still a
metric construction — but the t=const foliation is no longer singled out by a symmetry (no KV), so
it is a CHOSEN slicing, not metric-forced to a unique frame. The genuine independent content lives
NOT in a new local vector datum (that would be the aether import, F-IMPORT) but in the NONLOCAL
depth holonomy (Q2a) and the un-collapsed velocity scalar (Q2b). UN-PINNED: YES (theta turns on).

--------------------------------------------------------------------------------
## Q2a — THE NONLOCAL INVARIANT (delta_t 1-form + N3 loop-period density; DERIVED, exact)

The full-strain depth delta_t transports by the boost connection omega^0_1 (orthonormal coframe
E0=e^{A}c dt, E1=e^{B}dx; the depth = timelike-leg boost accumulation). Its exterior derivative is
the N3 loop-period density (boost curvature 2-form R^0_1 = d omega^0_1; no omega^omega term, single
2D boost). Computed for the GENERAL diagonal metric ds^2=-e^{2A(t,x)}c^2 dt^2+e^{2B(t,x)}dx^2, then
specialized to the LOCK A=-phi,B=+phi (q2q3_boostcurv.py, q2b_gamma.py — EXACT).

**Depth 1-form (general diagonal):**  omega^0_1 = c e^{A-B} A_x dt + (e^{B-A}/c) B_t dx.

**N3 loop-period density (general diagonal, EXACT):**
  R^0_1|_{dt^dx} = (e^{B-A}/c)[B_tt + B_t(B_t - A_t)]  -  c e^{A-B}[A_xx + A_x(A_x - B_x)].

**LOCK (UDT, A=-phi,B=+phi):**
  R^0_1|_{dt^dx} = c e^{-2phi}[phi_xx - 2 phi_x^2]  +  (e^{2phi}/c)[phi_tt + 2 phi_t^2].
Frame-invariant sectional curvature (q2b_gamma.py, unambiguous / gauge-free):
  R_{^0^1^0^1} = { c^2(2 phi_x^2 - phi_xx) - e^{4phi}(2 phi_t^2 + phi_tt) } e^{-2phi} / c^2.

**Is the N3 holonomy NON-EXACT time-live? YES** — R^0_1 != 0 => omega^0_1 is not closed =>
delta_t has genuine path-dependence / nonzero loop period (a real, non-gauge invariant; it is the
(t,x)-plane sectional curvature, frame-invariant, not gaugeable). This is a GENUINE nonlocal
invariant, unlike the coboundary delta_a (loop period identically 0 for all a — the wrong object).

**CRITICAL HONESTY (F-STEER):** it is NOT "non-exact time-live in CONTRAST to an exact static
case." The STATIC reduction (phi_t=0) is  R^0_1 = c e^{-2phi}[phi_xx - 2phi_x^2] != 0 — the delta_t
holonomy is ALREADY non-exact STATICALLY (matches the 08-05 Review-1 "honest residual": delta_t is
path-dependent stationary AND time-live). Time-live does NOT create the holonomy; it merely ADDS
the term (e^{2phi}/c)[phi_tt + 2phi_t^2]. So the nonlocal invariant exists, but its existence is
not what time-live buys — it is ordinary spacetime (sectional) curvature, present already static.

--------------------------------------------------------------------------------
## Q2b — ABSOLUTE-VELOCITY INVARIANT gamma = -g(U,u) (DERIVED, exact; q2b_gamma.py)

Matter 4-velocity U at rapidity w vs copresence: U = u cosh w + e_x sinh w. Then:
  gamma = -g(U,u) = cosh w.
By itself gamma is just the probe's rapidity — a CHOSEN-probe scalar (F-GAUGE): coordinate-invariant
for a given U, but its value is a property of (geometry + a chosen U), not of geometry alone. GR can
form -g(U,n) for any chosen unit n; gamma is "absolute velocity" ONLY if u is a PHYSICALLY preferred
frame (copresence) — that is the CHOSE posit, not a metric fact.

**The static collapse and its time-live fate (the real content):**
  E = -g(U, d_t) = c e^{-phi} cosh w,   |xi| = sqrt(-g(d_t,d_t)) = c e^{-phi},   E/|xi| = cosh w = gamma.
So the ALGEBRAIC identity gamma = E/|xi| still holds time-live. BUT statically E was a CONSERVED
Killing energy (d_t Killing) — so static gamma reduced to a conserved metric charge (=> trivial,
the CT-TRIVIAL collapse). Time-live d_t is NOT Killing (Q1), so E is NOT conserved along geodesics
— it is not a Killing energy, just an instantaneous contraction. Therefore time-live gamma is a
genuine scalar NOT reducible to any conserved metric charge: the structural obstruction that made
static gamma trivial is REMOVED.

**Verdict Q2b:** gamma is a genuine NON-KILLING scalar time-live (yes) — but (i) its physical status
as absolute velocity rests on the copresence posit (CHOSE), and (ii) the un-collapse happens for ANY
metric that loses the timelike KV. So it is real but NOT lock/UDT-specific (feeds Q3, F-GENERIC).

--------------------------------------------------------------------------------
## Q3 — UDT-SPECIFICITY via lock-relaxation (the bar the static probe failed; DERIVED)

Test (contract): relax the reciprocal lock g_tt g_xx = -c^2 (A=-B) to INDEPENDENT A,B; do the
invariants vanish/trivialize, or survive? (Survive => generic => F-GENERIC; vanish => lock content.)

- **N3 period density:** the GENERAL-diagonal R^0_1 (independent A,B) is NONZERO (Q2a formula). It
  does NOT vanish or trivialize off the lock. The lock A=-B is a smooth specialization, nothing is
  forced to zero by it. => the boost/sectional-curvature holonomy is F-GENERIC (any curved 2D metric;
  present already static). NOT lock-specific.
- **theta un-pinning:** theta ~ (time-derivative of the spatial metric) is nonzero for ANY B_t != 0,
  independent of the lock. => generic to any time-dependent metric. NOT lock-specific.
- **gamma un-collapse:** loss of the conserved Killing energy follows from loss of the timelike KV,
  which any time-dependent metric suffers. => generic. NOT lock-specific.

No invariant found in Q1-Q2 references phi / reciprocal-lock / copresence SPECIFICALLY. Every one is
the generic "time-dependent (or merely curved) GR metric" content — exactly the F-GENERIC failure the
static probe's Q3 hit, now confirmed to persist off-static. (Lock-only coordinate features exist,
e.g. sqrt(-g)=c constant in 1+1 under the lock, but that is a coordinate/gauge property, not a scalar
invariant — F-GAUGE.)

--------------------------------------------------------------------------------
## LANDED OUTCOME (OBSERVE; UNBANKED; owes two adversarial reviews + external per contract)

**Class: TL-INVARIANT-GENERIC** (a real invariant, but GR-generic, not UDT-specific).

- NOT TL-TRIVIAL: the un-pinning is REAL — theta = 3e^{phi}phi_t/c turns on, no h.o. timelike KV,
  and gamma no longer reduces to a conserved Killing energy. The static pinning theorem is broken.
- NOT TL-INVARIANT-UDT: by the Q3 lock-relaxation test every invariant/structure (boost holonomy
  R^0_1, un-collapsed gamma, expansion theta) survives with INDEPENDENT g_tt,g_xx and is present in
  any time-dependent GR metric — none references the reciprocal lock specifically. The delta_t
  holonomy is moreover non-exact ALREADY static (ordinary sectional curvature), so time-live does not
  even create it.

**LOAD-BEARING STEP:** the Q3 lock-relaxation test — the general-diagonal boost curvature
R^0_1 = (e^{B-A}/c)[B_tt+B_t(B_t-A_t)] - c e^{A-B}[A_xx+A_x(A_x-B_x)] is nonzero for INDEPENDENT A,B,
so the nonlocal depth holonomy (and the theta un-pinning and the gamma un-collapse) are generic
features of time-dependent GR metrics, NOT consequences of the reciprocal lock g_tt g_xx=-c^2. The
invariants are genuine (clearing F-GAUGE and TL-TRIVIAL) but not UDT-specific (failing F-GENERIC).

**FALSIFIER STATUS:** F-STEER guarded (I wanted TL-INVARIANT-UDT; the algebra gave GENERIC and I
report it — the holonomy is non-exact static too, not a time-live prize; gamma is cosh w, a probe).
F-GAUGE guarded (gamma-as-cosh-w and coordinate light speed / sqrt(-g)=c NOT invoked as invariants;
the reported invariant is the frame sectional curvature). F-GENERIC = the operative verdict (Q3).
F-IMPORT guarded (no aether/foliation action adopted; copresence posed as the native N2 depth
relation, not a local vector field). F-SCOPE stamped: time-live reciprocal-lock, free-kinematic.
F-LAWCLAIM held (no magnitude, no law, no matter dynamics).

**Honest residual (NOT a rescue):** the deepest faithful object N4 (Machian whole-configuration
constraint) needs a matter source and was deferred by the contract; nothing here tests it. If UDT
content lives in copresence, it is not visible in the free-kinematic invariants of the bare lock —
it would need the law/source (N4) that references phi/copresence non-generically. Nothing banks;
four-check N/A (working note).

## CONSOLIDATED (2026-08-06): both reviews -> TL-INVARIANT-GENERIC stands, STRENGTHENED; one residual

Files: ADVERSARIAL_REVIEW_1_missed_invariant.md (F-GENERIC-CONFIRMED), ADVERSARIAL_REVIEW_2_object_
residual.md (OBJECT-TOO-LOCAL). They DISAGREE on one object; the disagreement resolves in favor of
Review 1 via a decisive general argument, leaving one un-computed corner.

**Agreed (both, exact):** Q1 un-pinning is REAL (theta=3e^phi phi_t/c turns on; a HSO timelike KV
forces theta=0, so time-live genuinely un-pins copresence — the static pinning theorem is broken).
The LOCAL invariants are all GR-GENERIC (survive relaxing the lock). No reverse over-deflation on the
tested objects.

**Review 1's DECISIVE addition (verified exactly): the reciprocal lock g_tt·g_xx=-c^2 is a GAUGE
CONDITION on the bare metric.** A spatial reparametrization x=h(X) BREAKS the lock while leaving every
curvature invariant unchanged (Ricci scalar diff = 0 exactly, all sampled points). (Independent
reasoning: any static diagonal metric -f dt^2+h dx^2 reaches the lock via h'=c/sqrt(fh) — always
integrable — so "being in lock form" is a coordinate choice, not a geometric restriction.) Therefore
**no bare-metric invariant — local, nonlocal, or topological — can be lock-specific**, because
lock-specificity is not a diffeomorphism-invariant property. A holonomy PERIOD is a diffeo-invariant,
so it too is preserved by the lock-breaking diffeo -> not lock-special. This LOGICALLY resolves the
disagreement with Review 2.

**Review 2's residual (the one un-computed corner):** the depth-boost holonomy oint omega^0_1 around
a NONCONTRACTIBLE time-winding cycle (cyclic time) — a matter-free Aharonov-Bohm-type period a local
scan cannot see, carrying the lock combination A-B=-2phi, live in the banked T-lane (n_t). Review 1's
gauge proof COVERS it in principle (the period is diffeo-invariant, preserved by the lock-breaking
reparam, which is t-independent and compatible with cyclic time). But it was NOT directly computed on
the noncontractible manifold. HONEST STATUS: very likely gauge (Review 1's proof), one cheap direct
computation would close it definitively.

**CONSOLIDATED VERDICT: TL-INVARIANT-GENERIC, strengthened — the free-kinematic (bare-metric,
vacuum) level is EXHAUSTED, and we now know WHY: the reciprocal lock is a gauge condition, so
phi/copresence carries NO invariant content until anchored by a SOURCE or the LAW.** The N4/Machian
(matter-anchored) gate is therefore NOT a premature deferral (Review 2's worry) but the FORCED next
gate — Review 1 concurs: "a phi-coupled source/field-equation CAN see the metric form the vacuum
invariants cannot; that is the correct next gate." Corrected scope stamp: bare-metric, free-kinematic,
contractible-topology + coordinate-normal copresence; the cyclic-time winding-holonomy is the single
flagged residual.

**CANON TENSION (flag for Charles, do NOT overturn unilaterally):** this GENERALIZES the 2026-08-05
E=mc^2 finding (lock = Schwarzschild areal chart, GR-shared). Canon C-2026-06-18-1 frames the
reciprocal lock as "the UDT departure from GR"; the accumulating evidence is that the lock is
GAUGE/GR-shared and the genuine departure (if any) lives ONLY in the matter/law coupling, never in
the vacuum metric form. Candidate canon revision; Charles's call. Nothing banks; four-check N/A.
