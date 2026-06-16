# Corrected radial soliton with B=1/A FREED — results record

Driver: Claude (Opus 4.8, 1M). 2026-06-15. OBSERVE mode. DATA-BLIND (intrinsic
sqrt(kappa/xi) units; no wall numbers, no comparison to nature).
Frame: the forced correction from gate #55 (`whole_metric_solve_3D_results.md`):
the reduced #52 soliton imposed B=1/A (b=-a) inside the TWISTED body, violating
the (r,r) and angular Einstein equations. Here a(r) and b(r) are INDEPENDENT.

Scripts (committed with this doc; all run IN-PROCESS / blocking, no backgrounding):
`radial_Bfree_soliton.py` (engine + coupled solve), `radial_Bfree_validate.py`
(the gate), `radial_Bfree_depth.py` (what-changed + depth map).

THE SYSTEM (standard GR, areal gauge rho=r, B=1/A freed):
ds^2 = -e^{2a(r)} dt^2 + e^{2b(r)} dr^2 + r^2 dOmega^2, a,b independent.
Matter = settled L2+L4 unit-S^3 hedgehog, winding m=1, profile Theta(r), the
stress-consistent unit field. Solved SIMULTANEOUSLY: (t,t)=>m(r) [e^{-2b}=1-m/r],
(r,r)=>a'(r) [TOV-type, from G^r_r=kap8 p_r, NOT from B=1/A], the Theta EL,
(theta,theta) as a Bianchi CHECK. phi = -a (responds, not slaved).

---

## 0. THE GATE FINDING (the decisive correction made in this push)

Freeing B=1/A was necessary but NOT sufficient. The solver inherited from the
reduced #52 baseline a **LINEAR SEAL-INJECTION DEFECT**: to force m(seal)=0 it
smeared a defect `m += rs*span` linearly across the whole cell. The source mass
does NOT vanish at the seal (m_src(seal) = +0.284 here), so this injects a
constant, un-sourced `m' = rs/span = -0.0159` everywhere. Because
G^t_t = -m'/r^2, the (t,t) residual is then pinned and 1/r^2-amplified:
predicted res_tt(r=0.4) = -0.0159/0.4^2 = **-0.0993** — the EXACT observed floor
(0.099), and it does NOT converge with resolution.

This is an IMPORTED mechanism (Charter principle 1): closing the cell by adding
mass that no field sources. Removing it (default `seal_defect=False`) lets
m = m_core + m_src exactly, so m' = kap8 r^2 rho pointwise and **all three
Einstein residuals converge O(h^2)**. The soliton then simply has a genuine
Schwarzschild-like exterior mass m(seal) = +0.2197 (it is not forced to zero).

The legacy defect is preserved behind `seal_defect=True` for head-to-head only.

---

## 1. SOLVER VALIDATION GATE  — PASS

### (iii) Einstein ENGINE vs Schwarzschild & flat
- Schwarzschild (e^{2a}=1-2M/r, b=-a, M=0.3, N=4000): max|res_tt|=max|res_rr|=
  7.42e-7, max|res_thth|=3.21e-7.
- Convergence (vacuum max|G|): N=2000 -> 2.88e-6; N=4000 -> 7.42e-7;
  N=8000 -> 1.89e-7. Clean **second order**.
- Flat (a=b=0): max|G^t_t|,|G^r_r|,|G^th_th| = 0, 0, 0 (exact).

### (i) All three residuals -> 0 and CONVERGING on the corrected soliton
Canonical cell (14L), uniform grid, p=0.4, kap8=0.05; smooth body (r in [0.4, ri-0.5]):

| N    | M_MS     | max|res_tt| | max|res_rr| | max|res_thth| |
|------|----------|-------------|-------------|---------------|
| 600  | 0.281040 | 1.461e-3    | 4.607e-3    | 2.305e-3      |
| 1200 | 0.281000 | 3.647e-4    | 1.151e-3    | 5.771e-4      |
| 2400 | 0.280983 | 9.127e-5    | 2.880e-4    | 1.444e-4      |

