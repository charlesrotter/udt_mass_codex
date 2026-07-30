# BLIND ADVERSARIAL VERIFIER REPORT — P4 gradient seat (`udt_p4_gradient_seat_2026-07-29`)

Date: 2026-07-30. Verifier: blind adversarial, **same-session-spawned** (zero prior
context supplied beyond the dispatch; the standing caveat travels: this is NOT a hosted
external model — it is a separately-prompted agent of the same driver session, so
same-model correlated blind spots are possible; treat as the strongest *available*
independence, not absolute independence). Contract: `PREREGISTRATION.md`, verified
contract-first in git (9bc5cf5, 2026-07-29, commits ONLY the preregistration; all
derivation artifacts postdate it, 2026-07-30). Independent script:
`VERIFIER_INDEPENDENT_CHECK.py` (own jet layout, own total-derivative/Euler operators,
functions-of-x spot routes, plus two adversarial counter-computations) — 14/14, exit 0,
2.9 s; stdout preserved (`VERIFIER_INDEPENDENT_STDOUT.txt`). Framing: ADJUDICATE, not
confirm; the locking-with-mass leg attacked hardest per the contract's F-G1 duty.

## VERDICT: **PASS-WITH-REQUIRED-AMENDMENTS** (AM-1, AM-2 required; AM-3 minor)

