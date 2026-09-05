# G352 R1 preregistration sign repair

Date: 2026-09-05
Status: outcome-unseen repair to the frozen G352 preregistration

## Defect

`PREREGISTRATION.md` defines the supplied phase covector by `k_a=grad_a(Theta)` and uses the
repository convention

```text
omega=-u^a k_a>0.
```

It then incorrectly writes `omega=dTheta/dtau`. With signature `(-,+,+,+)` and a future-directed
null `k^a`, the definitions instead give

```text
dTheta/dtau=u^a grad_a(Theta)=u^a k_a=-omega.
```

## Registered repair

Every occurrence of the physical crossing rate in the G352 derivation and executable evidence will
use its positive orientation-independent magnitude:

```text
crossing_rate=abs(dTheta/dtau)/DeltaTheta=omega/DeltaTheta.
```

Equivalently one could reverse the phase orientation and use `-Theta`; no metric, observer,
frequency ratio, area ratio, conservation premise, or physical conclusion changes. The frozen
preregistration files remain byte-unchanged and their hashes remain authoritative.

## Scope

This repair is committed before any G352 derivation or outcome program is created or run. It may
repair only the phase-orientation sign. It may not change the adopted premise, choose a different
observer weight, add light/energy physics, or widen the maximum conclusion.
