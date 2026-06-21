# Re-grading UDT's Matter Sector on the Newly-Derived Gravitational Operator — Analytic OBSERVE

**Mode:** OBSERVE, METRIC-LED, DATA-BLIND (no mass/ratio/spectrum/catalog loaded or aimed at).
**Driver:** Claude Opus 4.8 (1M), agent for udt_mass_codex. **Date:** 2026-06-21. **NOT canon.**
**Compute:** CPU only, sympy 1.13.1, bounded analytic. No GPU, no heavy coupled solve, single process.
**Status:** UNVERIFIED (no blind verifier pass yet) — record-candidate, not banked.
**Scripts (new, /tmp, nothing committed):** `regrade_1_absorbability.py`, `regrade_2_conservation.py`,
`regrade_3_bianchi.py`, `regrade_3b.py`, `regrade_3c.py`, `regrade_4_exterior.py`, `regrade_5.py`,
`regrade_6_matterlaw.py`. All symbolic claims machine-checked unless tagged ANALYTIC.

Builds on (read this session): `native_dilation_weight_derivation_results.md` (the derived operator:
vacuum != GR, weight e^{2phi}, a(phi)=e^{+phi} DERIVED), `scale_symmetry_bootstrap_analysis_results.md`,
`branch_G/P_characterization_results.md`, `MATTER_SECTOR_MAP_new_foundation.md` (the MAP this executes),
`udt_matter_source_MAP_results.md` (the OLD absorbability result being re-graded),
`native_matter_step_results.md` (the committed soliton; M_MS=0.281), `angular_lagrangian_results.md`
(the OLD global-monopole exterior). `FOUNDATIONAL_ASSUMPTIONS_LEDGER.md` (F1, F3 — the entangled pair F0 flagged).

---

## 0. THE SHIFT BEING RE-GRADED (one paragraph, lay)

Every committed UDT matter result ran on the OLD gravity operator: standard Einstein vacuum (the
Einstein-Hilbert R-term, so empty space froze to Schwarzschild = "vacuum = GR") with matter that
dilates as a=-1 (so its weight on the source was exactly 1 = no departure). The old reassurance was:
"the scalar/matter weight can be ABSORBED into a renaming of the stress, so on the matter side UDT is
just GR — the weight does not physically matter." This session derived the corrected foundation: the
gravity action is two-player scalar-tensor `S_grav = INT sqrt(-g)[e^{2phi} R + X e^{2phi}(dphi)^2]`
with phi an independent field, so **vacuum != GR**; and the rest-mass coupling is DERIVED
**a(phi)=e^{+phi}** (NOT -1), with rest-mass weight e^{2phi} (NOT 1). The question: does the old
"absorbable -> UDT=GR on matter" survive, or does a(phi)=e^{+phi} now have TEETH?

---

## 1. THE OLD ABSORBABILITY ARGUMENT, AND EXACTLY WHERE IT BREAKS

The old proof (`udt_matter_source_MAP_results.md` Sec 2, blind-verified at the time) was a Bianchi
tautology and is RECORDED there as resting on premise **P2 = "Left side = STANDARD Einstein tensor
G_munu"**, self-flagged as **"THE smuggle-surface ... the genuinely native UDT left-hand-side law is
UNBUILT."** The argument, verbatim structure:

```
OLD operator:   G_munu = kappa0 e^{(a+1)phi} T_munu.
Define          T~_munu := e^{(a+1)phi} T_munu.   Then  G_munu = kappa0 T~_munu,
and             nabla^mu T~_munu = 0  IDENTICALLY,  because nabla^mu G_munu = 0 (contracted Bianchi).
=> T~ is a conserved source with a CONSTANT coupling => the system RELABELS to ordinary GR.
=> the weight (any exponent) is ABSORBABLE; the only non-removable departure is the dimensionless
   ruler ratio, which runs iff a != -1.  With a=-1: UDT = GR on the matter side.
```

**The single load-bearing step is `nabla^mu G_munu = 0` (contracted Bianchi for the EH tensor).**
That is what makes the relabeled source automatically conserved and hence absorbable. The native
left-hand-side law is now BUILT, and it is NOT the EH tensor. So the tautology must be re-tested.

---

## 2. THE NEW OPERATOR IS NOT DIVERGENCE-FREE — the absorbability tautology is BROKEN [DERIVED, machine-checked]

