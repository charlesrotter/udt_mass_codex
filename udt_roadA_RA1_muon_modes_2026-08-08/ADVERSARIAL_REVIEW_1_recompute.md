# ADVERSARIAL REVIEW 1 — RA1 full independent recompute + completeness attack

Date 2026-08-08 | reviewer: R1 (Fable, zero-context hostile) | package:
`udt_roadA_RA1_muon_modes_2026-08-08/` | contract: `PREREGISTRATION.md` (frozen)
Method: independent sympy recompute WRITTEN AND RUN BEFORE opening `derive_ra1.py`
(`review1_recompute.py` -> `review1_output.txt`, **32/32 True**), then line-by-line diff +
vacuous-key hunt. NOT committed.

## VERDICT: **SUSTAINED-AMENDED** (no claim killed; amendments are disclosure/completeness-level)

## 1. Independent recompute — everything load-bearing REPRODUCES

- **D1:** det g = -D/A, the inverse t-psi block (g^tpsi = h/D), the box assembly from the
  inverse metric, the SL form (p, w) = (sqrt(AD), r^2/sqrt(AD)), p*w = r^2, the dragging
  completion N = r^2(omega - m*Omega)^2 - m^2 D/r^2 with Omega = -h/r^2 — all exact
  (my keys detg..dragging_completion). The Liouville normal form and isometry verified with
  MY OWN multiplier derivation (s*sqrt(g), s = r/sqrt(AD)); my first run failed on MY
  factor-r bug, fixed, then exact. **x is exactly the mixing-deformed O2 measure: at h=0,
  dx = dr/A (optical) — machine-exact**, and at q=0 the wall rate is (R_w/h0)/sqrt(A)
  (proper-rate) — the identification is exact, not approximate.
- **D3 core:** sigma_eff = (n + min(n,2q))/2 confirmed against the FULL sqrt(A*D) exponent
  on 13 witnesses; x_wall finite iff sigma_eff < 1 (direct sympy integrals, log-marginal
  divergent); conjugation-term exponent (2s-1)/(1-s) > -2 identically. **Region map
  re-derived by my OWN classifier from scratch: 17/17 agreement**, including my extra
  probes (n=1/2 with q=-3; n=4 wedge/boundary/deep points). The MIXING-CREATED band is
  genuine: mu-off, 1<=n<2 gives sigma=n>=1, infinite optical x, U->0 => LP continuum
  (recomputed). **c_crit = -8*omega*m*R_w^2/(h0*(n-2)^2) recomputed EXACTLY from the full
  (unapproximated) integrand via sympy limits** — their K18b only checks the leading-order
  integrand; my full-expression check closes that gap. Centrifugal term subcritical on the
  critical line (only the dragging is critical).
- **THE CHIRAL WEDGE (attacked hardest):** WKB validity |U'|/|U|^{3/2} ~ d^{e/2-1} -> 0
  verified symbolically; attractive branch both-L2 => LC; repulsive branch action integral
  diverges => LP — all reproduced. **Essential-spectrum derivation (the demanded attack):
  in the counter-rotating channel U - lambda -> +infinity at the FINITE endpoint x_w for
  EVERY lambda (machine-checked) => that end is nonoscillatory for all lambda and
  contributes NO essential spectrum; the center end has U ~ (m^2 - 1/4)/x^2 >= 3/4/x^2
  (m != 0, required in the wedge anyway) — nonoscillatory for all lambda; finite interval,
  both ends nonoscillatory => sigma_ess EMPTY => the spectrum is GENUINELY purely discrete
  and bounded below — bound-state-like, NOT continuum-above-a-threshold.** The claim
  survives. One residual caveat (amendment A3 below): the pencil.
- **D4:** x_w <= x_opt direction verified (1/A^2 - r^2/(AD) = h^2/(A^2 D) >= 0, exact);
  R2 densification confirmed (x_w finite at h0 != 0, mu-off optical length divergent);
  Zeeman recomputed via the quadratic pencil solve: omega(m) - omega(-m) = -2m<h/r^2> =
  2m<Omega> exactly at fixed lambda (lambda even in m) — validity = first order in h0,
  nondegenerate mode, as stated. Weyl spacing pi/x_w is the standard finite-length count;
  the omega-linear pencil term is O(omega), subleading — spacing claim stands.
