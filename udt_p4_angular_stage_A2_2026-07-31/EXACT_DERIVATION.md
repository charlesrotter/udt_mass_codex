# Stage A2 — exact derivation record: the pointwise reduction ANGULAR-LIVE (TP2-1..TP2-4)

Date: 2026-07-31. Branch: grok. Contract: `PREREGISTRATION.md` (frozen first). Named checks in
`monospace` are exact zero-residual SymPy checks in `derive_angular_A2.py` (no floats, no numeric
solvers, deterministic; guard checks wired into the exit path). **Ceiling honored throughout:** no
response law selected, no fork decided (neither the lock-reading nor the NEW spatial-reading fork),
nothing solved, NO angular cycle census (Stage A3's contract; F-P1), no spectrum, no physics.

**Stamps carried by every statement:** T² stratum layer (A-L1 CHOSE; full-S³ TYPED);
EVERYTHING-ON within the cleared layers (φ, f, bh, the shift row N AND the angular mixed row m
all live in (t,x,y,z)); tri-graded jets ≤ 2 per direction (A-L2, higher TYPED); time-live-LINE
(A-L4); θ ABSENT (A-L5); N=2 wall layer; registered stationary presentation (general arenas
TYPED); polynomial/formal in the (k10, C) moduli; pointwise, one-parameter, off-shell on the
Route B / Stage-1 / T1 / T2 / A1 footing; BOTH lock-reading branches AND BOTH spatial-reading
branches carried to the SAME depth (F-P1 abbreviation clause honored); mode decomposition =
Category-A technique with the mode layer's bound stated wherever used; resonance-locus contacts
stamped OPEN-PENDING-CENSUS, never adjudicated. NO ADM/foliation and NO Kaluza-Klein/fiber-adapted
object appears anywhere: every derivation runs on covariant metric rows (canon C-2026-06-18-1) and
chart maps, exactly as T1/T2/A1.

---

## TP2-1 — the equivariance/character layer applied (the A1 tower on response components)

### 1.1 The φ-forcing, re-derived angular-live and PER T² MODE — VERDICT: INTACT, MODE-UNIFORM

The foundation leg (static: shift-equivariance ALONE forces Q = c_E·e^{−φ}; T2: intact
time-live) is re-derived with the angles on, per mode:

1. **The forcing condition is unchanged and the mode index is a spectator.** The anchor shift
   acts as (φ, c_E) → (φ+s, c_E·e^s) pointwise in (t,x,y,z) with s CONSTANT. c_E^p·e^{−q·φ} is
   orbit-invariant iff p = q — and attaching ANY T² mode phase e_n = e^{2πiny/P} leaves the
   residual law e^{(p−q)s} unchanged (`P1a`): the condition is IDENTICAL at every mode n. A
   mode-dependent exponent pair (p(n), q(n)) is forced to p(n) = q(n) for EVERY n by the same
   one-line condition: **the φ-forcing is MODE-UNIFORM.** Bare φ stays excluded.
2. **Angular modes open NO new φ-channel and close none.** Every tri-graded angular jet of φ is
   shift-invariant (`P1b`), and every new angular-live block (the m row, N, f, bh, moduli, any
   angular jet, any mode phase) is shift-INERT, so no product can compensate a p ≠ q mismatch
   (`P1c`): the unique φ-channel angular-live is STILL the anchored readout Q = c_E·e^{−φ}.
3. **The anchor-overlap fate of the angular jet legs** (`P1d`): across anchor presentations (the
   A1r absorption map — t, y untouched; x → e^{λs}x, z → e^{s}z): the y-leg jets are
   overlap-INVARIANT OUTRIGHT (the compact y-leg absorbs purely on the field side — a derived
   CONTRAST with the t- and z-legs); the z-leg jet carries the exact overlap factor
   ∂_z̃φ̃ = e^{s}∂_zφ with anchored combination (∂_zφ)/c_E overlap-invariant (the fiber-leg
   analog of TU1d's c_E·∂_tφ); the fiber-leg period rescales as a J07 overlap datum (banked A1r),
   so the z-mode lattice is presentation-stable while its period label is overlap data.

### 1.2 What the slack cocycles FORCE: the full invariant derivative (unifying TU1f and A4a)

- **THE derived operator** (`P1f`): D_x = ∂_x − vᵀG₃⁻¹∂_{(t,y,z)} — the g-orthogonal-to-
  {∂_t,∂_y,∂_z} projection of ∂_x, with v = (N_x, m_y, m_z) and G₃ = the (t,y,z) block including
  the angular shift components N_y, N_z; a native covariant-row object, no foliation used — is
  EXACTLY invariant under EVERY joint (ψ,χ,ζ)(x) slack map (field-level, arbitrary slack
  functions), and γ_xx^full = g_xx − vᵀG₃⁻¹v = 1/g^{xx} (the FULL projected spatial reading,
  A1q's discriminator functional) is invariant identically. T2's D_x = ∂_x − (N/g_tt)∂_t (TU1f)
  and A1's ∂_x − (g_xy/g_yy)∂_y (A4a) are the t-only and y-only SLICES of this one operator.
  Operator-level invariance ⇒ all D_x-jet orders transport invariantly (induction on the derived
  lemma; Category-A argument; first jet derived exactly).
- **The fiber-corrected angular derivative** (`P1g`): D_y = ∂_y − (g_yz/g_zz)∂_z is EXACTLY
  invariant under every ζ(y) fiber-translation slack (the angular-INTERNAL corrected operator);
  under the y-reparametrization slack y → h(y) it transforms by the exact CHAIN-RULE cocycle
  (D_y ↦ h′·D_y) — the h-layer's J07 overlap law acting on the operator exactly as A1p2 derived
  for the fields (overlap data, not an invariance).
- **Triangular invertibility** (`P1h`): (∂_x, ∂_t, ∂_y, ∂_z) → (D_x, ∂_t, ∂_y, ∂_z) is
  unit-determinant triangular; g_xx = γ_xx^full + vᵀG₃⁻¹v inverts the row map: coordinate and
  invariant presentations are two coordinates on the SAME tri-graded alphabet; no pointwise
  content rides the choice on-chart; across charts only the invariant presentation transports
  trivially (the frame presentation carries the additive slack cocycles, banked A1k/A1s4/T2i).
- **The mode grading is SLACK-STABLE** (`P1e`): under y → y + χ(x) the mode function e_n maps to
  a pointwise phase multiple e^{2πinχ(x)/P}·e_n — every mode subspace is preserved by every
  residual slack map; the T²-translation layer commutes with the slack layers. The mode index
  remains DUAL/decomposition data of a function (Category-A);
  its field-cycle content is Stage A3's contract (scope-exclusion, F-P1).

### 1.3 The NEW conditional character layer: the ℤ₂×ℤ₂ angular-mirror parity grading

`P1i`: the composed-mirror parity of a jet block is (−1)^{angular-jet order in the mirrored
direction} × (the field's composed parity) — the derived A1f/A1e2 parity assignments (y-mirror:
f, N_y, m_y, g_yz ODD; z-mirror: α, f, N_z, m_z, g_yz ODD; φ, bh, moduli EVEN) grade the WHOLE
tri-graded alphabet by a ℤ₂×ℤ₂ character. **Layer stamp (conditional — the T2 T-parity
discipline transposed):** imposed as a character rule at the METRIC layer only, and only WHERE
THE MIRROR IS GRANTED — the mirrors are BRIDGE FLOOR only (G18: no closure status; a spatial
reflection is orientation-reversing, so their coframe-layer status inherits T1's SO⁺
obstruction; admitting it there = CHOSE). The mirrors negate modes (A3e), so the granted cut
PAIRS the +n and −n mode sectors rather than acting mode-diagonally. Its reach into the banked
strata is TP2-3's finding (P3b).

### 1.4 The bare-angle exclusions' response-side fate

`P1j` (guard, banked A1n re-run): a component built with BARE y/z is not defined on the residual
T²-translation quotient and is not a function on the periodic domain — response components are
built from the tri-graded jet alphabet only; θ ABSENT; fitted angular averages stay excluded
(R13), with the banked distinction that a mode PROJECTION is Category-A analysis, not a fitted
average.

**TP2-1 verdict:** the φ-forcing is INTACT and MODE-UNIFORM (per-mode answer: the SAME forcing at
every mode; no new φ-channel); the slack cocycles force the invariant/frame alphabet split with
the FULL derived D_x and the fiber-corrected D_y; the new angular character content is (i) the
slack-stable mode grading (Category-A organizing layer) and (ii) the CONDITIONAL ℤ₂×ℤ₂
angular-mirror parity layer (granted-only, bridge floor); bare angles are excluded response-side.

---

## TP2-2 — the pointwise reduction, per SPATIAL-reading branch (same depth; lock fork carried)

### 2.1 COORDINATE spatial branch: the R_m (and R_N) slots through every re-posed requirement

Verdicts (each derived, not asserted):

- **R1/R2/J12 (census/provenance):** R_m slots censused (O19); one slot per 20-census direction
  (O18 time label and O20 period data are discrete/supplied data, no component slot — O20's
  periods join the J13 discriminator/completion controls); a missing R_m slot = the y-isometry
  era's presentation-freeze made visible (coordinate spatial reading).
- **J04 (shift):** m is shift-inert; anchored (`P1c`). Bare angles excluded (`P1j`).
- **R4/J06 (slots):** the m-sector pairing Gram = I₂ — nondegenerate, NO annihilator, NO
  trace/trace-free split (a vector row, not a symmetric kernel): **NO new forced-slot theorem
  arises in the m-sector, and NO null slot** (`P2a`). The static trace-free slot FORCING has NO
  m-analog and itself transfers untouched (moduli-sector; (t,y,z) spectators, banked A1 A2c).
- **R7(a)/J10 (equivariance):** δ_gauge m = 0 — every metric component including the m row is a
  local-Lorentz invariant (16-entry symbolic coframe, K₄ + generic boost, `P2b`), so R_m's K₄
  character is FORCED trivial (witness k10·m_y breaks equivariance). Parity layers: T-parity
  EVEN (δm carries no t-index); angular-mirror parity y-odd/z-even for R_m_y, y-even/z-odd for
  R_m_z (granted-only layer, `P1i`); m-involution ODD on the χ-branch strata (`P2e`). [AMENDMENT A-2, verifier round 1: the odd/even m-involution labels are exact on g_yz=0 / in the eigenbasis; the general action is flip-and-shear — the B⁻¹-pairing is the invariant object.]
- **R7(b):** δ_gauge m = 0 ⇒ the R_m slots pair NO gauge direction and drop out of every stratum
  Noether identity (TP2-3).
- **R8/R12/R13/J14:** tri-grade declaration typing; off-shell full-domain; pointwise (no fitted
  angular averages; mode projection = Category-A).

**COORDINATE-SPATIAL-BRANCH VERDICT (`P2c`): both R_m slots SURVIVE the full re-posed pointwise
requirement set as physical-content components** (witnesses R_m_y = m_y, R_m_z = m_z pass every
derived gate). Per-witness stratum stamps recur (`P2d`): R_m_y = ∂_yφ is legal at the granted-
mirror layer but m-involution EVEN [A-2: labels exact on g_yz=0 / eigenbasis; general action flip-and-shear; B⁻¹-pairing = the invariant] — a member OFF the χ-branch strata only (the omega-witness /
TU2e discipline, angular recurrence). The χ-branch stratum structure is DERIVED (`P2e`): the
branch slack is an exact INVOLUTION m → (−m_y, m_z − 2g_yz·m_y/g_yy) preserving mᵀB⁻¹m (clean
m_y-flip on g_yz = 0) — a stratum-conditional DISCRETE character cut (coordinate spatial reading);
the full joint conic family is CONTINUOUS with derived invariant mᵀB⁻¹m, its equivariance beyond
the ℤ₂ slice TYPED, its pointwise content = the P2f legs.

The R_N slots' banked T2 verdicts transfer angular-live ((y,z) spectators, `P2k`), with NEW
angular content: R_N_y / R_N_z are y-/z-mirror ODD under the granted layer.

### 2.2 PROJECTED spatial branch: diagonal+slack presentation; the R_m slack-pairing EXACT

The infinitesimal angular-slack laws are DERIVED on the general opened matrix (pullback
linearization = Lie derivative along χ(t,x)∂_y + ζ(t,x)∂_z; ALL ten component laws verified
against the A1g/A1g2/A1s2/A1s3 finite laws), and the pointwise pairing at the diagonal
presentation is EXACTLY (`P2f`):

    <R, delta_slack> = a_y·χ + a_z·ζ + b_x·(χ_x, ζ_x) + b_t·(χ_t, ζ_t) ,
    DRAG LEGS    a_angle = Σ_A R_A·∂_angle A     [moduli drags join on field readings — typed]
    x-SLOPE LEGS b_x = B·(R_m_y, R_m_z) + N_ang·R_N_x
    t-SLOPE LEGS b_t = B·(R_N_y, R_N_z) + N_ang·(e^{2φ}/c_E²)·R_φ ,   N_ang = (N_y, N_z).

**On the projected spatial branch the R_m slots pair PURE CHART-SLACK through the x-slope legs**,
with B nondegenerate (the pairing sees the whole R_m row). **THE SLACK-COUPLED-SECTOR LAW**
(new, derived): the SAME slack map pairs the R_m sector (x-slopes) and the R_N sector (t-slopes)
through the SAME angular block B, coupled by N_ang; on N_ang = 0 the legs separate cleanly. The
Noether-second-theorem divergence identity between drag and slope legs is INTEGRATION-layer —
POSED and TYPED, not imposed pointwise: no pointwise kill of R_m is derivable, none claimed. On
the coordinate spatial branch the same legs are J07 overlap-transport data (no identity owed).

### 2.3 Same depth, both branches — and the two forks' composition

- **The reading-independence theorem's angular analog: DERIVED** (`P2g`): the invertible
  triangular alphabet map (P1f/P1h) preserves EVERY character layer (K₄, T-parity, both
  angular-mirror parities, shift-orbit, mode grading) — ℛ_PW^A has the SAME character-matched
  module parametrization on both spatial-reading branches at the unconditional layers; T2's
  stratum qualifier transposes VERBATIM: the stratum-conditional m-involution cut rides the
  COORDINATE reading (on χ-branch strata the projected branch carries the equivalent content in
  the slack-pairing typing, not as a pointwise cut). A MAP FACT, not a resolution (F-P4).
- **Lock fork × spatial fork composition** (`P2h`, map fact — identity-level, not pointwise [N-2]): the FULL projected reading
  γ_xx^full = g_xx − vᵀG₃⁻¹v equals the sequential single-fork corrections
  g_xx − N_x²/g_tt − mᵀB⁻¹m EXACTLY iff N_y = N_z = 0; off that stratum they differ by an exact
  N_ang-cross term: the two projections are NOT independent when the shift row's angular
  components are on — the joint projected object is the single G₃-projection. Angular content
  stays a SPECTATOR of the lock fork's split term (banked A1b); NOTHING decides either fork.
- **J06 m-family** (`P2i`): DETERMINED (R_m = m) and RETAINED (R_m ≡ 0) branches both nonempty,
  neither chosen; projected branch reads slack-pairing present vs absent.
- **Mode structure** (`P2j`): every derived gate is MODE-BLIND (mechanically scanned) — the
  surviving space is MODE-UNIFORM: the same character-matched module structure per T² mode; the
  mode layer enters only through the alphabet's angular grading (A3c) and the granted-mirror
  ±n pairing (P1i). No per-mode kill exists at this layer.

**Surviving space (the TP2-2 deliverable):**

    R_PW^A = { (R_phi, R_f, R_bh, 2r_tr, 2r_tf, r_sh, M, R_N (3), R_m (2), R_wall, R_corner
               [, R_alpha][, R_cE][, branch-(c) slots TYPED])
        : trivial-K4 entries in A^A (tri-graded mode-uniform alphabet, jets <= 2 per direction);
          r_sh in chi_a-module; M in (chi_b + chi_c)-modules (banked modules, (t,y,z) spectators);
          all components T-parity-matched (metric layer, conditional — banked T2) AND
          angular-mirror-parity-matched (Z2 x Z2, GRANTED-ONLY, pairs +n/-n modes) AND
          N-parity-matched on psi-branch strata (lock-coordinate reading, banked T2) AND
          m-involution-matched on chi-branch strata (spatial-coordinate reading, NEW) [A-2: labels exact on g_yz=0 / eigenbasis; general action flip-and-shear; B⁻¹-pairing = the invariant] }
        CUT BY the stratum Noether identities (TP2-3: k_mod = 0 extended verbatim;
        resonance content OPEN-PENDING-CENSUS) — identical on all four reading branch-pairs at
        the unconditional layers; the R_N / R_m sectors' READINGS (physical vs chart-slack) ride
        the lock / spatial forks respectively, slack-coupled per P2f.

---

## TP2-3 — the banked spaces' fate

### 3.1 ℛ_PW^T EMBEDS EXACTLY as the mode-zero stratum — at the banked layers

`P3a`: every banked T2 block is angular-order-0 (the 9-letter bigraded alphabet IS the k=l=0
stratum of the 54-letter tri-graded alphabet) and m-free; on the mode-zero stratum with m = 0 the
stratum m-involution degenerates to the identity (level set {0}), the mode grading is trivial,
the m-sector slack legs vanish, and δ_gauge m = 0 adds no identity component: every
UNCONDITIONAL angular-live gate restricts to the banked T2 gate identically. **VERDICT: ℛ_PW^T
embeds as the mode-zero stratum of ℛ_PW^A EXACTLY, component-by-component (C-1 checks it
mechanically); NO member lost, NO deformation at the banked layers; the enrichment is purely
TRANSVERSE (the R_m row + angular jets + the mode organization).** Branch stamp: identical on
all four reading branch-pairs (at mode zero + m = 0 the spatial readings coincide identically).

### 3.2 THE NEW FINDING: the granted-mirror layer REACHES the mode-zero stratum

`P3b`: the NEW conditional angular-mirror parity layer does NOT vacate at mode zero — a DERIVED
CONTRAST with T2's T-parity layer (vacuous on the static stratum, TU3a). The mirror layer acts on
FIELD parities (f is odd-COMPOSED, A1f — independent of angular dependence), which the banked
strata already contain: WHERE THE MIRROR LAYER IS GRANTED, the banked member R_f = Q is cut even
at mode zero (mirror-EVEN pairing the mirror-ODD δf), while R_f = f·Q passes. **Precision of the
embedding statement:** the embedding is EXACT at the banked layers (all cuts the T2/static banks
actually carry); the mirror refinement is NEW granted-only conditional content (bridge floor,
G18, no closure status; coframe SO⁺-obstructed — admitting = CHOSE), stamped and NOT imposed
here. NO bank contradiction (F-P5 clean). Whether the mirror layer is ever granted is a
fork-decision seat (decision surface).

### 3.3 The EH-form's angular placement (map fact; F-B1-style observation, nothing selected)

`P3c`: exact 2D witness (diagonal profiles EVEN in y, mixed entry ODD — the derived A1f
parity): the exact Ricci tensor transforms with parity (−1)^{#y-indices} under the composed
angular mirror — Ric_xy ODD (exactly the parity the R_m_y slot requires), Ric_xx/Ric_yy/R
EVEN: curvature-built responses are angular-mirror-parity-matched. Placement: field sector,
trivial K₄ character, tri-grade ≤ 2 (two derivatives by construction; angular jets genuinely
enter), parity-matched at both conditional layers; as a LOCAL functional its mode content is
product/convolution structure — NO mode selection. Per spatial branch: the x-angular row pairs
physical δm (coordinate) vs chart-slack (projected). 4D generality by tensor naturality
(Category-A, cited); Bach-form stays in the typed jet-3/4 class (banked TC2).

### 3.4 The identity strata, angular-live

- **The tangency system is (t,y,z)-spectator, N-blind AND m-blind** (`P3d`): entries involve
  only the seven moduli symbols; generic rank 6 / empty nullspace (R7(b) generically vacuous).
- **The k_mod = 0 identity EXTENDS VERBATIM** (`P3d`): all 36 minors divisible by (k00 − k11);
  nullspace span(L23) on the stratum; the FULL angular-live pairing (screen + mixing + the three
  R_N slots + THE TWO R_m SLOTS + field slots) equals the banked identity exactly — it gains NO
  angular components and does NOT split (δ_gauge N = 0 banked; δ_gauge m = 0 derived P2b; zero
  field sector). **Per-mode fate: ONE pointwise identity, mode-blind in form; its mode
  decomposition is the CONVOLUTION grading of its bilinear terms — it does NOT split into
  mode-diagonal identities and GAINS no mode-indexed family.** Branch stamp: identical on all
  four reading branch-pairs (moduli-sector; N-/m-sector branch differences drop out).
- **k_mod = 0 remains the only CODIMENSION-1 cut** (`P3e`, Gröbner re-run angular-live).
- **The resonance locus: TYPED + OPEN-PENDING-CENSUS** (`P3f`): banked content travels as
  citation; NO angular-live adjudication; per-stratum statements await the queued census.
- **TWO new stratum types, typed and distinguished** (`P3g`): (i) the χ-branch chart-symmetry
  strata — DISCRETE character cut (the m-involution ℤ₂), NO Noether identity (the TU4e analog); [AMENDMENT A-1, verifier round 1: the joint conic also contains a DISCRETE ζ-only slice s=(0, −2m_z/g_zz) acting as the lawful involution m → (m_y − 2g_yz·m_z/g_zz, −m_z), preserving mᵀB⁻¹m — the discrete-slice census is TYPED, not exhausted.]
  (ii) the joint-conic strata — a CONTINUOUS 1-parameter lawful slack family (smooth curve
  through s = 0, implicit-function leg), but CHART-SLACK, not local-Lorentz gauge: NO new
  pointwise Noether identity (δ_gauge = 0 for metric rows); its content is the P2f legs with the
  divergence identity at the INTEGRATION layer (projected readings) / J07 overlap-transport
  (coordinate readings) — disjoint in kind from the moduli degeneration strata.

---

## TP2-4 — controls, coverage, and the honest split

### 4.1 C-1: T2 recovery (the calibration identity) — PASS, F-P7 NOT fired

Parsed MECHANICALLY from the banked T2 package (never hand-copied):

- **Component table** (`C1a`): killing the two R_m slots (the mode-zero + m = 0 restriction)
  recovers the banked 17-row ℛ_PW^T component table EXACTLY, in order,
  character-for-character (T2 ledger parsed mechanically), with the T-parity assignments
  matched row-by-row (T2's odd set = {R_N_x, R_N_y, R_N_z} = mine).
- **Identity + machine stamps** (`C1b`): the banked k_mod = 0 identity string parses to an
  expression equal to my re-derived one EXACTLY; the T2 results JSON parses mechanically
  (39/39 passed; load-bearing stamps TU2d/TU2i/TU3a/TU4b/C1a all passed; outcome OU-1).
- **Alphabet dims** (`C1c`): the angular-order-0 restriction of the 54-letter tri-graded
  alphabet is the 9-letter bigraded T2 alphabet exactly.

### 4.2 C-2: transitive static recovery (spot-scope) — PASS

`C2a` (mechanical vs the banked `routeA_stage2_results.json`): the mode-zero + static
restriction (kill R_N, R_m, branch-(c)) recovers the banked 12-component table exactly, in
order, character-for-character; the banked χ_a/χ_b/χ_c module generator strings parse to
expressions equal to mine exactly; the banked k_mod = 0 AND shear identity strings parse to
expressions equal to my re-derived ones exactly. SPOT-SCOPE stamp: these are the declared spot
legs; the full transitivity chain composes through T2's own banked C-1.

### 4.3 Coverage and the honest substantive/guard split

`R2_J05_component_coverage_angular` (guard): 19 component slots over the 20-object census —
12 banked + 3 R_N + 2 NEW R_m + 2 branch-(c) TYPED; O18 (time label) and O20 (period data) are
discrete/supplied data with NO component slot (the periods join the J13 discriminator/completion
controls); θ ABSENT; F-P1 self-audit mechanical (`G4`).

`derive_angular_A2.py`: **38 checks, 38 passed — 27 SUBSTANTIVE + 11 GUARD**, all wired into
the exit path; exit 0; deterministic (stdout, JSON and ledger byte-identical across re-runs,
verified); runtime < 4 s CPU, single process, exact SymPy throughout (`G3` self-scan; `G4` =
the F-P1 vocabulary scan on the record, ledger and decision surface). Guards enumerated (11):
S0 conventions re-run; P1j bare-angle re-run; P2k R_N transfer re-run; P3e Gröbner re-run; P3f
resonance citation/OPC stamp; C1c dims; R2/J05 coverage; G1 JSON roundtrip; G2 ledger shape;
G3 hygiene; G4 F-P1 scan. Reuse: K₄/generators/X/moduli conventions verbatim from the banked
scripts; the T2 ledger + JSON and the banked Stage-2 JSON are PARSED as control references,
never re-derived.

**Outcome class: OA2-1** — ℛ_PW^A is parametrized cleanly per branch: the SAME character-matched
module space over the tri-graded MODE-UNIFORM alphabet on all four reading branch-pairs
(lock × spatial) at the unconditional layers (reading-independence angular analog DERIVED, P2g),
differing in the R_N / R_m sectors' READINGS (physical vs chart-slack-paired, slack-coupled per
P2f); cut by the banked stratum identities extended verbatim (P3d) plus the conditional parity
layers (T-parity banked; ANGULAR-MIRROR ℤ₂×ℤ₂ granted-only NEW, reaching mode zero — P3b; the
stratum-conditional N-parity banked and m-involution NEW); ℛ_PW^T embeds exactly as the
mode-zero stratum at the banked layers (P3a); both controls pass. **Ceiling honored:** no
response law, no fork decided, no solve, NO angular cycle census (Stage A3; F-P1), no spectrum,
no physics.
