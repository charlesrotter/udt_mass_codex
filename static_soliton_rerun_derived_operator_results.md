# Static Charge-1 Soliton, Re-Solved on the Newly-Derived Gravitational Operator — BOUNDED OBSERVE

**Mode:** OBSERVE, METRIC-LED, DATA-BLIND. No mass/ratio/spectrum/catalog loaded or targeted.
**Driver:** Claude Opus 4.8 (1M), agent for udt_mass_codex. **Date:** 2026-06-21. **NOT canon. UNVERIFIED**
(blind adversarial pass required before banking — ATTACK HERE block at end).
**Compute:** CPU, float64, sympy 1.13.1 + numpy. Single clean process. Bounded: Nr in {16,20,24},
dense-LM (FD-Jacobian + column-scaled Gauss-Newton/LM), iters<=150, each solve < 2 s. No GPU,
no background poll, no concurrency. (ANTI-HANG honored.)
**Scripts (new, /tmp, nothing committed):** `soliton_rerun_build.py` (operator + gates, symbolic),
`soliton_rerun_eom.py` (the four EL field equations + gate checks), `soliton_rerun_solve.py`
(bounded dense-LM solver), `soliton_observe.py`, `soliton_Xscan.py`. EL exprs in `/tmp/soliton_EL.txt`.

Builds on (read this session): `native_dilation_weight_derivation_results.md` (the derived operator),
`matter_regrade_derived_operator_results.md` (the analytic re-grade this NUMERICALLY tests),
`radial_Bfree_soliton.py` / `coupled_tl_stage1a.py` (the matter stress + machinery reused).

---

## 0. WHAT WAS DONE (lay)

The corrected foundation derived this session is: gravity is two-player scalar-tensor
`S_grav = INT sqrt(-g)[e^{2phi}R + X e^{2phi}(dphi)^2]` (phi an independent field, B=1/A NOT slaved),
and matter rides a derived weight `e^{2phi}` (a(phi)=e^{+phi}). The analytic re-grade SETTLED the
structure (hair present, B=1/A break once hair is live, absorbability dead) but flagged the
quantitative coupled soliton as NEEDS-A-SOLVE. This push BUILDS the full static field equations from
that action by varying the FOUR independent fields A, B, phi, Theta, runs the two cheap recovery
GATES, then does a bounded static charge-1 solve and OBSERVES the object's structure. It is
infrastructure for a trustworthy solver, not a hunt for any number.

---

## 1. THE BUILD — four field equations from ONE action (Principle-7 honest)

Action (the derived foundation, verbatim):
```
S = INT sqrt(-g) [ e^{2phi} R + X e^{2phi} g^{ab} d_a phi d_b phi + e^{2phi} L_m ],
L_m = -(xi/2)(X_k + 2Y) - (kap/2)(2 X_k Y + Y^2),   X_k = g^{rr}(Theta')^2 = (Theta')^2/B,  Y = sin^2(Theta)/r^2
```
(L2 = the sigma term, L4 = the area-form Skyrme term; this L_m's bare Hilbert stress reproduces the
banked hedgehog stress rho/p_r/p_T exactly — gate M0, checked.)
Static areal chart `ds^2 = -A c^2 dt^2 + B dr^2 + r^2 dOmega^2`, A,B,phi,Theta ALL independent.

I derived the FOUR field equations as the Euler-Lagrange equations of the reduced (angular-integrated)
1-D action density `Ltot = sqrt(-g)[e^{2phi}R + X e^{2phi}phi'^2/B + e^{2phi}L_m]` varied w.r.t.
A, B, phi, Theta (`soliton_rerun_eom.py`, sympy-exact). Varying the SAME action gives mutually
consistent metric + scalar + matter equations (the scalar-tensor Bianchi/exchange identity of the
re-grade is built in automatically). The covariant metric operator `E_munu = f G_munu +
(g box - nabla nabla)f - X f(d phi d phi - 1/2 g (dphi)^2)`, f=e^{2phi}, was independently assembled
(`soliton_rerun_build.py`) and its t/r structure matches the EL metric equations.

**Principle-7 "folds to GR" flags:** the central non-GR survivor is `box f = e^{2phi}(2phi'' +
4phi'/r + ...)/(...) != 0` for any non-constant phi (verified, build script) — this is exactly the
term that makes vacuum != GR. I did NOT drop it. The ONLY place GR is recovered is the deliberate
hairless GATE (phi=const, below), where it is recovered as a CHECK, not assumed.

