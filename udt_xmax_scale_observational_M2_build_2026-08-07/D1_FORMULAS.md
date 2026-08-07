# D1 — native prediction formulas (M2 prereg §1 D1; frozen menu §2)

Date 2026-08-07 | agent: D1 derivation | machine check: `formulas_d1.py` → `formulas_output.txt`,
**52 checks, ALL TRUE** (each boxed formula cites its KEY). Exact sympy, float-free. NO data
touched; NO fit numbers (F-PEEK clean).

## Premise tags (travel with every formula)

- **Lock + areal anchor** [THEORY, canon C-2026-08-06-1]: ds² = −A c²dt² + dr²/A + r²dΩ²,
  A = e^(−2φ).
- **Observer normalization** [THEORY, prereg §1]: observer at r=0, φ(0)=0 ⇒ A(0)=1
  [KEY A_observer_normalization_all]. (c₀ = 1 throughout — O2's c₀ absorbed here.)
- **Redshift** [THEORY, banked ratio identity]: 1+z = A^(−1/2), i.e. z-depth δ ≡ φ = ln(1+z).
- **d_L convention** [banked, O2 row (g)]: d_L = (1+z)² r, Etherington-consistent with d_A = r
  [KEY Etherington_dL_eq_opz2_dA_all].
- **P-STATIC-RULER** [posit, prereg §4]: one native proper length ell, free nuisance.
- **Proper-ruler REALIZATION** [tagged premise, radial leg]: physical rods measure PROPER length
  in the realized metric, dℓ_p = A^(−1/2)dr. This is NOT the kernel's 'spatial' choice — that
  stays no-pin (CP2 standing).
- Menu frozen per prereg §2 (F-SHOP); n=1 unprivileged (F-STEER) — it appears below only as the
  banked machine cross-check.

## 1. Inversion, d_L, mu (exact; all monotone; endpoints match O2/O3 verdicts)

| | P1: A=(1−r/R_w)ⁿ | P2: A=e^(−r/X) | P3: A=(1+r/X)^(−α) |
|---|---|---|---|
| r(z) | R_w[1−(1+z)^(−2/n)] | 2X ln(1+z) | X[(1+z)^(2/α)−1] |
| KEY | P1_inversion | P2_inversion | P3_inversion |
| d_L(z) | (1+z)² R_w[1−(1+z)^(−2/n)] | 2X(1+z)² ln(1+z) | X(1+z)²[(1+z)^(2/α)−1] |
| d_A(z) | = r(z) | = r(z) | = r(z) |
| dr/dz | (2R_w/n)(1+z)^(−2/n−1) > 0 | 2X/(1+z) > 0 | (2X/α)(1+z)^(2/α−1) > 0 |
| KEY | P1_drdz_closed_form/_positive | P2_… | P3_… |
| z→∞ | r → R_w (wall, finite areal) | r → ∞ | r → ∞ |
| KEY | P1_r_limit_Rw | P2_r_limit_oo | P3_r_limit_oo |

mu(z) = 5·log10(d_L(z)) + const (per profile; the const absorbs units + M_B; mode A fits it free).

**Banked cross-check** [KEY P1_n1_banked_dL_z_zplus2]: P1 at n=1 gives d_L = R_w·z(z+2) exactly
(the banked L form) — reproduced, not assumed.

## 2. LOW-Z EXPANSION AND THE DEGENERACY STRUCTURE (load-bearing for D2/D3)

Every menu profile has the SAME two-parameter low-z form:

**d_L(z) = 2·X_eff·z·[1 + c₂·z + O(z²)]**, equivalently
**mu(z) = 5log10(z) + 5log10(2X_eff) + (5/ln10)·c₂·z + O(z²) + const**
[KEYs P{1,2,3}_lowz_slope_*, P{1,2,3}_lowz_curvature_c2, P1_mu_lowz_linear_term, P3_mu_lowz_linear_term]

| | P1 | P2 | P3 |
|---|---|---|---|
| X_eff (slope scale) | **R_w/n** | **X** | **X/α** |
| c₂ (curvature) | **3/2 − 1/n** | **3/2** | **3/2 + 1/α** |

What low-z data CAN and CANNOT separate:

1. **At leading order, ONLY X_eff is measured.** Low-z SNe constrain R_w/n (P1) or X/α (P3) as a
   single number — (R_w, n) and (X, α) are individually UNIDENTIFIED at O(z), and the three
   profiles are indistinguishable. Any low-z-dominated fit reporting an R_w interval alone hides
   a near-perfect (R_w, n) banana along R_w = n·X_eff.
2. **At second order, the shape enters through c₂ alone, and the menu splits into DISJOINT
   ranges**: P1 ⇒ c₂ < 3/2 (any n>0); P2 ⇒ c₂ = 3/2 exactly; P3 ⇒ c₂ > 3/2 (any α>0)
   [KEYs c2_trichotomy_P1_below, c2_trichotomy_P3_above]. So curvature sign relative to 3/2 is a
   clean model-class discriminator in principle — but P2 is the SHARED BOUNDARY/limit point:
   c₂(P1) → 3/2 as n→∞, c₂(P3) → 3/2 as α→∞, and P1 → P2 POINTWISE as n→∞ at fixed
   X_eff = R_w/n [KEYs c2_P1_limit_n_oo_is_P2, c2_P3_limit_alpha_oo_is_P2,
   P1_profile_limit_n_oo_is_P2]. Large-n P1 and large-α P3 are data-indistinguishable from P2 at
   ANY z where only the first two orders matter — intervals on n and α are expected one-sided
   open toward ∞ from low-z data.
3. **Within P1**: n is identified only via c₂ (and higher orders); R_w = n·X_eff then inherits
   n's uncertainty multiplicatively. Honest interval reporting must quote the (X_eff, n) [or
   (R_w, n) with full covariance] pair, never marginal R_w alone (F-SCOPE).
