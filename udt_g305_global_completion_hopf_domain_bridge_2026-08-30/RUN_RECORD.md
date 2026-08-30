# G305 run record

Date: 2026-08-30
Branch: `grok`
Preregistration commit: `fc0ee889`

Commands:

```bash
python3 derive_global_hopf_bridge.py
python3 verify_global_hopf_bridge_independent.py
python3 run_global_hopf_catches.py
```

Results:

- production: 77 exact assertions;
- independent: 459 assertions, 18 finite-difference metric cases, maximum error
  `3.5904363926420046e-09`, normalized Hopf number `-1.0000000010280863`;
- hostile controls: 10/10 caught.
- full repository regression: `199 passed, 1 xfailed`; the xfail is the registered matter-lane
  habit-pin sentinel.

No GPU, network, observation, fitted parameter, field equation, action, source, matter model,
physical `X_max`, or protected package was used.