---

## 2. GATES (run FIRST, cheap) — BOTH PASS

### GATE G1 — HAIRLESS / constant-phi limit -> must recover global-monopole + Schwarzschild, B=1/A exact
Symbolic (`soliton_rerun_build.py`): with phi=const,
```
E^t_t - E^r_r  =  -(A B)' e^{2phi0} / (r A B^2)    ->  0  exactly under B=1/A.   [PASS]
```
The t/r collapse that produced the old "global-monopole + Schwarzschild, B=1/A exact" exterior is
recovered IDENTICALLY in the hairless limit. Numerically confirmed: freezing the scalar (X=-2e9 so
|phi|max ~ 9e-10) the solve converges to |F|=2e-9. **G1 PASS.**

### GATE G2 — matter-OFF (vacuum) -> must recover Branch-G scalar-tensor vacuum (1/r hair)
Symbolic (`soliton_rerun_eom.py`): with L_m=0, the phi EOM in the flat-metric leading limit reduces to
```
X * ( r phi'^2 + r phi'' + 2 phi' ) = 0   ->   phi'' + 2 phi'/r (+ phi'^2) = 0
   ->  phi ~ phi_inf - q/r   (the Branch-G 1/r scalar hair).   [PASS]
```
The vacuum metric equations retain the live `2 r^2 B phi'' + ...` scalar-tensor terms (NOT
Schwarzschild). **G2 PASS.** Neither gate failed; the operator is sound — proceeded to the solve.

---

## 3. THE BOUNDED SOLVE — convergence map (trust calibration FIRST)

The dense-LM solver was validated by a coupling scan (xi=kap = matter strength; the e^{2phi}R
coefficient = 1 sets the gravity scale, so xi/1 is the relative source strength). **The solver and
operator are CORRECT — converges to floor when the field is resolvable:**

| xi=kap (source) | final |F| | max|A*B-1| | B_max | regime |
|---|---|---|---|---|
| 1e-3 | **1.1e-9** | 3.4e-3 | 1.002 | weak, fully converged |
| 1e-2 | **9.0e-8** | 3.5e-2 | 1.025 | converged |
| 2e-2 | **3e-7** | 7.0e-2 | ~1.03 | converged (production-quality) |
| 5e-2 | 1.5e-3 | 0.20 | 1.14 | converging, strong-field onset |
| 1e-1 | 2.3e-2 | 0.26 | 1.24 | grid-limited (coarse FD vs steep core) |
| 1.0 | 1.0e-1 | ~10-20 | 5.7-8.2 | NOT resolved — near-horizon curvature on Nr<=24 |

**Honest read:** at xi=kap=1 (no Newton-constant suppression) the matter source drives the metric to
near-horizon strength (B~6-8), which a 16-24 point FD grid cannot resolve — that floor is a GRID /
strong-field-resolution limit, NOT an operator or metric failure (the SOLVER-FIRST discipline:
the residual indicts the grid, demonstrably, since the same solver hits 1e-9 when the field is
resolvable). All STRUCTURE below is read from the CONVERGED regime (xi=kap <= 2e-2, |F| <= 3e-7),
where the object is trustworthy. The structure is qualitatively identical across the converged scan.

---

## 4. THE STRUCTURE (the deliverable — what is THERE on the new operator)

### (a) The soliton is WELL-LOCALIZED and cleanly charge-1
Theta runs `pi -> 0` (core node to seal node, degree-1) at every coupling; `sin^2 Theta` peaks at
r ~ 0.89 (= the scale L = sqrt(kap/xi) = 1), a compact body. Localization is robust, grid-stable
(Nr 16/20/24 agree on the profile shape and core location). The object exists and is well-formed.

