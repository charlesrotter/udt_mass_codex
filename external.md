# EXTERNAL REVIEW BRIEF — UDT macro-background derivation (self-contained)

**Date:** 2026-07-08 · **Authors:** Claude Opus 4.8 (1M) with Charles Rotter. **Audience:** external LLMs / physicists
reviewing during a work pause. **Purpose:** a self-contained account of a strategic pivot and a foundational derivation
in Universal Dilation Theory (UDT), so an independent reviewer can stress-test the reasoning — especially the
load-bearing premises flagged throughout. **We want you to try to break this, not to endorse it.**

Nothing here requires access to our repository; all equations and logic are reproduced inline. Where we cite an internal
document it is for our own provenance, not needed for your review.

---

## 0. What UDT is (one paragraph)
UDT is a proposed extension of general relativity built on a single physical idea: **positional dilation** — the rate of
time (and the associated clock/length scales) varies with position, and this variation is what an observer reads as
cosmological redshift. It is intended to be *relativistic* (a genuine extension of GR, reducing to relativistic
kinematics in the appropriate sense) and to eventually produce **mass and particles** as stable localized solutions of
its own field equations, with the cosmological ("macro") geometry serving as the background/substrate those localized
solutions live in and couple to. The long-term goal is **mass/particle emergence**; this brief is about the **macro
background** that emergence requires.

---

## 1. The strategic pivot — why we stopped doing particle work and turned to the macro background

The project's target is particle/mass emergence: a particle should be a stable, localized, self-consistent solution
("cell") of the UDT field equations. Two problems forced a pivot away from directly hunting particles:

1. **No properly-derived background.** A localized cell must be embedded in — and couple to — an ambient background
   dilation field. We had never *derived* that macro background from the field equations; it had only ever been (a)
   fit to data with a polynomial ansatz, (b) reverse-engineered from a "ladder" of cell-scale approximations, or (c)
   asserted via a circular algebraic identity. So the substrate emergence needs did not exist in derived form.

2. **Tool contamination.** The equations we had been using for "the background" turned out to be a **microphysics /
   finite-cell specialization** of the field equations (details in §4), carrying assumptions imported from the
   particle problem (a specific matter defect, finite-core and mirror-seal boundary conditions, a broken symmetry
   branch). Using a particle-scale tool to model the universe was a category error.

**The pivot:** derive the macro background (the dilation field `φ(r)` and the transverse geometry `D_A(r)`) **and its
matter/mass content** natively from the *uncontaminated* field equations, so that (later) a matter-coupled particle cell
can be embedded in a genuinely-derived environment. The matter content of the universe is not incidental here: we find
(below) that **matter is required even to have a sensible macro background at all**, which makes the macro matter budget
a first-class deliverable — and plausibly the very thing a particle couples to.

---

## 2. The founding postulates (the ONLY inputs to the metric)

UDT's metric is *derived*, not assumed, from three "owner postulates" (Charles's, verbatim), which encode two physical
ideas — **dilation-with-distance** and **observer-equivalence**:

> "Two properties follow directly from the SR and GR analogs: the dilation depends only on differences in φ, so no
> position is geometrically privileged; and dilations compose consistently across intermediate positions. Together
> these requirements uniquely determine the functional form of the metric — it is derived, not assumed. A mutual
> symmetry condition — each observer sees the other's clock run slow, with neither position preferred — forces a
> structural identity between the metric components."

Labelled:
- **(R1)** dilation depends only on *differences* in φ → **no privileged position** (position-translation symmetry).
- **(R2)** dilations *compose* consistently across intermediate positions (transitivity / one-parameter group).
- **(R3)** **mutual reciprocity**: each position sees the other's clock run slow, neither preferred.

These are the complete premise set for the metric-*structure* derivation. **Reviewer flag (load-bearing):** R1 has two
readings — a weak "no privileged zero of φ" (a gauge/shift freedom, which is what the derivation below actually *uses*)
and a strong "no privileged point in space" (full spatial homogeneity). The distinction matters in §6–§7; please keep
it in mind.

