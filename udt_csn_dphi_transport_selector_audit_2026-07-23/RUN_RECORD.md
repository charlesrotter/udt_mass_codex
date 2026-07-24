# Run record

Date: 2026-07-23

Preregistered base: `bc802bb0ec3b612f841963cc471440fc88741bbf`

Preregistration commit: `42edf80`

Compute: CPU only; `CUDA_VISIBLE_DEVICES` empty for repository tests

Versions:

```text
Python 3.10.12
SymPy 1.13.1
```

Controller:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  udt_csn_dphi_transport_selector_audit_2026-07-23/derive_csn_dphi_transport.py \
  --output udt_csn_dphi_transport_selector_audit_2026-07-23/DERIVATION_RESULT.json
```

Independent verifier:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -s \
  udt_csn_dphi_transport_selector_audit_2026-07-23/verify_csn_dphi_transport_independent.py \
  --production-result udt_csn_dphi_transport_selector_audit_2026-07-23/DERIVATION_RESULT.json \
  --output udt_csn_dphi_transport_selector_audit_2026-07-23/INDEPENDENT_VERIFICATION_RESULT.json
```

Repository tests:

```bash
CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 \
  python3 -m pytest -q tests/
```

Repository/package gates:

```bash
CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 python3 -s \
  udt_csn_dphi_transport_selector_audit_2026-07-23/verify_repository_gates.py
```

The repository gate reruns both algebra implementations into a temporary
directory and requires byte-identical JSON outputs.

No GPU process, long solve, network computation, action construction,
carrier adoption, artifact move, or repository reorganization was
performed.
