# Intrinsic ruler/full-screen Hopf descent audit

Date: 2026-07-28

Preregistration: `f362970`

Grade: `VERIFIED-WITH-CAVEATS_BOUNDED_STATIONARY_COMPATIBILITY_CLASSIFICATION`

## Result first

Both full-screen shears preserve the reciprocal ruler alignment. For every smooth invertible
screen `P`, the twist of the supplied stationary field is

```text
omega_K=plus_or_minus[c_E^2 alpha kappa exp(-3phi)/det(P)] theta1.
```

Hence nonzero clock twist still selects the ruler line exactly. Moreover, the six earlier exact
rank-three clock/ruler witnesses lie inside `C3`-open neighborhoods in which both independent shear
directions are released and the metric continues to select the unique clock line. The prior result
was not an artifact of freezing the screen to one scalar weight.

Founded normalization also remains exact:

```text
exp(-phi)theta1=sigma3,
```

which is the regular unit Hopf connection on the chosen stationary-orbit `S3`.

The new finding is an exact compatibility obstruction. Within the registered constant-twist
stationary family, the complete metric descends along that Hopf circle precisely when

```text
V(phi)=0,
V(h)+kappa(hR-Rh)=0,   h=P^T P.
```

These conditions allow global two-shear screens: pull back a generic smooth positive metric from
the quotient `S2`, express it in the global horizontal Maurer–Cartan pair, and choose the smooth
positive square root as `P`. But descent also makes the Hopf generator `V` a second continuous
Killing field. The old rank-three certificate, whose power came from there being exactly one
Killing direction, must then fail. Therefore the old uniquely recognizable clock stratum and the
full Hopf-metric-descent stratum do not overlap under that certificate.

## What this means—and does not mean

This is forward progress, not loss of the bridge:

- `DERIVED`: ruler alignment survives every general screen for a supplied stationary `K`.
- `DERIVED`: metric-intrinsic clock/ruler configurations persist on open neighborhoods with both
  shears.
- `DERIVED-CONDITIONAL`: the normalized ruler gives the unit Hopf connection on the chosen `S3`.
- `DERIVED`: exact full-metric descent conditions and anisotropic two-shear witnesses.
- `DERIVED NO-OVERLAP`: full descent is incompatible with the old rank-three unique-clock
  certificate.
- `OPEN`: another metric-intrinsic selector for the clock inside the resulting `(K,V)` symmetry
  plane.

It would be an overstatement to conclude that no metric-native clock selector exists. Only the
existing uniqueness method is excluded on the fiber-invariant branch. Likewise, the Hopf bundle
exists even on fiber-dependent branches; what fails there is descent of the complete metric, not
the coframe/topological bundle.

The spacetime ruler vector and orbit generator must also remain distinct:

```text
E1=exp(-phi)(V-alpha/c_E K),
pi_*E1=exp(-phi)V.
```

Thus the twist-selected spacetime direction projects to the Hopf line but is not itself a closed
Hopf orbit when the clock-ruler twist is nonzero.

## Original witnesses reclassified

The exact C01–C06 profiles retain their earlier metric-intrinsic clock/ruler status. At their north
certificate event, however, `V(phi)=3/50`, so none belongs to the fully descended stratum. Their
failure of descent was not previously part of their bounded existence claim and does not invalidate
it.

## Evidence gates

1. **Preregistered:** yes, `f362970`, before the general-screen twist, descent, and compatibility
   outcomes were computed.
2. **Full or bounded:** complete for smooth stationary `phi`, every invertible general screen `P`,
   and the registered Hopf generator inside the chosen `R x S3` coframe; not generic spacetime,
   other completions, or on-shell dynamics.
3. **Independent:** exact exterior/Hodge, dual-frame, screen Lie derivative, anisotropic descent,
   old-profile fiber derivative, rank obstruction, and causal counterexample are reconstructed by a
   no-production-import exact-rational implementation with 139 passing checks. A fresh adversarial
   review is recorded separately.
4. **Premises:** 22 rows distinguish founded, observational, chosen-control, free, working, and open
   inputs. Twenty-eight semantic/ledger mutation catches exercise the classified outputs and
   overclaim gates. They are separate from the independent exact algebraic reconstruction.

Maximum conclusion:

```text
GENERAL-P TWIST/RULER ALIGNMENT AND OPEN METRIC-INTRINSIC FULL-SCREEN NEIGHBORHOODS DERIVED;
FULL HOPF METRIC DESCENT FORCES A SECOND KILLING DIRECTION AND CANNOT USE THE OLD RANK-THREE
UNIQUE-CLOCK CERTIFICATE;
NATIVE CLOCK SELECTION INSIDE THAT SYMMETRY PLANE, CARRIER, ACTION, AND PHYSICAL BRANCH REMAIN OPEN.
```