The derived metric operator (from varying `S_grav`, two-player, covariant; matches Branch-G/weight-doc):
```
E_munu := f G_munu + (g_munu box - nabla_mu nabla_nu) f  -  X f ( d_mu phi d_nu phi - 1/2 g_munu (dphi)^2 ),
          f = e^{2phi}.
```
I computed `nabla_mu E^mu_nu` from scratch on the UDT static metric (full Christoffel ->
Ricci -> Einstein -> scalar-tensor blocks -> covariant divergence, `regrade_2_conservation.py`):

```
nabla_mu E^mu_t  = 0        (static)
nabla_mu E^mu_th = 0        (off the equator)
nabla_mu E^mu_r  = ( X r^2 phi'^2 - X r^2 phi'' - 2 X r phi' + 4 r^2 phi'^2 - 2 r^2 phi''
                     - 8 r phi' - 2 e^{2phi} + 2 ) * phi' / r^2          != 0.
```

**`nabla_mu E^mu_r != 0`.** This is the crux. The divergence is NOT zero; it is `phi'` times a
scalar-EOM-shaped bracket. Cross-check (`regrade_3c.py`): at X=0 (pure `f R` gravity, the relevant
piece for the angular/Branch-P sector) the bracket is EXACTLY `-1/2` of the scalar field equation
combination, i.e.
```
nabla_mu E^mu_r = -(1/2) (EOM_phi) phi'        [confirmed exactly at X=0; ratio = -2 -> -1/2 normalization].
```
This is the standard scalar-tensor Bianchi identity: **the gravity operator's divergence is the
scalar EOM projected along phi'.** It vanishes ONLY on-shell for phi (when EOM_phi=0), NEVER as an
identity. (The full-X bracket differs from my hand-assembled scalar EOM only by the X-kinetic
normalization term `X r (r phi'^2 - r phi'' - 2 phi')` — a bookkeeping factor on box-phi in my
by-hand EOM, `regrade_3b.py`; the X=0 case is unambiguous and confirms the structure.)

**Consequence for absorbability.** Because `nabla^mu E_munu != 0` identically, there is NO Bianchi
tautology that makes `E_munu = (1/2) Tw_munu` force a conserved relabeled source. The matter
conservation law is now the scalar-tensor EXCHANGE law (diffeo invariance of `S_matter`, derived
covariantly, `regrade_2` docstring):
```
nabla^mu Tw_munu = J_phi nabla_nu phi ,    Tw_munu = e^{2phi} T^bare_munu  (the weighted matter stress),
                                            J_phi = (1/sqrt-g) dS_matter/dphi = 2 e^{2phi} L_m.
```
This is a genuine source/exchange, not a relabeling: there is no `Omega(phi)` that turns `Tw` into a
divergence-free `T~` while simultaneously turning `E_munu` into a pure `G_munu`, because the left
side carries its own non-zero divergence `-(1/2)EOM_phi phi'` that must be matched by the matter
phi-source. The two are tied by the phi EOM, not removable by units/coordinates.

### 2.1 The subtle, important point: the teeth are from the OPERATOR, not from a=+1 alone [DERIVED]

A clean separation (`regrade_6_matterlaw.py`): in the OLD (EH) frame, **even a=+1 would have been
absorbable** — `T~=e^{2phi}T` is conserved by the EH Bianchi tautology for ANY exponent. So the
make-or-break is NOT "a is +1 instead of -1." **It is that the left side is no longer the EH tensor,
so the tautology that did the absorbing is gone.** On the new operator, a(phi)=e^{+phi} (weight
e^{2phi}) has TEETH precisely because there is no relabeling that removes it — the scalar field that
the weight couples to is a dynamical player whose own EOM ties the matter exchange to the geometry.

(Note the a=-1 vs a=+1 number is still physically meaningful as the matter-ruler-vs-metric-ruler
"in-step/out-of-step" condition of the old doc Sec 2 — but that fingerprint is no longer the WHOLE
departure; it now sits on top of an operator that already departs from GR in vacuum.)

---

## 3. ABSORBABILITY VERDICT

