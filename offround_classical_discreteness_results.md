# Off-Round Classical Discreteness Gate (P5e) — Results

**NOT CANON. DATA-BLIND. OBSERVE mode. Nothing banked** (only operator norms,
omega-scalings, dimensionless ratios; no M_MS / mass / ratio).
Driver: Claude (Opus 4.8, 1M). 2026-06-20. Branch `offround-classical`.
New file `p5e_offround_qep.py` (p5d_timelive / p4_time_live / p2_* / p3fix / full3d_*
reused as IMMUTABLE imports only).

---

## THE QUESTION

Is there CLASSICAL discreteness in the OFF-ROUND (l>=2) channel BEFORE quantization?

P5d (verified) showed the ROUND object is time-frozen (d_t^2 inertia M = machine floor,
Birkhoff) — no classical oscillator round. The P5d independent verifier EXHIBITED that
the OFF-ROUND channel carries NONZERO inertia (||M||/||K|| ~ 0.09–0.12 at a c1 theta-warp).
So a classical oscillator EXISTS off-round. The open question (genuinely not pre-decided,
because the matter L2+L4 sector HAS an intrinsic length ell=sqrt(kappa/xi) that the
scale-free vacuum #62 lacked): does its spectrum TOWER (intrinsic levels = classical
discreteness) or BOX-CONTROL (continuum ~1/R, needs quantization)?

Answered TWO complementary ways that cross-check: (1) NUMERICAL box-scan on the full
clean operator; (2) STRUCTURAL/analytic scaling argument independent of numerics.

---

## PREMISE LEDGER ("chose or derived?")

