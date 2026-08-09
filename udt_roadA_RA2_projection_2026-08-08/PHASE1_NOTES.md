# RA2 PHASE 1 — the ladder's angular projection, BLIND (symbols + coverage witnesses only)

Date 2026-08-08 | branch grok | RA2 derivation agent (Fable) | Contract: PREREGISTRATION.md
(frozen, e0355637). **NO observational value appears in this file, in `derive_ra2.py` at this
stage, or in the reasoning that produced them (F-RETRO). Machine keys: 23/23 True
(`run_output.txt`).** SCOPE STAMPS travel on every statement: SS9 lock-form ansatz; W1
metric-native scalar probe (tagged THEORY-choice, F-LAWHUNT); equatorial slice (spherical
realization = named inheritance); fixed-(m,omega) pencil analyticity (P-RA1-7); F-MUOFF
honored (mixing in from the first line; h=0 only as derived limits).

## 0. Ground (all re-derived or cited at source)
- RA1 CONSOLIDATED: normal form −v_xx + [Q_c + m²A/r² − 2ωmh/r²]v = ω²v with
  x = ∫ r dr/√(AD), v = √r·R, D = Ar² + h² [re-verified here, RA2_S1, S1b];
  the completed LC/LP/wedge region map; Weyl spacing Δω → π/x_w; Zeeman 2m⟨Ω⟩.
- D1 dictionary: d_A = r(z) = R_w[1 − (1+z)^(−2/n)], A(r(z)) = (1+z)^(−2), finite screen
  d_A → R_w [RA2_S2a,b]; angle of a transverse proper scale s at shell z: θ = s/r(z).
- D4 map+window channel: a RADIAL proper wavelength λ_p at shell z̄ imprints the angular
  scale θ ≈ λ_p(z̄)/r(z̄) (visibility: window spans ≥ one cycle, P-D12 travels).
- O2: closed-form measures exist at h=0 (optical/proper rows). With mixing ON, x(r) has no
  elementary closed form in the frozen class (checked; hypergeometric-type integrals) — so
  low-k levels below use CONTROLLED NUMERICS with machine-checked convergence, per prereg
  ("controlled WKB + machine-checked bounds"); the h→0 closed forms are the anchors.

