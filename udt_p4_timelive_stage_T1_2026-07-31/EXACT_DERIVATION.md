# Stage T1 — exact derivation record: the response inverse problem re-posed TIME-LIVE (TT-1..TT-5)

Date: 2026-07-31. Branch: grok. Contract: `PREREGISTRATION.md` (frozen first). Named checks in
`monospace` are exact zero-residual SymPy checks in `derive_timelive_T1.py` (no floats, no numeric
solvers, deterministic; exit nonzero on failure). **Ceiling honored throughout:** no response law
selected, nothing solved, no cycle census run, no topology branch adopted, no dynamics claimed.

**Stamps carried by every statement:** registered chart's time extension (T-L1 CHOSE, stamp
travels); EVERYTHING-ON per owner ruling (T-L2 RESOLVED: shift row LIVE; diagonal-frozen and
static enter only as in-package controls C-1/C-2); time-jet layer <= 2 (higher TYPED); wall layer
N=2 analog (deeper TYPED); the time-topology fork carried three ways, NONE adopted (T-L3 +
owner-kernel clarification); theta ABSENT (T-L6); both moduli census readings carried; all
pointwise statements off-shell on the Route B / Stage-1 footing.

---

## TT-1 — the time-live variation domain, exact

### 1.1 The foundation legs: what the derived time-hardware FORCES

The canonized hardware (C-2026-06-18-1) is: clock law g_tt = −e^{−2φ}c² (the COVARIANT time-time
row — the proper rate of a coordinate-stationary observer, `T1j_static_observer_rate_is_exp_minus_phi`:
dτ/dt|_{dx=0} = e^{−φ} exactly, shift-independent) and the reciprocal lock B = 1/A
(g_tt·g_rr = −c², kinematic). Extending the registered chart with time-dependence on everything
and the time–space mixed row LIVE, the following are DERIVED (not chosen):

1. **NO FREE LAPSE — exact form.** Under a time reparametrization t → h(t) the covariant
   components scale as g_tt → h′²g_tt, g_ti → h′g_ti, g_ij fixed. The clock row ALONE does not
   rigidify h (a compensating φ-redefinition exists); it is the RECIPROCAL LOCK that does:
   preservation of g_tt·g_rr = −c² forces h′² = 1, i.e. h′ ∈ {−1, +1}
   (`T1a_lock_forces_unit_time_speed_reading_i`), and the same rigidity holds in the projected
   reading of the lock (`T1b_..._reading_ii`) — reading-robust. **The residual time
   reparametrizations of the registered time-live chart are exactly t → σt + t₀, σ = ±1** — an
   affine group T₁ ≅ ℝ ⋊ ℤ₂ (`T1c_residual_time_maps_form_group`). GR's arbitrary-lapse freedom
   does not exist here; no derivation opened it.
2. **THE SHIFT ROW'S NATIVE FORM.** The primitive object is the covariant mixed row g_ti = N_i
   (three components in the extended chart) — entered DIRECTLY, never through an ADM
   lapse–shift split. The two parametrizations are exactly inequivalent when the shift is on:
   −1/g^{tt} = e^{−2φ}c² + N²/g_xx (`T1j_covariant_pin_is_not_ADM_lapse_pin`), i.e. pinning the
   canon clock row is NOT an ADM lapse pin — the difference N²/g_xx is the F-T2 discriminator,
   and this package pins the canon object. Canon lists all off-diagonal/shift terms FREE; the
   shift row therefore enters the variation domain as a VARIED FIELD (T-L2 RESOLVED), tag
   DERIVED-FREE-BY-CANON.
