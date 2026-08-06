# BLIND ADVERSARIAL VERIFICATION — c_eff <-> depth-profile binding test

Date: 2026-08-06 | Verifier: fresh zero-context agent (Fable 5), branch grok
Target: `DERIVATION_NOTES.md` (this directory) and its claims as relayed in
`udt_ceff_depth_orchestra_integration_2026-08-06.md`.
Method: ALL algebra recomputed independently in fresh sympy from the ground-truth
machinery only (`udt_complete_pair_phi_orchestra_audit_2026-08-05/EXACT_DERIVATION.md`:
`C_A = A^dagger A`, `A^dagger = g_p^-1 A^T g_q`, `delta_t = -(1/2) log lambda_timelike`).
NO code from `ceff_binding.py` was read or imported. Verification script:
scratchpad `blind_verify_ceff.py` (37 independent checks; all True; transcript below
summarized per claim). Redshift convention taken verbatim from
`simple_metric_L_native_optical_derive_results.md` (`A = e^{-2phi}`, observer at
`phi=0, r=0`, `1+z = 1/sqrt(A)`).

---

## CLAIM 1 — the three-way identity (PART 0). VERDICT: CONFIRMED, with one clarification.

Independently recomputed, all exact:
- `c_eff = sqrt(-g_tt/g_xx) = c_E e^{-2phi}` on `ds^2 = -e^{-2phi}c_E^2 dt^2 + e^{2phi}dx^2`. TRUE.
- `C_D = D_r^dagger D_r = diag(e^{-2phi}, e^{+2phi}, 1, 1)` on eta, `D_r = diag(r^-1,r,1,1)`,
  `r = e^phi`. TRUE. The `e^{-2phi}` eigenline is the eta=-1 (timelike) slot; causal label
  verified, not assumed.
- `lambda_timelike = e^{-2phi}`, `delta_t = phi`. TRUE.
- `c_eff = c_E * lambda_timelike` and `phi = -(1/2) log(c_eff/c_E)`. TRUE.

**The point-vs-two-point question (posed by the review charter).** The PART 0
`lambda_t = e^{-2phi}` is a strain eigenvalue computed with `g_p = eta` — i.e. the
comparison arrow FROM a `phi = 0` reference frame. I verified by direct substitution
that it is EXACTLY the `phi_p = 0` special case of the two-point eigenvalue
`lambda_t(p->q) = e^{-2(phi_q - phi_p)}` (machine check `1c_point_is_p0_special_case`:
True). So the PART 0 identity `c_eff(q) = c_E * lambda_t` is chart-anchored: it holds
with the implicit reference `p` at `phi = 0` (which the reciprocal-lock chart supplies —
`c_E` is by definition the cone value at `phi = 0`).

Is it stated honestly? **Yes, adequately.** DERIVATION_NOTES does not hide the structure:
PART 0 explicitly flags c_eff as a GAUGE quantity "within the reciprocal-lock chart
(F-GAUGE noted)", and PART 1 immediately supplies the honest two-point form
`c_eff(q)/c_eff(p) = lambda_t(p->q)` with "p fixed reference" named. The single
improvement owed (clarification, NOT a correction of any equation): PART 0 should say in
one line that its `lambda_t` is the `p = (phi=0)` arrow's eigenvalue, i.e. the point
identity is the reference-anchored special case of the PART 1 ratio identity. No stated
equation is wrong.

## CLAIM 2 — VERDICT B / separability of `a` (PART 2). VERDICT: CONFIRMED.

Independently recomputed with full 4-slot metrics
`g = diag(-e^{-2phi}c_E^2, e^{2phi}, R^2, R^2)`, arrow A = I:
- `C4 = diag(e^{-2Dphi}, e^{+2Dphi}, (R_q/R_p)^2, (R_q/R_p)^2)`. TRUE.
- `lambda_timelike(4-slot) = e^{-2(phi_q-phi_p)}`; free symbols contain NO `R_p, R_q`,
  and NO `a`. TRUE. Timelike eigenvalue is identical with screen on vs off. TRUE.
- `R` sits only in the spacelike screen eigenvalues. TRUE.
- `delta_a = (phi_q-phi_p) + a log(R_q/R_p)`; `d(delta_a)/da = log(R_q/R_p)` (pure
  screen, no phi); `delta_a|_{a=0} = delta_t`. TRUE. Killing-norm leg
  `log[N(p)/N(q)] = phi_q - phi_p` matches the timelike eigenvalue leg exactly. TRUE.

The load-bearing step as stated (timelike eigenvalue lives in the clock/Killing block;
`R` in orthogonal spacelike slots; hence `a log R` cannot enter the timelike eigenspace)
is sound FOR THE DIAGONAL split-preserving family considered — and the notes themselves
scope it so (PART 3 names the off-diagonal exception). Separability of the screen-AREA
coefficient `a`: CONFIRMED. VERDICT B as scoped: CONFIRMED.

## CLAIM 3 — ratio-invariant vs absolute-gauge, and the redshift relation.
## VERDICT: CONFIRMED (invariance) + CORRECTED (integration doc's redshift wording).

Invariance, independently verified:
- `c_eff(q)/c_eff(p) = lambda_t(p->q) = e^{-2(phi_q-phi_p)}`. TRUE (exact).
- `delta_t(p->q) = phi_q - phi_p`. TRUE.
- Spectrum of the two-point strain is invariant under independent endpoint frame changes
  `g -> L^-T g L^-1`, `A -> L_q A L_p^-1` (charpoly identical, symbolic). TRUE.
- Absolute c_eff changes under radial reparametrization (`g_xx -> b^2 g_xx` gives
  `c_eff -> c_eff/b`). TRUE — absolute c_eff is chart-dependent, as claimed.

