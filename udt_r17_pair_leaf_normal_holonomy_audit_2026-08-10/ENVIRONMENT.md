# Environment

The exact versions, command outputs, and their hashes are generated into `COMMAND_TRANSCRIPT.tsv`
by the package verification driver.  The scientific derivation is CPU-only.

Primary implementation: Python 3.10.12 plus SymPy 1.13.1 exact algebra.

Independent implementation: Python standard library only, using exact `Fraction` arithmetic,
dual numbers, Gauss--Jordan inversion, the inverse-matrix derivative identity, Koszul reconstruction,
and exterior differentiation.

External adversarial review: Codex `gpt-5.4`, sealed read-only 47-file intake (35 package files at
transmission time plus 12 actual manifest-pinned source files), session
`019fecc3-ba15-7e71-bc92-5d44f01a3908`. Focused provenance correction on the same authorized
payload: session `019fecc8-47bb-7fd1-a75a-22d2d5f2da69`.
