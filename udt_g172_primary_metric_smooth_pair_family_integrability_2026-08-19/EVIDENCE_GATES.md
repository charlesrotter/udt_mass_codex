# G172 evidence gates

## Gate 1 — preregistration

PASS. `PREREGISTRATION.md`, `PONDER_MAP.md`, and the 11-source frozen manifest were committed at
`23c1462e` before outcome code or result artifacts were created.

## Gate 2 — bounded full-space coverage

PASS WITH BOUNDED SCOPE. The proof retains arbitrary smooth nonnegative
\(a^2(r)=\gamma_{S^2}(\gamma',\gamma')\) on any connected interval inside the supplied regular
primary-metric domain. It does not sample or select angular profiles. Turning, pure-angular,
time-live, nonspherical, singular, and global-completion strata are explicitly excluded.

## Gate 3 — independent verification

PASS. The production SymPy derivation passes 26/26 checks. A separate standard-library
Fraction/dual-number implementation imports no production code or SymPy and passes 144,000 checks
over 12,000 registered samples. A fresh sealed gpt-5.4 review reproduced the load-bearing algebra,
reran the dependency-light verifier, and returned `G172_ACCEPTED_WITH_STATED_BOUNDS`.

## Gate 4 — premise audit

PASS. `python3 verify_current_scientific_premises.py` passed the complete 158-row registry and
current startup guards. The post-review regression suite returned 128 passed and one known unrelated
XFAIL. The package records `phi` as supplied, the angular curve as free-and-characterized, and the
family type as chosen and bounded. It excludes co-presence, `X_max`, observations, dynamics,
actions, sources, and G142--G160.

## Current grade

`VERIFIED_WITH_CAVEATS__G172_ACCEPTED_WITH_STATED_BOUNDS`