Every computed claim I re-derived independently is CORRECT (no refutation anywhere;
no check of the 21 is false; no smuggled constancy; no bank contradiction). The two
required amendments are scope/stamp completeness defects on the massive-landing leg —
both in the CUTTING direction (they narrow the massive class's stated conditions), so
neither rescues nor inflates the tempting outcome; the outcome class OG3 stands.

## Duty 0 — rerun / determinism / contract

- `derive_gradient_seat.py`: exit 0, 21/21; **byte-identical stdout across two reruns**
  and identical to the committed `DERIVATION_STDOUT.txt`; `gradient_seat_results.json`
  and `JET_ROWS_LEDGER.tsv` regenerate identically. Runtime 2.3 s (bound respected).
- Exact SymPy throughout: no floats, randomness, network, numeric solvers, GPU
  (grepped; `sp.solve` symbolic only).
- **17 substantive + 4 guards audited**: the 4 guards
  (`G1_row_system_per_branch_ledger`, `G3_slice2b_comparison_record`,
  `G4_wall_behavior_typing`, `G5_decision_map_and_stop_clause`) are always-True
  recording/typing rows, labeled `[guard]` in-script, in stdout, and in the JSON
  `kind` field — honestly split, never presented as residual computations.
- Contract-first: 9bc5cf5 contains PREREGISTRATION.md alone. VERIFIED.

## Duty 1 — the massive-landing leg (attacked hardest)

Independently re-derived, own formalism (V4, V5, V6, V8, V12 + counter-probes):

- **Affine atlas forced at a_F = 0** (V4): confirmed as a GENERIC solve — but see
  **AM-2**: at ΔG = g_f·g_h − g_x² = 0 the forcing FAILS (counter-computation VC1:
  g_f = g_h = g_x = 1 admits f″ = 1, h″ = −1). Nondegeneracy is nowhere declared.
- **The exact split** {L̃_G = 0} ∪ {p ≡ 0, E0 = L̃_fh free}: confirmed (polynomial
  coefficients of 2(p00 + p1·x)·L̃_G; L̃_G constant on the affine atlas so the split is
  exhaustive there).
- **Lock emergence (F-G2)**: GENUINE. Re-derived on the functions-of-x route with
  λ(x) an ARBITRARY sympy Function (V5): the first variation in p about p ≡ 0 on the
  affine class is exactly 2λ(x)·L̃_fh·v_p(x) with no boundary piece — the rows
  themselves force λ(x) ≡ 0 wherever L̃_fh ≠ 0. No ansatz smuggles constancy: λ enters
  as a free field; the p ≡ 0 class is itself a derived branch of the exact split, and
  its use is class-stamped. **Scoping of "wherever E0 ≠ 0" is exact**: on this class
  L̃_fh is constant (f, h affine), so the forcing is everywhere-or-nowhere — which also
  closes the nonzero-plateau loophole on the massive class (no partial-interior lock
  at v ≠ 0 coexists with E0 ≠ 0). The second emergence result (jet-quadratic member,
  V10: p-row factor λ·λ′², lock forced with continuity) also confirmed.
- **Masses** (V6, V12): all five rows zero on the witness; E = L̃_fh symbolic,
  generically nonzero; V = 2ℓ; M-GEN = M-DENS-coord = M-DENS-proper = 2ℓE0;
  M-WALL = [π_p] = 0 at p1 ≡ 0 — **consistent with the banked divergence law
  M-WALL = a_F·M-GEN at a_F = 0** (Slice-2b `TE2_MWALL_theta2_and_pslot` +
  `TE2_MWALL_P2_zero` re-read; the banked a_F = 0 facts — affine atlas forced,
  M-WALL ≡ 0 while M-GEN free — match the landing structure exactly).
- **Cutting conditions**: (a) supplied-parity collapse confirmed (V7); (b) linear-jet
  member condition — see **AM-1**: the stated formula is B-only and incomplete for
  field-coupled m″ content (counter-witness computed); (c) M-WALL = 0 dissent
  confirmed; (d) **p0 ≡ 0 honestly typed OPEN** — I hunted the bank for an
  admissibility statement on depth-identically-at-seal-value configurations: none
  found either way (Slice-2's regularity/nodeless results concern the nonconstant
  atlas; the completion layer J07/J08/J11 is typed OPEN in the bank) — OPEN is the
  correct type, and it is not glossed anywhere in the package; (e) the k_mod/k10/C
  free-direction degeneracy is reported, not hidden. With AM-1/AM-2 applied the
  condition list is complete at the declared jet order and member class.

## Duty 2 — the parity-geometry reading

- Route P (ea5d8a3) banks, field census: "λ(x), k_mod(x) forced ODD **about the
  wall**"; CANON (C-2026-06-10-2 + C-2026-07-04-1) places the mirror fold AT the
  seal/wall with the odd sector ⟹ Dirichlet-0 at the crease. So odd-under-mirror ⟹
  wall value 0 at each mirrored wall — the script's v = −v solve is the right reading.
- The implication (interior-constant continuous odd field ≡ 0) needs: connected
  interior whose closure reaches at least one odd-mirrored wall. In the registered
  one-parameter presentation the cell is an interval [−ℓ, ℓ] — premise holds; the
  mirrored-QUOTIENT reading (continuity to the crease pins the constant) is also
  stated and correct. The package itself names the only escape topology (an interior
  component not reaching a wall) and correctly notes none exists in this
  presentation; higher-dimensional/corner topologies stay TYPED (TG-4/completion).
  **No cell topology within the banked scope supports locking at a nonzero value.**
  The premise carries — VERIFIED as scoped. (Sub-interval plateaus at v ≠ 0 are not
  excluded by parity alone, but are disposed of honestly: forbidden on the massive
  class by the everywhere-forcing above; free directions on E0 = 0 strata; layer
  ODEs typed — TG-4.)

## Duty 3 — lock-reduction theorem + configuration-dependent weight

- **Lock-reduction**: confirmed AND extended (V3): my quadratic set adds the
  k_mod″-carrying cross terms the package's representative set omitted
  (k′_mod², k′_mod·k″_mod, k″_mod², λ′k″_mod, λ″k′_mod) — all rows still vanish at
  the lock. The theorem is sound as stated (each row term retains ≥ 1 m-jet factor).
- **Configuration-dependent weight**: confirmed and STRENGTHENED (V2): for an
  ARBITRARY no-m-jet response S(u-jets, λ) the field-row difference is exactly
  −λ′·∂²S/∂λ∂u′ (one structural term, general rule); the package's single-term
  −W_F·a_F′·λ′·p0·(momentum) is its anchored-member instance. It really is the ONLY
  new term on that class; λ-row algebraic; k_mod row vacuous — all confirmed.

## Duty 4 — alphabet legality + (k10, C) carry

- **B = f0 (obstructing) and B = h1·f0 − f1·h0 (admitting)** both re-derived on the
  witness (V8: locked row −f1; all five rows zero, respectively). Legality against
  Route D (a851028): local jet arguments only (no anchored nonlocal ∫m; no
  absolute-point/wall evaluation) — both exclusions pass; anchored-exponent rule
  (bare p0 excluded) — no p0 argument in either B; f0/h0 as response arguments are
  banked-legal (Slice-2b's own general member is `Ltil(p0, p1, f0, f1, h0, h1)`).
  The χ-grading constrains the (k10, C) sector per Route D; (λ, k_mod) is the
  trivial-character sector — the legality claims check out.
- **(k10, C) carry**: the identical-operator-form citation is legitimate (the G1a
  identity is modulus-generic) and the carry is DECLARED in the header — not a
  silent scope reduction (F-G3 does not fire on it). But see **AM-3**: "rows
  computed vacuous" overstates — k10/C are never instantiated as jet chains in the
  script; their vacuousness on the members used is by-inspection (zero dependence),
  true but not computed.

## Duty 5 — the Slice-2b comparison

- The banked pointwise massless theorem's stamps re-read at source: NO-moduli-jet
  response alphabet (Route D §4 records the stamp verbatim) + the a_F ≠ 0 atlas
  premise (Route P A1-corrected: "premise FAILS under P1-4D — UNCERTIFIED, not
  refuted; a_F′ vs a_F distinction"). The package's two legs are exactly right:
  (i) EXTENDS at the m-jet alphabet via the lock-reduction theorem + G2d (persists,
  member-conditional under linear-jet content); (ii) POPULATES the a_F = 0 slot —
  and it does NOT quietly convert Route P's UNCERTIFIED into a derivation: the chain
  is stated explicitly ("exactly the slot Route P A1 stamped UNDERIVED … now
  DERIVED") in G2e, in EXACT_DERIVATION §2.3, and in the comparison record, and the
  seat it runs is exactly Route D's A1-seat "DEFINED, not run". Neither leg is a
  supersession — no banked statement contradicted (F-G6 clean; the Slice-2b a_F = 0
  P2-side facts independently match the landing structure).
- The P1-triad leg (duty-1 equal-care question): its in-script sub-checks are
  partly definitional (E0_from_A is circular by construction of A_G), and the main
  E0 = 0 forcing leans on the banked citation — but the load-bearing escape
  (p ≡ 0 with E0 free) IS genuinely computed and killed (p-row = a_F·L̃_fh ≠ 0
  route), and I independently confirmed the "2E0·p0(x)" reading via the on-shell
  identity E-density = W·L̃ on the quadratic class (V11). The exclusivity leg is
  sound; suggest (non-blocking) the word "re-derived" there be read as
  "banked-leg cited + escape independently killed".

## Duty 6 — falsifier hunts

- **F-G3 (FIRST, ninth-catch watch): ONE FIRING = AM-2.** The landing/lock claims
  ride an UNSTAMPED nondegeneracy premise (ΔG ≠ 0; g_p is declared, ΔG is not) —
  a missing member-class/stratum stamp of exactly the named scope class, caught by
  counter-computation (VC1). Direction: CUTTING (a stamp that narrows the massive
  class's scope) — the anti-inflation discipline held; the omission is a stamp
  defect, not a steering artifact. All other stamps hunted (census branch, jet
  order, pairing, stratum, background, mass branch, alphabet) are present across
  ledger + prose + JSON.
- **F-G1 (steering, both directions): not fired.** The massive leg carries five
  computed cutting conditions including an obstructing witness the package itself
  built; the massless legs are computed with equal precision; the DSU's stop-clause
  argues FOR stopping as well as against; the branch split falls out of a_F(0) per
  the banked menu, not a chosen step. Inverse direction (killing the massive leg):
  no over-cut found — the admitting witness and the free-wall-data nonemptiness
  condition are both on record.
- **F-G2: not fired** — emergence verified on the general field (V5); no filter
  diagnostics found; the nonconstant sector is characterized in-package.
- **F-G4: not fired** — parity carried with derived consequences throughout
  (lock-at-zero, landing, N3 v_m kill, both-ways witness conditionality, β = 0).
- **F-G5: clean** — grepped all artifacts; only meta-references to the ban itself.
- **F-G6: clean** — Route D/P, reduction theorem, Slice-2b re-read at source; no
  contradiction; the landing lives in the slot the bank marked underived.
- **F-G7: none** — 21/21 exit 0, byte-identical ×2 (+ my 14/14).

## Duty 7 — contract compliance

TG-1..TG-5 all addressed (TG-4 honestly TYPED at solution level, as the prereg
allows). Stop-clause assessment: honest, reasons both ways, decision explicitly
Charles's — compliant. Ceiling respected: no census adopted; the fork is stated as a
MIXED map fact per pairing branch, its disposition assigned to step (3); no
dissolution/exclusivity DECLARED; no physics. Scope ladder: not needed (2.3 s);
the FULL-SCOPE claim is fair modulo AM-3's wording. `AUDIT_REPORT.md` is not yet
present — per the prereg's own method order it follows THIS pass (step 5); it must
exist before commit.

## REQUIRED AMENDMENTS

- **AM-1 (required).** The "EXACT GENERAL CONDITION" for the linear-jet conditional
  layer — (f1∂_{f0} + h1∂_{h0} + f2∂_{f1} + h2∂_{h1})B + a_F·p1·B = 0 — as stated in
  EXACT_DERIVATION §2.3, the `G2_linear_jet_conditional_layer` detail, ledger row
  JR5, and DECISION_SURFACE §1.3(b), is complete ONLY for m′-linear content.
  Field-coupled m″ content reaches the locked row through Dx²(W_F C)|lock (present
  in G2b's closed form and typed in G2j, but absent from the condition formula).
  **Counter-witness (VC2):** the alphabet-legal member S = W_F(L̃_G + (f0²/2)·m″)
  has locked λ-row = f1² ≠ 0 on the massive witness — it CUTS the massive class —
  while the stated condition is vacuously satisfied (B = 0). Fix: restate the admit
  condition as the full locked-row vanishing [−Dx(W_F B) + Dx²(W_F C)]|lock = 0
  along the locked solution, or scope the stated formula "for C-free members" at
  every occurrence. (Direction: cutting — narrows the massive class's conditions.)
- **AM-2 (required; the F-G3 firing).** Add the explicit nondegeneracy stamp
  (g_p ≠ 0 AND ΔG = g_f·g_h − g_x² ≠ 0; equivalently W3-degenerate members
  excluded) to `G2_P14D_landing_affine_forced`, `G2_lock_emergence_derived_not_
  imposed`, `G2_massive_locked_witness_all_rows`, `G3_masses_per_locked_class`,
  ledger JR1, and DECISION_SURFACE §1.2/§1.3 — and scope the "unique solve" wording
  GENERIC. **Counter-computation (VC1):** at ΔG = 0 the affine atlas is NOT forced
  (kernel direction f″ = 1, h″ = −1 solves the f/h rows). The banked
  quadratic-class atlas carries this implicitly; the landing claims must carry it
  explicitly.
- **AM-3 (minor).** Reword "(k10, C) sector … its rows computed vacuous on the
  member classes used" (script header, EXACT_DERIVATION header, limits (ii)) to
  "vacuous by inspection (zero dependence) on the member classes used; operator
  form cited" — or add the trivial computation. The current wording claims a
  computation that does not occur.

## Adjudication summary for the driver

No refutation. The doubly-tempting leg SURVIVES adversarial re-derivation on an
independent implementation — the lock genuinely emerges, the massive landing class
is real on its stated conditions, and every mass identity checks — but its
condition set was stated incompletely in two places (AM-1 formula; AM-2 stamp),
both fixable without changing any computed result or the OG3 outcome class.
Post-amendment closure by the SAME verifier is expected per the prereg
(multi-round precedent).

---

# AMENDMENT CLOSURE — same verifier, 2026-07-30

Adjudicated adversarially against the amended package (same-session-spawned blind
verifier; not-a-hosted-external-model caveat travels). **VERDICT: CLOSED.**

1. **Rerun:** exit 0, **27/27 = 23 substantive (17 original + 6 verifier-credited) +
   4 guards** (guard set unchanged by name and kind); deterministic (byte-identical
   stdout ×2, matches committed `DERIVATION_STDOUT.txt`; JSON/TSV regenerate
   identically); 3.8 s; exact SymPy only. JSON diff vs my preserved pre-amendment
   copy: **all 21 original checks survive with name/kind/pass unchanged; details
   changed at exactly the six amendment-target checks** (G2e, G2f, G2g, G2i, G2j,
   G3c) and nowhere else; the six added checks are the two counter-witnesses +
   four adopted strengthenings, all credited. Code inspection of the adopted
   blocks: `AM2_VC1` (kernel f″=1, h″=−1 at g_f=g_h=g_x=1, ΔG=0 checked explicitly),
   `AM1_VC2` (same member S = W_F(L̃_G + (f0²/2)m″), locked λ-row = f1², B ≡ 0
   confirmed via ∂S/∂m′ = 0), `ADOPTED_weight_general_rule` (−λ′·∂²S/∂λ∂u′, all
   three rows, arbitrary Function), `ADOPTED_lock_reduction_extended_set` (my nine-
   term set verbatim), `ADOPTED_triad_E_density_identity` (E-density = W·L̃ on both
   members + λ-row = a_F′p0·E-density, a legitimate extra tie),
   `ADOPTED_everywhere_or_nowhere_forcing` (Dx L̃_fh = 0 on the affine class) —
   **each reproduces my computation faithfully**.
2. **AM-1 CLOSED.** The restated condition — FULL locked-row vanishing
   [a_F′·p0·W_F·L̃_G − Dx(W_F B) + Dx²(W_F C)]|lock = 0 along the locked solution —
   is the mathematically correct general admit condition (it IS the G2b closed form
   both scripts verified at zero residual, set to zero; the λ-row is exactly what a
   locked configuration must additionally satisfy). Independently recomputed on my
   own layout at the landing (first term vanishing at p ≡ 0 confirmed):
   B = h1f0 − f1h0 → 0 (admits), C = f0²/2 → f1² (violates — my counter-witness
   correctly cuts), B = f0 → −f1 (cuts to f1 = 0). The B-only formula is retained
   ONLY as the explicitly-scoped C-free instance at every occurrence I listed
   (§2.3 detail, ledger JR5, DECISION_SURFACE §1.3(b), JSON) — verified present at
   each site.
3. **AM-2 CLOSED.** The GENERIC nondegeneracy stamp (g_p ≠ 0 AND ΔG = g_f·g_h −
   g_x² ≠ 0, W3-degenerate members excluded) present at all listed sites
   (G2e detail with "unique solve" scoped GENERIC, G2f, G2g, G3c, ledger JR1/JR5,
   DECISION_SURFACE §1.2/§1.3 and standing conditionalities); my degenerate
   counter-witness banked as a zero-residual check; the **NINTH-catch memorial**
   present in the falsifier record WITH its cutting direction (ordinal continuing
   Route P's eighth; "second named-class catch resolved against the massive/
   tempting side" — accurate).
4. **AM-3 CLOSED.** "vacuous BY INSPECTION (zero dependence) … operator form cited
   — not instantiated as jet chains" at the script header, EXACT_DERIVATION header
   + limits, and the ledger amendment row — the computation claim is gone.
5. **Did-NOT-change list verified by comparison:** OG3 (header + JSON, with the
   completed conditionality honestly folded into the outcome string); the TG-1 row
   system R_μ = ∂_m S − Dx∂_{m′}S + Dx²∂_{m″}S verbatim; the lock-emergence theorem
   with its exact "wherever L̃_fh ≠ 0" scope (now plus the adopted everywhere-or-
   nowhere leg); the triad leg; the four mass identities (M-GEN = M-DENS-coord =
   M-DENS-proper = 2ℓE0, M-WALL = 0); the EXTENDS/POPULATES comparison chain; the
   stop-clause CONTINUE-WITH-FLAG with the decision Charles's. `CORRECTION_LAYER.md`
   is faithful to my report (findings, directions, credits); `AUDIT_REPORT.md`
   faithfully records contract-first, 14/14, the emergence genuinely derived, the
   parity geometry as scoped, AM-1..3, and both catches' cutting directions.
6. **New-defect hunt: NONE FOUND.** No pass condition of the 21 originals weakened
   (load-bearing blocks inspected at code level — booleans identical to the
   pre-amendment code I read); no stamp removed; no claim upgraded beyond the
   amendments; the amendment banner and `credit` machinery do not alter the
   check-counting semantics (guards still 4, never counted substantive). Minor
   non-blocking note: ledger JR5's `row_form` column abbreviates "dB/dC-terms"
   (loose shorthand; the `locked_row` column carries the exact form) — cosmetic,
   no action required.

**CLOSED. The package is, in this verifier's judgment, ready for AUDIT_REPORT
four-check and commit; the standing caveat (same-session-spawned, not a hosted
external model) travels with both passes.**
