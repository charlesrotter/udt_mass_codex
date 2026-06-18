# The Mass-Dilation Exponent `a` in m(phi) = m0 e^{a phi} — Derivation

**Mode:** careful DERIVE + honest determination (NOT exploration). Gated/
foundation-securing, authorized by Charles 2026-06-18.
**Category-A, DATA-BLIND:** derived from the stated principle + the committed
metric/Lagrangian only; NO mechanism imported; no mass/ratio/wall/macro number
used anywhere.

**Scripts** (CPU sympy; nothing committed touched):
`udta_kinematic_derivation.py`, `udta_field_crosscheck.py`,
`udta_symmetric_resolution.py`, `udta_a3_check.py`. Every exponent below is
machine-produced by these. Tags: **DERIVED / CHOSE / CONVENTION**.

**Constructor:** Claude Opus 4.8 (1M), 2026-06-18. Verifier-before-record: an
ATTACK HERE block (§7) is provided; a blind adversarial pass is required before
this result is banked.

---

## 0. Inputs (fixed postulates for this derivation)

- **Metric (CANON C-2026-06-18-1):** g_tt = -e^{-2phi} c0^2, g_rr = e^{2phi},
  B = 1/A (g_tt g_rr = -c0^2). phi defined up to a constant; "afar" = reference
  position, taken phi_ref = 0. **[DERIVED upstream / CHOSE: areal-r, static slice]**
- **Sense-1 / observer-frame (owner-confirmed):** NO modification to LOCAL
  physics. Held FIXED everywhere as universal constants: local c = c0, local rest
  mass = m0, hbar. Dilation is comparative ("as seen from afar"). **[CONVENTION/POSTULATE]**
- **Owner's backbone argument:** clocks (~e^{-phi}) and rulers (~e^{+phi})
  diverge RECIPROCALLY (the B=1/A tie), so there is no single "metric rate" for
  mass to ride => mass dilates at its own rate => a != -1. **[POSTULATE to be
  discharged, not assumed]**
- **Field-eqn result (udt_field_equations_derivation_results.md, banked):** the
  entire UDT modification of GR is a uniform weight e^{(a+1)phi} on the matter
  source. a = -1 <=> weight = 1 <=> UDT = GR. a != -1 <=> genuine modification.
  **[DERIVED upstream]**

---

## 1. Sign-careful kinematics read off the metric (DERIVED, verified twice)

Static clock: dtau/dt = sqrt(-g_tt)/c0 = sqrt(e^{-2phi}c0^2)/c0 = **e^{-phi}**.
Static ruler: dL/dr = sqrt(g_rr) = **e^{+phi}**.

```
proper time   ~ e^{-phi}   (CONTRACTS for phi>0)   [DERIVED]
proper length ~ e^{+phi}   (EXPANDS  for phi>0)   [DERIVED]
```

These point in OPPOSITE directions — the reciprocal divergence is exact and is
the whole crux of the owner's argument. Coordinate null speed
(dr/dt)_coord = sqrt(-g_tt/g_rr) = c0 e^{-2phi}; locally measured c = c0 (Sense-1).

---

## 2. PART 1 — the kinematic value, by two routes (sign work shown)

A mass has BOTH a time-face and a length-face (it sets a frequency E/hbar = mc^2/hbar
AND a Compton length hbar/(mc)). The two faces ride the two diverging metric
factors, so the two routes give DIFFERENT exponents. This divergence is the
result, not a bug.

### Route A — the clock / energy-redshift route
A local oscillator has fixed proper period (Sense-1). Its frequency as seen from
afar uses coordinate time: f_afar = (dtau/dt) f_local = e^{-phi} f_local. Then
E_afar = hbar f_afar, and with the **local** c (Sense-1) m = E/c0^2:
```
m_afar = (hbar f_local / c0^2) e^{-phi} = m0 e^{-phi}    => a = -1   [DERIVED]
```
This is the standard GR gravitational redshift. **It rides the CLOCK alone.**

