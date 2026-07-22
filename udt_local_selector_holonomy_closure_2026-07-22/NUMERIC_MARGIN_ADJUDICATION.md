# Independent closure-margin adjudication

The first passing independent verifier reported a smallest *incremental modified-Gram–Schmidt
acceptance residual* of `1.5521343880052345e-9` at `V009_M2_B3_P3`, close to the `1e-9` insertion
threshold. That number depends on word ordering: an almost-dependent word can be accepted before a
later, well-conditioned word spans the same final direction. It is not a singular-value margin for
the completed algebra.

The issue was examined before banking. For the flagged configuration, the normalized complete word
span has:

| maximum word length | smallest four singular values | rank at `1e-7`, `1e-9`, `1e-11` |
|---|---|---|
| 1 | `1, 0.94974521, 0.69092828, 0.00253096` | `7, 7, 7` |
| 2 | `1.0484098, 0.94171489, 0.85640607, 0.6862501` | `16, 16, 16` |
| 3 | `3.01194028, 2.76602791, 2.51103485, 2.42445459` | `16, 16, 16` |

An independent all-row length-two word-span sweep found the smallest full-algebra relative
sixteenth singular value to be `0.0031273654923097264`, at `R12_1_M4_B2_P2`. This is more than six
orders of magnitude above the registered `1e-9` rank gate. The `5,376` full-algebra census is
therefore not a threshold artifact.

The verifier now records this final word-span singular margin rather than presenting the
order-dependent incremental insertion residual as a certification margin. No scientific row,
tolerance, or classification was changed.

