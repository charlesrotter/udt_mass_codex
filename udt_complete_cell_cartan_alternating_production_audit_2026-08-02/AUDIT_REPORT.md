# Complete-cell Cartan alternating-production audit

Date: 2026-08-02

Status: `VERIFIED-WITH-CAVEATS` — exact production plus a non-importing independent Koszul
reconstruction in the same warm context; no fresh blind model review.

## Result first

Outcome:

```text
SPLIT_RELATIVE_DIFFERENTIAL_PRODUCTION_ONLY__PRIMITIVE_AND_NATURALITY_OPEN
```

The complete stationary `S3` first-Cartan system contains a genuine contact coefficient

```text
t1=kappa exp(phi)/det(P)
```

and therefore supplies the exact identity

```text
-dphi wedge dlog|t1| = dphi wedge dsigma,
sigma=log(|det(P)|/D0).
```

Together with the founded `phi`, the antisymmetric primitive built from `log|t1|` equals the
cold-reviewed `lambda=(phi dsigma-sigma dphi)/2` modulo an exact constant-reference term. This is
the first bounded demonstration that the available alternating class is encoded by an actual
complete-cell first-Cartan coefficient rather than only written down from two arbitrary scalars.

## What the result does not establish

The construction still depends on the registered ruler/screen split. It is invariant under local
screen `O(2)` presentation changes (and orientation after `|t1|`), but no split-free angular scalar
or arbitrary complete-frame descent has been derived. The primitive is available, not selected as
a connection, response law, or equation.

The displayed `m=kappa exp(-phi)` term is explicitly not load-bearing: under a position-dependent
screen rotation its separation from the skew part of `L1` is presentation-dependent. Removing it
leaves the `phi,t1` derivation intact.

An exact full-curvature calculation on the complete isotropic-screen `S3` control finds zero
`dphi`/`dsigma` bilinear rows and zero alternating projections. Thus the identity is a Cartan
differential invariant, not a curvature term on that control. Full general-screen curvature remains
open. All eight complete FC07 mapping-torus controls have constant `phi`, so their pullback rank is
zero.

## Evidence

- preregistration commit `4fd8b6e` before production;
- 29-source immutable manifest commit `26615a7`, SHA-256
  `38eb34a623f844991d4b17f18d239bbcce7248f82f34fd70a3dc0011e04f79a1`;
- exact affine rank `1` and universally exact kernel dimension `5`;
- constructive smooth complete-`S3` rank-one witness and mandatory FC07 rank-zero control;
- full zero-torsion, metric-compatibility, scalar-closure, and `d^2 theta=0` checks;
- independent Koszul/frame curvature reconstruction with exact agreement;
- 11/11 exercised fail-closed semantic catches.

## Evidence gates

1. **Preregistered:** yes.
2. **Full or bounded:** full for the frozen first-Cartan candidate census and both actual complete
   families; curvature is full only on the stated isotropic-screen `S3` control, not full `GL(2)`.
3. **Independent:** exact non-importing Koszul reconstruction, but no fresh blind model; grade is
   capped at `VERIFIED-WITH-CAVEATS`.
4. **Premises audited:** yes; topology, stationarity, split, orientation, contact coefficient,
   presentation direction, branch pullback, action, carrier, source, density, and bootstrap scopes
   are explicit.

## Maximum conclusion

A split-relative complete-cell Cartan differential joint has been derived with fixed coefficient
one in the registered log-area normalization. No observer-natural response law, unique primitive,
dynamics, density bracket, bootstrap closure, action, source, carrier, mass, or matter result has
been derived.

