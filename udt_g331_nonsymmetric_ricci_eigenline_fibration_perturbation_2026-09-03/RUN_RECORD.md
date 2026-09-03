# G331 run record

Date: 2026-09-03
Device: CPU
Python mode: `python3 -S`
Long solve: none

## Preregistration

`31d907ab` — `Preregister G331 nonsymmetric eigenline test`

## Registered outcome runs

```text
G331 production PASS: 59 exact checks
G331 independent PASS: 44 exact checks
G331 hostile PASS: 10/10 caught
G331 package PASS: 47 aggregate gates
```

The production route uses exact second-order rational jets at independent interior points. The
independent route uses exact rational functions over the full interior `x` domain and separately
assembles the metric inverse, connection, Ricci tensor, and Ricci endomorphism. It imports no
production code and reads no production result.

The weighted metric counterfamily was discovered during execution rather than named in the frozen
preregistration. `EXECUTION_NOTE.md` records that chronology and makes fresh external independent
rederivation a required gate for the stronger spatial-metric non-openness claim.

## Fresh external adversarial review

The reviewer authenticated the sealed 41-file intake and all 39 manifest payloads, ran the four
registered commands in a writable ephemeral copy, and regenerated all four JSON artifacts
byte-for-byte. It independently rederived the post-preregistered weighted metric family and
returned:

```text
ACCEPT__G331_BOUNDED_EIGENLINE_FIBRATION_BOUNDARY
```

## Scope

Exact geometry and topology classification only. No GPU, fit, observation, constraint solve,
matter field, action, physical scale, or long-time evolution was run.
