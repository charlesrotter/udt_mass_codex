# UDT Modified Field Equations — Crux Derivation

**Mode:** careful DERIVE + honest determination (NOT exploration).
Gated/foundation-securing, authorized by Charles 2026-06-18.
**Category-A, DATA-BLIND:** derive from the stated principle only; import NO
mechanism; no mass/ratio/wall numbers used anywhere.

**Script:** `udtfe_field_equations.py` (sympy, CPU). Every symbolic claim below
is machine-produced by that script (and the inline `python3 -c` checks logged in
the session). Tags: **DERIVED / CHOSE / CONVENTION**.

**Constructor:** Claude Opus 4.8 (1M), 2026-06-18. Verifier-before-record: an
ATTACK HERE block is provided; a blind adversarial pass is required before this
result is treated as banked. **Nothing committed was changed.**

---

## 0. The owner's principle, verbatim (the postulates for this derivation)

> **(P0) DERIVATIVE-OF-POSITION HIERARCHY:** SR dilation depends on the 1st
> derivative of position (velocity); GR dilation on the 2nd derivative
> (acceleration ≡ gravity); UDT adds the 0th derivative — POSITION ITSELF.
> Dilation is a direct function of position phi.
>
> **(P1) MASS AND TIME both dilate with position:** m = m(phi), clock-rate =
> clock-rate(phi). Space dilates RECIPROCALLY (the B=1/A tie, already derived).
> NB mass-dilation with position is NEW vs GR (where rest mass is invariant) — it
> is the new SOURCE effect.
>
> **(P2) c IS NOT CONSTANT:** c = c(phi), a position-field, varying — markedly at
> cosmological and sub-nuclear EXTREMES. Promoting c from a universal constant to
> a position-field is the core modification of Einstein's equations.
>
> Already derived (HOLD): metric form (CANON C-2026-06-18-1)
> g_tt = -e^{-2phi}c^2, g_rr = e^{2phi}, B=1/A (g_tt g_rr = -c^2), from "remain
> relativistic". phi defined up to a constant.

---

## 1. c(phi) and m(phi) PINNED from the principle + metric form

### 1a. The local light speed

From g_tt = -e^{-2phi}c^2, g_rr = e^{2phi} (areal r^2 dΩ^2 for the slice), two
distinct "light speeds" exist and must not be conflated:

- **Coordinate null speed** (radial, ds^2=0):
  `(dr/dt)_coord = sqrt(-g_tt/g_rr) = c0 · e^{-2phi}`  **[DERIVED]**.
  Squared: `(dr/dt)^2 = c0^2 e^{-4phi}` — this is **exactly** CANON C-2026-06-13-1's
  radial wave speed `c_r^2 = e^{-4phi}` (verified identically in script). The
  program's committed "varying-c signature" IS this coordinate speed.

- **Locally measured null speed** (proper length / proper time):
  `v_local = sqrt(g_rr) (dr/dt)_coord / (sqrt(-g_tt) dt / c0) = c0` **exactly**,
  for ANY diagonal N(r), L(r) (script: `v_local for ARBITRARY N,L = c_unit`).

**KEY LEMMA (DERIVED).** For *any* diagonal metric the locally measured light
speed is the unit constant. The metric components ALONE cannot make the
*physically measured* c vary. So:

```
c(phi) read off the metric = c0 e^{-2phi}  COORDINATE speed   [DERIVED]
c(phi) physically measured by local rods/clocks = c0 (constant) [DERIVED]
```

### 1b. The dilated mass m(phi)

P1 says m = m(phi). R1+R2 (the composition/difference logic that forced the
exponential clock law) apply equally to any positional dilation, so the only
composition-consistent form is

```
m(phi) = m0 · e^{a phi}        [DERIVED form; exponent a still to pin]   [DERIVED]
```

The clock-rate dilation is `dτ/dt = e^{-phi}`. The natural P1 reading — "mass
dilates *with position the same way time does*" — is the statement that the rest
energy measured at the reference position redshifts like the clock, i.e. the
locally-measured rest mass tracks `e^{-phi}` (a = -1), OR is treated as an
independent new exponent if mass dilation is a genuinely separate dial. **This
single exponent a is the whole physical question (see §2).**

---

