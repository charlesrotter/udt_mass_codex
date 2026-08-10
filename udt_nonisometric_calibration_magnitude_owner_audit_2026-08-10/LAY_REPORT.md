# Lay report — we found two partial engines

The previous audit proved that the angular gearbox can carry a dilation amount correctly but does
not create that amount. This audit asked whether any existing part of the metric is already an
engine.

Two branches contain partial engines:

- In R17, the metric already knows the amount of clock dilation and already has the reciprocal
  clock/ruler mechanism. What it has not yet told us is whether those two pieces must be connected
  in the particular way that produces the physical observer-to-observer rule.
- In R18, the metric knows the clock-side dilation but has not supplied the ruler-side response.
  The same clock behavior can therefore lead to more than one final reciprocal reading.

Every ordinary geometric transport we checked is more like a driveshaft: it carries orientation
and path history, but because it preserves lengths it cannot create dilation. A complete
observer-pair surface can produce the full reading, but the metric has not yet selected which
surface represents the physical comparison.

So we have not found the complete engine. We have learned that the remaining gap is smaller and
branch-specific. R17 is the most complete case: the amount and the mechanism are both present, but
their compulsory connection is still unproved.