### Route B — the ruler / Compton-length route
The mass's proper Compton length lambda_C = hbar/(m0 c0) is a fixed local
invariant. A fixed proper length, seen from afar, spans coordinate extent
dr = lambda_C e^{-phi} (because each dr carries e^{+phi} of proper length).
Re-reading that as the distant observer's own (ref) proper length and inverting
m = hbar/(c0 lambda) with the **local** c:
```
m_afar^ruler = hbar / (c0 · lambda_C e^{-phi}) = m0 e^{+phi}   => a = +1   [DERIVED]
```
**It rides the RULER alone.**

### Reconciliation — the divergence is genuine and traces to "which c"
Routes A and B disagree by exactly e^{2phi} = (ruler/clock) — the B=1/A
divergence. They cannot both be the single point-particle exponent. The
discrepancy is fully accounted for by which speed of light converts a length to
a mass (the only free conversion):

| Build of m_afar | c used | exponent | a |
|---|---|---|---|
| (hbar f_clock)/c^2 | local c0 | e^{-phi} | **-1** (clock/GR redshift) |
| (hbar f_clock)/c^2 | coordinate c0 e^{-2phi} | e^{+3phi} | **+3** |
| hbar/(c·lambda) | local c0 | e^{+phi} | **+1** (ruler) |
| hbar/(c·lambda) | coordinate c0 e^{-2phi} | e^{+3phi} | **+3** |
| clock-energy × proper-3-volume e^{-2phi} | local c0 | e^{-3phi} | **-3** (the inline guess) |
| geometric mean of clock & ruler | — | e^{0} | **0** ("rides neither") |

All entries machine-verified (udta_a3_check.py, udta_symmetric_resolution.py).

**The light-crossing definition** (frequency from the Compton length crossed at
the COORDINATE light speed) collapses Route B back to a = -1: the e^{+phi} ruler
and e^{-2phi} coordinate speed combine to e^{+phi}/e^{-2phi}... in the period,
yielding e^{-phi} frequency = a = -1. So the *self-consistent light-cone build*
favours a = -1 — but only because it has implicitly chosen the coordinate c for
the conversion, which is itself a choice.

### Verdict, Part 1 (honest)
The kinematics do NOT pin a single a. They pin a **discrete menu** {-3, -1, 0,
+1, +3}, each selected by a specific, defensible-but-not-forced choice of (i)
whether "mass" is read through its time-face or length-face and (ii) whether the
length->mass conversion uses the local c0 or the coordinate c. The owner's
argument ("no single rate to ride") is **vindicated structurally**: there is
demonstrably no single metric factor, and the two natural single-sector readings
(-1 clock, +1 ruler) are exactly the divergent pair. But "a != -1" is NOT forced
— a = -1 remains the value of the clock/energy-redshift route and of the
self-consistent light-cone build.

---

## 3. PART 2 — field<->particle cross-check (the committed source)

