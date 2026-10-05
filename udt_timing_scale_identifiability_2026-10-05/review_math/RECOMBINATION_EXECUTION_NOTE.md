# Recombination capture correction

The first recombination of the already-saved31 replay solves was invoked in a
plain Python heredoc, without the capture wrapper's explicit2GiB/1BLAS limits.
No root solve or production occurred; two scalar proper-time integrals and
saved-value arithmetic passed. The original SAVED_RECOMBINATION_RESULT.json is
preserved. Its printed maxima were homothety1.0358802704502068e-10 and finite
slope2.564726209186574e-12. The mistake was an execution-record/resource-wrapper
omission; no scientific formula, finite cases or tolerance changed.

The same body is now saved as recombine_saved.py (only output destination and
an exact initial-result comparison added) and rerun with the required capture
wrapper. This supplies actual resource/command/stdout/stderr provenance.
No additional incidence solves; cumulative root cases remain67/100. The initial
unwrapped arithmetic is not retroactively claimed to have been resource-capped.