4. **Consequence for the fitter's parametrization (Category-A conditioning, not physics):**
   sample/optimize in (X_eff, shape) coordinates — (X_eff = R_w/n, 1/n) for P1, (X_eff = X/α,
   1/α) for P3 — where the low-z degeneracy is axis-aligned and the n,α→∞ limit is the interior
   point 1/n = 0. Report back in the frozen (R_w, n)/(X, α) with the exact Jacobian-free
   profile-likelihood (reparametrization leaves chi² surfaces invariant).

## 3. Transverse BAO projection (geometry, one line)

In ds² the proper transverse length of an arc of coordinate angle θ at areal radius r is
∫ r dφ = r·θ (the r²dΩ² term) ⇒ an object of proper transverse length ell at r subtends
**θ = ell/r** — geometry only, no cosmology. Hence, per profile [P-STATIC-RULER tag]:

- **θ_BAO(z) = ell / (R_w[1−(1+z)^(−2/n)])**  (P1)  [KEY thetaBAO_P1]
- **θ_BAO(z) = ell / (2X ln(1+z))**  (P2)  [KEY thetaBAO_P2]
- **θ_BAO(z) = ell / (X[(1+z)^(2/α)−1])**  (P3)  [KEY thetaBAO_P3]

Low-z: θ_BAO ≈ ell/(2·X_eff·z) for EVERY profile — only ell/X_eff is measured at low z (the §2
degeneracy again, now with ell in the numerator: SNe+BAO jointly still only pin ell/X_eff and
X_eff separately once curvature resolves) [KEYs thetaBAO_P{1,2,3}_lowz]. High-z signature:
P1 has a MINIMAL angle θ → ell/R_w as z→∞ (d_A = r → R_w finite; O2's demoted annotation,
re-derived here) while P2/P3 have θ → 0 [KEYs thetaBAO_P1_floor_ell_over_Rw,
thetaBAO_P{2,3}_to_zero].

## 4. Radial BAO projection (proper-ruler REALIZATION tag)

With dℓ_p = A^(−1/2)dr and δ = φ = −½lnA, for ANY profile A(r) (exact, machine-checked):

**dz/dℓ_p = (1+z)·dδ/dℓ_p = −A′/(2A) = dδ/dr**
[KEYs radial_identity_dz_dlp_eq_opz_ddelta_dlp, radial_dz_dlp_closed_form,
radial_dz_dlp_eq_ddelta_dr] — redshift-per-proper-length equals depth-per-areal-radius.

Δz_BAO(z; ell) = ell·(−A′/2A)|_{r(z)}, per profile [KEYs DzBAO_P{1,2,3}_closed_form]:

