# P4 Route C Stage 1 — exact derivation record (TC1–TC6)

Date: 2026-07-28. Branch: grok. Contract: `PREREGISTRATION.md` (frozen before this
derivation). Script: `derive_routeC_stage1.py` (exact SymPy, zero-residual checks,
deterministic, single CPU process). Results: `routeC_stage1_results.json`,
`SECTOR_COMPARISON_LEDGER.tsv`, `BACH_ODE_SYSTEM_FULL.txt`, `EH_ODE_SYSTEM_FULL.txt`.

**Stamps carried by EVERY conclusion in this document (F-C6):**

- Comparison domain: **CHOSE** (the registered stationary family; the stamp travels).
- C2/Bach candidate: `UNIQUE_CONDITIONAL_ONLY_IF_STRONG_CSN_RETAINED`; strong CSN is
  `CHALLENGED_OWNER_POSTULATE_NOT_DERIVED` (G04/G10) — an INACTIVE conditional branch.
- EH+Λ candidate: `CONDITIONAL_NOT_SELECTED` (G11); the EH-H3 spatial-infinity
  normalization is INADMISSIBLE for native finite cells and is NOT used anywhere here.
- No action is adopted, no mass claimed, no normalization chosen, no carrier adopted,
  no physics branch selected. Vacuum restricted equations only.

---

## TC1 — the declared comparison domain (census, chose-or-derived)

Base arena (registered stationary family, quoted from
`udt_higher_isometry_plane_ownership_audit_2026-07-28/PREREGISTRATION.md` lines 20–32):

```
g = -u (c_E dt + alpha A)^2 + u^{-1} A^2 + q_B,   u = e^{-2 phi} > 0
```

on `R_t x S^3` with `A = sigma_3` (registered Hopf connection), and its `R x T^2`
stratum with connection moment `f = A(Y)` and horizontal norm `b = q_B(Y-fV, Y-fV)`.

Concrete chart used (the local toric chart of the `R x T^2` stratum; the curvature
comparison is local, and the `R_t x S^3` Hopf members are contained in this chart as
specific profiles of `f` and `bh` — e.g. the round-fiber form has `f ~ cos(theta)`,
`bh ~ sin^2(theta)` with `x = theta`):

```
A   = dz + f(x) dy
q_B = e^{2 lambda phi} ( dx^2 + bh(x) dy^2 )          <- the symbolic transverse seat
g   = -u (c_E dt + alpha A)^2 + u^{-1} A^2 + q_B
```

Componentwise, in coordinates `(t, x, y, z)` with `q := u^{-1} - alpha^2 u` and
`W := e^{2 lambda phi}`:

```
g_tt = -c_E^2 u        g_ty = -c_E u alpha f      g_tz = -c_E u alpha
g_xx = W               g_yy = q f^2 + W bh        g_yz = q f
g_zz = q
```