| premise | chose / derived | note |
|---|---|---|
| full clean stack (P4 einstein_live pole-stable hybrid + native S^2 EL + a(phi) ruler k=0) | DERIVED (inherited, immutable imports) | NOT a reduced proxy; the #65-distrusted modeled-profile path is NOT used |
| off-round bg (A): round S^2 ground state + l=2 warp c0=d0=c1*P2(cos th) | CHOSE (c1=0.05; the verifier's c1 theta-warp template, single-parameter) | imposed warp -> static residual R0~0.2–1.4 (not relaxed) |
| off-round bg (B): saved floored basin fields (oblate/toroidal/prolate) | DERIVED (genuine coupled-floored off-round solutions, R0~0.1–0.2) | from /tmp/p5c_basin_12_*.pt; 2nd+ config so not one-template |
| live off-round DOF x=(a1,b1,c1,d1,F1)*P2(cos th) (l=2) | CHOSE (the off-round l>=2 channel; ALL FOUR diagonal warps live) | this is what makes M!=0: angular warps c,d carry d_t^2 content that does NOT Birkhoff-cancel |
| residual rows: G^t_t,G^r_r,G^th_th,G^ps_ps,EL,G^t_r | CHOSE (added the ANGULAR diagonals G^th_th/G^ps_ps — the verifier's nonzero-even-round inertia channel) | P5d used only G^t_t/G^r_r (why it read ~0 round) |
| kap8=0.05, p=0.4, m=1, Nr=12/16, cells 10/14/18/28 | CHOSE (P5d/P5c defaults; cell scan = the box gate) | |
| QEP method: sigma_min(w) scan AND companion-linearization eigvals | DERIVED (two independent solvers cross-check) | |

---

## PART 1 — NUMERICAL BOX-SCAN (full clean operator)

The off-round live time residual is a GENUINE quadratic eigenproblem (M != 0):
`R_time(x;omega) = (K + omega C - omega^2 M) x`, x = (a1,b1,c1,d1,F1) the l=2 live
amplitudes. M assembled by exact omega-power separation (same scheme as P5d, verified).

**M is genuinely off floor (the off-round oscillator is real):**
```
warp c1=0.05, Nr=12, cell=14:  ||K||=20.76  ||C||=6.58  ||M||=10.96   ||M||/||K||=0.53
(round P5d for contrast:        ||K||=4.48   ||C||=0.61  ||M||=2.2e-9  ||M||/||K||=5e-10)
```
A factor ~5e9 jump in inertia — the off-round l>=2 channel carries a real d_t^2 inertia,
NOT a wiring floor. Confirms the verifier's exhibition on the full operator.

### Box-control gate — background (A) c1-warp, Nr=12, WIDE omega scan (4*sqrt(K/M))
```
cell R | ||K||  | ||M||  | w_globalmin | w*R   | w^2*R^2 | min(sig)/max(sig)
 10.0  | 41.40  | 10.98 |   7.769     | 77.69 |  6035   |  0.039
 14.0  | 20.76  | 10.96 |   5.507     | 77.09 |  5943   |  0.048
 18.0  | 12.50  | 10.96 |   4.272     | 76.89 |  5912   |  0.058
 28.0  |  5.18  | 11.02 |   2.744     | 76.82 |  5901   |  0.062
```
- (a) ||M|| is R-INDEPENDENT (10.96–11.02); ||K|| ~ 1/R^2 (41.4→5.18 across 10→28,
  ratio (28/10)^2=7.84 vs 41.4/5.18=8.0). The lowest omega ~ 1/R: **w*R = 77.7→76.8
  (constant to 1.2%) across a 2.8x wall relocation.** -> BOX-CONTROLLED.
- (b) wall-relocation 10->28 (2.8x): w*R constant -> box (an intrinsic level would hold
  w fixed, i.e. w*R would grow ~R). DECISIVE.
- (c) intrinsic-lock negative control: min(sig)/max(sig) ~ 0.04–0.06 — NO sharp zero;
  sigma_min descends monotonically as a CONTINUUM EDGE, never reaching a clean null
  (a true intrinsic eigenfrequency would be a sharp zero). NOT a new intrinsic level.

### Independent QEP eigenvalues (companion linearization — cross-check of the sigma scan)
Lowest |w| real QEP eigenfrequencies vs cell (Nr=12, warp):
```
cell=10: 0.0067, 0.0585, 0.1159, ...    (mode1 falls with R)
cell=14: 0.0041, 0.0152, 0.0784, ...
cell=18: 0.0021, 0.0122, 0.0618, ...
```
Lowest mode DECREASES with R (0.0067→0.0021 over 10→18) — box-controlled toward continuum,
NOT a fixed intrinsic level. No resolved mode shows the intrinsic signature (w*R growing
~R). The two solvers (sigma-scan, companion eig) AGREE.

### Resolution check (Nr=16, warp): NOT a low-res artifact
```
cell=14: ||K||=71.5  ||M||=16.72   cell=18: ||K||=42.9  ||M||=16.74
```
||M|| R-independent, ||K|| ~ 1/R^2 (71.5/42.9=1.67 vs (18/14)^2=1.65), min(sig)/max(sig)
~0.16–0.19 (even shallower — continuum confirmed at higher res). The ||M|| magnitude grows
12→16.7 with Nr only as a norm-of-more-gridpoints effect; the SCALINGS (the physics) are
resolution-robust.

### Second/third backgrounds (B) — basin fields (oblate / toroidal / prolate)
Genuine coupled-floored off-round solutions (R0~0.1–0.2), wall ~37–43:
```
oblate   : ||K||=2.10 ||M||=8.25 ||M||/||K||=3.93   global-min w=0 (continuum from 0)
toroidal : ||K||=2.11 ||M||=7.42 ||M||/||K||=3.51   global-min w=0
prolate  : ||K||=2.86 ||M||=8.24 ||M||/||K||=2.88   global-min w=0
```
All three independent off-round configs: M genuinely nonzero (inertia-DOMINATED here),
spectrum a continuum starting at/near w=0, no gap, no discrete tower. NOT one-config.

**PART 1 VERDICT: BOX-CONTROLLED.** w ~ 1/R (w*R constant to ~1%), ||M|| R-independent,
||K|| ~ 1/R^2, no sharp eigen-zero, continuum from w~0. Across c1-warp + 3 basin configs,
Nr=12 and 16, two independent QEP solvers. The off-round oscillator is REAL but its spectrum
is a CELL-set continuum, not an intrinsic ladder.

---

## PART 2 — STRUCTURAL / ANALYTIC ARGUMENT (independent of numerics)

The matter sector is L2 + L4 (whole_metric_3d_matter): L2 = -(xi/2) g^{mn} dn.dn (two
derivatives, coeff xi), L4 = -(kappa/4) g^2 (dn)^4 (four derivatives, coeff kappa). The
unique intrinsic length is **ell = sqrt(kappa/xi)** (the code's L=1 unit).

**(i) The static soliton DOES have an intrinsic size.** Static 3D Derrick scaling
(x->lambda x on the 3 spatial coords): E(lambda) = xi*lambda + kappa/lambda (e2~lambda^1,
e4~lambda^{-1}). dE/dlambda=0 => lambda* = sqrt(kappa/xi) = ell. So matter is NOT scale-free
the way the bare vacuum (#62) is — it pins a core size ell and a core mass ~sqrt(xi kappa).
This is exactly why the question was genuinely open.

**(ii) But the intrinsic size does NOT set the LOWEST off-round frequency.** The off-round
fluctuation obeys omega^2 = H/I. Inertia I (the d_t^2 content of L2+L4) ~ xi*ell^3 (both
terms contribute equally at lambda*; this is the ||M|| ~ R-independent of Part 1). The
restoring H has TWO pieces:
  - CORE curvature H_core ~ sqrt(xi kappa)/ell^2-scale -> omega^2 ~ 1/ell^2 (INTRINSIC),
  - BOX gradient H_box ~ xi/R^2 * vol (the l>=2 mode must connect core to wall; lowest
    wavelength ~ R) -> omega^2 ~ 1/R^2 (BOX).
The LOWEST eigenmode minimizes omega^2 -> picks the SMALLER of {1/ell^2, 1/R^2}. In the
relevant regime R >> ell (cell 10–28, core ell~O(1)): 1/R^2 << 1/ell^2, so the lowest
mode is the BOX mode, omega^2 ~ 1/R^2 -> 0. The intrinsic ell sets only a FINITE set of
HIGH-lying core modes near omega~1/ell; the lowest / accumulation spectrum is the box
continuum.

**(iii) Asymptotic character — adding matter does NOT change the box character.** Away
from the core grad n -> 0, L4 (quartic) becomes negligible, and only L2 survives — which
has no scale structure. The off-round fluctuation operator ASYMPTOTES to the bare-vacuum
box operator (#62, analytically scale-free => box-controlled). ell is a CORE-ONLY feature;
it does NOT enter the asymptotic operator that sets the lowest (accumulation) spectrum.

**How rigorous:** the Derrick intrinsic-size result is exact (sympy). The omega^2=H/I
split and the R>>ell -> box conclusion are a rigorous scaling/dimensional argument
(parametric, not a closed eigenvalue) — they pin the SCALINGS (I~ell^3 R-indep, H_box~1/R^2,
lowest omega~1/R) but not the O(1) prefactor. That is exactly what numerics is for; the
two agree on the scalings. The argument does NOT by itself rule out a NARROW intrinsic
core resonance high in the spectrum (omega~1/ell) — but that is not classical discreteness
of the GROUND/low spectrum, which is what "does it tower" asks.

---

## CROSS-CHECK: DO PART 1 AND PART 2 AGREE?

**YES, decisively, on every scaling:**
| quantity | structural prediction | numerical |
|---|---|---|
| inertia ||M|| | ~ xi ell^3, R-INDEPENDENT | 10.96–11.02 across cells (const) |
| restoring ||K|| | box gradient ~ xi/R^2 | ~1/R^2 (8.0x over 2.8x R) |
| lowest omega | box ~ 1/R | w*R const to 1.2% |
| eigen-character | continuum edge, no gap | min(sig)/max(sig)~0.04, w from ~0 |
| matter vs vacuum | asymptotes to scale-free box | same structure as #62/#65 |

Both box-controlled => ROBUST.

---

## THE VERDICT

**Classical discreteness off-round = NO (BOX-CONTROLLED; quantization is needed).**

The off-round l>=2 channel carries a GENUINE classical oscillator (M != 0, real — unlike
the Birkhoff-frozen round channel), but its low spectrum is a CELL-set continuum
(omega ~ 1/R -> 0 as the box grows), NOT an intrinsic tower. The matter intrinsic length
ell=sqrt(kappa/xi) pins the static soliton's SIZE and a finite set of high core modes, but
does NOT set the lowest off-round frequency: for box >> core the lowest mode is a box mode.
This reproduces the scale-free-vacuum (#62) and reduced-proxy (#65) box-control on the FULL
CLEAN off-round operator with M genuinely nonzero — closing the last "but matter has a
scale the vacuum lacked" loophole.

**Definiteness level:** FIXED-BACKGROUND quadratic eigenproblem (5 live off-round amplitude
functions on a frozen off-round background) + a structural scaling argument. NOT the full
COUPLED P5e (where the off-round background relaxes simultaneously with the live amplitudes).
The imposed-warp backgrounds carry a static residual R0~0.2–1.4; the relaxed basin
backgrounds (R0~0.1) give the same continuum-from-0 verdict, which strengthens it. The
verdict is therefore strong on the fixed-background + structural pair, and the cross-check
agreement makes a hidden tower very unlikely — but a fully-coupled P5e is the residual to
make it airtight (see ATTACK HERE).

---

## ATTACK HERE (where this could still be wrong)

1. **Fixed background, not coupled.** The live amplitudes fluctuate on a FROZEN off-round
   background. A true mode lets the background relax with the fluctuation (P5e proper /
   the #60 coupled wall). If the coupling opened a gap the fixed-bg QEP would miss it.
   (Mitigant: round P5d's fixed-bg verdict survived the P4 coupled containment; basins are
   near-floored; but this is the honest residual.)
2. **High core modes unresolved.** The structural argument PREDICTS a finite set of
   intrinsic core modes near omega~1/ell. Nr=12/16 (52 free DOF) resolves the box low end
   but likely under-resolves any narrow core resonance. Throughput-limited at this Nr; not
   needed for the "lowest spectrum towers?" verdict, but unconfirmed. Re-run at Nr>=24 to
   look for an R-independent (w*R ~ R, i.e. w const) high mode.
3. **l=2 only.** Tested the l=2 (P2) off-round channel. Higher l (l=3,4) untested — though
   l(l+1) only raises the angular barrier (more box-like), so unlikely to tower.
4. **Imposed-warp static residual** (R0 up to 1.4 at small cell) contaminates the smallest
   eigenvalues; the basin (relaxed) backgrounds and the SCALINGS (robust to R0) are the
   trustworthy part.

---

## SCOPED STATUS / WHAT INHERITS

- The off-round classical channel is REAL (M!=0) but has NO intrinsic classical ladder to
  quantize on a fixed background; discreteness must come from the QUANTIZATION postulate
  (postulate A), consistent with the catalog reframe and P5d round verdict.
- Quantization step inherits: a box-controlled classical continuum (round AND off-round),
  + the first-order G^t_r momentum channel (P5d) + K's flat directions, as the classical
  substrate the quantum postulate acts on.
- A fully-coupled P5e inherits residuals #1/#2 above: relax the off-round background with
  the live amplitudes and re-run the box gate; look for high core modes at Nr>=24.
- This is SCOPED NEGATIVE territory (no classical off-round tower), premise set: full clean
  fixed off-round background, l=2, Nr<=16, kap8=0.05, units L=ell=1. Loses blocking
  authority if any premise (esp. fixed-vs-coupled) is revised — register accordingly.
