# P01 primary production resource note

Status: `PRIMARY OUTPUT FROZEN; RESOURCE REPLAY REQUIRED`

The corrected production run completed all 5,120 configurations on one Tesla
V100 in float64.  Its actual peak PyTorch allocation was
`20,687,226,368` bytes, whereas the preregistration estimated less than 6 GiB.
The device had 32 GiB and the run did not OOM, but the estimate was wrong and
the resource gate is not silently waived.

The root-level `ATLAS_*`, `CPU_ANCHOR_*`, and `TRANSPORT_CONVERGENCE.json`
files are the immutable primary output.  Before scientific interpretation, an
exact batch-16 replay must:

1. use the same source, seed, coefficients, shells, grid, transport method,
   dtype, and device;
2. peak below 6 GiB;
3. reproduce all coefficients exactly;
4. reproduce every discrete causal, repeated-tidal, nontrivial-holonomy,
   grid-resolution, and transport-resolution classification exactly; and
5. reproduce finite continuous features to scaled error at most `2e-10`.

Nonfinite transport entries must have the same finiteness/sign class.  The
replay is a resource and batch-independence check, not a new sample or an
outcome-dependent scientific retuning.  Until it passes, the primary atlas is
`VERIFIED-WITH-RESOURCE-CAVEAT`.
