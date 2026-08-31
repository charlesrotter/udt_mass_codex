# G306 run record

Date: 2026-08-30
Preregistration ancestry: pushed commit c5873d2c
Mode: CPU symbolic production plus implementation-distinct standard-library replay

## Production

Command:

    python3 udt_g306_intrinsic_hopf_section_frame_descent_classification_2026-08-30/derive_intrinsic_hopf_section.py

Result: PASS, 172 assertions.

## Independent replay

Command:

    python3 -S udt_g306_intrinsic_hopf_section_frame_descent_classification_2026-08-30/verify_intrinsic_hopf_section_independent.py

Result: PASS, 22,237 checks; maximum numerical error
1.0280862827727333e-09; independent normalized Hopf result
-1.0000000010280863.

## Hostile controls

Command:

    python3 -S udt_g306_intrinsic_hopf_section_frame_descent_classification_2026-08-30/run_catch_proofs.py

Result: PASS, 17 direct mutations caught.

No GPU, background solve, observation, fit, network download, protected package, or external action
was used.

