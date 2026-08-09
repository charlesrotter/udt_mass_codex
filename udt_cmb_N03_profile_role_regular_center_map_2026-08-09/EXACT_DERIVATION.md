# Exact N03 profile-role and regular-center derivation

## 1. Source extraction and role separation

The frozen current evidence contains a two-point comparison identity

```text
lambda_t(p,q)=exp[-2 Delta phi(p,q)],
c_eff(q)/c_eff(p)=lambda_t(p,q),
```

plus two explicitly narrower readouts: the point form of `c_eff(r)` after choosing a reference
observer, and the complete-arrow timelike-strain extractor on its regular stratum. The reference
readout is not the invariant pair object. The strain extractor is not automatically the unique
physical compositional depth. `SOURCE_CANDIDATE_CROSSWALK.tsv` keeps these distinctions visible.

The data-conditioned P1 separation profile also lives on ordered observer pairs. `X_max` is the
working limit of nonnegative pair separation at divergent comparison depth. The conditional C1
metric instead contains local coefficient functions `A(r)` and `h(r)` in a chosen centered areal
chart. Identifying pair separation with areal radius and copying P1 into the local lapse is an
additional role join; no frozen source derives it.

The audit maps eight mapped source-level families through 75 source-member crosswalk rows. This is
a rule-bound crosswalk of the explicit objects and registered members in the 16 frozen sources,
not a claim of semantic exhaustiveness over every possible interpretation of their prose.

## 2. Complete regular-center jets

For the conditional axial C1 envelope,

```text
ds^2=-A(r)dt^2+dr^2/A(r)+r^2[dtheta^2+sin^2(theta)dpsi^2]
     +2h(r)sin^2(theta)dt dpsi,
```

write

```text
A=1+a1 r+a2 r^2+a3 r^3+a4 r^4+...,
h=k0 r^2+k1 r^3+k2 r^4+....
```

The spatial block in Cartesian coordinates is

```text
g_ij=delta_ij+[(1/A)-1] x_i x_j/r^2.
```

The coefficient `[(1/A)-1]/r^2` begins with `-a1/r`; after setting `a1=0`, its next odd
radial term contains `-a3 r`. Smooth radial Cartesian coefficients have even expansions. The same
condition follows from the local scalar `g_tt=-A`. Hence

```text
A=1+a2 r^2+a4 r^4+....                              (1)
```

For the mixing one-form,

```text
sin^2(theta)dpsi=(-y dx+x dy)/r^2,
```

so smoothness requires `h/r^2` to be a smooth even radial function:

```text
h=r^2(k0+k2 r^2+...).                               (2)
```

Equation (2) is stronger than the N02 necessary condition `h=O(r^2)`. Within the conditional C1
realization in which `h` represents mixing, it is compatible with the mu-on premise. It does not
require `k0` to be nonzero, and it does not make `k0` a selected invariant, rotation observable,
or physical mu profile. Mixing may begin at higher order or away from the center.

The N01 distortion variable obeys

```text
B=h^2/(A r^2)=k0^2 r^2+(2k0 k2-a2 k0^2)r^4+... .   (3)
```

Thus the complete angular matrices return to their round value at the exact regular center while
the full mixing channel and angular coupling may turn on away from the center.

For a general smooth point-center, the statement

```text
q_AB=sphere_AB+r^2 q2_AB+....                       (4)
```

is a geodesic-polar or orthonormal-center statement about the leading small-sphere geometry. It is
not a universal component formula in every centered chart, nor is arbitrary `q2_AB` by itself a
sufficiency theorem. General screen shape and the shift-divergence term remain active beyond the
leading collapse. A completion with no collapsing orbit or preferred center is a separate,
unselected branch.

## 3. Source-derived profile and screen counts

The verifier reconstructs the registered multiplicities directly from frozen evidence:

