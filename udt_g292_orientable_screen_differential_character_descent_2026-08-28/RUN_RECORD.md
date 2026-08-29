# G292 run record

Date: 2026-08-28
Preregistration commit: `e6a1bdfb`

Commands:

```text
prerequisite: Python 3 with sympy available
PYTHONPYCACHEPREFIX=/tmp/udt_g292_pycache python3 -m py_compile derive_orientable_screen_flux.py verify_orientable_screen_flux_independent.py run_orientable_screen_flux_catches.py verify_package.py
python3 derive_orientable_screen_flux.py
python3 verify_orientable_screen_flux_independent.py
python3 run_orientable_screen_flux_catches.py
python3 verify_package.py
```

For a sealed read-only intake, first copy the package to a writable ephemeral directory such as
`/work/g292_review`, run the commands from that copy, and keep `PYTHONPYCACHEPREFIX` inside writable
ephemeral storage. Running `py_compile` against the read-only mount directly is not supported.

The first independent run stopped at the standard spherical coordinate pole because the directly
typed Christoffel expression divided by `sin(theta)`. The verifier was repaired to use the regular
curvature-density limit at the two Simpson endpoints. No metric, formula, parameter family,
tolerance, or preregistered landing changed. The repaired replay passed.

The sealed external reviewer reproduced the standard-library replay and hostile catches from a
writable `/work` copy. Its environment did not provide `sympy`; repair R1 now makes the aggregate
fail closed rather than reuse a preserved production JSON when that dependency is absent.

No GPU, ODE/PDE solve, observation, fit, action, source, mass, physical scale selection, Planck
cutoff, `X_max`, network access, or protected package was used.
