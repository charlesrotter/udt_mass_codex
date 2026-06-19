# Does Honest-UDT (f(phi)R Gravity Sector) Still Reduce to GR at Lab / Terrestrial / Solar-System Scales?

**Mode:** OBSERVE / consistency-test (CLAUDE.md "How we work"). This question can
FALSIFY the new gravity-sector result; I did NOT protect it. Report WHAT IS THERE.
**Constructor:** Claude Opus 4.8 (1M), agent for udt_mass_codex, **2026-06-18**.
**Scripts (new, this push, nothing committed):**
`gravity_local_c1_vs_fphiR.py`, `gravity_local_ppn_solve.py`,
`gravity_local_ppn_direct.py`, `gravity_local_gamma_readoff.py`,
`gravity_local_kinetic_escape.py`.

The NEW result under test: `udt_gravity_sector_rederivation_results.md` +
`gravity_sector_verifier_independent_results.md`. Honest field equation
`f(phi) G_mn + (g_mn box - nabla_m nabla_n) f(phi) = (1/2) T_mn`,
`f(phi)=c0^4 e^{-8phi}/(16 pi G)`, scalar-tensor / Brans-Dicke-type; vacuum != GR;
conformal kinetic coeff 96.

---

## HEADLINE FINDING (the make-or-break, stated up front)

**The new honest f(phi)R gravity sector DOES NOT reduce to GR at solar-system
scales. Worked weak-field PPN: gamma = 9 (not 1), an O(1) UNSUPPRESSED departure
that violates the Cassini bound |gamma-1| < 2.3e-5 by a factor ~3.5e5. By the
honest f(phi)R equations, light bending around the Sun would be 5x the GR value.
This is a FALSIFICATION — but of the f(phi)R ACTION, NOT of UDT.**

The reason it is not a falsification of UDT: **the corpus's VALIDATED gravity
sector (udt_validated_results.md §240) does NOT use the f(phi)R Einstein-Hilbert
action at all.** It uses the C1 PURE-KINETIC scalar action, whose vacuum is
Schwarzschild EXACTLY and which passes PPN (gamma=beta=1). And §240.4 **explicitly
RULED OUT** the `F_R(phi)R` form (candidate C2) and the Einstein-Hilbert `f(R)`
form (candidate C4) precisely because they fail. So the new re-derivation's
premise A1 ("the Einstein-Hilbert R-term is the native starting point"), which it
honestly flagged as an UNRESOLVED possible Principle-7 smuggle, is the load-bearing
fault line: **A1 is not just unresolved — the corpus already TESTED and REJECTED
the EH/`F_R(phi)R` action class, and the Cassini violation computed here is exactly
why.**

So the consistency test cuts BOTH the new result and the old one into sharp focus:
- If the native gravity action is **f(phi)R** (new doc's A1): vacuum != GR (new
  doc correct) **but solar-system tests FAIL (this doc)** -> that action is ruled
  out by Cassini, independently re-deriving §240.4's rejection of C2/C4.
- If the native gravity action is **C1 pure-kinetic** (corpus §240): vacuum =
  Schwarzschild exactly, PPN passes — **but then the new doc's "vacuum != GR" does
  not apply to UDT's actual gravity sector.** The new doc tested an action UDT
  does not use.

The two are DIFFERENT THEORIES. The whole question reduces to: **which action is
UDT's native gravity sector — and is THAT settled honestly?** (See §D.)

---

## A. Does UDT source phi LOCALLY (Sun/Earth) or is phi the cosmological depth field only?

**ANSWER: BOTH, in two architecturally-distinct sectors — and the gravity sector
DOES source phi from local mass.** This matters because it puts UDT squarely in
regime (b) of the task: a local mass digs a local phi-well with a local gradient,
so the Brans-Dicke-type term IS active around the Sun. There is no "phi is locally
constant so the new terms vanish" escape.

Corpus evidence (citations to `udt_validated_results.md` = VR,
`udt_canonical_geometry.md` = CG):

