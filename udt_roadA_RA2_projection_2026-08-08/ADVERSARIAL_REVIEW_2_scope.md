# RA2 ADVERSARIAL REVIEW 2 — F-RETRO/ordering + freedom-accounting honesty + F-TEMPLATE/scope

Date 2026-08-09 | Review agent 2 (Fable, hostile) | Brief: ordering audit, freedom accounting,
PARTIAL-landing honesty both directions, stamps, repairs. Independent machine work performed
(re-run, diff, token audit, witness-provenance check, R4 q-sweep). NOT committed.

## 1. F-RETRO / phase ordering (primary) — DISCHARGED, with one wording repair and one flag

**Hard form: CLEAN.** Independently verified: prereg committed e0355637 23:36:52 EDT before all
artifacts. Birth/mtime chain: run_output.txt BORN 23:50:56 (Phase-1 run), __pycache__ 23:52:16,
PHASE1_NOTES.md (marker) 23:55:51 → derive_ra2.py 23:57:31 → Phase-2 output append 23:57:38 →
PHASE2_COMPARISON.md 23:58:16. My own token audit of all Phase-1 artifacts (220/2.43/2.44/310/
538/809/1147/1446/1779/2075/Planck): CLEAN — the only "2.4" is the derived R4 ratio 2.4235.
- **Wording repair (A1):** DERIVATION_NOTES §4 "No Phase-1 file was edited after the marker" is
  imprecise: derive_ra2.py was REWRITTEN (new inode, birth=23:57:31) at the Phase-2 append and
  run_output.txt appended — mtimes alone cannot certify the Phase-1 section's integrity. I closed
  the gap myself: a fresh `phase1` run reproduces the banked Phase-1 block BYTE-EXACTLY (diff
  clean, 23/23). Amend to: "PHASE1_NOTES untouched after the marker (mtime); the Phase-1 script
  section certified by exact re-run reproduction, not by mtime."
- **Subtle form — two Phase-1 choices sit in foreknowledge-sensitive positions.** The prereg's own
  MAP-§4 pre-statement ("~2.4:1") was in context during Phase 1 BY DESIGN, and via the Phase-1
  rigidity formula β=(2−ρ₁)/(ρ₁−1) it implies target β≈−0.29. (i) The Dirichlet "canonical
  representative" (P-RA2-5) was declared in Phase 1, NOT the prereg; its band contains the target,
  the Neumann band (+0.13…+0.20) does not. Mitigation accepted: Friedrichs/Dirichlet is the
  standard mathematical canonical choice, and the Neumann variant + full Robin span were computed
  and ledgered blind. (ii) **The R4 witness moved, undisclosed:** RA1's R4 witness is (n=3,q=−2)
  (derive_ra1.py:141); RA2 used (3,−3/2), yet P-RA2-7 cites "the O2/RA1 witness pattern". My
  independent sweep: q=−2 gives ρ₁=1.514 (structurally different/likely numerically pathological
  ladder — a defensible Category-A reason to move, but it is nowhere stated); q=−1.0/−1.25/−1.5
  give ρ₁=2.502/2.445/2.424 — the region's ratio range SWEEPS THROUGH the measured 2.4393.
  Neither item voids the comparison (the ~2.4 disclosure was the protocol's own anti-dressing
  device); both CAP the evidential weight of K2/K5 — amendments A3/A4 below are mandatory.

## 2. Freedom accounting — ONE FALSE CLAUSE, otherwise verified

- **A2 (mandatory): "parameters actually fitted = 1 (scale)" is FALSE per the code.** Lines
  305–307 least-squares fit TWO parameters (a and intercept → β=−0.3063 is FITTED, then checked
  in-band). Honest form: "2 parameters fitted (scale + offset); 7 positions matched at 1–3%
  (5 residual dof); the FITTED offset falls inside the pre-declared Dirichlet band." "6
  independent ratios matched" with 1 parameter would require β FIXED from the band — not what ran.
- "No (n,q,h₀) scan": TRUE of the code (5 fixed witnesses only). "Robin freedom NOT spent": TRUE
  as no Robin sweep ran — but the binary Dirichlet-vs-Neumann representative selection is itself
  one bit of that freedom, spent in Phase 1 (see 1.ii); say so.
