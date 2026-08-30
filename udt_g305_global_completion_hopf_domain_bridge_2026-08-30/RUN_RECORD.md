# G305 run record

Date: 2026-08-30
Branch: `grok`
Preregistration commit: `fc0ee889`
Repair preregistration commit: `f4d021aa`
R3 completion preregistration commit: `ca462391`

Commands:

```bash
python3 derive_global_hopf_bridge.py
python3 verify_global_hopf_bridge_independent.py
python3 run_global_hopf_catches.py
```

Results:

- production: 77 exact assertions;
- independent after preregistered repair: 687 checks, 24 finite-difference metric cases, maximum
  metric error `3.5904363926420046e-09`, maximum chart-overlap error
  `8.881784197001252e-16`, normalized Hopf number `-1.0000000010280863`;
- hostile controls after second preregistered repair: ten cases make 11 direct evidence/premise
  field mutations, all named failures caught; deliberately corrupted baseline detected;
- package verifier: 30 required files and 11 source hashes pass in repository layout;
- fresh dependency-free sealed-layout replay: PASS for the independent, hostile, and package
  verifiers under `python3 -S`;
- full repository regression: `199 passed, 1 xfailed`; the xfail is the registered matter-lane
  habit-pin sentinel.

Fresh external review session `01a0546b-f395-75a1-b8bd-5cf94c6a6447` independently reproduced the
bounded geometry and topology and returned `REPAIRABLE_DEFECTS`. It found no scientific
contradiction. Its three evidence defects were preregistered before repair and sent through the
first repair-only external follow-up recorded below.

Repair-follow-up session `01a05487-f4d0-78b1-b98a-4738680e9342` accepted R1, R2, and the unchanged
landing but returned `REPAIRABLE_DEFECTS_REMAIN` because R3 added labels rather than mutating actual
evidence fields. The direct-field completion was preregistered before implementation; final R3-only
external follow-up remains pending.

No GPU, network, observation, fitted parameter, field equation, action, source, matter model,
physical `X_max`, or protected package was used.