**The exact redshift relation** (against `simple_metric_L_native_optical_derive_results.md`,
`1+z = 1/sqrt(A)`, `A = e^{-2phi}`, observer at phi=0; two-point form
`1+z = sqrt(A(obs)/A(emit)) = e^{phi_emit - phi_obs}` — conventions verified consistent):

```
c_eff(emit)/c_eff(obs) = lambda_t(obs->emit) = e^{-2(phi_e - phi_o)} = (1+z)^{-2}
```

**It is (1+z)^{-2}, NOT (1+z)^{-1}** (both machine-checked: R2 True, R3 "not equal"
True). Equivalently `c_eff = c_E * A` exactly, so the ratio equals `A_emit/A_obs`.

- DERIVATION_NOTES.md itself makes NO redshift claim (grep: zero hits) — nothing to
  correct there.
- The integration doc `udt_ceff_depth_orchestra_integration_2026-08-06.md` needs TWO
  precision corrections (neither is a kill; the underlying algebra is right):
  1. Line 28 & 41: "`c_eff(q)/c_eff(p) = lambda_t = phi_q - phi_p`" conflates the
     eigenvalue with its log-extractor. Correct: the ratio `= lambda_t = e^{-2(phi_q-phi_p)}`;
     the DEPTH `delta_t = -(1/2) log lambda_t = phi_q - phi_p`. A number is not its
     logarithm; the doc's own three-readings paragraph states this correctly, so this is
     shorthand drift, but in a load-bearing doc it must be fixed.
  2. "it is exactly redshift-with-distance": the monotone content is right, but the exact
     relation carries a square: ratio `= (1+z)^{-2}`. Any downstream use that equates the
     c_eff-ratio numerically to `1+z` (e.g. against the SNe curve) would be off by a
     power of 2 in the exponent. State the `(1+z)^{-2}` explicitly.

## CLAIM 4 — the mixing witness (PART 3 / sec.4). VERDICT: CONFIRMED.

Independently recomputed from the registered arrow
`A = [[1/2,0,0,0],[0,2,0,0],[1/4,0,1,0],[0,0,0,1]]` on eta:
- `C_A = A^dagger A`; clock-screen block `[[3/16,-1/4],[1/4,1]]`; charpoly
  `L^2 - (19/16)L + 1/4`. TRUE (exact match).
- Eigenvalues `(19 -+ sqrt(105))/32`; the `lambda_-` eigenline verified TIMELIKE
  (eigenvector norm `-1 + s^2 < 0`) and the `lambda_+` eigenline verified SPACELIKE —
  causal labels checked, not assumed. TRUE.
- `delta_t_mix = -(1/2) log[(19-sqrt(105))/32] = 0.648166889623 != log 2 = 0.693147180560`.
  TRUE (exact inequality, symbolic).
- Channel disjointness: the block-triangular character `delta_a(A) = delta_quotient +
  a log det Q_A` is verified blind to the 1/4 mixing entry (`det Q = 1`, quotient block
  identical with/without mixing => `delta_a = log 2` for ALL `a`, both arrows), while the
  STRAIN timelike eigenvalue differs (`(19-sqrt(105))/32 != 1/4`). So mixing changes
  `lambda_t` but not the `a`-family — exactly the disjointness the notes claim, and it
  matches EXACT_DERIVATION.md sec.7's statement verbatim. TRUE.

One scope note, already handled correctly by the notes: the mixing witness is a
frame-strain statement (g_p = g_q = eta, single registered arrow); the notes claim only
existence ("DOES modulate"), which is exactly what a witness supports. No overreach found.

---

## FALSE-PASS HUNT (what I tried to break and could not)

- Wrong causal labeling: checked eigenline signatures explicitly in claims 1, 4 (both
  eigenlines in the mixing block) rather than trusting slot position. Labels correct.
- Reference smuggling in PART 0: found the implicit phi_p = 0 anchor; verified it is the
  exact special case of the two-point object and is surfaced by PART 1 + the F-GAUGE
  flags. Clarification owed, no error.
- Redshift convention mismatch: `1+z = 1/sqrt(A)` (observer at phi=0) and
  `1+z = sqrt(A_obs/A_emit)` verified to be the SAME convention; no factor clash between
  the record and the strain machinery. The square lives in c_eff (ratio = (1+z)^{-2}).
- Invariance overclaim: verified charpoly invariance symbolically under independent
  endpoint frame changes AND verified absolute c_eff is NOT invariant under radial
  reparametrization — the gauge/invariant split is stated correctly.
- Screen-slot leakage: symbol-level check that neither `R` nor `a` appears in the
  timelike eigenvalue. Clean.

## OVERALL VERDICT: **PASS-WITH-CORRECTIONS**

The target's algebra is exact and fully reproduced from scratch; every equation in
DERIVATION_NOTES.md checks out, and its scoping (gauge flags, mixing-channel exception)
is honest. Required before this work is leaned on:
1. (DERIVATION_NOTES PART 0, clarification) add one line: the point identity
   `c_eff = c_E lambda_t` is the `p=(phi=0)`-reference special case of the PART 1 ratio
   identity.
2. (Integration doc, correction) fix `lambda_t = phi_q - phi_p` to
   `lambda_t = e^{-2(phi_q-phi_p)}` / `delta_t = phi_q - phi_p`.
3. (Integration doc, correction) state the exact redshift relation:
   `c_eff(q)/c_eff(p) = (1+z)^{-2}` — "ratio IS redshift" is qualitatively right but
   quantitatively carries the square.

With corrections 2-3 applied to the integration doc, the reconciliation audit may lean
on this work.
