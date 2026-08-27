# G282 registered no-write commands

Run from the repository root.

Preregistration and frozen-source gate:

~~~bash
python3 udt_g282_complete_history_depth_jacobi_minimal_law_type_2026-08-27/verify_preregistration.py
~~~

Exact symbolic derivation:

~~~bash
python3 udt_g282_complete_history_depth_jacobi_minimal_law_type_2026-08-27/derive_minimal_law_type.py
~~~

Independent standard-library Jacobi replay:

~~~bash
python3 udt_g282_complete_history_depth_jacobi_minimal_law_type_2026-08-27/verify_independent.py
~~~

Hostile mutation catches:

~~~bash
python3 udt_g282_complete_history_depth_jacobi_minimal_law_type_2026-08-27/run_catch_proofs.py
~~~

Fail-closed package verification:

~~~bash
python3 udt_g282_complete_history_depth_jacobi_minimal_law_type_2026-08-27/verify_package.py
~~~

All commands print to stdout and make no persistent changes.
