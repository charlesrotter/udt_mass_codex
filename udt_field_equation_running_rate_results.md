# UDT Field Equation as a Running-Rate Law — OBSERVE results

Agent: general-purpose (driver-delegated) | Date: 2026-06-18
MODE: **MAP / OBSERVE** — report what is there, premises attached, NO targeted
verdict, **NOT canon**. Verifier-before-record applies before any banking.
Scripts: `running_rate_geometry.py`, `running_rate_bianchi_absorb.py`,
`running_rate_philaw.py` (committed-but-not-by-me; do not edit, append new files).

Frame (Charles-confirmed 2026-06-18, lay): "UDT's field equation = Einstein's law,
but the trade-rate between mass-energy and curvature DEPENDS ON WHERE YOU ARE."
Candidate, the OTHER way (not the dead f(phi)R / Brans-Dicke way that gave γ=9,
Cassini-dead — see `udt_gravity_sector_rederivation_results.md` CORRECTION):

> **G_munu = kappa(phi) T_munu ,   kappa(phi) = (8 pi G / c0^4) e^{8 phi}**

LEFT side = the STANDARD Einstein tensor of the UDT metric (no curvature-side
modification). Metric (CANON C-2026-06-18-1; static/spherical/diagonal/areal-r =
CHOSEN): `ds^2 = -e^{-2phi} c0^2 dt^2 + e^{2phi} dr^2 + r^2 dOmega^2`, single slaved
`phi(r)`, `c(phi)=c0 e^{-2phi}`.

---

## TASK 1 — the law stated; left side verified standard; empty space is quiet

Computed the Einstein tensor of the metric directly (`running_rate_geometry.py`):

```
G^t_t = G^r_r   = (1 - e^{2phi} - 2 r phi') e^{-2phi} / r^2
G^th_th = G^ph_ph = (2 r phi'^2 - r phi'' - 2 phi') e^{-2phi} / r
```

This IS the standard Einstein tensor (left side carries NO e^{8phi}, NO (g box -
nabla nabla)f Brans-Dicke terms). **Vacuum check (G^mu_nu = 0):** substituting the
Schwarzschild profile `phi = -1/2 ln(1 - r_s/r)` makes **all four mixed components
vanish identically**. So:

> **Empty space (T=0) => exactly Schwarzschild => UDT vacuum = GR vacuum => Cassini-safe by construction.**

This is the deliberate contrast with the f(phi)R route: there the running rate sat
ON the curvature and survived into vacuum (γ=9, killed by Cassini). Here it sits on
the SOURCE, so it is absent in vacuum.

Also verified the geometry identity used in Task 4: **`Box_g phi = -G^th_th` exactly**
(difference simplifies to 0).

---

## TASK 2 — Bianchi => the source-conservation law (derived, then interpreted)

Contracted Bianchi gives `nabla_mu G^{mu nu} = 0` identically. Applied to
`G^{mu nu} = kappa(phi) T^{mu nu}`:

```
0 = nabla_mu(kappa T^{mu nu}) = kappa nabla_mu T^{mu nu} + (nabla_mu kappa) T^{mu nu}
d ln kappa / d phi = 8     (since kappa ~ e^{8phi})
=>  nabla_mu T^{mu nu} = -8 (partial_mu phi) T^{mu nu}            [DERIVED]
```

**The source is NOT ordinarily conserved.** Mass-energy exchanges with the dilation
field along phi-gradients, at rate 8 phi'. Native reading: as the source sits deeper
(phi more negative going inward in this sign convention), the trade-rate kappa=e^{8phi}
changes, and the Bianchi bookkeeping FORCES a compensating non-conservation of T —
mass-energy "leaks into / out of" the position-dilation as you move in depth. This is
the geometric expression of "mass dilates with position": the metric's own
consistency (Bianchi) MANDATES that a depth-dependent trade-rate be paired with a
depth-exchanging source. It is derived from the identity, not posited.

Chart-level form (static diagonal source `T^mu_nu = diag(-rho, p_r, p_t, p_t)`,
`running_rate_philaw.py`), the nu=r component is UDT's modified hydrostatic relation:

```
p_r' + (rho + p_r) phi' + (2/r)(p_r - p_t)  =  -8 phi' p_r     (UDT)
[ GR same LHS = 0 ]                                            (GR)
```

