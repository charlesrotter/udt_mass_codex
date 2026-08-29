# G292 fresh external `gpt-5.4` adversarial review

Date: 2026-08-28
Verdict: `ACCEPT_WITH_REPAIRS`

## Scientific defects

None found within the bounded claim. The intake supports the connection-level descent to a
degree-two differential character, identifies the integral class with the screen Euler class on
the orientable fixed-rank stratum, correctly limits persistence to kinematic sector persistence,
and does not justify any dynamics, conservation law, or history selection.

## Evidence, packaging, or wording repairs

1. `verify_package.py` skips the symbolic production replay when `sympy` is unavailable but still
   emits `status: PASS`. That is an evidence-gating defect against the preregistered requirement that
   production, independent replay, and hostile catches all agree.
2. `RUN_RECORD.md` records direct replay commands that are not sealed-mount-safe: `py_compile`
   writes `__pycache__`, and the production script requires `sympy` without declaring it. The replay
   instructions should use a writable copy or `PYTHONPYCACHEPREFIX` and declare the dependency.
3. `EXACT_DERIVATION.md` overcompresses scope by saying the theorem covers the full smooth
   orientable `SO(2)` connection stratum immediately after defining a projected metric connection.
   The abstract mathematics covers the metric-connection stratum once the bundle/connection are
   supplied, but only one explicit global metric realization family is exhibited.
4. `EVIDENCE_GATES.md` and `EXACT_DERIVATION.md` retain pending/open status language that becomes
   stale after this external review.

## Independent basis

- The reviewer recomputed `a_j=a_i-d theta_ij`, global `F=da`, integral Euler periods, and the
  differential-character boundary law.
- It confirmed the affine connection theorem after a supplied orientation-preserving isometric
  identification: `D^b=D+bJ`, `F^b=F+db`, and the closed-loop holonomy ratio.
- It confirmed that comparing the G225 sky connection on `TS^2` with a G290 pair screen requires a
  supplied direction map and bundle identification.
- It directly checked the global witness: fixed `diag(-1,1)` pair block and `Phi=0`, the connection
  and curvature formulas, pole regularity, total and cap flux, and smooth complete globally
  hyperbolic product geometry.
- From a writable ephemeral copy it reproduced all 3,600 point cases, 105 cap quadratures, 25,446
  assertions, and 8/8 hostile catches.
- It found the coordinate-pole repair honest and nonsemantic.
- It confirmed the nonorientable, rank-loss/caustic, topology-change, singular, population, and
  history-selection strata remain open.

The exact bounded scientific landing was retained unchanged.
