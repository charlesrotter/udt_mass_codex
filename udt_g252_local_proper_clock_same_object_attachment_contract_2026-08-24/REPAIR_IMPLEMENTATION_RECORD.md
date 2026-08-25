# G252 repair implementation record

Date: 2026-08-24

The preregistered repair changed only exact-source location handling:

- production accepts exactly one of `ROOT / relative` or `ROOT / sources / relative` and requires
  the manifest SHA-256;
- the independent implementation separately applies the same location law without importing
  production code;
- the package verifier applies its own exact resolver and now rejects missing, ambiguous, and
  hash-mismatched layouts while accepting repository and sealed layouts;
- all three saved scientific JSON records were regenerated with unchanged contents;
- the package verification record was regenerated with five new source-layout checks.

No source membership, source content, scientific equation, premise status, clock value, coefficient,
history, or conclusion changed.