i.e. UDT adds an explicit `-8 phi' p_r` exchange term to the equilibrium law.

---

## TASK 3 — PHYSICAL vs ABSORBABLE — the make-or-break — VERDICT (iii) DEPENDS

**Explicit transformation attempt.** Define the field-redefined source
`T~_munu := (kappa/kappa0) T_munu = e^{8phi} T_munu`, kappa0 = 8 pi G/c0^4. Then the
field equation becomes `G_munu = kappa0 T~_munu` — **GR with a CONSTANT coupling**.
Is T~ a legitimate (conserved) source?

```
nabla^mu T~_munu = e^{8phi}[ nabla^mu T_munu + 8 partial^mu phi T_munu ]
                 = e^{8phi}[ -8 partial phi T + 8 partial phi T ] = 0   (by Task 2)
```

**Confirmed at chart level** (`running_rate_philaw.py`): substituting UDT's on-shell
relation `nabla_mu T^mu_r = -8 phi' p_r` into `nabla_mu (e^{8phi}T)^mu_r` gives
**exactly 0**. So `T~` is covariantly conserved and `G = kappa0 T~` is, formally,
ordinary GR with an ordinary conserved source.

**=> The depth-running of kappa, taken BY ITSELF, is ABSORBABLE** — a redefinition of
what one calls the stress tensor. The exponent "8" does not survive as a physical
fingerprint.

**The dimensionless-invariant test** (corpus criterion,
`udt_field_equations_derivation_results.md` §2b — the only thing units/redefinitions
cannot move): a ratio of a MATTER-built ruler (Compton `lambda_C = hbar/(m c0)`,
`m ~ e^{-a phi}`) to a METRIC-built ruler (proper length `e^{phi} dr`):

```
ratio = lambda_C / (proper ruler) ~ e^{(a-1)phi}   [this convention; corpus form e^{-(a+1)phi}]
runs with phi  <=>  matter mass dilates with a DIFFERENT exponent than the metric ruler.
```

**The exponent "8" of the running coupling does NOT appear in this ratio.** The
non-absorbable physics is set entirely by the matter mass-dilation exponent `a`
(matter-ruler vs metric-ruler), which the field-equation FORM does not fix.

> **VERDICT: (iii) DEPENDS.** The running coupling `kappa(phi)=e^{8phi}` is, on its
> own, REMOVABLE bookkeeping (absorbed into a conserved `T~`, returning GR with
> constant coupling). It becomes a GENUINE, non-absorbable departure from Einstein
> ONLY in the presence of an additional native ingredient: **the matter's own
> mass-dilation must differ from the metric ruler (a != metric-locked).** That is the
> SAME dimensionless `a`-ratio crux the matter-sector derivation already isolated —
> the running-coupling reformulation relocates it but does not resolve it.

Honest note against false convergence: this is NOT outcome (i) PHYSICAL. The running
coupling alone does not give a depth-running dimensionless fingerprint; the c^4 piece
is exactly the absorbable varying-c kind the corpus already flagged as GR-trivial.

---

## TASK 4 — the phi-law it implies, vs GR

Using `Box_g phi = -G^th_th` and the th-th field equation `G^th_th = kappa T^th_th`:

```
Box_g phi = -(8 pi G/c0^4) e^{8 phi} T^th_th      [UDT running coupling]
Box_g phi = -(8 pi G/c0^4)          T^th_th      [GR constant coupling]
```

**Departure:** an explicit `e^{8 phi}` multiplicative WEIGHT on the source — a
0th-order-in-derivatives, depth-dependent source enhancement. It is NOT a kinetic /
mu^2 screening term (none inserted; none appears). But by Task 3 the SAME e^{8phi} can
be absorbed into `T~^th_th`, returning GR's phi-law; whether the weight is physical
is the same `a`-fork. So the phi-law "departs" only conditionally — exactly tracking
the Task-3 verdict.

---

## TASK 5 — is the steepness "8" forced?

