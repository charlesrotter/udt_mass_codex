# H4 · N2 — Native far-field / multipole reduction of the localized toroidal hopfion source

> **★ CONDITIONS-CHANGED (2026-07-06, N4a `H4_N4a_source_background_audit_results.md`, blind-verified):** the clean
> monopole **δφ = −δq/r** and the radius-independence / box-control diagnostic below are valid ONLY on a
> **source-free exterior** — a **Branch-G / continuum** far field, or a **shallow ambient** e^{−2φ_amb} < Z_φ/32.
> On a **deep Branch-P ambient** the exterior φ-operator is SCREENED — Z_φ(r²δφ')' + 8e^{−2φ_amb}δφ = 0, roots
> −½±√(Z_φ−32e^{−2φ_amb})/(2√Z_φ) — and above critical depth (φ_amb ≲ 1.73 at Z_φ=1) the far field is log-periodic
> **r^{−1/2}cos(ω ln r) with NO clean monopole mass.** N2 dropped the φ-dependence of the Branch-P source (it
> conflated matter-source-free T=0 with source-free; the geometric 𝒦 source persists in the ambient) — the same
> "round+φ≡0 is not a vacuum" fact N2 applied to the SHEAR but not to its own MONOPOLE. So **whether the hopfion
> has a clean far-field mass reduces to the OPEN G/P switch criterion for its far field** (equivalently its unpinned
> depth). The ℓ=0/ℓ=2 split, the source, frame C(a), and the Phase-structure below all STAND; only the monopole's
> unconditional-Branch-P reading is corrected to conditional.

**Status: BANKED, blind-verified (2026-07-06). Armchair/CAS (sympy symbolic only; NO numerical solve, NO data,
no open decision taken — branch/Z_φ symbolic, no seal class/seal-meaning chosen, frame C(a) read-surface-in-bulk
throughout).** Node N2 of `H4_backreaction_mass_MAP.md`, building on the blind-verified N1
(`H4_N1_offround_transverse_equation_results.md`). Deriver agent af7e8b933941e0572; blind adversarial verifier
a4f8815fc33d66105 (all 6 targets PASS; independently re-derived; hunted for a forced-cancellation identity and
found NONE). Provenance scripts: `h4_scripts/n2_checks.py`, `vv_n2.py` (sound, re-run to exact 0),
`n2_shear_BUGGY_do_not_cite.py` (UNRELIABLE — see caveat).

## Headline
A localized toroidal hopfion **admits a native far-field reduction** on a bulk read-surface (frame C(a): a
mathematical Gaussian surface in the universe cell's own P-bulk at ℓ_hopf ≪ r ≪ fold distance — NOT a private
seal). Clean structural split: **the mass-bearing MONOPOLE lives entirely in φ** (forced — the ledgered φ=φ(r)
longitudinal form has zero angular DOF), and **the higher multipoles live entirely in the transverse-metric shear
δh_AB.** The monopole δφ ≈ −δq/r is derived natively (the 1/r from the ρ=r area growth A=4πr², NOT from
Schwarzschild). **CF1 (net flux zero-or-not) stays OPEN** — exact cancellation is provably NOT forced, and is now
shown to be an intrinsically finite-amplitude (O(amp²)) question ⇒ a genuine N4 solve output. **No clean failure
trips**; the monopole reading is native, not hand-imposed spherical symmetry.

## Task 1 — the monopole reduction (PASS)
Integrating the N1 Branch-P equation ∂_r(√h Z_φ φ') = −2√h 𝒦 over the closed transverse surface (φ', Z_φ pull out):
```
d/dr[ Z_φ φ'(r) A(r) ] = −2 S(r),   A(r) ≡ ∫√h d²x,   S(r) ≡ ∫√h 𝒦 d²x   (the surface-integrated ℓ=0 source)
```
Because φ=φ(r) is longitudinal it can carry ONLY the ℓ=0 (monopole) projection; all anisotropy is carried by
h_AB (its traceless shear). In the clean exterior (source compact-support, H1: T=0, h→round ambient, A_amb=4πr²
by ρ=r) the homogeneous equation `d/dr[Z_φ δφ' · 4πr²]=0` gives, with δφ→0 outward:
```
δφ(r) = −δq/r   on the read-surface,   δq = δQ_φ/(4π Z_φ),   δQ_φ ≡ ∫√h Z_φ δφ' d²x (conserved flux)
```
The 1/r is NATIVE (round-ambient area growth), not a Schwarzschild import. JC1 ([√h Z_φ φ']=0) enters only as
LOCAL flux-continuity in the bulk, never as a wall. Round check (CAS): 𝒦_round=−2e^{−2φ}/r² reproduces
Z_φ(r²φ')'=4e^{−2φ}.

## Task 2 — CF1: net flux is NOT forced to cancel (PASS; stays OPEN, now strengthened)
Net far-field flux δQ_φ = −2∫δ(√h 𝒦) d³x. CAS identity (verified): for h_AB=[[a,s],[s,b]],
`√h 𝒦 = −½ e^{−2φ}(a'b'−s'²)/√h`, and det(∂_r h_AB)=a'b'−s'² is **QUADRATIC in the r-velocities**
(∂²/∂a'∂b' ≠ 0). A total r-derivative of any state function F(a,b,s,φ) is LINEAR in velocities ⇒ √h𝒦 is NOT a
total r-derivative ⇒ **no Gauss/divergence identity forces ∫√h𝒦 d³x = 0.** Verifier searched adversarially for a
missed identity (Gauss–Bonnet applies to R^(2) not 𝒦; on-shell √h𝒦=−½∂_rΠ_φ is circular; the Hamiltonian
constraint carries φ'² not a linear forcing) — **NONE forces cancellation.** Explicit compact profile returning to
ambient: ∫√h𝒦 dr = −4R⁷/105 ≠ 0 (δq=0 demonstrably not forced).
**★ Strengthening (verifier V3, recorded):** at LINEAR order about round ambient,
`δ(√h𝒦) = [ −(r·δa)' − (r·δb)' + 4δφ ]|sinθ|` — the h-shape pieces are **exact total r-derivatives** and integrate
to ZERO over compact support; the shear contributes only at **O(amplitude²)**. So the net far-field charge from a
localized shape deformation is intrinsically a **finite-amplitude** object — which REINFORCES "CF1 open, needs the
N4 finite-amplitude solve" (the sign-varying-integrand framing is exactly right). **CF1 stays OPEN.**
**Reconciliation with the positive L2+L4 energy (PLAUSIBILITY, not proof):** MS mass m'=4πρ²ρ'ε, ε>0, ρ'>0 ⇒
δm>0; MS identity ⇒ m=−q=M at O(1/r); so a positive geometric mass would sign-lock δq — but this presupposes the
far-field IS a Coulomb monopole (the thing CF1/CF6 test), so it is a lead, NOT a proof (and CF2 negative-mass
remains the pre-registered prime risk). N4 must compute ∫δ(√h𝒦)d³x on the resolved hopfion profile.

## Task 3 — what a read-surface measures (PASS)
Series of `1−2m/ρ = e^{−2φ}ρ'²` (ρ=r, φ=−q/r, φ_∞=0): **m = −q − q²/r + O(1/r²)** ⇒ at O(1/r) **δm = δM = −δq**
— the MS geometric mass and the Coulomb-charge mass **coincide**. (The sub-leading −q²/r is the genuine nonlinear
departure from Schwarzschild — Principle-2-relevant, not an import.) The conserved dilation flux
δQ_φ = 4πZ_φ δq = −4πZ_φ δM differs from the charge/geometric-mass by exactly **Z_φ** (agree only if Z_φ=1; with
the Z_φ fork OPEN they differ). **A read-surface reads BOTH masses (geometric δm and Coulomb −δq) as the same
number, and the flux as that × Z_φ.** Conventions flagged UNPINNED (not chosen): φ_∞=0 gauge; the M=−q sign; the
p_F factor-of-2 (Q=2p_F vs p_F=MS).

## Task 4 — no ℓ(ℓ+1) tower; shear exponent OWED (PASS-with-caveat)
G^(2)_AB ≡ 0 in 2D (CAS-verified, fully general non-round metric) ⇒ R^(2) exerts zero local stress and drops from
E^{AB}; and K_AB=½e^{−φ}∂_r h_AB carries only r-derivatives ⇒ **E^{AB} contains NO angular derivatives of h_AB.**
So the exterior shear operator has **no ℓ(ℓ+1) eigenvalue** — the shear multipoles do NOT split by ℓ the way GR's
1/r^{ℓ+1} tower does. This is a **genuine native departure from GR**, sound WITHIN the ledgered form (block-
diagonal, φ longitudinal, zero shift). **The precise shear radial exponent is OWED to a linearized solve about the
true exterior background φ_amb(r)** (round+φ≡0 is NOT a vacuum of E^{AB}); N2 correctly did NOT fabricate one.
"Mass is monopole-dominated regardless of the shear exponent, provided the shear does not grow" is honest **as a
conditional** (it rides on shear-decay = the owed exponent).
**★ CAVEAT (verifier):** `h4_scripts/n2_shear_BUGGY_do_not_cite.py` is UNRELIABLE (it wrongly assumed round+φ≡0
is a vacuum ⇒ nonzero spurious background E^{θθ}; sqrt(sin²) artifacts). Its indicial roots are meaningless — do
NOT cite them for any shear exponent. No banked claim depends on it (the exponent is explicitly deferred).

## Task 5 — form-consistency: monopole reading is NATIVE, not hand-imposed (PASS)
- **Exterior:** compact support + H1 (zero net π₂ flux, n→n_∞, F=0 outside the ball) ⇒ ordinary round vacuum ⇒
  no ℓ≥1 source ⇒ φ=φ(r) EXACTLY consistent ⇒ the monopole reading is native (it follows from the ledgered
  longitudinal form + the clean exterior, NOT from assuming h_AB round — h_AB carries the full toroidal anisotropy;
  that is where the multipoles live).
- **Interior:** the toroidal 𝒦 has ℓ≥2 (quadrupole) structure that COULD drive φ-angular parts (φ=φ(r,x)) — this
  is exactly N1 scope caveat #1 (radial-shift / angular-φ outside the ledgered form). Those interior ℓ≥2 φ-parts
  are confined to r<r_torus and decay faster than the monopole, so they do not undermine the far-field δq. **N4
  must allow, or check the smallness of, interior φ-angular ℓ≥2 excitation — do NOT silently inherit φ=φ(r).**

## Clean-failure audit (which tripped) — NONE
- Far-field reduction does not exist → NO (it exists, Task 1).
- Only multipoles survive / monopole forced zero (= CF1 tripped) → NO, CF1 OPEN (non-cancellation provable; net is
  finite-amplitude).
- Round-mass reading requires hand-imposed spherical symmetry → NO (native from the ledgered form + clean exterior).
- Revives the private sealed cell → NO (bulk Gaussian read-surface; JC1 = local flux-continuity; no seal chosen).
- Imports GR multipole machinery → NO (1/r from native area growth; G=8πT never written; Schwarzschild only as a
  far-field reference, with the −q²/r departure explicit).

## Scope caveats carried (honesty)
Within the ledgered metric FORM (φ=φ(r) longitudinal, block-diagonal, zero radial shift). OWED to a later solve:
(i) the shear radial exponent (linearized solve about φ_amb); (ii) CF1 net-flux sign+magnitude (N4 finite-amplitude
solve on the resolved hopfion); (iii) the interior φ-angular ℓ≥2 smallness check. Provenance clean (no GR import,
no sealed-cell revival, no open decision taken). **Next node = N3 (Charles's seal-meaning + which-mass decisions),
then N4 (the gated backreaction solve that computes CF1 + the mass sign + the pinning force).**