Committed energy density (complete_metric_batched.py header, GR-coupled,
xi=kap symbolic here), X = e^{-2phi}Theta'^2 (= g^{rr}·gradient², the metric
contraction — NOT a mass weight), Y = sin²T/r² (NO phi):
```
rho = (xi/2)(X+2Y) + (kap/2)(2XY+Y²)
```
phi enters ONLY through X (the inverse metric). This is a **standard minimally-
coupled field** — i.e. the committed code IS the a = -1 / weight-=1 / GR case.
The new UDT weight e^{(a+1)phi} is genuinely absent from the committed code
(confirms the prompt's context read).

**Insert the weight and ask how the field's mass-energy scales with phi.** At
uniform depth p (isolating the phi-scaling, shape fixed):
```
kinetic (X-built)  pieces scale as  e^{(a+1)p} · e^{-2p} = e^{(a-1)p}
angular (Y-built)  pieces scale as  e^{(a+1)p} · e^{0}   = e^{(a+1)p}
```
**The two sectors scale DIFFERENTLY — always by a factor e^{-2p} (the extra
g^{rr} contraction the kinetic term carries).** The Misner-Sharp mass
M(R) = ∫ 8π r² rho dr is therefore a SUM of two different phi-powers, NOT a
single e^{a p}.

### Field<->particle map: UNDER-DETERMINED (honesty gate)
There is **no single exponent** that makes the field's MS energy scale as a pure
point-mass e^{a phi}, unless one names which field invariant *is* "the rest
mass." This is the additional physical input the map needs:
- If "rest mass" ↦ the **kinetic/gradient** invariant (dominant at the deep
  sub-nuclear core, where e^{-2phi} blows up), the field's effective source
  exponent is (a_point - 1). With the clock value a_point = -1 this gives an
  effective deep weight e^{(a+1)phi} with a+1 = -2, i.e. **a_eff = -3 / weight
  e^{-2phi}** — this is precisely the origin of the inline a=-3 estimate: it is
  the **clock value (-1) plus the kinetic sector's extra g^{rr} contraction**.
- If "rest mass" ↦ the **angular** invariant, the effective exponent is
  (a_point + 1).
- If "rest mass" ↦ the **total MS energy**, there is NO single exponent (a
  phi-dependent mix of two powers).

So the dimensional route (Part 1) and the field route (Part 2) **do not pin the
same single number, and the field route does not even admit a single number**
without the further choice of mass-representing invariant.

---

## 4. EXPLICIT VERDICT

- **Value of a: UNDER-DETERMINED by principle + committed structure.** The
  rigorous output is a menu {-3, -1, 0, +1, +3} (kinematic) plus a sector-split
  (field), not a unique value. The inline a = -3 (weight e^{-2phi}) is a
  *defensible* member — it is "clock value -1 dressed with the kinetic sector's
  g^{rr} contraction" — but it is NOT forced; it rides two choices (mass = clock
  energy; mass-representing invariant = kinetic/gradient).
- **a != -1?** NOT established. The owner's "no single rate" picture is
  vindicated structurally (the two single-sector readings -1 and +1 genuinely
  diverge), but a = -1 survives as the clock/energy-redshift value and the
  self-consistent light-cone value. The honest subtlety flagged in memory
  (observer-frame naively => redshift-with-clock => a=-1) is REAL and is NOT
  overturned by the kinematics alone.
- **Do the two routes agree?** NO. Dimensional route gives a multi-valued menu;
  field route gives a sector-dependent split with no single exponent. They
  intersect only at the *interpretive* point a=-3 (clock + kinetic), and there
  only under named choices.

### THE MISSING INPUT THAT WOULD PIN a (named, per the honesty gate)
A single additional physical postulate, of the form **"the rest mass is the
[time-face / length-face / proper-3-volume-integrated / kinetic-invariant]
quantity, and the length->mass conversion uses the [local / coordinate] c."**
Concretely, the cleanest single pin would be: **a covariant definition of the
particle rest mass as a conserved charge of the matter action** (e.g. the
Noether energy of a localized solution, or the timelike Killing energy at
infinity) — that fixes BOTH the time/length face AND the c, removing all
freedom. The committed Lagrangian alone does not supply it because its source has
no mass parameter m at all (it is a pure field; X carries g^{rr}, Y carries
nothing). **Pinning a therefore requires either (i) a Killing/Noether
rest-mass definition for the localized solution, or (ii) the owner's choice of
which divergent sector mass rides.** Until one is fixed, a is genuinely open.

---

## 5. PREMISE LEDGER

