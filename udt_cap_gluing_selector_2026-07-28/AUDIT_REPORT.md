# Cap gluing of the plane-selector certificate — AUDIT REPORT (gate c)

Date: 2026-07-28. Branch: `grok`. Preregistration committed `ed01bda` BEFORE the derivation
ran. CPU-only symbolic derivation; no solve, no GPU, no canonization.

**GRADE: VERIFIED-WITH-CAVEATS** — blind adversarial pass (zero-context-framed,
same-session-spawned agent, not a hosted external model) returned **BANKABLE-AS-SCOPED
conditional on one required change**, which is applied (EXACT_DERIVATION.md §1.3b: the
load-bearing `u0 in (0, infinity)` is now DERIVED from registered premises — smooth `g` +
non-vanishing `K` force `u0 < infinity`; the non-vanishing surviving cap cycle forces
`u0 > 0` — instead of assumed). Two cosmetic wordings also applied (limit-form of the
`b = g(w,w)/y^2` statement; X-boundedness scoping clause). The verifier independently rebuilt
the mechanism (26/26 + numeric probes), attacked and DISSOLVED both suspected errors (w/Y
conflation; cap-cycle sign), reran the script byte-identically (72/72), and instantiated
T-c3 on its own non-witness complete member.

## Result first

- **T-c3: c = 1 is FORCED, exactly.** Any exceptional-stratum member (`alpha = 0`,
  `bu + f^2 = c` constant) with a regular cap has `c = f_cap^2`, and the registered two-cap
  toric completion forces `f_cap = +-1` at both caps. **Complete two-cap exceptional-stratum
  members have c = 1 exactly** — the double-plane witness's `S = 1` was forced by cap
  regularity, not accidental. Corollary: on complete members `|det G_KY| = c_E^2 = |det G_KV|`
  (the area-VALUE cannot discriminate there). Bonus lock: `S = c` forces
  `f2 = -b2 u0 / (2 f_cap)` (witness: `f2 = -2`, matched).
- **T-c1 (with a preregistration correction recorded):** the prereg's "(i) V closes /
  (ii) Y closes" dichotomy is EMPTY — V cannot close (`A(V) = 1` cannot -> 0) and Y is a free
  line; the actual closers are the cap cycles `(V -+ Y)/2` (at the `f -> +1` cap the closer is
  `(V - Y)/2`, moment `(1-f)/2 -> 0` — verifier-matched to round-S3 Hopf coordinates). At a
  regular cap: `f -> f_cap = -x/y = +-1` (opposite signs at the two caps); `b` MUST vanish at
  unit rate `b = rho^2/y^2 (1 + O(rho^2))`; `u -> u0 in (0, infinity)` DERIVED (§1.3b);
  `chi -> 0` FORCED (regular caps are depth-critical); `df -> 0` FORCED at `O(sqrt(b))` with
  `df^2/b -> 4 f2^2 y^2`.
- **T-c2 limit atlas:** `det G_KY -> -c_E^2` (equal to `det G_KV`); off-term `-> 0` at
  `O(sqrt(b))`; `tr D_KY -> 0`; both restricted D-matrices `-> 0` entrywise. `df -> 0` at caps
  is FORCED by regularity, not witness-specific.
- **T-c4:** no certificate leg is singular or discontinuous at a regular cap; the rate pair
  lands on the already-covered `chi = 0` degeneracy class. The only divergent object is the
  full-response trace `tr D3 = db/b ~ 2/rho` — not a certificate quantity. The selector
  theorem's principal-orbit scope is RETAINED (atlas = boundary annotation) and its
  exceptional stratum TIGHTENED for complete members (`c = 1`); the stratum remainder is
  NARROWED, not closed.

Falsifiers: F-c1 NOT fired (conditions derived; the prereg framing presupposition corrected
on the record in §1.1/§5, not papered); F-c2 NOT fired (no certificate quantity diverges);
F-c3 NOT fired (independent recompute; witness with symbolic eps/alpha; two exact-rational
non-witness families; verifier's own third family).

## Evidence

`derive_cap_gluing.py`: 72/72 zero-residual checks, exit 0, deterministic; verifier rerun
byte-identical; verifier independent script 26/26 + float probes confirming every claimed
rate (det quadratic, off/tr/chi `O(rho)`, `df^2/b` limit to 6 digits); negative controls
discriminate (c = 6/5 non-closing, c = 4/5 inadmissible, odd-jet C^1 break) — rebuilt by the
verifier on its own profiles.

## Limits

1. Family CHOSE (P06/P07/P14-class); registered two-cap toric completion (unimodular cap
   basis) CHOSE; principal-orbit certificate limits only — NO cap-extended response is
   claimed (`D3` genuinely diverges at caps). 2. The evenness-in-rho fact is Category-A
   standard mathematics (tagged, soundness-checked by the odd-jet negative control), scoped
   to no-cone caps. 3. The `-> 0` limits are scoped to transverse directions extending
   boundedly across the cap (T-c3 itself involves no X). 4. Non-registered completions
   (e.g. a Y-closing family) would give `c = x^2/y^2 != 1` — recorded, out of the registered
   scope. 5. No physics, no alpha value, no branch, no canonization.

## Verifier record

Blind adversarial pass, 2026-07-28 (scratch /tmp/scratch_verify_c/, independent script
26/26, float probes, determinism reruns). Attack 1 (c=1 chain): CONFIRMED — b -> 0 mechanism
rebuilt with no w/Y conflation (g(H,H) = b exact; y^2 b = g(w,w) - Q(x+yf)^2); the ONE genuine
gap found — u0 assumed — was itself discharged by the verifier from registered premises and
is now derived in §1.3b (required change, applied). Attack 2 (dichotomy correction):
CONFIRMED, suspected sign error dissolves (closer at f -> +1 is (V-Y)/2). Attack 3 (chi -> 0):
CONFIRMED as scoped (X-boundedness clause added). Attack 4 (limits/rates): CONFIRMED
independently incl. numeric rates. Attack 5 (controls): CONFIRMED discriminating on the
verifier's own profiles. Attack 6 (prose): honest tagging; prereg-presupposition correction
recorded in three places; max conclusion respected. Overall: **BANKABLE-AS-SCOPED** after the
u0 discharge — applied above.