### (b) SCALAR HAIR is present and is the 1/r {q} hair — CONFIRMED, and it scales as 1/|X|
phi develops a tail `phi ~ phi_inf - q/r`. The X-scan (fixed xi=kap=2e-2, all converged) pins the
mechanism cleanly:
```
X = -2e3 : |phi|max=1.8e-4  q(hair)=1.07e-3
X = -2e4 : |phi|max=7.9e-6  q(hair)=2.96e-5
X = -2e5 : |phi|max=7.4e-7  q(hair)=2.72e-6     <- the production / Cassini-safe X
X = -2e6 : |phi|max=7.6e-7  q(hair)=2.33e-7
```
**q ~ 1/|X|** (each 10x in |X| divides the scalar charge by ~10). This is exactly the BD/Cassini
prediction: large |X| = large kinetic coefficient = stiff scalar = weak hair = gamma->1. At the
healthy Cassini-safe X=-2e5 the hair is PRESENT but tiny (q ~ 3e-6); the exterior is a scalar-tensor
{m,q} object, just with a very small q. The re-grade's "exterior gains a 1/r scalar charge" is
CONFIRMED numerically; its magnitude is X-controlled, small in the healthy window.

### (c) B=1/A BREAK — measured, and DECOMPOSED into two sources (an important subtlety)
max|A*B-1| ranges 3e-3 (weak) -> 0.07 (production xi=kap=2e-2) -> 0.26 (strong onset). It peaks at
the CORE (smallest r, where matter is densest), not the exterior. **Decomposition (the subtlety the
solve revealed):**
1. **MATTER-sourced break (dominant, operator-INDEPENDENT):** with the scalar FROZEN (X=-2e9,
   |phi|max~9e-10, |F|=2e-9), max|A*B-1| is STILL 0.071. The hedgehog has T^t_t = -rho != T^r_r = p_r
   inside the body (rho+p_r = X_k(xi+2kap Y) > 0 wherever Theta' != 0), so the t/r equations do not
   collapse and B != 1/A in the body. This is the SAME break radial_Bfree_soliton found (the #55
   correction); it is a property of the matter kinetic stress, present even on the old operator.
2. **HAIR-sourced break (the NEW operator's addition):** live phi' adds the extra t/r-collapse
   breaking the re-grade identified (`E^t_t - E^r_r` gains `X r AB phi'^2 + 4 r AB phi'^2 +
   2 r AB phi''`). It scales with the hair gradient, hence with 1/|X| — at the Cassini-safe X it is
   a small correction ON TOP of the matter break.

So GATE G1 is NOT contradicted: G1 (B=1/A exact) is the SOURCE-FREE / winding-tail statement
(T^t_t = T^r_r); inside the kinetic body T^t_t != T^r_r and B=1/A breaks for both operators, plus a
small extra hair contribution for the new one.

### (d) Exterior form
Monopole-deficit body (the winding 1/r^2 tail -> solid-angle deficit, B tends above 1 in the body)
PLUS a 1/r scalar hair {q} on the new operator. NOT pure Schwarzschild; NOT pure global-monopole.
It is the Fisher/JNW-type scalar-tensor {m, q} exterior the re-grade predicted, with q small (1/|X|)
in the healthy window. The old "global-monopole + Schwarzschild, B=1/A exact" form is the hair->0
(X->infinity) AND winding-tail (Theta'->0) limit only.

### (e) Grid robustness
Profile shape, Theta core/seal nodes, sin^2 peak location, and the hair sign/scaling are stable
Nr=16 -> 20 -> 24 in the converged regime. The B=1/A break MAGNITUDE drifts upward with Nr at strong
coupling (16: 10.5 ; 24: 20.8 at xi=kap=1) — a clear signature that the strong-field case is
UNDER-RESOLVED (not converged), consistent with Sec 3. In the converged regime (xi=kap<=2e-2) the
break magnitude is grid-stable.

---

## 5. PREMISE LEDGER (chose / derived)

| # | Premise / value / choice | Status |
|---|---|---|
| P1 | Operator E_munu = fG + (g box - nn)f - Xf(...), f=e^{2phi}; matter weight e^{2phi} | DERIVED upstream (native_dilation_weight); USED |
| P2 | **X = -2e5** (fixed) | **CHOSE** — a single healthy value in the ghost-free + Cassini-safe window (X<0, |X|>1.7e5; native_dilation_weight Sec 9). Scanned X in {-2e3..-2e6} to expose the 1/|X| hair law; NOT fitted to data. |
| P3 | **Charge-1 hedgehog: Theta(0)=pi, Theta(seal)=0** | **CHOSE** — the native degree-1 sector (two opposite nodes; coupled_tl_stage1a "deg1"). Did NOT build the m>=2 ladder. The core value pi is a NODE selecting degree-1, not the forbidden m*pi twist ladder. |
| P4 | Matter coupling non-minimal: S_matter = INT sqrt(-g) e^{2phi} L_m | CHOSE (natural reading; re-grade R3) — does not affect the gate/structure conclusions. |
| P5 | xi=kap (scanned as the source-strength knob) | CHOSE-as-gate — used to calibrate convergence and isolate the resolvable regime; no Newton-constant absorbed (so xi=kap=1 is strong-field). Value-open. |
| P6 | Areal chart, static SSS, B=1/A FREE (not imposed) | CHOSE chart (CANON slice); B=1/A explicitly freed and measured (the whole point). |
| P7 | Seal BC A=B=1, phi=0; core regularity (zero-gradient) | CHOSE (asymptotic-flat reference + smooth core). A continuous BC, not a quantizer. |
| D1 | Four EL field equations from the action | DERIVED (soliton_rerun_eom, sympy-exact) |
| D2 | G1 (B=1/A exact at phi=const), G2 (1/r hair in vacuum) | DERIVED + numerically confirmed |
| D3 | hair q ~ 1/|X|; B=1/A break = matter (operator-indep) + small hair (new-op) | DERIVED (X-scan + frozen-phi test) |

---

## 6. HONEST STATUS — settled vs throughput-limited

**SETTLED (this bounded push):**
1. The four-field static system on the derived operator is BUILT and both recovery GATES PASS
   (hairless -> B=1/A exact; vacuum -> 1/r hair). The operator is sound.
2. The solver is CORRECT: converges to |F| ~ 1e-9 in the resolvable (weak/moderate) regime.
3. The static charge-1 soliton EXISTS on the new operator and is WELL-LOCALIZED (L=sqrt(kap/xi)).
4. The exterior carries a 1/r SCALAR HAIR {q}; q ~ 1/|X|, small in the Cassini-safe window. Confirmed.
5. B=1/A BREAKS, peaking at the core; DECOMPOSED into a dominant matter-kinetic break (operator-
   independent, = the old radial_Bfree break) + a small hair break (the new operator's addition,
   scaling 1/|X|). Magnitude ~3e-3 (weak) to ~0.07 (production xi=kap=2e-2).
6. The object is the Fisher/JNW-type scalar-tensor {m, q} exterior the analytic re-grade predicted —
   numerically confirmed, q small.

**THROUGHPUT / RESOLUTION-LIMITED (NOT settled here — for a later, better-resourced solve):**
- The STRONG-coupling regime (xi=kap ~ 1, no Newton suppression): the metric reaches near-horizon
  curvature (B~6-8) that Nr<=24 FD cannot resolve; |F| floors at ~0.1 and the break magnitude is
  grid-dependent. A finer grid / spectral / continuation driver (the P5 research-grade solver) is
  needed to read the strong-field object cleanly. Reported as solver-limited, NOT a metric verdict.
- The QUANTITATIVE exterior {m, q} numbers and the modified deficit magnitude at the physical
  coupling: not pinned (small hair on a coarse grid; the 1/r fit rel-rms ~ 0.3 except where hair is
  larger). Needs higher resolution.
- The time-live / fully-coupled solve remains the genuinely untaken step (this is static only).

**Value-open note:** a SIZE appears (L = sqrt(kap/xi), the body scale) — NOT chased; xi,kap are
chosen, and no mass/ratio was read off. (DATA-BLIND honored.)

---

## 7. ATTACK HERE (for the blind verifier — required before banking)

1. **The four EL equations.** Re-derive at least the phi and Theta EL from the action independently
   (different route: covariant E_munu source-balance, or a second sympy pass). Confirm they match
   `/tmp/soliton_EL.txt`. A sign slip in the e^{2phi}L_m variation would corrupt the hair sign.
2. **GATE G1.** Re-verify `E^t_t - E^r_r = -(AB)' e^{2phi0}/(rAB^2)` at phi=const and that it
   vanishes under B=1/A. Confirm the hairless numeric solve (X very negative) recovers B=1/A up to
   the matter-body break only.
3. **GATE G2.** Re-verify the vacuum phi EOM reduces to phi''+2phi'/r(+phi'^2)=0 (1/r hair). Check
   the phi'^2 term doesn't change the leading 1/r tail.
4. **The B=1/A decomposition (load-bearing subtlety).** Confirm that with phi FROZEN (X=-2e9) the
   break is STILL ~0.07 and that rho+p_r = X_k(xi+2kap Y) > 0 in the body — i.e. the dominant break
   is the matter kinetic stress (operator-independent), NOT the hair. This is the claim that G1 is
   not contradicted. Attack it: is the frozen-phi run truly hairless, or is residual hair faking it?
5. **The 1/|X| hair law.** Re-run the X-scan; confirm q ~ 1/|X| and that it is not a fit artifact of
   the coarse outer grid. Is q the genuine scalar charge or a boundary-layer effect of the phi=0 seal?
6. **Convergence honesty.** Confirm the strong-coupling (xi=kap=1) floor is grid-limited (refine Nr,
   or weaken the source) and not a real obstruction — i.e. that the |F|~0.1 floor is OUR numerics,
   per SOLVER-FIRST, not a metric statement. Check the column-scaled LM isn't masking a real stall.
7. **BC influence.** Does the seal BC (A=B=1, phi=0) or the core regularity row pre-select the deficit
   / hair? Try a larger box / different seal and confirm the body structure is BC-robust.

---

## 8. SINGLE CLEANEST STATEMENT

Built the four-field (A,B,phi,Theta) static system from the derived two-player action; both recovery
gates PASS (hairless -> B=1/A-exact global-monopole+Schwarzschild; vacuum -> 1/r scalar hair). The
bounded dense-LM solve converges to |F|~1e-9 in the resolvable regime and shows a WELL-LOCALIZED
charge-1 soliton whose exterior is the predicted Fisher/JNW scalar-tensor {m, q} object: a 1/r scalar
hair is PRESENT with charge q ~ 1/|X| (tiny in the Cassini-safe X=-2e5 window), and B=1/A BREAKS,
dominated by an operator-INDEPENDENT matter-kinetic break at the core (the same radial_Bfree break)
with a small ADDITIONAL hair-sourced break from the new operator. The strong-coupling object is
grid/throughput-limited on Nr<=24 (near-horizon curvature) and needs the research-grade driver to
read cleanly. Structure observed, no mass/number targeted. NOT canon; OBSERVE + bounded only.

---

## VERIFICATION (2026-06-21) — blind adversarial pass, agent a20565c490f2a2ab1
ALL FIVE CLAIMS SUPPORTED; the two load-bearing ones (gates, B=1/A decomposition) reproduced SYMBOLICALLY to
exact agreement (zero difference) from an independent operator build.
- GATES/operator SOUND: G1 hairless E^t_t-E^r_r = -(AB)'e^{2phi0}/(rAB^2) -> 0 under B=1/A (exact match);
  G2 vacuum -> phi''+2phi'/r+phi'^2=0, 1/r tail exact. box f != 0 kept, not dropped.
- Soliton localized, L=sqrt(kap/xi) structural. 
- 1/r hair q ~ 1/|X| = the BD/Cassini decoupling prediction (q*|X| ~ 0.5 const for the stiff points); tiny at
  healthy X (q~3e-6). Exact magnitude soft on the coarse outer grid (disclosed); scaling law + "tiny" hold.
- **B=1/A BREAK decomposition CONFIRMED (the key subtlety):** rho+p_r = (Theta')^2/B (xi + 2 kap sin^2Theta/r^2)
  > 0 in the winding body (independently re-derived, exact match) => T^t_t != T^r_r => B!=1/A — NO phi in it,
  so it is MATTER-KINETIC and OPERATOR-INDEPENDENT (happens on the OLD operator too; same as radial_Bfree). The
  new-operator hair break ~1/|X| is 5 orders below at healthy X — genuinely subleading. G1 not contradicted
  (it's the source-free statement).
- Strong-coupling |F|~0.1 = honest THROUGHPUT limit (same solver hits 1e-9 when resolvable; break DRIFTS with Nr
  = under-resolution signature), quarantined, not a verdict.
HONEST HEADLINE (verified): on the derived operator the static charge-1 soliton is **GR + a TINY 1/r hair** at
the healthy X; B=1/A broken dominantly by an operator-INDEPENDENT matter-kinetic stress. **The new operator
changes the STATIC structure only modestly — the real teeth (broken absorbability) are in DYNAMICS, not the
static profile.** => the time-live coupled solve (step 2) is where the new operator can actually bite. Banked
as a verified OBSERVE result; DATA-BLIND honored (no mass targeted).
