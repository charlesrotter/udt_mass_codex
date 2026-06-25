# Provenance of the Theta(core)=m*pi boundary condition — DERIVED or SKYRME IMPORT? — Results

Date: 2026-06-18. Driver: Claude (Opus 4.8, 1M context). NEW file
(append-never-edit). Mode: **OBSERVE / forensic AUDIT** (committed objects only,
quoted with file:line; nothing reconstructed from memory; nothing committed
changed). **DATA-BLIND** — no particle mass, ratio, or wall number loaded,
computed, or compared. Blind verifier: **PENDING** (ATTACK HERE block at end).

THE CRUX (handed down by the carrier audit, `fourth_component_sourced_results.md`
verifier verdict 2026-06-18, agent b7e3a4f0c1d29856, lines 219-234): the
S^2-vs-S^3 carrier question reduces to ONE upstream crux — the PROVENANCE of the
particle catalog's boundary condition `Theta(core)=m*pi, Theta(seal)=0`. Is that
BC DERIVED from UDT's own structure (seal/junction/core/topology), or is it a
SKYRME IMPORT (the pi_3 baryon convention) asserted without UDT-derivation? This
audit answers that, plus the decisive fork: is the catalog's m=1,2,3 distinctness
carried by the NATIVE pi_2 angular winding or the suspect pi_3 radial sweep?

Scripts: NONE were needed — the question is settled by reading the committed
solvers and docs. (No `bc_`-prefixed scripts written; the evidence is textual
and exact, quoted below.) Nothing committed was modified.

---

## Q1 — WHAT IS "m" IN THE CATALOG?

The catalog index "m" is set by **TWO charges simultaneously** in the committed
3-D field, but the m-sector PROTECTION (what makes the sectors distinct, i.e. what
prevents m=2 relaxing to m=1) is carried by **(b) the RADIAL chiral profile
boundary value Theta(core)=m*pi**, NOT by the azimuthal winding and NOT by the
native pi_2 area-form degree.

Evidence:

- The 3-D field carries an AZIMUTHAL winding cos(m*psi) AND a radial sweep:
  `full3d_spectral.py:208-220`:
  > `# n = (sinTheta sin th cos(m psi), sinTheta sin th sin(m psi), sinTheta cos th, cosTheta)`
  > `# winding m in psi.`
  > `def field_n(G, Th, m=1): ... sps, cps = torch.sin(m*G.PSg), torch.cos(m*G.PSg)`
  This is a unit **4-vector** (n_4 = cosTheta) — the SU(2)/S^3 hedgehog.

