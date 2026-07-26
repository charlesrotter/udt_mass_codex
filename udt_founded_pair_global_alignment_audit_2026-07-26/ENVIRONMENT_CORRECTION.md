# Execution-environment correction

The committed preregistration package included `requirements.txt` with anticipated
`sympy==1.14.0`. Before banking, the actual clean CPU environment reported SymPy `1.13.1`, the same
version used by the immediately preceding calibrated-readout audit. No package was installed or
downloaded and no algebraic route, tolerance, or outcome class changed.

The original `requirements.txt` is preserved as preregistered historical evidence.
`VERIFICATION_REQUIREMENTS.txt` records the dependency that actually produced the saved output.
The independent implementation imports no SymPy.

