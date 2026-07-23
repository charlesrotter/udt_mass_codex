# Commands

Build checkpoint evidence:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 build_checkpoint_evidence.py
```

Independent checkpoint verifier:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -s verify_checkpoint_independent.py
```

Deterministic zero-state startup rehearsal:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -s rehearse_startup_zero_state.py
```

Full repository test:

```bash
CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q tests/
```

Full repository and checkpoint gates:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -s verify_repository_gates.py
```

Determinism check after committing the correction:

```bash
sha256sum REPOSITORY_GATES.json
PYTHONDONTWRITEBYTECODE=1 python3 -s verify_repository_gates.py
sha256sum REPOSITORY_GATES.json
git status --short --branch
```

An external ephemeral-model rehearsal was not performed because no
task-specific external repository-disclosure grant was available.