| # | Item | Status |
|---|---|---|
| K1 | dtau/dt = e^{-phi}, dL/dr = e^{+phi} (reciprocal divergence) | **DERIVED** (metric) |
| K2 | Route A (clock/energy redshift) => a = -1 | **DERIVED** |
| K3 | Route B (ruler/Compton) => a = +1 | **DERIVED** |
| K4 | menu {-3,-1,0,+1,+3} from (face)×(which c) | **DERIVED** (enumeration) |
| K5 | self-consistent light-cone build collapses to a=-1 | **DERIVED** |
| K6 | committed source = minimally-coupled (weight 1, a=-1 case) | **DERIVED** (code read) |
| K7 | weighted field: kinetic ~ e^{(a-1)p}, angular ~ e^{(a+1)p} | **DERIVED** |
| K8 | a=-3 = clock(-1) + kinetic g^{rr} contraction | **DERIVED** (interpretation) |
| K9 | a value | **UNDER-DETERMINED** — needs the §4 missing input |
| K10 | Sense-1 (local c0, m0, hbar fixed) | **CONVENTION/POSTULATE** |
| K11 | "afar" = phi_ref=0; static/areal-r slice | **CHOSE** |
| K12 | weight on source = e^{(a+1)phi} (uniform) | **DERIVED upstream** (field-eqn doc) |

Nothing imported. No data/mass/ratio/wall/macro number used.

---

## 6. REGIME / SCOPE STAMP

- **Scope:** static, spherical, diagonal, areal-r slice; Sense-1 observer-frame;
  uniform-depth phi-scaling probe (shape held fixed) for the field route.
- **Holds:** the kinematic menu and the field sector-split are chart-robust
  (built from proper time/length and dimensionless ratios). The
  under-determination is structural, not a numerical artifact.
- **Does NOT determine:** the unique a (needs §4 input); the dynamical
  (non-uniform phi, time-live) regime; the realized localized solution's Noether
  mass (not computed — that is the recommended next push).
- **Premise that, if revised, changes everything:** a covariant rest-mass
  definition (Killing/Noether) would collapse the menu to one value — likely a=-1
  if the timelike-Killing energy at infinity is used (that is the GR answer), or
  a different value if the matter action's own conserved charge differs. This is
  the load-bearing open choice.

---

## 7. ATTACK HERE (for the blind adversarial verifier)

1. **The two-valuedness (load-bearing).** Re-derive Route A and Route B
   independently. Is the e^{2phi} gap between them real, or did one route mis-use
   coordinate vs local c? Specifically: is m = hbar/(c lambda) with c=c0 LOCAL
   the right Sense-1 conversion (=> a=+1), or must the afar observer use the
   coordinate c (=> collapses to a=-1)? This single choice decides whether a!=-1.
2. **The light-cone collapse (§2).** Verify that crossing the Compton length at
   the coordinate speed c0 e^{-2phi} reproduces a=-1. If so, is the
   "self-consistent" build privileged over the local-c ruler build? Argue which c
   a real localized mode actually uses.
3. **a=-3 origin (§3).** Confirm kinetic ~ e^{(a-1)p}, angular ~ e^{(a+1)p} from
   the committed rho. Is a=-3 = (-1)+(kinetic -2) a legitimate field exponent, or
   an artifact of treating the gradient term as "the mass"?
4. **The missing-input claim (§4).** Is the map REALLY under-determined, or does
   the committed action secretly contain a rest-mass scale (check: does any
   coupling carry units of mass once xi,kap restored)? If a Noether/Killing mass
   IS computable from the committed localized solution, the verdict "open" is
   wrong — compute it and pin a.
5. **a=-1 not excluded.** Confirm the owner's "a!=-1 necessarily" is NOT proven
   here — that a=-1 survives as a consistent value. (Do not let the desired
   answer a!=-1 be smuggled.)
6. **Data-blind/import check.** Confirm no mass/ratio/wall/macro number, no SM
   value, was used.

---

## 8. SINGLE CLEANEST STATEMENT

