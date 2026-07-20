# Independent verifier zero-mode correction

The first independent-verifier invocation matched all 288 background Bach records and all
nonconstant twist witnesses, but its constant-twist check failed the registered `1e-9` absolute gate.
The raw second-difference estimate was `3.0716170347962666e-09` even though the exact symbolic
operator vanishes.

This is an ill-conditioned diagnostic: a second finite difference divides machine-level cancellation
among three separately reconstructed two-coordinate curvature scalars by `epsilon^2`. The correction
does not loosen the tolerance. It tests the exact zero-mode content directly by comparing the full
finite-amplitude scalar at

```text
epsilon = -0.2, 0, +0.2
```

for every registered constant-`u` witness, requiring the same absolute `1e-9` bound. The noisy
second-difference value remains recorded separately rather than hidden.

No metric, profile, curvature sign, formula, physical premise, or outcome changed. The failed
pre-bank invocation supplies no scientific result.
