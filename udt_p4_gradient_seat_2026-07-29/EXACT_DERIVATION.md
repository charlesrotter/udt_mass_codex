# P4 gradient seat — exact derivation record: the jet-extended field-census moduli rows (TG-1..TG-5)

Date: 2026-07-30. Branch: grok. Contract: `PREREGISTRATION.md` (frozen before this
derivation). Script: `derive_gradient_seat.py` — **27/27 checks, exit 0 = 23 SUBSTANTIVE
zero-residual exact-SymPy checks (17 original + 6 verifier-credited, labeled
`[verifier-credited]` in-script/stdout/JSON) + 4 CITATION GUARDS** (guards =
recording/typing rows, labeled `[guard]` in-script and in the JSON, never counted as
residual computations), deterministic (no floats, no randomness, no network, no numeric
solvers, no GPU; stdout AND JSON AND TSV byte-identical across reruns — verified ×3
post-amendment), single CPU process, well under the 90-min budget (**FULL DECLARED SCOPE
— no scope-ladder reduction taken**: both moduli sectors carried — the (λ, k_mod) sector
computationally, the (k10, C) sector by the identical operator form + χ-graded legality
citation with its rows vacuous BY INSPECTION (zero dependence) on the member classes
used — not instantiated as jet chains [AM-3]; jets carried through m″ in the density
with higher jets TYPED). Outputs: `gradient_seat_results.json`,
`DERIVATION_STDOUT.txt`, `JET_ROWS_LEDGER.tsv` (7 rows + amendment stamp row),
`DECISION_SURFACE_UPDATE.md`. Every check named in `monospace` below is one of the 27.

**AMENDMENT BANNER (2026-07-30, post-verifier — see `CORRECTION_LAYER.md`):** the blind
adversarial pass (`VERIFIER_REPORT.md`, 14/14 own-construction checks incl. two
counter-probes) returned **PASS-WITH-REQUIRED-AMENDMENTS**; AM-1, AM-2 (required) and
AM-3 (minor) are applied throughout this record. **No pre-amendment COMPUTED claim
changed** — both required amendments complete stated CONDITION SETS on the
massive-landing leg, both in the CUTTING direction (the massive class is NARROWER than
first stated): AM-1 = the linear m-jet admit condition restated as FULL locked-row
vanishing (the B-only formula scoped to C-FREE members; field-coupled m″ counter-witness
adopted, `AM1_VC2_field_coupled_mpp_counterwitness`); AM-2 = the GENERIC nondegeneracy
stamp g_p ≠ 0 AND ΔG = g_f·g_h − g_x² ≠ 0 (W3-degenerate members excluded) added at
every landing/lock/mass site (counter-witness adopted,
`AM2_VC1_degenerate_block_counterwitness`; the F-G3 firing — memorialized §6). Four
verifier strengthenings adopted as credited checks (`ADOPTED_*`).

**Outcome class: OG3 (mixed/conditional — the exact conditions ARE the deliverable)**,
containing an OG1-shaped leg (a massive locked class at the P1-4D λ = 0 landing, with
the lock EMERGING from the rows; M-WALL dissenting at 0; wall-data-, member- (full
locked-row condition, AM-1) and nondegeneracy- (GENERIC ΔG ≠ 0, AM-2) conditional) and
an OG2-shaped leg (the massless verdict PERSISTS at the extended
alphabet for all quadratic-at-lock responses at a_F(lock) ≠ 0). NOT OG1 outright (the
massive leg is branch-local and multiply conditioned), NOT OG2 outright (the landing
class exists), NOT OG4 (nothing at the declared grade was left open).

**Binding boundary (carried on every statement):** locking was NEVER imposed or filtered
for — every constancy statement is either an evaluation locus of the GENERAL jet-extended
rows or a DERIVED consequence (two lock-emergence results, `G2_lock_emergence_derived_
not_imposed` and `G2_nonconstant_admitted_characterized`(b), where the rows themselves
force λ′ ≡ 0) (F-G2); both temptation directions are computed and on the record — the
massive leg carries its own cutting conditionalities (supplied-parity collapse, the full
locked-row member condition [AM-1], M-WALL = 0 dissent, p0 ≡ 0 degeneracy typed OPEN,
GENERIC nondegeneracy ΔG ≠ 0 [AM-2]) and the massless
legs are stated with equal precision (F-G1); full stamps travel (census branch, jet
order, pairing, stratum, background, mass branch, alphabet — nondegeneracy stamp added
post-verifier, the ONE F-G3 firing, §6) (F-G3); the odd-parity
forcing is carried WITH derived consequences (lock-at-zero; wall-slot parity kill;
witness-parity conditionality) (F-G4); no spectra/forces/particle language (F-G5); no
bank contradiction — the Slice-2b massless theorem's own alphabet + a_F ≠ 0 stamps are
exactly what scope this result around it (F-G6); no symbolic failure (F-G7: 27/27,
exit 0).

