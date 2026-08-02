# Pinned clean-environment replay

Date: 2026-08-01  
Mode: CPU only; temporary isolated target directory; no repository dependency mutation

The host environment carried `sympy==1.13.1` because installed Torch pins that version. The exact
audit dependency was therefore installed into `/tmp/udt_reciprocal_closure_sympy114_target` with:

```text
python3 -m pip install --disable-pip-version-check --no-input \
  --target /tmp/udt_reciprocal_closure_sympy114_target \
  -r udt_reciprocal_closure_joint_selector_audit_2026-08-01/requirements.txt
```

Resolved versions:

```text
Python 3.10.12
sympy==1.14.0
mpmath==1.3.0
```

Replay commands used `PYTHONPATH=/tmp/udt_reciprocal_closure_sympy114_target` and ran from repository
root. All returned exit code zero. Raw stdout SHA-256 values were:

```text
derive_reciprocal_closure.py  16567c92b4508c4590dad4347d04a40f57f12460ec5813ef1a310104fb04b511
independent_verify.py         1b5db246fbca6e7e704f241e3acd936774425f860751a12d1ae3086363d598d8
verify_result.py              c8861a21927542fb3733e2fdf849c35df63803f8788c88a9cdd3ddae9d7187d9
```

The primary replay reproduced `RESULT.json` with 24/24 exact checks. The package verifier returned
26/26 after the accepted external-review repair.
