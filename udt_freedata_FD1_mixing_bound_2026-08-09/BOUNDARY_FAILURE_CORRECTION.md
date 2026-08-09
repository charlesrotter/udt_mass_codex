# FD1 boundary-failure correction layer

Date: 2026-08-09
Status: preregistered correction after the frozen boundary-location gate failed; no threshold changed

## Preserved failure

`phase2_transition_refinement_failed_boundary.json` is immutable evidence of a 4/5 return. The
registered maximum grid-to-grid boundary log drift was `<0.10`; the observed maximum was
`0.13601190551256975`. The two failures are the `q/qcrit=0.75` exit edges:

- D: grid-180 `0.0473016`, grid-240 `0.0412864`, log drift `0.1360`;
- N: grid-180 `0.0284540`, grid-240 `0.0253747`, log drift `0.1145`.

That key is not relaxed, deleted, or reinterpreted as passing. Exact transition locations remain
`OPEN` at the requested precision.

## What did survive

Every original inside/outside endpoint retained its orientation at grid 320 and with the asymptotic
join moved 10x and 100x deeper. Every recomputed raw backward residual was below `1e-8`. Therefore
the failed edge-location gate does not by itself erase the fixed interior witnesses or turn the
sampled neighborhoods into single-grid points.

## Independent existence audit frozen here

The next run may certify only **existence of strict interior affine-comparison witnesses**, not edge
locations. It must use the already frozen independent Phase-I machinery: `solve_ivp` metric
coordinate plus nonlinear symmetric eigenvalue roots, without importing the production derivation.

Fixed inside witnesses, each required across all three SNe-conditioned `n` values:

```text
q/qcrit=0.75, wall D, hbar=0.01
q/qcrit=0.75, wall N, hbar=0.01
q/qcrit=0.95, wall D, hbar=0.5
q/qcrit=0.95, wall N, hbar=0.5
```

Fixed outside controls covering both sides of all four families:

```text
0.75 D: 0.001, 0.05
0.75 N: 0.002, 0.05
0.95 D: 0.1, 1.0
0.95 N: 0.1, 1.0
```

Required gates:

- all 12 inside configurations are strictly inside and all 24 outside configurations are outside;
- independent frequencies agree with the grid-240 atlas within 3%;
- independent raw backward residuals are below `1e-8`;
- every inside row also lies between the actual adjacent troughs;
- the registered affine residual is at most 3.1% on each inside row, while the one-scale diagnostic
  remains worse than 20%, forcing the spent-offset caveat to travel;
- the failed boundary artifact remains identified as failed;
- catch-proofs reject missing/duplicate witnesses, loss of the affine-offset disclosure, promotion
  of a failed inside witness, erasure of the one-scale mismatch, and erasure of the boundary failure.

The 3.1% line is still a historical comparison label, not a native selector or exclusion criterion.

Maximum conclusion if all gates pass:

```text
FD1-AFFINE-COMPATIBILITY-EXISTENCE-VERIFIED-WITH-CAVEATS;
EXACT WINDOW BOUNDARIES OPEN;
ONE-SCALE NATIVE PROJECTION NOT ESTABLISHED.
```
