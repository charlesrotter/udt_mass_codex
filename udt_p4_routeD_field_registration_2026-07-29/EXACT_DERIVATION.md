# P4 Route D — exact derivation record: the field-census registration test (TD-R1..TD-R6)

> **POST-VERIFIER NOTE (2026-07-29):** blind adversarial pass returned **PASS — no
> required amendments** (`VERIFIER_REPORT.md`); the three non-blocking observations
> were adopted per `CORRECTION_LAYER.md` — two credited verifier strengthenings now
> run in-script as `ADOPTED_T2analog_bracket_pointwise` (← V7) and
> `ADOPTED_finite_level_orbit_linear` (← V2e), taking the count 36/36 → **38/38**
> (29 → 31 substantive; guards unchanged). **No computed claim, verdict, ledger
> status, or declaration of the pre-adoption package changed.**

Date: 2026-07-29. Branch: grok. Contract: `PREREGISTRATION.md` (frozen before this
derivation). Script: `derive_routeD_registration.py` — **38/38 checks, exit 0 = 31
SUBSTANTIVE zero-residual exact-SymPy checks + 7 CITATION GUARDS** (incl. the two
credited `ADOPTED_*` verifier strengthenings; guards =
definitional-unpacking / citation / typing bookkeeping, labeled `[guard]` in-script
and in the JSON, never counted as residual computations), deterministic (no floats,
no randomness, no network, no numeric solvers, no GPU; stdout AND JSON byte-identical
across reruns — verified ×2), single CPU process, well under the 75-min budget
(**FULL DECLARED SCOPE — no scope-ladder reduction taken**; both moduli sectors
derived, not only (λ, k_mod)). Outputs: `routeD_results.json`,
`DERIVATION_STDOUT.txt`, `REGISTRATION_LEDGER.tsv`, `DECISION_SURFACE_UPDATE.md`.
Every check named in `monospace` below is one of the 38.

**Binding boundary (carried on every statement):** no step selected or phrased for
the outcome it favors — the named temptation was REGISTRATION-FAILS and the result
is REGISTERS, with the failure legs hunted explicitly on the record (F-R1; §1.3,
§2.3); every obstruction candidate was DERIVED from banked structure and disposed,
none invented, and no dynamics were invented to make the registration pass — the
extended-class DEFINITION is the banked Route-D spec verbatim (F-R2; §0); full
sector + structure + stratum stamps travel with every claim (F-R3); NO parity value
is assumed anywhere — ε_m enters only as supplied data, and every mirror statement
is parity-conditional (F-R4); no contradiction with the reduction theorem, Route B,
the alphabet, the cocycle laws, or CANON was found or introduced — the S1/S4
"unregistered" stamps are provenance statements about the PRIOR bank that this
package discharges going forward, not contradictions (F-R5); no symbolic failure
(F-R6: 38/38, exit 0).

**Standing scope stamps (travel with every statement):** registered positive
triangular chart; registered stationary one-parameter presentation (the transport
parameter x is the one-parameter direction; the moduli promote to functions of it);
anchored transport E(0) = I (banked registration); off-shell typing computations;
witness instances are FREE off-shell configurations chosen for exact integrability
(a registration theorem is off-shell); both census branches carried, NEITHER adopted
— this package REGISTERS the field branch's footing, it does not select it; no mass
leg run (TD-R4 types only; Slice-2b cited as map facts with stamps intact).

---

## 0. Premises (chose or derived — stamped)