- 3 round P1 strata;
- 21 corrected mixed `(n,q)` strata representing 210 nonzero-mixing profiles;
- 3 corrected `q=0` strata representing exactly 30 of those profiles;
- 21 RA1 literal near-wall lineage strata;
- the complete-screen aggregate `C01` through `C18`, exactly 18 members.

All three round P1 controls have `A'(0)=-n/R_w`, so they fail (1) if promoted to a centered local
lapse. Their pair/SNe role is unchanged. All 210 corrected mixed controls retain that `A` failure.
Moreover, `h/r^2=hbar(1-r/R_w)^q` has opposing Cartesian directional derivatives unless `q=0`;
only the source-derived 30-member `q=0` subset passes the full even mixing-jet test. None becomes a
complete witness because `A` still fails.

RA1 contains a genuine fork which must not be collapsed. Its literal near-wall family has
`h(0)!=0` and fails the collapsing-orbit order. Its P-RA1-8 SS3-regular completion requires improved
center behavior but supplies no explicit full-even center-to-wall profile. The endpoint-local RA1
classification survives; neither fork supplies the missing global profile.

The general C1 envelope has a nonempty regular local jet subspace (1)-(3), but no global profile,
`X_max` realization, physical screen, or boundary. The C01-C18 general-screen atlas is architecture,
including the full shift-divergence term, not a selected profile.

Within the frozen 16-source and declared conditional C1/general-screen envelopes, no mapped source
supplies a role-correct complete global profile.

## 4. The exact open mathematical home

P1 has a nonzero one-sided slope as a function of nonnegative pair separation. A smooth isotropic
local coefficient at a centered point cannot have that same linear `|x|` term: its Cartesian left
and right directional derivatives disagree. Therefore the identity join

```text
pair separation s = centered areal radius r,
pair comparison profile = local lapse A(r)
```

is excluded only in the declared smooth centered C1 branch. This is not a no-go for a no-center
topology, another local metric realization, or a nonidentity geometry-to-pair map.

Phi+orchestra derives the structural home of an exact signed compositional depth: a real cocycle on
the observer/path comparison groupoid. It does not select the physical cocycle. A one-form or
infinitesimal transport representation is conditional on an additional local first-order linear path-generator premise.
A transport/connection realization is therefore only a candidate subclass, not something N03
derives from general cocycle regularity. Angular screen, shift, and mixing data may enter the
physical cocycle, but their exact map remains open.

## 5. Global branch map

`ROLE_JOIN_BRANCHES.tsv` retains four unselected possibilities:

1. the pair-space relation, with the complete-geometry-to-physical-cocycle map open;
2. a smooth centered complete metric, with only local jets known;
3. a no-center global completion, with topology and physical cocycle open;
4. a chart-endpoint or horizon representation of the relational asymptote, which is not thereby a
   material or variational boundary.

No branch is selected and none supplies an eigensystem.

## Landing

```text
WITHIN THE FROZEN 16-SOURCE AND DECLARED CONDITIONAL C1/GENERAL-SCREEN ENVELOPES,
NO MAPPED SOURCE SUPPLIES A ROLE-CORRECT COMPLETE GLOBAL PROFILE;
THE SMOOTH CENTERED C1 LOCAL JET SPACE IS NONEMPTY AND COMPATIBLE WITH NONZERO
MIXING IN THE CONDITIONAL h-REALIZATION;
P1'S DIRECT IDENTITY PROMOTION TO THAT CENTERED LOCAL LAPSE IS EXCLUDED,
WHILE ITS OBSERVER-PAIR ROLE SURVIVES;
THE PHYSICAL GEOMETRY-TO-PAIR GROUPOID COCYCLE REMAINS OPEN,
WITH INFINITESIMAL TRANSPORT ONLY A CONDITIONAL CANDIDATE ROUTE.
```

No profile, boundary, action, probe, spectrum, source weight, population, polarization channel,
CMB fit, FD2 restart, or GPU work is selected.