> **a(phi)=e^{+phi} is now PHYSICAL — a genuine, non-removable matter-depth coupling.** The old
> "scalar weight is absorbable -> UDT = GR on the matter side" conclusion was a Bianchi tautology
> resting entirely on the EH left side (premise P2, self-flagged as the smuggle-surface). With the
> derived scalar-tensor operator, `nabla^mu E_munu = -(1/2)EOM_phi phi' != 0` identically, so the
> tautology is dead. The matter stress now obeys a scalar-tensor EXCHANGE law
> `nabla^mu Tw_munu = 2 e^{2phi} L_m nabla_nu phi`, which is a real source coupling, not a
> relabeling. **Matter = scale-breaker WITH TEETH: confirmed analytically.** (Scoped: static SSS
> slice for the explicit divergence; the identity `nabla E = -(1/2)EOM_phi phi'` is covariant and
> chart-independent in structure — the explicit check is static-spherical.)

This also vindicates the scale-symmetry MAP's reframe: vacuum is (anisotropically) scale-free, and
it is matter's dimensionful coupling that breaks the symmetry — and we now see the SAME thing in the
conservation structure: the matter source does not decouple/relabel; it exchanges with phi.

---

## 4. RE-DERIVE THE SOLITON EXTERIOR ON VACUUM != GR [DERIVED, machine-checked]

OLD exterior (`angular_lagrangian_results.md` D9, Task 6; `native_matter_step_results.md` Sec 0):
the winding hedgehog's long-range angular stress is `T^t_t = T^r_r = -xi/r^2`, `T^th_th = 0` (a
genuine 1/r^2 TAIL, not compactly supported). On the EH operator: `G^t_t = G^r_r` IDENTICALLY, so
the t- and r-equations COLLAPSE to one, the `T^th_th=0` leaves the g_rr-fixing theta-equation
untouched, and the solution is `e^{-2phi} = 1 - kappa8 xi - rs/r` = **global-monopole (solid-angle
deficit) + Schwarzschild, with B=1/A exact**.

NEW operator: I sourced the SAME winding tail into the scalar-tensor `E^mu_nu` and tested the two
structural facts that made the old exterior clean (`regrade_4_exterior.py`, A,B,phi all kept
independent — B=1/A NOT imposed, so it is TESTED):