---

## 3. How the metric was derived (from R1–R3)

Define the clock-rate function `f(φ) = √(−g_tt(φ)/c²)`. The dilation one observer at `φ_A` assigns to a clock at `φ_B`
is `D = f(φ_B)/f(φ_A)`.

- **R1** ("depends only on differences") ⟹ `D(φ_A,φ_B) = g(φ_B − φ_A)` for a single-variable `g`.
- **R2** (composition) ⟹ `g` satisfies `g(a+b) = g(a)g(b)`, whose continuous solution is **exponential**: `g(x)=e^{λx}`.
  Fixing the normalization of φ gives `f(φ) ∝ e^{−φ}`, i.e. **`g_tt = −e^{−2φ}c²`**.
- **R3** (reciprocity) ⟹ the structural identity **`g_rr = 1/(g_tt/(−c²)) = e^{+2φ}`** (the "B=1/A" reciprocal form).

Result (canonical, Charles-signed): the static, spherically-symmetric line element
```
ds² = −e^{−2φ(r)} c² dt²  +  e^{2φ(r)} dr²  +  D_A(r)² dΩ².
```
The redshift for static observers follows immediately: `1+z = e^{φ_source − φ_observer} = e^{φ}` (observer at `φ=0`).

**Crucial scope of R1–R3:** they fix the metric *form* (how φ enters `g_tt`, `g_rr`) and the *existence* of the redshift
law `1+z=e^{φ}`. They do **not** by themselves fix the spatial *profile* `φ(r)` nor the transverse function `D_A(r)`.
Those require the field equations (§4) and/or an added homogeneity assumption (§6). This gap is where the interesting
open questions live.

---

## 4. The field equations — derivation, provenance, and what we use

UDT is an *extension* of GR, so it needs field equations, and (Principle 1 of our charter) they must be derived
natively from the dilation structure, **not** inherited from GR by default.

**(a) The "EH-empty" pivot.** On the UDT metric family (`g_tt g_rr = −c²`), the bare Einstein–Hilbert integrand
`√(−g)·R` reduces to a *pure boundary term* (its bulk variation vanishes identically — verified by CAS). Physically:
the GR curvature action carries *no bulk content* for this family, so the field equations cannot come from it. This is
the native reason UDT does **not** reduce to "vacuum = GR" and its vacua are non-Schwarzschild. (Reviewer: this is the
key anti-"smuggled-GR" step; please check the claim that `√(−g)R` is a total derivative on `g_tt=−e^{−2φ}c², g_rr=e^{2φ}`
with general `D_A(r)`.)

**(b) The bulk dynamics** come instead from a shift-invariant (R1-respecting) scalar kinetic term for φ. The shared
action skeleton is
```
S = ∫ c √h [ (Z_φ/2) φ'²  +  R^{(2)}[h]  +  𝒦_branch  +  L_m^UDT ],
```
where `h` is the transverse 2-metric, `R^{(2)}[h]` its Ricci scalar, `𝒦_branch` an extrinsic-curvature term, `Z_φ` a
normalization constant, and `L_m^UDT` the matter Lagrangian.

**(c) Two regimes ("branches").** Varying the action gives two regimes depending on how `𝒦` is treated:
- **Branch G** (continuum / asymptotic): the depth-shift `φ→φ+const` is an exact symmetry ⟹ `(r²φ')'=0` ⟹
  `φ = φ_∞ − q/r` (a Coulomb-like, scale-free profile; `q` = a conserved "dilation charge").
- **Branch P** (finite-cell / microphysics): the shift symmetry is *broken* by finite-domain pinning ⟹
  `Z_φ (r²φ')' = 4 e^{−2φ}` — a self-sourcing equation with no asymptotic vacuum ("intrinsically finite-domain").