**Standing scope stamps (travel with every statement):** FIELD-moduli census (BR-M) on
the Route-D-REGISTERED alphabet (a851028: N1/N2/N3; anchored-exponent rule — p0 only
through e^{a·p0}, bare p0 excluded; nonlocal ∫m and absolute-point evaluations
alphabet-illegal; K₄ characters extended to jets pointwise — (λ, k_mod) trivial,
(k10, C) χ-graded); registered positive triangular chart; registered stationary
one-parameter presentation, fields (φ, f, bh) jets ≤ 2, cell x ∈ [−ℓ, ℓ]; density m-jet
order m, m′, m″ (higher jets TYPED); enumerated pairing branches (P1-4D a_F = 2λ,
P1-triad a_F = 1+2λ, P2 a_F = 0) — on the field census a_F = a_F(λ(x)) is
CONFIGURATION-DEPENDENT; banked odd-parity forcing (Route P ea5d8a3, premise ladder
P0+P1(+P2)): λ(x), k_mod(x) mirror-odd, wall values vanish; f/bh parities SUPPLIED
(both directions carried); quadratic-class generating density where instantiated;
GENERIC + KMOD0-level-set strata (the banked k_mod = 0 identity is pointwise-binding at
level-set points and IDENTICALLY VACUOUS on the field-sector sub-census containing every
member used here — Slice-2b TE4, cited); bootstrap lens (backgrounds explored;
self-consistent points reported; no background-fixed eliminations); mass branches =
the four banked LABELED definitions only (M-GEN / M-WALL / M-DENS-coord / M-DENS-proper),
none promoted.

---

## 0. Premises (chose or derived — stamped)

| Premise | Tag |
|---|---|
| Registered alphabet N1/N2/N3, exclusions, gauge law, K₄-jet characters, A1-seat definition | DERIVED input (Route D a851028; `G0_footing_recomputed` consistency) |
| Odd-parity forcing ε_λ = ε_kmod = −1 on the field census; k10 branch-split; C 2+2 | DERIVED input (Route P ea5d8a3; P0+P1(+P2) ladder travels; k10/C supplied remainder) |
| Pointwise rows = the field-census bookkeeping | DERIVED input (38577c9 reduction theorem) |
| Slice-2b atlas machinery, mass-branch identities, massless theorem WITH alphabet stamp | DERIVED input (d110fe0; machinery reused verbatim-pattern) |
| Pairing branches a_F = 2λ / 1+2λ / 0; anchored weight W_F = e^{a_F p0} | DERIVED input (Stage-3); on the field census a_F(λ(x)) handled exactly (`G1_configuration_dependent_weight_rows`) |
| f/bh wall parities | SUPPLIED (banked tag; carried BOTH ways — `G2_witness_parity_conditionality`) |
| Witness profiles (affine f/h; κ·sin(πx/ℓ) odd modulus; β·x tuned branch) | FREE exact witnesses (chosen for exact integrability + exact parity; alphabet-legality stated per use) |
| Continuity of moduli fields; polynomial-coefficient splits; Picard | Category-A (named where used) |
| SymPy exact, CPU, single process | Category-A conditioning |

## 1. TG-1 — the jet-extended pointwise moduli-row system (general form)

- **The row system, arbitrary response** (`G1_jet_rows_and_wall_slots_identity`, zero
  residual at fully arbitrary Function S(p0,p1,f0,f1,h0,h1,m,m′,m″)): the variation
  integrand decomposes EXACTLY as δS = Σ_a E_a(S)v_a + R_μ v_μ + Dx(Θ_ext) with

      R_μ = ∂_m S − Dx ∂_{m′}S + Dx² ∂_{m″}S        (the pointwise moduli row —
                                                      a DIFFERENTIAL condition in m(x))
      Θ_ext = Σ_a π_a v_a + (∂_{m′}S − Dx ∂_{m″}S)·v_m + ∂_{m″}S·v_m′

  — the Route-D-typed A1-seat content made explicit: on the registered alphabet the
  pointwise moduli row is the full 2nd-order Euler operator, and the wall block carries
  the **N3 moduli slots** (the J05 IBP leg extended to m″). Same operator form per
  sector; (k10, C) argument legality χ-graded (cited); jets beyond m″ typed.
