# Verification report

The package is certified within its preregistered bounded frame.

Science gates:

- 44 exact source identities replay;
- 36 exact production checks pass;
- all 30 local objects, 16 transitions, 18 invariants, 12 completions, and
  14 Hopf-crosswalk steps are present exactly once;
- independent stdlib/Fraction reconstruction imports neither SymPy nor the
  production module;
- production and independent outputs replay byte-identically;
- 26/26 registered failure mutations are rejected.

Repository gates:

- changes since preregistration are package-local;
- the six frozen native-action packages replay unchanged;
- current-path and frontier registries resolve;
- tests match the documented 70 passed/1 xfailed baseline;
- the original 54-path dirty checkout metadata is unchanged and its contents
  remain unread;
- no GPU, action, matter, density, mass, canon, or reorganization work
  occurred.

The absence of a fresh external model review caps the result at
`VERIFIED-WITH-CAVEATS`.