- **A3: the band-hit claim.** Band honesty: code BAND=(−0.42,−0.26) vs Phase-1's −(0.26…0.41) —
  lower edge widened 0.01 (immaterial: min measured β −0.3883) ; upper edge: measured peak-6
  β=−0.2626 is inside the computed edge (−0.2617, R1 β₈) by only 0.0009 — "all seven per-peak
  inside" is edge-sensitive at rounding level; quote the computed edges. Deeper: the DERIVED
  Phase-1 object is a FREE wall datum sweeping β over ≈[−0.4,+0.2]; the Dirichlet band is a
  ~25%-width representative sub-band. Amend "the offset rode a pre-banked derived band, not a
  tune" → "the fitted offset falls inside the band of the pre-declared canonical (Dirichlet)
  representative; the full derived wall-datum freedom spans ≈[−0.4,+0.2], so band membership is
  a consistency check on the canonical choice, not a parameter-free prediction." Also add "m=0"
  to the Phase-2 band sentence (the band is the m=0 table's; |m|>0 shifts β upward — banked).
- **A4: K5 is coverage, not prediction.** Since ρ₁ sweeps continuously through 2.4393 within R4
  (my q-sweep above), "R4 witness within 0.7%" must be restated: "the R4 region's admissible
  ratio range covers the measured first ratio; the chosen witness lands within 0.7% (witness
  choice = a spent continuous freedom; 1-of-5 regions)". Disclose the RA1→RA2 witness move and
  its (numerical) reason. The Phase-2 text's "2 params spent: scale + witness choice" partially
  concedes this — make it fully explicit.
- Look-elsewhere: 6 channels + 1-of-5 trials factor disclosed — adequate once A4 lands.

## 3. PARTIAL-landing honesty, both directions — SOUND with A5

- Over-claim: none found beyond A2/A3. The 25σ precision failure and the even/odd alternation
  are in the landed-outcome sentence itself with equal prominence — good. No "explains"-adjacent
  language anywhere (grep clean; F-TEMPLATE does not fire).
- **A5: the doublet tension is parked one notch too comfortably.** N6's fractional splittings at
  |m|=1 are HUGE (0.84/0.63/0.50); the measured table shows singlet peaks. "Untestable without
  source weights" is technically right, but the landing should carry the conditional forward:
  "the comb comparison is conditional on m=0-dominant weighting; |m|>0-dominant sourcing would
  predict large unobserved doublets." (This also mildly CONSTRAINS the future source sector — an
  under-claim in the package's favor.)
- Under-claim check: the band-hit is stated at honest strength (post-A3 it is correctly weaker).

## 4. Scope stamps — banner-level, minor repair

SS9/W1/equatorial/pencil banners head both Phase files and DERIVATION_NOTES §banner; the m=0 +
Dirichlet caveat travels on the low-k tables. **A6 (minor):** the two landed-outcome paragraphs
(PHASE2 §4, DERIVATION_NOTES §5) do not inline the stamps on the quotable sentence itself —
append "(SS9; W1 probe; equatorial inheritance; pencil analyticity; m=0 Dirichlet slice)" to
each. "No explains-the-CMB" verified package-wide.

## 5. Disclosed repairs — VERIFIED GENUINE

S1 decidable-form restatement (concrete rational functions, 3 rational points — disclosed, arc
precedent), N2 finer grid (1400, discretization-limit diagnosis in-comment), N4 Neumann zero-mode
predicate + interlacing — all in-script, all Category-A technique-level, and the full Phase-1
re-run reproduces 23/23 byte-exactly (verified here). Phase-2 7/7 arithmetic spot-checked.

## VERDICT: **AMENDED** (no falsifier fires; the comparison stands as RA2-PARTIAL)

Mandatory: A2 (the "1 fitted parameter" clause is false per code — the load-bearing accounting
repair), A3 (band-hit restated as canonical-representative consistency, computed edges quoted,
m=0 stamped), A4 (K5 → coverage statement + disclose the RA1→(3,−2)→RA2→(3,−3/2) witness move
and its reason). Secondary: A1 (ordering-evidence wording), A5 (doublet conditional), A6 (inline
stamps on the two landing sentences). With A2–A4 applied, RA2-PARTIAL is honest in both
directions and the F-RETRO discharge is real: no observational token predates the marker, the
ordering is machine-evidenced, and the genuinely blind content (the comb law, the Weyl spacing,
the band tables, the wedge/doublet structure) reproduces exactly.

— Adversarial review 2, 2026-08-09. Do not commit; consolidation owes A2–A4 before Charles.
