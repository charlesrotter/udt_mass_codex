# D1 — Native re-derivation audit of the early angular-sector constants (q=1/3, N=3, η=1/18) + the legacy QCD/QED overlap claims

**Mode:** provenance audit + gated re-derivation attempt (direction D1 of
`ponder_emergence_directions_2026-07-04.md`). DATA-BLIND: no particle masses/data touched; the
constants are targets of provenance, not fit targets. Operating discipline =
[[algebraic-objects-can-be-imports]] (Charles): honest failure is a first-class outcome.
**Driver:** Claude (D1 deriver agent), 2026-07-04. **Status: PROVISIONAL — NOT blind-verified,
NOT committed.** CAS scripts: `d1_rederive_n3.py`, `d1_rederive_q13.py`, `d1_rederive_eta18.py`
(all sympy, all PASS, bounded, no solves).
**Legacy archaeology:** two dedicated recon agents (dependency-chain reconstruction; QCD/QED
overlap enumeration) — their citations are folded in below with file:line.

**Allowed current-framework inputs (each use cited):** CANON C-2026-06-14-1 + refinement (the
native S² carrier n_a; ω_H1 = ε_abc n_a dn_b∧dn_c; L2+L4), C-2026-06-18-1 (metric form; static/
spherical/diagonal/areal = four independent CHOSE), the 2026-07-01 native field equations record
(`udt_field_equations_derivation_results.md`, `native_dilation_weight_derivation_results.md`,
`matter_regrade_derived_operator_results.md`), F2 forcedness (`F2_matter_action_forcedness_results.md`),
the derived seal/fold machinery (`universe_cell_fold_jc_sigma_results.md`,
`seal_junction_condition_results.md`), and the E1 composite condition set
(`microphysics_E1_composite_closure_results.md`).

---

## 0. HEADLINE VERDICTS

| Constant | Verdict | One-line basis |
|---|---|---|
| **N = 3** | **NATIVE-REDERIVED (conditional)** — the CONSTANT re-emerges from current objects by a route CLEANER than its legacy derivation (which does NOT survive) | Within the canonized unit-vector carrier class, rank 3 is forced two independent ways: the winding density of a rank-N carrier is an (N−1)-form, and only N=3 gives the 2-form the canonized L4 norms / the S² cell surface integrates (CAS-verified); π₂(S^{N−1})≠0 iff N=3 (classical). Conditions: the carrier class itself + the 2D cell surface (see §2). |
| **q = 1/3** | **IMPORT-DEPENDENT** | Every route to 1/3 rides a legacy-only posit: the source amplitude s=1/9 ("postulate or circular backsolve", NPG:13851) through the superseded-operator collar ODE, or the curvature-share closure posit (NPG:12996-13009 "postulate — not derivation"). CAS: q=1/3 ⟺ s=1/9 exactly (backsolve). The current framework's analogous seal quantity is a FREE OUTPUT (q_cell = Zρ_s²φ', E1 §1), not pinned; the native carrier source amplitude carries the CHOSEN coupling ξ. |
| **η = 1/18** | **IMPORT-DEPENDENT (value); no native home (object)** | The value needs either the POSTULATED factor 1/2 in 1/(2N²) (NPG:2513-2518: "the angular average alone gives 1/N or 1/N², not the extra 1/2") or the Λ²End selector whose functional obligation was never discharged (LHSF:176-179; DLNA:150,191-195). CAS: the two routes coincide identically at N=3 and only there — one lock, not two derivations. The DERIVED current seal (JC1/JC2, fold pins, E1 C1a–C2) contains **no boundary-coupling slot at all**: η has nowhere to live natively. |

**The single most decisive finding (plainly):** the three constants were never one family. N=3 is
real cargo — it re-emerges from the current framework's own canonized objects, more cleanly than it
was originally obtained. q=1/3 and η=1/18 are **derivatives of N=3 plus legacy posits that the
current framework does not supply** (s=1/9 and the ½-normalization respectively) — "rigid GIVEN
N=3" (F0:121) but with no native life of their own. And the record contains a documented
candidate→"NATIVE-DERIVED" promotion: `MATTER_SECTOR_MAP_new_foundation.md:87` cites "h1_types" as
the deriving authority, but `legacy/root_oneoffs_2026-07-01/h1_types_derive.py:79` **hard-codes
q = 1/3 as an input** (`q = sp.Rational(1,3)`) and derives none of the three. The F0 flag
(M14/M15 "needs provenance re-audit") was correct; this doc is that re-audit.