- **The configuration-dependent weight — the named crux, exact**
  (`G1_configuration_dependent_weight_rows`): with λ(x) a field, W_F = e^{a_F(λ(x))p0}
  gives each FIELD row exactly ONE new term versus the constant-moduli rows:
  E_a(full) − E_a(const-form) = −W_F·a_F′(λ)·λ′·p0·(momentum density of a), zero
  residual — the weight's configuration dependence enters the field equations only
  through λ′, and therefore VANISHES on any locked interior. STRENGTHENED
  (verifier-credited, `ADOPTED_weight_general_rule`): for an ARBITRARY no-m-jet
  response S(u-jets, λ) the field-row difference is exactly −λ′·∂²S/∂λ∂u′ — ONE
  structural term, member-general; the anchored-member term above is that rule's
  anchored instance (it really is the only new term on the class). The λ-row of the
  no-jet generated member stays the algebraic density a_F′·p0·W_F·L̃ (pointwise); the
  banked T4 blindness loci become level sets λ(x) = 0. The k_mod (and k10, C) rows are
  IDENTICALLY VACUOUS on the no-jet generated class — those moduli are FREE directions
  there (an honest degeneracy, reported, not filtered).
- Per-branch instantiation + ledger: `G1_row_system_per_branch_ledger` [guard] →
  `JET_ROWS_LEDGER.tsv` (7 rows: branch × sector × response sub-class, with row form,
  locked row, locking verdict, mass columns, stamps).

## 2. TG-2 — the interior-locking adjudication (GENERAL system; nothing imposed)

### 2.1 Two structure theorems that organize the whole adjudication

- **Lock-reduction theorem** (`G2_quadratic_jet_terms_vanish_at_lock`, arbitrary
  Function coefficients incl. cross λ′k_mod′ terms): every response term whose m-jet
  dependence is quadratic-or-higher at m′ = m″ = 0 contributes ZERO to every row at the
  lock locus. CONFIRMED AND EXTENDED (verifier-credited,
  `ADOPTED_lock_reduction_extended_set`): all nine λ/k_mod jet quadratics — including
  the k_mod″-carrying cross terms (k′_mod², k′_mod·k″_mod, k″_mod², λ′k″_mod, λ″k′_mod)
  the representative set omitted — also vanish at the lock; the theorem is sound as
  stated (each row term retains ≥ 1 m-jet factor). **Consequence: for the entire
  sub-class of registered responses with no
  linear m-jet term, the locking adjudication reduces EXACTLY to the no-m-jet-alphabet
  adjudication.** The jet extension acts on the NONCONSTANT sector instead (§2.4).
- **The locked row, general closed form** (`G2_locked_row_general_form`): for
  S = W_F(L̃_G + B·m′ + C·m″), G_λ|lock = a_F′p0W_F L̃_G − Dx(W_F B)|lock +
  Dx²(W_F C)|lock, with only the FIELD-chain part of Dx surviving:
  Dx(W_F B)|lock = W_F(a_F p1 B + B_{f0}f1 + B_{h0}h1 + B_{f1}f2 + B_{h1}h2).
  Pure-moduli coefficients are lock-inert; pure-moduli linear-m″ terms are
  null-reducible to quadratic (`G2_mpp_null_reduction`) hence lock-inert too. Linear
  FIELD-coupled jet terms reach the locked row — the member-conditional layer (§2.3).

### 2.2 What the parity forcing actually implies (derived, not assumed)

(`G2_parity_lock_at_zero`) A mirror-odd field's wall value solves v = −v ⟹ v = 0
exactly; the cell interior (−ℓ, ℓ) is connected with closure reaching the walls, so an
interior-constant continuous odd field is ≡ 0 on the whole cell (mirrored-quotient
reading identical — continuity to the crease pins the constant): **for the (λ, k_mod)
sector, interior locking is locking AT ZERO — no other locked value exists on this cell
topology.** Per-sector: λ, k_mod forced (P0+P1(+P2)); k10 per supplied branch (odd on
(a), even+shear on (b)); C two odd + two even combinations (supplied calibration).
Also solved exactly and load-bearing below: an affine field odd about both walls is
killed entirely; even about both walls loses its slope.

