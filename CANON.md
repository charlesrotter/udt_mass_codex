# CANON — Charles-Canonized Statements

Per the Self-Hardening Protocol, only Charles canonizes. This ledger
records canonization events: exact statement, date, what it forces,
provenance. Append-only.

## C-2026-06-10-1: The areal reading of positional dilation (R-areal)

**Statement:** Positional dilation grows with the AREAL radius: phi is a
function of r_areal (the invariant sphere size, sqrt(Area/4pi)), and the
B=1/A condition (g_tt * g_rr = -1) holds in the areal chart.

**Forces (banked theorems):**
- rho = r exactly (C2 theorem,
  native_positional_dilation_distance_readings.py): P0's areal choice is
  now a THEOREM, not a silent postulate.
- Branch (iii) of the discreteness map is CLOSED in the static sector
  (threshold rigidity theorem + areal reading): no saturating areal
  function, no static throats, no static threshold lifting.
- The beta(rho) derivation program is MOOT in statics.

**Provenance:** macro_sector_fork_resolution.md — the data-validated
macro stack (d_L = r(1+z), D_M = r, Misner-Sharp; Pantheon+ chi2/dof
0.94 beating LCDM at 0 free params; DESI BGS 0.90 sigma) operationally
instantiates this reading. Canonized by Charles 2026-06-10.

## C-2026-06-10-2: The finite-cell canon

**Statement:** Dilation is monotone on a finite domain terminated by a
physical boundary, mirrored across phi -> -phi. The universe is a finite
cell ([0, r_CMB], phi: 0 -> ln(1101) at the CMB boundary); matter cells
are finite inside-out cells (phi: 0 at the interface -> -infinity at the
core endpoint). There is no spatial infinity.

**Forces:**
- The open-domain threshold theorems lose their premise globally:
  branch (ii) (compact domain) is realized BY the cosmology.
  Discreteness is native and automatic; the box-control scaling is
  reinterpreted (the box is the universe).
- The matter cell's finite domain and its phi=0 interface are PHYSICAL
  structure (the mirror of the CMB boundary), not a hand-placed wall.
- The sharp open question becomes spectral SCALE-AUTONOMY: what makes
  particle-scale cells spectrally autonomous from the Gpc-scale global
  domain.
- The C=0 vs C>0 vacuum-selection question dissolves at macro scope
  (the cosmological profile is sourced; "vacuum gap").

**Provenance:** macro_sector_fork_resolution.md (legacy CG finite-domain
Class A closure, lines 846-859; current dispatches, Theory Rule 5).
Canonized by Charles 2026-06-10.

## C-2026-06-10-3: Program redirect for native discreteness

**Statement:** The native-discreteness program redirects to:
(a) the NONSTATIONARY phi-angular sector — the rung-2 weld
    (d_r(e^{-2phi0} H1) = 2 d_t(delta phi) + d_t K - ...), a derived,
    CMB-data-tested dynamical phi-angular coupling outside every static
    no-go — as the surviving home of the phi-angular interaction hunch;
(b) the transfer-ladder route (no continuum threshold needed);
(c) multi-cell/ensemble asymptotics (the orchestra).
Static throat/threshold-lifting mechanisms are retired per C-1.

**Provenance:** macro_sector_fork_resolution.md; AUDIT.md (S116 weld
derivation). Canonized by Charles 2026-06-10.

## Provenance annotation (2026-06-10, appended)

The origin prompts (2025-08-12, Grok; see PROVENANCE.md) bear on two
canon entries: C-1's areal reading is a later refinement — the original
"time dilation with distance" left the distance notion unspecified, and
R-areal was fixed by macro data. C-2's finite-cell canon matches the
founding intent directly — Prompt 2 already asserts redshift increasing
asymptotically "as you approach the universe boundary." Recorded as
provenance/consilience, not as evidence for either canon.

## C-2026-06-13-1: The nonstationary diagonal sector propagates in T

**Statement:** The whole metric, in its diagonal dilation-tie class
(g_tt = -e^{-2phi}, g_rr = +e^{2phi}), is STRICTLY HYPERBOLIC in time:
its own field equation has principal-part signature (-,+,+), with finite
positive wave speeds c_r^2 = e^{-4phi}, c_theta^2 = e^{-2phi}/r^2. The
metric PROPAGATES in T; it does not cell-collapse to an elliptic dead end.
The wave is physical (the Ricci scalar carries real phi_TT / phi_T^2).