`kappa ~ 1/c(phi)^4 = e^{8phi}`; the 8 = (power 4 on c) x (rate 2 in c=c0 e^{-2phi}).
That arithmetic is forced GIVEN that one writes 8 pi G/c^4 with c=c(phi). **But the
entire e^{8phi} is absorbable (Task 3), so 8 is NOT the physical steepness.** The
physical, non-absorbable steepness is whatever runs in the dimensionless ruler ratio
— governed by the matter exponent `a`, which is UNFORCED by the law. So: the "8" is
forced as a *coordinate/units* number, but the *physical* running rate is open and
equals the `a`-type quantity, not 8.

---

## PREMISE LEDGER (chose vs derived) + where GR can sneak back in

| # | Item | chose / derived | note / GR-leak risk |
|---|------|-----------------|---------------------|
| P1 | Metric form (static/spherical/diagonal/areal-r) | CHOSE (CANON C-2026-06-18-1 derives the *form* from "stay relativistic"; the static/round slice is chosen) | round+static => Birkhoff => vacuum forced GR anyway |
| P2 | Left side = STANDARD Einstein tensor G_munu (no f(phi)R) | **CHOSE** (this is the candidate's defining move) | **PRIMARY GR-LEAK.** Keeping the EH R-term / standard G on the left IS importing GR's curvature sector. Principle-7 flag: "empty=GR" is here by CONSTRUCTION, not derived. The native gravity action is still NOT derived. |
| P3 | kappa(phi)=8 pi G/c(phi)^4 (running coupling on source) | CHOSE (motivated by c=c(phi)) | the "8" is units arithmetic; absorbable (Task 3/5) |
| P4 | nabla_mu T = -8 phi' T (source law) | **DERIVED** from Bianchi + P2 + P3 | clean, identity-level |
| P5 | T~=e^{8phi}T conserved => absorbable | **DERIVED** (algebra + chart check) | the make-or-break |
| P6 | Matter ruler lambda_C ~ e^{-a phi}, local c=c0 | CHOSE (observer-frame Sense-1) | the `a` is OPEN; not derived here |
| P7 | Box_g phi = -G^th_th identity | **DERIVED** (sympy, residual 0) | — |

**Where GR sneaks back in (interrogation discipline):**
1. **P2 is the smuggle-surface.** By putting the standard Einstein tensor on the left
   and ALL the running on the source, we GUARANTEE "vacuum=GR" — the very property
   Charles flagged as suspect when it appeared on the f(phi)R side. Here it is a
   CHOSEN feature, honest but not derived. The native gravity action/curvature law of
   UDT is still unbuilt; we have only chosen which of two GR-compatible reformulations
   to wear.
2. The absorbability (Task 3) is precisely GR coming back: `G = kappa0 T~` IS GR.
3. The only thing that keeps UDT off GR is P6's `a != metric-locked` — a MATTER-sector
   fact, unproven, identical to the standing open crux.

---

## HONEST OVERALL READ

The "running-rate" field equation `G_munu = kappa(phi) T_munu` is **internally
consistent, Cassini-safe (empty=Schwarzschild by construction), and derives a clean
native source-exchange law `nabla T = -8 phi' T`** — that part is real and is the
geometric face of "mass dilates with position." BUT the make-or-break test is
**negative for a standalone gravitational departure**: the running coupling alone is
ABSORBED into a conserved redefined source `T~`, returning ordinary GR. The depth-
running leaves NO dimensionless fingerprint by itself; the "8" is the absorbable
varying-c^4 number.

So this reformulation does NOT, on its own, make UDT's field equation differ from
Einstein's. It **relocates** the entire physical question back onto the SAME unpinned
matter-ruler crux (`a`: does real matter dilate in lockstep with the metric ruler or
not?). Verdict (iii) DEPENDS. **What is still unpinned:** (1) `a` — the matter mass-
dilation exponent, the sole carrier of a non-absorbable fingerprint, still underived;
(2) the genuinely NATIVE UDT gravity action / left-hand-side law — we CHOSE the
standard Einstein tensor (P2), so we have not actually derived UDT's curvature sector
from the dilation principle, only selected a GR-compatible packaging. The suspect
"vacuum=GR" has not been escaped; it has been re-housed as a deliberate choice.

NOT canon. Recommend: verifier pass on Task-3 absorbability (the conserved-T~ claim is
load-bearing), then PONDER with Charles whether the honest target is the matter `a`
(matter-sector) or a truly native left-hand-side law (gravity-sector) — this push
shows the running-COUPLING packaging cannot substitute for either.
