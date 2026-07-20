# Direction–magnitude conceptual correction

Date: 2026-07-19

Base: `86874cb8482fc2a29bfc53251c3bcf4160eda4ed`

Status: `VERIFIED-WITH-CAVEATS`; append-only correction of physical interpretation

## Result first

Charles's objection is correct. The distance between two observers is not signed, and reversing
spatial direction cannot by itself turn clock slowing into clock speeding. The prior phrase
“physical signed position” was therefore a category error.

The exact signed quantity

`delta(P;O) = Phi(P) - Phi(O)`

survives, but only as an **ordered reciprocal comparison**. Exchanging the order negates it. That is
analogous to reversing an arrow, not acquiring a negative length.

A physical separation must instead be nonnegative. The smallest magnitude made from the ordered
comparison is `abs(delta)`, but this is only a candidate radial depth. A global observer distance
must come from the complete metric and therefore depends on radial scale, path, angular geometry,
representative, and any required slicing. This audit does not derive that global distance.

The normalized reciprocal imbalance `tanh(delta)` is correspondingly regraded as an **oriented
projective coordinate**. On a chosen one-dimensional axis its sign says which way the arrow points.
In three dimensions, magnitude and direction separate: a nonnegative radial quantity supplies “how
far,” while the angular sector supplies “which way.” The bounded expression `tanh(abs(delta))` is a
radial-display candidate, not a derived proper distance.

The clock interpretation also narrows. Two operations that had been conflated must be separated:

- reversing angular direction at fixed nonnegative depth; and
- exchanging which observer is first in an ordered comparison.

The first leaves depth and clock slowing unchanged. The second negates `delta` and exchanges the
ordered dual weights `exp(-delta)` and `exp(+delta)`; it is an inverse comparison, not a claim that
looking the other way speeds a clock up.

In the already-`CHOSE` local Lorentzian temporal slot, replacing signed comparison by nonnegative
depth gives the conditional clock factor `exp(-rho)`. It is unchanged when angular direction is
reversed and never exceeds its coincidence value. That branch survives as `CONDITIONAL`; it is not
an unconditional extraction theorem from Reciprocity and CSN alone.

Without supplying that chosen temporal slot, two distinct exact symmetric readouts,

- `sech(delta)`, and
- `sech(delta)^2`,

are smooth, Common-Scale Neutral, unchanged by pair exchange, equal to one at coincidence, and
decrease rather than speed up with increasing magnitude. Both arise from symmetric functions of the
same reciprocal pair. Thus Reciprocity, CSN, and direction-evenness alone do not select an
unconditional native scalar clock observable. These are countermodels to unrestricted uniqueness,
not proposed UDT clock laws and not countermodels to the explicitly chosen temporal-slot branch.

## Lay interpretation

An arrow can be positive or negative depending on which way it points. Its length cannot.

The previous work correctly found the algebra of the arrow: reversing the ordered comparison gives
the inverse reciprocal transformation. The mistake was calling the arrow's signed coordinate the
distance itself.

For physical geometry we need three separate readings:

1. the ordered comparison, which remembers orientation and composes algebraically;
2. the magnitude, which is never negative;
3. the angular direction, which says where the other observer lies.

The clock is a fourth object. Looking the opposite way at the same distance leaves it unchanged.
Swapping which observer is the reference is instead an inverse ordered comparison. The chosen local
Lorentzian slot already supplies one conditional slowing rule; deriving that rule without the slot
choice remains open.

## What survives unchanged

- The reciprocal CSN projective ray remains derived in its declared dual representation.
- The additive ordered comparison and its inverse/composition algebra remain exact.
- Normalized imbalance remains the unique three-anchor first-degree projective chart inside that
  mathematical class.
- The smooth chart counterfamilies remain exact, including on the nonnegative half interval.
- The additive `L dphi` seed inside the reciprocal-weighted spatial coframe remains insensitive to
  which bounded display is painted over depth.
- The finite-cell seal remains absolute `Phi(S)=0`.

None of those statements makes signed depth a physical distance or selects the scalar clock readout.

## Direction belongs to the angular sector

In one dimension, a signed coordinate can encode left versus right. In three dimensions it cannot
replace angular data. An oriented displacement has the schematic form