Check C01: `det g = -c_E^2 bh W^2 = -c_E^2 b W` with `b = W bh` — exactly the
plane-ownership audit's orbit Gram determinant `-b c_E^2` times the transverse leg
(consistency with the registered family's banked A01).

Census table (every choice tagged; contract §5 restated with the chart additions):

| Object | Status | Tag |
|---|---|---|
| Registered stationary family + `R x T^2` stratum as the arena | comparison domain | **CHOSE** (stamp travels on every conclusion) |
| Local toric chart `(t,x,y,z)`, fields functions of `x` only | chart of the declared stratum | CHOSE-chart (Category-A; local; loses no local content) |
| Transverse gauge `g_xx = e^{2 lambda phi}` exactly (no separate free `g_xx`) | coordinate gauge (x-reparametrization) | Category-A conditioning (gauge, not physics) |
| `u = e^{-2 phi}`, reciprocal `u`/`u^{-1}` pair on the `(t,z)` legs | registered family structure | THEORY (registered; the audited descended block) |
| Screen legs `∝ e^{lambda phi}`, `lambda` SYMBOLIC | transverse seat NOT frozen | DERIVED-necessity (G08 OPEN; 07-26 rank-zero bank; freezing = scar) |
| `phi(x), f(x), bh(x)` free fields; independent jets | varied-field census | free-and-explored |
| `alpha`, `c_E` constants (symbolic) | registered family data | CHOSE-constant (registration: constant `alpha`; no value picked) |
| `Lambda` symbolic, never fitted | EH+Λ candidate datum | THEORY-conditional (G11) |
| Bach equation = unrestricted variation of `√|g| C^2` | C2 side equation | THEORY-conditional (banked 07-20: "unrestricted bulk equation is proportional to the Bach tensor"); strong-CSN CHALLENGED stamp travels |
| `E_ab = G_ab + Lambda g_ab` = unrestricted variation of `√|g|(R-2Lambda)` | EH side equation | THEORY-conditional (standard unrestricted variational output; CONDITIONAL_NOT_SELECTED) |
| Full-vary-then-restrict order | method | THEORY (requirement 12; EH-RED scar; F-C1) |
| Vacuum comparison; source side typed-only (TC5 note) | scope | THEORY (authority boundary; G09 carrier = POSIT) |
| CM0-C excluded (equations unwritten) | recorded exclusion | RECORDED-EXCLUSION (census row; MAP L6 unaffected) |
| SymPy exact, CPU, single process, deterministic | conditioning | Category-A (soundness only) |

The overall nonzero constant multiplying each variational output is convention-dependent
(signature/orientation); every verdict below is invariant under nonzero constant
rescaling of either equation set (the vanishing loci are what is compared; where
PROPORTIONAL would have been found, the exact factor would have been reported).

## TC2 — the Bach equation restricted to the domain

Order of operations (F-C1): the **unrestricted** metric variation of
`√|g| C_abcd C^abcd` is the known covariant output — the equation proportional to the
Bach tensor

```
B_ab = ∇^c ∇^d C_acbd + (1/2) R^cd C_acbd
```

(banked provenance: `c2_finite_cell_boundary_variation_2026-07-20/AUDIT_REPORT.md`).
This covariant tensor is then EVALUATED componentwise on the domain metric — restriction
strictly after variation. Nothing here varies a pre-restricted action.

Restriction structure found (all zero-residual checks in the script):

- The mixed transverse row vanishes identically: `B_ax = 0` for `a ∈ {t, y, z}` (C10).
- `B_ab = B_ba` and `g^{ab} B_ab = 0` exactly on the domain (C08, C09) — the trace
  identity removes one of the seven surviving components.
- The seven surviving independent components are `B_tt, B_ty, B_tz, B_xx, B_yy, B_yz,
  B_zz` — including the lapse row `B_tt` and the momentum rows `B_ty, B_tz` (F-C2).
- Jet structure (C11): every component carries 3rd/4th x-derivative jets of
  `(phi, f, bh)`; the radial row `B_xx` is the lower-order (constraint-type) row.

The full exact ODE system (each component as an explicit polynomial in the jets
`p0..p4 = phi..phi''''`, `f0..f4`, `h0..h4 = bh..bh''''`, with `alpha, c_E, lambda`
symbolic and `u = e^{-2 p0}`, `W = e^{2 lambda p0}`) is written, component by component,
in `BACH_ODE_SYSTEM_FULL.txt` (it is the deliverable; the expressions run to thousands
of terms and are reproduced there verbatim, not paraphrased). The jet signatures per
component are in `routeC_stage1_results.json` (`jet_signatures.bach`).

## TC3 — the EH+Λ equation restricted to the domain

Unrestricted metric variation of `√|g| (R - 2 Lambda)` gives the covariant output
proportional to `E_ab = G_ab + Lambda g_ab` (Λ symbolic throughout, never fitted);
evaluated on the domain metric strictly after variation. Same seven independent
components; the restriction satisfies the contracted Bianchi identity
`∇_a G^{ab} = 0` exactly (C07 — soundness of the restriction). Jet structure: no
component carries any jet above 2nd order; `E_xx` is the 1st-order radial constraint.
Full system: `EH_ODE_SYSTEM_FULL.txt`.

## TC4 — component-by-component comparison (verdict: OC1, INEQUIVALENT)

**Pre-registered logical asymmetry (quoted):** inequivalence on this domain is DECISIVE
against exact sector-sharing for this pair — "an inequality on a subfamily refutes
equality on any superset — scoped to the compared pair and premise set." Agreement
would have been SCOPED-ONLY under the KER-R bound: "Static restriction cannot
determine all four-dimensional terms."

Verdict: **every one of the seven components is INEQUIVALENT**, with explicit exact
witnesses in BOTH directions, each verified by zero-residual substitution
(`SECTOR_COMPARISON_LEDGER.tsv` holds the full witness data; summary):

- **Direction A (per component):** a configuration with `B_comp = 0` exactly and
  `E_comp ≠ 0`. Construction: all jets at fixed rational values (`p0 = 0` keeps every
  exponential at 1, so all arithmetic is exact rational), the top jet solved linearly
  from `B_comp = 0`. Since no EH component contains 3rd/4th jets, `E_comp` is untouched
  and evaluates to `p + Lambda q` with `q ≠ 0`: nonzero for every `Lambda` except the
  single exceptional value `Lambda* = -p/q`. TWO witnesses with distinct `Lambda*` are
  given per component, so for EVERY `Lambda` at least one witness has
  `B_comp = 0 ≠ E_comp`.
- **Direction B (per component):** a configuration with `E_comp = 0` for SYMBOLIC
  `Lambda` (a low-order jet solved exactly as a rational function of `Lambda`) and
  `B_comp ≠ 0`. The two witnesses' Bach values are polynomials in `Lambda` with NO
  common root (exact gcd check), so for EVERY `Lambda` at least one witness has
  `E_comp = 0 ≠ B_comp`. For the radial constraint row `xx` no jet enters linearly —
  at `p0 = 0` the restriction gives EXACTLY
  `E_xx = [4Λ h0 + (α²−1) f1² − 4 h0 p1²] / (4 h0)` (verified zero-residual; `λ` and
  `h1` drop out) — so the witness uses the exact even-parity construction: `B_xx` is
  even under flipping all f-jets (an exact discrete-isometry check); with only `f1`
  nonzero among the f-jets, substitute `f1² = 4 h0 (Λ − p1²)/(1 − α²)`, which solves
  `E_xx = 0` identically for symbolic `Λ` and is a real domain point wherever
  `f1² ≥ 0`. THREE such witnesses with validity intervals `[0,∞)`, `(−∞,1]`, `(−∞,4]`
  cover every real `Λ`, and every real root of one witness's Bach numerator inside its
  validity interval is covered by another valid witness with gcd-coprime numerator
  (exact real-root isolation).
- **PROPORTIONAL / IDENTICAL are excluded** by the witness pairs: any relation
  `E = ρ·B` (or `B = ρ·E`) with nonzero factor `ρ` — constant or function — is
  contradicted at a witness where one side vanishes and the other does not.

**System-level witnesses** (the comparison does not rest on any single component, nor
on static energy, nor on the E2+E4 restriction — F-C2):

- **W-FLAT** (constants member `phi, f, bh` constant): Riemann `≡ 0` (C12), so
  `B_ab ≡ 0`, while `E_ab = Lambda g_ab ≠ 0` for every `Lambda ≠ 0` (C13).
- **W-EXP** (exponential member of the domain: `phi = x`, `bh = e^{2x}`, `f = 0`,
  `alpha = 0`, `lambda = -5/4`): the FULL Bach system vanishes identically, the Weyl
  tensor is NONZERO (not conformally flat — genuine Bach-flatness, not the trivial
  Weyl-flat case), and the trace-free Ricci tensor is nonzero — hence
  `G_ab + Lambda g_ab ≠ 0` for EVERY `Lambda`, including `Lambda = 0` (C16).
  This member solves the complete restricted C2/Bach system and fails the complete
  restricted EH+Λ system for every value of Λ.
- **W-EXP-CF** (branch point `phi = x`, `bh = e^{4x}`, `f = 0`, `alpha = 0`,
  `lambda = -1`): a CONFORMALLY FLAT (Weyl ≡ 0) non-Einstein member — Bach vanishes
  trivially, `G + Λg ≠ 0` for every Λ (C16c). The domain thus contains both trivially
  and nontrivially Bach-flat members that EH+Λ excludes.
- **Slice structure behind W-EXP** (C17, C17b, C18; SCOPED to the exponential
  subfamily `phi = kx`, `bh = e^{2sx}`, `f = 0`, `alpha = 0`, `k = 1` scaling gauge):
  every deweighted Bach component is divisible by `(4 lambda s + s^2 + 4)` — a
  ONE-PARAMETER Bach-flat branch, and the slice Bach-flat locus is this branch
  **ALONE** (A1 correction, 2026-07-28: an earlier wording claimed a separate
  "discrete root pair `lambda = ±5√21/21, s = ∓2√21/7`" — that pair is a redundant
  `sp.solve` output that satisfies `4λs + s² + 4 = 0` exactly, i.e. it lies ON the
  branch; zero-residual check C17b; the verifier's Gröbner basis of the quotient
  system, `{s − 2λ, 3λ² + 1}`, has no real solutions — `VERIFIER_INDEPENDENT_CHECK.py`
  V13c); the EH+Λ system on the same slice has NO roots at
  `k = 1`, and the flat member solves it only with `Lambda = 0`.
  Two structural observations reported (not verdicts): (i) the Bach-flat branch exists
  only because the `lambda` seat is unfrozen (`lambda·s = -(s^2+4)/4 < 0` is
  unsatisfiable at `lambda = 0`); (ii) the reciprocal `u`/`u^{-1}` lock on the `(t,z)`
  legs makes the restricted EH+Λ system rigid on this slice (flat only), while the
  4th-order Bach system is not.
- **Containment side (one-way sharing, stated precisely, F-C4):** every EH+Λ solution
  in the domain is expected to solve the Bach system (the standard 4D fact
  "Einstein ⇒ Bach-flat" — cited as Category-A mathematics, verified here only on the
  slice members, NOT re-proven on the full ansatz). The witnesses above show the
  converse FAILS: the two restricted equation sets are not equal, and the Bach system
  admits domain members the EH+Λ system excludes for every Λ. "Shares solutions
  one-way" is NOT "the same exact finite-cell static equations" — which is what
  condition 2 of the 07-18 fork requires.

**Outcome class: OC1** — exact inequivalence with witnesses. Scope stamps travel: the
domain is CHOSE; the C2 side is strong-CSN-CHALLENGED conditional; the EH side is
CONDITIONAL_NOT_SELECTED; the negative is pair-scoped (other pairs and the CM0-C
completion are untouched — this is NOT "route dead").

## TC5 — boundary typing ONLY (condition-4 data; no derivation, no boundary law chosen)

Typed against the join classes of `udt_finite_cell_completion_atlas_2026-07-21/
JET_MATCHING_ATLAS.tsv` (J07 = ANALYTIC_JOIN: "convergent local expansions agree /
analyticity is an extra premise"; J08 = DISTRIBUTIONAL_JOIN: "finite jumps with declared
weak geometry / junction functional and products open").

**C2/Bach side** (banked facts quoted from
`c2_finite_cell_boundary_variation_2026-07-20/AUDIT_REPORT.md`; nothing re-derived):

- Curvature momentum `P^abcd = 2 C^abcd`; boundary symplectic potential
  `Θ^μ = 4 C^{μabν} ∇_ν(δg_ab) − 4 ∇_ν C^{μabν} δg_ab`.
- On a non-null piece in Gaussian normal gauge:
  `n·Θ = −8ε E^ij δK_ij + Π_h^ij δh_ij + 4ε D_k(C^{nijk} δh_ij)`, with `E^ij = C^{ninj}`
  trace-free and edge flux `4ε s_k C^{nijk} δh_ij`.
- **Condition-4 data needed (typed):** the induced metric `h` AND the extrinsic
  curvature `K` as independent boundary data (a two-jet wall), momenta involving
  `∇C` (up to THIRD normal derivatives of the metric entering the boundary flux),
  plus CORNER data on codimension-2 edges. A smooth finite-cell completion is a
  J05/J06-class matching on jets through the order the flux sees (k ≥ 3), with J07
  (ANALYTIC_JOIN) only under the extra analyticity premise; a wall/shell completion is
  a J08 (DISTRIBUTIONAL_JOIN) with the "junction functional and products open" limit —
  for a 4th-order equation the weak-geometry products are harder than Israel-type and
  are OPEN. Charge structure: any physical charge additionally needs an integrable
  primitive, reference, orientation, improvement, and normalization (quoted); on
  conformally flat members the bare `C^2` boundary charge is ZERO (banked) — the bare
  boundary objects cannot select scale there.
- The 07-20 decisive negative stands: several inequivalent polarizations (clamp
  `(h,K)`; fix `h` + natural trace-free electric-Weyl equation; fix `K` + complementary
  momentum equation; both-free + corner condition; mixed/Neumann; conformal-class data)
  all make the problem differentiable and **current UDT premises select NONE of them.**

**EH+Λ side** (typed only; standard structure, no EH-H3 normalization imported):

- First-order boundary data: induced metric `h` with conjugate momentum built from `K`
  (GHY-type primitive), corner (Hayward-type) data at codimension-2 joints; the flux
  sees jets through FIRST normal derivative. Smooth completion: J05-class with k ≥ 1
  (J02/J03 value/first-jet matching at the generator); distributional completion:
  J08 Israel-type junction — better-controlled products than the 4th-order case but
  still carrying the atlas's "junction functional and products open" limit for a native
  finite cell. Reference/normalization for any charge: OPEN natively (the EH-H3
  spatial-infinity normalization is inadmissible here and is not used).

**Typed mismatch (recorded, not adjudicated):** the two actions require condition-4
data of DIFFERENT jet order (2-jet wall + 3rd-derivative momenta + trace-free-Weyl
corner structure vs 1-jet wall + K-momenta + Hayward corners). Even componentwise bulk
agreement would not have delivered condition 4 — and conversely, the TC4 bulk verdict
is robust against boundary-primitive shifts, per the BDY-TD threat row (quoted):
"Actions differing by total derivative/boundary primitive: bulk equation can remain
while momentum and charge shift." No boundary law is chosen here.

## TC6 — re-grade of the 07-18 OPEN fork (per Stage-1 evidence only)

The 07-18 record's six conditions (quoted in the contract §1) with Stage-1 status:

| # | Condition | Stage-1 status |
|---|---|---|
| 1 | two inequivalent COMPLETE actions passing every gate | UNTOUCHED (still ZERO complete-admissible candidates; the compared pair is conditional-only) |
| 2 | one declared domain and the SAME exact finite-cell static equations on both | **FAILS for this pair on this domain** — component-wise INEQUIVALENT with exact witnesses; by the pre-registered asymmetry the failure extends to any superset domain containing the registered family |
| 3 | same carrier-to-source variation | untyped here beyond scope note (vacuum comparison; the non-equivalent source identities `ρ+S=2ρ₄` vs `ρ+p_∥=2(ρ₂∥+ρ₄∥)` remain separate typed rows; no carrier adopted) |
| 4 | same differentiable boundary generator/topology/reference/orientation/normalization | TYPED ONLY (TC5): the two actions demand different-order boundary data; nothing selected |
| 5 | compatible nontrivial finite-cell solutions + global closure | NOT ADDRESSED (Stage 1 is equation-level) |
| 6 | controlled weak/static limit with uniform remainder | NOT ADDRESSED |

**Re-grade: CLOSED-for-this-pair (scoped).** For the pair (C2/Bach conditional,
EH+Λ conditional) on the declared CHOSE domain — and, by the subfamily-refutes-superset
asymmetry, on any static domain class containing it — condition 2 cannot be satisfied:
the two conditional actions do NOT share the exact static sector. The FORK ITSELF
REMAINS OPEN with narrowed conditions: a shared-static-sector theorem, if it exists,
must come from a DIFFERENT pair — e.g. the unwritten CM0-C nonvariational completion
(recorded exclusion), a KER-R kernel deformation of a completed base action (actions
differing by terms in the static kernel), or BDY-TD boundary-primitive variants of ONE
bulk action (which share the bulk sector trivially but differ in momenta/charges —
condition 4 is then the whole fight). Not "route dead" (F-C4 respected).

**S26 re-stamp (re-stamped, NOT discharged; no mass claim):** the S26 conditional row
("EH-conditional weak source/lapse mass M_N^(0)=2E4"; unlock leg: "Native branch
adoption or shared-sector theorem plus normalization") has its SECOND unlock leg
re-stamped: `SHARED-SECTOR-THEOREM: UNAVAILABLE-VIA-THE-(C2/Bach, EH+Λ)-PAIR-ON-THE-
REGISTERED-DOMAIN (Stage-1 witnesses; scoped)`. The leg survives only through a
different pair/completion; the first leg (native branch adoption) is untouched. S26
remains CONDITIONAL.

---

## Run record

`python3 derive_routeC_stage1.py` (grok, 2026-07-28; post-amendment A1/A2 rerun):
**33/33 checks PASSED, exit 0**, ~48 s single-process CPU; transcript preserved as
`DERIVATION_STDOUT.txt`. A second full run produced a byte-identical results JSON
(elapsed-time field aside) — deterministic. THROUGHPUT: the FULL
`(u, f, bh, alpha; lambda)` family was computed; the pre-declared bounded fallback
(diagonal strata reduction) was NOT needed and no THROUGHPUT-LIMITED stamp applies.
Check list: C01–C13, C14/C15 per component (7×2), C16/C16b/C16c, C17, C17b (A1
amendment check), C18 — all exact zero-residual SymPy assertions. (Pre-amendment run:
32/32 PASS; the amendment added C17b and changed no prior check or witness —
`CORRECTION_LAYER.md`.)

## Falsifier compliance record

- **F-C1**: no restrict-then-vary anywhere; both covariant tensors are the unrestricted
  variational outputs, evaluated after. PASS by construction (order visible in script).
- **F-C2**: verdict rests on all seven components including lapse `tt` and momentum
  `ty`, `tz` rows; system witnesses W-FLAT/W-EXP kill the full system, not an energy
  restriction. PASS.
- **F-C3**: all checks are exact zero-residual assertions; script exits nonzero on any
  failure. See run summary in `routeC_stage1_results.json`.
- **F-C4**: inequivalence stated pair-scoped (not "route dead"); one-way solution
  containment stated separately; no agreement promoted (none found); slice findings
  stamped SCOPED to the exponential subfamily.
- **F-C5**: no merit criteria anywhere (no solution filtered for shape); no
  spatial-infinity normalization imported; witnesses are provenance/honesty-checked
  configurations, not preferred solutions.
- **F-C6**: stamps restated at the head of this document and in every TC section's
  conclusions; JSON carries the same stamps.
