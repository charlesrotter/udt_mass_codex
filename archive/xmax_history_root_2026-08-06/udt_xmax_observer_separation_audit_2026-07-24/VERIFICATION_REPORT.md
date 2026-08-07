# Verification report

The separate verifier does not import the production derivation.  It:

- re-reads and hashes all 907 base-commit source identities;
- reproduces the exact candidate identity SHA-256;
- checks one disposition per candidate and all 61 load-bearing sources;
- independently evaluates a boundaryless finite-diameter circle, a
  radius/diameter control, angular dependence of three-observer separation,
  the conditional one-dimensional projective identity, and constant-CSN
  scale neutrality;
- verifies all relational open/retained/withdrawn status gates;
- exercises 16 corruption catches.

Result: `PASS`, with 16/16 catches.  This is an independent implementation
within the same session, not a fresh external model context.  The audit is
therefore `VERIFIED-WITH-CAVEATS`.

