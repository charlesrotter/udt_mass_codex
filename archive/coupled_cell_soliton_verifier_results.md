# BLIND ADVERSARIAL VERIFIER — Coupled Cell + Angular-Soliton Study

Verifier agent: Claude (Opus 4.8, 1M context), blind-adversarial role.
Date: 2026-06-14. Target doc: `coupled_cell_soliton_results.md`.
Scripts (independent; the constructor's scripts were NOT run):
`verifier_scripts_coupled_cell/v_*.py` (sympy CPU symbolic, mpmath 50-dps deep-phi,
V100 float64 for the eigenproblem and Derrick relaxations).

Method: every claim re-derived from the metric/Lagrangian with my own machinery,
then attacked. Negatives were attacked by actively hunting the structure they say
is absent. Premise-dependence reported honestly.

---

## Independent foundation check (before the 5 claims)

Re-derived `rho` from scratch from the minimal hedgehog `n=x/r`
(`L=-(xi/2)g^{mn}d_m n_a d_n n_a`, Theta=theta), computing the angular gradient
`g^{ab}d_a n . d_b n = 2/r^2`. With the standard global-monopole normalization this
gives **rho = xi/r^2, p_r = -rho exact, p_theta=0** — matches the study's DERIVED
input. (The bare `2/r^2` carries a factor 2 absorbed into the xi normalization; the
1/r^2 structure — the load-bearing fact — is independent and confirmed.)

---

## CLAIM 1 — CELL FINITIZES — **CONFIRMED**

Symbolic (sympy), independent:
- Integrand `rho * 4 pi r^2 = 4 pi xi` is **exactly constant in r** (d/dr = 0 verified).
- `E_coord = INT_{rc}^{ri} 4 pi xi dr = 4 pi xi (r_int - r_core)` — verified equal to
  the claimed closed form symbolically.
- `lim_{rc->0} E_coord = 4 pi xi r_int` — **finite; NO 1/r_core divergence.** The 1/r^2
  source is integrable against the r^2 bare measure. CONFIRMED.
- Misner-Sharp/bare-integral version `m_MS(r) = 4 pi xi (r - r_core)` — finite, linear.

Attack on the proper-volume / deep-phi reintroduction-of-divergence worry (the
study's own attack-point #1):
- Proper measure with deep-log background `e^{phi}=(r/r_int)^p`:
  `E_proper = 4 pi xi r_int/(p+1)` in the `rc->0` limit — **finite for all p>0**.
- mpmath 50-dps at p = 1, 5, 10, 50 (deep core, into the `e^{-2phi0}~5` regime):
  `E_proper` = 0.6283, 0.2094, 0.1142, 0.0246 — finite and *decreasing* (the
  `e^{phi}=(r/r_int)^p -> 0` weight SUPPRESSES the core). Deep phi does NOT
  reintroduce a divergence; not a float64 artifact.

Verdict: finite-by-truncation reading is correct. **CONFIRMED**, no premise risk
(holds with phi frozen, robust to background and to deep phi).

## CLAIM 2 — PHI ALONE DOES NOT FINITIZE — **CONFIRMED**

Symbolic: with `e^{-2phi}=1-delta-rs/r`, the MS mass `m(r)=r(1-e^{-2phi}) = delta*r + rs`.
- `lim_{r->inf} m(r)/r = delta` — **linear divergence** for delta>0; not convergence.
- Sign check: deficit `delta>0` makes the mass GROW (m(1e6)=1e4 at delta=1e-2), it does
  not flip to convergence. The E2-erratum sign concern (study attack-point #2) does not
  rescue localization: any nonzero deficit gives unbounded linear growth.
- The coordinate energy independently diverges: `E_coord(R)=4 pi xi R -> inf`.

Verdict: phi back-reaction alone gives a conical/deficit (global-monopole) geometry,
not a localized lump. **CONFIRMED.**

## CLAIM 3 — "ALL FREE, NOTHING DISCRETE" — **CONFIRMED (negative survives the hunt)**

This was attacked hardest. I built the SIMULTANEOUS core-regularity + seal-mirror-fold
BVP as a self-adjoint Sturm-Liouville eigenproblem on the V100 (bare measure r^2,
stiffness K_r=e^{-4phi}, mass-weight r^2; Neumann=sigma-even seal, Dirichlet=sigma-odd),
exactly the framing the study said the verifier should test directly.

Findings:
- On a bounded domain the eigenproblem trivially has a discrete MODE spectrum
  (e.g. {~0, 20.1, 59.4, 118, ...}). **This is not particle discreteness** — it is the
  standard Laplacian-on-an-interval spectrum.
- The real test (does the BVP admit a static solution only for special parameters?):
  I varied delta in {0.001..0.2} and r_int in {0.5..10} continuously and watched the
  lowest 5 eigenvalues. They move **smoothly and monotonically** — no gaps, no
  forbidden values, no parameter selection. The lowest eigenvalue stays ~0 (the static
  EOS zero-mode), continuously deformable for EVERY parameter value.
- Cell-size dependence is pure geometric scaling `eig ∝ 1/r_int^2` (Laplacian scaling) —
  **no intrinsic length emerges**, so size is not selected.
- Mixed parity (Dirichlet core + Neumann seal) likewise gives a continuously-moving
  spectrum; still no quantization of (p, delta, r_int).

Imposing BOTH BCs simultaneously does NOT overdetermine the static coupled solution:
symbolically the core-depth BC and the interface BC fix only the integration/closure
constants (p and rs), leaving (p, delta, r_int) free. **No hidden eigenvalue ladder.**

Verdict: the "free 3-parameter family, no discreteness" negative is **CONFIRMED** and
correctly scoped (static, single-cell, minimal-model). I actively hunted the missing
discreteness via the self-adjoint eigenproblem the study flagged and found none.

## CLAIM 4 — FORCED rs<0 (mass defect) — **CONFIRMED as a result, but BC-DEPENDENT (premise-attached)**

The interface BC `phi(r_int)=0` requires `m_areal(r_int)=0`, forcing
`rs = -[delta(r_int-r_core)+r_core(1-e^{-2p})]`. Since both bracketed terms are
strictly positive for delta>0, p>0, **rs<0 is strictly forced under that BC.** CONFIRMED
under C3.

Attack — is it structural or a BC artifact? I tested alternative native closures:
- **Mirror-fold / Neumann seal** (`d(e^{-2phi})/dr=0` at r_int — the study's OWN canonical
  seal): `rs = r_core(delta - 1 + e^{-2p})`. This is **generically NEGATIVE** across the
  physical range (small delta, p>=0.5: e.g. p=1,delta=0.1 -> factor -0.765), but it
  **flips POSITIVE for shallow core + large deficit** (p=0.1, delta=0.5 -> +0.319).
- **No interface pin (rs=0):** the deficit simply persists, `phi(r_int)<0`; no closure
  constant needed at all.

Verdict: `rs<0` is **not an absolute structural theorem** — it is strictly forced only by
the chosen `phi(r_int)=0` interface BC (C3), and is merely *generic* (not universal) under
the Neumann seal. The study's own ledger flags this honestly (C3 "forced rs<0"). The
load-bearing structural content — that closing the deficit to phi=0 demands a NEGATIVE
closure constant — is real and BC-tied, exactly as the study scoped it.
**CONFIRMED with the premise-dependence the study already attached.** Not a buried artifact.

## CLAIM 5 — DERRICK FORCED-STABILIZER NO-GO — **CONFIRMED**

Independent Derrick scaling for the radial-twist `Theta(r)` (the only deformation, since
the unit hedgehog has no profile freedom). Energy
`E = INT[(Theta')^2 r^2 + 2 sin^2(Theta)] dr` (3D, *4pi).

Analytic dimension count under `Theta_lam(r)=Theta(r/lambda)`:
- gradient term -> `lambda^1`; angular term -> `lambda^1`. So `E(lambda)=lambda*E1`,
  `dE/dlambda = E1 = const > 0`, no interior stationary point => **Derrick collapse**
  (E minimized at lambda->0, the lump shrinks to zero size).

Numerical, THREE independent probe profiles (different from the study's): study-bump,
arctan-kink, gaussian. All give `E(2 lambda)/E(lambda) ≈ 2.000` => `lambda^1` scaling
confirmed profile-independently (it is the dimension count).

Attack — does the background or the seal evade Derrick?
- Conical deficit background (scale-free, constant `e^{-2phi}=1-delta` prefactor): a
  constant prefactor cannot introduce a length; ratio stays ~2.0 at delta=0,0.1,0.3.
  Derrick survives.
- Finite-cell relaxation with seal BCs Theta(0)=0,Theta(L)=pi: relaxed energy scales
  **linearly with L** (~3.91*L), no interior minimum => the seal/boundary does NOT select
  a size. Boundary-induced stabilization (the study's attack-point #4) does not occur.

Verdict: no stable finite-size radial-twist soliton in the minimal model; a finite-size
radial particle would FORCE a stabilizer (Skyrme ~ lambda^{-1} or potential ~ lambda^{+3}).
**CONFIRMED.** Premise: load-bearing on C1 (minimal model: no Skyrme, no potential), as the
study flags.

---

## OVERALL VERDICT — THE STUDY'S VERDICT STANDS

| Claim | Verdict |
|---|---|
| 1. Cell finitizes (E=4pi xi (ri-rc), no 1/rc div, deep-phi safe) | **CONFIRMED** |
| 2. phi alone does NOT finitize (M~delta r diverges) | **CONFIRMED** |
| 3. All-free, NO hidden discreteness (eigenproblem hunted) | **CONFIRMED (negative survives)** |
| 4. rs<0 forced | **CONFIRMED, BC-dependent** (strict under phi(r_int)=0; generic under Neumann seal; the study already premise-attached this) |
| 5. Derrick no-go => stabilizer forced | **CONFIRMED** (analytic + 3 probes; not evaded by background or seal) |

Nothing CANNOT-REPRODUCE; nothing REFUTED. The cross-cutting verdict (finiteness comes
from the CELL, not phi; phi gives the deficit EOS/geometry; the realized particle is a
continuous free family with no discreteness or selected size; the minimal model admits no
radial soliton) is independently reproduced and survives an active adversarial hunt for
the missing discreteness and for a Derrick-evading boundary scale.

One honest sharpening for the record (not a refutation): the rs<0 result is correctly the
most premise-tied claim — it is strictly forced only by the phi(r_int)=0 interface BC and
is merely generic (can flip positive for shallow-core/large-deficit) under the Neumann
seal. This is consistent with the study's own C3 flag and does not change any verdict.