**(d) Provenance finding (the contamination, and what survives).** An audit established that the **Branch-P** equation,
its junction/"seal" conditions, and the specific `L_m^UDT` (an `S²→S²` winding-defect / hedgehog field of degree N) were
all constructed for the *particle* problem and are **not** appropriate macro tools. The **clean, foundational core** —
safe to build the macro background on — is: the EH-empty pivot (a), the shift-invariant kinetic and **Branch-G**
equation (c), and the metric form (§3). **What we did NOT inherit / what remains open (reviewer flags):**
- `Z_φ` (the kinetic normalization) is an unfixed constant (a genuine free lever; we set `Z_φ=1` by convention, and it
  is degenerate with an overall scale in what follows).
- Treating the transverse `h_AB` as an *independent* dynamical field (the "two-player" ADM split) vs. slaving it is a
  *choice*, not forced by R1–R3.
- What sources the macro φ is **not** fixed by the equations (see §4e). These are the honest gaps; we flag them rather
  than paper over them.

**(e) A structural fact we lean on heavily (please check):** in the native action, **matter does not source φ
directly** — `δS_m/δφ = 0` to leading order — because R1 shift-invariance forces matter onto the *undilated* channels.
Matter influences φ only *indirectly*, through the geometry (`matter → h_AB → 𝒦 → φ`). In Branch G the equation is
literally sourceless. This is why "what sources the macro φ" is a real, unresolved question, not a triviality.

**What we are using going forward:** the clean core — metric form (§3) + EH-empty pivot + shift-invariant kinetic +
the full field equations for `φ(r)` **and** `D_A(r)` with the transverse geometry *unfrozen* (not set to `D_A=r`).

---

## 5. The optics — luminosity distance (a correction we made this session)

To compare any background to supernova (SNe) data we need the luminosity-distance law `d_L = D_A·(1+z)^n`. We derived
`n` natively from the metric (photons on null geodesics — UDT's Maxwell sector is derived minimally-coupled on the
metric, so photon number is conserved) and found **n = 2**, i.e. **`d_L = (1+z)² D_A`** — the standard Etherington
reciprocity. The three contributing factors:
1. **energy per photon** reduced by `(1+z)` (frequency shift `1+z=e^{φ}`);
2. **photon arrival rate** reduced by `(1+z)` — in a static metric successive photons take identical *coordinate*
   travel times, so proper arrival intervals stretch by `dτ_o/dτ_s = e^{φ_s−φ_o} = 1+z`. **This is the same relation as
   factor 1** (frequency = crest-arrival rate); you cannot have the redshift without it;
3. **reciprocity area** factor `(1+z)²` (source-side area distance `= (1+z)D_A`).
Product: `F = L/[4π(1+z)⁴ D_A²]` ⟹ `d_L=(1+z)²D_A`.

**The correction:** our own SNe pipeline had been using **n = 1** (`d_L = r·e^{φ} = D_A(1+z)`) — which is literally
`√g_rr` where the metric forces `g_rr = e^{2φ}`, a dropped factor (the arrival-rate factor 2). That error had been
**flattering** the theory: the ~0.166-mag Pantheon+ fit that looked competitive with ΛCDM was obtained under n=1;
recomputed under the correct n=2 the same background gives ~0.47 mag. **Reviewer flag (load-bearing):** the entire SNe
comparison hinges on n. If you can construct a *legitimate, UDT-derived* reason the arrival-rate factor is absent
(without importing a time-dependent metric or photon non-conservation), that would reopen n=1 — we could not, and
believe Etherington forces n=2. Please attack this. (Caveat: we hold SNe as a *demonstration*, not a decisive yardstick
— at Pantheon+ precision many mildly-curved distance laws fit ~0.15–0.17 mag, so the SNe do not strongly select any
particular functional form.)

---

## 6. First attempt — the VACUUM macro background, and why it fails

