# Uniqueness-consumer and exchange-origin audit — AUDIT REPORT

Date: 2026-07-28. Branch: `review/external-perspective-2026-07-28` (worktree at `0659101`;
`grok` untouched). Preregistration: `PREREGISTRATION.md` (committed `3c6ffc8` BEFORE any
adjudication ran). CPU-only document/derivation audit; no solve, no GPU, no canonization.

**GRADE: VERIFIED-WITH-CAVEATS** — the blind adversarial pass (zero-context-framed, but a
same-session-spawned agent, NOT a hosted external model — the distinction is stated per this
audit's own META finding on grade-string conflation) CONFIRMED all three load-bearing verdicts
with independent sympy rederivations and a surviving spot-check; three non-fatal scope/
provenance tightenings were found and are folded into this report. Full record in §Verifier
record.

## Result first

**Both preregistered falsifiers FIRED. The audit's outcome is (b): the localized requirement,
not the driver's proposed unified reading.**

- **F1 fired exactly once**, on D1 (`udt_killing_plane_strata_transition_audit_2026-07-28`):
  a CONSUMES-UNIQUENESS verdict at the `alpha*df != 0` stratum. Fourteen other adjudicated
  consumers are DESCENDS / EQUIVARIANT-discharged / OUT-OF-SCOPE, and the C09 positive control
  passed by a genuine argument (criteria calibrated).
- **F2 fired twice** (N2, N4): the external review return's central conjecture — that the five
  July no-selector results are ONE reciprocity-rooted Z2 theorem seen five times — is
  **REFUTED**. The review return's §0 reading is hereby withdrawn as stated.

The refutation is productive: it replaces the unified reading with a sharper three-family
structure and a concrete, bounded, metric-led derivation target (below).

## Q2: the three-family origin structure (replaces the refuted unified reading)

- **Family A — genuine reciprocity-exchange** (N1 fully; N5's base layer): on the reciprocal
  diagonal, `phi -> -phi` acts exactly as the transposition J on the angular character pair
  (`H(-phi) = J H(phi) J^T`); its fixed locus fixes the metric but no member. One theorem, seen
  twice.
- **Family B — an independent lattice-sign Z2** (N4's plane exchange; N5's lift ambiguity): the
  element `diag(1,-1)`. Decisive computation (N4 witness): the plane-exchange isometry fixes
  `f = cos 2eta`, hence fixes `u = e^{-2phi}`, hence **fixes phi pointwise** — and `phi -> -phi`
  is not even an isometry of that witness. The plane swap exchanges which spatial circle
  partners K as ruler, with the reciprocal relation invariant on both sides.
- **Family C — non-exchange underdetermination** (N2 entirely; N3's core): no group at all —
  missing slice/branch/observer data and the perfectness of so(1,3) (two boosts generate a
  rotation), plus the swap-invariant continuous lambda modulus.

**New structural datum surfaced by the refutation:** the reciprocity transposition J and the
lattice sign element `diag(1,-1)` together generate the exact order-eight signed-permutation
stabilizer of the character pair — and the packages' unselected residues (N4's plane, N5's
lift) live precisely in the **sign coset that the reciprocity swap cannot reach**. What the
kinematics leaves unselected is not "the founding symmetry's orbit" but a specific
lattice-sign degree of freedom invisible to reciprocity.

## Q1: the consumer table

| Consumer | Verdict |
|---|---|
| C01 delta_K depth | EQUIVARIANT (tau = sign flip; discharged — downstream sign-agnostic) |
| C02 WR-L + SNe readout | DESCENDS (swap = relabeling; banked chi2 invariant; orientation pinned by OBSERVED redshift) |
| C03 X_max schema | DESCENDS (pair-symmetric by registered requirement S07) |
| C04 abs(c1)=1 Hopf prototype / G13 | DESCENDS (unit classes banked as the pair Q = +-1; "Does it choose chirality? NO") |
| C05 N22/T18 bridge rows | DESCENDS (current stamps are NO_SELECTION gate chains; member choice quarantined in their own open lists) |
| C06 handoff seat phi=0 | DESCENDS (fixed locus; member choice at the tie provably impossible; pair carried through) |
| C07 hopfion/carrier bridge (G09/G15) | DESCENDS (claims at abs(Q)/absolute-class/selector-OPEN level; G15 premise chain member-free) |
| C08 bootstrap G12 | OUT-OF-SCOPE (references only OPEN placeholders) |
| C09 pair module (CONTROL) | DESCENDS at module level — control PASSES; lift sub-claim EQUIVARIANT, discharged at abs(c1)=1 |
| **D1 Killing-plane strata** | **CONSUMES-UNIQUENESS — F1 fires** (see below) |
| D2 intrinsic-ruler descent | EQUIVARIANT (mirror-covariant; twist selector vanishes exactly on the exchange locus; inheritor = D1) |
| D3 calibrated readout | DESCENDS-after-DERIVED-breaking (Lorentzian signature forces clock = timelike eigenline, conditional on aligned readout) |
| D4 screen-response atlas | DESCENDS (conditional-on-supplied-pair; signs declared gauge) |
| D5, D6 lambda classifiers | DESCENDS (stratum-labeled classification; explicit non-selection) |

## The F1 finding (D1), exactly

D1 banks "Conditional on the registered `(K,V)` Killing plane … timelike clock: K, response
`-2X(phi)`; spacelike ruler: `V - (alpha/c_E)K`, response `+2X(phi)`" and the stamp
`UNIQUE_METRIC_FOUNDED_CLOCK_AND_RULER_LINES`.

- **At `alpha*df != 0`** the claim does not survive `V -> Y`: restricting the parent's exact
  3x3 Gram/response to `span(K,Y)`, K acquires a nonzero off-eigenline component
  `-alpha c_E df u^2/(b u + f^2)` — verifier-confirmed FULLY GENERAL in the family — and the
  spectra of the two members differ (`det D_KV = -4chi^2` vs
  `det D_KY = -4chi^2 + alpha^2 u^2 df^2`), so no involution tau on outputs exists. On the
  constant-determinant witness stratum (`b*u + f^2 = 1`) the rate shift is exactly the parent's
  own `det D_KY + 4chi^2 = alpha^2 u^2 df^2` with eigenvalues complex where
  `alpha^2 u^2 df^2 > 4chi^2` (witness-scoped per the verifier; the general criterion is
  `tr^2 < 4 det`). Independently rederived symbolically twice (adjudication + blind verifier).
  D1 declares the conditionality honestly (its S09), but the frozen criteria contain no
  declared-conditionality exemption: the member choice load-bears. **CONSUMES-UNIQUENESS.**
- **At `alpha = 0`** (the exchange-symmetric stratum) the clock output K DESCENDS — it is the
  shared, exchange-fixed line of both planes — and the ruler output is EQUIVARIANT
  (pair-valued), exactly the parent's `UNIVERSAL_SELECTION_REFUTED`.

**The localized requirement (F1's deliverable — a proposal, NOT authorized by this audit):**

1. **`alpha*df != 0` selector theorem (bounded, metric-led, plausibly derivable):** where the
   twist is on, the two topology-supplied planes are metrically INEQUIVALENT, and the intrinsic
   "K-is-an-eigenline with founded rates `+-2chi`" property provably distinguishes `span(K,V)`
   from `span(K,Y)` in the parent's own witness. Promoting that property to a fixed-metric
   selector theorem on the `alpha*df != 0` stratum would close the parent's
   `GENERIC_FIXED_METRIC_SELECTION_OPEN` exactly where a selector can exist. Falsifier: exhibit
   an admissible `alpha*df != 0` metric where BOTH planes carry K as eigenline with founded
   rates. Maximum conclusion: a conditional fixed-metric plane-selection theorem inside the
   registered constant-alpha family — no branch, action, carrier, or physics selected.
2. **`alpha = 0` pair-valued restatement:** re-express D1's deliverable as clock K (member-free)
   plus the unordered ruler pair `{V, Y}` — where selection is provably impossible, stop
   demanding it.

## What this does to the review return's recommendation

- §0's "one theorem five times" reading: **WITHDRAWN** (F2).
- "The kinematic selector hunt is finished": **CORRECTED** — it is finished for thirteen of
  fifteen consumers *by their own construction* (their authors pre-fenced member selection and
  the fences held under explicit swap arguments); it is genuinely OPEN for exactly one (D1),
  where it is now a localized, bounded target with a candidate derivation.
- "The gate is P4": **SURVIVES with corrected justification** — not because uniqueness is
  symmetry-forbidden everywhere (it is not: signature already breaks the founding exchange at
  the aligned layer, D3; observation anchors the orientation, C02; twist can break the plane
  pair, D1), but because Family C's obstructions are underdetermination whose missing data
  (variation domain, native response, branch) are P4 objects.
- The positive kinematic finding stands and is sharper than before: **the founding clock/ruler
  exchange is broken exactly where derived structure (signature, twist) or observed data
  (redshift) break it, is carried as an explicit pair everywhere else, and the residues the
  kinematics cannot reach live in the lattice-sign coset.**

## Caveats and owed checks

- META-1: the explicit witness-exchange map `(z1,z2) -> (z1, conj(z2))` was quoted by one agent
  from N4's `FRESH_ADVERSARIAL_REVIEW.md` while the census located the explicit formula only in
  the external review return; the phi-fixing computation is independent of which document
  states the map, but the citation must be pinned by the verifier.
- META-2: same-session adjudication throughout; grade capped at PROVISIONAL until the blind
  fresh-context verifier pass below is recorded.
- Every verdict inherits the parent registrations (P06/P07/P14-class CHOSE: block-screen
  coframe, stationarity, registered Hopf lattice, constant alpha) and the founding-readout
  conditionality (D3's aligned-readout condition; on the mixed-readout route the role question
  dissolves rather than being decided).
- Nothing in this audit selects a physical branch, action, source, carrier, density law,
  dynamics, or mass. Nothing on `grok` changes. Canonization is not requested.

## Verifier record

Blind adversarial pass, 2026-07-28, zero-context-framed same-session agent (scripts
`v1_gram.py`, `v2_witness.py`, `v3_readout.py`, sympy/mpmath). Instructed to BREAK the three
load-bearing verdicts with no knowledge of which outcomes the driver proposed.

- **V1 (D1 CONSUMES-UNIQUENESS + the distinguishing sub-lead): CONFIRMED.** Independent Gram
  rebuild verified `det G3 = -b c_E^2`; `D_KV = [[-2chi, -4*alpha*chi/c_E],[0, 2chi]]` for ALL
  alpha (clock/ruler eigenstructure exact on the registered plane); the (K,Y) off-eigenline
  component `-alpha*c_E*df*u^2/(b*u+f^2)` is exact and **fully general** (the load-bearing
  distinguishing claim needs no witness restriction); no intertwining tau exists
  (`det D_KV = -4chi^2` vs `det D_KY = -4chi^2 + alpha^2 u^2 df^2` differ whenever
  `alpha*df != 0`). SCOPE TIGHTENING (folded in): the identity
  `det D_KY + 4chi^2 = alpha^2 u^2 df^2` and the complex-eigenvalue threshold are exact only on
  the constant-determinant witness stratum (`b*u + f^2 = 1`); the general-family criterion is
  `tr^2 < 4 det` with `tr = X(ln(b*u+f^2)) != 0`. The "identical Gram at alpha=0" clause is
  witness-specific (generally the YY entry is `f^2/u + b`).
- **V2 (N4 DISTINCT-ORIGIN): CONFIRMED, with a package justification gap closed.** Direct
  computation: the witness assembles to `-c_E^2 u dt^2 + u^{-1}(round S3)`; the map
  `xi2 -> -xi2` is an isometry, swaps V and Y, and fixes eta, f, u, phi POINTWISE; on the cap
  lattice it is `diag(1,-1)`. META-1 PINNED: the explicit map `(z1,z2) -> (z1, conj(z2))`
  appears ONLY at `udt_higher_isometry_plane_ownership_audit_2026-07-28/FRESH_ADVERSARIAL_REVIEW.md:28`;
  `EXACT_DERIVATION.md:257` says only "an isometry exchanges them" — citations must point to
  the review file. GAP CLOSED: the package's one-line `phi -> -phi` non-isometry argument
  (value ranges of u) is incomplete alone (Killing normalization rescales u); the verifier
  closed it with a normalization-free invariant — Ricci-scalar ranges [5.40, 10.80] vs
  [1.20, 6.04] at eps=0.3 — so the non-isometry stands on a diffeomorphism invariant.
- **V3 (D3 derived signature breaking): CONFIRMED AND STRENGTHENED.** Full rederivation of
  B=0 forcing, `C = A b^2` isometry condition, and the conformal kill (`Omega^2 = 1`); the
  verifier generalized the theorem beyond the package's F_b to ALL eigenline-swapping linear
  maps `M = [[0,b],[c,0]]` (isometry or conformal), each forcing `sign(A) = sign(C)`,
  contradicting `AC < 0` — no false pass hides in the normalization. Mixed witness verified
  (`H=[[1,-2],[-2,1]]`: swap IS an isometry, both eigenlines spacelike, question dissolves
  outside the aligned class, consistently). Summary "derived-not-chosen, conditional on the
  aligned readout" ruled accurate, not an overclaim.
- **Spot-check (verifier's choice: C04 chirality): SURVIVES.** No signed flux banked anywhere
  found (atlas rows use `abs_c1`; both unit classes recorded; "Does it choose chirality? NO"
  verbatim); the 2k+1 countermodel family is exchange-symmetric with `det = 2k+1` verified.

Slips found: three, all non-fatal, all folded into this report (V1 witness-stratum scoping;
V2 justification gap + META-1 pin; no fatal misquotes or sign errors). Verdict: the audit's
classifications stand as scoped.