`nonnegative magnitude times direction`.

Angular reversal changes the direction and leaves the magnitude unchanged. Exchanging the ordered
observer pair also reverses its comparison arrow, but may invert a relational comparison; those are
not identical physical operations. The current audit does not choose
the topology, roundness, twist, transport, or global completion of that direction sector. This is
precisely why a metric-wide physical distance cannot be closed using the reciprocal radial pair
alone.

The static field's odd sign across the finite-cell seal may remain useful as doubled-cover or branch
bookkeeping. It cannot automatically mean negative distance or direction-dependent clock speed-up in
the physical quotient.

## Projective radius versus metric length

There are now two distinct radial notions:

- `L dphi` is the additive-depth seed inside the conditional spatial term
  `exp(2phi) L^2 dphi^2`; in a chosen representative, radial proper length carries the full
  reciprocal weight rather than merely `L abs(delta phi)`.
- `X_max tanh(rho)` is a bounded radial coordinate candidate.

A bounded coordinate need not equal proper length. Even if `X_max` is a universal coordinate reach,
the physical length along a path must be computed from the metric. Relating those objects requires a
separate theorem; the current foundation does not supply it.

The earlier counterfamily still matters. Smoothly changing the interior markings of the bounded
radial coordinate leaves the reciprocal coframe unchanged. Nonnegative distance therefore does not
rescue the missing projective readout selector.

## Clock scalar underdetermination

At ordered depth `delta`, the reciprocal weights are `u=exp(-delta)` and `v=exp(+delta)`. Reversing
the ordered observer comparison exchanges `u` and `v`. This does not describe angular reversal at
fixed `rho`.

Once `rho` is nonnegative, the chosen local Lorentzian temporal slot conditionally reads
`exp(-rho)`. Opposite angular directions at equal `rho` give the same result. What is not derived is
that this particular representative and slot must furnish the unconditional native measured clock
observable.

Reciprocity and CSN without that slot choice allow multiple symmetric normalized readouts. The two exact
counterexamples in this audit are distinct at `u=1/2`, `v=2`: one gives `4/5`, the other `16/25`.
Both are smooth and non-speeding as radial magnitude increases. This establishes underdetermination
of the premise-light extraction; it does not authorize either candidate or refute the chosen-slot
conditional branch.

Thus the reciprocal pair can remain fundamental without either component being naively identified
with the measured scalar clock rate.

## Seal correction

The absolute static seal remains `Phi(S)=0`. Relative to observer `O`,

- the ordered comparison is `-Phi(O)`;
- the minimal magnitude candidate is `abs(Phi(O))`; and
- the optional bounded projective magnitude is `tanh(abs(Phi(O)))`.

For a finite observer away from the seal, the seal is neither observer coincidence nor the
`X_max` endpoint. The previous algebra survives after its physical interpretation is narrowed.

## Revised open joins

The former single “projective-position join” splits into three distinct questions:

1. **Distance map:** derive nonnegative observer separation from the complete radial-angular metric.
2. **Clock map:** derive the scalar measured clock dilation from the reciprocal pair without relying
   on the chosen local Lorentzian temporal slot, or derive why that slot is selected.
3. **Radial display map:** determine whether `X_max tanh(rho)` is operational position or only a
   canonical bounded coordinate.

All three remain `OPEN`; none is adopted here.

## Evidence gates and limits

1. **Preregistered:** yes, commit `b3777f5`, before correction algebra.
2. **Full space or bounded scope:** exact orientation/magnitude algebra and explicit infinite radial
   chart family; not every global metric, path, angular completion, or clock functional.
3. **Independent verification:** separate symmetric clock counterexample, observer-swap algebra,
   direction/magnitude checks, prior-package immutability replay, and exercised semantic mutations.
4. **Premises audited:** correction overlay, status ledger, source inventory, repository gates, and
   authority boundary.

The prior package remains byte-identical. This correction retains `exp(-rho)` only conditionally in
the chosen local Lorentzian temporal slot. It does not derive a global distance, unconditional native
clock law, angular geometry, `X_max`, action, source, carrier, mass, or canon. Charles owns the
physics verdict.