We solved the clean-core field equations for the cosmological background with the transverse geometry **unfrozen**
(`φ(r)` and `D_A(r)` both dynamical, matter off). The vacuum Branch-G system (CAS-verified) reduces to:
```
φ'(r) = q / (Z_φ D_A²),        D_A''(r) = − q² / (4 Z_φ D_A³),
```
with `R^{(2)}[h] = 2/D_A²` integrating to a topological (Gauss–Bonnet) constant that drops from the equations of motion.
This has a genuinely **variable-curvature, non-constant** family of solutions (so the geometry is *not* forced to
constant curvature — the field equations have real freedom in `D_A`).

**The failure (structural, not numerical):** producing any redshift requires `q ≠ 0` (else `φ = const`, no redshift).
But with `q ≠ 0`, `D_A → 0` is a curvature/φ-singularity — so the observer cannot sit at a regular center. A luminosity
distance must satisfy `d_L → 0` as `z → 0`, which requires the observer at `D_A = 0`; impossible for `q ≠ 0`. Hence the
low-redshift Hubble behavior comes out wrong and the vacuum misses the SNe by **~2 magnitudes** — and it misses under
*both* n=1 and n=2, confirming the defect is the **sourceless vacuum itself**, not the optics.

**Interpretation:** a sourceless vacuum cannot make a *regular, redshifting* cosmology. Combined with a dimensional
observation — a maximum *distance* scale cannot be built from `c` and `G` alone (you need a mass) — this points to a
single conclusion: **the macro dilation field needs a matter source; matter is what makes the universe have a scale and
a regular structure at all.** (This echoes what we independently found at the particle scale: the *vacuum* is
scale-free and featureless; matter is the scale-and-structure-maker.)

**Also derived (the target the background must hit):** under n=2, the data require an angular-diameter distance
`D_A^req(z) = d_L^data(z)/(1+z)²`, which **rises, peaks near z ≈ 1.6, then turns over** — a non-monotonic shape. Any
successful native background must reproduce this turnover.

---

## 7. The plan — matter sourcing, closure, and the "vacuum-as-limit" hypothesis

Next step (not yet done; it is gated on a framing decision about what sources the macro φ, §4e):

