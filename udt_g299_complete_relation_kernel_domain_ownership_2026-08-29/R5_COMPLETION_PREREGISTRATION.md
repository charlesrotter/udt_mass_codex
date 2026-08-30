# G299 R5 replay-portability completion preregistration

Date: 2026-08-29

The repair-only reviewer verified scientific repairs R1--R4 and found one mechanical defect:
`derive_relation_domain.py` could not start in a minimal Python image without SymPy.

## R5 — dependency-free exact production replay

The production script may use SymPy when available, but must fall back automatically to exact
standard-library `Fraction` arithmetic when it is absent. Under `python3 -S`, the fallback must:

1. verify all nine frozen source hashes and nine source phrases;
2. reproduce the active-screen plane separator `-r^2 w`;
3. reproduce the shared W1 clock depth `Phi_T=Phi_L=-log(r)`;
4. reproduce the G274 equal-input/different-composition-output carry witness;
5. execute exactly 12,600 grid cases and 50,431 assertions;
6. emit the unchanged preregistered landing 3;
7. allow the independent verifier, hostile catches, and aggregate verifier to pass under
   `python3 -S`.

No scientific wording, equation, source universe, premise grade, candidate landing, or bounded
conclusion may change. R5 is packaging and replay portability only.
