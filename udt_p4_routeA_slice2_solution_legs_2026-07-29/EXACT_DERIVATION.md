# P4 Route A Slice 2 — exact derivation record: the solution-touching legs (TD1–TD6)

Date: 2026-07-29. Branch: grok. Contract: `PREREGISTRATION.md` (frozen before this
derivation; the BOOTSTRAP-LENS frame §2 — Charles's binding ruling — governs every
background statement here). Script: `derive_routeA_slice2.py` — **41/41 checks, exit 0 =
33 SUBSTANTIVE zero-residual exact-SymPy checks + 8 CITATION GUARDS** (guards =
definitional-unpacking / recording-table / citation rows, labeled `[guard]` in-script and
in the JSON, never counted as residual computations), deterministic (no floats, no
randomness, no network, no numeric solvers, no GPU; stdout byte-identical across reruns —
verified), single CPU process, well under budget (FULL DECLARED SCOPE — **no scope-ladder
reduction taken**; the representative-sub-family stamp below is the prereg TD1 clause, not
a reduction). Outputs: `routeA_slice2_results.json`, `DERIVATION_STDOUT.txt`,
`SOLUTION_ATLAS_LEDGER.tsv`, `SLICE2B_SURFACE.md`. Every check named in `monospace` below
is one of the 41.