- But the SEED that defines each sector is solved by the **1-D RADIAL** solver
  `spectral_radial_soliton.py`, which has **NO azimuthal/psi dependence at all**
  (the Theta-EL residual, `spectral_radial_soliton.py:96-109`, contains only r,
  Theta, Theta', a, b — no m and no psi). The ONLY place `m` enters the radial
  solver is the boundary row:
  `spectral_radial_soliton.py:141`:  `FT[0] = Th[0] - m*PI`
  `spectral_radial_soliton.py:142`:  `FT[-1] = Th[-1] - 0.0`
  So the seed's m-index is set ENTIRELY by the radial chiral-sweep endpoint
  `Theta(core)=m*pi` — the count of times Theta sweeps 0->pi radially.

- The sector PROTECTION is explicitly the radial BC, hard-pinned in the residual:
  `winding_catalog_map.py:12-13`:
  > `This is a TOPOLOGICALLY-PROTECTED seed: an m=2 config cannot relax to m=1`
  > `because the Theta winding BC (core=m*pi, seal=0) is hard-pinned in the residual`
  `full3d_spectral.py:49-50` (header):
  > `winding BC Theta(core)=m*pi, Theta(seal)=0`

So "m" = (b) the radial chiral profile boundary value Theta(core)=m*pi. This is a
**pi_3 / Skyrme-baryon** quantity (radial sweep count), NOT (c) the pi_2 area-form
degree, NOT (a) the azimuthal winding alone (the radial seed has none).

---

## Q2 — THE EXACT Theta BOUNDARY CONDITIONS

Every committed solve imposes DIRICHLET ends on the chiral profile, with the CORE
value scaling as m*pi and the SEAL value pinned to 0:

- Radial spectral solver (the seed generator):
  `spectral_radial_soliton.py:141-142`:
  `FT[0] = Th[0] - m*PI`   (core, r[0])
  `FT[-1] = Th[-1] - 0.0`   (seal, r[-1])
  `spectral_radial_soliton.py:38` (header): `Theta(core)=m*pi, Theta(seal)=0  (winding BC)`

- The full 3-D batched engine:
  `complete_metric_batched.py:101`:
  > `... Dirichlet ends Th(core)=m*pi, Th(seal)=0. ... BC Theta(core)=m*pi,`
  > `Theta(seal)=0 (charge-m hedgehog, unwound at seal).`

- The analytic 3-D winding seed:
  `winding_catalog_map.py:65`: `Th = m*PI * 0.5*(1.0 + np.cos(PI*x))  # m*pi at core, 0 at seal`

- The Stage-B complete-action sweep is hardwired at m=1 (NO `m*` factor): it scans
  (kappa8, depth p, seed) at FIXED Theta(core)=pi:
  `complete_metric_sweep_stageB.py:83`: `Th[:, 0] = PI; Th[:, -1] = 0.0`
  (i.e. Stage-B did NOT produce the m-catalog; it found "exactly 1 distinct stable
  type", `complete_metric_sweep_stageB_results.md:126,206-208`. The m=1,2,3 catalog
  came from `winding_catalog_map.py` varying the radial BC m*pi.)

So it is `Theta(core)=m*pi` (core value SCALES with m), `Theta(seal)=0` (fixed),
with the azimuthal m varying in lockstep in the 3-D field — but the radial BC alone
carries the sector label.

---

## Q3 — PROVENANCE OF THE CORE BC (the crux)

### 3a. The seal / junction / mirror-fold derivation does NOT demand a Theta value.

The committed seal/junction derivation (dpf, dpf2, w6/w7, the same-minus crease,
the transgression) constrains ONLY the METRIC/DILATION fields, never the matter
chiral angle Theta(r):

- The crease/junction count is over the METRIC angular amplitude (the c-driven
  g_Ttheta channel), via parity of harmonics across the fold:
  `dpf2_results.md:96-104` (n_odd(L)=L is a count of Dirichlet rows on the
  METRIC field, not on Theta).
  `dpf2_junction.py:73-80` (the derived junction count is on the metric mode).

- The transgression that delivers content "at the seal" is the METRIC Misner-Sharp
  charge, NOT the matter Theta. NAMING-COLLISION WARNING resolved:
  `dpf_derive.py:118-121`:
  > `The transgression Theta=(ln f)omega_H1 is EXACT, so by Stokes its ENTIRE`
  > `content is the boundary value at the seal: D = 4pi (ln f)_seal.`
  Here the uppercase "Theta" is the transgression **2-form** Θ = (ln f)·omega_H1
  (a metric-dilation charge built from the area form), delivering D = 4pi(ln f)_seal
  — a statement about the DILATION f at the seal, NOT about the matter angle
  Theta(r). The matter chiral angle never appears in the seal derivation.

- The seal/junction derivation's own boundary conditions are all metric/gauge:
  a(seal)=0 (additive gauge), b(core)=-p (depth dial). `spectral_radial_soliton.py:37,135`.

Conclusion 3a: the seal does NOT derive Theta(core)=m*pi. (Independently confirmed
by a full sweep of all seal/junction docs this push: no committed text derives the
Theta endpoints from seal/fold physics; the seal pins metric/dilation only.)

### 3b. Core regularity does NOT force it on the committed cell.

The strict-origin (r->0) regularity argument WOULD force a sweep (the L4 texture
energy kappa/(2r^2) is non-integrable at r=0), but the committed cell seals at a
FINITE inner radius:
- `complete_metric_sweep_stageA.py` rc=0.05 is tagged literally **[CHOSEN]**
  (a numerical/grid cutoff, "cell size FREE dimensionful input #39"), per
  `fourth_component_sourced_results.md:204-211` (blind-verified). CANON
  C-2026-06-10-2 puts the matter core at phi->-inf, which the finite-depth
  (p~0.4-0.8) committed solves never reach. So r_core=0.05 is NOT a derived seal
  radius; "does the cell reach r=0?" is UNRESOLVED. A numerical cutoff cannot
  settle the regularity case either way.

Conclusion 3b: on the actual committed (finite-r_core) cell, regularity does NOT
force Theta(core)=m*pi. (If the physical cell does reach r=0, regularity WOULD
force the sweep — but that is an open physical question, not a committed derivation.)

### 3c. It IS stated as a Skyrme-baryon / hedgehog CONVENTION — verbatim.

The BC is asserted as the topological-charge winding convention, with the field
explicitly named the SU(2)/S^3 Skyrme hedgehog:
- `matter_ansatz_derive.py:28`:
  > `CANDIDATE ANSAetze tested (all degree-1, charge fixed by Theta(core)=pi->Theta(seal)=0):`
- `matter_ansatz_derive.py:31-32`:
  > `S3_skyrme  : n4 = (sinTh sinth cosps, sinTh sinth sinps, sinTh costh, cosTh)`
  > `[|n4|=1, the SU(2)/S^3 chiral Skyrme hedgehog]`
- `spectral_radial_soliton.py:20`: `Matter = unit-S^3 hedgehog, winding m=1, profile Theta(r).`
- `spectral_radial_soliton.py:35`: `R_Th = Theta-EL (unit S^3 Euler-Lagrange)`

And — the load-bearing self-assessment — the project's OWN premise ledger TAGS the
endpoints as a CHOICE, not a derivation:
- `native_stabilizer_results.md:244-249` (the **CHOSE** section):
  > `- Charge-1 BC Theta(core)=pi, Theta(seal)=0 (the omega_H1 winding=1 carrier)`
  > `  [derived as the N=3/q=1/3 carrier; the specific pi->0 endpoints are the`
  > `  charge-1 hedgehog choice].`
  The "[derived as the N=3/q=1/3 carrier]" parenthetical refers to omega_H1 (the
  area-form / pi_2 charge) being the canonized native carrier — a GENUINE
  derivation. But the radial ENDPOINTS pi->0 (and their m*pi generalization) are
  tagged "the charge-1 hedgehog **choice**" — i.e. CHOSEN, not derived.

Conclusion 3c: the core BC is ASSERTED as the Skyrme/hedgehog winding convention,
and is self-tagged CHOSE in the premise ledger. No committed object DERIVES it.

---

## Q4 — WHAT DOES THE NATIVE pi_2 CHARGE ACTUALLY REQUIRE?

The native canonized charge is the H1 area form (CANON C-2026-06-14-1,
`CANON.md:121-122`):
> `omega_H1 = eps_abc n_a dn_b ^ dn_c (the same object carrying N=3, q=1/3)`

This eps_abc current uses **exactly 3 components** (a,b,c in {1,2,3}) and is
STRUCTURALLY BLIND to n_4 (`fourth_component_sourced_results.md:98-103,238-239`,
both constructor and blind verifier agree, BANKED). Its degree is the degree of the
(theta,ps) -> S^2 map — the ANGULAR winding. It requires NO condition on the radial
profile Theta(r):
- CANON itself, `CANON.md:138-141`: the pure topological n=x/r (Theta independent
  of r) "is exact everywhere"; a radial twist Theta=Theta(r) is the realized-soliton
  DRESSING (it softens the EOS), not the charge carrier.
- `fourth_component_sourced_results.md:90-94`: "the sweep is required ONLY for the
  pi_3 (S^3 baryon) charge. The pi_2 degree (S^2, omega_H1) is carried by the
  (theta,ps) winding ALONE." So `Theta(core)=m*pi` is EXTRANEOUS to the pi_2 charge.

NUANCE (from the blind verifier, `fourth_component_sourced_results.md:188-191,212-217`):
Theta==pi/2 (n_4=0, the pure S^2 representative) solves the EOM only as a CONSTANT;
the charge-1 ENERGY MINIMIZER under the committed BC Theta(core)=pi DOES sweep
(E=1.75 swept vs 24.0 flat). But that minimization ASSUMES the Theta(core)=pi BC —
which is exactly the pi_3 import under audit. So: the native pi_2 charge does NOT
require any Theta(r) condition; the Theta sweep is an energetic preference ONLY ONCE
the pi_3 baryon BC has been imposed (circular as a justification for that BC).

---

## Q5 — THE DECISIVE FORK

**The catalog's m=1,2,3 distinctness is carried by (ii) the RADIAL chiral-sweep
count Theta(core)=m*pi — a pi_3 / Skyrme-baryon quantity, provenance-suspect — NOT
by (i) the native pi_2 area-form / azimuthal winding.**

Code evidence:
- The seed generator `spectral_radial_soliton.py` is purely radial (no psi); its
  ONLY m-dependence is `FT[0]=Th[0]-m*PI` (line 141). So a sector's identity is the
  radial sweep count.
- The sector PROTECTION ("m=2 cannot relax to m=1") is attributed explicitly to
  the radial BC hard-pinned in the residual (`winding_catalog_map.py:12-13`), NOT
  to the azimuthal winding.
- The native eps_abc/omega_H1 (pi_2) charge is blind to n_4 and set by the angular
  map alone; varying Theta(core)=m*pi changes the RADIAL (pi_3) count, a different
  charge. The blind verifier already stated this:
  `fourth_component_sourced_results.md:193-196`:
  > `the m=1,2,3 CATALOG is indexed by Theta(core)=m*pi, the chiral-SWEEP`
  > `(pi_3-type baryon) count, NOT the pi_2 area-form degree`

Implication (per the fork as posed): the catalog's very type-LABELS depend on the
imported baryon BC. The native pi_2 family (if it carries an m-index at all) would
be indexed by the azimuthal/angular winding, which the committed catalog did not
independently vary or protect.

---

## VERDICT

### (B) The core BC `Theta(core)=m*pi` is a SKYRME IMPORT — asserted, not UDT-derived.

Steelman of "derived" attempted and FAILED on all three candidate routes:
1. SEAL/JUNCTION (3a): derives metric/dilation boundary data only (the c-driven
   Dirichlet count, the transgression D=4pi(ln f)_seal); never touches the matter
   chiral angle Theta. NOT a source of the Theta BC.
2. CORE REGULARITY (3b): would force a sweep only at strict r=0, but the committed
   cell seals at a [CHOSEN] finite r_core=0.05; the physical r=0 question is OPEN.
   NOT a derivation on the committed geometry.
3. STATED-AS-CONVENTION (3c): the BC is explicitly written as the SU(2)/S^3 chiral
   Skyrme hedgehog winding (`matter_ansatz_derive.py:28,31-32`;
   `spectral_radial_soliton.py:20,35,38`) and is SELF-TAGGED "CHOSE / the charge-1
   hedgehog choice" in the premise ledger (`native_stabilizer_results.md:244-249`).

What IS genuinely derived (do not over-correct): the NATIVE angular charge —
omega_H1 = eps_abc area form, N=3, q=1/3 (CANON C-2026-06-14-1) — is a real UDT
derivation. It is a pi_2 / S^2 object, blind to n_4, and requires NO radial Theta
condition. The IMPORT is specifically the RADIAL endpoints `Theta(core)=m*pi ->
Theta(seal)=0` (the pi_3 baryon winding number), which the catalog grafted on as
the sector index without UDT derivation.

### m=1,2,3 discreteness: carried by the SUSPECT pi_3 radial sweep, not the native pi_2 winding.

The catalog's distinct types are indexed and topologically protected by the radial
chiral-sweep BC Theta(core)=m*pi (pi_3 / baryon), confirmed in code. The native
pi_2 angular winding (the canonized omega_H1) is a different charge and was not the
catalog's distinguishing label. Per the fork: this is case (ii) — the catalog's
type-labels depend on the imported baryon BC.

### CONDITIONAL CLAUSE (stated exactly, mirrors the carrier audit's open question):
The import verdict is conditional on the committed finite-cell geometry
(r_core>0, the [CHOSEN] 0.05 cutoff). IF the physical UDT matter cell reaches the
strict origin r=0 (CANON C-2026-06-10-2's phi->-inf core), the L4 texture energy
divergence WOULD force a regularizing sweep Theta(0)=pi, sourcing the BC by
regularity — which would make Theta(core)=pi DERIVED (for m=1) by core regularity,
not imported. The committed solves never reach r=0; so under the ACTUAL committed
cell geometry the BC is an import. The S^2-vs-S^3 carrier therefore still reduces to
the single open physical fact: **does the matter cell reach r=0, or seal at finite
r_core?** This audit confirms the BC is NOT derived from the seal/junction (the one
UDT structure that might have supplied it independently of r=0), narrowing the open
question to core regularity alone.

DURABLE FINDINGS (banked):
- The native charge current eps_abc/omega_H1 is genuinely pi_2 / S^2 and blind to
  n_4 (CANON + two prior agents).
- The seal/junction derivation constrains metric/dilation only; the "transgression
  Theta" in dpf_derive.py is the metric 2-form, NOT the matter angle (naming
  collision, resolved here).
- The catalog's m-sector index = radial sweep Theta(core)=m*pi (pi_3), set by a
  1-D radial solver with no azimuthal content; the azimuthal cos(m*psi) rides along
  in the 3-D field but does not define the protected sector.
- The premise ledger already self-tags the endpoints "CHOSE / hedgehog choice."

---

## BLIND VERIFIER — PENDING. ATTACK HERE:

1. **Re-confirm "m" lives in the radial BC, not the angular winding.** Independently
   read `spectral_radial_soliton.py` and confirm the ONLY m-dependence in the radial
   solver is `FT[0]=Th[0]-m*PI` (line 141) and that the Theta-EL residual (lines
   96-109) and stress (lines 65-73) contain no m and no psi. If you find m entering
   the radial dynamics anywhere else, the Q1/Q5 verdict changes.

2. **Hunt a SEAL derivation of Theta I missed.** Search every dpf/dpf2/w6/w7/junction
   object for ANY committed line where the seal/fold/transgression DERIVES the matter
   chiral-angle Theta endpoints (not the metric/dilation, not the transgression
   2-form Θ=(ln f)omega_H1). If one exists, route (3a) is wrong and the verdict
   moves toward DERIVED. Confirm the dpf_derive.py:118 "Theta" is the 2-form, not the
   matter angle (check its definition and units).

3. **Attack the premise-ledger quote.** Verify `native_stabilizer_results.md:244-249`
   actually tags the pi->0 endpoints as CHOSE (not derived), and that the
   "[derived as the N=3/q=1/3 carrier]" parenthetical attaches to omega_H1 (the
   angular charge), NOT to the radial endpoints. If the endpoints are in fact tagged
   DERIVED elsewhere with a real derivation, exhibit it.

4. **Attack the r=0 conditional.** Is r_core=0.05 genuinely [CHOSEN] (a numerical
   cutoff) in `complete_metric_sweep_stageA.py`, or is there a committed derivation
   fixing the inner radius (which would let core regularity DERIVE Theta(core)=pi)?
   Independently check whether any committed solve reaches phi->-inf / r->0.

5. **Targeting check.** Was "IMPORT" reached by finding the absence of a derivation,
   or steered to a desired answer? Confirm no S^2/S^3 result was assumed to force the
   verdict. Verify the steelman of "derived" (all three routes 3a/3b/3c) was
   genuinely attempted before concluding import.

6. **Charge-current cross-check.** Confirm the native eps_abc current
   (`CANON.md:121`, `native_skyrme_derive.py`) is 3-component and that varying
   Theta(core)=m*pi changes the RADIAL winding (a pi_3-type count), NOT the eps_abc
   (pi_2) degree — i.e. that the catalog's m is the suspect charge, not the native
   one.

---

## BLIND VERIFIER VERDICT — 2026-06-18 (verifier agent ae844999686082572)

**STANDS-CONDITIONALLY** — conditional only on the same honestly-flagged open
fact (does the physical cell reach r=0?), and the verifier STRENGTHENS the import
verdict. Independent re-trace of all six axes from primary committed sources (no
reliance on the audit's scripts).

- Axis A (structural core) CONFIRMS: catalog m-index is the radial BC FT[0]=Th[0]-m*PI
  (spectral_radial_soliton.py:141); the Theta-EL residual + stress contain no m, no
  psi; sector protection is attributed to that hard-pinned radial BC; azimuthal
  cos(m*psi) rides along but does NOT define the protected sector.
- Axis B (steelman "derived") CONFIRMS no derivation: seal/junction/transgression
  constrain metric/dilation only; the dpf_derive.py:118 transgression "Theta" is the
  metric 2-form (ln f)*omega_H1 (naming collision, NOT the matter angle); the L4
  derivation is genuine but silent on radial endpoints. Self-tagged CHOSE in TWO
  places (native_stabilizer_results.md:244-249 AND radial_Bfree_soliton_results.md:164).
- Axis C SHARPENS (audit was too GENEROUS to "derived"): the committed regularity
  script (fourth_component_regularity_energetics.py:40-110) shows r=0 regularity
  forces only sin(Theta(0))=0 -- a NODE condition satisfied by Theta(0)=0,pi,2pi,3pi
  equally. It selects NEITHER the value NOR the m-ladder. So even IF the cell reaches
  r=0, regularity does NOT derive Theta(core)=pi for m=1, and gives nothing for m=2,3.
  The import verdict for the m>=2 catalog labels is ROBUST even in the r=0 limit.
- Axis D CONFIRMS: native pi_2 charge (omega_H1, eps_abc 3-component) needs NO radial
  Theta condition; pure n=x/r (Theta=pi/2) carries degree-1 (CANON.md:138-141).
- Axis E (targeting) clean: IMPORT reached by genuine absence-of-derivation; one
  UNDERSTATEMENT found (the r=0->m=1 generosity above), no overstatement.

NET BANKED: the m=1,2,3 winding-catalog discreteness is indexed by the imported
radial Skyrme BC Theta(core)=m*pi (self-tagged CHOSE), NOT by UDT's native pi_2
area-form/angular-degree charge. The seal/junction (the only other candidate UDT
source) does NOT supply it. The native pi_2 charge quantization (N=3, q=1/3, CANON
C-2026-06-14-1) STANDS and is untouched. OPEN: (a) does a native catalog of distinct
types come from the pi_2 area-form degree with Theta FREE (unsolved -- next push);
(b) does the cell reach r=0 (does NOT rescue the m-ladder even if yes, per Axis C).
