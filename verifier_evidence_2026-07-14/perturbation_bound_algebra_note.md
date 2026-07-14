# Item-3 deliverable: exact algebra/data behind "raw-operator doublet = 0.2509 ± ..." — WITH CORRECTION

## What the blind verifier claimed (its report, commit 1c2196c)
"Perturbation bound: doublet<->T/R coupling ~1.7e-2 -> second-order shift ~(1.7e-2)^2/0.245 ~ 1.2e-3.
Full-space doublet = 0.2509 +/- ~1e-3."

## The exact algebra (recomputed in noNull_evidence_seal.py; data in noNull_stability_evidence.json,
## perturbation_bound + enlargedRR_spectrum_V_QTR_u1 per grid/seed)

Setup: orthonormal span S = [v_dbl0, v_dbl1, v_iso, Q_TR(6), u1]; A = S^T H_raw S (H_raw = tangent+
free-mask projected FD Hessian, NO deflation); blocks A_d (doublet 2x2), B_TR (T/R 6x6), C (2x6 coupling).
Bound formula: |shift| <= ||C||_2^2 / gap, gap = min |lam_dbl - spec(B_TR)|.

Measured (seed 0; seed 1 identical to ~1e-9):
| N   | ||C||_2   | spec(B_TR)                                   | gap    | bound   | exact-in-span doublet |
|-----|-----------|----------------------------------------------|--------|---------|-----------------------|
| 128 | 1.692e-2  | 0.031, 0.122, 0.122, 0.331, 0.331, 17.64     | 0.0785 | 3.7e-3  | 0.2550, 0.2550        |
| 192 | 1.702e-2  | 0.046, 0.184, 0.184, 0.497, 0.497, 26.34     | 0.0681 | 4.3e-3  | 0.2557, 0.2557        |
| 256 | 1.690e-2  | 0.061, 0.245, 0.245, 0.672, 0.672, 34.89     | 0.0055 | 5.2e-2  | 0.2652, 0.2652 (+0.2311 pair below) |

## CORRECTION (flagged discrepancy)
The verifier's gap (0.245) treated the T/R subspace by its CONVERGED pseudomode eigenvalues (~0.002-0.006).
That is the wrong operand: the deflation span Q_TR consists of the RAW centered-difference generators,
whose Rayleigh block spec(B_TR) runs 0.03-35 — and at N=256 one element (0.2454) is near-resonant with
the doublet (gap 0.0055). The correct-formula bound is then 5.2e-2, and the EXACT diagonalization of
H_raw on the 10-dim span shows the deflated doublet 0.2509 mixing into pairs at 0.2311/0.2652.

=> The supported statement is:
   raw-operator doublet-like eigenvalues (within the probed span) = deflated value +/- ~2e-2 at 256^3
   — NOT +/- 1.2e-3. The verifier's numeric bound is RETRACTED as stated; its qualitative conclusion
   ("positivity unthreatened") STANDS:
   - every enlarged-RR eigenvalue is POSITIVE at every grid (minimum = u1 at +3.4e-4 at 256^3);
   - the independent full-space hunt (N=128, u1-only deflation) found the full-space floor to be the
     POSITIVE T/R cluster, with the doublet at +0.2542/+0.2543 — no negative direction;
   - worst-case within-span doublet value 0.2311 > 0 by a wide margin.

Caveats: enlarged-RR values are variational (upper bounds within the span); the raw full-space
eigenpairs could differ further — but the full-space hunt at 128^3 is the direct check of that, and it
found nothing below the positive T/R cluster. Hunts at 192/256 were not run (bounded verifier scope).

## Gate language (per dispatch): the doublet raw (full-H) relative residual is 3.34-3.38e-2 at all
grids. This does NOT satisfy the 1e-3 raw gate and is not claimed to. The 1e-3 gate was met by the
T/R-DEFLATED invariant-subspace residual eta_c (5.7e-4..9.3e-4). The isolated mode satisfies the raw
gate outright (3.6e-5 / 7.2e-5 / 7.4e-4).