Locking λ at 0 lands the pairing weight at a_F(0) — and here the branches SPLIT exactly
(`G0_footing_recomputed`, the Route-P A1 distinction carried): P1-triad a_F(0) = 1 ≠ 0;
P1-4D a_F(0) = 0, with a_F′ = 2 ≠ 0 on both (the row never vanishes by
pairing-relativity).

### 2.3 The adjudication per branch (locked sector)

- **P1-triad — ADMITTED, and only massless** (`G2_P1triad_lock_massless`): at the
  locked value the banked quadratic atlas applies (a_F = 1); the pointwise row
  2E0·p0(x) = 0 forces **E0 = 0 exactly** (the Slice-2b leg re-derived at the locked
  value), and the p0 ≡ 0 escape is independently killed by the p-row itself
  (a_F·L̃_fh = 0 at a_F ≠ 0). CONFIRMED via the on-shell identity (verifier-credited,
  `ADOPTED_triad_E_density_identity`): E-density = W_F·L̃ on the quadratic class, so
  the locked λ-row a_F′·p0·W_F·L̃ IS "2·p0·(E-density)" — the 2E0·p0(x) reading holds
  independently of the atlas citation. Locked survivors = {E0 = 0}: definite sub-class =
  constants; indefinite carries nonconstant E0 = 0 members (banked witness cited).
- **P1-4D — ADMITTED, with a massive class at the landing**
  (`G2_P14D_landing_affine_forced`): at the locked value the weight is W_F ≡ 1; the
  field rows FORCE the affine atlas u″ = 0 (**GENERIC unique solve — NONDEGENERACY
  STAMP [AM-2]: g_p ≠ 0 AND ΔG = g_f·g_h − g_x² ≠ 0, equivalently W3-degenerate
  members excluded; at ΔG = 0 the forcing FAILS — adopted counter-witness
  `AM2_VC1_degenerate_block_counterwitness`: at g_f = g_h = g_x = 1 the kernel
  direction f″ = 1, h″ = −1 solves the locked f/h rows, so the affine atlas is NOT
  forced there**); the pointwise λ-row
  2p0·L̃_G = 0 with p0 affine splits EXACTLY (polynomial coefficients): {L̃_G = 0 —
  definite: constants, massless} ∪ {p ≡ 0 with f, h affine FREE — E0 = L̃_fh(f1,h1)
  unconstrained}. This is precisely the a_F = 0 slot Route P A1 stamped UNDERIVED
  (banked atlas + I_p certificate presuppose a_F ≠ 0) — now DERIVED (generically).
- **LOCK EMERGENCE — the F-G2 discharge** (`G2_lock_emergence_derived_not_imposed`):
  on the p ≡ 0 class with λ(x) left COMPLETELY FREE, the p-row evaluates to
  2λ(x)·L̃_fh — wherever L̃_fh ≠ 0 the equations THEMSELVES force λ(x) ≡ 0. The lock is
  a CONSEQUENCE on this class, never an input. k_mod(x) stays a free odd direction
  (vacuous row — degeneracy reported). Rides the GENERIC nondegeneracy [AM-2] (the
  affine atlas behind the class: g_p ≠ 0, ΔG ≠ 0). EVERYWHERE-OR-NOWHERE
  (verifier-credited, `ADOPTED_everywhere_or_nowhere_forcing`): on this class L̃_fh is
  CONSTANT (Dx L̃_fh = 0 exactly at f″ = h″ = 0), so the forcing is
  everywhere-or-nowhere — either E0 = 0 (massless stratum, λ free) or λ(x) ≡ 0 on the
  WHOLE cell: no partial-interior plateau at λ ≠ 0 coexists with E0 ≠ 0 (the
  nonzero-plateau loophole on the massive class is CLOSED).