1. **Gravity sector: phi is locally sourced, exactly Schwarzschild.**
   The C1 vacuum field equation `phi'' + (2/r)phi' - 2 phi'^2 = 0` is "Newton's
   potential equation in disguise" — substituting `u=e^{-2phi}` gives 3D Laplace
   `u''+(2/r)u'=0`, `u=A+B/r`, and `B=-r_S` gives the Schwarzschild well
   `e^{-2phi}=1-r_S/r`, `r_S=2GM/c^2` (VR §240.0, §240.2, lines 28196–28238).
   **A local mass M produces a local phi-gradient identical to Schwarzschild.**
   `M_ADM G/c^2 = r_S/2 = GM/c^2 > 0` (VR §240.3). PROVENANCE.md:27 founding
   intent: "At intermediate distances, such as terrestrial and solar this
   spacetime reduces to GR as a special case."

2. **Matter/galactic sector: phi sourced by baryon density** via a screened
   Poisson equation `(1/r^2)d_r(r^2 e^{-2phi} phi') - mu_g^2 phi = -4 pi G rho_bar/c^2`
   (VR §5.1, line 355). Note the kinetic prefactor `e^{-2phi}phi'` = the **C1**
   structure, NOT f(phi)R. At galactic/solar/lab scales `mu_g r ~ 1e-5`, the
   screening term is negligible, and `v^2 = G M_bar/r = v^2_Newton` exactly (VR
   §5.1, line 359). `mu_g = 0.2473 Gpc^-1`, derived, global (VR §219). Crossover
   to non-Newtonian only at `1/mu_g ~ 4 Gpc` (cosmological).

3. **Cosmological sector: phi NOT sourced by local matter** — a BC-determined
   polynomial scaffold, `phi(0)=0 -> phi(r_CMB)=7.004` over `r* = 9.164 Gpc`;
   "no physical matter Lagrangian required" (VR §12.12.20, §40; CG §22.3 line 4295).
   The observer is a test particle on this background (VR line 7446).

**Consequence for the test:** because the gravity sector DOES dig a local
Schwarzschild-type phi-well around the Sun/Earth (regime b), the `(g box -
nabla nabla)f` derivative-of-coefficient terms are sourced locally and are O(1)
in the solar-system field — they are NOT suppressed by sitting at fixed cosmic
depth. The cosmological-constancy escape (regime a) is unavailable.

---

## B. Weak-field / slowly-varying expansion and the LEADING local departure from GR

I expanded the honest f(phi)R vacuum equations (`udt_gravity_sector_rederivation_results.md` §2)
two complementary ways. Both say the departure is O(1) and unsuppressed.

### B1. Order-counting in the field amplitude (script `gravity_local_c1_vs_fphiR.py`)
Writing phi = eps·P(r) and expanding the honest tt-equation numerator:
```
honest:  72 eps^2 r^2 P'^2  - 8 eps r^2 P'' - 18 eps r P' - 2 eps P  (+ O(eps^2 P^2))
GR bare: -2 eps r P' - 2 eps P
DIFFERENCE (honest-GR) = -8 eps r^2 P'' - 16 eps r P' + 72 eps^2 r^2 P'^2
```
The leading correction is **O(eps), LINEAR in phi** (coefficients -8 and -16 vs
GR's -2), NOT a gradient-squared O((phi' L)^2) suppression. (For a Schwarzschild
1/r profile the tt-linear piece happens to cancel and the tt residual is O(eps^2);
but the rr-equation keeps a linear O(eps) survivor — see B2 — and the metric must
satisfy both.)

### B2. Direct PPN gamma from the linearized metric (scripts `gravity_local_ppn_direct.py`,
`gravity_local_gamma_readoff.py`) — the load-bearing computation.
Metric `g_tt=-A c0^2, g_rr=B`, `A=1+alpha/r, B=1+beta/r`, phi SLAVED `phi=-1/2 ln A`,
`f=c0^4 A^4/16 pi G`. Built G^mu_nu, box f, nabla nabla f from scratch in sympy,
linearized, solved the two independent vacuum equations:
```
GR (Emix=0):         alpha = -beta        ->  gamma = -beta/alpha = 1     [validates the read-off]
HONEST f(phi)R:      alpha = -beta/9      ->  gamma = -beta/alpha = 9
```
PPN read-off convention `g_tt=-(1-2U), g_rr=1+2 gamma U`:
```
gamma_UDT(f(phi)R) = 9
|gamma - 1| = 8        Cassini bound 2.3e-5  ->  violated by 3.5e5 x
light bending = (1+gamma)/2 = 5 x GR  ->  8.76 arcsec vs measured 1.7517 +/- 1.1e-5e
```
The GR cross-check in the same machinery returns gamma=1 exactly, validating the
read-off. **Order of magnitude of the leading local departure from GR:
O(1) in the PPN coefficients — specifically gamma off by 8.**

