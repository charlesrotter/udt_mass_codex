# Lay report

## What was corrected

We had started treating `Xmax` as though we first had to decide which ruler
defines it. That reverses your idea.

In your framing, `Xmax` is defined by the event: it is the universal
distance limit where clock flow fades toward zero and dilation becomes
unbounded. Different rulers can assign different intermediate numbers on
the way there, but they do not define the finish line.

## What the repository already contained

The metric says that the clock factor is tied to `phi`. An already accepted
geometrical argument, called WR-L, then says how that clock factor changes
with position:

```text
fraction of the way to Xmax = 1 - the lapse coefficient.
```

In less compressed language:

- here, the clock factor is normal;
- moving deeper, the remaining fraction of room and the lapse coefficient
  fall together;
- the actual static clock rate is the square root of that coefficient, so
  it also slows toward zero;
- at `Xmax`, the remaining room, lapse, and static clock rate have all
  fallen toward zero;
- reaching the final point would require infinite optical/clock depth.

That is a real derivation inside the recorded static metric branch. It uses
the reciprocal metric plus the accepted rules that the wall has finite
proper room, infinite optical depth, and no curvature blow-up. So it is
stronger than a guessed curve, though it is not a theorem from the bare
metric line alone.

## Why the supernova work matters

The supernova analysis did not invent that curve. It tested several curves.
The same profile selected by WR-L was the one called the “linear ceiling,”
and it lay close to the Pantheon supernova data. The competing hyperbolic
`tanh` profile missed badly.

So two independent paths point to the same profile:

1. the metric plus WR-L geometry derives it; and
2. the supernova observations favor its resulting distance–redshift shape.

That is meaningful agreement. It is stronger than fitting a curve and then
calling the fit a law.

## What remains genuinely open

We know the shape of the approach to the limit on this branch. We do not
yet know why the complete universe must choose this entire branch, or what
number `Xmax` has in metres.

We also have only the clock half of the proposed clock-and-mass asymptote.
UDT still lacks the native mass definition needed to derive the mass
increase rather than borrowing a GR mass readout.

The clean current picture is therefore:

```text
meaning of Xmax: fixed as a working UDT postulate
clock asymptote: directly realized by the WR-L metric branch
exact position/clock profile: derived under the WR-L premises
supernova shape: independently supportive
global universe selection: open
numerical Xmax: open
native mass asymptote: open
```