- **The massive locked witness, all rows** (`G2_massive_locked_witness_all_rows`):
  p ≡ 0, f/h affine, λ ≡ 0 (emerged), k_mod = κ·sin(πx/ℓ) (exactly odd about both
  walls): all five rows zero-residual; conserved E = L̃_fh(f1, h1), symbolic,
  generically nonzero (positive on the definite sub-class). **Honest degeneracy
  stamps:** the depth field is IDENTICALLY at the seal value (p0 ≡ 0) — completion/
  canon admissibility typed OPEN, not claimed; k_mod, k10, C row-unconstrained.
  **Nondegeneracy stamp [AM-2]:** the class sits on the GENERIC affine atlas —
  g_p ≠ 0 AND ΔG = g_f·g_h − g_x² ≠ 0 (W3-degenerate members excluded).
- **Cutting conditionality — the attack on the tempting leg, computed**
  (`G2_witness_parity_conditionality`): the class's energy rides the affine slopes and
  the f/bh parities are SUPPLIED: odd (both walls) kills the profile entirely; even
  kills the slope; **either definite supplied parity on both fields collapses E0 to 0.
  The massive locked class is nonempty exactly when the supplied f/bh wall data leave a
  slope free.** The mass is CONDITIONED on the supplied wall structure — first-class.
- **The linear-jet conditional layer, witnesses both ways**
  (`G2_linear_jet_conditional_layer`): the locked row gains −(B_{f0}f1 + B_{h0}h1 + …)
  (G2b). Obstructing witness B = f0: locked row = −f1 ⟹ cuts the massive class to
  f1 = 0. Admitting witness B = h1f0 − f1h0: directional derivative vanishes on the
  affine atlas — all five rows zero on the SAME massive witness. **EXACT GENERAL
  CONDITION (restated per AM-1 — FULL locked-row vanishing, from G2b):
  [a_F′·p0·W_F·L̃_G − Dx(W_F B) + Dx²(W_F C)]|lock = 0 along the locked solution (on
  the p ≡ 0 landing the first term vanishes, leaving [−Dx(W_F B) + Dx²(W_F C)]|lock
  = 0). For C-FREE members this reduces to the previously stated
  (f1∂_{f0} + h1∂_{h0} + f2∂_{f1} + h2∂_{h1})B + a_F p1 B = 0 — that formula is
  complete ONLY for m′-linear content.** Field-coupled m″ content reaches the locked
  row through Dx²(W_F C)|lock — adopted counter-witness
  (`AM1_VC2_field_coupled_mpp_counterwitness`): S = W_F(L̃_G + (f0²/2)m″) has B = 0
  (the B-only condition vacuously satisfied) yet locked λ-row = f1² ≠ 0 on the
  massive witness — it CUTS the massive class to f1 = 0. At the extended alphabet the
  adjudication is MEMBER-CONDITIONAL with the exact condition = the full locked-row
  vanishing (cutting-direction completion: the massive class's condition set is
  narrower than first stated).
- **P2** — λ-row vacuous (a_F′ = 0): locking trivially admitted; moduli free; banked
  P2 column unchanged (cited).

### 2.4 The converse: nonconstant m(x) admitted behaviors (characterized, not filtered)

(`G2_nonconstant_admitted_characterized`) (a) FREE-DIRECTION class: on constant-field
backgrounds with L̃0 = 0, arbitrary odd λ(x) (and k_mod(x)) solve all rows — nonconstant
moduli ADMITTED, E = 0 (row-degenerate, massless). (b) Jet-quadratic member
S = W(L̃_G + cλ′²/2) on constant-field backgrounds: the p-row carries the exact factor
λ·λ′² — combined with the λ-row this forces λ′ ≡ 0, and parity pins λ ≡ 0: **for this
member class the full system FORCES the lock** (second emergence result). (c) The p ≡ 0
tuned branch λ = βx: admitted iff L̃_fh = −cβ²/2, and there the EXTENDED energy is
E_ext = 0 exactly (massless under M-GEN(ext)); in-cell parity kills it anyway (β = 0).
On parity-legal configurations this member's admitted behaviors collapse to the locked
ones.

## 3. TG-3 — mass status per solution class (availability derived; branch labels)

- **M-GEN AVAILABLE on the m-jet alphabet — derived**
  (`G3_extended_energy_first_integral`, arbitrary Function): the Ostrogradsky-form
  E_ext = Σ_a u′∂_{u′}S + m′(∂_{m′}S − Dx∂_{m″}S) + m″∂_{m″}S − S obeys
  Dx(E_ext) = −Σ u′E_a − m′R_m IDENTICALLY: conserved on the full field-census shell.
  M-GEN = 2ℓE_ext; reduces to the banked E on locked solutions. NV: no generator
  (banked refusal inherited).
