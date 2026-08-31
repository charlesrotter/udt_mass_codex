# G307 run record

Date: 2026-08-30

## Preregistration

- pushed commit: `1bdfe7d27b01954bea270d9540acd2de27570508`
- parent: `9385ea2f98be8042cd355a651ae0bc3357b7ff62`
- no executable or outcome artifact existed in that commit

## Production

Command:

```bash
python3 -S derive_directed_member_reconstruction.py
```

Result: PASS; candidate 2; 36 exact rational cases; 1,806 assertions; one member per chirality
after `(p,v)`; two members after route data; one after signed transverse-screen first jet.

## Independent replay

Command:

```bash
python3 -S verify_directed_member_independent.py
```

Initial result: PASS; 1,000 random oriented frames; 17,000 checks; maximum error
`4.1389114358025836e-13`; no production import. After preregistered R2, the verifier independently
solves both evaluation maps from `(p,v)`, recovers the closed formulas and full operators, and
passes 32,000 checks with the same maximum error.

## Hostile controls

Command:

```bash
python3 -S run_catch_proofs.py
```

Initial result: PASS; 14 semantic result mutations caught. After preregistered R3, the suite also
catches eight direct exact mathematical corruptions, for 22 total hostile cases.

## Premise audit

Command:

```bash
python3 verify_current_scientific_premises.py
```

Result: PASS.

## Repository regression

Command:

```bash
python3 -m pytest -q
```

Result: PASS; `199 passed, 1 xfailed in 137.60s`. The expected xfail is the registered matter-lane
habit-pin sentinel and is unrelated to G307.

## External review and repairs

Fresh gpt-5.4 review returned `G307_REPAIRABLE_DEFECTS` while finding no scientific defect and
retaining the exact landing. R1--R4 were preregistered and pushed at `f91bfb85`.

```bash
python3 -S verify_repair_portability.py
```

Result: PASS. Repository and sealed-layout builders produce identical manifests and detached
seals; missing and ambiguous source layouts are rejected.

## Repair-only external follow-up

Authorized sealed intake:

- path: `/tmp/udt_g307_repair_followup_8zv2k2cq`
- scope SHA-256: `7f9d49371d1aabca4bf407a33a814019d368295f4946aecb1deff9f717e8bf1a`
- manifest SHA-256: `e2faa3201f4bc21b6bd4d7822d722cfb1ec578adaf13259126b71792b9af0586`

The gpt-5.4 reviewer ran every sealed production, independent, hostile, portability, and package
check in a writable ephemeral copy and compared regenerated evidence with the sealed originals.
Verdict: `G307_REPAIRS_ACCEPTED`; no replay defects and no scientific regressions. The exact
landing, member census, metric, and reciprocal kernel remained unchanged.