Also settled in passing: **"H1" is a misnomer the record itself flags** — H¹(I×S²) = 0
(`h1_types_derive.py:116-119`; NPG:29796). The object is the ℓ=1 eigenspace of −Δ_S² (dim 2ℓ+1=3);
the area form lives in H². Every "dim H1 = 3" below reads "dim(ℓ=1 carrier) = 3".

---

## 1. THE ORIGINAL DERIVATION CHAINS (reconstructed, with the candidate→input promotions)

### 1.1 q = 1/3 — chain

```
finite-action filter (p < 1/2)                       [legacy premise, NPG:18643-18647]
  + source amplitude s = 1/9                         [POSTULATE/"circular backsolve", NPG:13851]
  + collar ODE f'' + 2f'/r + 2s f/r² = 0             [built on the SUPERSEDED operator]
  → slope-flow fixed point q(1−q)/2 = s              [DERIVED given the above; NPG:9397-9461]
  → q = 1/3 (outward-attractive root at s=1/9)       [NPG:9461]
  → self-classified "minimal native closure POSTULATE — not derivation"  [NPG:12996-13009, 13067]
  → promoted to allowed INPUT ("pre-spectrum outputs")                   [PS:26-34]
  → relabeled "NATIVE-DERIVED (h1_types)"            [MSM:87 — OVER-CLAIM; script imports q]
```
Three legacy routes existed (endpoint self-similarity 1−2p=p; the s-sourced flow; curvature-share
closure with ⟨n_a n_b⟩=δ/3); each carries its own open gap in the doc's own words (NPG §187
"One-third convergence audit": "The repeated 1/3 is not yet a theorem", NPG:13217). Routes 2 and 3
both reduce the 1/3 to **1/N (N=3) plus a posited closure** — CAS CHECK 4 (`d1_rederive_q13.py`).

### 1.2 N = 3 — chain

```
"least-action mixed-Hodge harmonic carrier branch on I×S²"   [ALLOWED INPUT; selection open, NPG:30764 P_domain]
  + ℓ=0 exclusion                                            ["selector assumption", NPG:18558]
  → carrier = ℓ=1 triplet, dim 2ℓ+1 = 3                      [spectral fact given the above]
  + "Unique Epsilon Source POSTULATE" (Pepsilon)             [NPG:2617-2619, 2648-2650]
  → dim Λ³(R^N) = 1 iff N = 3                                [rigid math; NPG:2582-2594; CAS CHECK 1]
  → banked as the C(N,3)=1 lock                              [F6:105, "explicitly NOT QCD color"]
```
The legacy discipline note was already there: "Do not relabel postulate consequences as derived"
(NPG:2663). The two DLNA locks (LOCK-FLOW, LOCK-2F) are rigid but graded "two locks at chance
level ~1/37, not a growing body of confirmations" (DLNA:142).

### 1.3 η = 1/18 — chain

```
two triplet averages (1/N each) → 1/N² = 1/9                 [rigid GIVEN N=3]
  + factor 1/2 "quadratic action normalization"              [POSTULATED; NPG:2513-2518]
  → η = 1/(2N²) = 1/18                                       [CANDIDATE; verdict NPG:2522-2525:
                                                              "not derived until the source-action
                                                              factorization is derived"]
  ∥ re-named 2/dim Λ²End(ℓ=1) = 2/36                         [LHSF:169-170; functional selector
                                                              "open" LHSF:199-204, never discharged
                                                              DLNA:150, 191-195]
  → promoted to allowed INPUT                                 [PS:32]
  → canon refinement demotes to "seal/boundary object, NOT a bulk potential"  [CANON:173]
  → relabeled "NATIVE-DERIVED (h1_types)"                     [MSM:87 — OVER-CLAIM]
```

### 1.4 W(P) = Tr(P)/12 (the C1 readout, audited as requested)

