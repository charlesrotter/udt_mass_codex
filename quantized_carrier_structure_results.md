# Quantized Carrier — Spectrum STRUCTURE (Postulate A on the native time-live carrier)

**Mode:** STRUCTURE-FIRST, DATA-BLIND. The first step of the post-postulate-A program.
**Agent:** claude-opus-4-8[1m]. **Date:** 2026-06-19. **Status:** NOT canon. Append-only working record. No git commit.
**Scripts:** `quantized_carrier_structure.py` (WKB / Bohr–Sommerfeld + shape-of-V_eff),
`quantized_carrier_eigensolve.py` (direct tridiagonal eigensolve cross-check, sign/stability, depth/n forms),
`quantized_carrier_depthform.py` (profile-robustness of the depth verdict).
**DATA-BLIND:** no lepton/mass/ratio/wall numbers loaded anywhere (contract 26fc757; verified by inspection).
**Anti-numerology:** no rational/integer promoted to evidence; the only constants are the exact geometric
`l(l+1)` (already banked as the charge) and `4pi`. No new identity claimed; no TEST-B classifier required.
**Comparison to lepton wall numbers: NOT done** (the later gated, pre-registered test).

---

## 0. The frame — what is being quantized, and with what (the boundary honored)

Charles's decision (2026-06-19): accept **POSTULATE A**. UDT = **quantized dilation-geometry**.
The geometry is native; quantization discretizes the continuous native carrier.

**KEPT NATIVE (not postulated, not imported):**
- the **time-live standing-wave carrier** (validated, blind-verified: timelive_nonround_native_solve_results.md):
  `L_space[U] = omega^2 M[U]`, `M>0`, `L_space` negative-definite, so `omega^2 = -<U,L_space U>/<U,M U> > 0`
  — a **continuous** standing-wave family.
- the **area-form CHARGE** centrifugal term `l(l+1)` (l>=1; native, banked: N=3, q=1/3, eta=1/18).
- the **dilation DEPTH** profile `v0(r)` (= the `e^{phi}` / `e^{2v0}` structure; deep negative core -> 0 exterior).
- **i = the area form** (Charles: i STAYS NATIVE — the harmonic-balance phase uses the area-form complex
  structure J, J^2=-1; the quantization is canonical quantization with the symplectic form = the area form).

**POSTULATE A (the ONLY quantum input):** (i) hbar as the quantum of action / Bohr–Sommerfeld
`oint p dq = (n+1/2) hbar`; (ii) spin-1/2; (iii) fermion statistics (distinct quantized states = distinct
particles, a catalog). NOTHING MORE. FIREWALL honored: no Dirac import, no gauge group, no SM masses/couplings,
no imported BC.

---

## 1. The native carrier, stated exactly (the object being quantized)

From the validated time-live non-round solve (blind-verified, §0 cite), the radial reduction of
`L_space[U] = omega^2 M[U]` in Liouville normal form is a **1D Schrödinger problem**:

```
-(P U')' + [ l(l+1) W(r) + Q(r) ] U  =  omega^2 M(r) U ,     P = M = W = e^{2 v0(r)} ,  l >= 1.
```

The validated classical reading of this operator (banked, verifier-confirmed): a **scattering/continuum
problem with an angular-momentum barrier** — an INTRINSIC floor `omega^2 = l(l+1) W_inf` plus a
BOX-CONTROLLED continuum above it (spacing -> 0 as R grows). **No classical binding well was found there.**

Putting it in Schrödinger form (substitute `U = M^{-1/4} psi`, exact; `M=P=W` ⇒ `W/M=1`, `P/M=1`):

```
-psi'' + V_eff(r) psi = E psi ,   E = omega^2 ,   V_eff(r) = l(l+1) + V_L(r) + Q/M ,
V_L(r) = (1/2) s'(r) - (1/4) s(r)^2 ,   s(r) = (ln M)' = 2 v0'(r)      [EXACT, sympy-derived]
```

Two structural facts visible immediately:
- the centrifugal/charge term is a **flat pedestal `l(l+1)`** (constant, because `W/M=1`), not an `r^-2` wall —
  it sets the **continuum threshold `V_inf = l(l+1)`** (`v0->0` exterior).
- **any binding WELL must come from the LIOUVILLE potential `V_L` of the dilation depth `v0(r)`** (or from Q,
  which is non-load-bearing here). `V_L` depends **only on DERIVATIVES of `v0`** — this is the load-bearing fact.

