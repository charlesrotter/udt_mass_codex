# Independent-verification note

The independent verifier uses only Python's standard library and exact
`Fraction` arithmetic. It does not import SymPy, the production
controller, or any function from the parent transport package.

It independently checks an even reversal witness, seal coincidence,
nonzero bulk connection difference, exact projector invariance under
one-form rescaling, and the nonlinear reparameterization shift of
`A0`. It also exercises twelve fail-closed conclusion catches.

This is independent code and method at the algebraic-witness level. It
is not a fresh independent language-model adjudication, so the banked
result remains `VERIFIED-WITH-CAVEATS` rather than a stronger settled
physics claim.
