# Parent numerical evidence fidelity

Reviewer inspected CHECK_CONTRACT.md, CHECK_FREEZE.json and the entire
check_beams.py after their outcomes. All four frozen hashes matched current bytes,
including unchanged initial candidate and discovery implementation. This is an
exposed code/output fidelity review, not blind confirmation or a second replay.

Actual candidate_checks receipt: started 22:06:27.464040 UTC, elapsed 7.674904 s,
exit 0, no timeout, RSS 85812 KiB. Output status PASS, no failure or warnings.

| Check | Actual maximum discrepancy |
|---|---:|
| Three complex-step Hessians vs original reduced flow | 2.6368e-16 absolute |
| Three same-segment directional-area reciprocity checks | 1.2976e-12 |
| Backward state restoration | 1.8690e-12 |
| Backward matrix composition, scaled | 1.1484e-13 |
| Source-observer area covariance | 1.1102e-15 |
| Target-observer area covariance | 2.6645e-15 |
| Target-observer quotient Gram matrix | 2.5697e-15 |
| Twelve invariant auxiliary/full-variation width comparisons | 2.6318e-10 |
| Three zero-amplitude homogeneous quadratures | 6.6957e-13 |
| Exposed worst discovery case tighter repeat, state | 1.2386e-11 |
| Eight long-reception illustrations, selected tighter repeat | 1.3114e-12 |

These satisfy their declared controls. The reverse-source normalization wo is
correct: h is homogeneous of degree one in p, so the backward position derivative
scales by wo when the source tangent is normalized to unit local frequency at the
other endpoint. The source-boost check allows a radial affine variation, which
the degree-zero path map annihilates; the physical transverse screen area gets
the expected source-Doppler-squared factor. The target projection adds a multiple
of k and preserves the quotient Gram matrix. Observer boosts are finite timelike
and remain supplied choices. G348 owns these laws; this code is regression support.

The pure-axis long-reception calculations use the exact auxiliary system and
quadrature in the full supplied metric, not a frozen/averaged field. They illustrate
the analytic orders but do not certify limits. The candidate's mixed-ray positivity
proof includes every psi; twelve numerical mixtures are not what establishes that
quantifier. The parent and reviewer retain distinct original-ray implementations;
within the parent checks, field/Hessian sharing limits the independence of repeats.

Three actual parent hostile runs were preserved and correctly rejected:

- Dropped spatial Hessian: exit 1, screen orthogonality 0.0003288246.
- `drop_source_lapse`: exit 1, invariant-width discrepancy 0.2477117. This flag
  actually multiplies measured widths by 0.75, a 25 percent width corruption;
  it does not literally omit the source L_e matrix. The reviewer's separate
  `source_normalization` variant does literally replace L_e by I.
- Wrong reverse normalization: exit 1, reciprocity discrepancy 0.1812349.

These are deliberately adverse variants, not unexplained baseline failures or
scientific repairs. The initial candidate and parent science code remain at their
frozen hashes. Source bookkeeping correction about an uncollected tool session
versus an already finished process is explicit in the check contract. No stronger
chronology or independence claim is warranted by the hashes.