### B3. Why not the textbook Brans-Dicke gamma=1/2? (script `gravity_local_kinetic_escape.py`)
Standard BD with conformal kinetic coeff 96 has omega=0 and gamma=(1+omega)/(2+omega)=1/2.
The SLAVED UDT computation gives gamma=9 instead, because phi is tied to g_tt
(phi=-1/2 ln g_tt), not an independent DOF — a genuinely different theory from
textbook BD. **Either value is O(1) away from 1; both fail Cassini.** The only way
to reach gamma=1 is omega -> infinity, i.e. ADD an explicit bare scalar kinetic
term `X(dphi)^2` with X dominating the conformal 96 by > ~40000. That term is NOT
in the f(phi)R action (premise A6); adding it to rescue Cassini would be a posited
mechanism (Principle 1 / hypothesis discipline).

---

## C. VERDICT

> **NO — the honest f(phi)R gravity sector does NOT reduce to GR at lab /
> terrestrial / solar-system scales. It predicts PPN gamma = 9 (light bending 5x
> GR), violating Cassini by ~3.5e5. This FALSIFIES the f(phi)R action as UDT's
> gravity sector.** The new terms are NOT suppressed locally: the gravity sector
> sources phi from local mass (A), so the (g box - nabla nabla)f terms are O(1) in
> the solar-system field, and the departure enters at leading (linear) order in
> phi (B), not at gradient-squared order.

> **BUT this is NOT a falsification of UDT.** UDT's actual validated gravity sector
> is the **C1 pure-kinetic action** (VR §240), whose vacuum is Schwarzschild
> EXACTLY (`phi''+(2/r)phi'-2phi'^2=0` solved by phi=-1/2 ln(1-r_S/r), residual = 0,
> script `gravity_local_c1_vs_fphiR.py` confirms) and which passes PPN
> (gamma=beta=1, Mercury 42.98"/cy, Cassini 1.7504"). The corpus §240.4 **already
> RULED OUT** the `F_R(phi)R` (C2) and Einstein-Hilbert `f(R)` (C4) action classes.
> **The Cassini violation computed here is an independent re-derivation of WHY
> §240.4 rejected those classes.**

> **THEREFORE the real status is DEPENDS-ON the native-gravity-action question
> (premise A1 of the new doc), and the two results are about TWO DIFFERENT
> ACTIONS:**
> - The new doc's "vacuum != GR / Brans-Dicke-96 / Schwarzschild fails" is CORRECT
>   **for the f(phi)R action** — and this doc shows that same action ALSO fails
>   solar-system tests. Consistent: f(phi)R is simply not a viable gravity sector.
> - UDT's actual gravity sector (C1 kinetic) gives vacuum = Schwarzschild AND
>   passes PPN. For C1 there is no (g box - nabla nabla)f term (it is not an EH
>   action), so the new doc's modification **does not apply to UDT's real gravity
>   sector.**

**The tension to resolve (for Charles / PONDER):** Charles's Principle 7
suspicion was that defaulting to GR's R-term smuggled GR back in. The honest
re-derivation vindicated that *the variation had been done dishonestly* IF the
action is f(phi)R. But the corpus's gravity sector is NOT f(phi)R — it is C1, an
action UDT *chose by an admissibility argument* (§240.1) precisely to get
Schwarzschild + PPN. So the live question is no longer "did dropping (g box -
nabla nabla)f hide a GR-departure" — it is **"is the C1 admissibility argument
(§240) itself a Principle-7 smuggle that engineered GR-recovery, or is C1 genuinely
the native action?"** The new f(phi)R re-derivation does not settle this; it shows
the OTHER branch (EH/f(phi)R) is Cassini-dead, which is consistent with §240
having discarded it. UDT survives Cassini **only on the C1 branch.**

---

## D. PREMISE LEDGER (chose vs derived) + does the answer hinge on local-phi-sourcing?