---

## 2. POSTULATE A applied — Bohr–Sommerfeld + direct eigensolve (two independent methods agree)

**Method 1 (WKB / postulate A):** `INT_{r-}^{r+} sqrt(E - V_eff) dr = (n+1/2) pi`, turning points `V_eff(r±)=E`.
**Method 2 (cross-check):** direct tridiagonal eigensolve of `-psi'' + V_eff psi = E psi`, FIXED grid `h`,
FIXED inner core (deep `r->0` FD-strain excluded, flagged), R-scan. The two agree.

### Finding 1 (CLEAN POSITIVE) — the dilation depth makes a GENUINE, INTRINSIC bound well

The Liouville potential `V_L` of the deep-core `v0(r)` **dips below its `r->inf` asymptote** over a finite
`r`-range ⇒ `V_eff` has a **WELL with two turning points** for a band of E (Step A.2: turning-point count = 2
for D = 1, 3, 6). Bohr–Sommerfeld then quantizes **between the two intrinsic turning points**, and the bound
levels are **R-INDEPENDENT** (direct eigensolve, l=1):

```
 D=1.5:  E_0 = 1.64337 (R=8), 1.64301 (R=16, 32, 64)   <- flat to 5 digits across an 8x range
 D=2.0:  E_0 = 1.00225  (R=8..64, identical)
 D=3.0:  E_0 = -1.24438 (R=8..64, identical)
 D=4.0:  E_0 = -4.8489, E_1 = 1.99(0) (R=16..64, flat)
```

This is a **real departure** from the validated classical finding (which saw only a scattering continuum with
a box-controlled band). **Postulate-A quantization of the depth well gives INTRINSIC discrete levels — not
box-controlled.** The quantization replaces the box: the turning points are set by `hbar` + the native depth +
the charge floor, not by the cell size `R`. This is also the OPPOSITE of the #44 / single-cell breathing
tower (which was `omega^2 ~ 1/R^2 -> 0`, box-controlled). **So the carrier, quantized, does produce an
intrinsic discrete well — the first such on this program.**

### Finding 2 (THE OBSTRUCTION — sign/stability) — the well over-binds into TACHYONS; the radial tower is SHALLOW

The validated carrier REQUIRES `omega^2 = E > 0` (a real standing-wave frequency). But a well deep enough to
hold many levels pushes the ground state to `E = omega^2 < 0` — a **tachyon / exponential instability**, not a
standing wave. The depth is therefore **bounded above** (l=1, direct eigensolve):

```
 D     E_0 = omega^2
 1.00   +1.968   stable
 2.00   +1.002   stable
 2.50   +0.044   stable (barely)
 2.75   -0.558   TACHYON  <- ground omega^2 goes negative beyond D* ~ 2.6
 4.00   -4.849   TACHYON
```

**Profile-robust** (gaussian / lorentzian / expcore / sech^2 cores all show the same crossover, `D* ~ 2.4–3.4`).
Counting STABLE (`E>0`) bound radial levels at every depth below `D*`, across all four profiles:

```
 MAX stable (E>0) radial bound levels  =  1   (every native-like profile)
```

So the **radial-overtone axis houses at most ONE stable level** before the well over-binds into instability.
**There is no tall radial tower of standing-wave masses** — the radial axis is NOT a generation ladder.
(This is the sharp, honest cost: an intrinsic well exists, but it is shallow, and depth past `D*` destabilizes
rather than adds levels.)

### Finding 3 (THE HIERARCHY OBSTRUCTION) — depth -> mass is POWER-LAW, NOT exponential

The lepton-hierarchy target is an **exponential-in-depth** mass law (`m ~ e^{-depth}`). It does **NOT** appear.
The binding `(V_inf - E_0)` vs the dilation depth `D` is, across all four native-like profiles:

```
 gaussian   :  binding ~ D^3.5   (POWER-LAW; exp-fit clearly worse)
 lorentzian :  binding ~ D^4.3
 expcore    :  binding ~ D^4.9
 sech2      :  binding ~ D^4.0
```

