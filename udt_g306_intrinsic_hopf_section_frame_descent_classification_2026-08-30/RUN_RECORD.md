# G306 run record

Date: 2026-08-30
Preregistration ancestry: pushed commit c5873d2c
Mode: dependency-free exact production plus implementation-distinct standard-library replay

## Production

Command:

    python3 -S udt_g306_intrinsic_hopf_section_frame_descent_classification_2026-08-30/derive_intrinsic_hopf_section.py

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

## External review and portability repair

Fresh external `gpt-5.4` review returned `REPAIRABLE_DEFECTS` with the bounded science supported.
Repairs R1--R4 were preregistered and banked at commit 1298deea before implementation.

The repaired production command runs with `python3 -S` and reproduces the original derivation JSON
and candidate census byte-for-byte. `verify_repair_portability.py` copied the package and all 15
frozen sources into a fresh temporary sealed layout, ran all four sealed commands successfully,
and proved that missing and ambiguous source layouts are rejected.

Repository-only gates were rerun after repair: the 288-row premise registry and 754 historical
dispositions passed; pytest reported 199 passed and one expected xfail.

No GPU, background solve, observation, fit, network download, protected package, or external action
was used.