- **D2:** indicial a^2 - m^2 = 0, conjugation -1/4, U -> (m^2-1/4)/x^2 => LP for |m|>=1,
  marginal LC at m=0; literal-h0 variant p(0) = h0 (regular ODE point), centrifugal barrier
  removed (1/h0^2) — all reproduced. The fork's disclosure is adequate; D3 IS untouched
  (Weyl classification is endpoint-local; the center variant changes only the number of
  center data — variant (b) makes r=0 a regular endpoint needing a posited axis datum,
  which the doc says). Center nonoscillatory for all omega => no essential spectrum from it.
- **D5/D6:** mu-off limits (p -> Ar, w -> r/A, N, dx -> dr/A, sigma -> n) reproduced; LC
  iff n < 1 = O2 optical-finiteness — the coincidence is exact. **Counterexample hunt on
  "mixing never destroys a discrete region": 32-point grid over n < 1, q in {3..-50} — none
  found; and it is a theorem: sigma_eff <= n < 1 for all q, and q < 0 < 2-n keeps the
  dragging subcritical for n < 1 (no wedge can enter n < 1).** Claim survives.

## 2. Findings (the attack's yield — none fatal)

- **A1 (undisclosed vacuous key): RA1_K14 is a tautology** — `q/(1-sig)*(1-sig) - q == 0`
  identically for ALL q, sigma (machine-confirmed); it verifies nothing about dragging
  subcriticality. The 4 disclosed restatements (K5, K18a/c, K24) are honest; K14 is a fifth,
  undisclosed, and genuinely vacuous rather than restated. The UNDERLYING claim (q > 0 =>
  s-exponent q/(1-sigma) > 0, subcritical) is true and independently verified here — no
  claim change, but the key should be flagged/fixed.
- **A2 (completeness gap, measure-zero line): n = 2 with q < 0 is in NO stated region**
  (R2 is 1<=n<2; R4/R5/R6 are n>2; R2'/R3 cover n>=2 only for q>=0). Recomputed: there
  sigma_eff = 1+q < 1 and the dragging exponent e = -1 > -2 (subcritical) => LC, ladder-
  possible, mixing-created (mu-off n=2 is LP). The landed-outcome union should include it
  (it glues R2's band to R4/R5 continuously). Map amendment, no verdict change.
- **A3 (wedge caveat, half-disclosed):** the intrinsic-quantization statement is per FIXED
  (m, omega) coefficients (P-RA1-7 stamps this); since U depends on omega, "the mode set"
  is the root set {omega : omega^2 in spec(L_omega)} — discrete by analyticity of the
  eigenvalue branches unless a branch identically equals omega^2 (non-generic), a step the
  doc leaves implicit. Should be made explicit at consolidation; does not threaten the
  finding (sigma_ess empty holds for every omega in the channel).
- **A4 (minor):** K18b verifies only the LEADING-order integrand for s(u); the exact
  c_crit is nonetheless correct (my full-expression recompute). K22 machine-checks only the
  final linear solve, not the perturbation step itself (formula independently confirmed).
- **Slice scope (checked, adequate):** the equatorial-slice robustness argument for D3 is
  sound — LP/LC and the u-exponents are invariant under bounded-both-sides factor changes;
  the full-sphere (non-separable) problem is honestly scoped as NAMED INHERITANCE; the
  center indices are flagged slice-sensitive. The q<0 divergent edge is fully treated
  (R4/R5/R6), not dropped. n <= 0 is outside the wall-asymptote class (O1), implicitly
  scoped.

## 3. Files

`review1_recompute.py` (independent, written before opening `derive_ra1.py`; final run
32/32 True in `review1_output.txt`; two of my own first-run bugs — a Liouville multiplier
factor r and positivity declarations — found and fixed on MY side, plus the gap-line/K14/
densification probes run separately and reported above).

**VERDICT: SUSTAINED-AMENDED** — the classification map, the mixing-created band, the
chiral wedge (including genuine intrinsic discreteness in the counter-rotating channel),
c_crit, the Zeeman splitting, the cavity-shortening inequality, and the mu-off coincidence
all reproduce exactly under hostile independent recompute. Amendments owed at
consolidation: fix/flag K14 (A1), add the n=2, q<0 line to the LC union (A2), make the
pencil-analyticity step explicit in the wedge's intrinsic-discreteness claim (A3).

— R1, 2026-08-08.