## 1. Premise ledger (chose-or-derived)
| # | premise | tag |
|---|---|---|
| P-RA2-1 | background/mixing class as RA1 (A=(1−r/R_w)^n, h→h0 u^q near wall), R_w=1, c0=1 in numerics | THEORY (frozen RA1 prereg; scale-free ratios) |
| P-RA2-2 | projection route P-b = the D4 map+window channel (λ_p at a common shell z̄ → θ = λ_p/r(z̄)) | THEORY (banked D4 dictionary; the D1 angular action is the identity, so the mode's own m goes to sky-m directly = route P-a) |
| P-RA2-3 | all modes evaluated at ONE common window/shell z̄ (the backdrop view) | DECLARED; consequence: every shell factor cancels in ratios [RA2_S4] |
| P-RA2-4 | multipole dictionary ℓ ≈ π/θ (half-wavelength) | CONVENTION, disclosed; RATIOS are convention-free (ℓ_k/ℓ_j = θ_j/θ_k either way) |
| P-RA2-5 | wall BC in plain-LC regions = Dirichlet truncation (Friedrichs-type representative) + Neumann variant to EXHIBIT the datum freedom | CHOSE, disclosed — the datum is RA1's named missing boundary datum; both shown [RA2_N4] |
| P-RA2-6 | center completion h = h0 (r/R_w)² (1−r/R_w)^q | THEORY(D2 SS3 center-regularity; RA1 P-RA1-8(a)); prefactor → 1 at the wall so the frozen near-wall class is exact at leading order; D3 untouched (endpoint-local) |
| P-RA2-7 | witness values = small rationals for REGION COVERAGE (R1 n=1/2,q=1; R2 3/2,0; R2b 2,−1/2; R4 3,−3/2; wedge 3,−3/4; h0=1/2, Zeeman check 1/10) | CHOSE for coverage (O2/RA1 witness pattern), not fitted; disclosed float list = these + tolerances |
| P-RA2-8 | numeric regularization: truncation [r_min, R_w−u_min], FD on clustered grid | Category-A (soundness checked: grid/cutoff drift keys N1, N5) |

## 2. P-a — the m-spectrum route (the mode's own angular number)
The equatorial mode is e^{imψ}: its own sky structure is angular frequency m directly
(spherical inheritance: ℓ ≥ |m|). Derived joint-spectrum structure, source-free:
- **Band form in m at fixed radial order k** [RA2_S6a]: treating the two m-carriers of the
  normal form as the pencil perturbation,
  **ω_k(m) = ω_k0 + m⟨Ω⟩_k + m²⟨A/r²⟩_k/(2ω_k0) + …** — a LINEAR (chiral, dragging) plus
  QUADRATIC (centrifugal) rotational band. Smooth in m; every integer m is admissible in
  every LC region. **NO ladder-privileged m exists source-free** — with two derived
  exceptions that are structural, not weightings:
  (i) **wedge chirality halving** [RA2_S7a–c; RA1 R5]: in the deep-mixing wedge only
  counter-rotating (ωmh0 < 0) modes are intrinsically quantized — the admissible m-set is
  HALVED by sign; a backdrop built from wedge modes carries one rotation sense only
  (parity-violating angular structure, mixing-created);
  (ii) **band-extremum accumulation** [RA2_S6c]: the mode density in m at fixed ω has a
  van-Hove-type accumulation at m*_k = ω_k0⟨h/r²⟩_k/⟨A/r²⟩_k (m* = 0 iff h = 0 —
  mixing-created, co-rotating side for h0 > 0).
- **Zeeman angular signature** [RA2_S6b, N3, N6]: ω_k(m) − ω_k(−m) = 2m⟨Ω⟩_k. The ±m pair
  at fixed k superposes to an angular pattern of frequency |m| rigidly ROTATING at the
  mode-averaged dragging rate ⟨Ω⟩_k (pattern speed = split/2m). At q=0 with the P-RA2-6
  completion the splitting is EXACT and k-independent: 2m h0/R_w² [N6: −1.00000 at
  h0=1/2, m=1 — first order is exact because Ω is constant there].
- **HONEST-OBSTRUCTION (prereg §2) — the P-a boundary, stated exactly:** the POSITION
  structure in m (admissible set ℤ; band shape; halving; doublet splitting; rotation rate;
  m* accumulation) is derivable source-free — all derived above. The POWER in m (which m
  are lit, hence where any PEAK in multipole sits) provably requires excitation/source
  physics: the spectrum admits every m with no source-free weighting, so a peak SERIES in
  multipole cannot be derived from route P-a. **P-a peak positions:
  RA2-OBSTRUCTED(source-required). The discreteness that CAN make a source-free position
  series lives in the radial order k — route P-b.**

## 3. P-b — the radial-projection route (the derived angular series)
- **Projection kernel** [RA2_S3, S8]: dℓ_p/dx = √D/r = √(A + h²/r²) — so a mode's local
  proper radial wavelength is λ_p(r) = [2π/√(ω² − U)]·√(A + h²/r²), interior form
  λ_p ≈ (2π/ω_k)·√(A + h²/r²). The mixing is the projection kernel's h-carrier: at h=0 it
  is √A (the D4 form); at the wall the kernel is dominated by h (the mixing keeps the
  projected scale finite where the mu-off one collapses with A).
- **The angular series** (common shell z̄, P-RA2-3): θ_k = λ_p(z̄)/r(z̄) ⇒
  **θ_k ∝ 1/ω_k and ℓ_k ∝ ω_k: the backdrop's angular series IS the frequency ladder.**
  Every shell/window/kernel factor is common to all k and CANCELS in ratios [RA2_S4]:
  **ℓ_k/ℓ_j = ω_k/ω_j exactly — shell-independent, convention-free, h0-scale-free.** The
  absolute scale (one overall parameter) rides {x_w(n,q,h0), the shell factor, ℓ(θ)
  convention} and is NOT derived here; the RATIOS are the derived object.
- **(i) Asymptotic ratio law** [RA2_N2; RA1 D4]: Weyl spacing Δω → π/x_w (verified ≤2%
  by k≈10–20 on all four LC witnesses) ⇒ **ℓ_k ≈ ℓ_A·(k + β): an EQUALLY-SPACED comb in
  multipole** (spacing ℓ_A set by the one free scale), with an OFFSET β (BC/potential
  phase). Ratio law ρ_k = (k+1+β)/(k+β), monotone in k and β, → 1 [RA2_S5a,b]. **Offset
  rigidity** [RA2_S5c]: the first ratio fixes β = (2−ρ₁)/(ρ₁−1); then EVERY higher ratio
  is determined — a 2-parameter (scale, offset) family predicts the entire series. This is
  where non-integer ratios live natively: β ≠ 0 makes every ratio non-integer.
- **(ii) Low-k anharmonicity, region by region** (m=0 channel, Dirichlet-wall
  representative; first 5 levels; full tables in run_output.txt):
  R1 (n<1): ratios 1 : 2.5081 : 3.9822 : 5.4494 : 6.9127; β_k = −0.315…−0.265 (k=1…5).
  R2 (mixing-created band): 1 : 2.7886 : 4.5239 : 6.2459 : 7.9608; β_k = −0.411…−0.314.
  R2b (n=2,q<0 line): 1 : 2.5691 : 4.1457 : 5.7115 : 7.2718; β_k = −0.354…−0.303.
  R4 (deep mixing): 1 : 2.4235 : 3.8682 : 5.3101 : 6.7499; β_k = −0.302…−0.291.
  Emergent Phase-1 regularity (stated blind): all four plain-LC Dirichlet ladders land in
  a NARROW offset band β ≈ −(0.26…0.41), i.e. the free-cavity β = −1/2 (Neumann-center ×
  Dirichlet-wall) raised by ≈ +0.2 by the Q_c conjugation potential; β_k drifts slowly
  upward with k (the anharmonic fingerprint, largest at k=1).
  The WALL DATUM moves the whole comb [RA2_N4]: the Neumann-type extension shifts β by
  ≈ +1/2 (R2: β₅ = +0.188 vs −0.315; zero-mode interlacing checked) — a Robin family
  sweeps β continuously. So within plain-LC regions the offset is the FREE wall datum
  (RA1's one missing boundary datum), spanning ≈ [−0.4, +0.2] over the witness set.
  The |m|>0 channels shift β upward further (center index |m|; the Bessel-phase +|m|/2).
- **The wedge channel** (intrinsic, NO wall datum; counter-rotating m=−1 witness): levels
  truncation-INSENSITIVE (drift 4×10⁻⁴ under 100× cutoff change vs 3.4 for co-rotating —
  the intrinsic-vs-extension contrast made machine-visible) [RA2_N5]. Its ladder is
  STRONGLY ANHARMONIC at low k: ratios 1 : 1.3304 : 1.6306 : 1.9124 : 2.1794 — spacings
  DECREASE toward π/x_w from above; ω₁x_w/π ≈ 6.6 (a thick soft confining wall lifts the
  whole ladder). A qualitatively distinct comb: dense, slowly-tightening, singlet.
- **Doubling of the projected series** (the prereg question): in plain-LC regions YES —
  every |m|>0 line is a DOUBLET, ℓ_k^± split fractionally by 2|m⟨Ω⟩_k|/ω_k [RA2_N3 ≤0.2%
  agreement with 2m⟨Ω⟩; RA2_N6: exact at q=0], collapsing to singlets at m=0 and as
  h0 → 0 (mixing-created signature). In the WEDGE channel NO — chirality removes one
  partner: singlet lines. Whether doublets are RESOLVED on a real backdrop depends on the
  m-power weighting = source physics (P-a obstruction travels to visibility, not to form).

## 4. Falsifier status at Phase-1 close
F-RETRO: no observational value loaded, cited, or used anywhere above; inputs audited
(script floats = witness rationals + tolerances, P-RA2-7); symbolic layer float-free
[RA2_S9]. F-MUOFF: h in every object; h=0 only as labeled limits [S8]. F-TEMPLATE: no
peak-making language; obstructions first-class. F-FREEZE: routes P-a/P-b both derived; the
equatorial→spherical inheritance + P-RA2 ledger travel. F-SCOPE: positions/ratios only;
heights/amplitudes untouched. Decidable-form restatements (disclosed): RA2_S1 checked on
concrete generic-position rational functions at exact rational points (abstract-Function
radicals defeat sympy simplify); first-run key repairs: the S1 quotient factor (√r/w, a
transcription slip caught by the machine check), N2 moved to the finer grid after a
discretization-limit diagnosis, N4 predicate corrected for the Neumann zero mode
(interlacing verified) — all three fixes are in-script, re-run clean.

PHASE1-BANKED: 23/23 machine keys True; no observational value loaded; ordering evidence =
this marker + file mtimes (PHASE1_NOTES.md and run_output.txt precede any Phase-2 artifact).