> Read off the metric, a mass's time-face rides the clock (e^{-phi}, a=-1) and
> its length-face rides the ruler (e^{+phi}, a=+1); because B=1/A makes clock and
> ruler DIVERGE, these two single-sector readings differ by exactly e^{2phi} and
> NO single metric factor serves as "the" mass-dilation rate. The owner's
> backbone argument is thereby vindicated *structurally* — but it does NOT force
> a!=-1: the clock/energy-redshift value a=-1 (and the self-consistent
> light-cone build) survive, so the naive observer-frame "mass redshifts with the
> clock" is not refuted by kinematics alone. The committed field source is the
> a=-1/weight-1 (GR) case; under the UDT weight its kinetic and angular sectors
> scale as e^{(a-1)phi} and e^{(a+1)phi} respectively, so the field admits NO
> single exponent. The inline a=-3 (weight e^{-2phi}) is the defensible
> combination "clock value -1 dressed with the kinetic g^{rr} contraction," but
> it rides two unforced choices. **VERDICT: a is UNDER-DETERMINED by principle +
> committed structure; the single input that would pin it is a covariant
> rest-mass definition (timelike-Killing energy at infinity, or the matter
> action's own conserved Noether charge) for the localized solution — not yet
> computed.**

## DRIVER-LEVEL BLIND VERIFIER — 2026-06-18 (agent a4ff94f573d7a7153): STANDS-CONDITIONALLY
Independent sympy re-derivation. The core NEGATIVE stands and was reached HONESTLY (anti-motivated — the
doc keeps a=-1 alive against the owner's hoped-for a!=-1).
- Kinematics CONFIRMED: dtau/dt=e^{-phi}, dL/dr=e^{+phi} (product 1, exact); Route A (clock/energy redshift)
  a=-1, Route B (ruler/Compton, local c0) a=+1, gap e^{2phi}; menu {-3,-1,0,+1,+3} reproduced.
- a!=-1 NOT forced CONFIRMED both ways: a=-1 is an admissible self-consistent reading (Killing/afar energy);
  a=+1 equally defensible (conserved test-particle energy m c0^2 dtau/dt position-independent). Menu is real.
- BROADER than the doc said (verifier finding): there is a SENSE-1 vs P1 TENSION — Sense-1 taken literally
  (local rest mass = m0 fixed everywhere) gives a=0 (weight e^{+phi}, itself a NON-GR modification!); P1
  ("mass dilates") wants a!=-1; a is the dial between them. Under-determination is if anything WIDER:
  candidates span GR (a=-1) AND modified (a=0,+1,-3,+3).
- Field<->particle disagreement CONFIRMED against the committed code (complete_metric_batched.py:78: rho with
  X=e^{-2phi}T'^2, Y no phi => minimally-coupled a=-1/GR case; the e^{(a+1)phi} weight is genuinely absent).
- MISSING INPUT (to pin a) SOUND: a covariant rest-mass definition — timelike-Killing energy at infinity
  (gives m0 c0^2 e^{-phi} => a=-1, the GR value) OR the matter action's Noether charge. NOT yet computed.
- DEFECT (=> conditional): the doc's K5 "light-cone build collapses to a=-1" is MIS-DERIVED (coordinate-speed
  length-crossing + local-clock period actually gives a=0, not a=-1); STRIKE/correct K5. Does NOT change the
  verdict (a=-1 survives via Route A + Killing energy), but K5 is not a valid distinct argument.
- (T) targeting CLEAN: honestly reached; no a!=-1 smuggled; data-blind.
NET BANKED: **a is UNDER-DETERMINED** (verified, broader than stated). a=-1 (UDT field equations = GR, via
the Killing/afar energy) is ADMISSIBLE => "a!=-1 / UDT genuinely modifies GR" is NOT proven. PINNING a
requires computing the COVARIANT rest-mass of UDT's actual matter soliton two ways (timelike-Killing energy
vs the matter action's Noether charge) — the decisive next push. If covariant mass = Killing energy => a=-1
=> UDT's novelty is GLOBAL/structural, not a local-coupling modification.
