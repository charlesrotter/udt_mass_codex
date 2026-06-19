# The MATTER-SOURCE Side of UDT's Field Equation — MAP + OBSERVE

**Agent:** Claude Opus 4.8 (1M), driver-delegated | **Date:** 2026-06-18
**MODE: MAP + OBSERVE.** Make the premises VISIBLE, report WHAT IS THERE with
premises attached. **NO particle mass/ratio derived (DERIVE is gated on Charles).
NO verdict targeted.** Anti-smuggling is the whole point. **NOT canon. Do not
commit.**

**Hard constraints honored (Charles, this session):** no imported matter OBJECT
(no soliton/Skyrme/area-form construction — that is consequence-stage); no
cosmological constant; no fitted mu^2 / mu^2=pi/3; the action is treated as
DOWNSTREAM, not assumed.

**This MAP builds ON (does not redo) three banked-this-session results:**
- `udt_field_equation_running_rate_results.md` (constructor) + `running_rate_verifier_results.md` (blind verifier, CONFIRMED): a SCALAR source-weight kappa(phi) alone is ABSORBABLE.
- `udt_field_equations_derivation_results.md`: the candidate departure = a source weight `e^{(a+1)phi}`; non-absorbability lives in a dimensionless ruler ratio.
- `udt_a_exponent_derivation_results.md` (+ its blind verifier, STANDS-CONDITIONALLY): the exponent `a` is UNDER-DETERMINED; a=-1 (GR) admissible.

---

## 0. ORIENTATION — the stage and what is settled

Stage: **METRIC (done)** -> **FIELD EQUATION [vacuum half done this session;
SOURCE half = this MAP]** -> consequences (later, gated).

VACUUM half settled this session (three independent confirmations on record):
empty space => exactly Schwarzschild => UDT vacuum = GR vacuum. The
running-rate doc verified the LEFT side carries no e^{8phi}, no Brans-Dicke
(g box - nabla nabla)f terms, and the Schwarzschild profile zeroes all four
mixed Einstein components. So the departure — if any — is NOT in vacuum/curvature;
it is in **how present mass-energy sources phi.** That is this MAP.

---

## 1. THE SOURCE LAW — stated, with the depth-weight explicit

Metric (CANON C-2026-06-18-1; static/spherical/diagonal/areal-r = CHOSEN slice):
```
ds^2 = -e^{-2phi} c0^2 dt^2 + e^{2phi} dr^2 + r^2 dOmega^2 ,  c(phi)=c0 e^{-2phi}
```

**The source law (the matter half of UDT's field equation):**
```
        G_munu  =  kappa0 · e^{(a+1)phi} · T_munu        [UDT]
        kappa0  =  8 pi G / c0^4   (CONSTANT)
```
- G_munu on the left = the STANDARD Einstein tensor of the UDT metric (vacuum half settled; no curvature-side modification).
- `T_munu` = a GENERIC mass-energy source (NO object imported).
- **`e^{(a+1)phi}` = the entire candidate UDT modification of GR's source side.** It is a 0th-order-in-derivatives, depth-dependent multiplicative weight. NOT a kinetic / mu^2 screening term (none inserted, none appears).
- `a` = the matter's own **mass-dilation exponent**: m(phi) = m0 e^{a phi}.

**Reading:** at phi~0 (lab/solar) the weight = 1 => GR. It departs only where
|phi| is large (cosmic boundary + sub-nuclear core) — matching the Sense-1
observer-frame picture (no local-physics modification; departure only at the
extremes).

**Equivalent "running-coupling" packaging** (same physics, relocated): write the
weight as a varying coupling on a bare T, `kappa(phi)=8 pi G/c(phi)^4 = kappa0
e^{8phi}`. The exponent 8 = (power 4 on c) x (rate 2 in c=c0 e^{-2phi}). NB the
"8" packaging and the "a+1" packaging are NOT the same number and NOT the same
claim — see §2/§5.

### The conservation / EXCHANGE law (attached, DERIVED via Bianchi)
Because the LEFT side is the standard Einstein tensor, contracted Bianchi
(`nabla_mu G^{mu nu}=0` identically) FORCES the source's conservation law:
```
   nabla_mu T^{mu nu}  =  -(d ln[weight]/dphi) (partial^mu phi) T^{mu nu}
   = -(a+1)(partial^mu phi) T^{mu nu}        [for the e^{(a+1)phi} packaging]
   = -8     (partial^mu phi) T^{mu nu}        [for the e^{8phi} packaging]
```
**The source is NOT ordinarily conserved: mass-energy EXCHANGES with the dilation
field along phi-gradients.** This IS "mass dilates with position," geometrically
MANDATED (not posited) by the metric's own consistency. Chart form (static
diagonal T = diag(-rho, p_r, p_t, p_t)), the modified hydrostatic relation:
```
   p_r' + (rho+p_r)phi' + (2/r)(p_r - p_t)  =  -(a+1) phi' p_r       [UDT]
   [ GR same LHS = 0 ]                                                [GR]
```

