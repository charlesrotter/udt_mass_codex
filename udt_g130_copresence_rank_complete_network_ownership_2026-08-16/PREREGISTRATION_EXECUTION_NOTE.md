# G130 preregistration execution note

Date: 2026-08-16

The preregistered countermodel family was

```text
g_s = -s dt^2 + s^-1 dr^2 + r^2 dOmega^2,  s > 0.
```

The preregistration proposed comparing the identity member `s=1` with one nonidentity member
`s=1/4`. Fresh adversarial review correctly observed that the active premise ledger separately
marks realized nontriviality as `OBSERVED_OR_SEPARATE_POSIT`. The family and falsification logic
are unchanged, but the executed witness was strengthened to compare two nonidentity members:

```text
s=1/4  <-> phi=+log(2),
s=4    <-> phi=-log(2).
```

Both have reciprocal clock-ruler determinant `-1`. At `r=1` their exact scalar curvatures are
`3/2` and `-6`, so they remain nonisometric and now satisfy realized nontriviality individually.
This post-review strengthening is recorded explicitly rather than silently rewriting the committed
preregistration.
