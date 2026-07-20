# Commands and environment

All calculations were CPU-only from repository root on branch
`codex/c2-reciprocal-transverse-twist-jacobi-2026-07-20`.

Successful load-bearing commands:

```text
python3 c2_reciprocal_transverse_twist_jacobi_2026-07-20/derive_twist_jacobi.py
python3 c2_reciprocal_transverse_twist_jacobi_2026-07-20/verify_twist_jacobi.py
python3 c2_reciprocal_transverse_twist_jacobi_2026-07-20/verify_package.py
```

Environment:

```text
Python 3.10.12
SymPy 1.13.1
Torch 2.5.1+cu121
dtype float64
device CPU
Linux 6.8.0-124-generic x86_64
```

`requirements.txt` pins the public SymPy and Torch versions used. The Torch installation includes a
CUDA build tag, but the verifier creates only CPU tensors and reports `cpu_only=true`; no GPU process
was launched.

The failed pre-bank verifier invocations and their corrections are preserved in
`INDEPENDENT_VERIFIER_CORRECTION.md` and `BACH_PROJECTION_CORRECTION.md`. Neither failed invocation
supplies a scientific result. The successful return is `VERIFICATION_RESULT.json` and its complete
point table is `VERIFICATION_POINTS.tsv`.
