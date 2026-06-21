# F7 — NATIVE COSMIC-SCALE REDO + COSMIC->PARTICLE BRIDGE STATUS

**Mode:** OBSERVE / make-visible. This REMOVES the imported-Hubble smuggle Charles caught
(scale_symmetry_bootstrap §CORRECTION: "R_cell ~ 4.46 Gpc = c/H0 at rho_crit" RETRACTED as an
LCDM import) and replaces it with a UDT-NATIVE statement of the cosmic scale, plus a clean
status of the ~10^40 cosmic->particle gap. H0 and rho_crit are treated as OUTPUTS to COMPARE,
never inputs.
**Constructor:** Claude Opus 4.8 (1M), agent for udt_mass_codex, 2026-06-21.
**Compute:** CPU only, sympy/mpmath dps=50, bounded analytic. Scripts (/tmp, uncommitted):
`f7_native.py`, `f7_h0.py`, `f7_bridge.py`. **Status:** UNVERIFIED (no blind verifier pass yet)
— record-candidate, not banked. READ-ONLY on all committed docs.

Builds on / replaces the retracted number in: `scale_symmetry_bootstrap_analysis_results.md`
(§CORRECTION). Uses: `step0_bridge_results.md`, `CANON.md` (C-10-2 finite cell; 1+z=e^phi;
Misner-Sharp = public charge; c^2=2GM/R), `CRITICAL_UNIVERSE_FRAME.md`,
`FOUNDATIONAL_ASSUMPTIONS_LEDGER.md` (F5, F7, §SCALE-SYMMETRY).

---

## 0. THE ONE ALLOWED INPUT, AND THE DISCIPLINE

The SOLE cosmic anchor permitted is the one redshift datum z_CMB, entered through UDT's
**native** law `1+z = e^phi` (CANON):
```
phi_seal = ln(1 + z_CMB) = ln(1101) = 7.0039741367...     [the native depth at the cell boundary]
```
This is the ONLY input. `c` and `G` are the theory's two constants (a units link L/T and a
gravitational coupling), NOT cosmological observations. **H0 and rho_crit are OUTPUTS** to be
compared to observation as a TEST — never inputs. DATA-BLIND on particle/lepton wall numbers
(none loaded). Allowed macro-comparison category: cosmic consilience (H0, z_CMB).

---

## (A) NATIVE COSMIC-SCALE REDO

### A.1 What the native inputs actually fix — ONLY the ratio M/R. [DERIVED, script f7_native.py]

The native critical / horizon condition (CANON, the finite cell sitting at its own
Schwarzschild compactness) is
```
c^2 = 2 G M / R              (ONE equation, TWO unknowns M and R)
```
where M is the native Misner-Sharp mass = the cell's PUBLIC CHARGE (CANON). This pins **only the
ratio**:
```
M / R = c^2 / (2G) = 6.7330e26 kg/m.       [DERIVED — exact, no observation beyond c,G]
```
It does NOT pin R or M separately. {R, M} form a one-parameter SCALE FAMILY: choose R, get
M = R c^2/(2G); choose M, get R = 2GM/c^2. **The overall size is a FLAT DIRECTION — the
dilatation modulus — and the critical law alone does NOT pin it.**

This is forced by dimensions, not a solver weakness:
- `phi_seal = 7.004` is **dimensionless** (a depth). It carries no metres.
- From `{c, G}` and any pure number you CANNOT build a length: [c]=L/T, [G]=L³M⁻¹T⁻²; the
  mass dimension never cancels without a THIRD dimensionful input (a mass, a length, a time,
  or hbar). (Machine-checked dimensional argument, f7_native.py.)

**So the native anchor {z_CMB via 1+z=e^phi} + {c,G} + the critical condition fixes the cosmic
cell's SHAPE/COMPACTNESS (M/R at criticality) but leaves its absolute SIZE unpinned.** This is
exactly the dilatation symmetry's flat modulus (scale_symmetry §2) seen at the cosmic scale.

### A.2 The effective expansion rate as a genuine OUTPUT (no import). [DERIVED structure]

Define the effective expansion rate the way an external observer would read it off the cell:
```
H_eff := c / R_cell.
```
Two native statements follow, and ONLY these two:
```
(i)   H_eff * R_cell = c          (an IDENTITY — the cell of size R is seen to "expand" at c/R)
(ii)  M_cell = R_cell c^2 / (2G)   (the critical condition)
```
**Crucially, (i)+(ii) reproduce the standard "R = c/H0 at critical density" relation NATIVELY,
from the UDT critical condition alone — WITHOUT importing H0 or rho_crit.** In LCDM, at
rho_crit = 3H0²/8πG the Hubble radius R=c/H0 satisfies c²=2GM/R identically; here that same
pairing falls out of the native critical condition. The earlier doc IMPORTED this; we now
DERIVE the *relation*. What we do NOT get is a *number*: H_eff is order-correct for ANY
cosmic-sized R_cell, but its VALUE is the unpinned modulus.

