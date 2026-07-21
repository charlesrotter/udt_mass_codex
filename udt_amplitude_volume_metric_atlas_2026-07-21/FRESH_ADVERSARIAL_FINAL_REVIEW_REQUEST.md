# Final fresh adversarial review request

Preserve the preceding correction review's `FAIL`. Its single remaining finding was that active
design constants were not parsed from and compared directly with the committed preregistration.

Audit the final correction:

- the verifier must parse the exact Halton-base, Hadamard-column, and radius code blocks from the
  hashed committed preregistration;
- parsed values must equal the active constants used to reconstruct the design;
- malformed or missing blocks must fail closed; and
- an exercised common-mode active-constant drift must fail the comparison.

Also confirm the earlier seven accepted correction groups remain intact, the verifier passes 44
checks and 20 catches, and no claim exceeds the finite registered sample. Return `PASS` or `FAIL`.
Do not edit files or supply affirmative physics.