**(a) The t/r collapse is BROKEN.** On the EH operator `G^t_t - G^r_r = 0` identically. On the new
operator:
```
E^t_t - E^r_r  =  [ X r AB phi'^2 + 4 r AB phi'^2 + 2 r AB phi''
                    - r A B' phi' - r B A' phi' - A B' - B A' ] * e^{2phi} / (r A B^2).
```
Setting phi=const collapses this to `-(A B)' e^{2phi}/(...)`, which vanishes under B=1/A — i.e. the
OLD result is recovered EXACTLY in the phi-constant limit (`regrade_5.py`, machine-confirmed). But
with the scalar hair LIVE (phi' != 0), the extra terms `X r AB phi'^2 + 4 r AB phi'^2 + 2 r AB phi''`
are NON-ZERO, so **`E^t_t != E^r_r`: the t/r equations no longer collapse, and B=1/A is no longer
automatically preserved in the exterior.**

**(b) Scalar HAIR is present in the true vacuum.** Beyond the winding tail (T=0), the operator is the
Branch-G vacuum, which (Branch G Sec 2b, blind-verified) is NOT Schwarzschild alone: it is a
two-parameter `{mass m, scalar charge q}` family with `phi ~ phi_inf - q/r`, `phi' ~ q/r^2`, MONOTONE,
no turning radius. So the soliton exterior now carries a 1/r SCALAR HAIR in addition to mass.

### Exterior verdict
> **The soliton exterior is genuinely DIFFERENT on vacuum != GR.** It is NO LONGER simply
> "global-monopole deficit + Schwarzschild with B=1/A exact." It is: **a scalar-tensor (Fisher/JNW/
> Brans-I-type) exterior carrying BOTH a mass m and a 1/r scalar charge q (phi-hair, phi'~1/r^2),
> with the angular winding still contributing its 1/r^2 deficit-type tail — but B=1/A is NO LONGER
> automatically preserved once the hair is live** (the t/r collapse that guaranteed it is broken by
> the scalar-tensor terms). The old global-monopole+Schwarzschild reading is recovered ONLY in the
> phi-constant (hairless) limit, which the new vacuum does not enforce. How matter "sits in the
> geometry" changes: it now communicates with the exterior through a propagating scalar charge, not
> only through mass + a frozen deficit.

**Honest analytic vs needs-a-solve:** the STRUCTURE above (hair present, t/r collapse broken, old
result = constant-phi limit) is settled analytically. The QUANTITATIVE exterior profile (the actual
{m, q} of the hedgehog soliton, whether B=1/A is mildly or strongly broken, the deficit's modified
magnitude) requires the bounded coupled ODE re-solve on the new operator — that is a NEEDS-A-SOLVE
item, not settled here. Branch-G shoots already show the vacuum hair is monotone/scale-free, so the
exterior gains a continuous charge, not a discrete structure (consistent with everything-on continuum).

---

## 5. CARRY-OVER vs RE-SCOPE LIST (the deliverable's spine)

### CARRIES OVER UNCHANGED (operator-robust — covariance/uniqueness/topology, not curvature-form)
| Result | Why it survives |
|---|---|
| **L2 native-ness (the FORM)** | unique 2-derivative diffeo+target-isometry scalar; covariance argument, independent of the gravity operator. |
| **L4 native-ness** | = metric-norm of UDT's OWN H1 area-form current (Skyrme = native object); blind-verified, operator-independent. |
| **omega_H1 charge, N=3, q=1/3, eta=1/18, deg-1 winding integral=1** | topological / dial-free; read off the area form; CARRY. |
| **S^2 carrier settlement** | action-target argument (n_4=0 the only interior critical point); the action terms are unchanged. CARRY. |
| **T^t_t = T^r_r inside matter (the B=1/A SOURCE)** | a property of the purely-angular winding stress, not of the operator; CARRY. *** But note: the EXTERIOR consequence (B=1/A preserved outside) does NOT carry — see re-scope. *** |
| **The winding-BC import verdict (#61)** | a provenance fact about the catalog's sector index; operator-independent. CARRY. |
| **Solver MACHINERY** (discretization, gates, 4x4 stress, JFNK/dense-LM) | operator-agnostic; the curvature operator is a contained swap. CARRY. |
| **CHARGE read-off CLEAN** (deg-1 winding=1, dial-free) | topological; CARRY (native_matter_step verdict survives for charge). |

### RE-SCOPED TO THE SUPERSEDED OPERATOR — must be re-run / re-graded
| Result | New status |
|---|---|
| **"matter source is ABSORBABLE -> UDT = GR on the matter side"** (udt_matter_source_MAP) | **OVERTURNED.** Rested on the EH Bianchi tautology (P2). On the new operator `nabla E != 0`, no relabeling exists. **a(phi)=e^{+phi} is PHYSICAL.** (Sec 2-3.) |
| **The exchange law `nabla T = -(a+1)phi' T`** (derived from EH Bianchi) | **RE-DERIVED.** Now the scalar-tensor exchange `nabla^mu Tw_munu = 2 e^{2phi} L_m nabla_nu phi`. (Sec 2.) |
| **Soliton exterior = global-monopole + Schwarzschild, B=1/A exact** (angular_lagrangian D9; native_matter_step Sec 0) | **RE-SCOPED.** New exterior = scalar-tensor hair {m,q} + winding tail; B=1/A NO longer automatic (t/r collapse broken). Old form = the constant-phi limit only. (Sec 4.) |
| **The "native hedgehog is static, T_tr=0, time-live orthogonal" PIVOT** (native_matter_step Sec 0) | **Already flagged a SLICE** by the background-track (T_tr survives for live d_t Theta). Independent of this re-grade, but its static read-off now ALSO sits on the superseded operator — doubly re-scoped. |
| **M_MS = 0.281 sqrt(kappa/xi)** and every mass number read at a=-1 + EH operator | **RE-SCOPED (needs re-run).** Used a=-1 (weight 1) AND standard Einstein. With a(phi)=e^{2phi} weight on the source AND the scalar-tensor operator, the coupled read-off changes. (Data-blind: we do not care about the number; the SOLVER must run the right foundation.) |
| **"classical metric is a CONTINUUM => must quantize" headline** | Already flagged REOPENED (vacuum != GR; classical does MORE). The matter feed used the old operator; re-scoped with the rest. (Branch-G shoots say the new exterior hair is still a continuum, so discreteness is NOT restored by the operator change alone — consistent.) |

---

## 6. WHAT THE RE-GRADE SETTLES ANALYTICALLY vs WHAT NOW NEEDS THE HEAVY SOLVER

**SETTLED ANALYTICALLY (this push, machine-checked):**
1. **Absorbability is BROKEN** — `nabla^mu E_munu != 0`, equal to `-(1/2)EOM_phi phi'` (X=0 exact);
   no Bianchi tautology; **a(phi)=e^{+phi} is physical, not removable.** (The make-or-break.)
2. The **conservation law** is the scalar-tensor exchange `nabla^mu Tw_munu = 2 e^{2phi} L_m nabla phi`.
3. The **teeth come from the OPERATOR** (left side != EH), not from a=+1 vs a=-1 alone.
4. The **exterior STRUCTURE is changed**: scalar hair {m,q} present; the t/r collapse that preserved
   B=1/A is BROKEN once hair is live; old global-monopole+Schwarzschild = the constant-phi limit only.
5. The carry-over list (Sec 5) is settled by provenance/covariance arguments.

**NEEDS THE HEAVY SOLVER (bounded, single-process, never background-poll — for LATER, gated):**
6. **Re-run the coupled matter soliton on the new operator** (scalar-tensor left + e^{2phi} matter
   weight): the quantitative exterior {m, q}, how strongly B=1/A is broken in the body/exterior, the
   modified deficit magnitude, the new M_MS read-off. The operator swap is contained (machinery
   carries); the re-run is the work.
7. **The time-live coupled native-matter solve** — still the genuinely untaken step (proven
   non-trivial by the T_tr probe); now to be run on the new operator with the native S^2 carrier and
   Theta free.

**NOT TOUCHED by this re-grade (remain open, per the MAP):** the F2 L2+L4 forced-ness/completeness;
the scale-breaker l=sqrt(kappa/xi) VALUE provenance (xi, kappa still chosen); the imported winding BC;
the p-selector. These are orthogonal to the operator change.

---

## 7. PREMISE LEDGER (chose / derived)

| # | Premise / value / choice | Status |
|---|---|---|
| R1 | Derived gravity operator E_munu = f G + (g box - nn)f - Xf(...), f=e^{2phi} | DERIVED upstream (native_dilation_weight, Branch G); USED here |
| R2 | Matter couples with rest-mass weight e^{2phi} (a(phi)=e^{+phi}) | DERIVED upstream (native_dilation_weight D2); USED here |
| R3 | S_matter = INT sqrt(-g) e^{2phi} L_m (the weight rides out front, phi indep of g) | CHOSE (the natural reading of "rest-mass weight e^{2phi}"; flagged — an alternative non-minimal placement could shift J_phi, but NOT the nabla E != 0 conclusion, which is matter-independent) |
| R4 | nabla_mu E^mu_r != 0 (machine-checked, static SSS) | DERIVED (regrade_2) |
| R5 | nabla E = -(1/2) EOM_phi phi' (the scalar-tensor Bianchi identity) | DERIVED exactly at X=0 (regrade_3c); structure confirmed; full-X normalization is a by-hand EOM bookkeeping factor (FLAG, minor) |
| R6 | Absorbability tautology requires nabla(left side)=0 (the EH Bianchi) | DERIVED (old doc P2, re-stated); its premise now FALSE |
| R7 | Exterior: E^t_t - E^r_r != 0 with live hair; = -(AB)' at phi const | DERIVED (regrade_4, regrade_5) |
| R8 | Vacuum carries scalar hair {m,q}, phi'~1/r^2, monotone, scale-free | DERIVED upstream (Branch G Sec 2b, blind-verified); USED here |
| R9 | Static SSS, areal chart for the explicit divergence/exterior computation | CHOSE (CANON slice; the divergence IDENTITY is covariant — the explicit exhibit is static-spherical) |
| R10 | Winding tail T^t_t=T^r_r=-xi/r^2, T^th_th=0 carries over | DERIVED upstream (angular_lagrangian D5); USED here |

---

## 8. ATTACK HERE (for a blind verifier — required before banking)

1. **The divergence (the central claim).** Re-compute `nabla_mu E^mu_nu` from scratch on the UDT
   metric; confirm `nabla E^mu_r != 0` and equals `-(1/2)EOM_phi phi'`. Pin the full-X normalization
   of the scalar EOM (I left an X-kinetic bookkeeping factor; X=0 is exact). A sign/factor slip here
   does not change the != 0 conclusion but should be cleaned.
2. **Is the matter coupling really non-minimal (e^{2phi} L_m)?** Check R3: "rest-mass weight e^{2phi}"
   — is the weight on the full Lagrangian, or only on a rest-mass term (point particle) so that field
   matter (the hedgehog) couples differently? This changes J_phi but NOT the broken-tautology verdict
   (that is matter-independent: nabla E != 0 regardless of T).
3. **The exterior t/r break.** Re-derive `E^t_t - E^r_r`; confirm it reduces to `-(AB)'` at phi const
   and is non-zero with live hair. Run a bounded coupled ODE shoot of the actual hedgehog on the new
   operator and report whether B=1/A is mildly or strongly broken in the exterior.
4. **Absorbability counter-attempt.** Try HARD to find an `Omega(phi)` field/metric redefinition that
   relabels the new system back to GR-with-conserved-source. The claim is none exists because
   `nabla E != 0`; a verifier should attempt the relabel and confirm it fails.
5. **Carry-over audit.** Spot-check that L2/L4 native-ness, the charge, and N=3/q=1/3 genuinely do NOT
   depend on the curvature operator (they shouldn't — they are pre-gravity covariance/topology).

---

## 9. SINGLE CLEANEST STATEMENT

On the OLD operator, the matter weight was absorbable by a Bianchi tautology that rested entirely on
the Einstein-Hilbert left side (self-flagged as the smuggle-surface), so "UDT = GR on the matter
side" held at a=-1. The native operator is now BUILT and is scalar-tensor: its divergence
`nabla^mu E_munu = -(1/2)EOM_phi phi' != 0` identically, so **the tautology is dead and a(phi)=e^{+phi}
is PHYSICAL — matter is a scale-breaker with teeth, confirmed analytically** (and the teeth come from
the operator, not from a=+1 alone). The soliton exterior is correspondingly RE-DERIVED: it gains a 1/r
scalar hair (mass + scalar charge {m,q}) and the t/r collapse that guaranteed B=1/A is broken once the
hair is live — the old global-monopole+Schwarzschild form is recovered only in the constant-phi limit.
What CARRIES over (operator-robust): L2/L4 native-ness, the omega_H1 charge with N=3/q=1/3/eta, the S^2
carrier, T^t_t=T^r_r inside matter, the imported-BC verdict, and the machinery. What is RE-SCOPED:
the absorbability/"UDT=GR-on-matter" conclusion (OVERTURNED), the exchange law (re-derived), the
exterior (re-derived), and every mass number read at a=-1+EH (needs re-run). The re-grade SETTLES the
absorbability and the exterior STRUCTURE analytically; the QUANTITATIVE coupled soliton on the new
operator and the time-live solve NEED the heavy solver. **NOT canon; OBSERVE + analytic only.**

---

## VERIFICATION (2026-06-21) — blind adversarial pass, agent a4aa12aa522f06b6c
SUPPORTED. Independent sympy recompute (full Christoffel->Ricci->Einstein->scalar-tensor operator->covariant
divergence, with A,B,phi ALL independent — B=1/A never imposed).
- **A1 (a=e^{phi} now PHYSICAL; teeth from the OPERATOR): SUPPORTED.** nabla_mu E^mu_r != 0 (factors as
  (bracket)*phi', vanishes only at phi'=0); at X=0 exactly -(1/2)(EOM_phi)phi'. CRUCIAL SUBTLETY CONFIRMED:
  nabla^mu G_munu = 0 identically on ANY metric, so on the EH operator the relabel e^{(a+1)phi}T is conserved
  for ANY constant a (a=-1 NOT special for absorbability); on the derived operator no conserved relabel exists.
  The teeth come from the OPERATOR (left side != EH), not from a=+1 vs -1. (Minor: the X!=0 EOM normalization is
  a by-hand bookkeeping factor; X=0 identity exact, conclusion untouched.)
- **A2 (B=1/A breaks in the exterior once phi-hair is live): SUPPORTED.** E^t_t-E^r_r != 0 with live phi',
  -> 0 recovering B=1/A in the phi=const/hairless limit (machine-confirmed).
NET: bank. The single most load-bearing change — "matter is absorbable -> UDT=GR on the matter side" — is
OVERTURNED; a(phi)=e^{phi} is a real, non-removable depth coupling (teeth from vacuum!=GR). Exterior = scalar-
tensor {m,q} hair (Fisher/JNW), B=1/A broken, still a continuum. Quantitative {m,q}/M_MS need the bounded re-run.
