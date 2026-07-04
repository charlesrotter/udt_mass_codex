# D2c — Route-B mixing-term discharge + the G|P composite condition set

**Date:** 2026-07-04. **Stage:** D2c of `microphysics_D2_two_regime_MAP.md` (APPROVED contract;
gate (a) = the Z=8/Route-B mixing-term tension, then the G|P E1-analog). **Scripts:**
`d2c_part1_mixing.py` (sympy, 25/25 PASS) + `d2c_part2_gp_conditions.py` (sympy, 22/22 PASS).
Purity harness `python3 -m pytest tests/` = 32 passed / 1 xfail (unchanged). **Status:
PROVISIONAL — derivation pass only; blind adversarial verifier NOT yet run (owed before any
banking); NOT committed.** Data-blind (no observational numbers used anywhere below; the
Δφ=ln 1101 anchor is *not* an input to any result here). Everything is scoped to
**round-static, diagonal, areal, concentric** (inherited CHOSE ×4, canon C-2026-06-18-1 +
E1 posture) — no claim is a frame verdict.

---

## PART 1 — THE Z=8 / ROUTE-B MIXING-TERM TENSION: ADJUDICATED

**Verdict: DISCHARGED-INCLUDED (bulk) + DISCHARGED-VANISHES (at the folds) + the tension's
practical half CONFIRMED: carrying Z=8 without the mixing term is NOT Route B and never can be.**
Precisely, four sub-verdicts, each CAS-exact:

### 1.1 The mixing term does NOT vanish in round-static bulk (DISCHARGED-INCLUDED)

Sources: the Route-B package `√h[4φ'² + 2e^φKφ']`, Z_φ=8 and the mixing term "an INSEPARABLE
package" (`native_geometric_action_results.md:74-78, 123-126`); the tension statement
(`f_rtheta_free_field_MAP.md:116-121`; carried `universe_cell_fold_jc_sigma_results.md:70-71,114`).

Round reduction (h=ρ²Ω): `2√h e^φKφ' = 4ρρ'φ'·sinθ` per steradian (M1d), using the exact identity
`(√h)' = √h e^φK` (M1c). Two structural facts:

- **Branch-blind:** `e^φKφ'` is EXACTLY shift-invariant (K∝e^{-φ}), so the mixing term needs no
  W_χ compensator and takes the SAME form in G and P (M2). It is a kinetic-sector object, not an
  angular-extrinsic one.
