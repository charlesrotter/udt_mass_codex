# N01 C1 harmonic coupling-matrix atlas — audit report

## Current verdict

`VERIFIED-WITH-CAVEATS`.

The bounded C1 matrix architecture is derived, locally checked by a separate implementation, and
accepted by a fresh zero-context adversarial review after checker and wording repairs. The caveats
are the conditional C1 screen, chosen scalar diagnostic, bounded basis/control grid, and complete
absence of a radial/eigenvalue or physical-screen solve.

## Result

The exact stationary C1 scalar equation becomes

```text
d_r[r^2 A W(B)d_r R]-[K(B)+H_m(B)]R
+[(r^2 omega^2+2h omega m)/A]M(B)R=0.
```

C1 retains fixed `|m|`, the sign through the external rotation-linear coefficient, and north/south
parity. At `B=0` and `|m|>0`, `K` and `H` are individually mixed but cancel to the diagonal spherical operator;
at `m=0`, `H=0` and `K` is already diagonal.
At first order only `Delta ell=0,2` occurs. For every `B>0`, the coefficient functions have no exact
finite polynomial bandwidth; the bounded atlas observes same-parity coupling across much of the
available basis.

The full record contains 15,420 matrix elements, 120 block summaries, and 36 exact first-order
controls. No element was rejected for shape or observational usefulness.

## Four gates

1. **Preregistered:** yes, commit `1537d669d411c1bb4c18c0814dc1aef3af7ea36d`.
2. **Full or bounded:** complete for the registered `B`, `|m|`, parity, five-matrix, and
   `ell<=16` universe; other screens and every physical solve remain explicit omissions.
3. **Independently verified:** yes. A separate local adaptive-quadrature implementation checked
   eight selected matrix elements and all 36 first-order rows. The cold review independently
   reconstructed the equation, all 180 first-order values, the complete key universes, 18 hard
   matrix controls at 50 digits, and the premise boundary.
4. **Premises audited:** yes, in `STATUS_LEDGER.tsv` and `COMPLETENESS_MAP.md`.

Therefore the bounded result is bankable as `VERIFIED-WITH-CAVEATS`, not as a physical screen,
spectrum, or UDT-native dynamics.

## Stop boundary

`NO_EIGENVALUE_SOLVE`. `FD2_REMAINS_GATED`. No radial boundary, physical `B(r)`, CMB comparison,
population, polarization, GPU work, or C1 promotion is authorized.