**Forces (and what it does NOT force):**
- The banked negative #22 ("no sector propagates hyperbolically in T;
  cells do not evolve") is CONDITIONS-CHANGED on those clauses: they
  rested on a single sign error (v_a3.py time-kinetic term +f_T^2/f^2,
  Euclidean/elliptic, vs the Lorentzian -f_T^2/f^2). The original
  "Hadamard ill-posedness" WAS the sign error (high-k discriminator:
  corrected sign bounded; v_a3 sign blows up ~1e60).
- It does NOT lift the no-shaped-matter conclusion: the fate polynomial
  2 f q v_h (f q v_r - v_h)^3 is f_T-free, so MOTION NEVER SOURCES SHAPE.
  The diagonal metric evolves but makes no nonstationary matter by itself.
- It CONFIRMS the C-2026-06-10-3 redirect's bet that the live home of the
  phi-angular interaction is the NONSTATIONARY sector, and it relocates
  the program's open frontier to the OFF-DIAGONAL angular row (where the
  centrifugal term is reported to flip attractive, where the gap test
  needs the measure-weighted self-adjoint eigenproblem, and where the
  "e_T never timelike" record is least settled).

**Provenance:** solution_space_map.md (queue-head open-ended scan);
ns_scan_results.md; blind verifier ns_scan_verifier_results.md
(agent a9cfcd85385bff920), independent re-derivation + high-k test.
Canonized by Charles 2026-06-13.

## Standing flag (Charles, 2026-06-10, appended)

The Planck blackbody derivation in the macro/CMB work relies on
quarantined or withdrawn mass-emergence theories. Macro observables that
ride it may be used as HYPOTHETICAL/common-mode layers only, never as
derived foundations. Do not build on sand: any macro computation must
carry a provenance grade per layer, and weld-discrimination conclusions
must be differential (conditional on the flagged common pipeline).

## C-2026-06-14-1: B=1/A is SOURCED inside matter by the angular sector

**Statement:** Inside matter, the defining UDT relation g_tt g_rr = -c^2
(equivalently B = 1/A, the two radial dials locked) is not merely postulated
but DERIVED: UDT's own angular-sector field — the unit 3-vector n_a whose
winding density is the H1 area form omega_H1 = eps_abc n_a dn_b ^ dn_c (the
same object carrying N=3, q=1/3) — sourced by the minimal covariant
two-derivative Lagrangian L = -(xi/2) g^{mu nu} d_mu n_a d_nu n_a built from
the UDT metric measure, produces a stress tensor with T^t_t = T^r_r in any
PURELY-ANGULAR (no-radial-gradient) configuration. Since the metric identity
g_tt g_rr = -c^2 <=> G^t_t = G^r_r <=> p_r = -rho, this T^t_t = T^r_r source
is exactly what the relation demands; it leaves the theta-equation that fixes
g_rr = e^{2phi} intact (deg-1 hedgehog: T^theta_theta = 0). Hence B=1/A holds
inside matter as a THEOREM of the angular source, not a choice.

**Scope / boundaries (binding — do not overstate):**
- Holds for any purely-angular config (d_r n = 0); the degree-1 hedgehog
  n = x/r is the unique member with also T^theta_theta = 0.
- ROBUST to native additions: a Skyrme term, a potential V(n), or the
  eta-seal coupling all preserve T^t_t = T^r_r (they change T^theta_theta and
  the solid-angle-deficit value only). So B=1/A does NOT hinge on the
  minimal-model choice; the SPECTRUM (masses) will, but the EOS does not.
