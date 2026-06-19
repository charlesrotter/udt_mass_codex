# Native phi-Law MAP — Does UDT's gravitational law for phi depart from GR's, derived DIRECTLY from the dilation-carrying metric (no action assumed)?

**Mode:** MAP + first-OBSERVE (CLAUDE.md "How we work"). Make premises VISIBLE,
report WHAT IS THERE, no targeted verdict, NOT canon. Anti-smuggling is the point.

**Constructor:** Claude Opus 4.8 (1M), agent for udt_mass_codex, **2026-06-18**.
**Scripts (new, uncommitted):** `native_phi_law_einstein.py` (Einstein tensor +
Box_g phi + identity check), `native_phi_law_routes_AD.py` (Routes A/D: 0th-order
search + varying-c conservation injection), `native_phi_law_route_B.py` (Route B:
hierarchy / curvature-invariant argument). sympy CPU, exact.

**Frame (Charles 2026-06-18, lay):** the UDT metric ALREADY contains positional
dilation. Derive the LAW phi obeys (UDT's gravitational field equation) DIRECTLY
from the metric, NOT by assuming an action and varying it; see where it departs
from GR. Hard constraints honored: (1) NO gravitational action assumed; (2) NO
cosmological constant Lambda used; (3) lean on the candidate phi-equation
`Box_g phi - mu^2 phi = -S`, treating the `mu^2 phi` term as the prime sighting
of a departure. Safeguard `derive-natively-not-inherited-form` applied: every
"folds away / reduces to standard" step interrogated.

---

## 1. THE METRIC'S EINSTEIN TENSOR (pure geometry — NO field equation assumed)

CANON metric C-2026-06-18-1 (CHOSE: static, spherical, diagonal, areal-r):
`ds^2 = -e^{-2phi} c0^2 dt^2 + e^{2phi} dr^2 + r^2 dOmega^2`, phi = phi(r) slaved
to the metric (phi = -(1/2) ln(-g_tt/c0^2)). This is just the curvature of the
given metric — no source, no action, no posited law.

```
G^t_t   = e^{-2phi}/r^2 * ( -2 r phi' - e^{2phi} + 1 )
G^r_r   = e^{-2phi}/r^2 * ( -2 r phi' - e^{2phi} + 1 )        [= G^t_t IDENTICALLY]
G^th_th = e^{-2phi}/r   * ( 2 r (phi')^2 - r phi'' - 2 phi' )
G^ph_ph = G^th_th
Ricci R = 2 e^{-2phi}/r^2 * ( -2 r^2 (phi')^2 + r^2 phi'' + 4 r phi' + e^{2phi} - 1 )
```

Two facts FORCED by the metric (read directly off the tensor):

- **(F1) G^t_t = G^r_r identically.** Forced by the metric's reciprocal warp
  (g_tt carries e^{-2phi}, g_rr carries e^{+2phi}). This is the corpus's
  "T^t_t = T^r_r" sourcing constraint (CG §9.1-9.2) — pure geometry, not an
  imposed condition.
- **(F2) The covariant d'Alembertian of phi equals minus the angular Einstein
  component, EXACTLY:**
  ```
  Box_g phi = e^{-2phi}/r * ( -2 r (phi')^2 + r phi'' + 2 phi' )  =  -G^th_th
  ```
  Verified symbolically `Box_g phi + G^th_th == 0` (machine-exact, matches corpus
  CG §9.3, numeric residual 1.36e-9 in `bianchi_bridge.json`). **This is UDT's
  native, action-free scalar law: `Box_g phi = -G^th_th`.** It is a geometric
  IDENTITY of the dilation-carrying metric, not an assumption.

**The single load-bearing observation about FORM:** every term in G^mu_nu, in R,
and in Box_g phi is built from **phi' , phi'' , (phi')^2 , and the warp factor
e^{2phi}**. There is **NOWHERE** a bare, algebraic, no-derivative term linear in
phi (a `mu^2 phi`). The geometry contains no such object.

---

## 2. ROUTES A-D: the phi-law each yields, and its departure from GR

### ROUTE A (geometry + conservation, varying-c)
Computed `nabla_mu( c(phi)^4/(8piG) * G^mu_nu )` honestly with c=c0 e^{-2phi}
RUNNING. Since `nabla_mu G^mu_nu = 0` (Bianchi identity, pure geometry), the only
NEW piece the varying-c injects is the derivative-of-coefficient term
`(d/dr)[c(phi)^4] * G^r_r`, which evaluates (normalized) to
```
proportional to  phi' * ( 2 r phi' + e^{2phi} - 1 )
```
**A `phi'` (derivative) term — NOT a bare `mu^2 phi`.** The running c DOES change
the conservation law away from constant-c GR (a real departure: equal curvature
maps to position-dependent physical energy because the conversion factor
c(phi)^4 runs — see Route D), but the departure it produces is **first/second
order in derivatives of phi**, never a 0th-order algebraic phi term. The
hoped-for `mu^2 phi` does NOT fall out of varying-c conservation.
*Departure vs GR:* YES, but only as a derivative-structure reweighting, not the
screening term.

