# Stage A1 — exact derivation record: the variation domain re-posed ANGULAR-LIVE (TA-1..TA-5)

Date: 2026-07-31. Branch: grok. Contract: `PREREGISTRATION.md` (frozen first). Named checks in
`monospace` are exact zero-residual SymPy checks in `derive_angular_A1.py` (no floats, no numeric
solvers, deterministic; guard checks wired into the exit path). **Ceiling honored throughout:** no
response law selected, nothing solved, NO angular cycle census (Stage A3's contract; F-A1), no
fork/posture/topology decided, no physics.

> **AMENDMENT 2026-07-31, verifier round 1 (PASS-WITH-REQUIRED-AMENDMENTS implemented; no leg
> refuted; OA1-1 survives).** AM-A: the residual slack census was INCOMPLETE — the fiber-translation
> (ζ) layer z → z + ζ is a lawful residual layer the original census missed (`A1s`–`A1s5`; the
> §1.2.6 residual-group statement is RESTATED). AM-B: under the coordinate pin the JOINT (χ′,ζ′)
> slack orbit of m is the LEVEL SET of mᵀB⁻¹m, not {m,−m} (`A1i2`/`A1j3`; irreducibility survives
> as NON-REMOVABILITY; fork framing unchanged). AM-C: the C-3 sweep vocabulary was widened
> (10 → 17 flagged anchors). Plus two clarify-notes (A1q branch-scope; A2b honest split). Check
> count 40 → 47 (38 SUBSTANTIVE + 9 GUARD). Details: `CORRECTION_LAYER.md`.

**Stamps carried by every statement:** T² stratum layer (A-L1 CHOSE, stamp travels; full-S³ = the
typed next layer); EVERYTHING-ON within the cleared layer (φ, f, bh, N AND the new angular mixed
row m all live in (x,t,y,z)); time-live-LINE composition (A-L4 owner ruling); angular jets ≤ 2
(A-L2 layer, higher TYPED); θ ABSENT (A-L5); N=2 wall layer; both lock-reading branches carried
(T1/T2) + the NEW spatial-reading fork carried (neither decided); both moduli census readings; all
pointwise statements off-shell on the Route B / Stage-1 / T1 / T2 footing. NO Kaluza-Klein /
fiber-adapted parametrization appears anywhere (F-A2): every derivation runs on covariant metric
rows (canon C-2026-06-18-1) and chart maps, exactly as T1 — `A1q` is the discriminator certificate.

---

## TA-1 — the angular-live variation domain, exact

### 1.1 The metric block OPENED natively (which components may depend on y; what is forced)

The registered chart (Route C TC1, the banked working chart of the R×T² stratum) is
g = −u(c_E dt + αA)² + u⁻¹A² + q_B with A = dz + f dy, q_B = e^{2λφ}(dx² + bh dy²), u = e^{−2φ}
— its one-parameter presentation (fields of x only, later (x,t)) was a CHOSE, here unfrozen.
With every field a function of (t,x,y,z), the DERIVED opening verdict, component by component:

1. **The clock row opens THROUGH φ ONLY.** g_tt = −e^{−2φ}c² is form-FORCED (canon); with
   φ = φ(t,x,y,z) the stationary-observer rate is dτ/dt = e^{−φ} exactly — neither the shift row
   N_i nor the new angular mixed rows m_a enter (`A1a`). φ's angular dependence itself is FREE BY
   CANON: C-2026-06-18-1 states SPHERICAL is an independent CHOICE, not a consequence — the
   angular opening of φ is canon-legal, not an extension of canon.
2. **The locked leg carries NO independent angular freedom.** On the registered family with the
   twist on and ALL fields angular-live, the projected (radar) reading of the reciprocal lock is
   EXACT: g_tt·γ_zz = −c_E² identically, γ_zz = e^{2φ} (`A1b`, `A1c`); the coordinate reading
   splits by exactly the t-angular mixing term −c_E²α²e^{−4φ} — the T1k fork structure verbatim.
   The identity is pointwise-algebraic: **angular dependence is a SPECTATOR of the lock-reading
   fork** (nothing angular decides it; it travels undecided, F-A4 honored). The locked-leg norm's
   angular dependence enters only through φ's.
3. **The x-angular mixed row (m_y = g_xy, m_z = g_xz) is PERMITTED, NOT FORCED, NOT EXCLUDED —
   and the stratum without it is not chart-invariant.** Canon lists ALL off-diagonal terms FREE
   (the same clause that admitted T1's shift row). BOTH components are now DERIVED slack-generated
   (AMENDMENT AM-A): the chart map y → y + χ(x) GENERATES g_xy = g_yy·χ′ from the diagonal-in-x
   stratum (`A1g`, the exact angular analog of T1o) and z → z + ζ(x) GENERATES g_xz = g_zz·ζ′
   (`A1s2` — pre-amendment the m_z structure was stated by analogy only) — so EXCLUDING the row
   would re-freeze the y-isometry (F-A4). The row enters the variation domain as a VARIED FIELD
   (everything-on), in NATIVE covariant-row form: `A1q` certifies
   1/g^{xx} = g_xx − g_xy²/g_yy ≠ g_xx — pinning the registered covariant row is NOT a
   fiber-adapted (Kaluza-Klein-type) pin; the difference g_xy²/g_yy is the F-A2 discriminator
   (the exact angular analog of T1j's anti-ADM certificate). BRANCH-SCOPE (verifier note 1):
   1/g^{xx} = γ_xx IS the projected spatial reading — the fork's projected branch pins exactly
   this derived functional; the F-A2 hazard attaches to IMPORTING A PARAMETRIZATION, never to a
   derived reading functional, so "this package pins the covariant row" is scoped to the
   coordinate-reading branch.
4. **The remaining components:** g_ty, g_tz = the T1 shift row, now angular-live; g_yy, g_yz =
   the angular block, carried by (bh, f) now angular-live; g_xx = the registered transverse
   gauge pin (Category-A; the x-reparametrization is spent on it — and the pin's READING is now
   a derived fork, §1.2 leg 3). Accounting: of the 10 covariant components, the clock row is
   canon-forced (through φ), the locked leg is lock-forced (through φ [+ twist reading]), g_xx
   is gauge-pinned; the other 7 are varied fields — 3 shift (T1) + 2 angular mixed (NEW) + 2
   angular block (banked fields, opened). **Nothing is excluded; nothing new is forced.**

### 1.2 The residual chart symmetry and the slack layers (the angular-translation fate)

1. **Constant T² translations SURVIVE as a residual symmetry layer** (`A1d`): (y,z) → (y+a,z+b)
   maps the registered form to itself with argument-relabeled fields — the exact angular analog
   of t → t + t₀. Period-compatibility is the only constraint (a domain fact, §TA-2).
2. **The fiber-leg reparametrization is RIGIDIFIED BY THE LOCK — within the z-only map class**
   (`A1e`, scope AMENDED per AM-A): z → k(z) rescales γ_zz by k′²; preserving the projected lock
   reading (clock row pinned by canon, t untouched) forces k′² = 1 — **the reciprocal lock
   rigidifies BOTH its legs** (t: banked T1a; the fiber leg: derived here;
   verifier-confirmed V1a). No free angular lapse exists on the locked leg; residual fiber maps
   IN THE z-ONLY CLASS z → k(z) are z → ±z + const. The y/t-dependent fiber TRANSLATIONS
   z → z + ζ are a SEPARATE lawful residual layer (leg 3b below) the original statement did not
   cover. (Second leg of the same rigidity: the unit-dz normalization of A.)
3. **The angular legs carry THREE derived slack structures (RESTATED — AMENDMENT AM-A/AM-B):**
   - **The χ-slack** (y → y + χ(x)): under the registered COORDINATE-reading spatial pin (g_xx),
     preservation within the χ-only class gives χ′ ∈ {0, −2g_xy/g_yy} — TWO branches (`A1h`,
     exhaustive within its stated class, verifier V1d), the second flipping m → −m with g_xx,
     g_yy preserved (`A1i`): a stratum-conditional ℤ₂ χ-branch. **AM-B restate:** {m, −m} is
     only the y-leg SLICE — under the JOINT (χ′, ζ′) slack the lawful branch set is a CONIC
     (constraint 2m·s + sᵀBs = 0) and the orbit of m = (g_xy, g_xz) is the LEVEL SET of
     mᵀB⁻¹m, exactly invariant (`A1i2`; witness (1,0) → (0,1)). IRREDUCIBILITY SURVIVES AS
     NON-REMOVABILITY: B pos-def keeps mᵀB⁻¹m ≠ 0 — the invariant mᵀB⁻¹m is the irreducible
     datum. Under a PROJECTED-reading spatial registration (pin γ_xx = g_xx − mᵀB⁻¹m, invariant
     under EVERY joint slack — `A1j`/`A1j3`), s = −B⁻¹m lawfully REMOVES the whole mixed row
     (`A1j2`/`A1j3`). **This is a NEW LOAD-BEARING SPATIAL-READING FORK** — the exact
     spatial-block analog of T1's lock-reading fork (T1p2/p3/p4 transposed): coordinate reading
     ⇒ non-removable m-DOF (invariant datum); projected reading ⇒ m is pure chart-slack.
     Decided by NOTHING in this package; both branches travel with full stamps (F-A4 honored;
     the fork itself is verifier-CONFIRMED both ways).
   - **The ζ-slack (fiber translations z → z + ζ) — the layer the original census MISSED
     (AM-A, the T1-AM-1 error class transposed):** z → z + ζ(y) maps the registered family TO
     ITSELF with f̃ = f + ζ′, all other fields argument-relabeled (`A1s`) — a lawful residual
     map (period-compatible ζ); ζ(x) GENERATES the m_z mixed row from the diagonal stratum
     (`A1s2` — O19's m_z leg upgraded from analogy to DERIVED); ζ(t) MOVES the shift row's
     z-component, N_z′ = N_z + g_zz·ζ_t (`A1s3`, the fiber-leg A1g2 analog). The layer's
     composition is DERIVED, not asserted: additive abelian within itself (`A1s4`, a J07
     overlap law), and SEMIDIRECT under χ and ψ, which act on ζ's y/t-arguments while ζ acts
     on no other layer (`A1s5`).
   - **The y-reparametrization slack** (y → h(y)): absorbed ENTIRELY into the fields
     (f̃ = f·h′, b̃h = bh·h′² — `A1p`): the y-direction's reparametrization freedom is UNSPENT
     by any registered pin (x-gauge spent on g_xx; z rigidified by the lock); the field-fixing
     residual is h′ = 1 (translations) + the mirror; general period-compatible h is a J07-type
     overlap datum with the exact CHAIN-RULE cocycle law (`A1p2`).
4. **The slack layers COMPOSE SEMIDIRECTLY, not as a direct product** (`A1k`, `A1l`, `A1g2`;
   ζ-legs `A1s4`/`A1s5`, AM-A): χ-maps compose additively, and so do ζ-maps (abelian J07
   cocycles, the T2i analog; loop content trivial by additivity — deeper loop structure is
   Stage A3's contract, F-A1); but the t-dependent χ-slack MOVES THE T1 SHIFT ROW
   (N_y′ = N_y + g_yy·χ_t — `A1g2`) and the t-dependent ζ-slack moves N_z (`A1s3`): the ψ-, χ-
   and ζ-sectors are slack-coupled, not disjoint. ψ∘χ vs χ∘ψ differ by χ(x,t+ψ)−χ(x,t) (`A1l`);
   χ/ψ act on ζ's arguments the same way (`A1s5`). The layered slack group CONTAINS the SEMIDIRECT
   TOWER (ζ normal under χ normal under ψ); the y-reparametrization layer h joins ABOVE the
   tower, NOT as a direct factor **[AMENDMENT AM-D, verifier closure 2026-07-31]**: h
   normalizes the ζ-layer by argument action (conjugate = ζ∘h) but does NOT normalize the
   χ-layer for general h (witness h = e^y); only the field-fixing subclass h′ = 1 commutes
   in as a direct factor (still acting on ζ's argument). The full slack group = the group
   GENERATED by {ψ, χ, ζ, h} under these derived relations.
5. **The angular mirrors, DERIVED with parity assignments** (bridge floor only — G18: no closure
   status inherited): y → −y forces f ODD-composed, (φ, α, bh) EVEN (`A1f`; on the opened matrix
   it flips exactly the y-row mixed components N_y, m_y, g_yz); z → −z forces α AND f ODD-composed
   (`A1e2`). Their coframe-layer status inherits T1's SO⁺ question (TYPED, not resolved).
6. **K₄ SURVIVES VERBATIM; (t,y,z) are ALL spectators** (`A1m`): the K₄ action is
   pointwise-algebraic — with every generator entry an arbitrary function of (t,x,y,z), the
   banked characters hold unchanged (λ, k_mod invariant; k10 χ_a; C signed flips). K₄ (frame
   layer) commutes with every coordinate-layer map. **RESTATED (AMENDMENT AM-A — the original
   "=" was refuted as too small; the group is LARGER): residual symmetry of the registered
   angular-live chart = K₄ × T₁ × [T² translations + derived mirrors] ⋉ the ENLARGED slack
   layers {ψ, χ, ζ, y-reparam}** — the ζ fiber-translation layer (leg 3b) joins χ and ψ,
   composing as the semidirect tower of leg 4 (with the reading-fork-conditional structure of
   leg 3).

### 1.3 The tri-graded jet structure and the alphabet gates

- **Bare angles are EXCLUDED from the alphabet, twice over** (`A1n`): (i) bare y shifts under
  the residual T² translations (not defined on the quotient — the exact analog of the banked
  bare-t exclusion TU1e); (ii) bare y is not even a FUNCTION on the periodic domain. Angular
  JETS are translation-covariant, single-valued, and anchor-shift-invariant: admitted.
- **The tri-graded alphabet** (`A1o`): jet letters ∂_t^i ∂_x^j ∂_y^k ∂_z^l (field) with
  i ≤ 2, j ≤ 2, k+l ≤ 2 — 54 letters per varied field; the angular-order-0 restriction is
  exactly the 9-letter bigraded T1/T2 alphabet. The tri-grade bound is a Category-A LAYER
  (A-L2); higher angular jets TYPED, never frozen.
- **The anchor shift extends angular-live** (`A1r`): φ → φ+s absorbed exactly by
  (c_E, α, f, bh) → (c_E e^s, e^{2s}α, e^{−s}f, e^{−2λs}bh) with unit rescale
  (x,z) → (e^{λs}x, e^s z), t and y UNTOUCHED: the compact y-leg absorbs purely on the FIELD
  side (no period rescale needed); the fiber-leg period rescales as an OVERLAP datum between
  presentations (T1q's reading). Shift-equivariance (F-RA4) extends with Q = c_E e^{−φ} invariant.

### 1.4 The census rebuilt (20 objects; full table = `ANGULAR_A1_LEDGER.tsv` rows O01–O20)

The 18 T1 objects each acquire an angular-dependence status (DERIVED-or-CHOSE-tagged in the
ledger), plus exactly TWO new census rows, both provenance-chained: **O19 angular_mixed_row_m**
(g_xy, g_xz; native covariant row; BOTH components slack-generated by derivation — m_y by χ
`A1g`, m_z by ζ `A1s2` (AM-A); irreducibility rides the NEW spatial-reading fork with the
invariant mᵀB⁻¹m as the irreducible datum, AM-B) and
**O20 angular_domain_structure** (the registered T² period data; fields P-periodic as a DERIVED
domain fact; no fork opened — the arena is banked; no cycle-census content rides the row, A3/F-A1).
Moduli rows gain a four-way angular-reading sub-fork (constant / m(t) / m(x,t) / m(x,t,y,z)),
typed, none chosen. Wall/corner/completion rows: §TA-2.

---

## TA-2 — the requirement set re-posed (R1–R15; verdicts in `ANGULAR_A1_LEDGER.tsv` rows R01–R15, J01–J15)

**The derived PERIODICITY requirement (the TA-2 headline, a domain fact not an imposition):** the
registered stratum's domain is R_x × T² (× R_t). A field is BY DEFINITION a function on the domain,
hence P-periodic in (y,z) (`A2a`) — derived from the banked toric arena registration (routeC :29,
the S³ descent), with the periods = registered data (census row O20). Interaction with the anchored
alphabet: periodicity constrains the CONFIGURATION space; it adds NO alphabet letters and removes
none (the shift/anchor rules are pointwise and periodicity-blind); bare angles were already excluded
(`A1n`). Everything beyond function-decomposition legality — any cycle content — is Stage A3's
contract (F-A1 honored: this section states only where fields LIVE, not what they wrap).

**Headline structure (verdict vocabulary as T1):**

- **Transfers-unchanged (4): R1, R4, R10, R14.** R4's exact conditions are pointwise-algebraic
  with (t,y,z) ALL spectators (`A2c` re-run); R1's index set extends to the 20-object census.
- **Extends-with-derived-modification (8): R2, R3, R5, R8, R9, R12, R13, R15.** R2: the component
  list is indexed by the 20-row census — a missing R_m component = a silent freeze (the y-isometry
  era's presentation-freeze made visible), with the R_m slots' reading riding the NEW
  spatial-reading fork (`A1j2`/`A1j3`). R3: DERIVED SIMPLIFICATION — the angular directions need
  NO completion data (T² closed, `A2b`); the completion census stays the banked spatial 12 FC
  families + the T1 time label. R5: one solution = one angular-live solution; the compact T²
  factor gives canonical angular integrals; the T1 slice-vs-history sub-fork travels; NO new
  fork. R8: the pairing's ANGULAR domain datum is FORCED-CANONICAL (compact T², exact
  orthogonality `A3a`) — in derived CONTRAST with the branch-dependent time-domain datum; the
  test runs on tri-graded jets. R9: the domain's cycle set gains angular content — SCOPE-EXCLUSION:
  that census is Stage A3's contract, NOT run (F-A1). R12: the T1 bank is re-read as a pullback of
  the angular-live object to the y-independent stratum (the static bank = the double pullback,
  C-2). R13: fitted ANGULAR averages join the excluded class — with the honest distinction that a
  mode PROJECTION (`A3a`) is analysis technique, not a fitted average. R15: an angular
  topology/completion/period label alone must not convert into a source term absent field support.
- **Gains-angular-component (3): R6, R7, R11(J07).** R6: walls stay TIMELIKE x-loci
  {x_w} × R_t × T² (`A2b`: induced (t,y,z)-block det = −c_E²·bh·e^{2λφ} < 0) with ANGULAR-VARYING
  germ/trace data TYPED at the N=2 wall layer; the ANGULAR MIRRORS are derived with parity
  assignments (`A1e2`/`A1f`) as BRIDGE floor only (G18: no closure status; coframe-layer status
  inherits T1's SO⁺ question, typed); HONEST SPLIT (AMENDMENT NOTE-2): T²-closedness DERIVES the
  absence of angular BOUNDARY/completion strata and corner types (`A2b`); the absence of interior
  angular JUNCTION loci is an INHERITED-PREMISE (the banked wall census: walls = x-loci, CANON),
  folded under a derived label pre-amendment, now split. R7: conservation statements gain angular
  flux components (posed, not solved; WS); the
  compact angular domain closes angular-flux integrals without boundary terms (integration-layer
  typing). R11/J07 (RESTATED, AM-A): THREE new derived overlap laws — the abelian additive
  χ-cocycle (`A1k`), the abelian additive ζ-cocycle (`A1s4`) and the y-reparametrization
  chain-rule cocycle (`A1p2`) — with the layers composing SEMIDIRECTLY (ψ on χ's argument `A1l`;
  χ/ψ on ζ's arguments `A1s5`) and the slacks moving the shift row (`A1g2` χ; `A1s3` ζ): the
  overlap data form a coupled layered system. Full J-row verdicts J01–J15: ledger.

**Breaks: NONE at A1 depth.** No banked requirement is destroyed; several become conditional on
the carried forks (the reading forks; the A3-deferred R9 content) — conditionality is a posing
fact, not a break.

**New requirements: NONE FORCED.** Three candidates examined, each absorbed: (i) periodicity — a
DOMAIN fact (`A2a`), not a new law; (ii) the angular pairing domain — the J03 supplied-structure
slot, here filled canonically by the registered compact domain; (iii) the angular slack overlap
laws — J07 instances (derived, `A1k`/`A1p2`/`A1l`).

**Class re-tally:** primary classes UNCHANGED — PW 8, WS 2, GC 4, R11 per-row; no migration at A1
depth. PW members now act on the TRI-graded jet space; WS members on angular-live solutions; GC
members carry the typed angular seats above. The C-1 control checks this tally restricts exactly.

---

## TA-3 — the angular character/mode layer (the organizing layer for A2, DERIVED)

The residual T² translation layer (A1d) is compact and abelian; its representation content
organizes the angular sector exactly:

- **Orthogonality is exact on the registered periods** (`A3a`): ∫₀^P e^{2πiny/P} dy = 0 for
  nonzero integer n (= P at n = 0) — the pairing's angular domain is canonical.
- **Translations DIAGONALIZE on characters** (`A3b`): y → y+a acts on e_n by e^{2πina/P} — the
  equivariance machinery for angular-live components decomposes per character.
- **Angular jets act by mode multiplication** (`A3c`): ∂_y e_n = (2πin/P)e_n — the tri-graded
  alphabet's angular grading is mode-compatible.
- **The derived mirrors act by mode negation** (`A3e`); K₄ acts on moduli only and COMMUTES with
  the decomposition (`A1m`) — T2's layered character table extends by one angular column, per mode.

**Status of the layer (F-A2 discipline):** harmonic decomposition is Category-A TECHNIQUE — the
organizing decomposition for Stage A2's equivariance/alphabet runs, NOT adopted physics; no
component is forced to live at any mode. **The mode bound is a LAYER** (A-L2): any A2 computation
bounding the mode index states the bound and types the remainder (T3-style); a silent cutoff would
be a frozen sector. The mode index is DUAL/decomposition data of a FUNCTION; it carries no
field-cycle content — that census is Stage A3's contract (F-A1).

---

## TA-4 — composition facts (derived or typed; nothing decided)

1. **Reading-independence's angular fate: first leg DERIVED, theorem TYPED.** The corrected
   derivative D_x = ∂_x − (g_xy/g_yy)∂_y is EXACTLY χ-slack-invariant (`A4a`, the TU1f analog);
   γ_xx is χ-invariant identically (`A1j`); the alphabet reorganization is triangular-invertible
   (`A4b`, the TU1g analog). The structure that carried T2's reading-independence theorem
   EXTENDS to the angular sector; whether the full theorem survives angular content is Stage A2's
   derivation (TYPED, not claimed, per the contract).
2. **The lock-reading fork's angular interaction: SPECTATOR.** The fork's split term is the
   t-mixing term exactly, pointwise (`A1b`); angular dependence neither creates, decides, nor
   deforms it. It travels undecided with both branches (T1 stamps).
3. **A NEW fork exists and is the angular analog, not an interaction:** the SPATIAL-reading fork
   (`A1h`/`A1i`/`A1i2`/`A1j`/`A1j2`/`A1j3`) — coordinate spatial pin ⇒ NON-REMOVABLE m-row
   (joint-slack orbit = the level set of mᵀB⁻¹m, `A1i2` — AM-B restate; the invariant is the
   irreducible datum); projected spatial reading ⇒ m fully removable chart-slack (s = −B⁻¹m,
   `A1j3`). Carried both ways, decided by nothing here (F-A4; fork verifier-confirmed both
   ways). Stage A2 must carry BOTH reading forks (lock and spatial) to the same depth.
4. **R-A travels TYPED** (A-L8): the angular-completion package's point-involution premise is
   neither used nor resolved anywhere in this package; the fold-selector/E0-collapse results stay
   conditional on it. No angular symmetry inherits ratified status by echo (G18; the mirrors of
   §1.2 leg 5 are bridge floor only).
5. **NO cycle/winding statements are made anywhere in this package** (F-A1): every mention of
   that content in this record is a scope-exclusion pointing at Stage A3; the banked kills' scopes
   (MAP §2) are untouched inputs, re-adjudicated nowhere here.

---

## TA-5 — the in-package controls, the A-L9 registry sweep, and the honest split

### 5.1 C-1: T1 recovery (the calibration identity) — PASS, F-A7 NOT fired

- **Object-by-object** (`C1a`): the y-independent restriction column of the 50-row angular-live
  ledger maps the 18 extended O-rows, 15 R-rows and 15 J-rows onto the banked
  `TIMELIVE_T1_LEDGER.tsv` rows one-to-one, in order, name-matched — parsed mechanically from
  BOTH files, never hand-copied. The two new rows restrict properly: O19 → ABSENT (the banked
  block-diagonal x-angular structure); O20 → ABSENT (arena scaffolding, not census, in the T1
  posing).
- **Requirement classes** (`C1b`): the banked tally PW 8 / WS 2 / GC 4 + R11 per-row parses from
  the T1 ledger and matches the angular-live ledger's claimed classes row-by-row: no migration.

### 5.2 C-2: transitive static recovery — PASS

- **My ledger → banked census** (`C2a`): the static+y-independent restriction column names the
  16 banked `VARIATION_DOMAIN_CENSUS.tsv` objects in order, exactly; O17 → the canonized DIAGONAL
  premise (N = 0); O18/O19/O20 absent from the static posing.
- **Transitivity leg** (`C2b`): the T1 ledger's own static-restriction column names the same 16
  objects in the same order (T1's C1a re-run mechanically): restriction composes
  angular-live → time-live → static exactly.

### 5.3 C-3: the A-L9 registry sweep (list BUILT; registry NOT edited)

`NEGATIVES_REGISTRY.md` swept mechanically (`C3a`). **AMENDMENT AM-C:** the original two-keyword
regex (`axisym` / `one-parameter`) under-covered its prereg spec — it missed the digit form
`1-PARAMETER` and the entry-#17 "spherical-average interface reading" premise class. The WIDENED
vocabulary (`axisym` / `one-param` / `1-param` / `spherical` / `even-sector`) flags
**10 → 17 candidate entries** (old sweep strictly contained in new; anchors + premise quotes in
`angular_A1_results.json` and `DECISION_SURFACE_UPDATE.md`; registry NOT edited). Per A-L9, each
flagged entry needs a premise-scope re-grade BEFORE it can block an angular-live result;
classification (genuine presentation-premise vs incidental wording) and any registry edit are
DRIVER work post-bank.

### 5.4 Honest substantive/guard split, reuse, outcome

`derive_angular_A1.py` (post-amendment): **47 checks, 47 passed — 38 SUBSTANTIVE + 9 GUARD**
(40 → 47: the seven amendment checks `A1s`–`A1s5`, `A1i2`, `A1j3`), all wired into the
exit path (T1-amendment precedent); exit 0; deterministic (stdout byte-identical across re-runs,
verified); runtime < 1 min CPU, exact SymPy throughout, no floats/numeric solvers/RNG/GPU (`G3`
self-scan; `G4` = the F-A1 vocabulary self-audit on the record and ledger). Guards enumerated
(9): `A1o` tri-graded count (declaration-grade), `A1p2` chain-rule instance, `A2c` banked R4
re-run, `C1b`/`C2b` declaration-grade table comparisons, `G1` JSON roundtrip (wired), `G2` ledger
shape, `G3` hygiene, `G4` F-A1 scan. Reuse: K₄/η/frame conventions verbatim from the banked T1 /
Route B scripts; the T1 ledger and banked census TSVs are PARSED as control references, never
re-derived. **Outcome class: OA1-1** — the angular-live posing closes cleanly: census (20
objects) + requirement re-posing (no breaks; none forced) + the angular symmetry/character layer
all derived; T1 recovery exact; static recovery transitive; the two reading forks (lock and the
NEW spatial) both carried, neither decided. Ceiling honored: no response law, no solve, NO
angular cycle census (Stage A3; F-A1), no topology/posture adopted, no physics.