---

## 2. WHERE A NON-ABSORBABLE FINGERPRINT ENTERS — the exact dimensionless ratio

**The make-or-break, already settled this session and blind-verified:** a SCALAR
weight on the source, with the standard Einstein tensor on the left, is
ABSORBABLE. Proof (Bianchi tautology, robust to arbitrary/anisotropic/
time-dependent T): define `T~_munu := e^{(a+1)phi} T_munu`; then
`G = kappa0 T~`, and `nabla^mu T~_munu = 0` IDENTICALLY (G/kappa0 is conserved by
Bianchi for ANY source). So the weight, BY ITSELF, relabels back to ordinary GR
with a constant coupling and a conserved source. **The exponent (whether 8 or
a+1) does NOT survive as a physical fingerprint of a scalar weight.** The blind
verifier could not build ANY curvature/geodesic/tidal invariant that
distinguishes "bare-T physical" from "T~ physical" — confirmed for every exponent.

So the physical departure is NOT carried by the weight's exponent. It is carried
by ONE dimensionless ratio that units/coordinates/relabelings cannot move:

> **The fingerprint = (a MATTER-built ruler) / (a METRIC-built ruler).**
> Matter ruler = the Compton length lambda_C = hbar/(m c0), with m ~ e^{-a phi} (so lambda_C ~ e^{+a phi} in proper terms; convention-dependent sign).
> Metric ruler = proper radial length, e^{+phi} dr.
>
> **Ratio  ~  e^{-(a+1) phi}**   (corpus form, `udt_field_equations_derivation_results.md` §2b; the running-rate doc writes the same object as `e^{(a-1)phi}` in its sign convention — same content, see that doc line 108.)

**The exact in-step vs out-of-step condition (this is the whole departure):**
```
   a = -1   <=>  weight e^{(a+1)phi} = 1  <=>  ratio e^{-(a+1)phi} = const
            <=>  matter ruler runs IN STEP with the metric ruler
            <=>  UDT = GR locally (novelty only GLOBAL/structural)

   a != -1  <=>  weight runs with depth  <=>  ratio runs with depth
            <=>  matter ruler runs OUT OF STEP with the metric ruler
            <=>  UDT GENUINELY DIFFERS from GR in the matter source
```
**`a` is the sole carrier of a non-absorbable fingerprint.** The "8" of the
running-coupling packaging is the absorbable varying-c^4 number; it is NOT the
physical steepness. This is the single most important structural fact of the
source side: *the entire UDT-vs-GR question on the matter side is the single
number `a+1` — is it zero or not.*

---

## 3. CANDIDATE READINGS of "mass tied to time" — DERIVED menu, none forced

Charles's principle input: "time is the PRIMARY function of the dilation
(redshifts, 1+z=e^phi); MASS seems tied to that; it's POSSIBLE they diverge."
Reading this off the metric directly (DERIVED, verified twice in the a-doc):
```
   proper time   dtau/dt = e^{-phi}   (CONTRACTS for phi>0)    [the CLOCK]
   proper length dL/dr   = e^{+phi}   (EXPANDS  for phi>0)    [the RULER]
   product = 1 exactly (the B=1/A reciprocal divergence)
```
**The crux of Charles's backbone argument is STRUCTURALLY VINDICATED:** clock and
ruler diverge in OPPOSITE directions, so there is NO single "metric rate" for
mass to ride. A mass has BOTH a time-face (frequency E/hbar = mc^2/hbar) and a
length-face (Compton length hbar/mc); the two faces ride the two diverging
factors.