- **M-WALL** (`G3_MWALL_N3_slots_parity`): the wall block carries the derived N3 moduli
  slots; **the odd-sector v_m slots are PARITY-KILLED at the variation level** (v = −v
  solve — exactly parallel to the banked v_p kill), the v_m′ slot survives; k10/C per
  supplied branch; all moduli slots identically vacuous on the no-jet generated class.
  The p-slot reading persists; on the massive locked witness [π_p] = 0.
- **The masses per locked class** (`G3_masses_per_locked_class`, same-solution):
  - P1-triad locked {E0 = 0}: **M-GEN = M-WALL = M-DENS-coord = M-DENS-proper = 0** —
    massless under all four labeled branches.
  - P1-4D locked landing class: V = ∫W_F dx = 2ℓ exactly (W ≡ 1);
    **M-GEN = M-DENS-coord = M-DENS-proper = 2ℓE0** with E0 = L̃_fh generically ≠ 0;
    **M-WALL = 0** — three of four branches read the same nonzero mass, M-WALL dissents
    at 0, consistent with the banked divergence law M-WALL = a_F·M-GEN at a_F = 0.
    Conditionality stamps travel (free wall data; the FULL locked-row member condition
    [AM-1]; GENERIC nondegeneracy g_p ≠ 0 & ΔG ≠ 0 [AM-2]).
  - P2: banked column unchanged (M-GEN free, M-WALL = 0).
