# Clean CPU-only verification record

Date: 2026-07-18
Repository: `/home/udt-admin/udt_mass_codex`
Accepted starting commit: `ded310a`
Result: `PASS`

## Environment construction

The workstation's first standard `python3 -m venv` attempt stopped before a
verifier run because Debian's `ensurepip` support was not installed. A proposed
system-package install could not authenticate with `sudo`; no system package was
changed. The failed bootstrap directory remains at
`/tmp/udt_selector_verifier_20260718.UbuSAO` under the no-deletion instruction.

The accepted run used a new environment at
`/tmp/udt_selector_verifier_20260718.Fdx9MX/venv`, created without pip and with
`include-system-site-packages = false`. The host pip installer placed only the
two exact locked distributions into that environment's private site-packages:

```bash
python3 -m venv --without-pip /tmp/udt_selector_verifier_20260718.Fdx9MX/venv
python3 -m pip --isolated install --disable-pip-version-check --no-deps --no-compile \
  --target /tmp/udt_selector_verifier_20260718.Fdx9MX/venv/lib/python3.10/site-packages \
  -r native_action_external_verifier_2026-07-18/requirements-verifier.txt
```

Installed versions:

- Python `3.10.12`
- SymPy `1.13.1`
- mpmath `1.3.0`

The acceptance run used an isolated parent interpreter and isolated child
interpreters. User site and system site-packages were disabled, the repository
was absent from the verifier import path, `CUDA_VISIBLE_DEVICES` was empty, and
no GPU library or workload was invoked:

```bash
PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES= \
  /tmp/udt_selector_verifier_20260718.Fdx9MX/venv/bin/python -I -B \
  /home/udt-admin/udt_mass_codex/native_action_external_verifier_2026-07-18/verify_frozen_adjudication.py \
  --repo /home/udt-admin/udt_mass_codex \
  --work-root /tmp/udt_selector_verifier_20260718.Fdx9MX/work_final \
  --report /home/udt-admin/udt_mass_codex/native_action_external_verifier_2026-07-18/VERIFY_RESULT.json
```

The earlier diagnostic work trees and the accepted final isolated work tree are
all retained under `/tmp/udt_selector_verifier_20260718.Fdx9MX/`; nothing was
deleted.

## Acceptance result

- 24 of 24 copied CAS scripts exited zero.
- All 24 produced empty stderr and byte-exact stdout matches.
- Altered-manifest, altered-stdout, nonzero-exit, stderr, and dependency-version
  catch-proof probes all passed.
- Every internal package manifest passed before and after replay.
- Every complete package-state digest, including path, bytes, size, and mode of
  every regular file, was identical before and after.

| Frozen package | Manifest SHA-256 | Complete state before | Complete state after | Unchanged |
|---|---|---|---|---|
| Stage-I A | `d72e8d6e1b4bc8682bd5518264a1a43a3b5f7b3b246b3d218ea6bfecc6927d19` | `f7fbe7ba496f59b71413583a52ac257c83b46cabbaaa4ec673dd43e170c0a020` | same | yes |
| Stage-I B | `a99937a8fbba57ac24f490c2974937718f7dfbc2f2f7dd7c960d57fc5e839b92` | `4d10413939c2905adfe5c2a01115188867446c2cf3cc07ee305e67f39a4b38e9` | same | yes |
| Stage-II A | `ad63ffacdd5282a35fe0aef62269464d987aa61b710a4d393d95836234fd670a` | `b7a0efd64f32f91a5afdce31e6c8601712e5b26157bd509d2cfd110e5abc4f41` | same | yes |
| Stage-II B | `30b2a3863f1d16e3b3507b5d0bf10a6b5b59c1e54d769cacc53127cc676d6d45` | `cc250221af55787ed62702f6fee6d31c495436becc6ffedc623fe5469b553fac` | same | yes |
| Arm C | `99fc0d6c26aff24e43b8636d74f80e3486c56131590552308b47c1d107ed500f` | `b6e7ca7997ced0000be4e15c18799c1e77630e51da5ea6d5467c829c8a00b47b` | same | yes |
| Final adjudication | `57be0046432c27046e84eaafd1706959558f43170d0f1e23dc3047966e512f33` | `2b4a2c3d6a6881753822bf096e28f170a464d5a29666a4d1d4fb93af8814ba7e` | same | yes |

The complete machine-readable result, including every script hash and output
hash, is `VERIFY_RESULT.json`. The verifier and this record are external to all
six frozen packages.