- **Δz_BAO = (ell·n/2R_w)·(1+z)^(2/n)**  (P1) — GROWS with z  [KEY DzBAO_P1_increasing]
- **Δz_BAO = ell/2X**  (P2) — CONSTANT in z  [KEY DzBAO_P2_constant]
- **Δz_BAO = (ell·α/2X)·(1+z)^(−2/α)**  (P3) — DECAYS with z  [KEY DzBAO_P3_decreasing]

The z-TREND of the radial scale is the same trichotomy as c₂ (grow/flat/decay ↔ c₂ <, =, > 3/2)
— a second, independent-leg class discriminator. Low-z: Δz_BAO → ell/(2X_eff) for all three
[KEY DzBAO_lowz_Xeff_all] — consistent with the transverse leg (Alcock–Paczyński-like ratio
Δz/(z·θ) → 1 at z→0 for every profile; deviations at higher z carry the shape). Radial leg
remains ATTEMPT-ONLY at M3 per prereg §4 (thin-shell S/N risk).

## 5. Scale-translation table (P1 wall per O2 measure; c₀=1; re-derived, matches O2 CONSOLIDATED)

| O2 measure | wall location (P1, params R_w, n) | KEY |
|---|---|---|
| areal | R_w (definitional; THE fitted scale) | — |
| proper radial | **2R_w/(2−n)** for n<2; DIVERGENT n≥2 (n=2 log) | P1_proper_wall_2Rw_over_2minusn; witnesses n=½: 4R_w/3, n=1: 2R_w, n=2: ∞ |
| optical/Fermat (= c·travel-time) | **R_w/(1−n)** for n<1; DIVERGENT n≥1 (n=1 log) | P1_optical_wall_Rw_over_1minusn; witnesses n=½: 2R_w, n=1: ∞ |
| z, d_L, depth δ | divergent, all n (from §1: z,d_L→∞ at r→R_w) | P1_r_limit_Rw + inversion |
| d_A | R_w (finite; = areal) | thetaBAO_P1_floor_ell_over_Rw |

P2/P3: no finite-radius wall (r→∞); X is the e-fold/decay scale, not a wall location. Reporting
per prereg §5: every P1 range gets these translations, labeled per-measure; branch-conditional
overlays are labels only (no-pin standing).

## FOR THE BUILDERS (D2/D3): exact callables + numerically-safe forms

All z>0; params positive. Use log1p/expm1 to avoid catastrophic cancellation at low z (the data's
bulk). `L ≡ log1p(z) = ln(1+z)` once per vector.

- r(z): P1 `Rw*(-expm1(-(2.0/n)*L))` ; P2 `2.0*X*L` ; P3 `X*expm1((2.0/alpha)*L)`
- log d_L (fit mu in log space; NEVER exponentiate then log):
  `log_dL = 2.0*L + log(r_of_z)` with r>0 guaranteed for z>0; then
  `mu = (5.0/ln(10))*log_dL + const`. For P1 at tiny z, `log(r)` via
  `log(Rw) + log(-expm1(-(2.0/n)*L))` is safe (argument ~ (2/n)L, no cancellation).
- θ_BAO(z) = `ell/r_of_z` (guard: z>0 only; r(0)=0 is the observer, never evaluated).
- Δz_BAO(z): P1 `0.5*ell*(n/Rw)*exp((2.0/n)*L)` ; P2 `0.5*ell/X` ;
  P3 `0.5*ell*(alpha/X)*exp(-(2.0/alpha)*L)`.
- Sampling coordinates (§2 item 4): P1 `(Xeff, invn=1/n)` with `Rw = Xeff/invn` (= Xeff·n);
  P3 `(Xeff, invalpha)`; report in frozen params. Keep n, α > 0 open intervals; expect one-sided
  posteriors toward the P2 limit (invn, invalpha → 0).
- Wall translations (P1 reporting): proper `2*Rw/(2-n)` if n<2 else INF; optical `Rw/(1-n)` if
  n<1 else INF — label per-measure (§5).
- Machine cross-check to wire into D4: n=1 ⇒ d_L−Rw*z*(z+2) ≡ 0 (KEY P1_n1_banked_dL_z_zplus2).

**F-STEER note:** no formula above privileges n=1 (it appears only as the banked cross-check);
defaults in D2/D3 must not seed n=1 or α=2.