Candidate readout (PS:1380-1401, 1455 "a readout rule candidate, not yet a mass formula"): the 12
= 36/3 traces to dim Λ²End = 36 and the isotropy factor 3 = N (LHSF:220 `BBᵀ = 3P_T8`). It
inherits BOTH parents: the Λ²End selector (undischarged) and N=3. The one DLNA-"FORCED" piece is
the identity bridge (η/2)·N = S_C1/R (DLNA:73) — an internal consistency of the legacy frame, not
a native derivation. **Adjudication: IMPORT-DEPENDENT** (same imports as η, plus the C1 side
action itself, which lived on the superseded operator).

---

## 2. THE RE-DERIVATION ATTEMPTS FROM CURRENT OBJECTS ONLY

### 2.1 N = 3 — RE-EMERGES (two independent current-framework forcings; `d1_rederive_n3.py`, all PASS)

The current framework canonizes the carrier as a **unit-vector multiplet n_a whose winding density
is the area form ω_H1 = ε_abc n_a dn_b∧dn_c, the pullback of the S² target area 2-form**
(C-2026-06-14-1; F2_matter_action_forcedness_results.md:133), with L4 = −(κ/4)|ω_H1|²_g. Ask the
rank question natively: for a rank-N unit carrier (target S^{N−1}), the unique SO(N)-invariant
winding density ε_{a1…aN} n dn∧…∧dn is an **(N−1)-form** (CAS CHECK 2: the invariant subspace of
Λ³(R^N) under so(N) has dim 1 at N=3 and dim 0 at N=4,5 — computed, not cited). Then:

- **Forcing A (degree match):** the object the canonized L4 takes the metric-norm of, and the only
  degree a winding density can have to be integrated over the spatial **2-sphere cell surface**, is
  a 2-form ⇒ N−1 = 2 ⇒ **N = 3**. (CHECK 3: at N=3 the hedgehog pullback = 2 sinθ dθ∧dφ, ∫ = 8π,
  exact.) The "3" is sourced by the two-dimensionality of the cell surface, +1 — NOT by the epsilon
  lock (which presupposes its own 3; circularity flagged in CHECK 1).
- **Forcing B (topology):** π₂(S^{N−1}) = Z iff N = 3, trivial for every other rank (classical,
  Hurewicz — cited, not computed). A rank-N carrier supports a topological point-defect charge on a
  2-sphere iff N=3. This is exactly the native-defect discovery ([[native-matter-defect-import-discovery]])
  re-read as a rank selector, and it independently retires S³ (N=4: π₂=0) — consistent with the
  blind-verified dynamical settle (`archive/s2_s3_identity_results.md` + VERIFIER "the S² settle
  STANDS", 2026-06-19; explicitly re-graded CARRY under the new operator,
  `matter_regrade_derived_operator_results.md` §5).

**Verdict: NATIVE-REDERIVED, conditional on two named premises:**
1. **The carrier class** (matter = unit-vector sigma-model multiplet with topological winding) —
   canonized (C-2026-06-14-1; anchor genuineness blind-verified, I_native == G1); its ultimate
   provenance is the legacy dpf density, but it is a CURRENT-framework object in good standing.
