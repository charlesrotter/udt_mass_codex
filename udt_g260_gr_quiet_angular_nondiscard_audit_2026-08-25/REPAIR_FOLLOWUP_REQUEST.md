# G260 repair-only external follow-up request

Date: 2026-08-25

Review only the corrected sealed intake. Verify only preregistered repair R1 and that the bounded
scientific landing is unchanged. Do not edit evidence files or continue the research. Run the
registered checks only in a writable ephemeral copy.

## R1 — dependency-free production replay

Run:

```bash
python3 derive_angular_nondiscard.py
python3 verify_independent.py
python3 run_catch_proofs.py
python3 verify_package.py
```

Verify that:

1. `derive_angular_nondiscard.py` imports only Python-standard-library modules and reconstructs the
   full four-dimensional spherical, isolated two-dimensional, flat-screen, angular-interlock,
   vacuum-family, trace-balanced, mass-aspect, and nonradial-pullback claims from exact metric jets.
2. It does not import `verify_independent.py`, read a prior `DERIVATION_RESULT.json`, or require
   SymPy.
3. Its output SHA-256 is
   `ddc9b6f0ef357cf433d171472e51d49ca7c87352d5464ec4cf2d3349aa429248`, exactly matching the
   prerepair manifested result.
4. The independent replay still passes 10,044 exact assertions without importing production code
   or reading the production result.
5. All eight hostile catches and package integrity checks pass.
6. No equation, premise grade, scientific question, or bounded conclusion changed.

## Required return

Return `ACCEPT_REPAIR`, `ACCEPT_WITH_FURTHER_REPAIR`, or `REJECT_REPAIR`, followed by concise
findings. The scientific question is not reopened. The retained ceiling is the original bounded
static-spherical GR-quiet non-discard theorem; no global UDT parent equation, source/history law,
or loud/global extension is selected.