### ROUTE B (hierarchy completion; Charles's SR/GR/UDT 0th-1st-2nd framing)
GR's phi-law is built from up-to-2nd-derivative (curvature) terms; the UDT-native
addition is supposed to be a 0th-derivative (algebraic-in-phi) term, and the
question was whether `mu^2 phi` IS that 0th rung, with its coefficient fixed by
the dilation composition rules. Finding: **phi is the LOG of the dilation**
(phi = -(1/2) ln(-g_tt/c0^2)). A `mu^2 phi` term is `-(mu^2/2) ln(-g_tt/c0^2)` —
the logarithm of a metric component. **No curvature/geometric invariant is
algebraic-linear in phi:** curvature invariants are polynomial in g and its
derivatives, so they carry e^{2phi}, phi', phi'' — never a bare ln-type `phi`.
Dilation composition is ADDITIVE in phi (depths add: phi_a then phi_b -> phi_a+phi_b),
an additive group with NO intrinsic scale -> the native dilation law is
**scale-free** and a `mu^2` BREAKS the phi->phi+const shift structure. So the
0th rung, if it exists, is NOT delivered by geometry; it must be ADDED as a
potential V(phi). *Departure vs GR:* the 0th rung is not forced — it has to be put
in by hand.

### ROUTE C (where does the corpus actually introduce mu^2? derived or posited?)
Quoted verbatim. CG **§2.1** gives the action-free operator `Box_g f =
(1/r^2) d/dr(r^2 e^{-2phi} f')` — "the exact geometric scalar Laplacian," no mu.
CG **§2.2** then states: *"Adding a mass/screening term via the **minimal
quadratic action** S_phi = (1/2)int sqrt(-g)[ (grad phi)^2 + mu^2 phi^2 - 2 phi S ]"*
which yields `(Box_g - mu^2) phi = -S`. **The `mu^2 phi` term enters by POSITING
a quadratic mass action and varying it** — exactly the action-first move the
current frame forbids, and exactly the smuggle the prior gravity push was
corrected for. The VALUE `mu^2 = pi/3` (CG §13.2) is then assigned by a
numerological identity `mu^2 = pi * <cos^2 theta>_{S2} = pi/3`, **verified by
matching meson eigenvalue ratios to <=1.8%** — i.e. it fixes the value of an
already-posited mass by fitting the particle spectrum, NOT by forcing it out of
the gravitational metric. *Verdict:* `mu^2` (the screening term) is **POSITED via
an added action**, not derived from the dilation-carrying metric.

### ROUTE D (what sources the metric, natively; does running-c force a non-GR relation?)
Set T := G/(8pi) as the corpus "geometric identity" stance. Two readings:
- As a pure tensor identity, T^mu_nu = G^mu_nu/(8pi) is content-free (any metric
  "sources itself"); CG §9.3/§9.1 already flags the polynomial source as
  "tautological."
- The PHYSICAL statement that survives: the conversion from curvature to physical
  energy is c(phi)^4/(8piG), and c(phi)=c0 e^{-2phi} **runs with depth**. So
  **equal curvature corresponds to DIFFERENT physical energy density at different
  position** — a genuine, non-trivial UDT departure from GR's fixed-c relation.
  This is real and FORCED by the dilation. BUT: it is a depth-dependent
  *reweighting of the source-to-geometry map*, again carried by e^{-2phi}
  (a warp factor / derivative-structure object), NOT a new algebraic `mu^2 phi`
  in phi's equation of motion. *Departure vs GR:* YES (running c(phi)^4
  conversion is a true physical departure), but it is NOT the screening term and
  does not by itself yield a discrete spectrum.

---

## 3. THE KEY QUESTION (answered honestly)

**Is the `mu^2 phi` (0th-order/position) departure FORCED by the dilation-carrying
metric + native consistency, or CHOSEN/imported?**

**CHOSEN / imported.** Three independent lines (geometry inventory in §1, varying-c
conservation in Route A, curvature-invariant argument in Route B) all show the
metric's geometry contains **no algebraic-linear-in-phi term anywhere** — only
phi', phi'', (phi')^2 and e^{2phi}. The corpus itself introduces `mu^2 phi` by
**adding a minimal quadratic mass action** (CG §2.2) and then **fits its value**
`mu^2 = pi/3` to the meson spectrum (CG §13.2). It is not forced by the metric;
it is the one place an external action is grafted on.

