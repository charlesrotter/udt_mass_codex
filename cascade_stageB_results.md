# Cascade Stage B: the N-ladder is a COMPLETE consecutive-integer spectrum, twin-sided with parity inversion

**Date:** 2026-07-02. **Pre-registration:** `cascade_characterization_miniMAP.md` Stage B addendum
(Charles's per-rung table + the FROZEN accumulation-fit forms, committed `3c92a1b` BEFORE the
sweep). **Survey:** agent `af83644a55ba2f652` (761 shots; scripts `cascade_stageB_*.py`, data
`cascade_stageB_rungs.json`, `cascade_stageB_sweep.json`). **Blind adversarial verifier:** agent
`a826e7c47368930ab` (178 shots; own DOP853 chunked shooter + Illinois root finder + own
graduated-floor counter; NO survey files read; scripts `cascade_bv6_*.py`).
**Scope:** round-static Branch-P reduction; family A1 m=3 Z=8 (CHOSE); ρ_c=1 gauge. One family —
cross-family ratio universality is Stage C.

**VERIFICATION NOTE (driver error, caught by the blind protocol):** the bv6 prompt mis-stated
the C1 window census as "exactly N=1–6" — a DRIVER transcription error (the survey's own table
has N=7 at d=4.1552e-3, inside the window). The blind verifier, with no access to the survey
numbers, found the true contents (N=1–7) and flagged the discrepancy loudly — refuting the
PROMPT, matching the SURVEY rung-for-rung. Recorded as a working demonstration of why the
verifier is blinded against the driver, not only against the survey.

## Banked results (survey + blind verification agreeing; 15 rungs independently reproduced to 9–10 digits)

**B1 — COMPLETE INTEGER CENSUS: N = 0,1,2,…,22 all PRESENT, none missing, none duplicated**
(23 confirmed rungs, below-stuck side). Verifier's finer-grid (Δd/d=0.99%) sweep of
d∈[4.0e-3, 7.0e-3]: exactly the consecutive integers there, no extras, no aliased pairs (dip
detector: no near-zero arcs without sign change; min inter-root |miss| ≈ 0.24). Twin equality
N_δ = N_ρ' on every rung, both agents, all floors (N_δ never wobbled at ANY floor; N_ρ'
undercounts only at loose floors, the banked false-inequality direction).

**B2 — Per-rung table** (the pre-registered unlabeled ratio table; full precision in
`cascade_stageB_rungs.json`): q falls 12.62 → 0.380 from N=0→22 (monotone after one N=1→2
parity wobble); L_proper grows 3.56 → 42.02; identity checks across all rungs:
|Δφ − ln(1101)| ≤ 8.6e-14, |2m/ρ(seal) − 1| ≤ 3.1e-10, H_drift ≤ 2.6e-9.

**B3 — PARITY (verifier-sharpened statement):** ρ_s alternates about the cylinder value with
N-parity — below side: odd N → ρ_s<1, even N → ρ_s>1; χ alternates in step; zero exceptions in
every rung touched (13 verified blind). **Correct amplitude statement:** |ρ_s−1| shrinks
STRICTLY WITHIN EACH PARITY CLASS (odd: .357>.245>.161>.118>.065>.041; even: .210>.150>.114>.042)
but is NOT monotone rung-to-rung (N3>N2 etc.). [Survey's "shrinking with N" wording corrected.]

**B4 — THE TWIN LADDER:** the above-stuck side carries ITS OWN copy of the SAME integers —
verifier found consecutive N=8,9,10,11 (survey: N=2,9,10) — with q and L nearly coincident at
equal N (sub-1% at N=9,10) and **ρ_s parity INVERTED** (above side: odd → ρ_s>1, even → ρ_s<1;
exact mirror; confirmed on all four verifier rungs). No above-side root in d'∈(8e-3, 1.4e-2]
(monotone same-sign miss, no dips; even-pair caveat noted). No above-side N=0/N=1 found
(grid-limited).

**B5 — ACCUMULATION LAW: "UNCLASSIFIED" (the frozen-fit guard fired honestly).** None of the
five pre-committed forms (d(N): power/exponential/log; L(N): linear/power) has noise-like
residuals — all show structured (arch/U-shaped) patterns. Raw sequences banked for the record:
d(N+1)/d(N) rises 0.52 → 0.966 (not geometric, not fixed-power over the range);
L(N+1)−L(N) rises 1.53 → ~1.80 with parity alternation. NO post-hoc form was fit. Any future
q(N) or refined-d(N) law requires its own PRE-COMMITTED form set before analysis (same guard).

## Hazard instances (reusable method yield)
- Bracket-ambiguity observed live: a loose N=20 bracket contained N=21 as well (both resolved).
- N_ρ' loose-floor undercount reproduced at N≥13 and on the above side (−1 at floor 1e-4);
  graduated-floor discipline remains mandatory.
- Verifier found + fixed a chunked-shooter bug in ITS OWN harness pre-data (failed chunk
  containing the seal) — same class as the Stage A survey bug; both banked as a solver-harness
  pattern: ALWAYS scan a failed chunk's partial dense output for the seal.

## Gaps (carried)
72 unbisected below-side tail brackets (d ≤ 2.11e-3); the aliased window d∈(1.45e-3, 2.11e-3)
(≈11 rungs extrapolated, unrefined); sweep floor d=2e-4; above-side coverage coarse (8/11
brackets unbisected); ladder beyond N=22 unconfirmed; single family, single Z on this walk.

## NEXT (for the PONDER with Charles — now unlocked)
1. **INTERPRETATION** (gated on Charles): a complete consecutive-integer, twin-sided,
   parity-alternating spectrum of closed universe cells, indexed by a count that is
   simultaneously field-oscillations and interior marginal spheres. The eigenmode-corpus
   CONDITIONS-CHANGED question is now ripe (per the mini-MAP: with Charles only).
2. **Stage C:** cross-family/cross-Z ratio tables in N (now well-defined); q(N) forms to be
   frozen BEFORE analysis; the aliased window + tail as a targeted follow-up.
3. OWED standing: Z=8/Route-B mixing term; canon Δφ wording; claude.ai relay.
