# Time-Live Non-Round Native Solve — The Convergent Centerpiece (structural-first)

**Mode:** STRUCTURAL-FIRST (semi-analytic, sympy-exact) + NUMERIC-CONFIRM (demoted to a check).
**Agent:** claude-opus-4-8[1m]. **Date:** 2026-06-19. **Status:** NOT canon. Append-only working record.
**Scripts:** `timelive_nonround_structural.py` (sympy-exact operator analysis),
`timelive_nonround_numeric.py` (BC-clean SL eigen R-scan).
**DATA-BLIND:** no lepton/mass/ratio/wall numbers loaded anywhere (verified by inspection).
**Anti-numerology:** no rational/integer promoted to evidence; the only constants are the exact
geometric `l(l+1)` and `4pi` already banked. No TEST-B classifier required (no new identity claimed).

---

## 0. The question (restated) and the convergence that located it

Three tracks converged here (frontier-time-live-native-matter memory; STATE 2026-06-19):
- **B2** proved (sympy-exact): about the ROUND background the native angular nonlinearity `-v_theta^2`
  linearizes to **EXACTLY ZERO** (its variation is `-2 v0_theta * delta v_theta`, and `v0_theta=0` round),
  so the fluctuation operator is the pure dressed Laplacian, eigenvalue `-l(l+1)W(r)`, `W>0` =>
  SIGN-DEFINITE DAMPING, no discrete tower.
- **wcc** proved (numeric, blind-verified): the round cell is the only STATIC fixed point — every lobe
  relaxes to round; the seal closure holds no dynamical angular mode (gap 0.648 > 0).
- **the time-live anchor** proved (sympy-exact): a TIME-LIVE native profile has `<T_tr>_{l=0} != 0`, so it
  sources `G_tr`, ESCAPES Birkhoff, UNFREEZES time. The static/round slice is exactly where phi-angular dies.

**THE DECISIVE STRUCTURAL QUESTION:** about a NON-ROUND (`v0_theta != 0`) AND TIME-LIVE (`d_t != 0`)
background, does the fluctuation operator become DISCRETE (a standing-wave eigencondition with bound
modes — the catalog/generations home), or does it stay sign-definite (no spectrum)?

---

## 1. PREMISE LEDGER (chose / derived / forced) — front-loaded for Charles

