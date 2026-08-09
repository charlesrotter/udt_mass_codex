# Strict-refinement return — two certification failures preserved

Date: 2026-08-09  
Artifact: `corrected_full_atlas_strict.json`  
SHA-256: `46e8aeda120f6c51fbfc000cf56e5db5a78fe2092ae12b06b20523bc468ec1d5`

The strict replay completed every saved root, but failed two gates.

## 1. Preregistered count arithmetic was wrong

The correct total is

```text
420 spectral rows * 3 m channels * 8 positive roots = 10,080 roots.
```

The preregistration and script mistakenly named 5,040.  The loop was row-driven and actually
processed all 10,080, as the preserved transcript shows.  The count key therefore fails by design;
the artifact is complete despite the false expected denominator.

## 2. Three row/channel residual maxima remain above the frozen gate

The maximum fell from `4.4994475719329153e-05` to `3.1651399137290735e-08`, but the gate is `<2e-8`.
Exactly three row/channel maxima fail.  All share

```text
inv_n=0.9284, q/qcrit=0.95, hbar=0.001, wall=D,
m=-1,0,+1.
```

The other 1,257 row/channel maxima pass.  The maximum absolute change among all 10,080 strict roots
is `5.7209348369724466e-11`; the exact q=0 split error is `1.8943735469179046e-12`.

A diagnostic reroot of only the affected 24 frequencies with the same endpoint integrator and
integration tolerances, changing Brent `xtol` from `5e-15` to `1e-18`, gives channel maxima

```text
m=-1: 3.4733e-12
m= 0: 4.6769e-12
m=+1: 6.4257e-12
```

and changes those strict frequencies by at most `1.0953e-15`.  This supports an ultrafine
root-certification correction; it is not yet the banked passing atlas.