| Premise | Tag |
|---|---|
| Extended-class definition: E′ = X(x)E with founded H fixed; moduli m(x) = (λ, k_mod, k10, C)(x); K(x) lower-triangular | THEORY (banked Route-D spec, `RESIDUAL_DECISION_SURFACE.md` verbatim; census rows 11–14 fork (ii); Stage-2 BR-M row) — NOT invented (F-R2) |
| Anchor E(0) = I | THEORY (banked E02 registration, 07-25; Route B T1(a) uses the same anchored-family definition) |
| η, chart, generator conventions, K₄ list, concatenation order M₂M₁ | THEORY / DERIVED input (Route B convention copy; K₄ = Route B T1 A1-amended) |
| Witness instances: C(x) = C₀ + C₁x with K(x) = γx·E21 (mixing sector); K(x) = diag(λ(x)∓k_mod(x)) affine (seat sector); m = u² (locality witness) | FREE off-shell typing witnesses (chosen for exact integrability; alphabet-legality noted per check) |
| Picard/linear-ODE uniqueness; exp > 0; discrete-value continuity ⟹ locally constant; Im(ΛvΛ⁻¹) = Λ·Im(v) | Category-A (named calculus/linear-algebra steps, banked Slice-2/forcing precedent lane) |
| Mirror/seal action on moduli (ε_m) | SUPPLIED (F-R4; never valued — Route P's question) |
| SymPy exact, CPU, single process | Category-A conditioning |

## 1. TD-R1 — class coherence (the x-dependent members form a coherent registered class)

### 1.1 The derived gauge law is connection-type

From the banked class definition and metric equality alone: two anchored field
members present the same physical metric family g = EᵀηE iff the pointwise
comparison L(x) = Ẽ E⁻¹ is Lorentz at every x (exact identity
(LE)ᵀη(LE) − EᵀηE = Eᵀ(LᵀηL − η)E — `R1_gauge_law_metric_equality_leg`), proper
orthochronous by the anchor L(0) = I. Differentiating, the field-class
presentation/gauge law is

    X  ↦  L X L⁻¹ + L′L⁻¹        (connection-type; L′ = 0 recovers the banked
                                   constant-class conjugation law)

— DERIVED, not posited. The class-coherence question is exactly: which L(x) keep
the class stable, and does the NEW derivative term open or destroy structure.

### 1.2 Chart stability

- **Block form is stable:** for ANY field member, (XM) upper-right = H·U and
  upper-left = H·ρ identically (generic Function blocks), so M′ = X(x)M gives
  U′ = HU with U(0) = 0 ⟹ U ≡ 0 (Picard, named), and **ρ(b,a) = e^{(b−a)H} —
  member-independent: the base transport is universal (the founded H)**
  (`R1_transport_chart_stability_upper_right`).
- **Positivity is stable:** on the diagonal instance Q = diag(exp∫k00, exp∫k11)
  solves Q′ = K(x)Q with positive diagonal (`R1_instance_chart_positivity_diagonalK`);
  the x-dependent mixing instance (C(x) = C₀+C₁x, K(x) = γx·E21) has exact
  closed-form transport with the Duhamel block, zero residual
  (`R1_instance_xdep_transport_solves_ODE` — extends the banked ADOPTED Duhamel
  leg, which had K = 0, to x-dependent K).

### 1.3 The class-wide stabilizer theorem (with the failure-leg hunt)

The field-class class-wide gauge condition — B′(x) + [B(x), X] tangent to the class
for EVERY member X — is a homogeneous linear system in the 12 unknowns (B, B′) of
**rank 12: only B ≡ 0** (`R1_classwide_stabilizer_trivial_field`). The connection
term opens NO new continuous gauge. The one genuine candidate loophole was named
and killed on the record (F-R1 duty — this is where a registration could have
GAINED an illegitimate gauge or LOST coherence): the base boost L01 preserves V
under bracket (zero residual on all 7 directions), but its affine condition
a′A + a[A,H] = 0 solves to exactly a = a′ = 0 (`R1_L01_loophole_named_and_killed`).

### 1.4 The finite residual: exactly the pointwise K₄ (exhaustive)

Four exact steps, each zero-residual, no ansatz:

1. **Screen plane invariant.** S := Σ Im(v) over V = span(e₂,e₃) exactly (rank 2);
   class-preserving L(x) satisfy L V L⁻¹ = V pointwise (from member DIFFERENCES,
   where the connection term cancels), hence preserve S
   (`R1_GV_image_span_is_screen`).
2. **Block-diagonal forced.** Screen-preserving Lorentz maps decompose exactly:
   S₂ᵀS₂ = I; det(S₂)² − 1 in the ideal (Gröbner) ⟹ det S₂ ≠ 0 ⟹ W = 0 via
   adj(S₂ᵀ)S₂ᵀ = det·I; then Pᵀη₂P = η₂ (`R1_GV_blockdiagonal_forced`).
3. **Screen block signed-diagonal.** S₂ ∈ O(2) preserving K-lower-triangularity
   solves EXHAUSTIVELY (sp.solve) to the four signed diagonals
   (`R1_GV_screen_signed_diagonal`).
4. **Base block pinned WITH the connection term.** P ∈ O(1,1) with
   PHP⁻¹ − H + yA = 0 (y = the O(1,1) connection coefficient of the curve) solves
   EXHAUSTIVELY to the four signed diagonals with y = 0 — **every boost is killed;
   the connection term cannot compensate** (independent components on H, N, A);
   orthochronous keeps P ∈ {I, diag(1,−1)} (`R1_GV_base_block_pinned_connection`).

Enumeration of the surviving 8 candidates under det = +1 + orthochronicity yields
**EXACTLY the banked K₄**; each element preserves the x-dependent class pointwise
and fixes X₀ (`R1_finite_residual_is_pointwise_K4`). Since the surviving values
form a discrete set, any continuous field-class gauge map is locally constant
(named Category-A), hence on a connected cell a SINGLE GLOBAL K₄ element: **the
field-class residual chart quotient is the same exact K₄, acting pointwise, and
NO patchwise sign-flip ambiguity exists** — the field-census moduli quotient is
(sections)/K₄(global), a clean orbifold-section space with no gluing obstruction.

### 1.5 Anchored presentation orbits are singletons; the unanchored dressing flow

Per-member, general Function-moduli member, B(0) = 0 (anchor): the upper-right
conditions are exactly U′ = HU − UK(x) ⟹ U ≡ 0; the upper-left then kills the
boost pointwise; the single remaining condition is exactly
**θ′ + 2k_mod(x)θ = 0**, and θ(0) = 0 ⟹ θ ≡ 0 (`R1_anchored_orbits_singleton`).
Anchored orbits are SINGLETONS — same grade as Route B T1(a).

**Grading upgrade (post-verifier, credited):** the singleton claim also holds at
the **FINITE level**, not just infinitesimally — the finite orbit ODE
L′ = X̃L − LX is LINEAR in L with the same Picard structure (upper-right block
exactly Lu′ = HLu − LuK(x), Lu(0) = 0 ⟹ Lu ≡ 0; then Lp ≡ I; the screen
condition's θ ≡ 0 branch is the unique anchored solution) — the claim is NOT a
linearization artifact (`ADOPTED_finite_level_orbit_linear` ← verifier V2e;
adopted per `CORRECTION_LAYER.md`).

**Derived structure (observation, recorded honestly):** UNANCHORED, every field
member carries a 1-parameter screen-rotation presentation dressing
θ(x) = θ₀e^{−2∫k_mod} with induced chart flow (δλ, δk_mod, δk10, δC) =
θ·(0, −k10, 4k_mod, J₂₃C); the banked anchor kills it; on k_mod ≡ 0 members it
degenerates to the banked Stage-2 stratum jump (consistency); the U-sector analog
is generically obstructed (witness computed); full unanchored classification
TYPED-NOT-EXHAUSTED — the anchored (registered) statement is complete
(`R1_unanchored_screen_dressing_flow`).

### 1.6 K₄/jets/transport coherence and the pointwise pins

K₄ acts pointwise on members exactly as banked; jets to 2nd order inherit the
characters; and gTg⁻¹ IS the anchored transport of the conjugated member — the
quotient is coherent at member, jet, AND transport levels
(`R1_K4_pointwise_on_field_members_and_transport`). The T4-analog:
det T(x,0) = e^{2∫λ} exactly, so the banked conditional volume pins promote to
POINTWISE loci (4D-blind ⟺ λ(x) ≡ 0) — pins stay conditional, nothing selected
(`R1_T4analog_volume_scaling_pointwise`).

**TD-R1 verdict: the x-dependent members form a COHERENT registered class** —
same chart, same trivial continuous stabilizer, same exact K₄ (now pointwise/global
on the connected cell), singleton anchored orbits. Stamps: both sectors, GENERIC +
promoted degeneration loci (§5), anchored, off-shell.

## 2. TD-R2 — transition/cocycle registration (the full J07 requirement)

The COMPLETE requirement for a global field-census assignment on the finite cell,
enumerated with per-item status (`R2_transition_data_requirement_typed`):

| # | Transition-data item | Status | Basis |
|---|---|---|---|
| 1 | per-overlap datum = block triple (ρ, Q, L) of the segment transport | **CLOSED (derived)** | ρ universal = e^{ΔxH} (§1.2); Q in-chart; L Duhamel; segment data exist canonically and are in-class: ∂_b T(b,a) = X(b)T(b,a), T(a,a) = I, upper-right zero, Q lower-triangular (`R2_segment_transport_wellposed_in_class`) |
| 2 | two-sided twisted cocycle law on overlaps | **CLOSED (derived)** | banked S2 legs + the law EXACT on the x-dependent-K instance (`R2_two_sided_law_xdepK_instance` — beyond the banked K = 0 Duhamel leg) |
| 3 | composition associativity (triple concatenation) | **CLOSED (derived)** | generic blocks, both bracketings identical, zero residual (`R2_associativity_three_segments`) |
| 4 | reversal/inverse data + interval loop holonomy | **CLOSED (derived)** | T(a,b) = [[ρ⁻¹,0],[−Q⁻¹Lρ⁻¹,Q⁻¹]] in-class; back-and-forth loop = I: J11 holonomy on the interval groupoid TRIVIAL (`R2_reversal_inverse_in_class`) |
| 5 | mirror-interface datum (mirrored cell, CANON) | **SUPPLIED (parity-conditional; F-R4)** | the depth mirror gives generator −X(−x), H-block −H ∉ class (banked S3 promoted pointwise, `R2_mirror_interface_supplied_dressing_conditional`): the interface datum requires the SUPPLIED seal dressing; ε_m never valued. **FAIRNESS (F-R1): the constant branch needs the SAME supplied datum — a shared supplied slot, NOT a field-branch obstruction** |
| 6 | completion-class cycle holonomy | **GC obligation (typed)** | J11 classification per completion class — IDENTICAL in type to the constant branch (Route B C4: J07 open for all strata there too) |

**TD-R2 verdict: NO DERIVED OBSTRUCTION.** The banked two-sided law supplies
closure under promotion; the only non-derived items (5, 6) are supplied/GC slots
the constant branch shares. Observation, recorded two-sidedly
(`R2_no_effective_member_denominators`): the banked E04 effective-member
reconstruction carries denominators (e^{(φ₁+φ₂)h_j} − 1) while the field-class
transition data are denominator-free — the drift law's denominators are an
artifact of forcing a constant effective member onto a composite; the symmetric
counter-note (the constant branch's S1 provenance seniority) is carried.

## 3. TD-R3 — alphabet registration

- **Shift/c_E interaction (the contract's named question), derived:** re-anchoring
  maps the anchored transport of X(·) to that of the translated member X(·+s)
  through the banked transition data (`R3_shift_translation_covariance_transport`);
  the moduli functions CO-TRANSLATE with all other local blocks; the c_E absorption
  stays confined to the (φ, c_E) pair — **m(x) does not interact with the
  absorption beyond co-translation by the same shift.** The banked anchored-exponent
  rule (Q-powers: p = q) is unchanged with m-entries spectating
  (`R3_mjet_alphabet_legality`).
- **Character legality:** m(x) and its jets to 2nd order carry the banked K₄
  characters pointwise (d/dx commutes with the constant conjugation; §1.6).
- **The locality boundary, derived (this is where the alphabet DOES cut):** an
  anchored nonlocal entry ∫₀ˣ m du in a bulk component FAILS the co-translation
  test (exact witness, residual s³/3) — the same anchor defect as bare φ — while
  the local jets pass (`R3_locality_boundary_nonlocal_excluded`). Bulk alphabet =
  LOCAL m-jets only; transports/holonomies live in the J07 transition layer;
  absolute-point/wall evaluations only through supplied-structure slots (banked V8
  resolution extended to moduli). This also draws the R13 boundary (no
  integrated-moduli functional as a pointwise coupling).

**TD-R3 classification: REGISTRABLE-WITH-NEW-DECLARED-ENTRIES (both sectors); no
obstruction derived; no dynamics invented** (`R3_declared_entries_ledger`).
Declared entries, each ledgered with provenance (declaration legal per contract):

| Entry | Content | Provenance tag |
|---|---|---|
| N1 | the seven moduli values m_μ(x) as running-point bulk arguments | census rows 11–14 fork (ii) (DERIVED-as-moduli upstream; promotion typed there) |
| N2 | the moduli jets m_μ′(x), m_μ″(x) per jet order | Stage-2 BR-M row ("+7 character-typed moduli-jet arguments per jet order"); characters recomputed here |
| N3 | wall/corner m-jet slots on the varied-boundary fork | this package's R4 wall-term leg; supplied-structure slots per the banked V8 resolution |

Exclusions (derived, not chosen): absolute-point m-evaluations and anchored
nonlocal m-integrals in bulk components; character-mismatched m-dependence (banked
rule, pointwise).

## 4. TD-R4 — response/census extension (typed; NO mass legs)

- **Tangent:** + 7 function-valued directions δm_μ(x), character-typed, K₄
  pointwise.
- **J05 instantiated:** with m-jet densities the pairing obeys
  ∫(D_m v + D_{m′}v′) = ∫(D_m − d/dx D_{m′})v + [D_{m′}v]_walls exactly
  (`R4_J05_pairing_wall_slots`): every δm_μ(x) pairs as a POINTWISE density row
  (the reduction theorem's field-fork form), and the varied-boundary fork REQUIRES
  the N3 wall m-jet slots (gate-5-type differentiability; P3 reading inherits
  moduli wall terms — banked forcing check 17 recomputed with explicit variation).
- **J06 instantiated:** the slot theorem holds pointwise (Gram diag(2,2,1);
  R_kmod(x) = 2r_tf(x); pure-trace kernels k_mod-blind at every x; tr X(x) = 2λ(x))
  — the determined-vs-retained branches extend per family as DENSITY branches;
  the k_mod discriminator still routes exclusively through the trace-free slot
  (`R4_J06_slot_theorem_pointwise`).
- **The moduli-jet response content, TYPED (the A1-clause seat)**
  (`R4_response_extension_typed_A1_seat`): the registered BR-M component space =
  the Stage-2 parametrization with the declared m-jet arguments added per grade.
  The banked Slice-2b field-census massless statement is scoped to the
  NO-moduli-jet alphabet (map fact, stamps intact); on the now-registered alphabet
  the pointwise moduli rows may carry jet terms — the row becomes a DIFFERENTIAL
  condition in m(x) rather than an algebraic one — so the massless re-derivation
  seat is now DEFINED (a Slice-2b-analog derivation on the extended alphabet),
  **not run**. No mass branch, census branch, or pairing adopted.

## 5. Stratum structure under promotion

The stratum obstruction promotes pointwise: [L23, X(x)](2,3) = 2k_mod(x) exactly
(`R5_stratum_level_set_pointwise_bind`): **k_mod(x) = 0 becomes a LEVEL SET**, the
banked pointwise Noether identity binds AT its points (pointwise-bind, per the
reduction theorem), generic zero-crossings add the banked J09-type
continuation/exclusion obligations (forcing guard 15, inherited); the resonance
loci λ(x) ∓ k_mod(x) ∈ {±1} promote identically; the deeper C ≠ 0 sub-variety
census stays TYPED-NOT-EXHAUSTED (inherited stamp). The θ-flow of §1.5 shows the
level-set structure is CONSISTENT with the class-level gauge story (the stratum
jump is the k_mod ≡ 0 degeneration of a globally-derived flow).

## 6. TD-R5 — the verdict (per sector, stamped)

- **(λ, k_mod) sector: REGISTERS** (`R5_verdict_lambda_kmod_sector`) — (i) class
  coherence derived; (ii) transition data closed; (iii) alphabet registrable with
  declared entries; (iv) mirror compatibility PARITY-CONDITIONAL on supplied
  ε_λ, ε_kmod (same supplied status as the constant branch); (v) response
  extension typed + J05/J06 instantiated; (vi) level-set stratum structure
  derived. Stamps: registered positive triangular chart; stationary one-parameter
  presentation; anchored transport; off-shell; GENERIC + KMOD0-level-set strata
  (deeper resonance census TYPED-NOT-EXHAUSTED, inherited).
- **(k10, C) sector: REGISTERS** (`R5_verdict_k10_C_sector`) — identically, with
  the χ-graded character rule extending pointwise (members, jets, transports) and
  the mixing-block cocycle closing with x-dependent K. Same stamps; RES-CNEQ0
  binds pointwise on promoted loci, deeper stratification inherited.
- **Registration grade (honest):** Route-B-Stage-1-analog (class / orbits /
  quotient / cocycle / alphabet / response-typing) — exactly the grade the prereg
  §1 (i)–(vi) definition demands. The BR-M response-space EXHAUSTIVE
  parametrization (a Stage-2-analog on the m-jet alphabet) is a NAMED further
  seat, not part of the registration definition. **Post-verifier (credited): the
  grade comparison is airtight requirement-for-requirement** — the one Route-B
  Stage-1 layer without an explicit Route-D check, T2 (bracket/subalgebra), is
  now closed with zero residual: [X₁(x), X₂(x)] lands in the class tangent V
  pointwise and is traceless, verbatim extension
  (`ADOPTED_T2analog_bracket_pointwise` ← verifier V7; T5/T6 are
  Route-B-specific selection questions, out of grade).

**Outcome class: OR2** — the registration SUCCEEDS; both census branches now
stand on registered class footing; the census fork is REAL and goes to Charles.
Not OR1 (no obstruction was derivable — every candidate was hunted and disposed:
the boost-connection loophole, the shift/anchor interaction, the mirror interface,
patchwise K₄ flips, nonlocal alphabet pressure, chart positivity), not OR3 (both
sectors register identically), not OR4 (nothing needed to be left open at the
declared grade).

**Map-fact restatement (the census fork; no promotion)**
(`R5_census_fork_map_fact_restatement`): the S1/S4 provenance asymmetry is
DISSOLVED AT THE CLASS LEVEL (pending verifier + Charles); the fork stands as a
PURE domain-definition choice — Charles's, or Route P's parity lever (ε_m
SUPPLIED, the one derivable discriminator). Honest residue of asymmetry: (a) the
constant branch keeps its Stage-2 exhaustive jet ≤ 2 response parametrization —
the field branch's response space is defined + typed, not exhausted; (b) the
Slice-2b attachment with stamps intact: constant census ⟹ integrated rows ⟹
massive locus nonempty; field census ⟹ pointwise rows ⟹ {E0 = 0} massless AT
THE BANKED NO-MODULI-JET ALPHABET, with the A1-clause re-derivation seat now
DEFINED on the registered m-jet alphabet (typed, not run). Neither branch adopted;
no mass claim made.

## 7. Falsifier record (derivation-side)

- **F-R1 (steering): not fired — structure audit.** The tempting outcome
  (REGISTRATION-FAILS, forcing the constant census and the massive branch) was NOT
  reached; conversely, the success direction was attacked on the record: the
  candidate obstructions were each computed to conclusion (§1.3 loophole; §2 items
  5–6 honestly left supplied/GC rather than claimed closed; §3 locality exclusion
  derived and stated as a CUT the field alphabet takes; the anchor-dependence of
  orbit singletons stated openly in §1.5). Both directions of every asymmetry are
  on the record (S1 seniority note carried against the denominator observation).
- **F-R2 (invented obstruction / invented registration): not fired** — the class
  definition, anchor, and every structural law are banked citations; the new
  declared alphabet entries are DECLARATIONS (ledgered, §3), not dynamics; no
  kernel, equation, or mechanism was introduced.
- **F-R3 (scope stamps): policed** — every claim carries sector + structure +
  stratum stamps; the registration GRADE itself is stamped (Route-B-Stage-1-analog)
  with the not-exhausted layers named (BR-M response parametrization; deeper
  resonance census; unanchored dressing classification).
- **F-R4 (parity assumption): not fired** — ε_m appears only as supplied data;
  every mirror statement is parity-conditional; the swap-dressing candidate stays
  a cited Route-P input.
- **F-R5 (bank contradiction): none found** — recomputed banked facts matched
  everywhere (Route B stabilizer/K₄; forcing S2/S3/S5 legs; Stage-2 stratum
  obstruction; D3 anchoring; slot theorem); the promotion legs EXTEND banked
  results without altering any.
- **F-R6 (symbolic failure): none** — 38/38, exit 0, byte-identical reruns ×2
  (36/36 pre-adoption; the two `ADOPTED_*` checks added post-verifier).

**Limits that travel:** (i) computational legs ride the named closed-form
instances (mixing: polynomial C(x) with nilpotent-family K(x); seat: affine
diagonal K(x)) plus generic-block identities — the generic-member statements
(chart stability, stabilizer, K₄, orbits, θ-flow) are Function-valued and
member-general, the instance statements are instance-stamped; (ii) jets treated
to 2nd order where jet claims are made (matching the banked exhaustive layer);
higher jets inherit by the same commutation argument, typed; (iii) the finite
exhaustiveness of the residual gauge is complete at the stated conditions
(continuous curves on a connected cell; locally-constant is Category-A);
(iv) items (5)/(6) of the J07 requirement are supplied/GC for BOTH branches — a
shared conditionality, not a closure; (v) the registration is of the CLASS and
its response TYPING; the exhaustive BR-M response parametrization and any mass
re-derivation on the m-jet alphabet are named, unrun seats; (vi) deeper
resonance/C ≠ 0 stratification inherited TYPED-NOT-EXHAUSTED.
