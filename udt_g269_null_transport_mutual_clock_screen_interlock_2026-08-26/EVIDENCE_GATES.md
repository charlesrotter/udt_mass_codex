# G269 evidence gates

Date: 2026-08-26

1. **Preregistered:** `PASS` — alternatives, domains, controls, mutations, falsifiers, and maximum
   conclusion were committed and pushed at `c79f29e6` before production or independent results.
2. **Bounded scope:** `PASS_WITH_CAVEATS` — all smooth regular affine null relations with supplied
   endpoint unit clocks; physical query population, singular/global strata, and history remain out.
3. **Independent verification:** `PASS_INTERNAL` — 34 exact symbolic checks, 143,715
   implementation-distinct exact-rational assertions over 12,000 cases, a 101-value fixed-ratio
   separator, and 10/10 shared-validator mutation catches.
4. **Premise audit:** `PASS_WITH_CAVEATS` — transport scalar is metric-derived conditionally;
   physical mutual-clock interpretation remains working, and no distance/history claim is made.

Repository-wide gates also pass: the 250-row current-premise registry and startup guards pass, and
the full test suite reports `172 passed, 1 xfailed`. The expected failure is unchanged and is not a
G269 failure.

Current grade: `INTERNALLY_VERIFIED_AWAITING_FRESH_EXTERNAL_REVIEW`.

Maximum conclusion: coefficient-free bilocal transport scalar, sharp screen-conditioned bound, and
planar sech equality on supplied regular null relations only.
