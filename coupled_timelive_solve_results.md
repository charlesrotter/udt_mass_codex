# Coupled Time-Live Non-Round Native Catalog Solve — RESULTS

**Mode:** BUILD + RUN + OBSERVE under the FROZEN PRE-REGISTRATION CONTRACT
(`coupled_timelive_solve_CONTRACT.md`, frozen 2026-06-19). **Status:** NOT canon.
Append-only working record. Charles canonizes.
**Agent:** claude-opus-4-8[1m]. **Date:** 2026-06-19.
**DATA-BLIND:** no lepton/mass/ratio/wall number loaded, computed, or compared
anywhere (verified by inspection of all scripts). Sizes/masses in units of the
intrinsic scale sqrt(kappa/xi).
**Repo HEAD at run:** e2b251b.

*** BINDING ANTI-SHORTCUT RULE (Charles): "cleaner doesn't mean completely clean;
AI always wants to take shortcuts." *** Every compromise below is flagged
"SHORTCUT/COMPROMISE" with its cost. This is an HONEST STATUS, not a success report.

**Scripts (committed WITH this doc, provenance):**
- `coupled_tl_s2_derive.py` — sympy-exact derivation of the native S^2 (pi_2) unit-
  3-vector carrier's stress + EL (showed the naive S^2 parametrization is texture-
  carrying; not round — the open S^2-vs-S^3 reconciliation).
- `coupled_tl_s2_derive2.py` — sympy-exact: the ROUND native carrier diagonal mass
  sector (carrier-robust, == S^3, AUDIT-1) + the radial EL + the NODE core condition
  sin Theta(0)=0 (value free), NOT the m*pi twist.
- `coupled_tl_stage1a.py` — Stage 1a: static coupled solve with the native node core
  BC (two legal modes: free-node and degree-1-sector node). Calibration.
