# Commands

All production and verification work was CPU-only in the clean audit worktree.

```text
python3 udt_motif_hopf_correspondence_audit_2026-07-22/build_correspondence_atlas.py --workers 8
python3 udt_motif_hopf_correspondence_audit_2026-07-22/derive_toric_control.py
python3 udt_motif_hopf_correspondence_audit_2026-07-22/summarize_correspondence.py
env CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=8 MKL_NUM_THREADS=8 python3 udt_motif_hopf_correspondence_audit_2026-07-22/verify_review_corrections.py
env CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=8 MKL_NUM_THREADS=8 python3 udt_motif_hopf_correspondence_audit_2026-07-22/verify_correspondence_independent.py
env CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 python3 udt_motif_hopf_correspondence_audit_2026-07-22/verify_package.py
```

The correction and independent replay stdout/stderr are preserved in their transcript files. The
four fresh adversarial failures, correction records, and full terminal transcripts are also
preserved. `build_correspondence_atlas.py` now emits the same ten-row lineage required by the
corrected verifier; no manual post-build lineage repair is required.