All three drop ~4x per N-doubling = **O(h^2)** — contrast the #55 reduced
soliton's body (r,r) ~ 0.16 (frozen). The earlier seal-defect run had res_tt
frozen at ~0.099 (non-converging); with the defect removed res_tt now converges
to ~1e-4. **GATE (i) PASS.**

### (ii) B=1/A RECOVERED in the unwound exterior
The m=1 hedgehog has a power-law sin(Theta)/r tail (no compact support), so
|Theta'| never reaches 1e-6; "unwound" = winding >=3 orders below the body peak.
Extended cell (28L), p=0.4, N=2400, near-vacuum tail |Theta'|<1e-3 (r in
[15.3, 27.5], 1049 pts):
- e^{a+b}: mean = **1.003938**, std = **4.07e-7**  =>  a+b -> const  =>  e^a e^b
  = const  =>  **B=1/A recovered** in the exterior.
- twisted body (|Theta'|>1e-1): max|a+b| = 0.196 — the genuine interior departure
  from B=1/A (the decoupled interior warp). **GATE (ii) PASS.**

---

## 2. THE CORRECTED SOLITON  — EXISTS

At the canonical dial (p=0.4, kap8=0.05, 14L cell, N=2400):
- **M_MS = 0.280983** (intrinsic units), stable to 4 dp across N=600..2400.
- **size**: width (Theta = pi/2 crossing) = 0.838.
- **core**: b0 = -0.400 (the dial sets e^{-2b} at the core), a0 = 0.1425
  (=> phi0 = -a0 = -0.1425, deep-negative core as required).
- **HOW b departs from -a in the twisted body** (the freed warp): interior
  max|a+b| = **0.192**, mean|a+b| = 0.0129. So a != -b inside the soliton by up
  to ~0.19 (the EOS-softening / decoupled interior warp), collapsing to 0 in the
  exterior. This departure is exactly what the reduced #52 wrongly set to zero.

The soliton is a single smooth, regular, self-consistent solution. EOS
p_r + rho = X(xi + 2 kap Y) >= 0 holds (no exotic matter introduced).

---

## 3. WHAT CHANGED vs the invalidated reduced #52

Head-to-head at p=0.4 (14L, N=600), isolating the two corrections:

| solver                                   | M_MS      | width  | note |
|------------------------------------------|-----------|--------|------|
| reduced #52 (b=-a tie, seal defect)      | 0.289735  | 0.7192 | invalid (frozen residuals) |
| freed + defect kept (B free only)        | 0.283695  | 0.8476 | B-freeing alone: M -2.09% |
| **freed CORRECTED (delivered)**          | 0.281040  | 0.8380 | total vs #52: **M -3.00%** |

- Freeing B=1/A alone moves M_MS by **-2.1%** and widens the core (width
  0.719 -> 0.848). Dropping the seal defect adds another ~-0.9%.
- Profile shift: max|Theta_corrected - Theta_#52| = 0.219 (a real, O(0.1)
  reshaping of the winding profile, not a tiny perturbation).