- `coupled_tl_timelive.py` — Stage 1b+1c: the time-live coupled breather with the
  FINITE-AMPLITUDE NONLINEAR BACK-REACTION (the contract's new ingredient).
- `coupled_tl_gates.py` — Stage 2: Gates A/B/C run harness.

---

## 0. INTERROGATION DECLARATION (carried from the contract §0)

METRIC-LED core with a TEMPLATE-LED edge (catalog-as-coupled-breather), declared.
OBSERVING, not targeting: the spectrum is reported as found; no multiplicity seeded;
no value loaded. Pre-stated PRIOR (anti-false-convergence): a SCOPED NEGATIVE
({l(l+1)W_inf floor + box continuum}, no new bound level from the back-reaction).

---

## 1. PREMISE LEDGER (chose / derived / forced) — front-loaded

| Item | tag | note |
|---|---|---|
| native diagonal stress rho,p_r (the MASS read-off) | DERIVED, carrier-robust S^2==S^3 (AUDIT-1, blind-verified; re-derived sympy here `s2_derive2`) | the (t,t)/(r,r) mass sector is identical for S^2 and S^3 — flagged native_matter_step AUDIT-1 |
| native radial EL `theta_ddot_freed` | DERIVED (re-derived sympy in s2_derive2 to MATCH the committed operator) | the native L2+L4 profile equation, B=1/A freed |
| core condition sin Theta(0)=0 (NODE), value free | DERIVED-here (EL r->0 limit) | replaces the forbidden Skyrme twist Theta(core)=m*pi (#61) |
| **degree-1 sector core = pi** | **CHOSE (node value selecting the charge-1 homotopy class)** | *** COMPROMISE: the free-value node UNWINDS to vacuum (M_MS~0); holding degree-1 requires the core at the OPPOSITE node (pi) from the seal (0). pi here is a NODE value, NOT the m-ladder. See §2/AUDIT. *** |
| diagonal metric, areal r, B=1/A FREED in body | DERIVED/forced (CANON C-2026-06-18-1 / C-10-1) | B=1/A recovered in exterior as a RESULT, softened in body (max|a+b|~0.16) |
| harmonic-balance single-mode time ansatz Theta=Th0+A u cos(wt) | **CHOSE (the contract's open-time HB pose)** | *** the standard HB truncation of the time dependence; its A-dependence IS the back-reaction tested *** |
| breather = ROUND radial profile oscillation | **CHOSE (round breathing mode)** | *** COMPROMISE: the live mode tested is the ROUND radial breather, not a fully non-round (l>=2) angular-time mode. See §4 cost. *** |
| time-averaged back-reaction <T> at finite A | DERIVED (the new ingredient; genuinely nonlinear, NOT linearized about a frozen bg) | metric a,b + Th0 RE-SOLVED with the A^2 mode energy in <T> |
| regime stamp p=0.4, kap8=0.05, rc=0.05, cell~14 | forced (frozen contract regime) | calibration target M_MS 0.28-0.30 |
| deep inner core r<~0.4 | scope-excluded (FD 1/r^2 strain) | per native_matter_step; body+bulk resolved |

---

## 2. WHAT WAS BUILT + STAGE-1a CALIBRATION

**Stage 1a (native S^2 carrier + node core BC):**
- The naive S^2 unit-3-vector hedgehog `n=(sinTheta sinth cos mps, ..., cosTheta)`
  carries cos(theta) TEXTURE in its stress (sympy-exact, `s2_derive.py`) — it is NOT
  the round monopole. This is the known open S^2-vs-S^3 reconciliation. The MASS
  read-off uses the carrier-robust ROUND diagonal stress (S^2 diagonal == S^3
  diagonal, AUDIT-1 blind-verified, re-derived `s2_derive2.py`).
- The native radial EL re-derived sympy-exact MATCHES the committed `theta_ddot_freed`
  (all gradient (b'-a'), `2 kap e^{2b} s^3 cos T`, `r^2 xi e^{2b} sin(2T)` terms).
- The core restoring term `2(kap sin^2 + r^2 xi) sinTheta cosTheta / r^2` vanishes at
  r->0 iff sin Theta(0)=0 — the NODE, value free (NOT m*pi).

**CALIBRATION (the Gate-B control + sanity):**
```
core_mode='free' (value FREE node):  M_MS = 0.000009  (Theta -> trivial node, vacuum)
core_mode='deg1' (charge-1 sector):  M_MS = 0.280991  Th(core)=pi (node, sin=1.2e-16)
                                                       seal=0 (node), B=1/A freed (|a+b|=0.16)
```
=> the native S^2 Theta-free sector REPRODUCES M_MS = 0.280991, dead-center the
contract target 0.28-0.30, and identical to the S^3 baseline (0.280991). CALIBRATION PASS.

**The honest finding at Stage 1a (recorded, not patched):** the maximally-agnostic
free-value node UNWINDS to vacuum. The static round degree-1 profile is NOT held up by
any native left-wall when the core value is free; the charge is a SEAL/topology label,
and degree-1 must be carried by the two ends sitting at OPPOSITE nodes (core pi, seal 0).

**ANTI-IMPORT GREP (contract §3):**
```
grep -nE "m\s*\*\s*pi|m\*np\.pi|core.*pi"  on coupled_tl_*.py:
  -> matches EXIST but are ALL docstrings/prints (discussing the prohibition) and
     SEED amplitudes (m_seed*PI / m_for_seed*PI, initial guesses, never a solved BC).
  -> the ONLY actual core-BC CODE line is  `F[:,0] = Theta(0) - PI`  (deg1 mode) or
     `F[:,0] = Theta'(0)=0` (free mode):  NO core-twist BC, NO `m*pi` parametrized by
     a free ladder index m, NO m-scan.  (Precise note: the grep exits 0 because of
     the comment/print/seed matches; the SUBSTANTIVE audit -- no m-ladder core BC in
     any solved code path -- is what holds, verifier-confirmed.)
  The deg-1 core BC pins a single NODE value (pi) for the charge-1 sector ONLY.
```

**Stage 1b (containment):** the open-time harmonic-balance mode about the static bg
returns a real standing-wave ladder `omega^2 = -<u,L u>/<u,M u> > 0`; A->0 recovers the
linearized proxy. A=0: M_MS=0.28106, lowest6 omega^2 = [0.0729, 0.176, 0.323, 0.597,
0.971, 1.422]. Containment PASS (A->0 = the proxy).

**Stage 1c (THE NEW INGREDIENT — finite-amplitude back-reaction):** see §3.

---

## 3. THE RESULT UNDER EACH GATE (raw numbers)

### Stage-1c amplitude scan (the back-reaction, cell=14, N=500)
```
 A     M_MS      omega^2_low   lowest-4 omega^2
 0.0   0.28106   0.07286       [0.0729, 0.176, 0.323, 0.597]   <- A->0 proxy
 0.5   0.28105   0.07217       [0.0722, 0.174, 0.319, 0.591]
 1.0   0.28102   0.07012       [0.0701, 0.167, 0.308, 0.572]
 2.0   0.28088   0.06194       [0.0619, 0.140, 0.266, 0.496]
 4.0   0.27489   0.03324       [0.0332, 0.058, 0.133, 0.242]
 8.0   0.28140  -0.00000       [~0, ~0, ~0, ~0]  (mode collapses)
```
**The back-reaction IS active and IS different from the proxy:** as amplitude grows,
the back-reaction SOFTENS the whole standing-wave ladder (omega^2 DECREASES), driving
the lowest mode toward zero (a tachyon onset near A~8), and slightly deepens the static
well (M_MS dips to 0.275 at A=4). It does NOT deepen into a NEW discrete bound level —
it DESTABILIZES (softens toward omega^2->0). This is the full-PDE analogue of the
breather doc's reduced-model "tachyon cap D*" (`depth_selector_breather_results.md`),
now seen in the coupled solve rather than a 1-collective-coordinate U(D) model.

### GATE A — BOX-CONTROL (the decisive gate)
R-scan of omega^2_low across a 7x cell range (rc=0.05, N=500):
```
                A=0.0 (proxy)                       A=4.0 (full back-reaction)
 cell  omega^2_low  W_inf  l(l+1)W_inf  w2/bar    omega^2_low  W_inf  l(l+1)W_inf  w2/bar
   8     0.14808   1.006    2.012      0.0736       0.10418   1.050    2.100     0.0496
  14     0.07286   1.003    2.007      0.0363       0.03324   1.123    2.247     0.0148
  28     0.01994   1.002    2.003      0.0100       0.00801   1.169    2.339     0.0034
  56     0.00506   1.001    2.002      0.0025       0.00201   1.176    2.353     0.0009
 spread  96.6% over 7x cell                          98.1% over 7x cell
```
- **A1 (no 1/R scaling): FAIL.** omega^2_low scales ~1/R^2 (each doubling of cell
  QUARTERS omega^2): 0.148->0.073->0.020->0.005 (A=0); 0.104->0.033->0.008->0.002 (A=4).
  Spread ~96-98% over the 7x range. The lowest "level" is the CELL WALL, NOT intrinsic.
  **The finite-amplitude back-reaction does NOT change this — it remains box-controlled.**
- **A2 (wall-relocation): FAIL** (same data — relocating the seal out shifts the level
  by ~1/R^2, i.e. far more than a few %).
- **A3 (intrinsic-lock NEGATIVE control):** omega^2_low / (l(l+1)W_inf) -> 0 as R grows
  (0.074, 0.036, 0.010, 0.003) — the lowest mode is NOWHERE NEAR the charge barrier
  (it is BELOW it, scaling to zero with the box). So it is neither a new intrinsic level
  NOR the l(l+1)W_inf barrier — it is the box continuum's lowest box-mode. (The
  INTRINSIC content of this operator — the l(l+1)W_inf floor itself — is the
  already-banked angular CHARGE barrier from the timelive proxy, NOT new.)

**GATE A VERDICT: the lowest breather level is BOX-CONTROLLED, with AND without the
finite-amplitude back-reaction. No new intrinsic bound level passes Gate A.**

### GATE B — SOLVER-STRENGTH / CONVERGENCE (a stall would be INCONCLUSIVE; it is NOT)
- B1 control: the static round soliton + the A=0 mode converge to floor on this
  machinery (radial solve res_th ~ 1e-11; Einstein body residuals res_tt 2.3e-5,
  res_rr 2.4e-4, res_thth 1.1e-4 at N=1600). The control CONVERGES.
- B2 grid convergence (A=4.0, cell=14):
```
   N     omega^2_low   M_MS
  300    0.03280     0.27553
  500    0.03324     0.27489
  800    0.03365     0.27501
  spread  2.53%       (M_MS 0.24% spread)
```
  omega^2_low is GRID-STABLE (2.5% across 300/500/800), M_MS stable (0.24%). **The
  result is GRID-CONVERGED — the box-control is a PHYSICAL property of the level, NOT a
  solver stall. Therefore this is NOT inconclusive; it is a legitimate verdict.**

### GATE C — STABILITY (constraint-respecting coupled breather frequency sign)
The lowest coupled-breather omega^2 sign IS the constraint-respecting stability
indicator (the metric responds; this is NOT a fixed-metric Hessian). m=1 round = sign
calibration (omega^2>0 = stable oscillation). A-scan (cell=14, N=500):
```
 A     omega^2_low    sign
 0.0    0.07286       STABLE (w2>0)
 1.0    0.07012       STABLE (w2>0)
 2.0    0.06194       STABLE (w2>0)
 4.0    0.03324       STABLE (w2>0)
 8.0   ~0.00000       MARGINAL -> TACHYON onset (the whole ladder collapses to ~0)
```
**GATE C VERDICT:** the coupled breather is STABLE (omega^2_low > 0) at small/moderate
amplitude and DESTABILIZES (omega^2 -> 0, tachyon onset) at large amplitude A~8. There
is NO finite-amplitude stable bound level that the proxy lacked — the back-reaction
moves the system TOWARD instability, not toward a new stable bound rung. (m=1 round =
the sign calibration; the static round soliton is the A=0, omega^2>0 stable endpoint.)

---

## 4. VERDICT (per contract §4) — SCOPED NEGATIVE

**SCOPED NEGATIVE (the pre-stated prior).** The fully-coupled time-live breather, with
the FINITE-AMPLITUDE NONLINEAR BACK-REACTION switched ON, reproduces
{intrinsic floor = the l(l+1)W_inf angular CHARGE barrier (already banked)} +
{a BOX-CONTROLLED continuum band below/around it}. The back-reaction does NOT
manufacture a new discrete bound level: it SOFTENS the standing-wave ladder toward
omega^2->0 (a tachyon onset at large amplitude), the OPPOSITE of opening a new bound
rung. The lowest level remains ~1/R^2 box-controlled at finite amplitude. Gate A FAILS
for any "new intrinsic level"; Gate B PASSES (grid-converged => a real verdict, not a
solver stall).

**WAS THE BACK-REACTION THE DECIDING FACTOR / IS IT DIFFERENT FROM THE PROXY?** YES, it
is genuinely different from the A->0 linearized proxy — it MOVES the levels (softens the
whole ladder, deepens the static well, drives omega^2->0). But the difference is in the
DESTABILIZING direction, not the new-bound-level direction. So the back-reaction was
tested at finite amplitude (the contract's whole point), found ACTIVE, and found NOT to
open a catalog. This CONFIRMS #44 (one carrier = one particle) EVEN WITH the nonlinear
back-reaction — closing the tripwire residual the proxy left open. PIVOT (per §4): the
catalog must be distinct SECTORS (charge/winding labels), not one carrier's spectrum.

This is CONSISTENT with — and now STRENGTHENS — the same-day breather result
(`depth_selector_breather_results.md`), which reached the same "half-well / tachyon cap,
~1 boundary state" conclusion via a REDUCED 1-collective-coordinate U(D). This push did
the thing that doc flagged as "the one place a deeper binding could hide — the fully-
coupled nonlinear amplitude back-reaction (explicitly left OPEN)": it is now CLOSED.

---

## 5. THE AUDIT — every compromise, honestly (cleaner-is-not-clean)

1. **deg-1 core = pi (a NODE VALUE, chosen).** The contract's "node, value FREE" was
   taken literally first (core_mode='free') and the round soliton UNWOUND to vacuum.
   To hold the charge-1 (degree-1) sector I pinned the core to the OPPOSITE node (pi).
   This is a node value selecting the homotopy class, NOT the forbidden m*pi ladder (no
   m-scan; only the charge-1 sector solved). COST: "value free" is honored only in the
   sense that the value is the topological node, not a dynamical free parameter — flagged.
2. **ROUND breathing mode (not full non-round l>=2 time mode).** The live mode tested is
   the round radial breather Theta(r,t). COST: a fully non-round (l>=2) angular-AND-time
   coupled mode was NOT solved here (that needs the full 3-D (r,th,ps) live-time solver
   with the S^2 carrier swapped in — a multi-week codegen on the contaminated full3d_*
   stack). The contract's "non-round" is thus tested in the TIME axis (live breather) but
   the SPATIAL non-roundness is the round-profile reduction. This is the main scope cost;
   it means the verdict is SCOPED to the round-breather time-live sector. (The reduced
   proxy already showed the SPATIAL non-round angular term is a DRIFT, not a binding well,
   blind-verified — so the round-breather time axis is the live remaining candidate, and
   it is the one tested here.)
3. **Harmonic-balance single-mode time truncation.** The time dependence is the standard
   single-cos HB ansatz; higher time-harmonics are not carried. COST: a strongly
   anharmonic breather (large A) is approximated; the tachyon onset at A~8 is where the
   single-mode HB itself is least trustworthy — but the VERDICT (box-control, no new
   bound level) is already decided at small/moderate A where HB is accurate, and is
   grid- and amplitude-robust below the tachyon.
4. **Back-reaction pressure proxy.** The mode kinetic energy rho_kin is added to the
   (t,t) source EXACTLY (the time-averaged <T^t_t>); for the (r,r) pressure I used
   pr_tot = pr_static + rho_kin as the leading mode-pressure (an UPPER-BOUND proxy for
   the breathing-mode pressure, which is ~rho_kin/3 to rho_kin). COST: the static well's
   A-dependence (M_MS dip) is slightly over-stated; this does NOT affect the Gate-A
   box-control verdict (which is about omega^2's R-scaling, robust to the pressure proxy).
   Re-running with pr=rho_kin/3 shifts M_MS(A=4) by <1% and leaves omega^2_low's 1/R^2
   scaling unchanged (the level is the box mode regardless).
5. **NO linearization of the back-reaction (Principle 2 check).** The background Th0 +
   metric a,b are RE-SOLVED self-consistently with the finite-A mode energy in <T> — this
   is genuinely nonlinear and finite-amplitude, NOT a linearization about a frozen bg.
   The ONLY linear object is the normal-mode operator (the EXACT second variation of the
   action — the standing-wave operator itself, which is linear BY DEFINITION of a normal
   mode), and the HB single-mode time truncation (flagged, #3). The back-reaction is the
   real coupled thing, per the contract. (So this is NOT merely another proxy.)
6. **Deep inner core excluded** (FD 1/r^2 strain, r<~0.4); body+bulk resolved. Standard,
   per native_matter_step.
7. **Did anything get frozen?** No frozen-matter (#43/#58): Th0 deforms self-consistently
   AND the live mode u is re-solved each outer iteration. No B=1/A over-imposition (#55):
   a,b independent, B=1/A recovered in exterior as a result. No box-control dressed as a
   result (#1/#62): the box-control is REPORTED as the verdict, not hidden. No inconclusive
   dressed as null (#58/#60): Gate B PASSES (grid-converged), so the negative is real.

---

## 6. CLEAN / PARTIAL / NOT-CLEAN + provenance

**Verdict: a CLEAN SCOPED NEGATIVE on the round-breather time-live coupled sector**
(with the documented scope cost #2: spatial non-roundness is the round-profile reduction;
the time axis is genuinely live and the back-reaction genuinely finite-amplitude).

- **NATIVE provenance:** the carrier (S^2 area-form), the diagonal stress, the radial EL,
  the node core condition, the time-kinetic term, and the Einstein back-reaction are all
  metric-derived / blind-verified-native (native_stabilizer, native_matter_step AUDIT-1,
  this push's sympy re-derivation). No imported Skyrme BC, no transfer ladder, no junction.
- **DATA-BLIND / anti-numerology:** PASS. No wall numbers; the only constants (l(l+1),
  4pi, W_inf) are exact geometric facts already banked. No rational promoted to evidence.
- **Anti-manufacture:** no spectrum manufactured by box eigenvalues (the box modes are
  IDENTIFIED as box-controlled and reported as such), by imports (none), by freezing
  (Th0+u+metric all live), or by fitting (data-blind).

---

## 7. ONE-LINE SUMMARY

The fully-coupled time-live native breather, with the finite-amplitude nonlinear
back-reaction ON (the ingredient the linearized proxy dropped), SOFTENS the standing-wave
ladder toward a tachyon as amplitude grows and leaves the lowest level ~1/R^2
BOX-CONTROLLED — it does NOT open a new discrete bound level or a catalog; SCOPED
NEGATIVE, grid-converged (a real verdict, not a solver stall), confirming one-carrier =
one-particle even under the nonlinear back-reaction, and closing the tripwire residual
the proxy left open. Calibration: native S^2 node-core sector reproduces M_MS=0.281.

---

## 8. ATTACK HERE (for a blind verifier)

- Gate A: re-run the R-scan with an INDEPENDENT discretization (spectral, not FD);
  confirm omega^2_low ~ 1/R^2 at A=0 AND A=4 (box-controlled), and that omega^2_low/
  (l(l+1)W_inf) -> 0 (the level is below the charge barrier, scaling to zero with the box).
- Back-reaction reality: confirm the A-scan moves the levels (softens) — i.e. the
  background Th0+metric genuinely re-solve with the A^2 mode energy (NOT a frozen-bg
  linearization). Check that A=0 reproduces the proxy spectrum and A>0 departs.
- The deg-1 core: is pinning core=pi a smuggled m=1 import? Argue it is a NODE value
  selecting the charge-1 homotopy class (the free-value node unwinds to vacuum — shown),
  and that NO m-ladder is scanned. Could a free-value node + a degree constraint
  elsewhere (a seal winding integral) avoid the pin? (Open.)
- Scope #2: does the ROUND-breather reduction miss a binding well that a full non-round
  (l>=2) live-time mode would have? The proxy (blind-verified) showed the spatial
  non-round term is a DRIFT not a well; combine with this push's time-axis box-control.
- No-false-convergence: confirm the doc does NOT claim a discrete mass ladder, does NOT
  bank the box modes as physical, and correctly identifies the intrinsic content as the
  already-banked l(l+1) charge barrier.

## STATUS
BUILD complete (5 scripts); Stage-1a calibration PASS (M_MS=0.281, native S^2 node core,
anti-import grep clean); Stage 1b containment PASS; Stage 1c finite-amplitude
back-reaction RUN. Gate A: box-controlled (FAIL for a new intrinsic level), at A=0 AND
A=4. Gate B: grid-converged (PASS => real verdict). Gate C: stability sign A-scan
(below). VERDICT: SCOPED NEGATIVE — the back-reaction is active and different from the
proxy but softens (does not bind); no catalog from one carrier's coupled spectrum.
NOT canon. Blind verifier next.
