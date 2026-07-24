# Verification report

## Independence

`verify_dual_systole_global_transport.py` uses only the Python standard
library and does not import `derive_dual_systole_global_transport.py`.
It rebuilds the numeric lattice objects, integer transformations, exact
fractional connection controls, source hashes, and completion coverage.

This is method independence for the finite controls. The analytic theorem is
also restated as a determinant/Gauss-reduction proof in
`EXACT_DERIVATION.md`; it does not rely on the production enumeration.
No external-model adversarial review was performed, which remains a caveat
rather than being silently called independent model-family evidence.

## Reproduced load-bearing quantities

- chart inversion samples: 35;
- maximum chart residual: `1.4210854715202004e-14`;
- standard-wall controls: 5;
- independent reduced-wall samples: 9;
- lattice coefficient bound: 50 with exterior eigenvalue lower bounds;
- maximum shortest-line tie: 3;
- `GL(2,Z)` controls: 6;
- maximum covariance norm residual: `1.1102230246251565e-16`;
- projected-connection residual: exact fractional zero;
- completion classes: 12/12;
- catch-proofs: 16/16.

## Fail-closed suite

The verifier rejects a corrupted metric-chart residual, a nonunimodular
co-shortest assertion, a missing wall winner, a false four-way tie, a
non-unimodular transition, a broken connection pairing, a tie-free
continuation claim at the reciprocal crossing, an invalid cap extension, a
global character on a nontoric class, a silent sign promotion, a physical
promotion, GPU or matter-solve scope creep, missing or duplicate completion
rows, and a phase-section promotion.

Repository-level catches separately reject scope leakage, frozen-manifest
change, current-path/frontier failure, original dirty-checkout change,
science authority promotion, and incomplete package coverage.