- **The Slice-2b comparison, exact** (`G3_slice2b_comparison_record` [guard]): the
  banked massless theorem is stamped no-moduli-jet alphabet + a_F ≠ 0. This push
  **(i) EXTENDS it at the registered m-jet alphabet** — massless persists for every
  quadratic-at-lock response at a_F(lock) ≠ 0 (member-conditional under linear m-jet
  content, condition = the full locked-row vanishing [AM-1]); **(ii) POPULATES the
  premise-failure slot it explicitly
  did not cover** (the a_F = 0 landing, reached exactly BY the parity forcing on
  P1-4D). Neither leg is a supersession: no banked statement is contradicted — the
  banked stamps did their job. The banked INTEGRATED-branch (constant-census) results
  are untouched (not this push's domain).

## 4. TG-4 — wall behavior (typed) — `G4_wall_behavior_typing` [guard]

λ, k_mod vanish at both walls (with even jets; odd jets free there). Wall-localized
m-variation: nonzero odd profiles are plateau-with-transition-layer shaped; for no-jet
members such profiles have no row dynamics on the degenerate strata and are FORBIDDEN on
the massive p ≡ 0 class (λ ≡ 0 forced everywhere); for jet-carrying members the layer
obeys the derived row ODEs — general layer profiles TYPED (solution-level work beyond
scope). N3 wall slots: odd-sector v_m slots parity-killed; v_m′ survives; k10/C per
supplied branch. Corners/completion inherited TYPED.

## 5. TG-5 — implication map + stop-clause

`G5_decision_map_and_stop_clause` [guard]; full text in `DECISION_SURFACE_UPDATE.md`.
Stop-clause (honest): the finding is NOT merely confirmatory — flagged to Charles;
assessment CONTINUE-WITH-FLAG (step (2) supplies exactly the data this result is
conditioned on); the stop decision is Charles's.

## 6. Falsifier record (derivation-side)

- **F-G1 (double-temptation steering): not fired — structure audit, verifier-confirmed
  both directions.** The tempting
  outcome (locking-with-mass) was reached ONLY on one branch's landing class, and the
  same package computes every cutting condition against it: the supplied-parity
  collapse (`G2_witness_parity_conditionality`), the obstructing linear-jet witness
  (`G2_linear_jet_conditional_layer`) with the full locked-row condition and the m″
  counter-witness [AM-1], the M-WALL = 0 dissent, the p0 ≡ 0
  degeneracy typed OPEN, and the GENERIC nondegeneracy stamp [AM-2]. The massless legs
  (P1-triad; quadratic-at-lock reduction;
  the tuned nonconstant branch's E_ext = 0) are derived with equal precision. No step
  was selected for the outcome it favors: the branch split falls out of a_F(0) per the
  banked weight menu. (Verifier: no over-cut found in the inverse direction either —
  the admitting witness and the free-wall-data nonemptiness condition are on record.)
- **F-G2 (locking imposed): not fired** — locking enters only as an evaluation locus of
  general rows, and on the load-bearing classes constancy is DERIVED (two independent
  emergence results: the p-row forcing λ ≡ 0 on the p ≡ 0 class; the jet-quadratic
  member forcing λ′ ≡ 0 on constant-field backgrounds). No diagnostic filters for
  locked solutions; the nonconstant sector is characterized in the same package.
- **F-G3 (scope stamps — NINTH-catch watch): ONE FIRING = AM-2, MEMORIALIZED WITH ITS
  DIRECTION.** The landing/lock claims rode an UNSTAMPED nondegeneracy premise
  (ΔG = g_f·g_h − g_x² ≠ 0; g_p was declared, ΔG was not) — a missing
  member-class/stratum stamp of exactly the named scope class, caught by the
  verifier's counter-computation (VC1: at ΔG = 0 the affine atlas is NOT forced —
  kernel direction f″ = 1, h″ = −1), now adopted in-package
  (`AM2_VC1_degenerate_block_counterwitness`). **The NINTH catch of the named scope
  class (ordinal continues Route P's EIGHTH), CUTTING-direction — the second
  named-class catch resolved AGAINST the massive/tempting side** (the omission had
  let the massive-landing claims read broader than derived; the stamp NARROWS the
  massive class's scope — the anti-inflation discipline held; a stamp defect, not a
  steering artifact). Corrected at every site (G2e/G2f/G2g/G3c details, ledger
  JR1/JR5, `DECISION_SURFACE_UPDATE.md`); "unique solve" scoped GENERIC. All other
  stamps (census branch, jet order, pairing, stratum, background, mass branch,
  alphabet) were hunted and found present; the landing result is stamped to its
  branch, its response sub-class, its supplied-data conditions, its degeneracies, and
  now its nondegeneracy.
- **F-G4 (parity dropped): not fired** — the forcing is carried WITH derived
  consequences (lock-at-zero; the a_F(0) landing; the N3 v_m parity kill; the witness
  parity conditionality both ways; the β = 0 parity cut on the tuned branch).
- **F-G5 (physics language): policed** — structure-only wording throughout.
- **F-G6 (bank contradiction): none found** — Slice-2b, Route D, Route P, and the
  reduction theorem are recomputed or cited with stamps intact; the landing class lives
  exactly in the slot the bank marked underived.
- **F-G7 (symbolic failure): none** — 27/27, exit 0, byte-identical reruns ×3
  post-amendment (21/21 ×2 pre-amendment; the verifier's independent script 14/14).

**Limits that travel:** (i) computational legs instantiate the quadratic-class
generating density (the banked census representative class); the general theorems
(G1a, G2a, G2b, G3a) are arbitrary-Function and member-general; (ii) density m-jets
carried to m″, higher jets typed; the (k10, C) sector rides the identical operator form
+ χ-graded legality citation, with its rows vacuous BY INSPECTION (zero dependence) on
the member classes used — not instantiated as jet chains [AM-3]; (iii) the massive
landing class is conditioned on: free f/bh wall data, the FULL locked-row member
condition [AM-1] (the B-only formula is its C-FREE instance; field-coupled m″ content
cuts via Dx²(W_F C)|lock), GENERIC nondegeneracy g_p ≠ 0 & ΔG = g_f·g_h − g_x² ≠ 0
(W3-degenerate members excluded) [AM-2], completion-admissibility of p0 ≡ 0 (typed
OPEN), and the P0+P1(+P2) parity ladder; (iv) NV cells: only the banked refusals
inherited — no new NV
derivation; (v) the nonconstant sector is characterized on named background classes
(constant-field, p ≡ 0); general nonconstant field × nonconstant moduli coupled
solutions are TYPED beyond the witnesses given; (vi) wall-layer solution profiles typed
(TG-4); (vii) blind verifier pass RUN (2026-07-30, same-session-spawned — caveat
travels): **PASS-WITH-REQUIRED-AMENDMENTS** (`VERIFIER_REPORT.md`, independent script
14/14 preserved); AM-1/AM-2/AM-3 applied per `CORRECTION_LAYER.md`; same-verifier
closure on the restatements owed before the driver banks (multi-round precedent).
