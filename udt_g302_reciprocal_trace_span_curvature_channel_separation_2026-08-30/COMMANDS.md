# G302 registered commands

Run from the repository root:

```bash
python3 udt_g302_reciprocal_trace_span_curvature_channel_separation_2026-08-30/derive_trace_span_and_geometry.py
python3 udt_g302_reciprocal_trace_span_curvature_channel_separation_2026-08-30/verify_independent.py
python3 udt_g302_reciprocal_trace_span_curvature_channel_separation_2026-08-30/run_catch_proofs.py
python3 -S udt_g302_reciprocal_trace_span_curvature_channel_separation_2026-08-30/verify_domain_census_independent.py
python3 -S udt_g302_reciprocal_trace_span_curvature_channel_separation_2026-08-30/run_domain_catch_proofs.py
python3 udt_g302_reciprocal_trace_span_curvature_channel_separation_2026-08-30/verify_package.py
python3 verify_current_scientific_premises.py
python3 -m pytest tests/
```

The first attempted production invocation used `python3 -S`; it failed before derivation because
`-S` hides the installed SymPy site package.  Ordinary `python3` is therefore the registered
dependency-bearing production route.  The independent rank calculation itself uses only standard
library exact fractions.
