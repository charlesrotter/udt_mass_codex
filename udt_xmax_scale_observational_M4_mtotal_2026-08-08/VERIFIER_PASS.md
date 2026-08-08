# VERIFIER_PASS — M4 blind adversarial pass (2026-08-08, fresh-context verifier)

Scope: PREREGISTRATION.md (2f709b05), compute_m4.py, m4_results.json, M4_RESULTS.md.
Ground cite-checked: M3 SNE_RESULTS.md CONSOLIDATED; O2 DERIVATION_NOTES sec. 4(a)/(b);
M2 D1_FORMULAS.md (X_eff = R_w/n, KEY table; proper 2R_w/(2−n) n<2; optical R_w/(1−n) n<1,
DIVERGENT n≥1 with n=1 log-divergent).

## 1. Independent recomputation (own arithmetic first, then diffed)

Inputs verified against M3 CONSOLIDATED verbatim: X_eff 2086.0 [2059.1, 2113.2] Mpc;
inv_n 0.947 [0.9284, 0.9658]; 2.82σ/3.89σ exclusion figures match.
- n: 1/0.9470 = 1.05597→1.056; 1/0.9658 = 1.03541→1.0354; 1/0.9284 = 1.07712→1.0771. MATCH.
- R_w = n·X_eff: 2202.7 / 2132.0 / 2276.2 Mpc. MATCH (D1 relation confirmed against M2).
- proper 2R_w/(2−n): 4666.7 / 4420.6 / 4932.8 Mpc. MATCH.
- M = x·Mpc·c²/G (c²/G·Mpc = 4.15511e49 kg/Mpc): all six (kg, M_sun) entries reproduce to the
  displayed precision (e.g. best areal 9.153e52 kg / 4.602e22 M_sun; hi-corner proper
  2.050e53 kg / 1.031e23 M_sun). MATCH. Constants: c exact, G CODATA-2018, Mpc IAU — correct.
- H0-equivalent: 299792.458/(2·2086.0) = 71.86 km/s/Mpc. MATCH.
- zHD claim spot-check: n=1.0785 at X_eff=2086 → areal 2249.8, proper 4882.9 Mpc — both inside
  the envelope; "moves numbers by less than the envelope width" VERIFIED (note: rides zCMB's
  X_eff, zHD has no own mode-B X_eff; acceptable as stated).
- Corner pairing bounds: both M rows are monotone INCREASING in n and in X_eff (areal n·X;
  proper 2nX/(2−n), ∂n>0 for n<2), so (X_lo, n_lo)/(X_hi, n_hi) are the true rectangle
  extremes; and the marginal-interval box CIRCUMSCRIBES the joint ellipse for ANY correlation
  sign, so "corner combinations OVERSTATE" is correct in DIRECTION and the envelope is a
  genuine bound. VERIFIED.

## 2. D2(b) attack (directed): content or tautology?

The doc's "close to tautological" label is honest but the RESIDUAL-content sentence overstates.
Finding: ΛCDM's Hubble-sphere bookkeeping mass is c³/(2GH0) = (c/2H0)·c²/G exactly — i.e. the
D3 external number IS x·c²/G evaluated at x ~ c/H0 (times O(1–10) volume/density conventions).
Since the fit reproduces H0 ≈ 72 by construction of the low-z limit (D2(a), same SH0ES anchor
on both sides), the "same order as external bookkeeping" match is arithmetically GUARANTEED
and is NOT independent corroboration. The only empirical content is that the SNe select a wall
scale of order c/H0 — which is exactly D2(a), already labeled "not a result." Also "rather
than somewhere absurd" implies an internal sanity criterion that does not exist (there is no
independent M_total against which a value could be absurd).
AMENDMENT DEMANDED (exact wording, replacing M4_RESULTS.md lines 30–33 from "What is NOT
tautological" through "at exactly that strength."):
  "The residual non-tautological content is ONLY this: the SNe select a wall scale of order
  c/H0 (D2(a)). The same-order match with D3's external bookkeeping is itself arithmetically
  guaranteed given that (the external number is ≈ (c/2H0)·c²/G by ΛCDM's own construction,
  and both sides ride the same ladder anchor) — so M4 contains NO independent numerical
  corroboration of criticality. The consonance is recorded as direction-not-evidence, fully."
No sentence smuggles "the universe is critical" as a finding; the kernel meeting-point section
is properly IF/THEN-conditional.

## 3. Premise carriage + language scan

- Order-of-magnitude label, anchor ± chain, P1-conditional, measure tags: present on the json
  labels block, the results header, and the table. PASS.
- Optical row: equal ink (full table row + D2-adjacent prereg clause). PASS. Note
  (strengthening, no change owed): ground rule is divergent iff n≥1 (n=1 log), so the row's
  divergence does NOT even depend on the 2.82σ-only n=1 exclusion; "at fitted n>1" is
  conservative and true across the whole envelope.
- F-LEAN-BAO: grep — BAO appears only in the D2(c) sentence + the prereg contract text. PASS.
- F-SCOPE: no "the mass of the universe", no precision claims, no verdict words in results
  ("Charles-confirmed" refers to the lead's provenance, not a result). PASS.
- Trivia (no action): M_sun 1.98892e30 vs IAU nominal 1.98841e30 (0.03%, irrelevant at OOM);
  M3's "R_w at best n: 2202.6" vs M4's 2202.7 = rounding of inv_n before inversion (0.1 Mpc).

## VERDICT: SUSTAINED-AMENDED
Amendment list: (1) the D2(b) rewording above (the "not tautological" residual is itself
guaranteed arithmetic; delete "rather than somewhere absurd"). Nothing else owed. All numbers
reproduce; the table, envelope logic, H0-equivalent, and all falsifier gates hold.
