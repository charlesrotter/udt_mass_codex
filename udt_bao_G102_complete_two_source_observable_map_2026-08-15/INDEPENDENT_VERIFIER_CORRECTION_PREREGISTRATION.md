# Independent-verifier fixture correction preregistration

Date: 2026-08-15

Recorded after the primary symbolic script passed and before the independent verifier was executed.

## Failure found by inspection

`verify_two_source_independent.py` contains manually entered expected pair-count vectors that do not
correspond to its own frozen four-data/five-random synthetic catalog and three exact cosine bins.
The verifier has not yet been run. Direct pair listing gives:

```text
DD = (8,15,12),
DR = (19,18,13),
RR = (2,4,4).
```

With the already frozen totals `(35,50,10)`, the exact Landy--Szalay vector is

```text
(-58/35, 19/70, 39/70).
```

## Frozen repair

Change only the four hardcoded expected vectors to those values. Do not change:

- a catalog point or weight;
- a bin threshold or boundary convention;
- a normalization total;
- the pair-count loops;
- any production/symbolic formula;
- a tolerance (all checks remain exact);
- the conclusion ceiling.

This is a verifier-fixture repair, not a scientific retuning and not an observational-data result.
It remains disclosed because the expected vector was written incorrectly before the first run.
