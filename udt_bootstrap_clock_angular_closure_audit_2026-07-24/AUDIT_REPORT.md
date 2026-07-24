# Bootstrap-aware clock/angular closure audit

Date: 2026-07-24

Preregistration: `2fc97f4`

Grade: `VERIFIED-WITH-CAVEATS`

## Result first

Charles's concern was correct in a precise, bounded sense: the recent B19
and WR-L failures were obtained without a complete self-consistent native
matter response. They remain valid in those branches, but they are not
universal no-go results for a matter-filled bootstrap universe.

A complete bootstrap could alter the screen tidal curvature and remove the
round-screen degeneracy. More importantly, the audit found that the desired
clock-curvature match would then select its own screen line.

Let `T` be the complete two-dimensional screen tidal operator and
`a=d delta/d lambda` the reciprocal clock rate. If

```text
Delta=(tr T)^2-4det T > 0
```

and

```text
det(T+a^2 I)=0,
```

then exactly one screen eigenvalue is `-a^2`. Its intrinsic projector is

```text
P_clock=I-(T+a^2 I)/(tr T+2a^2).
```

Thus simple spectrum plus clock matching supplies both the screen line and
tidal invariance. A line no longer has to be chosen by hand.

## What remains

Two geometric gates remain:

1. parallelism, equivalently `[T,D_lambda T]=0` on the simple-spectrum
   domain; and
2. descent through complete finite-cell gluing/holonomy.

There is also a path-level caveat. The negative-curvature relation gives
pointwise natural-frame generator similarity. If the clock rate varies, the
pointwise eigen-intertwiner varies too. A full cocycle equivalence needs
either constant `a` in that frame or an additional metric-derived connection
or normalization term. No such term was inserted.

## What bootstrap can and cannot do

The owner-stated narrow-density principle currently acts after complete
solutions are obtained. In that form it can accept or reject a universe, but
it cannot create local equations.

For

```text
rho_tot=M_native/V_proper,
```

the exact variation is

```text
delta rho_tot
  =(delta M_native-rho_tot delta V_proper)/V_proper.
```

The volume term is purely trace and cannot select a transverse line. The
mass variation could be anisotropic and could change `T`, but only after a
native off-shell mass/matter functional and its metric variation exist.
Neither currently exists.

Therefore the missing object is not a value of density. It is the
same-solution response interface:

```text
native off-shell mass/matter functional
+ local metric/matter variation
+ differentiable finite-cell boundary/global variation.
```

This is the minimum architecture through which bootstrap could affect the
clock–angular geometry without circular insertion.

## Complete registered census

The frozen source universe contains 35 load-bearing sources, the exact 28
registered equation families, and all 12 registered finite-cell completion
families.

- Zero equation families supply a complete simultaneous
  metric–matter–boundary bootstrap.
- Zero completion families supply a complete `(g,phi,matter)` solution with
  density feedback.
- The bootstrap selector family explicitly leaves its varied functional,
  functional derivative, and representative map open.
- The conditional carrier branch may contain directional matter structure,
  but it has no native metric source and cannot be used as an unconditional
  bootstrap.
- No density value, center, width, response law, carrier, action, or
  boundary rule was invented.

## Regraded negatives

- B19: exact conditional branch failure; not a matter-filled universal
  no-go.
- WR-L: exact local profile failure; not a matter-filled universal no-go.
- Geometry-only finite-cell density census: still correct. Its constant
  branch map arose because density was not an argument of the equations,
  not because physical density has no effect.

## Verification

The pinned SymPy `1.14.0` production replay passed 33 exact checks. A
separately structured standard-library/Fraction implementation reconstructed
27 screen cases, nine matched projectors, nine parallel-transport cases,
three connection cases, and 27 density variations. It replayed all 35 source
hashes, eight bootstrap routes, 28 equation families, 12 completion families,
and rejected 23 exercised corruptions.

No fresh external-model semantic review was launched, so the result is
`VERIFIED-WITH-CAVEATS`, not a canon candidate.

## Honest conclusion

Bootstrap is now a credible potential resolver of the clock–angular seam,
not because “density bends things,” but because a simultaneous native matter
variation could create the exact anisotropic tidal structure that selects
the matched line.

Current UDT does not yet derive that response. The irreducible solder,
complete action, native source, boundary completion, density window, scale,
carrier emergence, and mass remain open.