- Interior warp now present: max|a+b| = 0.25 (zero by construction in #52).

**Did it surface NEW STRUCTURE?**  NO new branch, NO bifurcation, NO existence
change, NO selection. The correction SHIFTS NUMBERS (~3% in mass, ~18% in width)
and adds the interior a-vs-(-b) warp, but the solution remains a single smooth
family. Reported whichever way it fell: it fell to "shifted numbers + a real
interior warp," not "new structure."

---

## 4. CORRECTED DEPTH-MASS MAP (B=1/A freed, defect dropped)

14L cell, N=600 (M_MS stable to 4 dp vs N=1200), kap8=0.05:

| p    | M_MS_corr | width  | max|a+b| | a0=phi0 |
|------|-----------|--------|----------|---------|
| 0.20 | 0.272185  | 0.7933 | 2.76e-1  | -0.2160 |
| 0.30 | 0.276248  | 0.8144 | 2.65e-1  | -0.1848 |
| 0.40 | 0.281040  | 0.8380 | 2.53e-1  | -0.1550 |
| 0.50 | 0.286676  | 0.8642 | 2.42e-1  | -0.1262 |
| 0.60 | 0.293288  | 0.8933 | 2.31e-1  | -0.0982 |
| 0.70 | 0.301025  | 0.9254 | 2.21e-1  | -0.0714 |
| 0.80 | 0.310057  | 0.9607 | 2.10e-1  | -0.0460 |
| 0.90 | 0.320582  | 0.9994 | 2.01e-1  | -0.0228 |
| 1.00 | 0.332824  | 1.0417 | 1.92e-1  | -0.0032 |
| 1.20 | 0.363531  | 1.1379 | 1.76e-1  |  0.0000 |
| 1.50 | 0.430410  | 1.3137 | 1.62e-1  |  0.0000 |

log-slope d(ln M_MS)/dp, strictly RISING:
0.148, 0.172, 0.199, 0.228, 0.260, 0.296, 0.334, 0.375, 0.441, 0.563.

**The super-exponential shape (#54) SURVIVES** the B-freeing and the defect
removal: the log-slope rises monotonically with depth (a constant slope would be
plain exponential; rising = super-exponential). No structure acquired — smooth,
single-valued, monotone. The interior warp max|a+b| DECREASES with depth, while
phi0 = a0 rises toward 0 as the dial deepens b.

CAVEAT / dial flag: for p >= 1.2 the core hits the e^{-2b} clamp (min=1e-9), so
a0=phi0 reads exactly 0.0000 — a numerical floor at very deep dials. The shape
conclusion rests on p <= 1.0 (all clean); the deep points only extend the trend.

---

## 5. PREMISE LEDGER (chose-or-derived)

| premise | chose / derived | note |
|---|---|---|
| areal gauge rho = r | CHOSE (gauge) | non-restrictive coordinate choice for a radial metric, not the forbidden physical imposition; canon R-areal |
| a(r), b(r) independent (B=1/A freed) | DERIVED-need | forced by gate #55; the whole point |
| (t,t)->m, (r,r)->a', EL->Theta, (th,th) check | DERIVED | standard mixed Einstein eqs + Bianchi |
| unit-S^3 hedgehog matter, m=1 | CHOSE (the settled L2+L4 field) | stress + EL verified consistent (nabla.T=0) |
| **NO seal-injection defect** (m=m_core+m_src) | DERIVED-need (THIS push) | the legacy defect violates (t,t); removed. m(seal)=0.22 != 0 is a RESULT, not imposed |
| depth dial p: m_core = rc(1-e^{2p}) | CHOSE (the control dial) | the one intrinsic control; sweeps the map |
| kap8 = 0.05 | CHOSE | canonical coupling from complete_metric_sweep_stageB |
| cell size 14L (28L for ext test) | CHOSE | canonical; M_MS insensitive to it (exterior is vacuum) |
| BC: Theta(core)=pi, Theta(seal)=0; a(seal)=0 | CHOSE | center regularity + seal closure |
| xi = kap = 1 | CHOSE (units) | the single intrinsic scale kappa/xi=1 |

NEW DIALS introduced this push: none beyond `seal_defect` (a comparison toggle,
default False = the physically correct choice). FLAGGED numerical limit: e^{-2b}
clamp saturates the core for p >= 1.2.

PRINCIPLE 2: full nonlinear throughout; only sanctioned function-replacements
(trapezoid quadrature, FD Jacobian, exp-arg clamp guarding transient Newton
iterates). No linearization used as a result or as an input.

---

## 6. BOTTOM LINE (data-blind binary read)

With B=1/A honestly freed AND the imported seal-injection mechanism removed, the
UDT metric + settled angular winding field **natively produces a regular,
self-consistent, gravitationally-massed soliton** — a single smooth family whose
mass rises super-exponentially with core depth and whose interior carries a real
a-vs-(-b) warp (B=1/A holds only in the exterior). The correction shifts the
mass ~3% and the width ~18% vs the invalidated #52 and adds the interior warp,
but surfaces NO new branch / bifurcation / selection. This is the first faithful
piece of the honest binary test: UDT DOES produce mass structure here; whether
it produces the DISCRETE catalog remains open (no quantization emerged at the
classical radial level — consistent with the quantum-completion frontier).