**The candidate readings and what each does to the source weight** (each tagged
chose/derived; all machine-verified in the a-doc):

| Reading of "the mass" | rides | exponent a | weight e^{(a+1)phi} | UDT vs GR | chose/derived |
|---|---|---|---|---|---|
| time-face / clock / energy-redshift (local c0) | clock e^{-phi} | **-1** | 1 | = GR | DERIVED value; choice of "mass=clock energy" CHOSE |
| length-face / Compton ruler (local c0) | ruler e^{+phi} | **+1** | e^{2phi} | != GR | DERIVED value; choice of "mass=ruler" CHOSE |
| Sense-1 literal (local rest mass m0 fixed everywhere) | neither | **0** | e^{+phi} | != GR (!) | verifier finding; CHOSE |
| clock energy x proper-3-volume e^{-2phi} | mixed | **-3** | e^{-2phi} | != GR | the inline guess; CHOSE (two choices) |
| geometric mean (clock & ruler) | neither | **0** | e^{+phi} | != GR | CHOSE |
| time/length face x coordinate c (not local) | — | **+3** | e^{4phi} | != GR | CHOSE |

**Is any reading FORCED by "time primary + mass tied to time"?** NO — it is a
MENU {-3, -1, 0, +1, +3}, each selected by two defensible-but-not-forced choices:
(i) is "mass" read through its time-face or length-face, and (ii) does the
length->mass conversion use the local c0 or the coordinate c0 e^{-2phi}. "Time
primary" does pick out the time-face/clock reading as natural — which gives
**a = -1 = GR**. So "time primary, mass tied to time," taken at face value,
actually points AT the GR value, not away from it. Charles's "they may diverge"
is the live alternative (a != -1) but is NOT forced by the principle.

**Honest tension the verifier surfaced:** Sense-1 taken LITERALLY (local rest
mass = m0, fixed everywhere) gives a = 0 — itself a NON-GR weight e^{+phi}. So
the under-determination is if anything WIDER than "a=-1 vs not": the menu spans
GR (a=-1) AND several distinct modified values (0, +1, -3, +3). "a is the dial"
between Sense-1-literal and "mass dilates."

---

## 4. THE SELF-VARIATION STRUCTURE — does matter enter self vs probe differently?

This session found that because **phi IS the metric**, varying the action with
respect to phi carries an extra `+e^{-2phi} phi'^2` term (coefficient -1 vs -2)
relative to the test-probe equation: the metric's own DOF re-enters when phi is
self-consistent, not a fixed background.

**OBSERVE — how the matter source enters this distinction:**
- A geometry identity holds on this metric: **Box_g phi = -G^th_th** (DERIVED, sympy residual 0, in both running-rate doc and its verifier). So the th-th field equation IS the phi-equation: `Box_g phi = -kappa0 e^{(a+1)phi} T^th_th`. The matter source enters the SELF-consistent phi-equation as a weighted source term `e^{(a+1)phi} T^th_th` — i.e. **the matter's coupling to phi inherits exactly the same e^{(a+1)phi} weight** as the rest of the source law. There is no separate, second weight for matter-sourcing-phi.
- The self-vs-probe distinction (the -1 vs -2 coefficient) lives in the GEOMETRY/kinetic side (the Box_g phi operator on a self-consistent phi), NOT in the matter weight. A test probe in a fixed phi-background sees the GR source; a self-consistent phi sees its own back-reaction PLUS the weighted matter source.
- **Key OBSERVE:** the self-variation extra term is itself of the absorbable varying-coefficient kind on the GEOMETRY side — and the vacuum half being settled (=GR vacuum) is precisely the statement that this geometry-side term folds away at T=0. With matter present, the matter source enters through the same weight `e^{(a+1)phi}`; it does NOT acquire an extra self-vs-probe factor of its own. So the self-variation structure does NOT add a second independent fingerprint — it routes back to the same single `a+1`.

**Caveat flagged (Principle 7 / the derive-natively safeguard):** the "this
geometry-side term folds away => vacuum=GR" step is EXACTLY the kind of step the
safeguard says to interrogate. It was interrogated this session for the VACUUM
half (three confirmations). For the MATTER-present case the folding has NOT been
re-checked with a self-consistent phi AND a generic T simultaneously — that is a
named open check (§7), not a closed result.

