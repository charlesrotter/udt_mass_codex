# Environment

The exact versions, command outputs, and their hashes are generated into `COMMAND_TRANSCRIPT.tsv`
by the package verification driver.  The scientific derivation is CPU-only.

Primary implementation: Python 3.10.12 plus SymPy 1.13.1 exact algebra.

Independent implementation: Python standard library only, using exact `Fraction` arithmetic,
dual numbers, Gauss--Jordan inversion, the inverse-matrix derivative identity, Koszul reconstruction,
and exterior differentiation.
