# Radial-shear variation-domain correction

The first background harness run recovered the product action exactly but stopped because it
expected the reduced `r`-only shear projection to vanish on every full-Bach product branch. Instead
it found

```text
Euler_s | full Bach = (8/3) K (y_second - 2K).
```

This conflicts with the already independently replayed pointwise Bach tensor unless the domains of
variation are distinguished. The expectation was therefore invalid, not the algebraic result.

Holding `F(theta)`, its angular domain, and the toric periods fixed while changing the two leg scales
by functions of `r` is not an unrestricted compact-support variation of a curved angular surface.
It can change cap regularity, cone angle, or angular identification. Its reduced Euler expression is
an ansatz/domain projection and is not allowed to replace the full metric equation.

The distinction has an exact catch-proof. A constant-curvature product with
`y_second=-2K` and higher derivatives zero is an Einstein product and satisfies the complete product
Bach system. The restricted radial shear projection is nevertheless `-32 K^2/3`. Conversely, the
conformally flat branch `y_second=2K` makes that restricted projection vanish. Promoting the latter
to a selector would silently discard a legitimate Bach-flat Einstein branch through the frozen
angular variation domain.

The script is corrected to record and test this obstruction rather than require the spurious
projection to vanish. The preregistration already required ansatz projections not be renamed the
unrestricted equation. No profile, tolerance, physical premise, or outcome was changed after seeing
the result.