**What the metric DOES force, action-free (the native phi-law that actually
emerges):**
```
Box_g phi = -G^th_th        (exact geometric identity, §1 F2)
```
This is GR's massless-scalar STRUCTURE (a pure second-order divergence operator,
no mass term) tied to the metric's own angular curvature. **In the screening
sense, UDT's natively-forced phi-law has NOT yet been shown to depart from GR's.**

**The departures that ARE native/forced** are (i) the reciprocal constraint
G^t_t = G^r_r (F1), and (ii) the running c(phi)^4 curvature->energy conversion
(Route D) — both real, both carried by the warp factor, NEITHER a `mu^2 phi`
screening term, NEITHER yet shown to produce discreteness.

---

## 4. PREMISE LEDGER (chose / derived / forced) + GR-sneak-back-in list

| # | Item | Status |
|---|------|--------|
| P1 | static, spherical, diagonal, areal-r metric ansatz | **CHOSE** (CANON C-2026-06-18-1; areal-r is a theorem given the other choices) |
| P2 | phi slaved: phi = -(1/2) ln(-g_tt/c0^2) | **derived** from metric def |
| P3 | c(phi) = c0 e^{-2phi} runs with position | **derived** (CANON; the dilation) |
| P4 | Einstein tensor G^mu_nu above | **derived** (pure geometry, sympy-exact, no law assumed) |
| P5 | Box_g phi = -G^th_th | **derived/FORCED** (exact identity, verified) |
| P6 | G^t_t = G^r_r | **derived/FORCED** by the metric |
| P7 | running c(phi)^4 conversion = real non-GR source map | **derived/FORCED** (Route D) |
| P8 | `mu^2 phi` screening term in phi's EOM | **CHOSE / POSITED** (added quadratic action, CG §2.2) |
| P9 | mu^2 = pi/3 value | **CHOSE / fit** (pi*<cos^2>; verified by meson-ratio match, CG §13.2 — value-assignment to a posited mass, not a metric-forcing) |
| P10 | source S(r) | **CHOSE/tautological** (corpus itself: "any profile implies its own source," CG §9.3) |

**Every place GR's form could have / did sneak back in (interrogated):**
- (a) **Assuming an action at all** — CG §2.2 grafts `S_phi = int sqrt(-g)[(grad phi)^2 + mu^2 phi^2 ...]`. This IS the action-first move forbidden here. The `mu^2 phi` departure rides entirely on this graft.
- (b) **"Box_g phi is the natural scalar law"** — true and action-free, but it is GR's massless-scalar FORM. Adopting it as the phi-law (then perturbing) re-imports GR's law unless a native mass is forced — and none is (§3).
- (c) **T := G/(8pi)** (Route D first reading) — writing the source as 8pi T = G is Einstein's relation; if read as the *law* rather than a tautology it re-imports standard Einstein. The push held it as identity only.
- (d) The prior (now-corrected, solar-system-falsified) push assumed
  `S = int sqrt(-g)[c(phi)^4/(16piG) R + L_m]` and varied it (PPN gamma=9). NOT
  repeated here; flagged as the cautionary precedent for action-first.

---

## 5. HONEST OVERALL READ

**OUTCOME (iii) with a live (ii)-flavored caveat — NOT (i).**

(iii) read: **Nothing in the dilation-carrying metric FORCES a `mu^2 phi`
departure.** The natively-forced scalar law is `Box_g phi = -G^th_th`, which is
GR's massless-scalar structure tied to the metric's angular curvature. The
corpus's `Box_g phi - mu^2 phi = -S` differs from GR's `Box phi = -S` ONLY by the
`mu^2 phi` term, and that term is **added by hand via a quadratic action** and its
value **fit to the meson spectrum** — it is CHOSEN, not derived. So, on the
gravitational/metric side and at the level Charles asked about, **UDT's phi-law
has not yet been shown to depart from GR's by a forced mechanism.** Reported
plainly, per the method (no false convergence to "it's modified").

The live, genuinely-native departures the metric DOES force — and which deserve
the next OBSERVE/PONDER, because they are real and un-smuggled — are:
1. **The running c(phi)^4 conversion (Route D):** equal curvature = different
   physical energy at different depth. A true non-GR physical statement, forced
   by the dilation, currently unexploited as a *dynamical* modifier.
2. **The reciprocal constraint G^t_t = G^r_r (F1):** strongly restricts what can
   source the metric (corpus: pure-EM or balanced Dirac+EM), forced by geometry.

Neither of these is a 0th-order `mu^2 phi`, and neither has yet been shown to
produce discreteness — but they are the honest native material. **The `mu^2 phi`
screening term, the corpus's headline departure, is a posited/fitted input, not a
metric-forced law.** If a native UDT gravitational law distinct from GR exists, on
this evidence it must come from the running-c conversion and/or the reciprocity
constraint acting dynamically — NOT from an added mass potential.

*MAP+OBSERVE only. Not canon. No verifier pass yet. No commit.*