| # | Premise | Status | Effect on verdict |
|---|---|---|---|
| L1 | Gravity sector sources phi from local mass (Sun/Earth -> Schwarzschild well) | **DERIVED** (VR §240.2, C1 vacuum = Schwarzschild) | Kills the "phi locally constant" escape -> for f(phi)R the new terms ARE active locally. |
| L2 | f(phi)R action with f=c0^4 e^{-8phi}/16piG (the new doc's A1+A2) | **CHOSE / UNRESOLVED** (new doc A1, flagged possible Principle-7 smuggle) | THE hinge. If this is the native action -> Cassini FAIL (gamma=9). If not -> not UDT's sector. |
| L3 | C1 pure-kinetic action is UDT's actual gravity sector | **DERIVED-BY-ADMISSIBILITY** (VR §240.1 uniqueness within analytic classes) but the admissibility CONSTRAINTS (incl. "operational PPN consistency") are a CHOSE input | If C1 is native -> reduces to GR / PPN passes; f(phi)R modification N/A. |
| L4 | §240.4 ruled out F_R(phi)R (C2) and EH f(R) (C4) | **DERIVED** (corpus) | Independently corroborated here: those classes fail Cassini (gamma!=1). |
| L5 | phi SLAVED (phi=-1/2 ln g_tt) for the gamma=9 computation | **DERIVED** (B=1/A / metric structure) | gamma=9 (slaved) vs 1/2 (independent BD); BOTH O(1)!=1, verdict robust to this choice. |
| L6 | Static / spherical / diagonal / areal-r weak field | **CHOSE** (CANON C-2026-06-18-1 slice) | PPN is defined in exactly this regime; appropriate. A non-static/non-SSS dressing could in principle alter numbers but cannot remove an O(1) gamma deviation without a new mechanism. |
| L7 | No added bare scalar kinetic term in f(phi)R action (new doc A6) | **CHOSE** | Adding X(dphi)^2 with X >~ 40000*64 could force gamma->1, but that is an imported mechanism (Principle 1). |
| L8 | Cassini |gamma-1|<2.3e-5, light-bending 1.7517"+/-1.1e-5 | observational input | Standard. |

**Does the answer hinge on local-phi-sourcing? YES, but the hinge resolves
AGAINST f(phi)R either way.** Because phi IS locally sourced (L1), the f(phi)R
modification is locally active and fails Cassini. Were phi instead purely
cosmological (locally constant), the f(phi)R new terms would vanish locally and it
would reduce to GR trivially — but the corpus is explicit (A) that the gravity
sector sources phi locally as Schwarzschild, so that escape is closed. The DEEPER
hinge is L2 vs L3: **which action is native.** UDT passes Cassini on the C1 branch
and fails it on the f(phi)R branch. The new re-derivation's value is to have shown,
honestly, that the f(phi)R branch is both vacuum-non-GR AND solar-system-dead —
re-confirming §240.4 from a fresh direction and sharpening Charles's Principle-7
question onto the C1 admissibility argument itself.

---

## E. RECOMMENDED REGISTRY / CANON FLAGS (for Charles)

- **NEGATIVES_REGISTRY:** the f(phi)R / EH `F_R(phi)R` gravity action is
  CASSINI-FALSIFIED (gamma=9; |gamma-1|=8; light bending 5x), premise set =
  {f=c0^4 e^{-8phi}/16piG, no bare kinetic term, static-SSS weak field, phi slaved}.
  This corroborates VR §240.4 C2/C4 rule-outs.
- The new doc's flag that "bare-vacuum no-go's #62/#63 are CONDITIONS-CHANGED" is
  scoped to the f(phi)R action. Under the C1 (native, §240) action vacuum IS
  Schwarzschild, so #62/#63's "vacuum=GR/Schwarzschild" premise STANDS for C1.
  The CONDITIONS-CHANGED flag should itself be tagged "f(phi)R-branch only."
- **Open Principle-7 question (un-smuggled, for PONDER):** is the C1 admissibility
  argument (VR §240.1, which INCLUDES "operational PPN consistency" as an
  admissibility constraint) a legitimate native derivation, or did requiring
  PPN-consistency up front engineer GR-recovery? The honest re-derivation does NOT
  answer this; it only kills the competing EH branch. This is where the parent
  theory could still be sneaking in — at the CHOICE of admissibility constraints,
  not at the variation.
