# Candidate-exposed fidelity checks

Exposed after SOURCE_FIRST.md was written: TSI1 INITIAL_CANDIDATE.md and
NUMERICAL_FREEZE.md. The source-first report received one line-break typo fix
after exposure; no scientific change. Parent reports independently freezing
the angular route before reading this reviewer's matching angular lead.
This reviewer does not attest unseen discovery chronology beyond those disclosures.

The construction-result schema probe also printed numerical output; that
exposure is explicitly disclosed. No blind numerical confirmation is claimed.
No parent producer code has yet been read or imported. Candidate audit found
no source-fidelity defect: smooth differentiated asymptotics, units, source
cadence, angular reference, mass interface, calibration/selection and
finite-data limits all survive. In particular the angular derivation is confined
to b_*=0 rather than extended to a generic angular endpoint.

Freeze additional checks before execution: independently recompute the six
saved60-digit cases with R=100000, E=1 or10, b_*=0,2,-3 using the unchanged
source-first branch implementation at50 digits. Compare b,A,Z and timing drift
with relative error divided by max(1,|value|)<1e-25. Compute angular theta and
its proper-time rate by direct R and b partial differentiation and the independently
derived db/dR, with the same1e-25 tolerance. Independently integrate receiver
proper time between each pair of the two saved finite-difference endpoints and
recompute both averaged logarithmic rates, tolerance1e-25. These two endpoint
readouts use saved b/Z/theta and do not re-solve incidence.

Budget remains<=100 including all review cases:12 source-first finite solves,
8 exact/control groups, then6 new solves and2 saved-endpoint average controls.
CPU-only,2GiB,one BLAS thread,no timeout; existing capture. No parent-code
execution or mutation is needed. Preserve any failed output; stop and report
before source-preserving repair. Later semantic integration review and hash
attestation remain required.