## 2. *** THE DEEP DETERMINATION — physical vs absorbable ***

The question: is UDT's varying-c the **trivial coordinate** kind (=> collapses to
GR) or a **genuine physical** modification (UDT ≠ GR)?

### 2a. The varying-c in the metric is ABSORBABLE (coordinate / units)

Three independent arguments, all confirmed in script:

1. **Locally measured c is constant regardless of the metric** (§1a lemma).
   `v_local = c0` for arbitrary N(r), L(r). A varying *coordinate* light speed is
   present in ordinary Schwarzschild too (the corpus itself states this at
   udt_canonical_geometry.md §21.4: "the standard GR result… locally measured
   speed is always c… Shapiro delay is the integrated coordinate effect"). This is
   sense (i) — NOT a modification.

2. **Putting cl(r) into g_tt is not a new degree of freedom.** Write
   g_tt = -e^{-2phi} cl(r)^2. The script shows the Ricci scalar then depends on
   cl(r) — but only because cl(r) has been *folded into the lapse*: defining
   `phĩ := phi - ln cl(r)/c0... ` (equivalently absorbing cl into the definition
   of the potential), the metric is identical in form to a const-c metric with a
   shifted phi. A position-dependent factor on `dt^2` alone is reparametrized away
   into phi; it carries no invariant content beyond what phi already carries. So
   "c = c(phi) in the metric" adds nothing the existing phi did not already encode.

3. **The committed `c_r^2 = e^{-4phi}` is the coordinate speed**, verified
   identically equal to `(dr/dt)_coord^2`. GW170817 consistency in the corpus
   (§21.5) is the GR-trivial "both ride the same coordinate delay" cancellation.
   This is the coordinate sense throughout.

**Verdict on P2 taken alone: the varying-c, as a metric/coordinate statement,
ABSORBS into a units/coordinate choice. By itself it does NOT modify the field
equations — UDT collapses to GR on this front.** (This is a first-class result,
and it agrees with the program's own §21.4 note.)

### 2b. The genuinely-new ingredient is m(phi) — and ITS absorbability is the test

GR has invariant rest mass. P1's m(phi) is the one ingredient with no GR
counterpart. The non-absorbability test is a **dimensionless ratio of two rulers
built from different sectors** — a metric ruler and a matter (Compton) ruler —
because units/coordinate choices cancel in dimensionless invariants and CANNOT
hide a real difference there.

- Metric proper ruler: `e^{phi} dr`.
- Matter Compton ruler: `λ_C = ħ/(m c) ~ e^{-a phi}` (with locally-measured c
  constant, §2a).
- **Ratio** (matter ruler)/(metric ruler) `~ e^{-(a+1) phi}` (script).

```
a = -1  =>  ratio exponent = 0  =>  phi-INDEPENDENT  => ABSORBABLE (collapses to GR)
a ≠ -1  =>  ratio runs with phi  => PHYSICAL, NON-ABSORBABLE (genuine UDT modification)
```

**The single most decisive argument.** A varying c or a varying phi can ALWAYS be
absorbed into coordinate/unit choices because they are properties of *the metric /
the chart*. The ONLY thing that cannot be absorbed is a phi-dependence of the
**ratio between a matter-built standard and a metric-built standard** — because a
units rescaling moves both together and cancels in the ratio. That ratio runs with
phi **iff the mass-dilation exponent a ≠ -1**, i.e. iff matter does NOT dilate in
lockstep with the metric's own rulers. Therefore:

> **UDT is a genuine modification of GR if and only if m(phi) dilates with a
> different exponent than the metric's clock/ruler (a ≠ -1). If matter rides the
> metric exactly (a = -1), UDT is GR in disguise (a units choice).**

The make-or-break is thus **NOT** the varying-c (absorbable, GR-trivial) but
**whether the mass-dilation is metric-locked or independent**. This is a sharp,
testable fork — and it relocates "the modification" out of the metric/curvature
and into the **matter coupling**, exactly where the orchestra-metaphor angular
source (C-2026-06-14-1) lives.

**HONEST STATUS:** the principle as stated (P1+P2) does NOT *by itself* pin a.
"Mass and time both dilate with position" is consistent with a = -1
(metric-locked, GR-trivial) and with a ≠ -1 (genuine). The owner's framing — that
mass dilation is "the NEW source effect" not present in GR — *intends* a ≠ -1
(otherwise it is not new). But that intent must be DISCHARGED by a derivation of a
from the metric/action, not asserted. **The derivation of `a` is the genuine
open crux this push exposes** — and it is a matter-sector question, not a
metric/curvature one.

---

## 3. The modified field equations

Carry the Einstein structure through with c → c(phi) and source mass → m(phi) as
position-fields. The action is GR + matter, with c promoted in the metric, in the
coupling, and in the stress:

```
S = ∫ d^4x sqrt(-g) [ c(phi)^4 / (16 π G) · R  +  L_matter(m(phi), c(phi), g) ]
```

Varying g^{μν} gives, in mixed form,

```
G^μ_ν  =  (8 π G / c(phi)^4) · T^μ_ν[m(phi), c(phi)]      [field equation]   [DERIVED-structure]
```

**Curvature side (computed, script §4–5).** For the locked diagonal form
g = diag(-e^{-2phi}c0^2, e^{2phi}, r^2, r^2 sin^2θ) the mixed Einstein tensor is

```
G^t_t = G^r_r = e^{-2phi} ( -2 r phi' - e^{2phi} + 1 ) / r^2          [DERIVED]
G^θ_θ = G^ψ_ψ = e^{-2phi} ( 2 r phi'^2 - r phi'' - 2 phi' ) / r       [DERIVED]
G^t_t - G^r_r = 0  identically  (the B=1/A consequence, source-free)  [DERIVED]
```

**Promoting c → cl(r) in g_tt** gives (script §5)

```
G^t_t - G^r_r = -2 e^{-2phi} cl'/(r cl)                                [DERIVED]
```

— nonzero, BUT (per §2a-2) this is the cl-folded-into-phi reparametrization, not
new invariant content: it is removed by redefining phi, so it does not constitute
a modification of the *equations*, only of the *chart*.

**Matter side — where the modification (if a≠-1) actually enters.** The stress
tensor of a source built from m(phi) carries the dilation explicitly. For the
program's own angular/topological source (CANON C-2026-06-14-1),
L = -(ξ/2) g^{μν} ∂_μ n_a ∂_ν n_a (+ L4), the position-dilation enters T through
the metric measure AND through any m(phi)-weighting of the field normalization.
The modified phi field equation is then the screened-scalar equation already in
the corpus (§2.2),

```
(1/r^2) d/dr( r^2 e^{-2phi} phi' ) - μ^2 phi = -S(r)                  [matches corpus fragment]
```

with the **modification living in S(r)**: if a ≠ -1, the source carries an extra
`e^{(a+1)phi}` weight (the non-cancelling ruler ratio of §2b) that GR's
invariant-mass source does not. **That weight — and only that weight — is the
genuine UDT modification of the field equations.** With a = -1 it is unity and the
equations are GR's.

**Tags:** the Einstein-tensor expressions are DERIVED. The action form (c^4/16πG
coupling, c in T) is the CONVENTIONAL GR structure with c promoted (CONVENTION +
DERIVED-structure). The exponent a is **UNPINNED by the stated principle** (the
open crux). The areal r^2 dΩ^2 and static/diagonal slice are CHOSE (per
C-2026-06-18-1: four un-forced choices).

---

## 4. Reduction + consistency checks

**(a) Reduce to GR when variation is switched off?** YES. Set c(phi) → c0
constant and a = -1 (matter rides the metric): the ruler ratio is phi-independent,
the source weight is unity, and the field equations are exactly Einstein's on the
metric form. Confirmed: with const c the Einstein tensor above is the standard
SSS Einstein tensor; G^t_t = G^r_r is the usual B=1/A consequence.

**(b) Consistent with existing fragments?** YES.
- `c_r^2 = e^{-4phi}` (CANON C-2026-06-13-1) = `(dr/dt)_coord^2` — verified
  identically equal (script). The angular wave speed `c_θ^2 = e^{-2phi}/r^2` is
  the corresponding transverse coordinate speed (g_tt/g_θθ = e^{-2phi}c0^2/r^2 /
  c0^2). Both are coordinate speeds — consistent with §2a.
- The screened-phi equation `(1/r^2) d/dr(r^2 e^{-2phi} phi') - μ^2 phi = -S`
  (§2.2) is recovered as the phi field equation; the modification (a≠-1) is a
  reweighting of S, not a new operator. Consistent.

**(c) Does the VACUUM modified equation differ from Schwarzschild/Birkhoff?** NO.
In vacuum S = 0, m(phi) is absent (no matter), so the a-exponent never enters; the
only field equation is `G^θ_θ = 0`, identical to GR's, whose
asymptotically-flat solution is Schwarzschild (Birkhoff). **The bare-vacuum no-go's
are therefore NOT GR artifacts that UDT evades** — UDT's vacuum IS GR's vacuum,
because the genuine modification lives entirely in the *matter* sector (the m(phi)
source weight), which vanishes in vacuum. This is decisive and honest: **UDT can
only differ from GR where matter (m(phi)) is present**; the modification cannot
rescue a *vacuum* result.

---

## 5. PREMISE LEDGER (chose / derived / convention)

| # | Item | Status |
|---|---|---|
| L1 | coord null speed `(dr/dt)=c0 e^{-2phi}` | **DERIVED** (metric, ds^2=0) |
| L2 | locally measured c `= c0` for any diagonal metric | **DERIVED** (proper-length/proper-time) |
| L3 | `c_r^2 = e^{-4phi}` is the coordinate speed (matches C-2026-06-13-1) | **DERIVED** |
| L4 | varying-c in metric absorbable into phi/units | **DERIVED** (Ricci shows cl folds into lapse) |
| L5 | `m(phi)=m0 e^{a phi}` functional form | **DERIVED** (R1+R2 composition) |
| L6 | non-absorbability ⇔ ruler ratio runs ⇔ `a ≠ -1` | **DERIVED** (dimensionless invariant) |
| L7 | exponent `a` value | **UNPINNED** — open crux, matter-sector question |
| L8 | field eqn `G^μ_ν = (8πG/c^4) T^μ_ν` with c,m promoted | **CONVENTION** (GR structure) + DERIVED curvature |
| L9 | screened-phi eqn as the phi field equation | DERIVED-structure, matches corpus §2.2 |
| L10 | static / spherical / diagonal / areal-r slice | **CHOSE** (per C-2026-06-18-1, 4 un-forced choices) |
| L11 | vacuum = Schwarzschild/Birkhoff | **DERIVED** (modification vanishes with matter) |

Nothing imported. No data, mass, ratio, or wall number used.

---

## 6. REGIME / SCOPE STAMP

- **Scope:** the static, spherical, diagonal, areal-r slice of the field
  equations, with c and source-mass promoted to position-fields. Covers the
  physical-vs-absorbable determination in full generality (the §2a lemma and §2b
  ratio argument are chart-independent); covers the vacuum reduction exactly.
- **Holds:** the verdict (varying-c absorbable; modification iff a≠-1 in matter;
  vacuum = Schwarzschild) is robust to chart and to the spherical/static slice,
  because it rests on (i) a coordinate-invariant lemma and (ii) a dimensionless
  ratio.
- **Does NOT determine:** the value of a (the open crux), the off-diagonal /
  non-stationary sectors (free per C-2026-06-18-1), or the realized matter source
  beyond the angular-sector fragment.
- **Premises that, if revised, void the verdict:** if "locally measured c" is
  redefined (e.g. UDT denies the local-Lorentz tangent space — but that would
  break "remain relativistic", R1-R3), L2/L4 change and varying-c could become
  physical. Flag in NEGATIVES_REGISTRY if revisited.

---

## 7. ATTACK HERE (for the blind adversarial verifier)

1. **The §2a lemma (load-bearing):** Recompute `v_local` for a general diagonal
   metric. Is it REALLY c0 for arbitrary N(r),L(r)? Try a non-diagonal (shift)
   term g_{tr} — does a frame-dragging term make local c anisotropic/physical?
   (If yes, the off-diagonal sector — free per C-2026-06-18-1 — could host a
   physical varying-c the diagonal slice misses. This is the strongest possible
   attack on the "absorbable" verdict.)
2. **The §2b ratio (the crux argument):** Is "(matter ruler)/(metric ruler) runs
   with phi" REALLY the unique non-absorbable invariant, or could a units choice
   that rescales ħ, G, or charge ALSO absorb the a≠-1 case? Check that no global
   constant rescaling removes `e^{(a+1)phi}` (it cannot — it is position-dependent
   — but verify ħ/G/charge can't carry a compensating phi-dependence without
   themselves becoming position-fields, which would be a NEW postulate).
3. **cl-folds-into-phi (§2a-2):** Verify that g_tt=-e^{-2phi}cl(r)^2 is genuinely
   the SAME geometry as g_tt=-e^{-2phĩ}c0^2 for some phĩ — i.e. confirm cl carries
   no invariant content beyond phi. Compute a second curvature invariant
   (Kretschmann) both ways and check the cl-dependence is pure reparametrization.
4. **Vacuum = Schwarzschild (§4c):** Confirm that with no matter, a never enters,
   so the vacuum equation is identical to GR's and yields Schwarzschild. Attack:
   could a vacuum c(phi) (no matter, but c still a field) source curvature via the
   c^4/16πG coupling's variation? Vary the action w.r.t. c as an independent field
   and check whether a vacuum c-equation appears that GR lacks.
5. **The a-pinning (the open crux):** Try to DERIVE a from the metric/action
   alone (e.g. from how a test mass's worldline action m(phi)∫dτ extremizes, or
   from the energy-at-infinity redshift). If a is forced to -1, UDT collapses to GR
   even in matter; if forced to ≠-1, UDT is genuinely modified and the value of a
   is the first new physical number. Determine honestly which (or that the
   principle leaves it open).
6. **Import/data-blind check:** confirm no mass/ratio/wall number, no SM/GR value,
   was used. (GR is used only as field-equation structure + local-Lorentz clock
   reading.)

---

## 8. SINGLE CLEANEST STATEMENT

> Promoting c to a position-field c(phi) does NOT modify Einstein's equations:
> the locally measured light speed is c0 for any metric (a coordinate-invariant
> lemma), the metric's varying-c is the GR-trivial coordinate speed
> `c0 e^{-2phi}` (= the committed `c_r^2=e^{-4phi}`), and a varying c in the metric
> folds into a redefinition of phi. The ONLY genuinely-new, non-absorbable
> ingredient is the position-dilation of MASS, m(phi)=m0 e^{a phi}: UDT is a real
> modification of GR **iff matter dilates with a different exponent than the
> metric's own rulers (a ≠ -1)** — detectable only in the dimensionless ratio of a
> matter-built ruler to a metric-built ruler, which units choices cannot hide. The
> modification therefore lives entirely in the MATTER COUPLING (a reweighting
> `e^{(a+1)phi}` of the source), never in vacuum: UDT's vacuum IS Schwarzschild /
> Birkhoff. Pinning the exponent a from the metric/action is the genuine open
> crux this derivation exposes — and it is a matter-sector question, not a
> curvature one.

---

## 9. BLIND VERIFIER VERDICT — 2026-06-18 (verifier agent a749944227799e5c0)

**STANDS.** Independent sympy re-derivation (no constructor code reused);
nothing committed changed. Verifier files: `udtfe_verify_blind.py`,
`udtfe_verify_axisC.py`, `udtfe_verify_axisC2.py`.

- **A (local c, incl. off-diagonal attack) PASS.** `v_local = c0` for arbitrary
  diagonal N(r),L(r). The strongest attack — a shift `g_tr=s(r)` — gives only
  COORDINATE one-way anisotropy; the invariant null condition shows any static
  observer still measures c0. The off-diagonal escape route is CLOSED; "absorbable"
  survives the free off-diagonal sector.
- **B (coordinate-speed = committed signatures) PASS.** `(dr/dt)^2=c0^2 e^{-4phi}`
  matches `c_r^2=e^{-4phi}`; `c_th^2=c0^2 e^{-2phi}/r^2` matches the committed value.
- **C (cl folds away) PASS, with a wording caveat.** Ricci AND Kretschmann
  differences are identically zero across two (phi,cl) splittings — no invariant
  content in cl. CAVEAT: "folds into phi" is loose; cl folds into the LAPSE, and a
  cl-in-g_tt-only metric holding g_rr fixed LEAVES the B=1/A family
  (g_tt g_rr = -cl^2 != -c0^2). The absorbability conclusion is correct; the wording
  is imprecise. (Noted here, not a defect in the verdict.)
- **D (ruler ratio — the load-bearing argument) PASS.** `e^{-(a+1)phi}` is
  phi-independent iff a=-1; a global rescale of hbar/G/charge cannot kill a
  position-dependent factor. Genuinely non-absorbable iff a!=-1.
- **E (vacuum = Schwarzschild) PASS.** The exponent `a` does NOT appear anywhere in
  the vacuum Einstein tensor; Schwarzschild zeroes G^t_t and G^th_th. Vacuum is
  exactly GR.

**Single most important finding (verifier):** the central verdict is sound and
Axis D is the genuinely-correct load-bearing argument. The honest qualifier — that
P1+P2 do NOT pin `a` (consistent with both a=-1 collapse and a!=-1 modification) —
is already disclosed as the open crux, so the result is not oversold. The
derivation establishes the precise CONDITION under which UDT is a modification and
correctly relocates it to the matter sector; it does not yet establish that UDT IS
a modification (that needs `a` pinned).

CANONIZATION = Charles's call.

## DRIVER-LEVEL BLIND VERIFIER — 2026-06-18 (agent a15684af7ae3e9cce): STANDS-CONDITIONALLY
Independent sympy re-derivation from scratch (no constructor code reused). All five computational/
structural claims CONFIRM; the honest catch (Claim 6) verified + disclosed.
- C1 (c(phi)): coordinate null speed c0 e^{-2phi} (sq = c0^2 e^{-4phi} = committed c_r^2); LOCAL speed
  = c0 for any diagonal metric; the off-diagonal-shift escape CLOSED (orthonormal static frame gives
  local speed c0 regardless). Varying-c ALONE is the trivial coordinate kind => absorbable => GR. CONFIRMS.
- C2 (m=m0 e^{a phi} unique, a free): Cauchy multiplicative eqn forces exponential; a unpinned. CONFIRMS.
- C3 (THE make-or-break: UDT modifies GR IFF a != -1): (matter Compton ruler)/(metric proper ruler)
  ~ e^{-(a+1)phi}, phi-independent iff a=-1; a global rescale of hbar/G/charge cannot remove a position-
  dependent factor (would require a fundamental constant to itself become a field = a different theory).
  Beyond-GR content in a minimally-coupled metric theory can only live in matter coupling differing from
  equivalence-principle behavior = exactly what a parameterizes. iff SOUND; a=-1 = GR-collapse. CONFIRMS.
- C4 (curvature side unmodified; modification only in the source weight e^{(a+1)phi}): full independent
  Einstein tensor: G^t_t=G^r_r identically, c0 absent from mixed G (folds into lapse). CONFIRMS.
- C5 (reduction + VACUUM=Schwarzschild/Birkhoff EXACTLY): Kretschmann identical across the lapse-absorption
  split; in vacuum T=0 the weight multiplies zero so a never enters => UDT vacuum = GR vacuum. DECISIVE
  COROLLARY: the bare-vacuum no-go's (Phases 1-2, #62/#63) are NOT rescued by the modification — they are
  UDT verdicts too. (Scoped: c slaved to phi, not an independent dynamical field.) CONFIRMS.
- C6 (honest catch): the stated principle (P0 hierarchy / P1 mass&time dilate / P2 c not constant) does
  NOT pin a; a static test-mass action leaves a as a free slope. So this does NOT prove UDT IS modified —
  it proves the CONDITION (a!=-1) and relocates the live question into the MATTER coupling. CONFIRMS.
(T) clean: data-blind, category-A, no modification overclaimed or genuine one dismissed.
NET BANKED: UDT's field equations = G^mu_nu=(8piG/c^4)T^mu_nu with c->c(phi)=c0 e^{-2phi} (coordinate;
local=c0) and matter source carrying a WEIGHT e^{(a+1)phi}; the CURVATURE/VACUUM side is IDENTICAL to GR
(=> vacuum=Schwarzschild/Birkhoff, bare no-go's confirmed). UDT genuinely modifies GR IFF a != -1 (mass
dilates out-of-step with the metric's rulers); the principle does NOT pin a => PINNING a (a matter-sector
question) is the crux. Canonization = Charles's call.
