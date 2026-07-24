# Run record

Date: 2026-07-23  
Device: CPU only; `CUDA_VISIBLE_DEVICES` blank for repository gates  
Preregistration commit: `59bc92f`

## Environment

```text
python3 --version
python3 -c "import sympy; print(sympy.__version__)"
```

Exact versions are also recorded in the machine-readable results.

Observed:

```text
Python 3.10.12
SymPy 1.13.1
```

## Production

```text
python3 \
  udt_reciprocal_transport_naturality_selector_audit_2026-07-23/derive_reciprocal_transport_naturality.py \
  --output \
  udt_reciprocal_transport_naturality_selector_audit_2026-07-23/DERIVATION_RESULT.json
```

Result: all 16 exact/source checks passed.

## Independent verification

```text
python3 \
  udt_reciprocal_transport_naturality_selector_audit_2026-07-23/verify_reciprocal_transport_naturality_independent.py \
  --production-result \
  udt_reciprocal_transport_naturality_selector_audit_2026-07-23/DERIVATION_RESULT.json \
  --output \
  udt_reciprocal_transport_naturality_selector_audit_2026-07-23/INDEPENDENT_VERIFICATION_RESULT.json
```

Result: 9/9 exact checks, 12/12 catches, and 5/5 agreement checks passed.

## Repository gates

```text
CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 python3 \
  udt_reciprocal_transport_naturality_selector_audit_2026-07-23/verify_repository_gates.py
```

The exact test counts, package replays, navigation checks, and
dirty-checkout metadata result are stored in `REPOSITORY_GATES.json`.
