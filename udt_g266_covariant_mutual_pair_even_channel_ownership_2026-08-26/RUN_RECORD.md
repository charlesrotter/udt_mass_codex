# G266 run record

Date: 2026-08-26

Commands:

```bash
python3 udt_g266_covariant_mutual_pair_even_channel_ownership_2026-08-26/derive_even_channel.py
python3 udt_g266_covariant_mutual_pair_even_channel_ownership_2026-08-26/derive_even_channel_stdlib.py
python3 udt_g266_covariant_mutual_pair_even_channel_ownership_2026-08-26/verify_independent.py
python3 udt_g266_covariant_mutual_pair_even_channel_ownership_2026-08-26/run_catch_proofs.py
python3 udt_g266_covariant_mutual_pair_even_channel_ownership_2026-08-26/verify_package.py
```

Results: 25 exact symbolic checks, 768 implementation-distinct exact-rational assertions, and 8
mutation catches. No observations, fit, ODE/PDE solve, GPU, protected input, or persistent runtime
output was used.

After the fresh external review, the repair-only replay also requires exact equality of the SymPy
reference, dependency-free standard-library result, and recorded JSON when SymPy is available; in
a dependency-free sealed environment the standard-library result is the exact package authority.
Source hashes are resolved fail-closed in either the live repository layout or the sealed
`private_sources/` layout, with an explicit wrong-hash rejection check.
