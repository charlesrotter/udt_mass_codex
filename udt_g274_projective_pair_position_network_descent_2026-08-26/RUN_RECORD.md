# G274 run record

Date: 2026-08-26

- branch: `grok`
- preregistration commit: `ab020eca`
- production arithmetic: SymPy exact rational/symbolic
- production checks: 26
- independent arithmetic: standard-library `fractions.Fraction`
- independent cases: 20,000
- independent exact assertions: 240,004
- active-screen cases: 20,000
- vector-only separators: 20,000
- radial Möbius controls: 20,000
- overlap covariance controls: 20,000
- persistent outputs: the three registered JSON evidence files only
- GPU: not used; no ODE/PDE or long solve required
- observational outcomes: not inspected

The only failed execution was the preregistered mechanical JSON boolean serialization issue recorded
in `PREREGISTRATION_EXECUTION_NOTE.md`.
