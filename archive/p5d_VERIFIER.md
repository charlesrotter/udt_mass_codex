# P5d — Blind Adversarial Verifier Pass

**Verifier agent:** claude-opus-4-8[1m] (independent blind subagent, id a97b89e89d0e05544).
**Date:** 2026-06-20. **Target:** `p5d_timelive.py` + `p5d_timelive_results.md`.
**Mandate:** try to BREAK the headline claim (M=0 / no classical oscillator on the round
time-live channel); report the truth either way. DATA-BLIND. Anti-hang held (Nr<=16,
single sequential process, no background, every call <5 min).

## Result: CLAIM CORRECT — could not be broken.

| Test | Result | Verdict |
|---|---|---|
| 1. Re-assemble K,C,M (Nr=12,cell=14) | ||K||=4.48, ||C||=0.613, ||M||=2.24e-9 -> ||M||/||K||=5.0e-10 | PASS (machine floor, not 1e-3) |
| 2a. dtt_g (d_t^2 content) nonzero? | dtt_g(omega=1)=1.6e-1 NONZERO; dt_g=1.9e-1 | PASS (inertia IS computed/wired) |
| 2b. dtt_g reaches the kernel? | kernel(dttg on) - kernel(dttg=0) = 5.6e-2 NONZERO | PASS (reaches dGamma[T]/Riemann) |
| 2c. Net diagonal G^t_t shift? | dG^t_t ~2e-13 across omega{0.1,0.3,1.0}; G^t_r=0.24/0.71/2.38 (linear) | PASS (genuine Birkhoff CANCELLATION, not a dropped term) |
| 3. Hunt a nonzero M (eps,w1 scan) | worst ||M||=5.3e-8, max|M entry|=1.3e-9 (both << 1e-6 break threshold) | PASS (no oscillator found) |
| 4. Containment (omega->0==static) | ||time-rows(x=0,omega=0)||=3.16e-10 (~0); K cond=inf (zero modes) | PASS |
| 5. Released-amplitude BC mask | pins EXACTLY 4 nodes [a1(seal),b1(core),F1(core),F1(seal)]; 32 interior DOF freed | PASS (P4 pins released) |
| extra. R/resolution independence of M=0 | ||M||: 2.85e-9/2.24e-9/2.08e-9 (cell 10/14/18), 2.93e-9 (Nr=16); ||K||~1/R^2; global-min omega=0 every cell | PASS (not a single-grid artifact) |

**Verifier final verdict (verbatim essence):** "The diagonal d_t^2 inertia operator M is at
machine floor (||M||/||K|| ~ 5e-10), and this is a VERIFIED Birkhoff cancellation, not a
dropped/unwired term: dtt_g is nonzero, it provably reaches the kernel's curvature, and it
cancels in the diagonal G^t_t while the first-order G^t_r momentum channel survives linearly
in omega. The round time-live channel carries no classical oscillator / no discrete frequency /
no tower. R- and resolution-independent. No smuggled target found (no pi-ladder, no banked
M_MS/ratio, no desired-frequency search); the QEP was posed open and returned no frequency."

**Honest caveats the verifier flagged (scope, not errors — all already stated in the results doc):**
1. Round/diagonal channel only, by construction; the off-round l>=2 channel is P5e-deferred and
   untested. Verdict applies to the round ground state, as scoped.
2. K is rank-deficient (6 zero modes at Nr=12); the "no nonzero omega" conclusion rests on BOTH
   M=0 AND K's flat directions — both point the same way (no restoring oscillator).
3. The d_t^2 content is supplied analytically via harmonic balance (phase0 (C): kernel d_dx is
   spatial-only), so M=0 is the analytic-HB inertia cancelling in the diagonal = exactly the
   physical Birkhoff statement, correctly wired. Not a contamination.

(Minor numeric note: verifier saw dtt_g~0.16 and dG^t_t~2e-13 vs the doc's ~0.11 and ~1e-15 —
both reflect a larger live amplitude in the verifier's probe; both at floor; immaterial to the
verdict.)
