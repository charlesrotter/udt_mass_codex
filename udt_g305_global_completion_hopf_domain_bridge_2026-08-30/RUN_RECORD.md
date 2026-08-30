# G305 run record

Date: 2026-08-30
Branch: `grok`
Preregistration commit: `fc0ee889`
Repair preregistration commit: `f4d021aa`

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
- hostile controls after preregistered repair: 10/10 evidence mutations caught; deliberately
  corrupted baseline detected;
- package verifier: 27 required files and 11 source hashes pass in repository layout;
- fresh dependency-free sealed-layout replay: PASS for the independent, hostile, and package
  verifiers under `python3 -S`;
- full repository regression: `199 passed, 1 xfailed`; the xfail is the registered matter-lane
  habit-pin sentinel.

Fresh external review session `01a0546b-f395-75a1-b8bd-5cf94c6a6447` independently reproduced the
bounded geometry and topology and returned `REPAIRABLE_DEFECTS`. It found no scientific
contradiction. Its three evidence defects were preregistered before repair. Repair-only external
follow-up remains pending.

No GPU, network, observation, fitted parameter, field equation, action, source, matter model,
physical `X_max`, or protected package was used.