### A.3 The H0-comparison TEST — stated honestly. [the deliverable]

What the native theory OUTPUTS for comparison to observation:
- The **relation** H_eff·R_cell = c at critical compactness — structurally CORRECT (this is
  why a critical universe looks like it expands at ~c/R; consilient with observed cosmology
  at the level of FORM). No tuning; derived from c²=2GM/R.
- A definite cosmic **order of magnitude** IF R_cell is any cosmic-scale length: H_eff lands at
  the ~10⁻¹⁸ s⁻¹ (tens of km/s/Mpc) order for R_cell ~ Gpc. **Order-correct, derived, not tuned.**
- A specific **number** for H0 (e.g. "67"): **NOT predicted by the native anchor alone.** It
  requires pinning R_cell, which is the deferred coupled solve (A.4).

Honest "is H0 a disguised input?" check: NO. We never fed H0 or rho_crit anywhere. The only
place an observed H0 appears in this doc is f7_h0.py as a back-solved COMPARISON ("if R_cell
were c/H0=4.47 Gpc then M_cell=5.6e79 protons") — explicitly labelled a target to compare
against, used in no derivation. The native content is the *relation* and the *order*, with the
absolute number deferred.

### A.4 What is GENUINELY DERIVED vs what needs the deferred coupled solve. [the honest split]

DERIVED from the native anchor (no import):
- The cosmic cell sits at criticality M/R = c²/(2G) (exact). [A.1]
- The depth at the boundary is phi_seal = 7.004 (native 1+z=e^phi on the one z datum).
- The effective expansion relation H_eff·R = c and M = Rc²/2G — the native restatement of
  "Hubble radius at critical density", with H0/rho_crit as OUTPUTS not inputs. [A.2]
- Therefore: a critical UDT cell is **order-correct** for cosmic H0 / size — the right FORM
  and the right ORDER, with NO tuning. The H0 comparison PASSES at order-of-magnitude / form.

NEEDS THE DEFERRED COUPLED SOLVE to PIN (the unpinned modulus, F5/scale-symmetry S8 pinning gap):
- The absolute R_cell (hence the absolute H0 *number*, hence M_cell). The candidate pinning
  mechanism is the finite-cell CLOSURE: does integrating phi from 0 to 7.004 across the cell
  WITH the field equation force ONE R? That is the "determines-vs-relates" question
  (CRITICAL_UNIVERSE_FRAME): does whole-metric closure DERIVE z_CMB / pin the size, or only
  RELATE the labels? **Open.** The one available linear time-live probe still box-controlled
  (omega·R = const), a warning that pinning is not yet demonstrated.

**Native cosmic-scale statement (replaces the retracted import):**
> The native anchor (z_CMB through 1+z=e^phi) plus the critical condition c²=2GM/R fixes the
> cosmic cell's COMPACTNESS (M/R) and depth (7.004) exactly, and OUTPUTS the effective-expansion
> *relation* H_eff·R=c — order-correct for the observed H0 with NO import and NO tuning. The
> absolute SIZE (and thus the H0 *number*) is the dilatation modulus, **unpinned by the law
> alone**; pinning it is the deferred finite-cell closure / coupled solve. The honest result is
> exactly the allowed first-class form: **scale set by the anchor up to the unpinned modulus;
> H0 comes out order-correct as an OUTPUT; the number awaits the coupled solve.**

The import is REMOVED: no 4.46 Gpc, no "=c/H0", no rho_crit=3H0²/8πG, no ~9 Gpc CMB-cell
matching. What survives is native: the critical relation and the order, with H0 as an output.

---

## (B) COSMIC -> PARTICLE BRIDGE STATUS

### B.1 What step0 already PROVED — M alone does NOT bridge. [DERIVED, re-verified script f7_bridge.py]

Independently re-derived (sympy, exact) the universality-killer:
```
(R / lambda_C) / sqrt(M_u / m)  =  sqrt(2)·sqrt(G)·sqrt(R)·m^(3/2) / hbar.
```
This carries **m^(3/2)** — it is NOT probe-independent (it ranges over ~5 orders across
electron->tau). So the only candidate universal geometric factor on the cosmic mass M FAILS:
there is NO single M-anchored length × one universal factor that lands every particle. Each
particle's size still requires its own mass m as an independent input. Confirmed:
- M alone fixes exactly ONE length, the horizon R = 2GM/c² = the COSMIC size (size ratio 1).
- The only other M-anchored lengths from {c,G,M,hbar} are hbar/(Mc) (sub-Planckian) and their
  geometric mean = sqrt(2)·l_Planck — probe-independent, 20+ orders too small. None is a
  particle size.
- The dilation DEPTH cannot carry the gap: bridging the size ratio ~10⁴⁰ needs |phi|=ln(10⁴⁰)≈92;
  the available matter-cell depth is |phi0|~0.8 (e^{-2phi0}~5). **Short by ~115x in the
  exponent.** The ~10⁴⁰ cannot come from phi. (Re-checked f7_bridge.py.)

### B.2 The IRREDUCIBLE open question. [stated cleanly — the point of F7]

What makes particle-scale cells **spectrally autonomous** from the Gpc-scale global domain?
Equivalently: what selects the ~10⁻¹⁵ m particle cell as a stable, self-contained configuration
~40 orders below the cosmic ruler, WITHOUT re-inserting the particle mass m by hand?

Why it is hard (the structural obstruction, now named precisely):
1. The classical theory is (anisotropically) scale-free on the depth+gradient sector
   (scale_symmetry, blind-verified): isolated cells are scale-FREE families (omega~1/R). The
   one length-pinning mechanism that DOES exist — matter's own dimensionful couplings
   l=sqrt(kappa/xi) — sets only high core modes, not a spectrum, and does not by itself produce
   a ~10⁴⁰ ratio.
2. The cosmic scale-setter (rho_bg -> curvature radius, the bootstrap) lands at the HUBBLE
   radius BY CONSTRUCTION (homogeneous density -> cosmic curvature length). Nothing in a
   homogeneous-background bootstrap reaches DOWN 40 orders. (scale_symmetry Sec 3.3.)
3. So a particle-scale cell cannot inherit its size from either (i) the dilation depth (B.1,
   ~115x short) or (ii) the cosmic bootstrap (lands at Gpc). It must be set by its OWN internal
   structure (the cavity + angular/topological sector, q=1/3 / N=3 selection) producing a
   DISCRETE size whose ratio to R is the ~10⁴⁰ — and that selector is the still-unbuilt piece.

This is **not a thing to close now.** It is the IRREDUCIBLE KNOWN-OPEN gap (C-10-2's "sharp open
question"), now stated cleanly enough that it stops being a vague "open": the gap is the
*absence of a per-particle discrete-size selector autonomous from the cosmic ruler*, and the
two trivial routes (depth, cosmic bootstrap) are PROVEN insufficient.

### B.3 Does the scale-symmetry result change the bridge picture? — NO (it set the COSMIC scale only).

The scale-symmetry/bootstrap work (i) confirmed the dilatation symmetry and re-read box-control
as its fingerprint, and (ii) mechanized the COSMIC scale (criticality pins the cosmic modulus).
It did NOT touch the cosmic->particle ratio: the bootstrap reproduces step0's verdict from a
second direction (cosmic curvature length only). So the bridge picture is UNCHANGED — and now
*reinforced* from two independent directions (step0's m^(3/2) killer + the bootstrap's
cosmic-only reach). F7 SPLITS cleanly:
- **F7 cosmic-scale half:** native-anchored (Part A) — relation + order derived, number deferred.
- **F7 cosmic->particle half:** the IRREDUCIBLE open gap (B.2) — what's needed (a native
  per-particle discrete-size selector), why it's hard (the two trivial routes are proven
  insufficient). NOT closed; STATED cleanly.

