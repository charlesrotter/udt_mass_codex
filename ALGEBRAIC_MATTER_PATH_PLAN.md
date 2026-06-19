# PARALLEL PLAN — The Algebraic Path to Matter (+ numeric check track)

**Status:** PLAN / MAP (Charles + driver, 2026-06-18). **NOT canon.** Lay framing + technical targets.
Forked-agent repo-evidence pass + the session's armchair reframe both point here.

---

## The strategic insight (Charles, 2026-06-18)

~A week of NUMERIC routes to matter (solitons, catalogs, field-equation couplings) all
dissolved as "built on sand." The diagnosis is now sharp and **partly structural, not just an
AI failing**:

- A numeric solver **must** discretize — a grid, a box `R`, a core cutoff, a truncation, a BC.
  **Each is a fixed value**, so a numeric run **cannot be "completely clean" by construction** —
  the discretization *is* a smuggled scale. This is exactly why masses kept coming out
  box-controlled (`~1/R`) or grid-dependent. A "full clean solution-space *scan*," done
  numerically, is close to a contradiction in terms.
- On top of that structural pressure, an AI driver reaches for the tractable slice. **Both
  pressures push the same way** — toward sand.

**The alternative — an ALGEBRAIC path.** Exact symbolic / topological / representation-theoretic
structure: **no grid, no box, no cutoff, no BC ⇒ no fixed value for a shortcut to hide in.** And
algebra **characterizes the whole solution space at once** (solving a polynomial gives *all* roots)
rather than *scanning* it numerically — sidestepping the full-scan limitation directly. Discreteness
is then **guaranteed by the algebra** (integers / cohomology classes have no continuum), instead of
hoped for from a numeric scan that kept failing to produce it.

**This is returning to UDT's own DNA, not a detour.** Every clean, discrete success has been
algebraic; every numeric build became sand. Repo evidence (forked-agent count): `character` 256,
`Diophantine` 209, `closed-form` ~200, `cohomology` 72, `area form` 60, `representation theory` 22,
`transfer ladder` 11, `index theorem` 6, `junction condition` 5. The clean wins —
`q=1/3`, `N=3`, `η=1/18` (area form / cohomology, integers, no grid); `1+z=e^φ` (identity); SNe
(closed-form); the Diophantine cosmological coefficients `{3/2, cos(π/5), 2/3}`; the founding
integer-insight (digits as keys into algebraic space) — **all live in this layer.**

---

## Two parallel tracks

### TRACK A — numeric (BACKGROUND; CHECK only, not the instrument of discovery)
The gated native-matter step on the cleanest kernel (time-live + native L2+L4), running in
background (agent `ada94df…`). Role: a concrete data-point and a **spot-confirmation** for algebraic
results — an algebraic mass should agree with a clean numeric mass where both exist. All shortcuts
flagged; no presumed success. **We do NOT bet the program on it**, and the strong prior is it lands
where #56/#60/phase3b did (continuum / `~1/R` box scale / solver wall). Retained as a check, demoted
as a discoverer.

### TRACK B — algebraic (FOREGROUND; the primary bet)
Find matter's structure — charge, mass, spectrum — as EXACT algebraic / topological /
representation-theoretic objects of the metric. **Switch the layer, not the solver.**

- **B0 — charge (DONE; the template).** Integer read-off from the area-form degree / H1 cohomology:
  `N=3`, `q=1/3`. Discrete, no solver, no grid. *Re-state the METHOD cleanly* — it is the template
  every other read-off must imitate.

- **B1 — mass as the dilation COST of the charge (closed-form read-off).** Pose the
  **Misner–Sharp mass against the area-form charge** *symbolically* — mass as an exact functional of
  an algebraically-determined profile, **discrete because the charge is**. NOT a numeric soliton
  mass. (Adjacent algebraic fact found this session: the exponent `a` is assembled from the metric's
  *own* `e^{±2φ}` dilation exponents — an algebraic combination native to the metric, not a number
  to crunch. The mass-cost should be the same kind of object.)

- **B2 — the spectrum / discreteness (the real prize).** The generations / mass hierarchy as
  ALGEBRAIC structure where discreteness is GUARANTEED. The corpus already names the natural home:
  the **transfer-ladder / junction-condition algebra** — a recursion / representation problem with
  exact (integer / rational) solutions and **no grid to import a scale**. Charles's standing
  phi–angular hunch enters HERE as the *algebraic coupling* of the radial-dilation structure to the
  angular-cohomology structure (an index-theorem / representation-theoretic pairing, not a coupled PDE).

**Tools:** exact symbolic (sympy identities, mpmath high-precision anchors), de Rham / cohomology,
representation theory of the metric's symmetry group (`SO(3)×ℝ_t×ℤ₂ᴾ×ℤ₂ᵀ`), index theorem,
transfer-ladder / junction recursion, integer-relation detection (PSLQ-style — the digit-as-search-key).
**NO grids, NO numeric PDE as the instrument of discovery.**

**Guardrail (the algebraic path's "no-shortcut" rule).** The KNOWN failure mode here is **NUMEROLOGY**
— small-rational / integer coincidences (caught before: `{3,5,7}`, the `Δp_F` splice). Every
algebraic read-off MUST pass the project's TEST-B null-test classifier (generalize → solve →
check N-specificity; small-rational coverage ~16–23%) and be **pre-registered** before testing.
This is the algebraic analog of "no numeric shortcuts," and it is non-negotiable.

---

## Why TRACK B escapes the sand (structural argument)

1. No grid / box / cutoff / BC ⇒ no fixed value ⇒ no shortcut can sneak in.
2. Exact symbolic ⇒ the engine enforces no-fudging (you cannot shortcut an identity).
3. Characterizes the WHOLE solution space at once ⇒ no numeric scan ⇒ sidesteps the AI-full-scan
   limitation Charles named.
4. Discreteness is GUARANTEED by the algebra ⇒ the very thing numerics kept failing to produce is
   *free* here.
5. Matches the tool to where UDT has actually produced clean results.

**Honest risk (not hidden):** the algebraic structure for *mass* might not close as cleanly as it did
for *charge* — not everything is algebraic, and B is a BET (a well-motivated one), not a guarantee.
The guardrail (null-test) is what keeps a *failed* B-bet from masquerading as numerology success.

---

## Convergence with the armchair reframe

Track B is the **algebraic form** of the session's reframe ("a particle is read off the geometry like
charge, not built"): the read-off must be EXACT / algebraic, not numeric. Numeric crunching was the
wrong tool *because* it forces the fixed-value compromises; the algebraic read-off is the right tool
*because* it doesn't. **Next concrete move:** B1 — pose "what does the area-form charge cost in
dilation" as a symbolic closed-form, with B2's transfer/junction spectrum as the follow-on.
