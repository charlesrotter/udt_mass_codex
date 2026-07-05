# H4 · N5b — Whole-cell dilation-FLUX-BUDGET / public-dilation-CHARGE closure: does it pin ξ, Z_φ, or (ξ,Z_φ)? — verdict NOT INDEPENDENT of N5a ⇒ ξ (and Z_φ) UN-ANCHORED at armchair

**Status: BANKED — BLIND-VERIFIED (verifier agent a40dce45cfcede943, 2026-07-05: OVERALL HOLDS, no attack flips
the verdict — nothing pins ξ/Z_φ/(ξ,Z_φ) at armchair; independently confirmed p_F=γ/2 is a CONTINUOUS MS charge
(z_CMB-sourced, NOT a quantized quantum number), Z_φ genuinely cancels (criticality is a geometric-MASS statement,
F7), and the co-varying seal identity. ONE REQUIRED CORRECTION FOLDED IN (attack 3): the too-strong "no quantized
charge budget" / Q_H-only rebuttal is REPLACED by explicit engagement of the native D2b FLUX LADDER — which DOES
exist but quantizes DEPTH/PROFILE, not absolute size or ξ (registry P-B "discrete set while absolute size stays
free"), whose absolute anchor is z_CMB (forbidden), and which with the active-P hopfion becomes the gated candidate
D. Minor: CAS §7 is confirmatory-only (the source reading is the real evidence); p_F=MS ⇒ 2p_F=2·MS, factor-of-2
UNPINNED.)**
Armchair / CAS node (sympy algebra + structural reading only; NO numerical solve, NO coupled BVP, NO
fully-coupled compute). Executes node **N5b** of `H4_N5_whole_cell_criticality_MAP.md` §7 (candidate B — flux
closure). DATA-BLIND (no lepton masses; z_CMB / 7.004 used only as the closed OUT anchor, never live; no
fitting); no SM/particle labels; ξ, κ, N, Q_H, Z_φ, φ_amb symbolic/free. Frame **C(a)** (ONE cosmic cell;
hopfion = localized active-P defect ON the ambient bulk; NO private seal / NO carved cell / NO private fold).
CAS re-run inline in §7.

---

## 0. One-line verdict

The whole-cell dilation-flux budget is **Gauss's law for the native φ-field**: integrating the P-branch φ
equation over the cell gives `Π_φ(R) = ∫_cell(source) = −Z_φ M`, which is the **conservation identity that
DEFINES** the very mass `M = −q` that N5a's single criticality relation `M/R = c²/(2G)` already constrains.
Requiring the flux to **close at the cosmic seal** adds nothing, because the seal's public charge is (canon)
`Q = 2p_F = Misner–Sharp mass = the cell's own M` — it **co-varies** with M along the critical line rather than
supplying an independent value. **CAS confirms the closure residual is identically 0 and solving it for ξ returns
∅.** Therefore **flux closure is N5a's one relation dressed in Z_φ-charge language (CF-N5b-i FIRES)**, it inherits
N5a's free dilatation modulus R (CF-N5b-iii FIRES: the budget closes for any ξ), and it pins **neither bare ξ,
nor Z_φ, nor the combination (ξ,Z_φ)** at armchair. The `Z_φ` enters ONLY as the flux↔charge normalization and
**cancels** out of the criticality relation (which uses `M = −q` directly). Candidate B is therefore **reduced,
like candidate A, to the gated non-perturbative N5d solve (candidate D)** — the only surviving channel where a
ξ-scale relation could be pinned; un-closable at armchair (ε≫1, CF-N5f). This is a pre-registered first-class
"does-not-pin" outcome, not a failure, and it **reinforces** N5a.

---

## 1. The native flux-budget equation (Task 1 — derived, no carve)

### 1.1 The conserved dilation flux and the charge
Native field equations (`native_field_equations_constrained_two_player_results.md:110,119`;
`d2b_no_structure_in_G.md:47`) give the round-reduced φ-EL with the branch geometric term:

    Branch P:   Z_φ (r²φ')' = 4e^{−2φ}  (+ 𝒦-shear / matter contributions)          [DERIVED]
    Branch G:   (Z_φ r²φ')' = 0         ⇒  Π_φ ≡ Z_φ r²φ' = const                     [DERIVED]

The **conserved dilation flux** (per solid angle) is `Π_φ = Z_φ ρ²φ'` (`d2b:47`, `d2c:237`); the surface-
integrated form is `Q_φ = ∫√h Z_φ φ' d²x` (`H4_N2_farfield_reduction_results.md:42`). The **Coulomb charge** is
`q = ρ²φ'|_bdy` (from `φ = φ_∞ − q/r`, `native_...:110`), so **`Π_φ = Z_φ q`** exactly. The identifications
(`H4_N2:68–71`): the **geometric (Misner–Sharp) mass equals minus the Coulomb charge, `M = −q`**, to O(1/r)
(they depart at O(1/r²), the genuine nonlinear term `+2q²`), and the flux differs from the charge/mass by exactly
`Z_φ`: **`Π_φ = Z_φ q = −Z_φ M`** (agree only if Z_φ=1).

### 1.2 Integrate over the whole cell (the budget = Gauss's law)
N4rev's monopole operator and N2's surface-integrated form are the same statement
(`H4_N4rev_...:12`, `H4_N2:36`):

    ∂_r[ Z_φ φ'(r) A(r) ] = −2 S(r),   A(r)=∫√h d²x,  S(r)=∫√h 𝒦 d²x                  [DERIVED, N2 Task 1]

Integrate from the **even core** (`Π_φ(0)=0`, `d2b:150`) to the cell boundary R:

    Π_φ(R) = Z_φ φ'(R) A(R) = −2 ∫_cell √h 𝒦 d³x ≡ Q_φ(total)                          [the flux budget]

This is **Gauss's law**: the boundary flux equals the volume-integrated source `𝒦`. With the active-P hopfion as
content (revised-N4 S4: interior active-P everywhere, Σ≠0 — the source is the P-branch geometric term `4e^{−2φ}`
plus the hopfion's **shear-modulation** of √h𝒦, which enters at O(amplitude²), `H4_N2:58`), the budget reads

    Π_φ(R)  =  −Z_φ M  =  Z_φ q       with   M = M_ambient + δM_hopfion,   q = −M      [budget, C(a)-clean]

Keeping every factor: the **flux the interior sources** = `Π_φ(R) = −Z_φ M`; the **flux the cosmic seal
terminates** = `Z_φ × (public charge)`. Canon (`seal_matching_junction_results.md:26–27`): *"the exterior public
charge q IS the interior dilation flux through the seal; public charge Q = Misner–Sharp mass = 2p_F."* So the
seal's terminated charge is **the cell's own MS mass**, `Q_seal = −M` (with the p_F factor-of-2 itself flagged
UNPINNED, `H4_N2:72`). **Closure** ("sourced = terminated"):

    Π_φ(R) = Z_φ Q_seal   ⟺   −Z_φ M = Z_φ(−M)   ⟺   0 = 0                             [CF-N5b-i: IDENTITY]

The closure is an **identity** — the CAS residual is exactly 0 (§7 check 3), and solving it for ξ returns ∅.

---

## 2. ★ Independence test (Task 2 — the pivotal task)

**Question:** is flux closure a genuinely NEW equation, or N5a's criticality `M/R=c²/(2G)` rewritten in
charge/flux language?

**Verdict: NOT INDEPENDENT. It is the same one relation, dressed in Z_φ.** Three distinct sub-statements, none
of which adds a constraint on ξ:

1. **Gauss's law (flux = integrated source) is an IDENTITY, not a constraint.** `Π_φ(R) = ∫_cell(source)` holds
   automatically for ANY solution of the field equation — it is the definition of the enclosed charge `q`, and
   `M = −q`. Zero new equations. It merely *computes* the same M that criticality uses.

2. **The Z_φ cancels out of criticality.** Criticality uses the **geometric mass `M = −q`** directly
   (`M/R=c²/2G`), whereas the flux is `Π_φ = Z_φ q`. Substituting `M = −Π_φ/Z_φ` into criticality (§7 check 2)
   gives `c²/(2G) = −Π_φ/(Z_φ R)` — one relation among (Π_φ, R) in which **Z_φ appears solely as the flux→charge
   conversion factor and does not add information**. So even the Z_φ-normalization is not an independent lever.

3. **The seal charge co-varies with M — it is not an independent value.** The hope (MAP candidate B / CF-N5e)
   was that the seal terminates a *specific fixed* public charge, giving a second equation. But `Q_seal = 2p_F =
   MS mass = M` (canon). It rides the SAME critical line, so requiring `Π_φ(R) = Z_φ Q_seal` reduces to `M = M`
   (identity, §1.2). The ONLY thing that would fix p_F/Q_seal absolutely is the depth anchor `φ_seal = 7.004 =
   ln(1+z_CMB)` — which is **z_CMB DATA, FORBIDDEN here** (and F7 §B proved even the seal + cosmic-criticality do
   not pin ξ).

**What NEW information could the flux/charge statement carry that mass/size does not?** Two candidates, both die:
- *The Z_φ-normalization* (flux ≠ mass by exactly Z_φ). Dies by (2): Z_φ is the conversion factor and cancels;
  criticality is Z_φ-blind because it uses M=−q, not Π_φ.
- *The nonlinear flux/mass difference* (they differ at O(1/r²): `M=−q` only to leading order, `+2q²` beyond). This
  is a genuine nonlinear departure, BUT to turn it into a second independent equation you need a second *fixed*
  boundary datum (the seal charge value) — which is exactly the co-varying `2p_F` (dies by (3)) or the forbidden
  z_CMB depth. At armchair it supplies no independent constraint.

**⇒ Flux closure inherits N5a wholesale:** ONE relation `M/R = c²/(2G)` with **R the unpinned dilatation
modulus** (F7 A.4). CF-N5b-i FIRES. It cannot pin ξ for the same reason N5a cannot.

---

## 3. Z_φ kept explicit — Route A vs Route B (Task 3)

- **Route A (Z_φ FREE — CHOSE/OPEN).** Flux `Π_φ = Z_φ q = −Z_φ M`. Z_φ scales flux-vs-mass but **cancels from
  criticality** (§2.2). The budget is one relation with R free ⇒ **ξ and Z_φ BOTH free**; nothing pins either,
  and there is no independent datum to pin even the combination against (the seal charge co-varies). CF-N5b-ii/iii.

- **Route B (Z_φ = 8 + forced mixing — CHOSE/OPEN).** The Route-B flux is `Π_φ^B = 8ρ²φ' + 4ρρ' = 8ρ²φ̃'`
  (`d2c:64,83`), flux law `Φ_B' = 4e^{−2φ}ρ'² ≥ 0` (`d2c:74`). The kinetic block is identical across branches
  (JC1 `[Z_φρ²φ']=0`), and **E_m(core)=2 is Route-blind** (`d2c:74`). Fixing Z_φ=8 fixes the flux↔charge scale
  but **does not add a criticality equation** — same as Route A, criticality still uses M=−q. So even with Z_φ
  pinned to 8, ξ stays free (R free). **CAVEAT that bites (d2c, `d2c:23,93`):** the live solvers carry Z=8
  **WITHOUT** the inseparable `2e^φKφ'` mixing term ⇒ they are *"not Route B and never can be."* So any pin that
  relied on the Route-B mixing structure (a φ'-JUMP at a G|P seal, `d2c:88`) would be **frame-invalid on the live
  path** — CF-N5b-v. In frame C(a) there is **no G|P seal around the hopfion** anyway (that wall = C(b) = STOP,
  CF-N5b-iv), so the Route-B mixing machinery has no place to act here. Net: neither route pins ξ.

---

## 4. Pin verdict (Task 4)

Does the budget pin **(a) bare ξ**, **(b) a combination (ξ,Z_φ) / √(ξκ)/Z_φ**, or **(c) nothing**?

**Answer: (c) NOTHING — ξ and Z_φ both free.** Reasons, in order of decisiveness:

1. **Same-relation (CF-N5b-i, decisive).** The budget is Gauss's law = the conservation identity defining
   `M=−q`; closure at the co-varying seal is `M=M`. It is N5a's one criticality relation, not a second equation.
   §7 check 3: solve-for-ξ → ∅.

2. **Free-modulus escape (CF-N5b-iii, independently decisive).** Even reading the budget as a magnitude balance,
   the interior source integral depends on the hopfion size `ℓ_hopf ∝ √(κ/ξ)` and the cell radius R — and **R is
   the unpinned dilatation modulus** (F7 A.4/S8 gap). For ANY ξ, one slides R along the critical line so the
   budget closes. The flux **depends on the unpinned modulus ⇒ the budget cannot pin ξ.** (Same escape N5a found:
   ℓ_hopf/ρ_c ∝ 1/√ξ, f(ξ) not a number.)

3. **The one native quantization (the D2b flux ladder) quantizes DEPTH, not size or ξ (verifier-corrected).** The
   MAP names candidate B's mechanism as the "D2b flux ladder / P-interior closure machinery"
   (`H4_N5_...:115`), and that ladder **DOES exist** — the native N=0..22 depth ladder = the integral of the
   P-source, a genuine quantization closure (canon C-2026-07-02-1 / C-2026-07-03-2, "the universe = the N=0 ground
   state of its own ladder"; `d2b:68,150`). So the earlier draft's flat "there is no quantized charge budget" was
   TOO STRONG. But the ladder does NOT pin ξ, for three independently-checked reasons: (i) it is **STATIC-PROFILE /
   depth-node** discreteness — it quantizes the dimensionless depth/node-count while the **absolute size R stays
   free** (`NEGATIVES_REGISTRY.md:88`, P-B: "discrete set while absolute size stays free"); the modulus N5a/F7 call
   unpinned survives intact; (ii) its closure variables are cosmic/geometric (γ, a_seal, θ₀, depth) and their
   ABSOLUTE anchor is `γ=7.004=ln(1+z_CMB)` = z_CMB DATA (forbidden data-blind); ξ is not a ladder variable; (iii)
   once the active-P hopfion contributes to the P-source at O(amp²), requiring closure on a rung becomes the
   **coupled non-perturbative whole-cell closure = candidate D (N5d)**, correctly gated (ε≫1, CF-N5f). Separately,
   the dilation charge is **not** the topological Hopf charge Q_H (which fixes only the *shape* integrals Ê₂,Ê₄ + a
   VK nonzero-minimizer bound); imposing `q ∝ Q_H` to manufacture a size-quantization would be an IMPORT. **Net:
   the native quantization is real but depth-not-size ⇒ no armchair ξ-pin; the size-relevant closure is candidate D.**

4. **Combination (b) also fails.** The only combination the flux could carry is `Π_φ = Z_φ q`; but Z_φ cancels
   from criticality and there is no independent datum to pin `√(ξκ)/Z_φ` against (the seal charge co-varies).
   So not even a (ξ,Z_φ) combination is pinned at armchair. (Had the seal charge been an independent fixed number,
   we would report the (ξ,Z_φ) combination per CF-N5e; it is not — it is the co-varying MS mass.)

**Only surviving channel:** the **coupled non-perturbative whole-cell virial fixed point (candidate D, N5d)** —
where the cell-filling shear energy modifies the flat-space balance ε≫1. Un-closable at armchair (CF-N5f). N5b,
like N5a, is **reduced to D**. (This also confirms the MAP's "A and B may be the same whole-cell closure seen two
ways" — they are: both are `M/R=c²/2G` with R free, one in mass language, one in flux/charge language.)

---

## 5. What is DERIVED vs OPEN vs REFUTED

**DERIVED (armchair, CAS-checked, C(a)-clean):**
- The whole-cell flux budget is **Gauss's law**: `Π_φ(R) = −2∫_cell√h𝒦 = −Z_φ M = Z_φ q` (even core kills the
  inner boundary term). Keeps every Z_φ and e^{−2φ}.
- Flux closure at the cosmic seal is an **IDENTITY** (`Q_seal = 2p_F = MS mass = M`, canon; residual ≡ 0, §7).
  It is **NOT an independent equation** — it is N5a's single criticality relation in Z_φ-charge language
  (CF-N5b-i). Z_φ enters only as the flux↔charge conversion and **cancels** from criticality.
- The budget pins **nothing about ξ**, and not even the combination (ξ,Z_φ), at armchair (CF-N5b-ii/iii);
  ξ and Z_φ both remain free. `ℓ_hopf/ρ_c ∝ 1/√ξ` reported honestly (heir of H4-CF4 / N5a).
- The one native quantization (the **D2b flux ladder**) is real but quantizes **DEPTH/PROFILE, not absolute size
  or ξ** (registry P-B; absolute anchor = z_CMB, forbidden); its hopfion-coupled form is candidate D (gated). The
  interior dilation charge is continuous (geometric-source integral), not the topological Q_H. ⇒ no *size/ξ*
  quantized budget at armchair.

**OPEN / GATED (cannot be closed at armchair):**
- Whether the **coupled non-perturbative whole-cell virial fixed point** (candidate D, N5d) pins ℓ_hopf/ρ_c hence
  ξ. This is the ONLY surviving anchoring channel; ε≫1 forbids a perturbative close (CF-N5f). Both N5a and N5b
  reduce to it.
- CF1 (net far-field flux zero-or-not) remains OPEN from N2 (exact cancellation provably NOT forced; shear at
  O(amplitude²)) — but its resolution does not change the pin verdict (it changes the *magnitude* of δM, still
  absorbed by the free R modulus).

**REFUTED / pre-registered failures confirmed:**
- **Candidate B (flux closure) as a bare-ξ or (ξ,Z_φ) anchor at armchair** — REFUTED: it is criticality in flux
  language (CF-N5b-i) with the same free-modulus escape (CF-N5b-iii).
- Route-B-specific pins die on the live path (d2c "never Route B" mixing caveat, CF-N5b-v) — and have no G|P seal
  to act on in C(a).
- (Inherited) Candidate C (active-P onset), Candidate E (z_CMB) remain closed clean failures.

---

## 6. For the verifier — attack surface (aim hardest where a confirmation-smuggle is most likely)

1. **★ Is the "identity" real, or did I hide a second equation?** Attack §1.2/§2.3: is `Q_seal = 2p_F = MS mass =
   M` genuinely the SAME M as in criticality (co-varying), or is 2p_F an independent datum I wrongly collapsed? If
   the seal public charge can be fixed WITHOUT z_CMB data and WITHOUT a private seal, the closure becomes a real
   second equation and could pin the R modulus (⇒ pin ξκ, CF-N5e). Check the canon `Q=2p_F=MS` and the p_F
   factor-of-2 "UNPINNED" flag (`H4_N2:72`) — I claim these make the seal charge co-vary, not anchor.
2. **★ Did Z_φ REALLY cancel?** Attack §2.2: criticality uses `M=−q` (Z_φ-free) while flux is `Z_φ q`. Is there a
   native step where the criticality law itself must be written in flux units (so Z_φ does NOT cancel)? If
   criticality is natively a FLUX statement (not a mass statement), Z_φ survives and a (ξ,Z_φ) combo could be
   pinned. I claim `M/R=c²/2G` is the geometric-mass statement (F7), Z_φ-blind. Attack that.
3. **Charge-vs-topology smuggle.** §4.3: I assert the dilation charge q is continuous, NOT locked to Q_H. Someone
   wanting discreteness will try `q ∝ Q_H` (quantized ⇒ pins ξ). Verify there is NO native identity forcing it —
   if there is, the budget could quantize and the verdict flips. (This is the most tempting import.)
4. **Frame smuggle (CF-N5b-iv).** Confirm no step draws a private seal / carved cell / private fold around the
   hopfion (that = C(b) = STOP). The seal used is the ONE cosmic seal; JC1 is local flux-continuity, not a wall.
5. **Active-P vs φ-blind tension.** The hopfion matter is φ-blind (d2b: φ-blind ⇒ source-free ⇒ q=0), yet
   revised-N4 says active-P (Σ≠0). I resolved this as: the φ-source is the P-branch GEOMETRIC term `4e^{−2φ}` +
   O(amplitude²) shear, NOT a direct matter-φ coupling. Verify this is right and that it does not secretly give
   the hopfion an independent quantized charge (ties to attack 3).
6. **Non-perturbativity gate.** Confirm no step CLOSES the pin with a perturbative magnitude argument (ε≫1);
   candidate D stays gated (CF-N5f). The budget is used only structurally.
7. **Independence claim vs N5a.** The core deliverable is "not independent of N5a." Verify I did not manufacture
   that by under-reading the flux statement — is there ANY solve-relevant content in `Π_φ = Z_φ q` beyond what
   `M = −q` already carries? I claim no (Z_φ = conversion factor). If yes, N5b is independent and the verdict
   changes.

---

## 7. CAS checks (sympy; algebra only, no solve) — §7 reproducible

**Check 1 — flux budget = Gauss's law (identity).** Integrating `∂_r[Z_φ r²φ'] = source` over [0,R] with even
core φ'(0)=0 telescopes to `Π_φ(R) = ∫₀^R source dr` — the definition of the enclosed charge. No constraint;
computes `q`, and `M = −q`.

**Check 2 — Z_φ cancels from criticality.** With `M = −q`, `Π_φ = Z_φ q ⇒ Π_φ = −Z_φ M`. Substituting `M =
−Π_φ/Z_φ` into `M/R = c²/(2G)` gives `c²/(2G) = −Π_φ/(Z_φ R)` — one relation in (Π_φ, R); Z_φ appears only as the
flux/charge conversion. (sympy `subs` + `simplify` confirms.)

**Check 3 — closure at the seal is an identity; solve-for-ξ → ∅.** With `Q_seal = −M` (canon Q=2p_F=MS mass) and
the budget `Π_φ(R) = −Z_φ M`, the closure `Π_φ(R) = Z_φ Q_seal` has residual `(−Z_φ M) − Z_φ(−M) = 0`
identically. `sympy.solve(Eq(−Z_φ M, Z_φ(−M)), ξ) → []` (ξ unconstrained). (Re-run clean this node.)

**Evidential-weight caveat (verifier-flagged):** checks 1–3 are CONFIRMATORY only — check 3 ASSUMES `Q_seal=−M`
(the co-varying seal identity), which is the very point at issue, so the CAS does no independent work. **The
substantive evidence is the SOURCE READING** (p_F=γ/2 a continuous z_CMB-sourced MS charge — `archive/dpf_results.md`,
F7 P4/P5; Q=MS mass — `seal_matching_...:26`; criticality Z_φ-free — F7 A.1), not the algebra. The CAS just checks
the algebra is self-consistent once the sourced identities are granted.

(Reproducible sympy in the session scratchpad; all elementary and re-run clean. NO numerical solve, NO BVP.)

---

## 8. Premise ledger (chose / derived / theory / habit)

| Premise | Tag | Note |
|---|---|---|
| Conserved dilation flux `Π_φ = Z_φ ρ²φ'`; charge `q = ρ²φ'|_bdy` | **DERIVED** (`d2b:47`, `native_...:110`) | the budget's object |
| `Π_φ = Z_φ q` (flux = Z_φ × charge) | **DERIVED** (`H4_N2:70`) | Z_φ is the flux↔charge conversion |
| Geometric mass `M = −q` (to O(1/r); depart at O(1/r²), `+2q²`) | **DERIVED** (`H4_N2:68`, `native_...:63`) | criticality uses M, not Π_φ |
| Budget = Gauss's law `Π_φ(R) = −2∫√h𝒦 = −Z_φ M` (even core Π_φ(0)=0) | **DERIVED** (`H4_N2:36,42`; `d2b:150`) | integrated field eq; identity |
| Seal public charge `Q = MS mass = 2p_F` (so `p_F = MS`, `2p_F = 2·MS`) | **DERIVED (canon)** (`seal_matching_...:26`; co-variance backed by F7 P4/P5) | `p_F=γ/2` a CONTINUOUS z_CMB-sourced MS charge (NOT a quantized quantum number, verifier-confirmed) ⇒ co-varies with M, not an independent datum |
| p_F factor-of-2 (Q=2p_F vs p_F=MS) | **UNPINNED** (`H4_N2:72`) | a dimensionless factor cannot pin a scale/coupling; cancels like Z_φ |
| Universe cell criticality `M/R = c²/(2G)` | **DERIVED (frame-closed, verified)** (F5/F7) | honor "circular-by-construction"; the one relation |
| R = dilatation modulus, unpinned data-blind | **DERIVED** (F7 A.4/S8) | the free-modulus escape; the depth anchor is z_CMB DATA (forbidden) |
| Hopfion interior ACTIVE-P everywhere, Σ≠0 | **DERIVED** (revised-N4 S4) | source = P-branch `4e^{−2φ}` + O(amp²) shear, NOT direct matter-φ coupling |
| Hopfion matter φ-blind | **DERIVED** (H3 prereg) | resolves w/ active-P via the geometric source (attack 5) |
| Dilation charge q continuous (not the topological Q_H); native quantization = D2b flux LADDER (depth, not size/ξ) | **DERIVED** (ladder: canon C-2026-07-02/03; depth-not-size: registry P-B) | q∝Q_H would be import; the real ladder quantizes depth, leaves R free, hopfion-coupled form = candidate D (attack-3 correction) |
| Frame C(a): no private seal/cell/fold for the hopfion | **THEORY/CHOSE — Charles-ruled (N3)** | violation = C(b) = STOP (CF-N5b-iv) |
| Z_φ fork (Route A free / Route B=8 + mixing) | **CHOSE / OPEN** | cancels from criticality; Route-B mixing = "never Route B" on live path (CF-N5b-v) |
| Backreaction NON-PERTURBATIVE (ε≫1) | **DERIVED** (revised-N4 S6) | forbids perturbative CLOSURE; candidate D gated |
| z_CMB / 7.004 as an anchor | **DATA — OUT of scope** | the only thing that would pin p_F / R; forbidden |
| CAS sympy positivity assumptions | **Category-A conditioning** | soundness, not physics |

---

## 9. Pre-registered clean failures (frozen BEFORE the verdict)

- **CF-N5b-i — FIRED.** Flux budget = criticality in flux/charge language ⇒ inherits N5a's un-anchored ξ. (The
  central verdict: Gauss's law identity + co-varying seal charge ⇒ no independent equation.)
- **CF-N5b-ii — partially engaged.** The budget does not even pin a (ξ,Z_φ) combination at armchair — Z_φ cancels
  from criticality and there is no independent datum to pin `√(ξκ)/Z_φ` against. (Would fire as the *reported*
  outcome IF the seal charge were an independent fixed value; it is not.)
- **CF-N5b-iii — FIRED.** The unpinned dilatation modulus R (and size ℓ_hopf∝√(κ/ξ)) lets the budget close for
  any ξ ⇒ nothing pinned. Independent of CF-N5b-i and equally decisive.
- **CF-N5b-iv — held (no smuggle).** No private seal / carved cell / private fold was drawn around the hopfion;
  the seal is the ONE cosmic seal, JC1 used only as local flux-continuity. (STOP tripwire not triggered.)
- **CF-N5b-v — held/relevant.** A Route-B-only pin (relying on the `2e^φKφ'` mixing / φ'-jump at a G|P seal)
  would die under the d2c "never Route B" caveat AND has no G|P seal to act on in C(a). No such pin was banked.
- **CF-N5b-vi (added this node; verifier-corrected) — the native quantization is DEPTH, not size/ξ.** The one
  genuine native quantization (the **D2b flux ladder**, N=0..22 depth ladder = integral of the P-source) quantizes
  the dimensionless depth/node-count while the **absolute size R stays free** (registry P-B); its absolute anchor
  is z_CMB (forbidden); ξ is not a ladder variable; the hopfion-coupled form is candidate D (gated). Separately the
  dilation charge is not the topological Q_H — imposing `q ∝ Q_H` would be an IMPORT. So there is no *size/ξ*
  quantized budget at armchair, even though a *depth* quantization exists. (§4.3; the earlier "no quantized budget"
  was too strong — corrected.)

---

## 10. LAB-LOG
- (this node) armchair/CAS only; sympy checks 1–3 re-run clean (closure residual ≡ 0; solve-for-ξ → ∅); NO solve,
  NO BVP. Reads: N5 MAP, N5a, native_field_equations, d2b, d2c, N4rev, N2, seal_matching, CANON. NOT committed
  (verifier-before-record). **Owes a blind adversarial verifier pass** before any banking or NEGATIVES_REGISTRY
  edit. Verdict REINFORCES N5a and CLOSES candidate B at armchair (reduced to the gated N5d solve = candidate D).