| Item | tag | note |
|---|---|---|
| native field eqn `v_mm + e^{2v}(v_thth+cot th v_th - v_th^2) = Phi(e^{-2v}-e^v)` | DERIVED (wint ★, wcc, verified two ways) | the object being linearized |
| `-v_theta^2` linear variation = `-2 v0_theta u_theta` | DERIVED-here exact (script Part 1) | the prompt's "new term" |
| time term: round=frozen (Birkhoff), non-round l>=2 = vacuum WAVE `+d_t^2 h` | DERIVED (phase0, verifier-confirmed PHYSICAL not gauge) | NOT imported; native escape |
| harmonic balance `u = U e^{i omega t}` => `omega^2` generalized eigenproblem | DERIVED-from-kernel (phase0 (C)) | the standing-wave pose |
| only STATIC fixed point is round (no non-round static bg) | from corpus (wcc, blind-verified) | load-bearing: non-round must be time-carried |
| dressed SL operator `-(P U')' + [l(l+1)W+Q]U` with P,W,Q smooth bounded -> const exterior | **CHOSE (generic native-like model)** | *** SHORTCUT: not the pointwise converged coupled v0; see §6 *** |
| source-potential proxy `Q(r) >= 0` | **CHOSE** | tested: setting Q=0 does NOT change the floor verdict (§5) |
| cell size R | **SCAN variable** (not fixed) | the box-control gate runs on it |
| seal BC (Dirichlet / Neumann) | both tested | not the artifact (§5 [3]) |
| inner core r->0 | Dirichlet regularity node (l>=1) | deep core FD-strain excluded, flagged |
| no imported Skyrme BC `Theta(core)=m pi` (#61) | HONORED | native carrier, Theta free |

---

## 2. THE STRUCTURAL VERDICT (the decisive part) — three findings, honest and two-edged

### Finding 1 — the prompt's "new `-2 v0_theta delta v_theta` term" is a DRIFT, not a binding potential (a myopia correction)

The prompt's hypothesis was that the non-round term `-2 v0_theta * delta v_theta` is the discretizer.
Exact symbolic analysis (script Part 1-2) shows this is **partly wrong, and the correction matters**:

```
d/d_eps [ -(v_theta)^2 ]|_0  =  -2 v0_theta u_theta     [EXACT]   (round: =0 — B2 reproduced)
angular operator about non-round bg:  A[u] = u_thth + (cot th - 2 v0_theta) u_th
```

This is a **first-derivative (advection/drift)** term, NOT a zeroth-order potential. An SL operator
`u'' + p(th) u'` is self-adjoint in weight `w = exp(INT p) = sin(th) e^{-2 v0(th)}`. So the new term
is exactly absorbed by a change of weight `sin th -> sin th e^{-2 v0}`: the operator stays **self-adjoint
and its principal part stays sign-definite (a Laplacian in a deformed weight)**. A drift cannot by itself
flip the operator's sign or create a bound state. **So non-roundness alone, on the angular axis, does NOT
manufacture a discrete bound tower** — it re-weights the same sign-definite Laplacian. This is the honest
correction to the push hypothesis (and exactly the "myopic single-term" trap the charter warns of).

The genuine zeroth-order POTENTIAL in the full operator comes from the SOURCE term
`-Phi(e^{-2v}-e^v)`, whose variation is `V_pot = Phi(e^{3v0}+2)e^{-2v0}` (script Part 3) — and that is the
same potential wcc already diagonalized about the round bg and found gap 0.648 > 0 (no soft mode).
About a non-round bg `V_pot` becomes theta-dependent, but **no non-round STATIC background exists**
(wcc: lobes relax to round), so there is nothing static to linearize about. **The non-roundness must be
carried by the TIME sector — and that is where the real change lives (Finding 2).**

### Finding 2 — TIME-LIVE flips the sign-definite SAME operator from "no spectrum" to a STANDING-WAVE LADDER

The native time term is DERIVED, not imported (phase0, blind-verified): the round vacuum class is
Birkhoff-frozen (no `d_t^2`), but the **non-round l>=2 sector obeys a vacuum WAVE equation** — `G_thth`
carries `+d_t^2 h` with a gauge-invariant (radiative) coefficient. In harmonic balance `u = U(m,th)e^{i omega t}`,
the live `+d_t^2 -> -omega^2`, so the field equation becomes a generalized eigenproblem

```
L_space[U] = omega^2 M[U],   M > 0   =>   omega^2 = ( -<U, L_space U> ) / <U, M U>.
```

**The decisive structural point (two-edged):** the SAME sign-definiteness B2/wcc reported as "no
spectrum" is, read on the time-live axis, exactly what makes `omega^2 > 0`:
- `-L_space > 0` (the wcc gap, the `-l(l+1)W` damping) is *precisely* the condition for a REAL
  oscillation frequency `omega^2 > 0` (a genuine standing wave) rather than `omega^2 < 0` (an
  exponential instability).
- B2/wcc's "sign-definite damping, no tower" is the STATIC statement (no bound state, no growing mode) —
  TRUE and unchanged. But the TIME-LIVE reading of the same operator is a **ladder of real standing-wave
  frequencies** `omega_l^2 = -lambda_l / M_l > 0`, one per spatial eigenmode `lambda_l = -l(l+1)W`.

So: **the time-live non-round carrier DOES turn the dead static operator into a standing-wave eigenproblem.**
Charles's phi-angular hunch finds a carrier here: the phi-angular damping operator, run on the time axis,
IS a standing-wave spectrum. **But "a spectrum exists" is not "a discrete intrinsic mass ladder exists" —
that is the box-control question, and it is where the result is decided (Finding 3).**

### Finding 3 — the spectrum is an INTRINSIC FLOOR + a BOX-CONTROLLED CONTINUUM, NOT a discrete bound tower

Numeric R-scan of the standing-wave operator (script `timelive_nonround_numeric.py`, BC-clean
interior SL eigensolve; GPU/CPU agree to 6e-14):

**(a) The lowest frequency is R-INDEPENDENT (intrinsic), not box-controlled:**
```
 R     omega^2(l=1, lowest)
 8     1.995
 32    1.974
 128   1.975
 512   1.984          <- flat across a 64x cell range => INTRINSIC, not ~1/R^2
```
This is the OPPOSITE of the CS4 / single-cell-spectrum box-controlled finding (`omega^2 ~ 1/R^2 -> 0`).

**(b) But the floor is exactly the CENTRIFUGAL ANGULAR BARRIER `l(l+1)W_inf`, not a bound state:**
setting the source proxy `Q=0` identically, the floor equals `l(l+1) * W_inf` (W_inf = exterior `e^{2v0}`):
```
 l=1: floor 1.98  vs l(l+1)W_inf = 2.0   (ratio 0.99)
 l=2: floor 5.43  vs            6.0       (0.91; the shallow core well dips it slightly)
 l=3: floor 10.06 vs           12.0       (0.84)
```
The floor is the bare `-l(l+1)W` damping term of B2 read as a standing-wave gap — an INTRINSIC mass-GAP
set by the discrete angular harmonic `l(l+1)` and the gauge/exterior `W_inf`, **NOT** the cell wall.

**(c) The spectrum ABOVE the floor is a BOX-DISCRETIZED CONTINUUM (the gap collapses as R grows):**
```
 R     gap(omega^2_2 - omega^2_1)
 16    0.105
 32    0.041
 64    0.029
 128   0.025      <- spacing -> 0 as R grows => a continuum band, box-discretized
```
The level spacing falls toward zero with cell size (between ~1/R and ~1/R^2). So the "tower" above the
floor is **the box's own discretization of a continuum** — box-controlled, NOT physical levels.

**(d) The angular ratios are the box's spherical-harmonic ratios:** `omega_l/omega_1 ~ sqrt(l(l+1)/2)`
(1.00, 1.67, 2.25, 2.81 vs 1.00, 1.73, 2.45, 3.16) — the `l(l+1)` centrifugal ladder, not an intrinsic
mass family. Seal BC (Dirichlet vs Neumann) shifts the floor < 1% — not the artifact. Profile-robust
across three smooth native-like `v0`.

---

## 3. THE HONEST SPECTRAL NATURE (assembled)

The time-live non-round native fluctuation operator is a **self-adjoint wave operator** whose spectrum is:

> an INTRINSIC mass-GAP floor `omega^2 = l(l+1) W_inf` (the centrifugal angular barrier, R-independent,
> profile-robust, gauge-set by the exterior `e^{2v0}`), with a BOX-CONTROLLED CONTINUUM band above it
> (level spacing -> 0 as the cell grows).

This is the spectrum of a **scattering / continuum problem with an angular-momentum barrier**, not a
**bound-state tower**. There IS native discreteness in it — but it is the discreteness of the integer
angular harmonic `l(l+1)` (the SAME `l=1 (2l+1) = 3` / area-form `4pi` discreteness already banked as the
CHARGE in B1), now appearing as the gap of a standing wave. It is **NOT a new discrete ladder of bound
masses**, and the only genuinely tower-like structure (the levels above the floor) is box-controlled.

**So the make-or-break lands as: a HALF-OPEN result.** Time-live non-round does what B2/wcc could not — it
gives a live standing-wave operator with an INTRINSIC (non-box) lowest frequency. But that intrinsic
quantity is the already-known angular `l(l+1)` barrier, not a new bound spectrum; the bound tower that
would house generations does not appear, and the continuum above the gap is box-controlled.

---

## 4. NUMERIC CONFIRMATION STATUS (every compromise flagged)

- **Standing-wave modes found:** YES, real `omega^2 > 0` for every l (confirms Finding 2 structurally).
- **Box-control of the lowest mode:** the floor is **INTRINSIC** (R-flat over 64x; profile-robust;
  BC-robust; floor = `l(l+1)W_inf` exactly with Q=0). The band ABOVE it is **box-controlled** (spacing -> 0).
- **GPU/CPU cross-check:** floor agrees to 6e-14 (V100 cuda float64 vs numpy).
- *** SHORTCUT TAKEN (load-bearing, §6): the radial operator uses a GENERIC smooth-bounded native-like
  `v0(r)` (deep negative core -> 0 exterior), NOT the pointwise-exact converged COUPLED `v0` from a full
  time-live metric+matter solve. *** COST: the ABSOLUTE floor value rides on the modeled profile's exterior
  `W_inf` and on whether the true coupled `v0` has the same exterior. The STRUCTURAL conclusions — (i) the
  floor is the intrinsic `l(l+1)` centrifugal barrier, (ii) it is R-independent, (iii) the band above is a
  box continuum — are properties of any sign-definite SL operator with a bounded exterior-asymptoting
  potential and are profile-robust here, so they are trustworthy; the absolute number is not banked.
- *** SHORTCUT TAKEN: the full COUPLED time-live solve (metric a,b + matter Theta + live d_t Theta +
  harmonic balance + omega closure on the native S^2 carrier with Theta free) was NOT built. *** This is the
  Phase-1/2 build (DESIGN §6), a multi-day effort. COST: I confirm the spectral NATURE semi-analytically +
  with a faithful reduced operator; I did not run the production coupled eigensolve. The structural verdict
  does not depend on it (it depends on the sign-definiteness, which B2/wcc proved exactly, + the time term's
  sign, which phase0 proved exactly).
- *** SCOPE: deep inner core (r->0) excluded from the read (FD 1/r^2 strain), per native_matter_step. ***

---

## 5. CLEAN / PARTIAL / NOT-CLEAN + provenance

**Verdict: PARTIAL (a clean structural NON-CLOSURE on the bound-tower question, with one clean POSITIVE
sub-result).**

- **CLEAN positive:** the time-live non-round operator is a genuine self-adjoint standing-wave eigenproblem
  with `omega^2 > 0` and an INTRINSIC (R-independent, box-control-PASSING) lowest frequency — a real
  departure from B2/wcc's dead static operator. Derived natively (Finding 2): the wave term is the
  phase0 vacuum-wave escape (blind-verified physical), not imported.
- **CLEAN negative (the bound tower / generations home):** the intrinsic frequency is the already-banked
  angular `l(l+1)` centrifugal barrier (the charge discreteness re-read), NOT a new discrete bound mass
  ladder; the only tower-like levels (above the gap) are a box-discretized continuum (spacing -> 0).
  So **the time-live non-round carrier does NOT open a new discrete mass spectrum.**
- **Provenance:** NATIVE. The field equation, the `-v_theta^2` term, the time/wave term, and the angular
  `l(l+1)` barrier are all metric-derived (B2/wcc/phase0, blind-verified). No imported Skyrme BC (#61
  honored). No transfer ladder / junction / index import (B2's import list NOT used). The one modeled
  object (the radial `v0` profile) is flagged a SHORTCUT and its conclusions shown profile-robust.
- **Data-blind / anti-numerology:** PASS. No wall numbers; the only constants (`l(l+1)`, `4pi`) are exact
  geometric facts already banked, not fits; no new rational promoted to evidence.

---

## 6. HONEST READ — does the TIME-LIVE NON-ROUND native carrier OPEN a discrete spectrum?

**No — not a new discrete BOUND tower. But it is NOT the same dead end as B2/wcc, and the reason is
informative.** Honest, two-edged, no false convergence:

1. **What genuinely changed (the carrier is NOT dead):** B2/wcc found the phi-angular operator
   sign-definite => "no spectrum" on the STATIC axis. This push shows that on the TIME-LIVE axis the SAME
   sign-definiteness gives a real standing-wave operator with an INTRINSIC lowest frequency (box-control
   PASS on the floor). So "static round = no spectrum" was indeed a slice; the time-live non-round operator
   is alive and has intrinsic structure. Charles's phi-angular hunch has a real carrier here.

2. **Why it still does not house generations (the named obstruction):** the intrinsic content of that
   standing wave is the **angular `l(l+1)` centrifugal barrier** — which is the SAME discreteness already
   banked as the CHARGE (`l=1 (2l+1)=3`, area-form `4pi`). It is not a NEW quantity. The genuinely
   tower-like part (levels above the gap) is a **box-discretized continuum** (spacing -> 0 as the cell
   grows) — box-controlled, not physical. So the operator delivers an intrinsic mass-GAP (one number per
   angular harmonic, = the charge structure) but **no discrete bound ladder of masses** above it. The
   lepton-generation "same charge, different mass" family is still NOT here.

3. **Named obstruction (this push's deliverable):** *the time-live non-round native standing-wave operator
   has an INTRINSIC angular-barrier floor but a BOX-CONTROLLED continuum above it — it supplies a mass-gap
   tied to the (already-banked) charge discreteness, not a new discrete bound-state spectrum.* The
   discretizer for a bound TOWER (a binding well that traps multiple levels independent of R) is still
   MISSING. A drift term (the non-round `-2 v0_theta u_theta`) cannot bind; the source potential about the
   round bg does not (wcc gap > 0); and the time axis converts the damping floor into a standing-wave gap
   but adds only a box continuum above it.

4. **Anti-shortcut honesty:** I did NOT manufacture a spectrum by box-eigenvalues (I explicitly tested and
   FOUND the tower-levels box-controlled and reported them as such), by imports (none used), by freezing
   (the time and angular axes are the live variables of the analysis), or by fitting (data-blind). I did
   take the modeled-radial-profile shortcut (§4) and flagged it; its conclusions are profile-robust. I do
   not narrate convergence: this is one informative tile — time-live revives the operator and gives an
   intrinsic gap, but the bound-tower / generations question remains OPEN with a sharper obstruction.

5. **Where a bound tower could still live (direction, not a result):** a genuine R-independent bound TOWER
   needs a true POTENTIAL WELL (a zeroth-order attractive term binding several levels), which neither the
   drift nor the centrifugal barrier provides. Candidates not built here: (i) the FULLY COUPLED time-live
   solve where the mode's own amplitude back-reacts (a nonlinear breather frequency-amplitude relation
   omega(A) — DESIGN §5.1 candidate, genuinely absent from this linearized read); (ii) the off-diagonal
   ROTATION sector (g_tpsi frame-dragging, phase0 B1) coupling to the wave sector; (iii) a SECOND seal
   (S^2xS^1 integer family, B2 table #9). All UNBUILT. Stated as targets, not convergence.

---

## 7. ONE-LINE SUMMARY

The TIME-LIVE NON-ROUND native carrier **revives** B2/wcc's dead static operator into a genuine
self-adjoint **standing-wave** eigenproblem with an **INTRINSIC, box-control-passing lowest frequency** —
but that intrinsic frequency is the already-banked **angular `l(l+1)` centrifugal barrier** (the charge
discreteness re-read as a mass-gap), and the only tower-like levels above it are a **box-discretized
continuum**; so the carrier supplies a **charge-tied mass-GAP, not a new discrete BOUND mass tower** — the
generations discretizer remains missing, now with a sharper named obstruction (the non-round term is a
drift not a binding well; the time axis adds only a box continuum above the centrifugal gap).

---

## 8. ATTACK HERE (for a blind verifier)

- **Finding 1 (drift not potential):** independently confirm `d/d_eps[-(v_theta)^2] = -2 v0_theta u_theta`
  and that `u'' + (cot th - 2 v0_theta) u'` is self-adjoint in weight `sin th e^{-2 v0}` (so the new term
  is a weight change, not a sign-flip). Is there any way a drift term creates a bound state? (No, for a
  real SL operator — verify.)
- **Finding 2 (sign of the time term):** confirm the non-round l>=2 vacuum wave term enters as `-omega^2`
  with `M>0`, so `omega^2 = -lambda/M > 0` follows from `-L_space>0` (the wcc gap). Check the matter-sourced
  version (`<T_tr> != 0`) gives the same sign (a hyperbolic, not elliptic, time sector).
- **Finding 3 (box-control):** re-run the R-scan with an INDEPENDENT discretization (spectral, not FD);
  confirm (i) floor R-independent, (ii) floor = `l(l+1)W_inf` with Q=0, (iii) band spacing -> 0. THE KEY
  ATTACK: is the floor's intrinsic-ness an artifact of the modeled exterior `W_inf`? Test with a profile
  whose exterior `v0` does NOT go to a constant (if the true coupled solve has a non-flat exterior the
  floor value moves — but its R-INDEPENDENCE should persist, since it is the potential floor not the wall).
- **The load-bearing shortcut (§4/§6):** does using a modeled `v0(r)` instead of the converged coupled
  time-live `v0` change any STRUCTURAL conclusion (floor intrinsic / band box / no bound tower)? Argue
  whether the full coupled solve could introduce a binding WELL absent from the reduced operator (the
  nonlinear-amplitude back-reaction is the one place it could).
- **No-false-convergence check:** confirm the doc does NOT claim a discrete mass ladder, does NOT bank the
  box-continuum levels as physical, and correctly identifies the intrinsic floor as the (already-banked)
  charge `l(l+1)` discreteness rather than a new result.

## STATUS
STRUCTURAL-FIRST complete (sympy-exact Findings 1-2; numeric-confirm Finding 3, GPU/CPU cross-checked).
PARTIAL verdict: clean positive (intrinsic standing-wave floor — the static slice WAS the trap) + clean
negative (no new discrete bound tower; the tower is box-continuum, the floor is the charge barrier).
Native provenance; data-blind; anti-numerology PASS. Two SHORTCUTS flagged (modeled radial profile; full
coupled solve not built) — neither changes the structural verdict. NOT canon. No git commit. Blind
verifier next.

---

## BLIND VERIFIER VERDICT — 2026-06-19 (verifier agent af7895a3a57248863): ALL THREE STAND

Independent re-derivation (from-scratch sympy Christoffel->Ricci->Einstein for Claim 2; own self-adjoint
eigvalsh finite-volume eigensolver for Claim 3 — did NOT trust constructor scripts). Data-blind. No git commit.
Scripts: timelive_nonround_verif_claim{1,2,3}.py; verdict: timelive_nonround_VERIFIER.md.

- **CLAIM 1 (drift, not a binding potential): STANDS.** Variation `-2 v0_theta u_theta` exact (zero residual),
  =0 round (B2 reproduced). `u'' + (cot th - 2 v0_theta)u'` self-adjoint in weight `sin th e^{-2v0}`
  (`w'/w=p`, `w A[u]-(w u')' = 0` identically). ATTACK confirmed: a real self-adjoint 1D drift CANNOT bind —
  `<u,Lu>_w = -INT w (u')^2 <= 0` since `w>0`; drift amplitudes up to 5.0 produce NO positive (bound) eigenvalue.
- **CLAIM 2 (time-live => omega^2>0 standing waves): STANDS.** Negative-definite L_space + positive M +
  hyperbolic `-omega^2` => `omega^2 = l(l+1)W/M > 0`. From-scratch l=2 quadrupole `G_thth`:
  `coeff(h_tt)=r^2 P2/c^2` (nonzero, radiative) and **`coeff(h_tt)/coeff(h_rr) = -1/c^2` EXACTLY** — a
  Lorentzian WAVE (opposite relative sign), NOT diffusion. Matches constructor term-for-term.
- **CLAIM 3 (intrinsic floor + box-controlled continuum, no bound tower): STANDS — CLEANER than reported.**
  The constructor's ~1% floor drift over R=8..512 is a DISCRETIZATION artifact (rmin and h scaling with R);
  with grid held FIXED the floor is R-independent to 5 decimals (l=1: 1.97440; l=3: 9.91471) — a minor
  constructor UNDER-claim. Q=0 floor ~ l(l+1)W_inf; band spacing -> 0 (0.107->0.019); ratios ~ sqrt(l(l+1)/2).
  KEY ATTACKS pass: Q-proxy shifts value but stays R-flat; a NON-asymptoting exterior MOVES the value
  (~2.236) but R-INDEPENDENCE SURVIVES (= local potential floor, not the wall); Dirichlet == Neumann to 5 digits.

- **Over/under-claim audit:** NO over-claims. The doc correctly refuses to bank a discrete mass ladder,
  correctly tags the box-continuum levels and both SHORTCUTS. One UNDER-claim (noisier-than-real floor
  flatness). The one place a bound well could still hide — fully-coupled nonlinear amplitude back-reaction —
  is genuinely unbuilt and correctly left OPEN.

NET BANKED: time-live non-round REVIVES the dead static operator into a real standing-wave problem with an
INTRINSIC floor that IS the already-banked angular `l(l+1)` (charge) barrier, a BOX-CONTROLLED continuum
above it, and NO new discrete bound mass tower. The PARTIAL / half-open framing is honest and verifier-confirmed.
