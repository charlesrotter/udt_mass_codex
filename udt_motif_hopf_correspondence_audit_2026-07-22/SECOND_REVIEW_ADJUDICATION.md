# Second fresh-review adjudication

Date: 2026-07-22

The second fresh `FAIL` was accepted in full. It again preserved the raw census, exact conditional
toric/Hopf-seed witness, scientific maximum, and overall `LEAD`, while rejecting the first
correction's package certification.

| blocker | repair | result |
|---|---|---|
| fixed Jacobian reused along sampled edges | integrated each stored `(J,K,L)` into an explicit zero-constant cubic polynomial map and evaluated its Jacobian at every inverse-mapped node | 63,438 eligible edge assignments, zero discordance; confirmatory because reviewer exposed and probed this interpretation first |
| 60 uncertainty-bearing point cases absent | mutually exclusive point-status census written and validated | 67,396 both classified; 33 one-sided uncertain; 27 both uncertain |
| 50 skipped edges absent | every possible edge counted with reason | 63,488 possible = 63,438 matched + 50 `ORIGINAL_EDGE_UNMATCHED+TRANSFORMED_EDGE_UNMATCHED` |
| validator accepted six load-bearing corruptions | all six fields plus uncertainty, skip, map-mode, and connection mutations added to fail-closed validator | 23/23 corrupted records rejected |
| coordinate-map regularity unstated | inversion and Jacobian gates added | maximum inverse residual `1.1102230246251565e-16`; minimum absolute determinant `0.9643147372973677` |

The second correction does not strengthen the scientific conclusion. It makes the previously
accepted bounded conclusion reproducible and completely accounted at its stated scope.

