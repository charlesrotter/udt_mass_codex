# G265 run record

Date: 2026-08-26
Branch: `grok`
Preregistration commit: `8f716271`

Commands:

```text
python3 derive_closure.py
python3 verify_independent.py
python3 run_catch_proofs.py
python3 verify_package.py
```

Results:

- exact symbolic checks: `18/18`;
- independent quadrature/RK4 assertions: `63/63`;
- mutation catches: `8/8`.

Fresh sealed GPT-5.4 review reproduced the bounded algebra and returned `ACCEPT_WITH_REPAIRS`.
The repair replay additionally requires exact live/recorded result equality and catches an in-memory
recorded-landing mutant. The sealed repair-only GPT-5.4 follow-up reproduced all gates and returned
`REPAIRS_ACCEPTED`.

No observational outcomes, protected packages, GPU solve, fit, imported field equation, source,
matter model, radiative transfer, or numerical `X_max` entered.
