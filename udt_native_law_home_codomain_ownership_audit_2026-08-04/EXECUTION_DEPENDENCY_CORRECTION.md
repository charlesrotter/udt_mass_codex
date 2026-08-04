# Execution dependency correction

The preregistration commit recorded `sympy==1.13.3`, but the synchronized repository environment and
the immediately preceding August 4 audit packages use SymPy `1.13.1`. Before final verification, the
package pin was corrected to the actually executed version `1.13.1`.

This is an environment-record correction. It changes no candidate, premise, tolerance, algebra,
classification, conclusion, or source hash. Production and independent calculations are rerun after
the correction; the independent calculation uses only the Python standard library.