**AMENDED 2026-07-29** per `VERIFIER_REPORT.md` (verdict PASS-WITH-REQUIRED-AMENDMENTS;
both amendments F-D3-class STAMP repairs — no computation refuted, no falsifier fired;
record = `CORRECTION_LAYER.md`): **A1** — the depth-profile SHAPE is sign(a_F)-scoped
(well for a_F > 0 / bump for a_F < 0; sign-free content unchanged; 3 new `A1_*` checks,
the verifier's sign-free re-derivation adopted); **A2** — the locus-nonemptiness claim
now carries its (a_F, ℓ) = (1, 1) witness stamp, with the verifier's general-(a_F, ℓ)
BOTH-signs legs adopted as the 2 new `A2_*` checks (pre-amendment 36 checks all
surviving, math and pass conditions unchanged; detail-string stamps amended only).

**Slice-2 boundary (binding, carried on every statement):** NO candidate crowned (F-D1);
NO elimination — F-D2 was never engaged (nothing here is eliminated, so no
background-robustness proof is owed); every only/all/none/works/fails statement carries
its cell + fork-branch + stratum + BACKGROUND stamps (F-D3, the NAMED class, three prior
catches); banked inputs recomputed as consistency only (F-D4); no symbolic failure —
41/41 (F-D5); every R5 triple reads ONE solution (F-D6); no carrier, no source content
beyond typed rows (F-D7); the bootstrap neither imposed nor suppressed — every
representative's self-consistent locus computed and reported, or explicitly reported
NOT-DERIVABLE with its reason (F-D8 both directions).

**THE REPRESENTATIVE-SUB-FAMILY STAMP (travels with EVERY atlas claim).** The exhaustive
member of each READY cell is an arbitrary element of a functional-dimension-sized class
(the banked Stage-2 parametrization); solving 𝓡 = 0 for the whole cell in full generality
is not a bounded task. Per the prereg TD1 clause, each cell's atlas rows are
REPRESENTATIVE FAMILIES — the banked Stage-3 witnesses (W1, W2-fs, W3, ω) plus the
generated free-quadratic family GEN-QUAD — each tagged CHOSE(representative) in §0. Every
"solution space" claim below is scoped to its representative family; NONE is a cell
census. Full-cell generality is the first Slice-2b handle.

**Standing scope stamps (travel with every statement):** jet ≤ 2, registered stationary
one-parameter presentation (fields (φ, f, bh), jets p/f/h 0..2), registered positive
triangular chart, BASE branch (moduli constant ⟹ INTEGRATED moduli rows — derived in §1;
BR-M's pointwise rows typed NOT-EXHAUSTED upstream, OUT of READY scope), enumerated
pairing branches (P1-4D a_F = 2λ; P1-triad a_F = 1+2λ; P2 a_F = 0; P3-bulkP2/P3-bulkP1 =
declared bulk + wall blocks), READY bin only (RES-CNEQ0 CENSUS-REQUIRED; 4th-order
EXTENSION-REQUIRED; carriers G09/F-D7 out; time-live out). Anchored Q = c_E e^{−p0} at
supplied c_E (p0 = log(c_E/Q), exact relabeling, banked).

---

## 0. Premises (chose or derived — stamped)

| Premise | Tag |
|---|---|
| Registered chart, K₄, E02 footing; ℛ_PW + k_mod = 0 identity | DERIVED input (banked; recomputed `S0_*`) |
| Gate-cut ledger: READY cells, witnesses, anchored-log iff, TC3 wall census | DERIVED input (Stage-3 bank 21d589c; cited, re-instantiated only) |
| R5 same-solution rule; R14; gate specs | DERIVED input (Stage-1 bank) |
| Route C restricted EH system | DERIVED input (GR-as-reference lane; its CONDITIONAL stamps travel) |
| BASE-branch integrated moduli rows ∫W_M R_μ dx = 0 | DERIVED (definitional unpacking of the enumerated pairing on constant directions — `T0_base_branch_integrated_row`) |
| GEN-QUAD representative L̃₀ = (p1²+f1²+h1²)/2 | **CHOSE (representative)** — the minimal nonzero generated family; instantiates, never filters; full-generality atlas = Slice-2b |
| ω, W1, W2-fs, W3 representatives | DERIVED input (the banked Stage-3 witnesses, reused as reps) |
| R5 volume functional V = ∫W_F dx per branch | THEORY (the branch's own T4-enumerated volume — the pairing branch supplies it) |
| R5 mass instantiation M = ∫E0dens dx (member's own first-integral energy) | **CHOSE (declared instantiation slot)** — CONDITIONAL: the banked mass rows (adjudication) are CONDITIONAL/OPEN; the stamp travels with every R5 number |
| Mirror parity instance ε_φ = −1 (spatial mirror, static sector) | THEORY-cite (CANON C-2026-06-10-2 / C-2026-07-04-1); f/bh parities SUPPLIED, tagged |
| Cell half-length ℓ, anchor c_E, seat λ, retained moduli, 𝔠 | FREE explored BACKGROUND coordinates (bootstrap-lens §2a — never fixed by assumption) |
| Picard uniqueness for solved-form ODE systems; log-monotonicity; integral positivity/continuity | Category-A (cited calculus, named where used) |
| SymPy exact, CPU, single process | Category-A conditioning |

## 1. Structural theorems (T0 — whole-atlas)

- **Zero-set/pairing theorem** (`T0_weight_invertibility_zero_set_theorem`): the anchored
  weight W_F = e^{a_F p0} has exact inverse and is positive, so the FIELD-sector zero set
  of a FIXED component tuple is IDENTICAL across the enumerated anchored family. Pairing
  dependence of 𝓡 = 0 enters ONLY through (a) G3 cell MEMBERSHIP of the tuple (banked,
  pairing-relative) and (b) the W_M-weighting of the integrated moduli rows. Scope:
  enumerated branches, jet ≤ 2, stationary presentation, BASE branch. Visible instance:
  the SAME two zero-set atlases (affine, nodeless quadratic-w) appear in the LE cell of one
  branch and the NV cell of another (§2) — cell membership moves, the zero set does not.
- **BASE-branch moduli reading** (`T0_base_branch_integrated_row` [guard]): on the
  constant-moduli fork the δm_μ coefficient of the enumerated pairing is the INTEGRATED
  scalar row ∫W_M R_μ dx = 0 — one relation per cell per modulus. The pointwise row
  R_μ = 0 is the BR-M reading (typed NOT-EXHAUSTED upstream; out of READY scope).

## 2. TD1 — the solution atlas (per representative family; exact)

### 2.1 GEN-QUAD (LE cells; one symbolic tuple covers all five branches)

R_p = a_F(f1²+h1²−p1²)/2 − p2, R_f = −(a_F p1 f1 + f2), R_h = −(a_F p1 h1 + h2), with the
generated λ-slot 2p0·L̃₀ on the a_F′ ≠ 0 branches (`TD1_LE_generated_components_match`;
Helmholtz (i)–(iii) re-instantiated at symbolic a_F, `TD1_LE_rep_helmholtz_reinstantiated`;
this member is λ-INDEPENDENT in its field sector, so its forced-nonzero λ-slot is exactly
the banked anchored-log iff condition in action — consistency, cited).

**Exact solution family (a_F ≠ 0)** (`TD1_LE_well_solution_zero_residual` — identical
zero residual, no constraint juggling):

    e^{a_F p0} = w(x) = (a_F² E0/2)·x² + w1·x + w0 ,   f′ = c_f/w ,   h′ = c_h/w ,
    free parameters (w0 > 0, w1, c_f, c_h, f(0), h(0)),
    E0 = (w1²/a_F² + c_f² + c_h²)/(2 w0) .

- **Emergent sign structure** (`TD1_LE_disc_E0_sign_structure` — observed, not imposed):
  disc(w) = −a_F²c² ≤ 0 exactly and 2w0E0 = a sum of three squares, so every real member
  has **E0 ≥ 0** (anchored-weight positivity forces nonnegative energy), w has **no real
  root for c ≠ 0** (a globally regular, nodeless depth profile), and E0 = 0 exactly on
  the constant solutions (`TD1_LE_E0zero_constants_only`). E0 ≥ 0, regularity, and
  nodelessness are **sign-free in a_F**. c = 0 gives w = A(x−x₀)² (depth → −∞ at x₀;
  regular on the cell iff x₀ outside it) — edge subfamily, enumerated.
- **Shape is sign(a_F)-scoped (A1 amendment — verifier catch, adopted):**
  p0″(vertex) = 8A²/(a_F³c²) has the **SIGN of a_F**
  (`A1_vertex_curvature_sign_of_aF`, instantiated both ways): for **a_F > 0** the depth
  profile is a single-MINIMUM **well**; for **a_F < 0** — which occurs INSIDE the
  explored background range (P1-4D a_F = 2λ at λ < 0; P1-triad a_F = 1+2λ at λ < −1/2) —
  it is a single-MAXIMUM **bump**, equally regular and nodeless
  (`A1_bump_instance_regular_nodeless`: the explicit a_F = −1 member w = x²/2 + 1,
  zero residual, disc = −2 < 0, p0″(0) < 0). "Symmetric" means about the VERTEX of w,
  not the cell center. The closed form itself is verified at FREE REAL a_F of both signs
  (`A1_well_zero_residual_signfree` — the TD1 positive=True declaration was conditioning,
  not load-bearing). SCOPE: GEN-QUAD representative, a_F ≠ 0 branches, BASE branch.
- **First integrals, derived** (`TD1_LE_energy_first_integral`, `TD1_LE_shift_currents`):
  E0dens = e^{a_F p0}L̃₀, e^{a_F p0}f1, e^{a_F p0}h1 — all exactly conserved on-shell.
- **Exact quadratures** (`TD1_quadrature_f_closed_form`, `TD1_quadrature_logw_closed_form`
  — verified by differentiation): f, h in closed atan form; ∫p0 dx = [G(ℓ)−G(−ℓ)]/a_F
  with the explicit antiderivative G. Honest labels: closed form for E0 ≠ 0, c ≠ 0; edges
  (c = 0: f, h constant; a_F = 0: affine) enumerated.
- **Local exhaustiveness** (`TD1_LE_solution_space_rank6`): the parameter→initial-data
  map has rank 6 (exact, rational point); with the system in solved form u″ = F(u, u′)
  (Picard, Category-A cited) the LOCAL field-sector solution space is EXACTLY the 6-dim
  initial-data manifold, covered by the closed form where w > 0.
- **Background transition** (`TD1_LE_blindness_affine_case`): at a_F = 0 the tuple
  degenerates exactly to (−p2, −f2, −h2) → the AFFINE atlas. a_F = 0 is the whole P2-side
  AND the banked T4 blindness loci INSIDE the P1 branches (λ = 0 for P1-4D; λ = −1/2 for
  P1-triad): **the solution-space shape (quadratic-w — well for a_F > 0 / bump for
  a_F < 0 — vs affine) is background-controlled through the pairing weight** — an exact
  background transition inside a single branch, and the WELL↔BUMP flip at the same loci
  is a second sign-scoped facet of it (A1) (observation).
- Full family coordinates: 6 field parameters × retained moduli (k_mod, k10, C — and λ on
  the P2 side) × background (λ, c_E, ℓ, 𝔠) — all explicit; c_E and 𝔠 drop out of the
  components (proven, §6) and remain readout/completion coordinates.

### 2.2 ω-shape (moduli-sector LE representative, its banked cells)

(`TD1_omega_zero_set_k10_stratum`) The only nonvacuous row is the integrated k10-row
k10·∫W_M dx = 0 with positive integrand, so the EXACT solution space is **the stratum
{k10 = 0} × all fields free × other moduli retained × all backgrounds** — a_M-independent
(pairing-supply branch-independence proven for this row). The ω zero set is exactly the
χ_a-fixed stratum.

### 2.3 NV representatives

- **W1 = (p2, f2, h2)** (`TD1_W1_affine_atlas_and_NV_defect`): zero set = the affine
  atlas (6 params, all moduli retained, all backgrounds); Helmholtz-(ii) defect exactly
  −2a_F p1 e^{a_F p0} — NV on the a_F ≠ 0 branches precisely OFF the blindness loci, LE
  at a_F = 0 (re-instantiating the banked adjudication at symbolic a_F).
- **W2-fs** (the W2′ field sector, zero moduli slots; banked NV under P2)
  (`TD1_W2fs_same_zero_set_under_P2`): the IDENTICAL tuple to GEN-QUAD at a_F = 2λ — the
  P2-side NV cells carry the FULL nodeless quadratic-w atlas (well for a_F > 0 / bump for
  a_F < 0, per the A1 sign stamp; here a_F = 2λ with λ a free background coordinate, so
  both signs occur) and NO λ-row (moduli slots zero): no background tie.
- **W3 = (p1, 0, 0)** (`TD1_W3_underdetermined_member`): zero set = {p0 const} × f, bh
  ARBITRARY × moduli retained — this member's on-shell system is per-member
  DEGENERATE/UNDERDETERMINED (its f/bh rows vanish identically); no contradiction with the
  banked DETERMINED-TYPE count (which types the generic member).

### 2.4 KMOD0 stratum (both cells)

(`TD1_kmod0_noether_residual_zero_reps`, `TD1_kmod0_L23_quotient_reps`) All named
representatives satisfy the banked stratum Noether identity IDENTICALLY (field-sector
members: r_tf = M = 0, the banked all-strata carrier class; ω: r_sh does not enter), so
the KMOD0 atlases are the GENERIC ones restricted to k_mod = 0, uncut. The L23-orbit
quotient is carried: gauge tangent (δλ, δk_mod, δk10, δC) = (0, k10, 0, J·C); GEN-QUAD's
components are (k10, C)-independent (family L23-invariant; quotient acts on retained
moduli coordinates only); ω's zero set {k10 = 0} is invariant and stays on-stratum.

## 3. TD2 — R5 same-solution closure and the self-consistent loci (§2c)

**R5 triple on ONE GEN-QUAD solution (F-D6 clean)** (`TD2_R5_V_M_rho_closed_forms`):

    V = ∫w dx = (2/3)(a_F²E0/2)ℓ³ + 2w0ℓ   (the branch's OWN declared volume — THEORY),
    M = ∫E0dens dx = 2ℓE0                   (M-instantiation = member energy — CHOSE,
                                             CONDITIONAL: banked mass rows OPEN; stamp travels),
    ρ = M/V (exact closed form);  ρ·V = M on the same solution.

**The background-tie row (exact)** (`TD2_lambda_row_exact_form`): the generated λ-slot
obeys W_M R_λ = ∂λ(W_F L̃₀) for BOTH enumerated P1 instances (a_F′ = 2) and EVERY supplied
a_M (the W_M cancels — pairing-supply branch-independence PROVEN); on-shell the integrand
is 2p0E0, so the BASE-branch λ-row is

    2·E0·I_p = 0 ,   I_p = ∫_{−ℓ}^{ℓ} p0 dx = [G(ℓ) − G(−ℓ)]/a_F   (exact closed form).

**Self-consistent locus, computed and reported per §2c:**

- **P1-side GEN-QUAD**: {E0 = 0 (constants)} ∪ {I_p = 0}. The nontrivial branch is
  NONEMPTY at every a_F ≠ 0, ℓ background — **proof coverage (A2 amendment):**
  `TD2_selfconsistent_locus_nonempty` exhibits the two exact sign legs at the SINGLE
  background point (a_F, ℓ) = (1, 1) [witness stamp; note the leg implication
  "w ≤ 5/8 < 1 ⟹ I_p < 0" is a_F-SIGN-DEPENDENT — I_p = (∫log w)/a_F flips with a_F];
  the general claim rests on the verifier's general-(a_F, ℓ) BOTH-signs symbolic legs,
  adopted as `A2_locus_legs_general_sign_pos`/`_neg` (leg A′: w = x²/(8ℓ²) + 1/2 ≤ 5/8;
  leg B′: w = x²/ℓ² + 2 ≥ 2; E0 > 0 proven symbolically on both and along the connecting
  path) + continuity of the explicit closed form (Category-A) ⟹ an I_p = 0 root with
  E0 > 0 exists — **nonconstant self-consistent solutions at every a_F ≠ 0
  background, both signs**. (The two calculus steps — log-monotonicity, integral
  positivity/continuity — are named Category-A; everything else is zero-residual
  algebra.)
- **P2-side members, ω, W1, W3** (`TD2_P2_no_background_tie`): the tie row is
  IDENTICALLY zero → self-consistent locus = ALL backgrounds (degenerate; reported, not
  suppressed — F-D8). The P1 tie degenerates to this exactly at the blindness loci.
- **NV-cell members**: mass functional NOT-DERIVABLE at this slice (no generated
  energy for a nonvariational member; adopting one would be an import) → the
  self-consistent point is reported **NOT-DERIVABLE-AT-SLICE-2** with this reason —
  explicit report per F-D8, typed to Slice-2b.

## 4. TD3 — the lens classification (bootstrap-lens §2; per representative family)

(`TD3_lens_classification_record` [guard]; every entry scoped cell+branch+stratum+background)

| Class | Members |
|---|---|
| WORKS-GENERICALLY | GEN-QUAD (all 5 branches; solutions at every admissible background — constants everywhere, nodeless quadratic-w profiles for a_F ≠ 0 [well for a_F > 0 / bump for a_F < 0 — A1 sign stamp], plus the nontrivial I_p = 0 locus), W1, W2-fs, W3, ω |
| CONDITIONAL-ON-BACKGROUND (§2d positive) | NONE FOUND among representatives at this slice |
| FAILS-BACKGROUND-ROBUSTLY | NONE (no elimination claimed; F-D2 never engaged) |
| UNDETERMINED | the R5 leg of all NV-cell representatives (mass functional NOT-DERIVABLE; reported) |

**Bootstrap observation record (observation only — R14/G12; `TD4_R14_diagnostic_column`):**
- FOR: on the background-anchored pairings (a_F′ ≠ 0) the member's own integrated λ-row IS
  a bootstrap-shaped self-consistency equation (2E0·I_p = 0) tying the solution's content
  to the background seat — it EMERGED from the pairing structure, never imposed; its
  nontrivial branch is populated at every background.
- AGAINST universality: the tie is ABSENT under the weight-free pairing (P2) and at the
  blindness loci — the bootstrap-shaped structure is pairing-branch-RELATIVE, so the
  response structure alone does not force a bootstrap.
- Neither strengthens to adoption; settling is Charles's, later (prereg ceiling).

## 5. TD4/TD5 — on-shell legs and duties

- **Gate-1 on-shell closure** (`TD4_gate1_onshell_record` [guard]): GENERIC — GEN-QUAD/
  W1/W2-fs explicitly integrated determined systems (rank-6 data manifold + closed forms;
  0 or 1 active integrated moduli rows, rest retained/reported); W3 per-member DEGENERATE.
  KMOD0 — same solutions at k_mod = 0, identity trivially consistent, L23 quotient
  carried. RES-CNEQ0 untouched (CENSUS-REQUIRED).
- **Gate-4 currents, none assumed** (`TD4_symmetries_derived_not_assumed`): f-shift,
  h-shift, x-translation are DERIVED symmetries of GEN-QUAD (components f0/h0-independent,
  autonomous); currents e^{a_F p0}f1, e^{a_F p0}h1, E0dens conserved on-shell (exact). No
  continuous symmetry claimed for ω/W3.
- **R14**: diagnostic column only (§4 above).
- **Gate-5 canon-parity leg** (`TD5_parity_admissible_witness`): the ε_φ = −1 trace
  conditions p0(±ℓ) = p2(±ℓ) = 0 cut an exact sub-locus of the GEN-QUAD family, NONEMPTY:
  the everywhere-regular witness E0 = c² = 1/(a_F ℓ)², w = x²/(2ℓ²) + 1/2 (w(±ℓ) = 1,
  min 1/2, both shift currents on). f/bh parities SUPPLIED (tagged, not derived).
- **NV wall duty** (`TD5_NV_wall_duty_record` [guard]): NV reps declare zero
  wall/corner components → varied-fork wall equations vacuous, held-fork consistency
  trivial; live content = parity of the SOLUTIONS' own traces (W1-affine: odd p0-trace
  forces the intercept 0 at each wall — exact); nonzero NV wall blocks = Slice-2b.
- **Gate-2, carrier-free typed form** (`TD5_gate2_J06_record` [guard]): per-modulus J06
  branches recorded — GEN-QUAD@P1-side: λ DETERMINED (2E0·I_p row), k_mod/k10/C RETAINED
  (explicit branch, not omission); GEN-QUAD@P2-side: all RETAINED; ω: k10 DETERMINED
  (forced to 0), rest RETAINED; W1/W2-fs/W3: all RETAINED. No source rows touched (F-D7).
- **4th-order class Slice-2b requirements typed** (`TD5_jet34_slice2b_requirements`
  [guard]): jet-3/4 parametrization; wall grade 4 + 3rd-jet momenta (self-pairing
  impossible at jet ≤ 2, banked); Bach-side instance; per-candidate wall depth.

## 6. TD6 — cross-check, fork independence, survivors map

- **Route C restricted-EH cross-check** (`TD6_EH_crosscheck_exact_solution`;
  GR-as-reference lane, CONDITIONAL stamps travel): the exact family p0 = const,
  f = const, bh = (Ax+B)², Λ = 0 solves ALL SEVEN restricted rows identically at every
  (α, λ, c_E) background — an exact consistent sub-family of the overdetermined
  7-row/3-field restricted system (regular off the coframe-degeneracy root, J01).
  Observation only; the restricted-EH G3 tile stays un-run (Slice-2b).
- **Fork-branch independence PROVEN for the atlas rows**
  (`TD6_fork_branch_independence`): components contain no α (L8/BR-A), no 𝔠 (L4/BR-C), no
  c_E (anchor drops out; c_E stays a readout background coordinate); integrated moduli
  rows a_M-independent (pairing supply); BR-B role-only (banked). Scope: the named
  representatives — NOT a cell-general claim.
- **Survivors map**: `SOLUTION_ATLAS_LEDGER.tsv` — 20 READY cells × representative
  families × fork stamps × exact solution spaces × R5 closure × self-consistent locus ×
  lens class × gate records × Slice-2b handle (`TD6_ledger_coverage` [guard]).

## 7. Outcome and falsifier record (derivation-side)

**Outcome class: OD1** — the survivors map is populated with lens classes; no cell's
representative set is empty at any background; no elimination; no §2d
conditional-on-background find among representatives; the bootstrap observation record
carries one FOR-shaped structural emergence (the pairing-anchored tie) and one
AGAINST-universality observation (pairing-relativity of the tie). OD2/OD3/OD4 not
triggered.

- F-D1 clean — no member crowned/ranked; the ledger is the ceiling.
- F-D2 clean — never engaged (no elimination made; nothing restated).
- F-D3 policed — every works/fails/all/none statement carries cell + branch + stratum +
  background stamps; the representative-sub-family stamp travels with every atlas claim.
  TWO F-D3-class stamp gaps were verifier-caught post-derivation and repaired (A1 sign
  stamp, A2 witness stamp — `CORRECTION_LAYER.md`; the FOURTH instance of the named
  scope class in this arc, memorialized in `AUDIT_REPORT.md`).
- F-D4 clean — banked facts recomputed as consistency (K₄, identity, witnesses' cell
  memberships re-instantiated at symbolic a_F); no contradiction found.
- F-D5 none — 41/41, exit 0; deterministic rerun byte-identical (×3 post-amendment).
- F-D6 clean — every R5 triple reads one solution (V, M, ρ all on the same (w, c_f, c_h)
  member).
- F-D7 clean — no carrier, vacuum + typed rows only; gate 2 run in carrier-free typed
  form only.
- F-D8 clean both directions — no bootstrap in any definition/filter/crown; every
  representative's self-consistent locus computed and reported (LE cells) or reported
  NOT-DERIVABLE with its reason (NV cells; typed to Slice-2b).

**Limits that travel:** (i) representative-sub-family atlas, not a cell census (the
prereg TD1 clause; full generality = Slice-2b); (ii) all statements at jet ≤ 2, BASE
branch, stationary presentation, enumerated branches, READY bin; (iii) the R5 mass
instantiation is CHOSE/CONDITIONAL (banked mass rows OPEN) — every R5 number is
conditioned on it; (iv) local-in-x exhaustiveness only (Picard-local; global extension
governed by w > 0, reported); (v) two named Category-A calculus steps (log-monotonicity;
integral positivity/continuity) inside the locus-nonemptiness and ω-row arguments; (vi)
NV mass functional not derivable here — R5 for NV typed to Slice-2b; (vii) wall blocks,
corners, resonance cells, 4th-order class, carriers, time-live: untouched (typed); (viii)
every depth-profile SHAPE word is sign(a_F)-scoped (well: a_F > 0; bump: a_F < 0 — A1);
the sign-free structural content (E0 ≥ 0, regularity, nodelessness, closed form) is not.