**The reason is structural and exact (the load-bearing mechanism):** the dilation amplitude
`e^{2 v0} = e^{-2 D f(r)}` IS exponential in the depth `D`, but `V_eff` is built from the **Liouville potential
`V_L = (1/2)s' - (1/4)s^2` with `s = 2 v0'`** — i.e. **only from DERIVATIVES (log-derivatives) of `v0`**. The
log-derivative `s = 2 v0'` is **linear** in `D`, so `V_L ~ (v0')^2 ~ D^2` and the well depth / binding scale as a
**POWER of the depth parameter, not `exp(D)`**. The exponential gets "differentiated away." **The `e^{phi}` depth
amplitude does NOT pass through to an exponential mass law on this radial-carrier route.** This is the #44-flavor
failure in a new dress, and it is profile-robust ⇒ a structural obstruction, not a profile artifact.

### Finding 4 — the only tall, clean discrete axis is the area-form CHARGE `l(l+1)` (already banked)

The angular/charge quantum number `l` (l>=1) shifts the threshold and well together:

```
 l=1: V_inf = l(l+1) = 2,   E_0 = 1.00,   (2l+1) = 3
 l=2: V_inf = 6,            E_0 = 5.00,   (2l+1) = 5
 l=3: V_inf = 12,           E_0 = 11.00,  (2l+1) = 7
```

This `l(l+1)` ladder IS genuinely discrete and intrinsic — but it is **exactly the already-banked CHARGE
discreteness** (`l=1, (2l+1)=3`, area-form `4pi`, N=3), NOT a new mass tower. So the one tall clean discrete
structure the quantized carrier offers is the charge axis re-read, consistent with B1/B2/timelive — not a new
generations ladder.

---

## 3. The spectrum STRUCTURE (the deliverable) — functional form of `m_n`

Assembled, with `E = omega^2`, `m_n ~ omega_n = sqrt(E_n)` (E = hbar omega; mass = dilation cost of the mode):

| property | verdict |
|---|---|
| **DISCRETE?** | YES — postulate-A quantization of the intrinsic depth well gives discrete levels. |
| **INTRINSIC (not box)?** | YES for the bound well — R-independent to 5 digits over 8x cell range. (Continuum ABOVE threshold stays box-discretized, as before — but the BOUND levels are intrinsic.) |
| **functional form `m_n(n)`** | a **SHALLOW well: at most ONE stable radial level** (`E>0`) per (D, l); the radial overtone `n` does NOT generate a tall tower — depth past `D*` ⇒ tachyon, not more levels. |
| **`m_n(depth D)`** | **POWER-LAW `binding ~ D^{3.5..4.9}`, NOT exponential** (profile-robust). The `e^{phi}` amplitude is differentiated away by the Liouville construction. |
| **`m_n(l)`** | the `l(l+1)` charge ladder — intrinsic and discrete, but = the **already-banked charge**, not a new mass family. |
| **RATIOS `m_n/m_0` scale-free?** | YES by construction — the overall dimensionful prefactor (`sqrt(kappa/xi)`, hbar-unit, core width) cancels in `sqrt(E_n/E_0)`. Ratios retain only the dimensionless depth `D` and `l`. (But with ~1 stable radial level, there is no nontrivial radial ratio to form.) |
| **EXPONENTIAL-hierarchical?** | **NO** — neither in `n` (only 1 level) nor in depth (power-law). This is the named obstruction. |

**`m_n` functional form, honestly:** `m^2 = E = l(l+1) - |binding(D)|`, `binding(D) ~ D^k` (k≈3.5–4.9),
with a single stable radial node, valid only for `D < D*(profile)` (above which `m^2 < 0`, unphysical).
Discrete in `l` (= charge); a single stable radial level; power-law (not exponential) in depth.

---

## 4. Where SPIN-1/2 / STATISTICS / the area-form i enter the structure

- **spin-1/2 (postulate A ii):** enters as the **`(n+1/2)` Maslov / zero-point shift** in Bohr–Sommerfeld.
  With **i = the area-form J** (native), the canonical 1-form `p dq` is the area-form symplectic potential and
  the half-integer index is the **area-form Maslov index** (2 turning points ⇒ Maslov 2 ⇒ `+1/2`). So the `+1/2`
  zero-point is the **native spin-1/2**, not an imported convention. (In this radial problem the area-form i does
  not add or remove levels vs a generic i; it CERTIFIES the `+1/2` is native.)
- **fermion statistics (postulate A iii):** makes each discrete `(n, l)` state a **DISTINCT PARTICLE** in the
  catalog (one occupant per quantized state) — the particle-catalog frame, now with a quantization rule selecting
  the states.
