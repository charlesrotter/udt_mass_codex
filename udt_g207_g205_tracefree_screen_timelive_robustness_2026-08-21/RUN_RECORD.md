# G207 run record

Date: 2026-08-21

## Commands

```bash
python3 derive_tracefree_screen_robustness.py
python3 verify_tracefree_screen_independent.py
python3 run_boundary_diagnostics.py
python3 verify_source_manifest_repository.py
python3 run_catch_proofs.py
python3 verify_package.py
```

CPU/SymPy and exact standard-library fractions only. No GPU process and no long solve.

## Outcomes

- Production: 36/36 exact symbolic assertions passed.
- Independent: 110,009 assertions across an independent Euler-Lagrange orbit reconstruction and
  10,000 distinct exact-rational pair cases passed.
- Every rational case preserved the determinant-one ambient metric and completed reciprocal
  identity while changing the generic clock, pair-area, and shift readouts.
- Boundary: 100-digit Gaussian and bounded-screen controls passed.
- Mutation catches: 24/24 caught.
- Source provenance: seven live repository hashes matched the preregistered manifest.
- Package replay: byte-stable under `UDT_NO_WRITE=1`.
- External review: `VERIFIED_WITH_CAVEATS`; no mathematical error or scientific repair.

The first reviewer launch exited before the reviewer started because the installed CLI requires the
approval flag before `exec`. The corrected launch used the same sealed intake, digest, prompt, and
scope. The only post-review text repair was the missing LaTeX backslash in `\log\!\left`; it changes
no formula or scientific content.