- BREAKS under a radial twist: for Theta = Theta(r),
  p_r + rho = xi e^{-2phi}(Theta'(r))^2 >= 0, zero iff Theta' = 0. A
  realized smoothed-core soliton satisfies p_r = -rho exactly only where
  Theta' = 0; the pure topological n = x/r is exact everywhere.
- A canonical SCALAR cannot do this (p_r + rho = e^{-2phi} phi'^2 > 0): the
  source MUST be the angular/topological sector. phi RESPONDS.

**Forces:**
- RESOLVES the B=1/A fork (external_input_notes.md fork #1, the queue head)
  in favor of KEEP. Model A ("relax B=1/A inside matter; a scalar sources a
  two-function interior") is excluded for the topological sector: the
  one-function form is sourced, not relaxed.
- STRENGTHENS C-2026-06-10-1: the areal-reading B=1/A, previously a
  vacuum-validated postulate, is now derived inside matter via the angular
  source. The relation g_tt g_rr = -c^2 is the first defining UDT relation
  shown to be SOURCED by a derived UDT object rather than postulated.
- Confirms the convergent direction (our findings + two external models): the
  angular/topological sector is the SOURCE of matter, phi is the response
  (slaved via p_r = -rho). This is the program's FIRST constructive positive.

**Provenance:** angular_lagrangian_results.md (constructor, Claude Opus 4.8,
agent a440405d389552f39); angular_lagrangian_verifier_results.md (BLIND
adversarial verifier, Claude Opus 4.8, agent a4edbefa0e29edfa2) — anchor
genuineness independently re-derived from the original dpf density
(rescued_workspaces/.../v_c1_closedforms.py:90-99), I_native == G1 to ~1e-48;
sympy-exact stress tensor + V100 float64 machine-zero over 4096 points. Two
non-blocking errata recorded (G1/H prose; deficit sign convention).
Canonized by Charles 2026-06-14.

## Refinement to C-2026-06-14-1 (appended 2026-06-14; exterior-vs-interior)

The native angular Lagrangian is now settled as L2 + L4 — the minimal
two-derivative kinetic term PLUS the native winding-current term L4 =
-(kappa/4)|omega_H1|^2_g (the Skyrme term DERIVED as the metric-norm of our
own H1 area form; an import that named a real UDT object; NO bulk potential —
eta=1/18 is a seal/boundary object). L4 stabilizes a soliton of definite size
sqrt(kappa/xi) (one scale), curing the Derrick collapse of the minimal model
(#43). CONSEQUENCE for C-2026-06-14-1: a REALIZED sized particle carries a
radial profile (Theta'!=0 through its body), so by the canon's own scope
(B=1/A breaks under a radial twist) g_tt g_rr = -c^2 is EXACT only in the
particle's UNWOUND EXTERIOR and is EOS-softened (p_r+rho = e^{-2phi}Theta'^2
(xi + 2 kappa sin^2 Theta/r^2) > 0) throughout its twisting interior — the
same structure as a GR star (B=1/A exact outside, corrected inside). The
canonized "B=1/A sourced inside matter" is thus the EXTERIOR / idealized-knot
law; a realized particle has a genuine EOS-softened interior body. This
REFINES, does not retract, C-2026-06-14-1 (blind-verified a1f2213b6410a6f35;
native_stabilizer_results.md). Recorded by Charles 2026-06-14.

## C-2026-06-18-1: The bare metric form is DERIVED from relativity (exponential + B=1/A, source-free)

**Statement:** Requiring UDT to REMAIN RELATIVISTIC derives the functional form of
the metric; it is not assumed. From three relativistic requirements —
(R1) positional dilation depends only on DIFFERENCES in phi (no position is
geometrically privileged); (R2) dilations COMPOSE consistently across intermediate
positions; (R3) MUTUAL RECIPROCITY (each position sees the other's clock run slow,
with neither preferred) — it follows that:
- the clock-rate law is EXPONENTIAL in phi: g_tt = -e^{-2phi}c^2 (forced uniquely by
  R1 + physical regularity; R2 then automatic);
- the time and radial components obey the reciprocal lock B = 1/A, i.e.
  g_tt g_rr = -c^2, SOURCE-FREE / KINEMATIC (from R3, no matter, no action, no field
  equation, no asymptotic flatness).
phi is defined only up to an additive constant (only differences are physical = R1 as
a gauge freedom). The derived structure remains relativistic (Lorentzian signature for
all phi; local Lorentz invariance intact).

**Scope / one named caveat (binding — do not overstate):**
- The B=1/A step uses ONE natural analog identification (P8): the direction conjugate
  to time under reciprocity is the phi-GRADIENT (radial) direction, not a transverse
  one. This is the physically obvious choice but it IS a choice, not forced by relativity
  in the abstract. Reciprocity transverse to grad phi is vacuous (zero phi-difference =>
  identity). No circularity (the identification does not assume B=1/A). The exponential
  law (R1) carries no such caveat.

**Forces:**
- Relativity locks ONLY the exponential dilation law + the reciprocal tie along grad phi.
  It leaves FREE: the angular/transverse block, all off-diagonal/shift terms (rotation,
  shear), the TIME-DEPENDENCE of phi (non-stationary allowed), the chart, and the
  topology. Therefore STATIC + SPHERICAL + DIAGONAL + AREAL-r are four INDEPENDENT
  CHOICES, not consequences — they must not be smuggled; they are part of the solution
  space to be solved/observed.
- RECONTEXTUALIZES C-2026-06-14-1: B=1/A is relativistic-KINEMATIC and UPSTREAM. The
  angular-source derivation (T^t_t = T^r_r => B=1/A) is DOWNSTREAM CONSISTENCY — matter
  must RESPECT the relativistically-forced tie; it does not create it. C-2026-06-14-1 is
  refined (not retracted): it remains true that the angular source respects/realizes the
  tie inside matter.
- The Einstein identity G^t_t - G^r_r = -(AB)'/(rAB^2) becomes a downstream check: with
  AB=1 forced, it vanishes identically for arbitrary A, no source.

**Provenance:** relativistic_metric_rederivation_results.md (constructor, Claude Opus 4.8,
agent aa7c4d21d426fea02; relrederiv_checks.py sympy-exact) + BLIND adversarial verifier
(Claude Opus 4.8, agent ad75fef845c31a128; independent re-derivation, verify_relrederiv_*.py)
— STANDS-CONDITIONALLY on the named premises P4 (regularity, physically mandatory) and P8
(the reciprocity slot-identification). Owner stated the R1/R2/R3 requirements 2026-06-18.
Canonized by Charles 2026-06-18.

---

## C-2026-07-02-1 — The universe-cell anchor is a Δφ statement; the zero sits AT the CMB fold

**Statement:** The finite-cell canon C-2026-06-10-2's wording "the universe is a finite cell
([0, r_CMB], phi: 0 -> ln(1101) at the CMB boundary)" is CLARIFIED (not retracted): the
physical content is the DIFFERENCE Δφ = φ(CMB fold) − φ(core) = ln(1101) (1+z = e^Δφ). The
blind-verified fold derivation (universe_cell_fold_jc_sigma_results.md: the odd fold φ→−φ pins
φ = 0 AT the CMB fold) fixes the canonical convention: **φ(CMB fold) = 0, interior running
φ: −ln(1101) → 0.** In Branch P the absolute shift is physical (e^{−2φ} source), so this is a
substantive convention, not gauge; all universe-cell work of 2026-07-02 (T2 identities, T3
closure, the cascade/ladder program) is built on it and blind-verified within it.

**Forces:** the fold-pinned convention is canonical for all cell solves; the original wording
is to be read as the same Δφ with the zero relocated to the fold.

**Provenance:** fold JC derivation + blind verification (agents a15ecc62590d15bd4 /
a18115fe9d95cfb84); gauge flag raised in universe_cell_fold_jc_sigma_results.md; operated as
Δφ by Charles from the T2 ruling (breathing edges) onward.
**Charles-authorized 2026-07-02 (session ruling: "the canon Δφ amendment... all owed").**

---

## C-2026-07-03-1 — Canonical-energy orientation: E_phys = −∫L (flat-limit anchored; SCOPE-TAGGED)

**Statement:** For the round-static Branch-P reduction on the banked pins (Route-A action,
per-4π units, seal-proper clock t via φ(r_s)=0), the physical energy orientation is
**E_phys = E_can = −∫L_banked dr**, anchored by the flat-space decoupled limit (a Category-A
reference limit): at φ=0, ρ=r the banked L reduces to −U, so E_can = +∫U ≥ 0 — the standard
positive potential energy of a static matter lump; the opposite sign would assign flat-space
matter NEGATIVE energy. The competing MS/ε-positivity anchor (E_phys = +∫L) is REFUTED AS
FORCING (no positivity theorem on a closed cell with an indefinite kinetic sector; the
negative cell totals are binding-energy structure — a ~1‰ cancellation, +1149 matter vs
−1161 geometry; the anchor is not sign-coherent across rungs). Neither anchor is a theorem;
this entry records Charles's adjudication of the call.

**SCOPE TAG (binding — travels with every use of this orientation):** E_can is the Noether
energy of the ansatz-fixed STATIC REDUCTION; the TIME SECTOR of the native action is
UN-DERIVED. The full theory's t-Hamiltonian (constraints + boundary terms) is named future
work, and its derivation re-opens this entry (CONDITIONS-CHANGED discipline applies).
Banked trap: H ≡ 0 is the r-flow Hamiltonian, NOT the t-energy.

**Forces:** the stability-table reading. Under E = −∫L: fundamentals have ZERO finite
energy-downhill directions (the universal ultra-soft fold-pair mode is energy-UPHILL, weakly
restoring); excited rung N has exactly N+1 energy-downhill directions; the twin fundamental
(2,1) has one solid downhill.

**Provenance:** ladder_energy_orientation_results.md — aim-blind chain (deriver
ae6e21433233df796, CAS 16/16; blind adversarial verifier a15704db803b00023, own
Christoffel/Ricci from scratch; the deriver's own preferred anchor was refuted by its
verifier — the aim-blind protocol working as designed). External cross-check vetted the
presentation and concurred (2026-07-03).
**Canonized by Charles 2026-07-03 (ruling R1 of the stability ponder).**

---

## C-2026-07-03-2 — The fundamentals are STABLE (minimum-class, round-static scope); the ladder SELECTS them: the universe = the N=0 ground state of its own ladder

**Statement:** Under C-2026-07-03-1, within round-static constraint-respecting counting
(exact hyperbolic-pair + Haynsworth counting on the derived stability operator; v₀=0
convention pinned by theorem):
- the FUNDAMENTAL rungs are **MINIMUM-CLASS**: zero finite energy-downhill directions; their
  single universal ultra-soft fold-pair mode (blind-verified, `ladder_softmode_results.md`)
  is energy-uphill;
- EXCITED rung N has exactly N+1 energy-downhill directions — a clean Morse ladder vanishing
  at the ground;
- the TWIN FUNDAMENTAL (2,1) is the unique fundamental-class rung with a solid downhill
  (−5e-4), qualitatively distinct;
- therefore the landscape SELECTS the fundamentals uniquely: **the universe = the N=0 ground
  state of its own ladder.** This emerged from counting under the stability filter's
  pre-registered mini-MAP — not from a merit gate.

**CLASS TAG (binding — the word "stable" always carries it):** stability is granted WITHIN
the round-static constraint-respecting counting only. ANGULAR stability and DYNAMICAL
(time-evolution) stability are named, scoped follow-ons — not yet run. The soft mode's
MAGNITUDE rides a CHOSE (α,β) mass convention; its sign/uphill-vs-downhill character is the
solid content. Inherits the C-2026-07-03-1 scope tag (un-derived time sector).

**Canon-adjacent NOTE (Charles ruling R4 — a note, NOT canon):** the verified fold-pair soft
mode matches the pre-arc F5 ledger line — "the otherwise-flat dilatation modulus, weakly
pinned at criticality" — written before the stability arc; resonance language was kept out of
ALL agent prompts and the identification arrived uninvited. Recorded as a consilience
observation: an identification, not a derivation.

**Provenance:** `stability_filter_miniMAP.md` (Charles's 3 pins) → `stability_operator_results.md`
(derived operator, blind-verified; bv13 caught a ±1 mix) → `stability_stage2_results.md`
(30-rung table, blind spot-pass) → `ladder_softmode_results.md` (fold-pair identification,
blind pass bv15) → `ladder_energy_orientation_results.md` (orientation). External cross-check
concurred (2026-07-03).
**Canonized by Charles 2026-07-03 (rulings R2 + R3 of the stability ponder).**

---

## C-2026-07-03-3 — Matter-cell core wording CLARIFIED: even fold at FINITE depth (the φ→−∞ core retired)

**Statement:** C-2026-06-10-2's wording "matter cells are finite inside-out cells (phi: 0 at the
interface → −infinity at the core endpoint)" is CLARIFIED (finite-cell content NOT retracted):
the φ→−∞ core was an early exploratory description from the first attempts to probe emergent
behavior, and Charles had let it go long before this derivation (Charles, 2026-07-03: "I let go
of negative phi to infinity a long time ago"). The DERIVED replacement (E1, blind-verified):
within round-static Branch-P, the embedded matter-cell core is an **EVEN MIRROR FOLD at FINITE
depth** — φ'(0) = ρ'(0) = f_r(0,θ) = 0 as natural boundary conditions from stationarity alone;
φ monotone up through the cell (the exact, matter-independent flux law (ρ²φ')' ≥ 0 excludes any
φ→−∞ dive with ρ bounded); the core values are FREE individually but pinned in combination by
the migrated critical closure **E_ang(core) = 2** (C2 chain, E1). The finite-cell content of
C-2026-06-10-2 — finite mirrored domains, no spatial infinity — STANDS unchanged.

**Scope:** exclusion of the φ→−∞ core is airtight within the probed asymptotic classes
(regular; power-law; plus the verifier's extensions: essential-singular φ with power ρ, ρ→∞
power-law, log-corrected dives). Combined essential/oscillatory asymptotics = the one named
residual gap. Round-static, diagonal, areal, concentric composite, Branch-P.

**Direction note (tagged HUNCH, not canon evidence — hypothesis discipline):** Charles's
standing picture (2026-07-03): the finite core depth/size is the native analog of a minimal
(Planck-like) length. Tagged consilience already in the derived record: E1's necessary maps
contain a DERIVED core-size floor ρ_c ≥ N√(κ/(2(2−ξN))) ∝ √κ — the canon carrier scale
√(κ/ξ) appearing as a minimal core size. Verifiers should aim hardest at results that would
confirm this picture.

**Provenance:** `microphysics_E1_composite_closure_results.md` (deriver ae9d381bdc0692d51,
CAS 24/24; blind adversarial verifier a50cf068b5ecf05e2, 8/8 HOLD, exclusion extended three
classes by the verifier's own probes).
**Canonized by Charles 2026-07-03 (ruling R-A of the E1 ponder, this session).**

**Canon-adjacent NOTE (NOT canon — Charles ruling R-C, E1 ponder 2026-07-03): THE CRITICALITY
MIGRATION.** Derived + blind-verified (same E1 provenance as above): carving a particle cell out
of the real universe cell moves the universe's critical closure inward — the ambient loses its
inner fold's U(ρ_c)=2 condition and the particle core inherits it as **E_ang(core) = 2**; the
chain is C2 (H-balance at the shared seal) + H_amb ≡ 0 forced at the real outer fold + H
conservation. The cosmos's "matter at one critical amount" rule reappearing at the particle
core. Graded a margin note, not canon: derived (stronger than the F5 identification note) but
one reduction deep (round-static, diagonal, concentric, Branch-P) — elevation waits on E2
showing cells actually close on it.

## C-2026-07-04-1 — Seal-involution SECTOR SPLIT (clarification of the mirror-fold canon, NOT an overturn)

**Statement:** the durable mirror-fold canon (seal = same-minus MIRROR FOLD; C-2026-06-10-2
"mirrored across φ→−φ") is CLARIFIED by localizing WHICH involution acts on WHICH sector:
- **STATIC fields' seal boundary conditions are governed by the SPATIAL depth mirror
  σ_φ : (φ→−φ, r→radial reflection).** Its fixed surface is φ=0 = r_s, a spatial crease, so it
  CAN impose a radial BC. φ is odd under σ_φ ⇒ **Dirichlet φ(r_s)=0** with φ' free ⇒ the flux
  seal q = Zρ_s²φ' (matches the already-derived fold JC, universe_cell_fold_jc_sigma_results.md:26-30).
- **TIME-ON / rotating / off-diagonal fields are governed by the temporal mirror t→−t** (the W6
  same-minus involution). A static field is t-independent, so t→−t imposes no BC on it (only a
  node-in-time, ω-blind); the temporal mirror's authority is exactly the sector the spatial mirror
  cannot reach.

This keeps the theorem-grade FOLD (seal ≠ edge; Z₂ quotient) and the durable canon intact, and
RE-ALIGNS with canon's own primary wording ("mirrored across φ→−φ"); the "= time reversal t→−t"
layer was always the row-conditional W6 gloss and is retained for its proper (time-on) sector. It
is NOT a new mechanism and NOT an overturn — it makes explicit which involution the banked fold-JC
derivation already used for the static fields.

**Correction folded in:** the pre-foundation `seal_junction_condition_results.md` (2026-06-21)
assigned φ EVEN→Neumann via t→−t; that is WRONG (t→−t cannot act on static φ; Neumann φ'(r_s)=0
would zero the flux q, destroying the flux seal). The corrected native assignment is Dirichlet
φ(r_s)=0. **Do not retain the old φ-Neumann wording.**

**Scope / open:** the "seal ignores ω" reading for a spinning phase is NOT part of this canon —
a time-on winding phase Nψ+ωt is governed by t→−t (→ Nψ−ωt), and whether the seal kills / pins /
permits ω is the OPEN NODE-1 question, not settled here.

**Provenance:** NODE 0.5 re-grade (deriver a648221a6b7df3aba) + blind adversarial verifier
(ad14fbc6898ee1930: C1/C2/C3 SUPPORTED, C2 as re-localization, C3 strengthened, C4 "seal ignores
ω" INCOMPLETE→held open; no GR-smuggle). Doc: `node05_seal_parity_regrade_results.md`.
**Canonized (as a CLARIFICATION) by Charles 2026-07-04.**

## C-2026-07-05-1 — P16: spinning matter stays φ-blind (Branch B refuted as native; conservative)

**Statement (Charles, verbatim):** P16-C stands. Branch B is refuted as a native-derived branch because
the spin→φ source requires importing physical-metric minimal coupling. That is outside the current
UDT-native action and violates the no-import rule. Branch A is the current lean: spinning matter remains
φ-blind under the derived channel-corrected coupling. **Do NOT overstate this as a universal theorem about
all possible future matter frames.**

**Scope / what it means:** the DIRECT founding depth×spin route (an ω≠0 internal rotation sourcing φ and
reshaping the core depth) is NOT natively available — reaching it requires the forbidden GR minimal-coupling
import. This is a statement about the CURRENT native action + no-import rule, NOT a theorem foreclosing a
future native matter frame Charles may adopt. The as-derived matter coupling is the channel-corrected ḡ
(φ-blind); B ("matter gradients contract with the physical metric") = GR minimal coupling.

**Provenance:** first P16 note (a648-era, C/lean-A) → deeper contract-driven derivation (a8a9046a1d2e2c2c2,
argued B) → HARD blind adversarial verifier (afdcd31f357869084, REFUTED B on three textual hinges; reversal
engine contradicted by the banked gp_switch "only 𝒦 breaks the shift"). Docs:
`p16_phi_sourcing_decision_note.md` (top banner), `p16_native_derivation_contract.md` (frozen contract).
**Canonized (conservatively) by Charles 2026-07-05.**

## C-2026-07-09-1 — WR-L: residual form \(A=1-r/X\) selected by wall regularity

**Statement:** On the simple reciprocal metric (\(ds^2=-e^{-2\phi}c^2dt^2+e^{2\phi}dr^2+r^2d\Omega^2\), \(A=e^{-2\phi}\)), residual composition (\(A_{12}=A_1A_2\)) together with affine seat re-centering (no residual throne: remaining areal room subtracts as \(r'=r-r_0\), \(X'=X-r_0\)) forces the one-parameter family
\[
A=\Bigl(1-\frac{r}{X}\Bigr)^{\alpha}.
\]
The wall-regular residual selector package **WR-L** — Charles-accepted axioms —
1. residual composition / re-centering (above),
2. finite proper room \(\ell=\int dr/\sqrt{A}<\infty\),
3. infinite optical reach \(\ell_{\mathrm{opt}}=\int dr/A=\infty\),
4. no curvature/shell singularity at the wall (\(G^\theta{}_\theta=\tfrac12 A''+A'/r\) finite as \(r\to X\)) —

selects uniquely \(\alpha=1\). Therefore
\[
\boxed{A=1-\frac{r}{X}\qquad\Leftrightarrow\qquad\frac{r}{X}=1-A.}
\]
This is the residual embedding **L**.

**Forces:**
- L is **DERIVED** under simple metric + residual re-centering + WR-L wall axioms — not SNe-selected, not free chart shopping, not a stress-ratio slogan as primary.
- Inside the re-centering family, \(S_r=S_A\) (areal room survival equals metric residual) is a **theorem** at \(\alpha=1\), not a taste.
- On L, the faces \(p_t=-\rho/2\) (Einstein readout) and \(\mathrm{d}r/A=2X\,d\phi\) (P-opt with \(\kappa=2X\)) are **consequences / dual confirmations**, not independent hinges that float the form.
- Bare R1–R3 / residual composition alone do **not** force L (the family is forced first; wall regularity picks the point). Do not write “forced by the metric alone.”

**Scope / what it does not force:**
- Absolute scale \(X\) / one ruler remains free until fixed by observation or a further relation.
- Center regularity (\(\rho\sim 1/r\) continuum face on L) is separate from **wall** regularity — not settled by this entry.
- Local-mass rooms, time-live residual dynamics, and microphysics are outside this macro residual-form selection.
- Free \(D_A\) remains quarantined; this entry is simple-metric only.

**Provenance:** Charles sharper derivation (affine re-centering + wall package, 2026-07-09); CAS/numeric verification `simple_metric_L_wall_regularity_closure_out.json`; full record `simple_metric_L_wall_regularity_closure_results.md`; status reconcile `simple_metric_L_equivalence_principle_GAP.md`. Bare NPC attack (FAIL without wall package): `simple_metric_L_principle_closure_attack_results.md`. Charles: accepts the three wall conditions (“I have no problem with those conditions”); ledger entry authorized this session.
**Canonized by Charles 2026-07-09.**

## C-2026-07-09-1a — WR-L audit precision (append to C-2026-07-09-1; not an overturn)

**External triple-blind consolidated audit (2026-07-09; banked `simple_metric_WR_L_external_triple_blind_audit_results.md`):**
core derivation CONFIRMED sound and honestly scoped.

**Precision upgrades (binding wording):**

1. **α=1 vs α=2 fork (own consciously).** Curvature finiteness alone admits \(\alpha=2\) as well as \(\alpha=1\). Only the accepted **finite proper room** axiom kills \(\alpha=2\) (log-divergent proper distance). \(\alpha=1\) = finite proper + infinite optical = **causal ceiling**. \(\alpha=2\) = infinite proper = unreachable spatial infinity.

2. **Horizon, not hard edge of space.** The \(\alpha=1\) wall is a causal / Schwarzschild-type horizon at finite proper distance: infinite optical reach, \(z\to\infty\), with a **trapped interior beyond** \(r=X\) (signature flip). Wording: “ends at \(x_{\max}\)” means **causal horizon at finite proper distance with interior beyond**, not a wall of space.

3. **Mass lock not part of this canon entry.** \(r_{\max}=2GM/c^2\) / MS cascade remains **Principle-7 flagged** (GR-form / definitional under MS packaging) — see audit record; not elevated by WR-L.

4. **P_ell not part of this canon.** Explicitly **retired** as imposition / SNe detour (audit V2).

**Provenance:** Charles-relayed V1/V2/V3 consolidated verdict; in-repo CAS prior. Local blind agent IDs not supplied — do not invent.
**Accepted into ledger by Charles 2026-07-09 (audit bank).**

## C-2026-07-09-1b — WR-L scope: wall selector, silent at center (append; not overturn)

**Statement (scope precision, 2026-07-09):** Package WR-L / C-2026-07-09-1 selects the residual **wall** form \(A=1-r/X\). Its axioms do **not** constrain the exact interior to \(r=0\). Extending \(A=1-r/X\) all the way to the seat is a **CHOSE extrapolation**. Under that extrapolation, the center is a true weak curvature singularity (\(R=6/(Xr)\), \(K=8/(X^2r^2)\); generic in the power family \((1-r/X)^\alpha\)) — not a coordinate artifact. Regularization requires metric content beyond wall-only WR-L (non-round / time-live / residual atlas). \(\rho\sim 1/r\) is not a derived particle core.

**Provenance:** `simple_metric_WR_L_center_nogo_atlas_results.md`, `simple_metric_WR_L_center_invariants_second_pass_results.md` (two external passes + local CAS).
**Banked as scope precision of C-2026-07-09-1 (2026-07-09).** Full Charles-canon confirmation optional — math/results carry the claim.

## C-2026-07-09-1c — Residual re-centering ⊥ center regularity (append; fork open)

**Statement (2026-07-09):** On the simple reciprocal metric, center regularity requires \(A'(0)=0\) (i.e. \(A=1+O(r^2)\)). The residual re-centering family \(A=(1-r/X)^\alpha\) has \(A'(0)=-\alpha/X\neq 0\) for every \(\alpha>0\). Therefore **exact global residual re-centering and center regularity are mutually exclusive.** The center curvature singularity under global L is the structural price of re-centering, not an optional inward paint.

**Fork (not settled by this entry):**
- **(A)** re-centering exact globally → center is a genuine reachable singularity (no literal vacuum seat at \(r=0\)).
- **(B)** re-centering wall-asymptotic only → regular quadratic core allowed; WR-L is exterior/wall form only.

**Provenance:** `simple_metric_WR_L_center_recenter_exclusion_results.md` (external third pass + local CAS). Revises the “CHOSE extrapolation only” emphasis of C-2026-07-09-1b when re-centering is taken as global.
**Banked as derived exclusion + open fork (2026-07-09).** Charles picks (A) or (B).

## C-2026-07-09-2 — Seat singularity under residual re-centering (Charles ruling A) + dS continuum lean

**Statement (Charles, 2026-07-09):**

1. **Residual re-centering is exact** for the residual L chart (Choice 1 = fork **A**). The seat \(r=0\) is the chart’s \(\phi=0\) point. Charles accepts a curvature singularity / continuum breakdown there as consistent with \(\phi=0\) as a **regime boundary** between macro residual description and micro/particle sector — not as a demand for a smooth vacuum core on the same L line. Fork **B** (smooth L core / wall-only re-centering) is **not** adopted.

2. **Regular continuum window (working lean):** Charles accepts the external EOS-window suggestion as working guidance: under reciprocal Einstein + CHOSE \(p_t=w\rho\) + DEC, the only wall+center-regular point is \(w=-1\) (static de Sitter face \(A=1-r^2/X^2\), \(\rho=3/(8\pi X^2)\), \(\Lambda=3/X^2\) if so identified). L remains the residual/singular relative chart, **not** demoted as residual law and **not** identified with dS.

**Forces:** do not “fix” L’s seat with a quadratic vacuum patch on the L line; do not claim dS is forced by residual re-centering alone; keep residual L and continuum dS as dual layers until a native glue is derived.

**Scope:** Working charter / lean — \(\Lambda\) is **not** full UDT theorem from first principles; EOS+DEC remain CHOSE for the window scan. Provenance: `simple_metric_Charles_rulings_center_dS_2026-07-09.md`, center exclusion + EOS window results.
**Ruled by Charles 2026-07-09.**