2. **The 2D cell surface** — rides the finite-cell canon (C-2026-06-10-2, itself the A1 posit per
   F0) + the round/spherical frame (a CHOSE per C-2026-06-18-1's four-independent-choices clause).

GIVEN those two (both already load-bearing for everything else in the matter sector), N=3 is
forced, uniquely, twice over. **The legacy ROUTE does not survive** (mixed-Hodge branch selection
open; ℓ=0 exclusion an assumption; the epsilon-singlet demand a postulate) — the constant survives
by a different, shorter path. This is the "true cargo" case D1 was looking for.

### 2.2 q = 1/3 — DOES NOT RE-EMERGE (`d1_rederive_q13.py`, all PASS)

- The one legacy route with a real mechanism (the slope flow) is **exactly s-conditional**: CAS
  CHECK 3 backsolves s = 1/9 as the unique source amplitude giving q = 1/3; generic s gives
  generic q. s = 1/9 is self-graded "a postulate or circular backsolve" (NPG:13851) — and its only
  algebraic reading is 1/N² (dimension-ladder numerology, DLNA-cheap).
- The collar ODE itself was built on the **superseded operator** (pre-2026-07-01 field equations);
  CONDITIONS-CHANGED applies to the whole radial scaffolding q lived in.
- Current-framework check (documentary): in the derived cell/seal machinery the analogous quantity
  is a **free output**, not a pinned number — "φ'(r_sU) free ⇒ q = Zρ_s²φ' is an OUTPUT"
  (`microphysics_E1_composite_closure_results.md` §1); no 1/3 appears anywhere in the blind-verified
  fold/ladder record (grep-confirmed: no 1/3 in universe_cell_fold / E1 / seal-JC docs).
- A native re-pose ("what log-slope does the carrier's winding stress source at a collar?")
  inherits the coupling ξ, whose VALUE is CHOSEN (`MATTER_SECTOR_MAP_new_foundation.md` §2, crux
  verdict) — so no dial-free 1/3 can currently come out.

**Verdict: IMPORT-DEPENDENT.** Named imports: **s = 1/9** (legacy postulate) + **the
superseded-operator collar equation** (legacy radial scaffolding). Minimal missing native link,
stated exactly: *a derivation, on the 2026-07-01 native operator, of a dial-free collar source
amplitude from the carrier stress* — today that amplitude is ξ-dependent and ξ is CHOSEN. Until
that exists, q=1/3 is 1/N wearing a posited closure.

### 2.3 η = 1/18 — DOES NOT RE-EMERGE (`d1_rederive_eta18.py`, all PASS)

- Value routes: (A) 1/(2N²) needs the postulated ½ (CAS CHECK 5: λ/N² = 1/18 at N=3 forces
  λ = ½ exactly; no current object supplies it). (B) 2/dim Λ²End needs the never-discharged
  functional selector. CAS CHECK 4: routes A and B **coincide identically at N=3 and only there**
  — the "two routes" are one lock (rigid GIVEN N=3, chance-graded by DLNA), not convergent
  derivations.
- Object-level (the sharper current-framework fact): η was canon-demoted to "a seal/boundary
  object, NOT a bulk potential" (CANON:173; reaffirmed F2_closure_results.md §3.2). The seal has
  since been **actually derived** — JC1/JC2, the odd-fold pins (φ=0, ρ'=0, H=0), the E1 conditions
  C1a/C1b/C1c/C2 — and the derived set **contains no boundary-coupling slot**. Nothing forces an η
  term; nothing forbids adding one, but adding one would be a NEW POSIT (exactly the flag
  F2_closure already raised for promoting η to a bulk potential).

**Verdict: IMPORT-DEPENDENT for the value 1/18** (named imports: the ½-normalization posit, or
equivalently the Λ²End functional-selector debt), **with the object itself currently HOMELESS**:
the current framework's derived boundary machinery has no place where η enters. If a future native
boundary action term emerges from the fold/seal variational structure with a coefficient, THAT
would be the legitimate re-derivation target; none exists today.

### 2.4 Minimal native premise sets (summary)

| Constant | Minimal premise set under which it holds | Which premises the current framework supplies |
|---|---|---|
| N=3 | carrier class (unit-vector, winding) + 2D cell surface | **BOTH** (canonized / canon+CHOSE) — hence NATIVE-REDERIVED |
| q=1/3 | N=3 **+ s=1/9** (or the share-closure posit) + the legacy collar scaffolding | N=3 only — s and the scaffolding are legacy-only |
| η=1/18 | N=3 **+ λ=½ normalization** (≡ the Λ²End selector) + a boundary term to live in | N=3 only — λ underived, no boundary slot in the derived seal |

### 2.5 CHOSE / premise ledger for THIS audit (everything I leaned on, tagged)

- Round/spherical frame + finite cell: **CHOSE + canonized posit** (C-2026-06-18-1 four-choices
  clause; A1 per F0) — the N=3 verdict is conditional on them, said so.
- Carrier class (unit-vector n_a): **THEORY(cite C-2026-06-14-1)**, blind-verified anchor; legacy
  ancestry acknowledged.
- S²-vs-S³ settle: **THEORY(cite s2_s3_identity_VERIFIER + matter_regrade §5 CARRY re-grade)** —
  Bin-2 re-grade at point of use done (the CARRY table re-graded it under the new operator).
- ξ, κ values: **CHOSE** (MATTER_SECTOR_MAP crux) — used only negatively (to show no dial-free q).
- π₂/Hurewicz table and Λ-invariant theory: **classical mathematics** (CHECK 2 computed the
  invariant dimensions rather than citing where feasible).
- h1_types script: used as documentary evidence of what it computes (its own blind verifier is
  PENDING per `archive/h1_types_results.md:10`) — nothing in my verdicts rides its physics claims.

---

## 3. THE EARLIER QCD/QED OVERLAP CLAIMS — ENUMERATION + ADJUDICATION (scope extension)

*(Enumeration built from the legacy record by a dedicated recon agent (citations file:line as
reported and spot-checked); per-item adjudication under the same discipline. Null-test tagging per
`dimension_ladder_null_audit.md` (DLNA): exact small-rational matches are cheap — expressibility
coverage ~16% strict / ~23% generous grammar, DLNA:108; the dense-(rational)·π^k null hit a random
target within 1% at P=0.98 (mass_emergence §2). Classifier boundary: everything in
`udt_canonical_geometry.md` (CG) §18-19 predates BOTH nulls (banked 2026-03/04); the TEST-B
classifier ran 2026-06-10.)*

### 3.1 The pre-classifier CG stratum (2026-03/04) — the QCD/QED overlaps as originally banked

| # | Claim (as stated) | How obtained | Scrutiny record | D1 adjudication |
|---|---|---|---|---|
| A1 | "QED is fully proved" — Lamb shift, g−2, hydrogen "automatically passed" (CG:3107-3146) | equivalence argument: loop momenta see no S² curvature; angular algebra "geometrically protected" | never prosecuted head-on; rebuild docs narrowed to "only the classical SKELETON derived" (external_input_notes:133) | **IMPORT-DEPENDENT** — named imports: the gauged **Dirac / Form-T scaffold** (disallowed post-rebuild, PS:42) + the **superseded operator** (pre-2026-07-01). CONDITIONS-CHANGED besides. |
| A2 | su(3) kinematics exact; "QCD as the rank-2 geometric limit" (CG:3131-3146) | rank-2 tensor on ℓ=1; 8=3⊕5 | prosecuted (mass_emergence §1): algebra **[DERIVED]**, rank-2 identification **[ANSATZ]** (Dirac-index↔tensor-rank conflation, verifier-confirmed); Casimir 4/3 vacuous | **SPLIT:** the algebra 9=1+8, 8=3+5 **NATIVE-REDERIVED** (it is End(R³) structure, inherits §2.1's conditions); the QCD/rank-2 READING **IMPORT-DEPENDENT** (named import: the Dirac-index conflation). |
| A3 | 1/α_EM = 36π/I₂ → 137.036 with "Schwinger-analog" correction (CG:2894, 3246-3285) | four-factor bridge off the gauged Dirac action; I₂ an ODE output (conjectured closed form π²/12 REFUTED, CG:2894) | **pre-classifier**; never TEST-B'd; rides the [ANSATZ] rank-2 bridge | **IMPORT-DEPENDENT** — named imports: η=1/18 (§2.3), the Dirac bridge, the superseded radial operator. Two-step chain each tuned toward the target; pre-classifier tag. |
| A4 | α_s/α_EM = 9/4 "exact" (CG:3144) | multiplicity ratio (2ℓ+1)²/(2j+1)² | prosecuted: number [DERIVED] arithmetic, name "**a §2 label**" (mass_emergence:210) | **IMPORT-DEPENDENT** — the (2j+1)=2 slot is a **spinor import** (postulate-A object); the coupling name a LABEL. |
| A5 | α_s IR-freezing, Λ_QCD ≈ 133 MeV "falsifiable prediction" (CG:3916-3923) | radial ODE integral saturating | pre-classifier; the doc itself concedes dynamics "not yet derived" (CG:3146) | **IMPORT-DEPENDENT** + CONDITIONS-CHANGED (superseded radial dynamics). |
| A6 | θ_QCD = 0 "solves strong CP geometrically" (CG:3581) | reality of S² harmonics / real structure constants | pre-classifier; unprosecuted | **SPLIT:** the geometric fact (the carrier is REAL — n_a real, real structure constants) is native and still true; the θ_QCD READING is **IMPORT-DEPENDENT** (needs the su(3)-GAUGE identification, which #50 blind-verified is NOT classically native). |
| A7 | sin²θ_W = 3/13; PMNS 4/13, 4/7, 1/45; δ_CP = −4/13 (CG:3341-3653) | partition fractions on the "13-dim coupling space" 4+9=13 | **pre-classifier small rationals** — exactly the DLNA-cheap class; never TEST-B'd; the CMB use demoted (CG:1941) | **IMPORT-DEPENDENT** — the 4 = (2j+1)² is the spinor import again; and pre-classifier cheap-match tag (denominators 7, 13, 45 inside the ~16-23% coverage universe). |
| A8 | quark charges ±2/3, ∓1/3; base masses 4mₑ/9mₑ; m_t = 84·4·π⁶·mₑ; N_c=3; g_A=4/π (CG:3695-3781) | multiplicity squares; charge:=√(B₁/B₃) | **fully prosecuted** (mass_emergence §2): charges **[LABEL]** (tautology; "NOT the SM quark charges", cr192); base-mass FORM [FITTED]; MS-bar match **corpus-retracted as "a mirage"**; π-mass generation ratios **[FITTED], DROP** (dense-π P=0.98); N_c=3 = "[DERIVED] integer wearing a [LABEL]" | **IMPORT-DEPENDENT / RETIRED** — the surviving cargo is only the integer 3 (see B1/§2.1). |
| A9 | nuclear force = QCD; deuteron C/63; He-4 C/5 (CG:2544-2548, 3757) | combinatorial coefficients on a three-exchange potential | self-demoted IN-ERA: "one-point algebraic match", QUARANTINE-as-prediction (CG Session 26; LHSF:95) | **IMPORT-DEPENDENT / QUARANTINED** (stands as the record left it). |

**Stratum verdict:** every CG-era QCD/QED overlap that was re-prosecuted came back LABEL / FITTED /
ANSATZ / retracted; the ones never re-prosecuted (A1, A3, A5, A6, A7) are pre-classifier,
Dirac-scaffold-dependent, and sit on the superseded operator. **None of Part A re-emerges from the
current framework.** Their common true cargo is the same N=3/End(R³) algebra of §2.1.

### 3.2 The native-rebuild stratum (2026-06-10→15) — what the re-scrutiny already sorted, re-adjudicated

| # | Item | Legacy scrutiny it survived | D1 adjudication under the CURRENT framework |
|---|---|---|---|
| B1 | **N=3** (explicitly NOT QCD color; F6:105) | TEST-B classifier 2026-06-10: two locks, uniquely N=3, "chance ~1/37" — strongest classifier survivor | **NATIVE-REDERIVED (conditional)** — §2.1 SUPERSEDES the locks with a shorter premise set (carrier class + 2D cell surface; two forcings). The classifier-era "weak-but-real" grade upgrades: no longer a value-match, a structure theorem. |
| B2 | **q=1/3** (+ the 2/3 assignment) | rode B1 through TEST-B; the u/d charge ASSIGNMENT prosecuted [LABEL] | **IMPORT-DEPENDENT** (§2.2: s=1/9 + superseded collar scaffolding). The SM charge assignment stays LABEL. |
| B3 | **End(H1)=1+8, 8=3+5** (su(3)-adjoint echo) | algebra recomputed natively (PS §1); dim-7 gluon echo verifier-killed (#35); no native gauge field for the 5 symmetric generators (#50, blind-verified) | **algebra NATIVE-REDERIVED** (= End(R³) of the current carrier; inherits §2.1 conditions); the **SU(3)-gauge/color reading IMPORT-DEPENDENT** (named import: a local gauge principle the metric does not supply — #50). |
| B4 | **W(P)=Tr(P)/12** (weights 1/4, 5/12, 2/3; composites 36/84/108/180) | banked "licensed readout"; 108/180 explicitly unlicensed; 84 FINGERPRINT | **IMPORT-DEPENDENT** (§1.4: rides the undischarged Λ²End selector + the C1 side action on the superseded operator). Composites stay FINGERPRINT. |
| B5 | **η/2 ↔ Λ²End(H1)=36** selector | DLNA's own "most specific naming in the whole ledger" (F3) — best classifier survivor among the value-matches; functional selector OPEN | **IMPORT-DEPENDENT** (§2.3). CAS CHECK 4 adds: the 1/(2N²) and Λ²End routes coincide identically at N=3 and only there — one lock, not two. The functional obligation is still the upgrade gate, and the current derived seal offers it no home. |
| B6 | **i = S² area form** (structural-i; "why QM is complex" derive-candidate; F6 N-2/N-3, sympy-exact, "survives the hardest attack") | verifier-confirmed symplectic identity; dynamical/ℏ half explicitly parked | **NATIVE-REDERIVED (conditional, structural half only)** — ω_H1 IS the symplectic/Kähler form of the CURRENT canonized carrier target; it inherits exactly §2.1's premise set and survives with N=3. The i-FLOW/ℏ half stays **UNDERDETERMINED** (the parked clock/ℏ gap — nothing in the current framework forces or forbids it). |
| B7 | **WZW / soliton-as-fermion** (#49/#50/#51/#53) | each blind-verified STANDS; 5th-refusal SHELVE (reframe-observation-led 2026-06-15); CONDITIONS-CHANGED triggers logged | **IMPORT-DEPENDENT, stands SHELVED** — the fermion is postulate-A material (F6); the parity firewall (even L4 scalar cannot contain the odd Hopf 3-form, #47c) is a statement about the CURRENT canonized L2+L4 and therefore CARRIES. |
| B8 | **The photon / EM-native positive** (#47-pos, em_forcing; "metric induces a connection only for U(1)×SO(3)×SO(3,1)", #50) | verifier-cleared, canon-candidate — the strongest surviving positive of the cluster | **UNDERDETERMINED (pending re-grade)** — honest Bin-2 application: em_forcing (2026-06-14) and #50 ran on the PRE-2026-07-01 operator and are NOT in the matter_regrade CARRY table. The induced-connection argument looks kinematic (likely operator-robust) but that is exactly the judgment a re-grade must make, not this audit. Named gap: **re-grade #47-pos/#50 on the native field equations.** |
| B9 | **(5/3)e^{−1/18} splice; p_F=γ/2; c*=0.498912γ²** | splice verifier-KILLED ("W(P) never multiplies p_F in any real functional"); p_F, c* banked solid | splice **RETIRED** (stays dead — and note it was the only place η=1/18 entered an observable-form object). p_F=γ/2, c*: native CELL quantities, not SM overlaps; old-operator provenance — CONDITIONS-CHANGED flag on their numerical values. |
| B10 | **Koide / √m** (S13.11) | blind-checked "native GIVEN postulate A"; constant-ratio ladder killed by data (#48); SHELVED with the fermion | **IMPORT-DEPENDENT** (named imports: postulate-A fermion + the Dirac √m footing) — stands shelved. |

### 3.3 Null-test discipline, applied (the explicit tagging the scope extension asked for)

- **Banked PRE-classifier, never TEST-B'd:** A1, A3, A4, A5, A6, A7 (and A8/A9 before their
  prosecutions). Every member of this set that WAS later re-examined got downgraded — the
  base rate says treat the unexamined ones (α_EM chain, mixing angles, IR-freezing, θ_QCD) as
  scaffolding-grade until independently re-derived. None passes TEST-B today: each has a free
  slot ((2j+1) spinor dims, I₂, the 13-space) that is not N-generalizable in the TEST-B sense
  because its generalization parameter is an import, not a framework dial.
- **Ran TEST-B and survived:** B1 (N=3 locks), B2's 1/3-as-1/N, B5 (η/2 naming) — all at the
  classifier's own "chance ~1/37, not a growing body" weight. Of these, only N=3 has since
  acquired a non-value-match (structural) derivation (§2.1); the other two still await their
  functional gates and are adjudicated import-dependent above.
- **Not value-matches (classifier n/a):** A1 (equivalence claim), B6 (structural identity),
  B7/B8 (existence/no-go results) — these live or die by operator-provenance, which is how they
  are adjudicated above.

### 3.4 What Charles's "may have been scaffolded" resolves to

The scaffolding hypothesis is CONFIRMED for the QED/QCD overlap layer specifically: the precision
matches (α, mixing angles, Λ_QCD, g−2/Lamb "automatic" passes) all ride the Dirac Form-T scaffold
+ the superseded operator + pre-classifier match discipline, and none re-emerges. What was NOT
scaffolding — the cargo that keeps surviving every era and re-emerges here from current objects —
is small and structural: **N=3 and its operator algebra 9=1+8=1+3+5 (§2.1, §3.2-B3), the real
(phase-free) carrier structure (A6's geometric half), and the structural-i identity (B6)** — all
consequences of the ONE canonized object ω_H1 on the unit-3-vector carrier. Plus one positive
awaiting its operator re-grade: the EM-native/photon result (B8).

---

## 4. VERIFIER HOOK (ATTACK HERE)

- Re-run the three CAS scripts (seconds each; sympy only).
- Attack §2.1's Forcing A for circularity: does "the winding density must be a 2-form" smuggle the
  answer? The defense is that the 2 comes from the CELL SURFACE dimension (a frame CHOSE already
  carried project-wide), not from the target — check that no step uses rank 3 before concluding it.
- Attack the q/η verdicts for missed native routes: grep the 2026-07-01+ record for any derived
  equation pinning a dimensionless collar slope or boundary coupling (I found none; falsify that).
- Check the h1_types finding (MSM:87 vs `h1_types_derive.py:79`) by reading the script directly.

---

## VERIFIER RECORD (blind adversarial pass — agent a8e6f8faa37a495d0, 2026-07-04)

**All 8 attacks HOLD (one with correction, applied); SAFE TO BANK.** Both directions attacked:
the confirming grade (N=3 native) hardest per hypothesis discipline, AND the demotions
steel-manned before acceptance.

- **N=3 STRENGTHENED:** the verifier's own all-k invariant computation (Λ^k(R^N), N=2–6,
  independent generator-action code; `d1_bv_n3_attack.py`) closes the circularity loophole this
  doc's CHECK 2 (Λ³-only) left open — the unique SO(N)-invariant is the top N-form for every N,
  AND via the isotropy representation there is NO SO(N)-invariant 2-form on S^{N−1} of any kind
  except at N=3. §2.1's citation is CORRECTED to ride the all-k result. The "round CHOSE"
  condition is RELAXED: any closed orientable 2-surface works (degree theory; 2D-ness comes
  from 3 spatial dimensions) — conditions now: carrier class (THEORY) + 2D cell surface only.
  Route B (π₂) verified for all N≥1, no presupposition.
- **q=1/3 demotion HOLDS — steel-man failed 4 ways** (`d1_bv_q13_steelman.py`): (S1) native
  collar flow fixed point rides free ξ/Z; (S2) φ'(r_s) genuinely free in the derived pin set,
  and the framework's OWN banked numbers refute universality (U_seal = 2−q²/(2Zρ_s²) spans
  0.052–0.671 across families — q varies); (S3) the isotropic share is native but no
  share-closure exists in the derived condition set; (S4) ladder constants all Z-dependent;
  repo grep finds 1/3 post-2026-07-01 only in the over-claim rows. No native dial-free 1/3.
- **η=1/18 homelessness HOLDS** (seal set verified slot-free first-hand; CHECK 4 reproduced —
  one lock at N=3, not two derivations).
- **PROMOTION ERROR BIGGER than §4 stated:** beyond MSM:87, the same over-claim sits in the
  banked, blind-verified `matter_regrade_derived_operator_results.md:189` CARRY row and MSM:59.
  Git timing: h1_types_derive.py was born (2026-06-14, af0d95e) with q hard-coded; the
  NATIVE-DERIVED labels were written 2026-06-21 (b72abeb) — a mislabel at bank time, not later
  drift. All three locations now carry correction flags (this commit). F6:105 was the honest
  entry (explicit provenance caveat).
- **QCD/QED enumeration HOLDS** (6 citations verbatim-verified; pre-classifier dating
  consistent; B8 photon re-grade genuinely owed — absent from the CARRY table).
- **H¹→H² misnomer HOLDS**, label-only, no doc rides it materially. Convention note: the ∫ω
  8π-vs-4π discrepancy with MSM:59 is a wedge-normalization factor 2; both read degree 1
  after their own normalization.
- Hygiene: CAS scripts reproduce; dead assert removed from d1_rederive_q13.py (this commit);
  pytest 32/1xfail; data-blind confirmed (legacy value-claims appear only inside citations).
