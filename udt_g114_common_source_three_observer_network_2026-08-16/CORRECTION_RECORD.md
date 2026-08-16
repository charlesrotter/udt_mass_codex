# G114 correction record

## Source-affine calibration correction

During derivation, the initially written `Q+Q` source phase lift was recognized as the
source-normalized or matched-frequency form. The general native-affine junction is

```text
diag(Q_ji, (omega_j/omega_i) Q_ji),
```

and is conformally symplectic. Exact unequal `omega=(2,3,5)` controls were added in both
implementations; the ratios telescope around the observer loop. No prior outcome was discarded.

## Adversarial evidence-harness repairs

The fresh reviewer found three false-pass risks:

1. the package verifier trusted saved JSON instead of rerunning the scripts;
2. the scripts returned shell success even on a logical `FAIL`;
3. the independent caustic check assigned its expected matrices rather than independently
   producing them.

Repairs:

1. `verify_package.py` now subprocess-reruns both implementations and exact-compares fresh JSON;
2. all three scripts exit nonzero on failure;
3. production derives and checks the exact oscillator fundamental matrix, while the independent
   verifier integrates the oscillator to `pi` with fixed-step RK4.

The bounded follow-up returned `PASS`. The mathematical landing did not change.