- **The corrected round-static EOMs (Route B, per-4π reduced):**

      L̄_P^B = 4ρ²φ'² + 4ρρ'φ' + 2 − 2e^{−2φ}ρ'²   (+ matter, unchanged)
      L̄_G^B = 4ρ²φ'² + 4ρρ'φ' + 2 − 2ρ'²

      φ-EOM (P):  (8ρ²φ' + 4ρρ')' = 4e^{−2φ}ρ'²        [mixing adds −4(ρρ')' to the EL; M3a,b]
      ρ-EOM (P):  ρ'' = 2φ'ρ' + e^{2φ}ρ(φ'' − 2φ'²)     [mixing adds −4ρφ''; M3c,d]
      φ-EOM (G):  (8ρ²φ' + 4ρρ')' = 0                   [conserved Φ_B; M4a]
      ρ-EOM (G):  ρ'' = ρφ'' − 2ρφ'²

  Neither added piece is identically zero (M3b,c). **The current live system (Route-A structure,
  any Z including 8) is NOT Route B — the omission is a real dynamical difference, not a
  relabeling.** The T3-header re-tag ("Z=8 = Route-B's value carried as a Route-A probe, NOT
  derived", `cell_solver_universe_T3.py:12-18`) remains the correct posture for everything banked.

- **Field-redefinition identity (the clean way to see the difference):** with
  `φ̃ ≡ φ + ½ln ρ`, the Route-B kinetic block `4ρ²φ'² + 4ρρ'φ' ≡ 4ρ²φ̃'² − ρ'²` exactly (M5).
  So round-reduced Route B = Route-A Z=8 kinetics **in the shifted field φ̃** MINUS an extra ρ'²
  gradient term (P: total −(2e^{−2φ}+1)ρ'²; G: −3ρ'²). Route B is not a rescaled Route A.

- **NEW (flagged for PONDER, out of this task's scope): Route B deforms the vacuum.** Flat
  (ρ=r, φ=const) FAILS the Route-B G φ-EOM (residual −4; M4b); the Route-B G "flat-analog" family
  is `ρ = ar+b, φ = φ₀ − ½ln ρ` (M4c). The mixing term sources φ on flat angular geometry. This
  is a large observable handle on the fork (macro constraints) — a consilience lever, exactly
  what `native_geometric_action_results.md:90` anticipated. Not adjudicated here.

### 1.2 At the banked universe-cell folds the mixing contribution VANISHES (DISCHARGED-VANISHES there)

The banked one-line claim ("fold VALUES unchanged", `universe_cell_fold_jc_sigma_results.md:70-71`)
is now a derivation:

- **Even fold:** the Route-B momenta are `Π_φ^B = 8ρ²φ' + 4ρρ'`, `π_ρ^B = −4e^{−2φ}ρ' + 4ρφ'`;
  the natural-BC system Π_φ=π_ρ=0 is nondegenerate (det = −32ρ²e^{−2φ}−16ρ² ≠ 0) and still forces
  exactly `φ'=ρ'=0`, values free (M6). E1's even-fold core carries to Route B.
- **Odd fold (mirror-image partner, D1 machinery):** the mixing contributions CANCEL IN THE JUMPS:
  `[π_ρ] = 8cosh(2φ_s)ρ'_s` — identical to Route A, any φ_s — so **ρ'(r_s)=0 survives**; and with
  ρ'_s=0, `[Π_φ] = −8ρ_sρ'_s ≡ 0`, so **φ'(r_s) stays free** and the fold flux is
  `Φ_B(r_s) = 8ρ_s²φ'_s` = the Route-A Z=8 form (M7a,b). The banked fold PINS and fold VALUES are
  Route-B-robust; the interior PROFILES between the folds are not (§1.1).
- **H-machinery intact:** `H^B = H^A(Z=8) + 4ρρ'φ'` (vanishing wherever ρ'=0), conserved
  (autonomy, M8a,b); at the even core `H^B = E_ang − 2`, so the transversality closure
  **E_ang(core) = 2 is Route-blind** (M8d). The Route-B flux law is `Φ_B' = 4e^{−2φ}ρ'² ≥ 0` with
  `Φ_B = 8ρ²φ̃'` — **monotonicity migrates from φ to φ̃ = φ + ½ln ρ** (M8c). This one change is
  load-bearing in Part 2 (§2.6).

### 1.3 At a G|P seal the mixing term COUPLES the junction conditions (the part (b) answer)

Route-A JCs decouple (JC1 ⇒ φ' continuous; JC2 ⇒ ρ'_G = e^{−2φ_s}ρ'_P). Under Route B, because
Π_φ^B carries ρ' and π_ρ^B carries φ', the pair is a coupled 2×2 system — uniquely solvable (M9):

    JC1^B:  [8ρ²φ' + 4ρρ'] = 0   ⇔   [8ρ²φ̃'] = 0      (the Route-B dilation flux = the φ̃-flux;
                                                          φ̃' is what is continuous, M9c)
    JC2^B:  [−4W̃ρ' + 4ρφ'] = 0   (W̃ = e^{−2φ} on P, 1 on G)
    ⇒  ρ'_G = (2e^{−2φ_s} + 1)/3 · ρ'_P ;   φ'_G − φ'_P = (1 − e^{−2φ_s})ρ'_P/(3ρ_s)   (M9a,b)

  **φ' itself JUMPS at a Route-B G|P seal** (unless φ_s=0 or ρ'_P=0). The public charge under
  Route B is `q_B = 8ρ²φ̃'`, continuous through everything.

### 1.4 Adjudication for the gate

- Nothing banked on the live path rides on Route B: fold pins/values, E_m(core)=2, the budget
  identity structure are Route-B-robust (§1.2); interior profiles/ladder numerics are Route-A
  objects at stated Z (already so tagged). **The gate is discharged: Part 2's condition set below
  carries Z as "Route A, Z free (probe values {1,8})" and separately states every Route-B form.**
- **The residual fork is physical and now sharper:** Route B ≠ Route A + Z-choice; it deforms the
  vacuum (M4b,c), couples the JCs (§1.3), and relaxes the φ-monotonicity to φ̃ (§1.2) — the last
  point flips Part 2's Route-A no-go into an open question under Route B (§2.6). The fork remains
  a consilience call (Charles); the math alone still does not select.

---

## PART 2 — THE G|P COMPOSITE CONDITION SET (the E1-analog under the weight-jump)

Objects: particle cell `[0, r_p]` = Branch P with the derived native S² L2+L4 carrier (canon
C-2026-06-14-1; reduced Lagrangian = Step-0 V2, `f2d_virial_step0_results.md:34-38`); at `r_p` a
shared movable seal to **Branch G** (`W_χ = e^{2φ}`; `seal_matching_junction_results.md:14-40`;
φ, ρ continuous — the stated JC2 assumption, CHOSE-cited). Architectures per the D2 MAP table:
**A1** = P-cell | G | odd fold; **A2** = P-cell | G | P-shell (T3 ambient `L_m=−U(ρ)`) | odd fold.
Corner machinery for shared movable interfaces = `embedded_cell_closure_H_amb_results.md:19-38`
(banked, blind-verified, derived there for general unequal Lagrangians — covers G|P directly);
specialized in CAS here. Matter is represented at reduced-radial level by a stand-in amplitude
with `L̄_m = −½A(ρ,a)a'² − V(ρ,a)`, A>0, ρ'-free, φ-blind — exactly the banked carrier's corner
structure (`cell_solver_f2d.py:202-207`: I_r and I_4r are both positive quadratic forms in f_r);
the θ-resolved statements cite E1's K1/K1' (blind-verified).

### 2.1 The particle core (r = 0) — E1's even fold carries over UNCHANGED

Stationarity alone: all momenta vanish ⇒ `φ'(0)=ρ'(0)=0, f_r(0,θ)=0`, values `φ_c, ρ_c` free
(G2; Route B identical by M6). The E1 §3 core-class exclusions (φ→−∞ excluded by the flux law;
ρ→0 excluded; power-law cores excluded) used ONLY interior-P structure + finite seal flux — all
architecture-independent — so they carry over verbatim under Route A. **Route-B scope note
(honest):** the even-fold BCs and the flux law carry (M6, M8c), but the E1 exotic-core exclusion
sweep has NOT been re-run against the Route-B EOMs — owed if Route B is ever promoted.

### 2.2 The G|P seal set at r_p (the C1a/C1b/C1c/C2 analogs) — Route A

    C1a  [Zρ²φ'] = 0        ⇔  φ'_G = φ'_P                (JC1; kinetic identical both branches)
    C1b  [π_ρ] = 0          ⇔  ρ'_G = e^{−2φ_p} ρ'_P      (JC2 weight-jump; direction = banked
                                                            solver-header form, G3a)
    C1c  π_f(r_p,θ) = 0     ⇔  f_r(r_p,θ) = 0  ∀θ         (one-sided natural BC: the carrier ends
                                                            mirror-flat; SAME as E1 — the carrier is
                                                            absent on the G side either way, G3b)
    C2   [H] = 0            ⇔  **E_ang(r_p) = 2x(1−x)·ρ'_P²,   x ≡ e^{−2φ_p}**        (G3c)

**The E1 "geometry cancels" step does NOT carry over — as suspected.** At a P|P seal the
gradient terms cancel identically and C2 collapses to the local match `E_ang = U(ρ_p)` (G7 —
reproduced as the control: that cancellation was a same-weight accident). At a G|P seal the W_χ
jump leaves an irreducible **gradient residue**: the local angular energy must equal a
weight-mismatch term built from the seal's ρ-gradient. Two immediate teeth:

- `2x(1−x) ≤ ½` for all x>0 (max at x=½, i.e. φ_p=½ln2) ⇒ **|ρ'_P(r_p)| ≥ √(2E_ang) ≥ √(2ξN)**
  (with E1's K12 floor, cited) — a G|P seal needs a hard ρ-gradient on the P side (G4b).
- Sign: RHS > 0 **iff φ_p > 0** (G4a). This is the load-bearing fact of the whole build:

### 2.3 THE SIGN OBSTRUCTION — the Route-A G|P composite closes NOWHERE (derived, scoped)

Chain (each link CAS-verified, assembly G4c):
1. Cell: `Φ = Zρ²φ'` has Φ(0)=0 (even core) and `Φ' = 4e^{−2φ}ρ'² ≥ 0` (matter-independent —
   both media φ-blind; G1a) ⇒ φ' ≥ 0 in the cell and `q = Φ(r_p) ≥ 0`.
2. G-layer: `φ' = q/(Zρ²) ≥ 0` (G1b). A2's P-shell: same flux law, Φ(r_q)=q≥0 ⇒ φ' ≥ 0.
3. Odd fold: `φ(r_sU) = 0` (banked derived pin) ⇒ **φ ≤ 0 everywhere inside — in particular
   φ_p ≤ 0 and φ_q ≤ 0** (equality only for the all-flat q=0 configuration, which forces ρ'≡0 in
   the cell and hence E_ang(r_p)=0 — impossible for N≥1).
4. C2 at r_p needs φ_p > 0 (§2.2). Contradiction.

**Scoped negative:** *round-static, source-free (Class-A-embedded) seals, φ,ρ continuous,
Route-A structure (any Z>0 — VERIFIER-CORRECTED: the flux-law chain needs Z>0; a Z<0 ghost kinetic inverts the obstruction; all banked probes are Z∈{1,8}), L2+L4 carrier with E_ang>0, even core, φ(outer fold)=0 (twisted-fold escape: see verifier record): the G|P
particle composite — A1, A2, and ANY interleaving of source-free vacuum-G and φ-blind-P segments
between r_p and the fold — admits NO closure.* Note the strength: the C2 collapse is independent
of the H-level (G3d), so this does NOT ride on the free-fold/transversality posture — only on the
corner conditions at r_p plus the monotonicity chain. The same obstruction hits A2's far interface
independently (`U(ρ_q) = 2x(1−x)ρ'_shell²`, same form — G5 — needing φ_q>0 or U(ρ_q)<0; the banked
fundamentals have U>0 throughout).

**Named escapes (honest, in-frame first):** (i) **Route B** — the only in-frame escape that costs
no new posit: monotonicity migrates to φ̃, giving `φ_p ≤ ½ln(ρ_sU/ρ_p)`, which is POSITIVE iff ρ
grows seal→fold (G9; necessary, not sufficient) — **the G|P architecture is Route-A-impossible
but Route-B-open: a structural discriminator between the routes, exactly the consilience lever
the fork was waiting for**; (ii) Class-B seal source `S_seal ≠ 0` at r_p (Charles's open call,
MAP gate (c)) — C2 gains a seal-energy term that must supply `E_ang + 2x(x−1)ρ'_P² > 0`;
(iii) leaving round-static (ω≠0, off-round, time-live — pre-named next freedoms);
(iv) discontinuous φ at the seal (violates the stated posture — flagged only). A fifth
configuration the MAP's table does not cover — a G-CORE architecture (G inside, P outside) —
is NOT derived here; **STOP-flagged** for the MAP owner rather than silently swept.

### 2.4 The far side + the G-layer's exact structure

- **A1 (G runs to the universe seal):** the odd fold is EXACT for Branch G (banked D1 PONDER-tag —
  its natural home). Fold set: `φ(r_sU)=0` (essential), `ρ'(r_sU)=0` (mirror-partner jump),
  `H_G(r_sU)=0` (transversality, free position — same CHOSE posture as canon E_m(core)=2).
- **The vacuum G-layer is semi-analytic** (G6): on-shell `H_G = q²/(2Zρ²) − 2ρ'² − 2`; with
  H_G=0, **(ρ²)'' = −2 exactly** (ρ² a downward parabola whose apex IS the fold, since apex ⇔
  ρ'=0) and `φ = φ_p + (q/Z)∫dr/ρ²`. At the fold, ρ'=0 ∧ H_G=0 forces `(Z/2)ρ_s²φ'² = 2`, i.e.
  **q = 2√Z·ρ_sU — the banked T2 window CEILING exactly SATURATED** (G6c): a matterless fold sits
  at the ceiling; the banked universe cell sits below it precisely because its fold carries
  matter (`U(ρ_s) = 2 − q²/(2Zρ_s²)`). A clean consilience between the G-layer and the T2 window.
- **A2 (second interface at r_q):** the shell-side condition set at r_q is C1a/C1b (weight-jump
  direction now G-inside/P-outside, same relation) + `C2_q: U(ρ_q) = 2x(1−x)ρ'_shell²` (G5) —
  the weight-jump residue is interface-universal (E_ang at a carrier seal, U at an ambient seal).
  Then the shell runs to the standard banked odd fold.

### 2.5 H-conservation / the criticality migration — SURVIVES the branch change

Branch G's different symmetry structure (global φ→φ+λ ⇒ its own conserved flux q) is EXTRA
structure, not a replacement: every segment (cell, G, shell) is r-autonomous, so each conserves
its own H (G8-cell/G/shell); the corner condition at every movable seal is H-CONTINUITY
(branch-blind, from the banked two-domain machinery); transversality at the free outer fold sets
H=0 there. The chain `0 = H(fold) = H_shell = H_G = H_cell` then delivers, at the even core,
**E_ang(core) = 2 — the same critical closure, through any number of G|P interfaces, under both
routes** (G8-core; Route B via M8d). What Branch G adds is that BOTH H and q are constants of its
segment (in P, q is monotone instead — the flux law). The criticality migration of E1 §2 is
architecture- and branch-robust; only its REACHABILITY is killed by §2.3 under Route A.

### 2.6 The ambient-selects-size scale pin — SURVIVES IN FORM, CHANGES CARRIER, and (Route A) dies of unreachability

E1/P|P: the ambient pins the cell through position-dependent local data — C1 gradients + C2's
`U(ρ_p)`. At a G|P wall there is no local matter value to match; Branch G is scale-free, shift-
symmetric, matterless. What replaces the local pin is the **G-layer's integrated global tie**:
`φ_p = −(q/Z)∫_{r_p}^{r_sU}dr/ρ²` (< 0 for q > 0 — the quantitative face of the obstruction) plus
the fold-saturation `q = 2√Z ρ_sU`. So the pin **changes form from local (station value) to
global (the Coulomb run to the fold)** — and under Route A that global tie is exactly what makes
the C2 sign unreachable. Under Route B the same global tie reads in φ̃ (`q_B = 8ρ²φ̃'` constant),
and the pin's sign question becomes the geometry question ρ_sU vs ρ_p (G9).

### 2.7 Counting (conditions vs unknowns) — BOTH architectures are SQUARE

Shooting from the core; brackets/carrier params fixed per run as in E1 §4. M = θ-modes of the
core profile g(θ)=f(0,·).

| | unknowns | conditions | square? |
|---|---|---|---|
| **A1** | φ_c, ρ_c, g[M], r_p, r_sU = **M+4** | r_p: C1c [M] + C2 [1] (C1a/b consumed by the shot); r_sU: φ=0, ρ'=0, H_G=0 [3] = **M+4** | **YES** |
| **A2** | + r_q = **M+5** | + C2_q [1] at r_q (C1a/b consumed) = **M+5** | **YES** |

Identical bookkeeping to E1's P|P composite (M+4 vs M+4): the weight-jump does not change the
count — G|P seals consume the same conditions as P|P seals. **Square ≠ nonempty:** under Route A
the square system is EMPTY by §2.3 (a real-solvability obstruction, invisible to counting);
under Route B the count is the same (the coupled JCs still uniquely determine the outgoing shot,
M9) and emptiness is OPEN. No Δφ-anchor row appears because the anchor was never imposed (§ head;
in a real run the E1 ledger-#5 treatment would apply unchanged).

### 2.8 What crosses the interface vs what is P-locked (the MAP's Q2, stated precisely)

**Crosses (continuous/conserved through G):** the values (φ_s, ρ_s); the dilation flux
`q = Zρ²φ'` (Route B: `q_B = 8ρ²φ̃'`) — the particle's public charge, constant across the entire
G-layer (G1b), Gauss-visible arbitrarily far; the Hamiltonian level H (corner-continuous, §2.5) —
i.e. the criticality budget. These are exactly TWO scalars + the shared values: **a G-layer
transmits nothing else.**

**P-locked (terminates at r_p):** the carrier field f itself (C1c ends it mirror-flat ∀θ; no
θ-dependent junction survives); its energy E_ang (enters only the LOCAL C2 row); its χ-pinning
role (a medium whose matter pins χ is P by the switch criterion — the E1 #8 content-assignment
CHOSE is here CONSISTENT with, though still not derived from, `gp_switch_criterion` — carrying a
carrier into G would contradict the branch definition); its φ-coupling (P's e^{−2φ} source).

**The D1 survivors' precise status:** the winding degree N is a boundary/topology label of the
cell (pole BCs), branch-independent as ALGEBRAIC content — but across a G-layer it is carried
ONLY as an imprint on the two transmitted scalars (q, H) and the seal values; no field crosses.
"The invariant angular sector links the regimes" is realized as: **the algebra crosses, the
carrier does not.**

---

## Premise ledger (chose-or-derived; every fixed thing tagged)

| # | Premise | Tag |
|---|---------|-----|
| 1 | Round + static + diagonal + areal | **CHOSE ×4** (inherited, canon C-2026-06-18-1) |
| 2 | Concentric composite | **CHOSE** (E1 scope; off-center = E2+ 3-D matching, cited refusal) |
| 3 | φ, ρ continuous at every seal | **CHOSE-cited** (JC2 stated assumption / orbifold posture, `seal_matching_junction_results.md:39-40`) |
| 4 | Source-free seals (no S_seal; Class-A-embedded) | **CHOSE-cited** (E1 #9; Class B = named escape, Charles's open call = MAP gate (c)) |
| 5 | Seal positions r_p (and r_q) free variables of the action | **CHOSE** (banked embedded posture, E1 #10) |
| 6 | Outer fold position free (transversality H=0) | **CHOSE** (banked free-endpoint posture — same premise canon E_m(core)=2 rides on); NOTE: §2.3's obstruction does NOT ride on it (G3d) |
| 7 | Carrier = L2+L4 only; (ξ,κ) free-explored; N free integer | **THEORY** (canon C-2026-06-14-1 + refinement) |
| 8 | Carrier confined to [0,r_p] | **CHOSE** (E1 #8) — now noted CONSISTENT with the derived switch criterion (a χ-pinning medium is P), still not itself derived |
| 9 | Ambient (A2 shell) = potential-only φ-blind U(ρ), T3 slice family | **CHOSE** (per banked bracket; `cell_solver_universe_T3.py:8`) |
| 10 | Z shared across all media; Route A: Z FREE (probe {1,8}) | **THEORY** (one action) / **FREE-explored**; Route B: Z=8+mixing = the derived inseparable package (Part 1) |
| 11 | W_χ = e^{2φ}(G) / 1(P) | **DERIVED** (banked, `native_geometric_action_results.md:15-17`) |
| 12 | Mirror-image partner at the odd fold | **CHOSE** (= closed-cell premise, banked D1) |
| 13 | Reduced-radial matter stand-in `−½Aa'²−V` for corner algebra | **DERIVED-faithful** (matches the banked carrier's quadratic-f_r, ρ'-free, φ-blind corner structure; θ-resolved C1c = E1 K1/K1', cited not re-derived) |
| 14 | q ≥ 0 | **DERIVED** (flux law + even core; G1a, G2) |
| 15 | All EOMs, JCs, C2 collapses, sign lemma, G-layer closed form, counting rows | **DERIVED** (CAS 25/25 + 22/22) |
| 16 | E_ang > 0 floor (E_ang ≥ ξN + κN²/2ρ²) | **DERIVED-cited** (E1 K12, blind-verified) |

## Standing for the verifier (attack surface, named)

(a) the C2 collapse signs at G|P — the JC2 weight-jump DIRECTION is load-bearing (flip it and the
obstruction inverts to φ_p<0-required); (b) the monotonicity chain §2.3 (esp. that no φ-blind
matter can source φ and that the G-layer preserves q); (c) the H-level independence of the C2
collapse (G3d); (d) the Route-B odd-fold jump cancellation (M7) — it underwrites "banked fold
structure Route-B-robust"; (e) the reduced matter stand-in's faithfulness (ledger #13); (f) the
counting (§2.7), esp. that C1a/b are consumed not counted; (g) the M4b/M4c Route-B vacuum
deformation (a big claim about the fork — verify independently).

## LAB-LOG

- 2026-07-04: `d2c_part1_mixing.py` 25/25 PASS; `d2c_part2_gp_conditions.py` 22/22 PASS (one
  check initially FAILED on a symbol-assumption artifact — rho_s declared real-not-positive made
  sympy return ± roots in G6c; fixed by checking the identity directly, not the physics).
  pytest 32/1xfail. Single process, seconds each, no solves, no background polling. Data-blind.
  **NOT committed; blind adversarial verifier pass OWED before any banking** (verifier-before-
  record). Forks STOP-flagged for the MAP owner: the G-core architecture (not in the MAP table,
  not derived); the Route-B vacuum-deformation consilience lever (PONDER with Charles).

---
## VERIFIER RECORD (blind adversarial pass — agent a9cfb0141acd701ee, 2026-07-04): ALL ATTACKS HOLD + TWO CORRECTIONS (applied)
**Part 1 fully confirmed by independent re-derivation** — incl. the high-stakes chain: the
odd-fold jump cancellation [π_ρ]=8cosh(2φ_s)ρ'_s identical in both routes ⇒ **all banked fold
pins + E_ang(core)=2 are ROUTE-B-ROBUST (verified)**; the shift identity (Route B = Route-A Z=8
kinetics in φ̃=φ+½lnρ minus ρ'²); flat-fails-Route-B-G exact, flat-analog family solves both
Route-B G EOMs (cross-doc lock with D2b-E3's slaved-φ).
**Part 2, the sign obstruction, attacked hardest and HOLDS AS SCOPED:** C2 residue
E_ang(r_p)=2x(1−x)ρ'_P² re-derived from the verifier's own two-domain corner assembly; JC2
direction confirmed by two independent routes; H-level independence CAS-proven (was a logic
assertion); the φ_p≤0 chain's premise ride made exact: even core + φ-blind matter + source-free
seals + φ(outer fold)=0 + **Z>0 (correction 1, applied inline)**. **Correction 2: the escape
enumeration must include D2b-E2's twisted folds** — for architecture A1 the outer fold ends a
G-layer where φ→2a−φ is exact for every a; if Charles admits twisted folds, φ(r_sU)=a>0 breaks
link 3 FOR A1 (A2 stays killed — its fold ends a P-shell where no a works). The scoped negative
stands (φ(fold)=0 is an explicit premise); the three escapes are now named: ROUTE B (verified:
φ̃-monotonicity, φ_p ≤ ½ln(ρ_sU/ρ_p), necessary-not-sufficient; Route-B C2 residue
(2/3)(1+2x)(1−x)ρ'_P² independently re-derived), CLASS-B SEALS, TWISTED FOLDS — all three are
Charles-level forks. Survivors confirmed: criticality migration branch-blind; G-layer
semi-analytic (ρ²)''=−2; fold saturation q=2√Z·ρ_sU verbatim-matches the banked T2 ceiling
(genuine consilience); countings A1 M+4/M+4, A2 M+5/M+5 square (square ≠ nonempty). Q2
characterization sound: a G-layer transmits exactly (q, H) + seal values — the algebra crosses,
the carrier does not. Cross-doc: the D2a and D2c kills are independently scoped, consistent,
mutually reinforcing. SAFE TO BANK with these corrections.
