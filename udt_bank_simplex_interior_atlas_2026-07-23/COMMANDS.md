# Commands

Production:

```bash
/usr/bin/time -f 'elapsed=%E maxrss_kb=%M' timeout 1200s \
  python3 udt_bank_simplex_interior_atlas_2026-07-23/build_bank_simplex_atlas.py
```

Observed:

```text
exit code: 0
elapsed: 1:49.43
maximum RSS: 868868 KiB
GPU runs: 0
```

Independent replay:

```bash
/usr/bin/time -f 'elapsed=%E maxrss_kb=%M' \
  python3 udt_bank_simplex_interior_atlas_2026-07-23/verify_bank_simplex_independent.py
```

Observed:

```text
exit code: 0
elapsed: 0:28.32
maximum RSS: 3031844 KiB
```

Repository test command and exact result are recorded in `REPOSITORY_GATES.json`.