---

## 5. PREMISE LEDGER (chose vs derived) + every GR / fitted-quantity leak surface

| # | Item | chose / derived | GR-leak / fitted-leak risk |
|---|---|---|---|
| P1 | Metric form (static/spherical/diagonal/areal-r) | CHOSE the slice (form DERIVED from "stay relativistic", CANON C-2026-06-18-1) | round+static => Birkhoff => vacuum forced GR regardless |
| P2 | **Left side = STANDARD Einstein tensor G_munu** | **CHOSE** | **PRIMARY GR-LEAK.** Keeping the EH R-term IS importing GR's curvature sector; it MAKES the scalar-weight absorbable (Bianchi tautology). "Vacuum=GR" is by CONSTRUCTION here. The genuinely native UDT left-hand-side law is UNBUILT. |
| P3 | Source weight = e^{(a+1)phi} (uniform scalar) | DERIVED upstream (field-eqn doc) GIVEN P2 + m~e^{a phi} | a scalar weight => absorbable by §2; departure only via the ratio |
| P4 | Exchange law nabla T = -(a+1) phi' T | **DERIVED** (Bianchi + P2 + P3) | clean, identity-level |
| P5 | T~ = e^{(a+1)phi} T conserved => weight absorbable | **DERIVED + blind-verified** | the make-or-break; CONFIRMED |
| P6 | Non-absorbable fingerprint = ratio e^{-(a+1)phi}, runs iff a!=-1 | **DERIVED + blind-verified** | the sole carrier |
| P7 | m(phi) = m0 e^{a phi}, local c0/m0/hbar fixed (Sense-1) | CHOSE (Sense-1 postulate) | the `a` is OPEN; not derived |
| P8 | Value of `a` | **UNDER-DETERMINED** (menu {-3,-1,0,+1,+3}; a=-1 admissible) | a=-1 = GR is a live member; "a!=-1" NOT proven |
| P9 | Box_g phi = -G^th_th (matter sources phi via same weight) | **DERIVED** (sympy residual 0) | — |
| P10 | "geometry-side self-term folds away with matter present" | **NOT yet checked** (only vacuum checked) | OPEN; Principle-7 interrogation target |

**Where GR / a fitted quantity could sneak in:**
1. **P2 is THE smuggle-surface.** Standard G on the left guarantees vacuum=GR AND makes every scalar source-weight absorbable. The departure is then confined to one number `a`. If the genuinely native left-hand-side law differs (non-scalar, Cassini-safe, non-relabelable), the whole matter-source framing could be the wrong sector — this is the gravity-sector question, firewalled separately.
2. **The absorbability IS GR returning:** `G = kappa0 T~` literally IS GR. The only thing holding UDT off GR on the matter side is `a != -1` (P8), which is unproven.
3. **No fitted quantity entered:** no mu^2, no mu^2=pi/3, no Lambda, no mass/ratio/wall/macro number, no SM value. The weight's "8" (running-coupling packaging) is units arithmetic, and is absorbable anyway. Clean on the fitted-leak axis.
4. **Choosing `a` by hand would be the fitted-leak risk to come.** Any future pin of `a` MUST be DERIVED (a covariant rest-mass definition), never inserted to make masses come out.

---

## 6. CAN THE IN-STEP vs OUT-OF-STEP QUESTION BE SETTLED FROM THE PRINCIPLE ALONE?

**Honest answer: NO — not at the level of the source law with a generic T.**
- The dilation principle + the committed structure pin a MENU, not a value. a=-1 (GR, in-step) survives as the clock/energy-redshift reading and as the timelike-Killing-energy reading; a=+1, 0, -3, +3 survive under other defensible choices. The two routes (kinematic dimensional vs field<->particle) do NOT pin the same number, and the field route admits NO single exponent at all (its kinetic sector scales e^{(a-1)phi}, angular e^{(a+1)phi} — different powers, because the kinetic term carries an extra g^{rr}=e^{-2phi} contraction).
- **What the principle DOES settle (real, banked):** (a) the source LAW form, with the depth-weight explicit and the Bianchi exchange law attached; (b) that a scalar weight is absorbable, so the departure is funneled into the single dimensionless ratio e^{-(a+1)phi}; (c) the exact in-step (a=-1) vs out-of-step (a!=-1) condition; (d) the structural vindication of "no single metric rate for mass to ride" (clock and ruler genuinely diverge).

