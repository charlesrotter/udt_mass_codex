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

Result: PASS; 1,000 random oriented frames; 17,000 checks; maximum error
`4.1389114358025836e-13`; no production import.

## Hostile controls

Command:

```bash
python3 -S run_catch_proofs.py
```

Result: PASS; 14 of 14 direct mutations caught.

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

Result: PASS; `199 passed, 1 xfailed in 136.39s`. The expected xfail is the registered matter-lane
habit-pin sentinel and is unrelated to G307.

External adversarial review remains pending at this record stage.