---

## PREMISE LEDGER (chose vs derived)

| # | Premise / choice | Status |
|---|---|---|
| P1 | phi_seal = ln(1101) = 7.004 (native 1+z=e^phi on the one z_CMB datum) | INPUT — the single allowed anchor (CANON); native law, observational z |
| P2 | c, G are the theory's two constants (units + gravitational coupling) | given (not cosmological inputs) |
| P3 | Critical condition c²=2GM/R (finite cell at own compactness) | CANON (C-10-2 / CRITICAL_UNIVERSE_FRAME); native |
| P4 | M = Misner-Sharp = cell's public charge; its VALUE is a solution label | CANON; the label is the unpinned modulus |
| **P5** | **{z_CMB, c, G, c²=2GM/R} fix ONLY M/R = c²/2G; size is a flat modulus** | **DERIVED (dimensional + algebraic, f7_native.py) — the central native statement** |
| P6 | H_eff := c/R_cell; H_eff·R=c and M=Rc²/2G are the only outputs | DERIVED (structure); reproduces "R=c/H0 at rho_crit" NATIVELY, no import |
| P7 | H0/rho_crit are OUTPUTS (order-correct), never inputs | discipline held; verified no import (see ATTACK) |
| **P8** | **absolute R_cell / H0 number needs the deferred finite-cell closure (coupled solve)** | **PINNING-DEFERRED (F5/scale-symmetry S8; determines-vs-relates open)** |
| P9 | (R/lambda_C)/sqrt(M_u/m) ∝ m^(3/2) -> no universal M-factor bridges particles | DERIVED (sympy exact, f7_bridge.py) — re-verifies step0 |
| P10 | depth |phi0|~0.8 vs needed ~92 -> dilation depth ~115x short for the ~10⁴⁰ | DERIVED (f7_bridge.py) — re-verifies step0 |
| P11 | cosmic->particle gap = absence of a native per-particle discrete-size selector | STATED (the irreducible open half) — not closed |