**(A) Matter-sourced background on the clean core, under n=2 optics.** Introduce matter with a *regular* finite core
(density `ρ_c > 0` at the center, curing the vacuum's central singularity) and solve the coupled `(φ, D_A, ρ)` system.
Question: does a matter-sourced native background reproduce the required rise-then-turnover `D_A^req(z)`?

**(B) The closure discipline (this is the key methodological point).** The matter amount is **not** a free knob to be
tuned until the SNe fit. Instead, **the matter budget is bracketed until the universe cell CLOSES** — i.e. until a
self-consistent, regular, finite background solution *exists*. UDT's standing conjecture (the "critical universe") is
that a valid closed cosmology exists only for **one critical amount (or a narrow window) of matter**. If so, that
critical amount is a *prediction*, and the redshift–distance relation, stellar-survey matter density, and the predicted
visible/dark split are all **downstream checks against a derived number**, never inputs used to reverse-engineer a fit.
(UDT predicts the "missing mass" is ordinary but non-luminous baryons — of order ~90% dim baryons — rather than exotic
dark matter; this becomes a checkable consequence once the closure amount is fixed.) **Reviewer flag:** please scrutinize
whether "closure selects a unique/critical matter amount" is plausible or whether closure is achievable for a continuum
of amounts (which would weaken the prediction to a fit).

**(C) The "vacuum-as-limit" hypothesis (Charles, intuitive — flagged as a lead, not a result).** The vacuum solution
came out with a **square-root** shape (`D_A ∝ √(1+z)` on one branch). Conjecture: the vacuum is a *limiting* structure —
analogous to how `c` is a limit in special relativity, where physical quantities are functions of proximity to the
limit through a square root (the Lorentz factor `γ = 1/√(1−v²/c²)`). Here the analogous limit is a **maximum distance
`x_max`** (the coordinate radius where `φ→∞`, `z→∞`; finite in coordinate terms, infinitely far in proper distance —
an unreachable horizon, exactly like `c`). The correct matter-*closing* solution might then be a function of that
vacuum limit. Candidate concrete forms to test: (a) the vacuum is the *exterior/edge* limit near `x_max`, matter
*regularizes* the interior center, and the interior is matched onto the vacuum limit *at closure* (star-interior ↔
Schwarzschild-exterior style); (b) a literal `γ`-analog with observables `∝` a `√`-function of `(1 − r/x_max)`; (c)
perturbative, full = vacuum × (1 + matter correction). **Owed check before leaning on it:** does the vacuum `√`-shape
actually connect onto the data-required high-z shape (§6)? Do not assume it does.

---

## 8. What we most want an external reviewer to check
1. **The EH-empty pivot (§4a):** is `√(−g)R` genuinely a pure boundary term on this metric family? If it has bulk
   content we missed, the whole "native field equations" story changes.
2. **The optics n=2 (§5):** is there any *legitimate, UDT-derived* escape to n=1, or is `d_L=(1+z)²D_A` forced?
3. **`δS_m/δφ = 0` (§4e):** is it true that matter does not directly source φ in this action, only indirectly via
   geometry? This determines whether "matter sourcing the background" even works the way we plan.
4. **The vacuum failure (§6):** is the "redshift ⟹ q≠0 ⟹ central singularity ⟹ observer off-center" chain airtight, or
   is there a regular sourceless redshifting solution we missed?
5. **Closure uniqueness (§7B):** does requiring a regular closed background plausibly select a *critical* matter amount,
   or a continuum?
6. **The homogeneity reading (§2 flag):** does "no privileged position" (R1) license fixing the spatial profile, or only
   the metric form? We believe only the form; a stronger reading would change §6–§7.

---

## 9. Methodology (how we work — and the non-droppable review lane)
We operate under a discipline that separates *making assumptions visible* from *deriving results*: we map a problem and
its premise ledger before solving; we tag every value/boundary-condition as derived / chosen / assumed; we ask
"observing or targeting?" before each solve (never sculpt toward a desired answer); and every banked result — positive
or negative — gets a blind adversarial verification before it is recorded. Negative results are first-class.

The following clause governs what a critic (including you) may and may not block. **It must travel verbatim with this
brief:**

> **LEAVES ROOM FOR THE WORK — the allowed lane (binding; no trigger may fire to block these).** These triggers police
> the SMUGGLE OF PHYSICS, never the BORROWING OF METHOD. CATEGORY-A (conditioning / numerical technique / *how* we
> solve) is ALWAYS GREEN and only needs a soundness/convergence check: borrowing JFNK/Newton-Krylov,
> continuation/homotopy, spectral/collocation, preconditioners, junction-condition/DtN/Calderón & geon formalism,
> machine-precision Taylor replacement — and USING GR AS A REFERENCE/LIMIT (flat/Schwarzschild/de Sitter anchors,
> contrasting to see where UDT departs). A technique changes HOW we solve the UDT equations, not the physics: it is NOT
> a "mechanism/term/coupling" (does not trip #2) and need NOT be "derived from the metric" (does not trip #5); only two
> duties — apply it to the UDT equations (don't silently swap in GR's), and soundness-check it. CATEGORY-B (a change to
> the PHYSICS — a mechanism, coupling, equation-form, source, or a structure-holding BC) is gated. Default for a real
> technique or a GR-as-reference comparison is GREEN; progress is the point. *(This clause is non-droppable and MUST
> travel verbatim with any cross-check payload / local-LLM export — a "forbid"-only half over-blocks.)*

In short: when you review, please distinguish **method** (borrowing a solution technique, or using GR/ΛCDM as a
reference to see where UDT departs — always fine) from **physics smuggling** (adding a mechanism, coupling, or
equation-form that isn't derived from the dilation metric — the thing to catch). We are trying to find what is *real*,
not what confirms the theory.