3. **THE SLACK CLASS AND ITS PARTIAL FREEZING (residual freedom of the shift).**
   *[AMENDED 2026-07-31, verifier round 1 — AM-1/AM-2: the original leg overstated "the spatial
   pin kills ψ"; the branch structure is now derived as checked steps.]* The map t → t + ψ(x)
   preserves the clock row exactly (`T1n`) and moves the shift row affinely:
   N′ = N + g_tt ψ′, g′_xx = g_xx + 2Nψ′ + g_tt ψ′² — from the diagonal stratum it GENERATES
   shift (`T1o`). The freezing is READING- and PIN-dependent, exactly:
   - The registered spatial pin ALONE gives ψ′ ∈ {0, −2N/g_tt} — TWO branches
     (`T1p2_spatial_pin_alone_two_branches`); uniqueness of ψ′ = 0 requires ALSO pinning the
     shift row — a pin on a varied field (`T1p_spatial_and_shift_pins_jointly_kill_psi`).
   - The second branch ψ′ = −2N/g_tt is a LAWFUL residual chart map on strata where
     2Ne^{2φ}/c² is t-independent: it preserves the clock row, the spatial row and BOTH lock
     readings, and flips N → −N (`T1p3_Z2_residual_branch_flips_N_stratum_conditional`) —
     a stratum-conditional ℤ₂ ψ-branch of the residual symmetry. The orbit of N stays {N, −N}:
     **irreducibility-as-non-removability SURVIVES** (the branch flips N's sign, it never
     removes N) (`T1r_shift_irreducible_under_residual_group`, restated).
   - **THE READING FORK IS LOAD-BEARING (AM-2):** under a PROJECTED-reading spatial
     registration (pin γ_xx, not g_xx), ψ′ = −N/g_tt is lawful wherever N/g_tt is
     t-independent and REMOVES the shift entirely — the new chart is DIAGONAL with
     g′_xx = γ_xx, clock row and projected lock reading exactly preserved
     (`T1p4_projected_reading_pin_makes_N_removable`). **So the shift row's irreducibility is
     CONDITIONAL on the COORDINATE-reading (i) spatial pin of the registered chart** (leg 4's
     fork; T-L1 CHOSE covers the pin, and the condition is now stamped, not silent).
   Across charts of the extended class the ψ-slack survives as a J07-type OVERLAP datum
   (its cocycle law is derived in TT-2/J07, `T2i`).
4. **THE LOCK'S TWO TIME-LIVE READINGS — a derived fork, carried.** With the shift on, the
   coordinate reading (i) g_tt·g_xx and the projected/radar reading (ii) g_tt·γ_xx
   (γ_xx = g_xx − g_tx²/g_tt) split by exactly γ_xx − g_xx = N²e^{2φ}/c²
   (`T1k_two_lock_readings_differ_iff_shift`): they coincide identically on the diagonal
   stratum (the entire banked record — which is why canon is SILENT on the split). Derived
   structural fact, reported not adopted: reading (ii) is exactly ψ-slack-invariant
   (`T1l`) while reading (i) is a ψ-frame quantity (`T1m`, certified nonzero shift). The fork
   travels as an open premise (T-L ledger row, new): LOCK-READING ∈ {coordinate, projected};
   both rigidify the lapse identically (`T1a`/`T1b`).
   *[AMENDED 2026-07-31, verifier round 1 — AM-2: fork UPGRADED from carried-cosmetic to
   **LOAD-BEARING**.]* The fork is not presentation-deep — it decides the shift row's status
   (leg 3, `T1p4`): under reading (i) the time-live domain has an IRREDUCIBLE shift DOF; under
   reading (ii) the shift is PURE CHART-GAUGE on the registered chart (removable where N/g_tt
   is t-independent). That is physical-content for Stage T2 and it is decided by NOTHING in
   this package: canon states the lock on the diagonal stratum where the readings coincide
   identically (`C2a`; CANON.md:186–217 is silent on the shift-on extension, and its own line
   is that DIAGONAL is a choice) — no banked structure constrains the fork, so BOTH branches
   travel with full stamps (F-T4 honored: not resolved here).
5. **ANCHOR SHIFT, TIME-EXTENDED (D3 extension).** φ → φ+s is absorbed by c_E → c_E·e^s PLUS
   the derived unit rescale (t, r) → (e^s t, e^{−s} r): clock row, locked radial row, and the
   anchored readout Q = c_E e^{−φ} all exactly invariant (`T1q`). On the registered chart
   (units pinned; the areal leg carries r²) the shift acts as an OVERLAP map between
   presentations, not a chart automorphism — shift-EQUIVARIANCE (F-RA4) extends with the t-leg
   factor surfaced. Matches banked D3; nothing new imposed.

### 1.2 The residual chart symmetry: does K₄ survive, grow, or deform?

**Answer (derived, layered): K₄ SURVIVES VERBATIM, and the residual symmetry GROWS by the
derived time factor — with the growth itself split across two layers.**

- Every K₄ element fixes the frame time axis (Λ⁰₀ = 1, zero time-space mixing —
  `T1d_K4_elements_fix_frame_time_axis`; SO⁺ membership + closure re-verified `T1e`/`T1f`).
  The K₄ action is pointwise-algebraic: with every generator entry an arbitrary function of
  (x,t) the banked characters hold unchanged — λ, k_mod invariant, k10 χ_a, C signed flips —
  t is a SPECTATOR of the quotient (`T1s_K4_moduli_characters_t_spectator`). K₄ acts trivially
  on the metric components N_i (frame rotations leave g invariant).
- The time factor: translations t → t + t₀ always; the reflection σ = −1 is LAYERED. At the
  METRIC-presentation layer t → −t preserves g_tt, g_ij and flips g_ti (`T1h`) — a residual ℤ₂
  acting on the shift row by sign. At the REGISTERED-COFRAME layer it is OBSTRUCTED: restoring
  the future-pointing time leg needs a frame element with Λ⁰₀ ≤ −1, and the exact column-0
  identity Λ⁰₀² = 1 + Σᵢ(Λⁱ₀)² ≥ 1 splits O(1,3) into Λ⁰₀ ≥ 1 (orthochronous; contains K₄) and
  Λ⁰₀ ≤ −1 — disjoint from the banked SO⁺ registration (`T1g`, `T1i`). **So [AMENDED
  2026-07-31, verifier round 1 — AM-1]: residual symmetry on the registered time-live chart
  (coordinate reading) = K₄ × ℝ_t (translations) TIMES the stratum-conditional ℤ₂ ψ-branch of
  §1.1 leg 3 (ψ′ = −2N/g_tt where 2Ne^{2φ}/c² is t-independent; acts as N → −N only —
  `T1p3`), with the time-reflection ℤ₂ present at the metric layer only; admitting the latter
  at the coframe layer requires ENLARGING the gauge registration beyond SO⁺ — a CHOSE, not a
  derivation. Under the projected reading the ψ-maps are instead a removal slack (`T1p4`; leg
  4 fork, LOAD-BEARING).** No element of K₄ is killed; nothing deforms; the K₄-quotient
  structure of the moduli transfers with t as spectator.

### 1.3 The census rebuilt (18 objects; full table = `TIMELIVE_T1_LEDGER.tsv` rows O01–O18)

The 16 banked objects each acquire a time-dependence status (DERIVED-or-CHOSE-tagged in the
ledger), plus exactly TWO new census rows, both provenance-chained:

- **O17 shift_row_N (g_ti; 3 components N_i(x,t))** — VARIED-FIELD; tag DERIVED-FREE-BY-CANON
  (C-2026-06-18-1 lists off-diagonal terms free) + T-L2 RESOLVED (owner ruling). Native form =
  the covariant mixed row (§1.1 leg 2). *[AMENDED 2026-07-31, verifier round 1 — AM-2 stamp:]*
  irreducibility is CONDITIONAL on the lock-reading fork — under the COORDINATE-reading (i)
  spatial pin, irreducible (all residual maps, including the stratum-conditional ℤ₂ ψ-branch,
  act on N by sign only — §1.1 leg 3); under the PROJECTED-reading (ii) registration, N is
  removable chart-slack (`T1p4`). Fork LOAD-BEARING, both branches travel. K₄-trivial,
  T₁-sign character (§1.2). Static restriction: N ≡ 0 — the canonized DIAGONAL choice,
  recovered as a control stratum (C-2), not re-smuggled as a default.
- **O18 time_topology_label 𝔱 ∈ {(a) line, (b) circle, (c) finite time-cell}** — a discrete
  domain label the extended domain cannot avoid carrying (the domain's own definition depends
  on it); tag FREE-AND-EXPLORED, NONE adopted; owner-kernel standing note travels ((b)/(c)
  derivation-only entry). Typed in TT-3; static restriction: absent (the t-direction
  factorizes out of the static posing — C-1).

Field rows gain (x,t)-dependence (φ, f, bh — canon leaves φ's time-dependence explicitly FREE);
moduli rows keep the const-vs-field fork and gain a TIME-READING sub-fork typed three ways
(constant / m(t) / m(x,t)) with the K₄ characters t-spectator (`T1s`); wall strata become
timelike surfaces (W × ℝ_t; derived in TT-3's `T3b`) with time-extended germ data; corner
strata extend by × ℝ_t with the branch-(c)-only new corner type TYPED; the completion label 𝔠
stays spatial and is JOINED (not replaced) by 𝔱; chart registration extends per §1.1–1.2.
Time-jet layer ≤ 2 on every varied object (Category-A bound, stamped; higher jets TYPED).

---

## TT-2 — the requirement set re-posed (R1–R15; verdicts in `TIMELIVE_T1_LEDGER.tsv` rows R01–R15, J01–J15)

**Verdict vocabulary:** transfers-unchanged / extends-with-derived-modification / breaks(how) /
gains-time-component. Every verdict carries its derivation or exact reason in the ledger row; the
computational legs are the `T2*` checks. Headline structure:

- **Transfers-unchanged (4): R1, R4, R10, R14.** R1's provenance audit is definition-level (its
  index set extends to the 18-object census — content unchanged). R4's exact conditions are
  pointwise-algebraic and t is a spectator (`T2g`, `T2h`: any functional of tr X has identically
  zero k_mod-pairing with t-live symbols; the volume-density channel likewise). R10 is honored
  by construction (the domain is built on the Route B bank). R14 is a WS discipline statement
  untouched by the extension.
- **Extends-with-derived-modification (8): R2, R3, R5, R8, R9, R12, R13, R15.** R2: the
  component list is now indexed by the 18-row census — a missing R_N component = a silent freeze
  (exactly the static era's presentation-freeze, now visible). R3: completion arguments gain 𝔱
  and (branch (c) only) time-completion data. R5: "one solution" = one time-live solution; the
  mass/volume/density relation acquires a typed sub-fork — per-time-slice vs whole-history
  reading — undecidable before a response law exists (still WS; the fork is a POSING fact).
  R8: the Helmholtz test's declared pairing now requires a TIME-DOMAIN datum (branch-dependent;
  see TT-4); self-adjointness is tested on the bigraded jets (time-jets ≤ 2). R9: the cycle set
  of 𝒟 becomes topology-branch-dependent; on (a) no new time-cycles exist; on (b)/(c) the census
  is Stage T3's contract — NOT run here (F-T1). R12: the static bank is RE-READ as a pullback —
  the time-live 𝓡 is the primary object and the banked static posing is its restriction to the
  static stratum; defining on the stratum and varying is now itself the named restrict-then-vary
  violation. R13: fitted TIME-averages join the excluded class (same clause, new instance).
  R15: the honesty condition extends verbatim to 𝔱 — **a time-topology label alone must not
  convert into a source/matter term absent field support** (the bridge-hope guard is already a
  requirement instance, not a new rule).
- **Gains-time-component (3): R6, R7, R11(J07).**
  - **R6 (the temporal-mirror branch, DERIVED — the seam-machinery extension).** The temporal
    involution is derived from the metric form, not posited: form preservation under t → −t
    FORCES φ EVEN-composed (the exponential clock law forbids a φ sign flip), the shift row
    ODD-composed, spatial data EVEN-composed (`T2a_temporal_mirror_parity_assignment_derived`).
    Parity jet-kill at a symmetric locus t=0: even fields lose ALL odd t-jets (∂_tφ = 0 — a
    moment of time symmetry), the shift row vanishes there with all even jets (`T2b`, `T2c`) —
    the exact S0d analog, giving the wall-slot structure a temporal mirror would carry. THE
    BRIDGE-VS-CLOSURE LINE (G18, maintained from the start): all of the above is BRIDGE-floor
    content (what a temporal mirror IS, derived). Whether any locus is CLOSED by it —
    fold/partner/glue+B/open-end, the TS1 τ-menu transposed to a time-wall — is branch-(b)/(c)
    business with derivation-only entry; **the temporal mirror does NOT inherit the spatial
    closure's ratified status**, and it is structurally DISTINCT from the spatial mirror: the
    spatial mirror flips the FIELD sign (φ → −φ, weight swap), the temporal mirror reflects the
    ARGUMENT with φ unflipped (`T2d`). Additional derived obstruction: at the registered-coframe
    layer the t-reflection needs a non-orthochronous frame element (TT-1 §1.2), so a temporal
    mirror cannot even be DEFINED at that layer without enlarging the SO⁺ gauge registration —
    a CHOSE any branch-(b)/(c) entry would owe explicitly. The timelike-wall part of R6: wall
    jet-pairing extends with the time-jets of wall traces (wall layer N=2 analog; deeper TYPED).
  - **R7:** equivariance legs transfer pointwise (t spectator — `T2e`, `T2f`); the Noether
    identity leg transfers as an identity; the CONSERVATION row gains a live time-component:
    current statements become continuity-TYPE (∂_t density + div flux) instead of div-only —
    posed, not solved (their content waits on a response law; WS).
  - **R11/J07:** the chart-overlap obligation gains the derived ABELIAN time-slack cocycle:
    successive ψ-maps compose additively on ALL metric components
    (`T2i_psi_overlap_cocycle_composes_additively`), sitting alongside the banked twisted E08
    two-sided law (which itself transfers with t spectator). J-row verdicts: J01/J02/J12/J14/J15
    transfer; J03 (pairing typing + time-domain datum), J04 (shift-equivariance time-extension,
    TT-1 leg 5), J05 (the full tangent gains δN slots), J06 (moduli time-reading), J08 (𝔱 in
    descent data), J09 (type-changing strata are now potential dynamical loci; the declaration
    obligation is unchanged), J10 (K₄ × time factor; SO⁺ registration now load-bearing), J11
    (time-loops branch-conditional → T3), J13 (discriminator slots persist; 𝔱 joins the
    completion controls) all extend — per-row detail in the ledger.

**Breaks: NONE at T1 depth.** No banked requirement is destroyed by the extension; the honest
finding is that several become CONDITIONAL ON THE TOPOLOGY BRANCH (R9's cycle set, R6's closure
question, R8's time-domain, J11's loops) — conditionality is a posing fact, not a break.

**New requirements: NONE FORCED.** Three candidates were examined and each is absorbed: (i) the
pairing's time-domain declaration — part of the pairing-structure typing (§1.5 analog / J03),
a supplied-structure slot, not a new law; (ii) the ψ-slack overlap law — a J07 instance
(derived, `T2i`); (iii) hyperbolic well-posedness — NOT a requirement: canon's hyperbolicity
(CANON.md:79–80) is a derived FACT about one banked diagonal class, and elevating an
initial-value well-posedness demand into the requirement set would be the F-T2 template import.
The constraint-vs-evolution decomposition was neither needed nor used anywhere in TT-1/TT-2;
whether the native time-live equations force such a split is a Stage-T2+ OUTPUT question.

**Class re-tally (pointwise/whole-solution/global):** primary classes UNCHANGED — PW 8 (R1, R2,
R4, R7, R8, R10, R12, R13), WS 2 (R5, R14), GC 4 (R3, R6, R9, R15), R11 per-row: no requirement
migrates class at T1 depth. What changed inside classes: PW members act on the BIGRADED jet
space (t-jets ≤ 2); WS members act on time-live solutions (with R5's slice-vs-history fork);
GC members become branch-conditional as above. The C-1 control (TT-5) checks this tally
restricts exactly to the banked one.

---

## TT-3 — the time-topology fork, TYPED (none adopted; no cycle census run — F-T1 honored)

Causal-type anchors, derived with the shift on: spatial walls extended in time are TIMELIKE
surfaces (g^{xx} = g_tt/det > 0 since det = g_tt·g_xx − N² < 0 — `T3b_spatial_wall_times_Rt_is_timelike`);
a t = const locus would be SPACELIKE (g^{tt} = g_xx/det < 0 — `T3b_time_wall_would_be_spacelike`)
— causally unlike every banked wall. Per branch:

- **(a) time = ℝ (line).** LEAST-IMPOSED relative to the owner kernel (kernel: time FLOWS,
  silent on extent) — but it remains the INHERITED DEFAULT, tag HABIT-IF-UNEXAMINED traveling
  until either derived or deliberately chosen. Raises: NO time-walls, NO time-cycles; the
  completion question is the behavior class at t → ±∞ — an open supplied datum of the pairing's
  time-domain (functional-analytic class, same status as P2's dual-space datum). NOTE: the
  finite-cell "no spatial infinity" principle is SPATIAL-scoped AND ratified-not-bedrock; it
  supplies NO argument against a time-line. Entry cost: nothing derivational — which is exactly
  why its default status must stay tagged. R9 on (a): no new cycles.
- **(b) time = S¹ (circle).** NO owner-kernel standing; entry is DERIVATION-ONLY (a derivation
  that completion/requirements force compact time — none exists in the bank) or an explicitly
  tagged free exploration. Raises: a period modulus T (a NEW census object IF entered), R9
  time-periods, J11 time-loop holonomy — all Stage T3. Derived map fact (`T3a`): with static φ
  the proper period is τ(x) = e^{−φ(x)}·T — a time-circle would LOCK position-dependent proper
  periods to the depth field (the clock law transports the period across the cell); t-dependent
  φ case typed only (τ = ∫e^{−φ}dt). No time-walls (S¹ has no boundary). The BRIDGE HOPE lives
  here — named, not fed: nothing in TT-1/TT-2 favors (b); the derived facts above are
  branch-CONDITIONAL typings, not evidence for the branch.
- **(c) time = finite cell [0,T].** NO owner-kernel standing; derivation-only entry; the
  finite-cell principle (spatial, ratified-not-bedrock) supplies NO shortcut. Raises the full
  wall machinery transposed to time: SPACELIKE time-wall strata (`T3b`), time-extended germ
  data with the TEMPORAL-MIRROR bridge floor of TT-2 (parities φ EVEN / N ODD; jet-kill), a
  time-completion census (the analog of the 12 FC families — NOT enumerated here; Stage T3),
  and NEW corner strata (spatial wall × time-wall). The TS1 τ-menu transposes as TYPES:
  FOLD-QUOTIENT ↔ temporal-mirror closure (G18: no inherited ratified status + the coframe-layer
  obstruction CHOSE); PARTNER ↔ continuation beyond the time-wall; GLUE+B ↔ a temporal seam
  functional — **named F-T2 hazard: a "glue+B at t = 0" surface term is exactly where the
  initial-value template could re-enter dressed as wall machinery; any such entry owes a native
  derivation**; OPEN-END ↔ free temporal endpoint. All TYPED; none populated, none adopted.

Owner-kernel standing note (travels verbatim): branches (b)/(c) enter by derivation only; the
bridge hope has no foundation story here and the verification bar on any (b)/(c) finding is
RAISED, not lowered.

---

## TT-4 — the response one-form re-posed (posing only)

The general time-live response over the 18-object census:

    𝓡 = ( R_φ ; R_f , R_bh [, R_α][, R_c_E] ;            — field slots, now (x,t)-dependent
          R_λ , R_k_mod , R_k10 , R_C ;                   — moduli slots (time-reading fork carried)
          R_N_x , R_N_y , R_N_z ;                         — NEW: shift-row slots (O17)
          {R_∂ per timelike wall stratum} ; {R_corner} ;  — wall/corner slots with time-jets of traces
          [branch (c) only, TYPED: {R_timewall}, {R_timecorner}] )

- **Grading:** BIGRADED jets (spatial jet order, time jet order ≤ 2; higher TYPED). A candidate
  declares both orders; the domain typing stays order-agnostic.
- **Equivariance structure:** unchanged in kind — equivariant family, contragredient transport,
  character-matched relative K₄ invariance — all pointwise with t spectator (`T2e`–`T2h`, `T1s`);
  the new R_N slots are K₄-trivial and T₁-sign-odd (they pair δN, which flips under the
  metric-layer time reflection), i.e. their character data is DERIVED from TT-1 §1.2.
  *[AMENDED 2026-07-31, verifier round 1 — AM-2 stamp:]* what the R_N slots CARRY rides the
  lock-reading fork: physical-content components under the coordinate reading; pairings of
  pure chart-slack under the projected reading (`T1p4`) — carried both ways into Stage T2.
- **J-obligation analogs:** the chart-overlap laws now include time — the banked twisted E08
  cocycle (t-spectator) PLUS the derived abelian additive time-slack cocycle (`T2i`); loop
  holonomy of the slack cocycle is trivial by additivity; time-loops are branch-conditional (T3).
- **Pairing structures:** P1/P2/P3 re-type verbatim with ONE new supplied datum each — the
  TIME-DOMAIN of integration (branch (a): a decay/integrability class on ℝ_t; branch (b): the
  period; branch (c): the time-cell with its wall terms, making P3's stratified reading
  REQUIRED there). Enumerated; none adopted.
- **WHERE THE STATIC ℛ_PW SITS (posing fact, the TT-4 headline):** it EMBEDS. Killing the
  shift-row slots and the branch-(c) slots recovers EXACTLY the banked component list
  (`T4a_component_list_static_restriction_matches_stage1`); the banked static object is the
  TANGENTIAL restriction of the time-live 𝓡 to the static stratum (R12's pullback reading).
  Not a deformation, not a break — with one honest caveat stated: ON the static stratum the
  time-live object still carries transverse components (R_N at N = 0; time-jet pairings) that
  the static bank never carried; the embedding is of the banked object INTO the larger one,
  and the transverse content is exactly what Stage T2 must derive (embed/deform/break at the
  LAW level is a T2 question — here it is answered at the POSING level only).

---

## TT-5 — the in-package controls, the #22 re-grade, and the honest split

### 5.1 C-1: static recovery (the calibration identity) — PASS, F-T7 NOT fired

- **Object-by-object:** the static restriction (t-independence, N = 0, t-direction factored) of
  the 18-row time-live census equals the banked 16-row `VARIATION_DOMAIN_CENSUS.tsv` EXACTLY,
  in order, parsed mechanically from both files (`C1a_census_static_recovery_object_by_object`).
  The two killed rows restrict properly: shift_row_N → the canonized DIAGONAL premise (N = 0);
  time_topology_label → absent (the t-direction factorizes out of the static posing).
- **Requirement-by-requirement:** the re-posed primary classes restrict to the banked
  PW 8 / WS 2 / GC 4 + R11-per-row tally exactly; no class migration; 15 R-rows + 15 J-rows
  present (`C1b_requirement_class_recovery`).
- **Banked exact checks through the time-live machinery restricted static:** the tangent block
  form [[2I₂, Cᵀ],[C, K+Kᵀ]] and D3 anchor absorption re-derived identically (`C1c`); the K₄
  membership/closure re-runs are `T1e`/`T1f`; the R4 blindness re-runs are `T2g`/`T2h`.

### 5.2 C-2: the diagonal-frozen (shift-off) control stratum

Derived relation to the full domain: a codimension-3-function stratum (N_i ≡ 0), on which the
two lock readings coincide IDENTICALLY (`C2a`) — the banked record's silence on the reading
fork is exactly this stratum's shadow. The stratum is NOT invariant under the extended chart
class: the ψ-slack maps it out of itself (`C2b`), so shift-off is a chart-conditional CONTROL,
never a physics restriction. What the live shift adds, exactly (`C2c`): (1) the three R_N
response slots + δN tangent directions; (2) the lock-reading fork (LOAD-BEARING per AM-2); (3)
the ψ-slack J07 overlap datum (on-chart it reduces to the stratum-conditional ℤ₂ branch under
the coordinate reading and to a removal slack under the projected reading — §1.1 leg 3,
AMENDED); (4) the nontrivial metric-layer time-reflection action (N → −N); (5) the
ADM-inequivalence discriminator (−1/g^{tt} = e^{−2φ}c² + N²/g_xx).

### 5.3 The #22 negative — premise-set re-grade (T-L7; recorded here, registry edit owed at commit)

Banked premise set (NEGATIVES_REGISTRY.md ~452): "P1 metric class + full time row, axisymmetric
even sector, C1-only, Q ≠ 0 convention"; two clauses ("no sector propagates hyperbolically in
T"; "cells do not evolve") already CONDITIONS-CHANGED 2026-06-13 (the v_a3 sign error; canon
C-2026-06-13-1). Re-grade against the Stage-T1 domain: the surviving clauses (fate polynomial
f_T-free; motion never sources shape; no bounded-in-T continuation) were derived on the
OLD-OPERATOR, DIAGONAL (no shift row), SINGLE-CARRIER (C1-only), pre-E02/pre-moduli footing.
The Stage-T1 domain is none of these: shift row live, E02 seven-parameter coframe class,
moduli sector, both census readings, temporal-mirror structure derived not assumed. VERDICT:
**#22's premise set does NOT cover the time-live P4 domain; it retains authority ONLY on its
own stratum (diagonal, C1-only, old-operator) and cannot block any Stage-T finding.** It is
not refuted here (no solve was run — ceiling); it is SCOPED. #57/#65 stay retired (wholesale
2026-06-19 retirement; no re-entry claimed or needed).

### 5.4 Honest substantive/guard split and reuse declaration

*[AMENDED 2026-07-31, verifier round 1 — AM-3: the original tally read "42 checks = 33
SUBSTANTIVE + 9 GUARD" with G1 appended AFTER the tally (latent: a G1 failure could not flip
the exit code), the guard enumeration listed G1 but omitted the counted guard
`T3b_lorentzian_det_negative_diagonal`, and C1b/T4a were graded SUBSTANTIVE though
declaration-grade. All fixed:]* `derive_timelive_T1.py`: **46 checks, 46 passed — 34
SUBSTANTIVE + 12 GUARD** (old→new: 42 counted + 1 latent = 43 executed → honest recount 43 =
31 SUBSTANTIVE + 12 GUARD, matching the verifier's ≈31 estimate; + 3 new amendment
substantive checks `T1p2`/`T1p3`/`T1p4` = 46 = 34 + 12). Guards enumerated exactly (12):
banked re-runs T1e/T1f/T2f/T2h/C1c; declarations T4b/C2c; re-graded declaration-grade
C1b (literal table copy)/T4a (self-authored list comparison); baseline certificate
T3b_lorentzian_det_negative_diagonal; hygiene G3/G1 — with G1 now WIRED into the tally/JSON/
exit path (a G1 failure flips exit nonzero); exit 0; deterministic (byte-identical re-run);
runtime ~15 s CPU, exact SymPy throughout, no floats/numeric solvers/RNG/GPU (`G3` self-scan). Reuse: K₄/η/X/tangent/seat/D3 constructions taken verbatim
from the banked Stage-1 script; the banked census TSV is parsed as the C-1 reference, never
re-derived. Outcome class: **OT-1** — the time-live posing closes cleanly (census + requirement
re-posing + response slots all derived; static recovery exact; fork typed, none adopted).
Ceiling honored: no response law, no solve, no cycle census, no topology adopted, no dynamics,
no physics.

---

## AMENDMENT 2026-07-31, verifier round 1 (all three implemented; full record in `CORRECTION_LAYER.md`)

- **AM-1 (missed ℤ₂ residual branch — overstated group claim).** New checked steps `T1p2`
  (spatial pin alone: ψ′ ∈ {0, −2N/g_tt}) and `T1p3` (the second branch = a lawful
  stratum-conditional ℤ₂ residual map where 2Ne^{2φ}/c² is t-independent: preserves clock row,
  spatial row, both lock readings; flips N → −N). Residual-group claim restated in §1.1 leg 3,
  §1.2, `T1r`, ledger O16/O17/J10, and the results JSON. Irreducibility-as-non-removability
  SURVIVES: the orbit of N is {N, −N}; the branch flips N's sign and never removes it.
- **AM-2 (the load-bearing reading fork — the substantive amendment).** New checked step
  `T1p4`: under a projected-reading spatial registration, ψ′ = −N/g_tt lawfully REMOVES the
  shift (diagonal chart, g′_xx = γ_xx) wherever N/g_tt is t-independent. O17's irreducibility
  and every statement riding it are stamped CONDITIONAL on the coordinate-reading (i) spatial
  pin. The lock-reading fork is UPGRADED to LOAD-BEARING (§1.1 leg 4, ledger, decision
  surface): coordinate reading → irreducible shift DOF; projected reading → shift is pure
  chart-gauge on the registered chart. Decided by NOTHING in this package (F-T4: canon states
  the lock where the readings coincide; no banked structure constrains); both branches travel
  to Stage T2 with full stamps.
- **AM-3 (bookkeeping honesty).** G1 wired into the tally/JSON/exit path; guard enumeration
  reconciled (T3b_lorentzian added; G1 properly counted); C1b/T4a re-graded GUARD/declaration-
  grade. Counts old→new: 42 (33S+9G, G1 latent) → 46 (34S+12G), honest pre-amendment recount
  43 = 31S + 12G. Neither OT-1 nor the C-1 control is touched by any amendment.