---

## ATTACK HERE (for a blind verifier)

1. **Did I re-import H0 / rho_crit anywhere?** Check: the only appearance of an observed H0 is
   in f7_h0.py as a back-solved COMPARISON target ("if R=c/H0 then M=..."), used in NO
   derivation. The native content (M/R=c²/2G; H_eff·R=c; M=Rc²/2G) uses only {z_CMB-depth, c, G,
   the critical condition}. Confirm rho_crit=3H0²/8πG never enters as an input — it only appears
   as the LCDM statement we DECLINE to import, recovered as an OUTPUT relation.
2. **Is the H0 an OUTPUT or a disguised input?** The claim is: native theory outputs the
   *relation* H_eff·R=c (derived from c²=2GM/R) and the cosmic *order*, but NOT the number
   (R_cell is the unpinned modulus). Attack: is there a hidden length smuggled in that secretly
   pins R? Confirm {c,G,dimensionless 7.004} cannot build a length (dimensional proof) — so no
   number can be claimed without a 3rd dimensionful input or the closure solve.
3. **The flat-modulus claim (P5).** Re-derive that c²=2GM/R pins only the ratio and that
   {R,M} is a genuine one-parameter family. Confirm the depth 7.004 (dimensionless) cannot pin
   R without the finite-cell closure tying depth->length.
4. **The m^(3/2) killer (P9).** Independently recompute (R/lambda_C)/sqrt(M_u/m); confirm m^(3/2),
   not constant — the universality-killer.
5. **Depth shortfall (P10).** ln(10⁴⁰)≈92 vs |phi0|~0.8; confirm ~115x exponent shortfall, no
   re-reading of the depth closes it without invention.
6. **Bridge unchanged by scale-symmetry (B.3).** Confirm the bootstrap reaches only the cosmic
   curvature length and leaves the ~10⁴⁰ ratio untouched (consistent with step0 from two
   directions).

---

## NET (for the ledger)

**F7 cosmic-scale half — NATIVE-ANCHORED (import removed).** The smuggled "4.46 Gpc = c/H0 at
rho_crit" is gone. Native replacement: {z_CMB via 1+z=e^phi -> phi_seal=7.004} + {c,G} + the
critical condition c²=2GM/R fix the cosmic cell's COMPACTNESS (M/R=c²/2G, exact) and depth
(7.004), and OUTPUT the effective-expansion relation H_eff·R=c — order-correct for the observed
H0 with NO import and NO tuning. The absolute SIZE / H0 number is the dilatation modulus,
UNPINNED by the law alone; pinning it is the deferred finite-cell closure (determines-vs-relates).
**H0-as-output verdict: PASSES at form + order of magnitude; the number is pinning-deferred.**

**F7 cosmic->particle half — IRREDUCIBLE OPEN GAP, now stated cleanly.** M alone does NOT bridge
(no universal M-factor; sqrt(M_u/m) carries m^(3/2); dilation depth ~115x short for the ~10⁴⁰).
The irreducible open question: what makes particle-scale cells spectrally autonomous from the
Gpc domain — i.e. the absence of a native per-particle DISCRETE-SIZE SELECTOR, with the two
trivial routes (depth, cosmic bootstrap) PROVEN insufficient. The scale-symmetry result set the
COSMIC scale only and does NOT change this. Not to be closed now; STATED so it stops being vague.

---

## VERIFICATION (2026-06-21) — blind re-import pass, agent a02dcf67f85280c2e
VERDICT: CLEAN (no re-import). (A) M/R=c^2/2G is genuinely native ({c,G} only, no z/H0). The dimensional
no-length proof is SOUND (c^a G^b = length has EMPTY solution set; a 3rd dimensionful input is required) => the
absolute size R_cell (the H0 NUMBER) is genuinely UNPINNED/non-derivable, hence NOT a hidden import. Observed H0
appears ONLY as a back-solved comparison TARGET, in NO derivation (every native eqn consumes only
{phi_seal-depth, c, G, critical condition}); rho_crit enters nowhere as input. The imported-Hubble smuggle is
genuinely REMOVED; "H0-as-output PASSES at form+order, number pinning-deferred" is honest (not tuned). (B) Bridge
re-verified: factor carries m^{3/2} (probe-dependent, sympy-exact); depth shortfall ln(1e40)/0.8 = 115x confirmed
-> the cosmic->particle gap is honestly IRREDUCIBLE-OPEN, stated cleanly. CLEAN.