**The MINIMAL additional input needed to settle it (named precisely):** a
**covariant definition of the particle's rest mass** — either the timelike-Killing
energy at infinity, or the matter action's own conserved Noether charge — for an
ACTUAL localized solution. That definition fixes BOTH free choices at once (the
time-face/length-face AND which c), collapsing the menu to one value. The
committed field source cannot supply it because it has NO mass parameter m at all
(it is a pure field; the e^{-2phi} in it is the metric contraction g^{rr}, not a
mass weight — confirmed against complete_metric_batched.py line 78).

**Why that input is NOT yet available:** computing a covariant rest mass requires
an actual localized matter SOLUTION — which is the imported-OBJECT /
consequence-stage that this session's hard constraints (and the gating on DERIVE)
explicitly hold OUT. So:

> **The matter-source departure is PARTIALLY derivable now.** Settled at the
> source-law level: the law's FORM, the exchange law, the absorbability of the
> scalar weight, and the EXACT fingerprint+condition (a+1 = 0 <=> GR). NOT
> settable now: the VALUE of `a` (in-step vs out-of-step), because that requires
> a covariant rest-mass of an actual localized object — the gated, future,
> consequence-stage step. The principle hands us a sharp BINARY (is a+1 zero?) and
> the exact quantity to compute, but not the answer.

---

## 7. NAMED OPEN CHECKS (for PONDER / future gated work — not done here)

1. **The decisive pin (gated):** compute the covariant rest mass of UDT's actual localized matter solution TWO ways — timelike-Killing energy at infinity vs the matter action's Noether charge — and read off `a`. If they agree and = m0 c0^2 e^{-phi} => a=-1 => UDT's novelty is GLOBAL/structural, not a local matter-coupling. If they differ / give a!=-1 => UDT genuinely modifies GR's source. (Requires the consequence-stage object; out of scope this session.)
2. **The self-vs-probe folding WITH matter present (§4, P10):** re-derive whether the geometry-side self-variation term genuinely folds away when phi is self-consistent AND a generic T is present simultaneously — the Principle-7 interrogation, done for vacuum, NOT yet for the matter-present case.
3. **The gravity-sector alternative (firewalled, separate push):** whether a genuinely native, non-scalar, Cassini-safe LEFT-hand-side law exists that is NOT relabelable to GR. If it does, the matter-source framing (P2) is the wrong sector and `a` may be moot. This is the gravity-sector-modification question Charles flagged; kept OUT of this matter-source MAP by the firewall.

---

## 8. SINGLE CLEANEST STATEMENT

> UDT's matter-source law is `G_munu = (8piG/c0^4) e^{(a+1)phi} T_munu` with the
> standard Einstein tensor on the left; Bianchi then FORCES the source to exchange
> with the dilation field, `nabla T = -(a+1) phi' T` — the geometric face of "mass
> dilates with position." But that scalar depth-weight is ABSORBABLE
> (blind-verified): it relabels back to ordinary GR with a conserved source, for
> ANY exponent. The ENTIRE non-absorbable UDT-vs-GR departure on the matter side is
> the single dimensionless ratio (matter ruler)/(metric ruler) ~ e^{-(a+1)phi},
> which runs with depth IFF `a != -1`. Reading "time primary, mass tied to time"
> off the metric VINDICATES the structural claim that clock (e^{-phi}) and ruler
> (e^{+phi}) DIVERGE so no single metric rate exists for mass to ride — but it does
> NOT force a!=-1: the natural time-face/clock reading gives a=-1=GR, and the menu
> {-3,-1,0,+1,+3} spans both GR and modified values. **The in-step (GR) vs
> out-of-step (UDT) question is a SHARP BINARY (is a+1 zero?) that the principle
> hands us cleanly but CANNOT settle at the source-law level — settling it requires
> a covariant rest-mass definition (timelike-Killing energy or the action's Noether
> charge) of an ACTUAL localized object, which is the gated, consequence-stage
> step held out this session.** NOT canon; MAP + OBSERVE only.
