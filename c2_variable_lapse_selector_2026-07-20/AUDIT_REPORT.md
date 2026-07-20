# Conditional C2 Variable-Lapse Selector Audit

Date: 2026-07-20  
Base: `309e85fb51fd8d6562eb2ffd020ac3e5259fcdb7`  
Preregistration commit: `25a8e01`  
Mode: CPU-only exact conformal reduction, compact Bach equation, orbit matching, and independent 4D curvature  
Status: **VERIFIED-WITH-CAVEATS** — preregistered exact derivation, independently written 4D
coordinate-curvature checks, base-source replay, and 33 exercised fail-closed catches pass; no fresh
external-model review was authorized.

## Result first

Allowing the clock rate to vary with angular depth does **not** create a new regular compact solution
inside the conditional fixed-basis `C^2` family. It sharpens the earlier result into a CSN statement:

- an isolated change of the clock relative to the spatial rulers creates conformal curvature;
- the same change applied to the complete clock-and-ruler coframe is a CSN-equivalent copy of the
  round solution;
- modulo that common rescaling, the compact Bach equation still leaves the round angular geometry
  and a constant lapse.

The exact verdict is:

`CONDITIONAL_ROUND_CSN_CLASS_SURVIVES_POSITIVE_VARIABLE_LAPSE_IN_COMPACT_FIXED_BASIS_C2_FAMILY`.

This does not select an absolute clock rate, radius, `Xmax`, material action, or finite-cell boundary.
It also does not test a time/fiber shift, acceleration connection, or genuine time dependence.

## Exact reduction

The registered metric is

`g4 = epsilon_t N(eta)^2 d tau^2 + g3[H(eta),s]`,

with positive lapse `N`, positive depth shape `H`, constant positive squashing `s`, and the same
conditional reciprocal-toric capped `S3` geometry used in the parent audit.

Because `N>0`, rescale the complete metric:

`g_hat = N^-2 g4 = epsilon_t d tau^2 + N^-2 g3`.

In four dimensions, the `C^2` density and the Bach zero set have the required conformal covariance.
The variable-lapse question is therefore exactly equivalent, inside this branch, to the earlier
constant-lapse product question for the rescaled spatial metric `N^-2 g3`.

The compact product `B_00` equation forces that rescaled spatial metric to have constant sectional
curvature. Matching it to a round metric in the **same fixed reciprocal toric basis** gives:

1. the orbit cross component is proportional to `sin^2(eta)cos^2(eta)(s^2-1)`, so `s=1`;
2. the two orbit coefficients sum to one, forcing the common orbit factor to one;
3. their ratio gives the same depth coordinate, up to exchanging the two axes;
4. radial matching gives `H=1` and makes `N` constant.

Thus there is no new positive nonconstant-lapse Bach-flat branch in this compact no-shift family.

## The decisive clock-versus-common-scale check

For a round spatial metric with a depth-dependent clock factor,

`g4 = N(eta)^2 d tau^2 + g_round`,

the exact Weyl norm is

`C4^2 = 2 N^-2 |(Hess_round N)_TF|^2`.

For a torus-invariant lapse, two angular Hessian eigenvalues differ by

`-N'/(sin(eta)cos(eta))`.

So zero Weyl curvature forces `N'=0` on the connected regular interior. A changing clock **by
itself** is a genuine relative distortion between temporal and spatial metric sectors.

The independent 4D Christoffel/Riemann implementation used

`N = 1 + (1/3) sin^2(2 eta)` at `eta=pi/8`

and obtained exactly

`R=26/7`, `Ricci^2=524/49`, `Riemann^2=972/49`, `C4^2=64/21`.

By contrast, for the common complete-coframe copy

`g4 = Omega(eta)^2[d tau^2 + g_round]`,

with `Omega=exp[(1/3)sin^2(2eta)]`, the independent calculation gives

`C4^2=0`

while the individual Ricci and Riemann invariants remain nonzero. This directly distinguishes
conformal flatness from ordinary flatness and confirms that the common factor is a CSN copy rather
than an isolated clock deformation.

## Lay interpretation

Think of a local clock and local rulers as a matched measuring kit.

If only the clock is stretched while the rulers are held fixed, their ratio changes. The conditional
metric equation detects that mismatch and rejects a smoothly varying version of it in this compact
branch.

If the clock and every ruler are stretched by exactly the same local factor, none of their pre-scale
ratios changes. CSN says that is another description of the same underlying scale-free geometry.

So the result does not say “time cannot dilate.” It says that, before a physical scale is selected,
a lapse function is not an independent free field in this branch. A regular nonconstant lapse can
survive at zero Weyl cost only when the spatial coframe carries the matching factor, placing the
whole metric in the same CSN class.

## What remains genuinely open

The compact conclusion depends on a positive lapse, a smooth boundaryless capped `S3`, a static
diagonal metric, and a fixed reciprocal toric basis. The audit deliberately preserves:

- lapse zeros, poles, or causal degenerations as unclassified singular strata;
- a physical finite-cell interval, where the discarded Laplacian may become boundary flux;
- time/fiber and reciprocal time/radial shift/connection terms;
- genuine time dependence and acceleration;
- a moving angular basis, function-valued squashing, alternative caps, quotients, and topology.

Those are not small-print loopholes. In particular, a shift/connection is the first omitted
dimensionless field capable of coupling the clock sector to the angular fiber without merely
rescaling the complete coframe.

## Scale and matter ruling

No absolute size appears. The round solution still has a common CSN calibration orbit. `c` and `G`
remain observational anchors, and electron mass remains a possible downstream calibration, but none
enters or solves these dimensionless equations.

No `S2` carrier, section, soldering, `L2+L4` functional, source, or material mass was assumed or
derived. The result constrains a conditional metric branch; it is not a matter action.

## Four evidence gates

1. **Preregistered:** yes, commit `25a8e01` before derivation.
2. **Full space or bounded scope justified:** bounded positive static diagonal fixed-basis compact
   family; every named omitted branch is retained in the ledgers.
3. **Independently verified:** yes in-package, by separate 4D coordinate-curvature contractions and
   independent orbit/Hessian algebra; no fresh external-model review.
4. **Every premise audited:** yes for the declared slice; conditional `C^2`, toric realization,
   compact caps, no physical boundary, and no shift remain explicit.

The correct banked grade is therefore **VERIFIED-WITH-CAVEATS**, not a complete UDT theorem.