- **degeneracy / multiplicity:** each `l` carries `(2l+1)` area-form orientations; the area-form i's orientation
  count is where J enters the multiplicity. (Not assigned to observed particles here — gated, data-blind.)

---

## 5. PREMISE LEDGER (native / postulate-A / chosen) — front-loaded

| Item | tag | note |
|---|---|---|
| carrier `L_space[U]=omega^2 M[U]`, `M>0`, `L_space` neg-def, omega^2>0 | **NATIVE** (validated, blind-verified) | timelive_nonround_native_solve_results.md |
| Liouville form `-psi''+V_eff psi=E psi`, `V_eff=l(l+1)+V_L`, `V_L=(1/2)s'-(1/4)s^2` | **DERIVED-here exact (sympy)** | the load-bearing "only-derivatives-of-v0" fact |
| `l(l+1)` centrifugal/charge floor, l>=1 | **NATIVE** (banked charge: N=3, q=1/3) | B1/B2/timelive |
| `E = omega^2`, `m_n ~ omega_n` (E=hbar omega, mass=dilation cost) | **POSTULATE A (i) + native dilation cost** | hbar quantum of action |
| Bohr–Sommerfeld `oint p dq=(n+1/2)hbar` | **POSTULATE A (i)** | the discretizer |
| `i = area-form J`, Maslov `+1/2` = spin-1/2 zero-point | **NATIVE i (Charles) + POSTULATE A (ii)** | i stays native |
| fermion statistics ⇒ distinct states = distinct particles | **POSTULATE A (iii)** | catalog |
| depth profile `v0(r) = -D f(r)`, deep core -> 0 exterior | **CHOSE (generic native-like)** | *** SHORTCUT: not the pointwise coupled v0; tested 4 profiles (gaussian/lorentzian/expcore/sech^2) — all agree *** |
| core width `a`, set =1 | **CHOSE (unit; cancels in ratios)** | scale-free in the dimensionful unit |
| source proxy `Q(r)` | **CHOSE; non-load-bearing** | Q=0 does not change the floor (prior result) |
| inner core `r->0` excluded (FD strain) | **forced; flagged** | single-cell-spectrum-box-controlled caveat honored |
| cell size `R` | **SCAN variable** (R-independence is a test, not fixed) | box-control gate ran |

---

## 6. HONEST OBSTRUCTION CHECK (the deliverable verdict)

**Does quantizing the native carrier cleanly give a DISCRETE, INTRINSIC, SCALE-FREE, plausibly-HIERARCHICAL
structure ready for the gated value test? — HALF-OPEN. A real positive AND a sharp obstruction, two-edged:**

**The clean POSITIVE (genuine, not narrated):** Postulate A *does* what the year of classical solves could not —
it turns the continuous native carrier into a discrete spectrum with an **INTRINSIC (non-box) bound well** created
by the dilation depth's Liouville potential, R-independent to 5 digits. This is the first time the program has an
intrinsic (not box-controlled, not box-continuum) discrete level on this carrier. The quantization genuinely
replaces the box. **i stays native; the `+1/2` is the native area-form spin-1/2.** This part is ready and clean.

**The named OBSTRUCTION (three-pronged, profile-robust, must not be hidden):**
1. **The radial tower is SHALLOW — one stable level, then TACHYON.** Depth past `D* ~ 2.4–3.4` drives
   `omega^2 < 0` (instability), so deepening does not add radial levels. The radial-overtone `n` is **not** a
   generation axis.
2. **Depth -> mass is POWER-LAW (`~D^{3.5..4.9}`), NOT exponential.** The `e^{phi}` amplitude is differentiated
   away by the Liouville construction (`V_eff` sees only `v0'`, linear in D). **The lepton-style exponential
   hierarchy does not come out of the quantized radial carrier.** (This is the #44 failure mode re-appearing on
   the quantized carrier — reported plainly, per the prompt's explicit instruction not to repeat it silently.)
3. **The only tall clean discrete axis is the `l(l+1)` CHARGE — already banked**, not a new mass family.

**Net:** quantizing the native carrier yields a **clean intrinsic discrete WELL (positive)** but **not a
clean hierarchical generation tower (obstruction)** — the radial axis gives ~1 stable level and a power-law
(not exponential) depth law, and the discrete-and-tall axis is the charge it already had. **So it is NOT yet
ready for the gated value test as a lepton-generation spectrum.** The discretizer for a *tall, exponential,
multi-level* tower is still missing on this carrier.

**Where a tall tower could still live (DIRECTION, not a result — no false convergence):**
- the **nonlinear back-reaction / breather amplitude** (the fully-coupled time-live solve where the mode's own
  amplitude feeds back: `omega(A)`) — genuinely unbuilt, flagged in the timelive doc as the one place a deeper
  binding can hide;
- a **COMPOSITE label** (the area-form charge `l` × a small radial `n`) as the catalog index, rather than a tall
  single-axis tower — consistent with the particle-catalog frame (discreteness = a catalog of stable cells, not a
  quantized ladder);
- a depth law that enters through the **amplitude `e^{phi}` directly** (e.g. the mass = dilation-cost INTEGRAL
  `INT (1-e^{-2phi})`, which IS exponential in depth) rather than through the carrier's **frequency** (which sees
  only `v0'`) — i.e. the hierarchy may live in the **cost functional**, not the **eigenfrequency**. (Stated as a
  target; the cost-vs-frequency split is the precise next question.)

---

## 7. ANTI-SHORTCUT / DISCIPLINE statement

- **DATA-BLIND:** PASS. No wall numbers; comparison to leptons NOT done (gated).
- **Anti-numerology:** PASS. No rational promoted to evidence; `l(l+1)`, `4pi` are exact banked geometry.
- **No manufactured exponential:** I explicitly TESTED the depth law and FOUND it power-law; I did NOT fit an
  exponential. I explicitly tested the radial tower and FOUND it shallow (1 level + tachyon); I did not narrate a
  tower.
- **Intrinsic-vs-box verified:** R-scan run; bound levels R-independent to 5 digits (intrinsic); the continuum
  above threshold remains box-discretized (reported, not banked as physical).
- **Two methods agree:** WKB Bohr–Sommerfeld and direct tridiagonal eigensolve give the same well, sign, and forms.
- **SHORTCUT FLAGGED (load-bearing):** the radial `v0(r)` is a modeled native-like profile, not the pointwise
  converged COUPLED time-live `v0`. Tested across 4 profiles — the structural verdicts (intrinsic well; 1 stable
  level + tachyon; power-law depth; charge axis = banked) are **profile-robust**. The ABSOLUTE numbers are not
  banked. The fully-coupled nonlinear back-reaction is the one place a deeper/different well could still appear,
  and is correctly left OPEN.
- **No false convergence:** this is ONE informative tile — quantization gives an intrinsic well (real advance) but
  not an exponential generation tower (sharp obstruction). The discretizer for a tall hierarchical tower remains
  missing on this carrier.

---

## 8. ONE-LINE SUMMARY

Postulate-A quantization of the native time-live carrier **does** produce a genuine **INTRINSIC (non-box) discrete
bound well** from the dilation depth's Liouville potential (R-independent to 5 digits — the first intrinsic
discrete level on this program, with the `+1/2` a native area-form spin-1/2) — **but** the radial tower is
**SHALLOW (one stable level, then tachyon)**, the depth->mass law is **POWER-LAW not exponential** (the `e^{phi}`
amplitude is differentiated away by the Liouville construction — the #44 failure on the quantized carrier), and
the only tall clean discrete axis is the **already-banked `l(l+1)` CHARGE**; so the quantized carrier gives a
clean intrinsic discreteness but **NOT yet a clean exponential lepton-generation tower** — the named obstruction
is that mass enters the eigen-FREQUENCY through `v0'` (power-law), and a tall/exponential tower would have to come
from the nonlinear breather back-reaction or from the dilation-COST functional (exp in depth), both UNBUILT.

## STATUS
STRUCTURE-FIRST complete: WKB + direct eigensolve agree; intrinsic well (positive) + shallow/power-law/charge-axis
obstruction (negative), profile-robust across 4 native-like depth profiles. NATIVE provenance (carrier, charge,
depth, area-form i all native; only hbar/spin/statistics postulated). DATA-BLIND; anti-numerology PASS. One
SHORTCUT flagged (modeled radial profile; fully-coupled nonlinear solve not built) — profile-robust, does not
change the structural verdict. NOT canon. No git commit. Blind verifier next.
