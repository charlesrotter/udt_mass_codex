# STEP 0 — THE BRIDGE / SCALE-ANCHOR CHECK

Dynamic-Phi / Universal-MS-Scale synthesis (DYNAMIC_SCALE_SYNTHESIS.md).
Run 2026-06-14. Exploratory, dimensional + geometric. mpmath dps=50.
Scripts: `step0_bridge.py`; log `/tmp/step0.log`.

**Question.** Does anchoring the absolute scale by the universe's total
Misner-Sharp mass M produce a PARTICLE-sized cavity, and WHICH ratio does the
cavity geometry use to bridge cosmic -> particle?

**INPUT vs DERIVED (declared up front).**
- INPUT: M_universe (via the CMB radius R), and the probe rest masses m.
- DERIVED: every ratio, implied depth, implied scale, and the closed-form
  bridge factor below.
- DATA-BLIND: the lepton wall ratios (contract 26fc757) are never used; no
  tuning toward any spectrum. No Dirac import (resonator template banked-dead).

---

## 1. Cosmic anchor (corpus-exact)

| quantity | value | provenance |
|---|---|---|
| R = r_CMB | 9.164 Gpc = 2.8277e26 m | udt_canonical_geometry.md:1840; macro_sector_fork_resolution.md:67 |
| phi_CMB (dilation DEPTH) | ln(1101) = 7.003974 | udt_canonical_geometry.md:1471; CANON C-2026-06-10-2 |
| z_CMB | 1100 (1+z = 1101) | udt_canonical_geometry.md:1467 (T_CMB=2.725 K) |
| M_universe = c^2 R/(2G) | **1.9039e53 kg = 1.138e80 m_proton** | horizon condition; DYNAMIC_SCALE_SYNTHESIS.md:44 |

M_universe is INPUT (the horizon/Misner-Sharp condition `c^2 = 2GM/R` evaluated
at the CMB boundary in the deep-well limit, udt_canonical_geometry.md:1415-1425).
The ~1.1e80 proton count is the textbook observable-universe value — anchor sane.

---

## 2. Per-probe table

| probe | m (kg) | lambda_C = hbar/(mc) [m] | r_charge [m] | M_u/m | R/lambda_C | sqrt(M_u/m) |
|---|---|---|---|---|---|---|
| electron | 9.109e-31 | 3.862e-13 | -- | 2.09e83 | 7.32e38 | 4.57e41 |
| muon | 1.884e-28 | 1.868e-15 | -- | 1.01e81 | 1.51e41 | 3.18e40 |
| tau | 3.168e-27 | 1.111e-16 | -- | 6.01e79 | 2.55e42 | 7.75e39 |
| pion (pi+) | 2.488e-28 | 1.414e-15 | 6.59e-16 | 7.65e80 | 2.00e41 | 2.77e40 |
| proton | 1.673e-27 | 2.103e-16 | 8.409e-16 | 1.14e80 | 1.35e42 | 1.07e40 |
| neutron | 1.675e-27 | 2.100e-16 | -- | 1.14e80 | 1.35e42 | 1.07e40 |
| Planck | 2.176e-8 | 1.616e-35 (=l_P) | -- | 8.75e60 | 1.75e61 | 2.96e30 |

Mass ratios ~1e80-1e83; size ratios ~1e38-1e42. The famous "10^80 mass /
10^40 size" split is reproduced.

---

## 3-4. Bridge analysis — which ratio, and the Dirac-square test

**The Dirac-square relation `M_u/m ~ (R/lambda_C)^2` is APPROXIMATE, not exact.**
In logs:

| probe | ln(M_u/m) | 2 ln(R/lambda_C) | ratio |
|---|---|---|---|
| electron | 191.85 | 178.98 | 1.072 |
| muon | 186.52 | 189.64 | 0.984 |
| pion | 186.24 | 190.20 | 0.979 |
| proton | 184.34 | 194.01 | 0.950 |

The ratio is ~1 to 5-7%, but it DRIFTS systematically with the probe (1.07 ->
0.95 from electron to proton). That drift is the tell: it is exactly the
residual mass-dependence. Algebraically (sympy, exact):

```
(R/lambda_C)^2 / (M_u/m)  =  (R m c/hbar)^2 / (R c^2/(2 G m))  =  2 G R m^3 / hbar^2 * (1/c^?)
```
— it carries `m^3`, so it is probe-dependent (column ranges 2.6e-6 for the
electron to 1.6e4 for the proton). **There is no exact universal Dirac square
across probes.** The clean square holds only for the WHOLE mass itself:
`R/lambda_C(M) = 2GM/c^2 / (hbar/Mc) = 2 (M/M_planck)^2` — the universe's size
ratio is its own mass ratio squared, mediated by the **Planck mass**, not by
any particle.

**The dilation depth cannot bridge alone (demonstrated).** A dilation factor
maps scales by at most `e^{|phi|}`. The matter-scale depth is phi0 ~ -0.80
(`e^{-2phi0} ~ 4.95 ~ 5`, the banked hadronic value) — a factor of ~5. To
bridge the SIZE ratio ~1e40 one needs `|phi| = ln(1e40) ~ 90`; to bridge the
MASS ratio ~1e80, `|phi| ~ 185`. The available depth (~0.8) is short by a
factor of ~100 in the exponent. **So the ~10^40 cannot come from phi.** It has
to come from the absolute SCALE RATIO itself — i.e. from the free units that M
is supposed to set. The dilation depth shapes the cavity locally (factor ~5);
it does not carry the cosmic->particle separation.

---

## 5. THE MAKE-OR-BREAK: is the bridge UNIVERSAL? — **NO.**

A single M-anchored absolute length, times a universal geometric factor, would
place ALL probes at their correct sizes iff the factor `R/lambda_C` were the
same for every probe. It is not (lambda_C ~ 1/m differs per probe). The only
candidate universal bridge — `R/lambda_C = K * sqrt(M_u/m)` with K constant —
**fails by a closed-form proof (sympy):**

```
(R/lambda_C) / sqrt(M_u/m)  =  sqrt(2) * sqrt(G) * sqrt(R) * m^(3/2) / hbar
```

This carries **m^(3/2)** — it is NOT probe-independent. Numerically the "constant"
ranges over 0.0016 (electron), 4.76 (muon), 7.23 (pion), 126 (proton), 328 (tau):
not a constant at all. **=> There is no single M_universe-anchored scale + one
universal geometric factor that lands every particle. Each particle's size still
requires its own mass m as an independent input.**

What M alone fixes is exactly ONE length: the horizon `R = 2GM/c^2` — which
hands back the COSMIC size (size ratio 1). The only other M-anchored lengths from
{c, G, M, hbar} are `hbar/(Mc)` (absurdly sub-Planckian) and their geometric
mean `sqrt(R · hbar/(Mc)) = sqrt(2)·l_Planck = 2.286e-35 m` — the Planck length,
**probe-independent and 20+ orders too small for any particle.** None of these is
a particle size. To reach a particle you must re-insert the particle mass m.

**Make-or-break verdict: the bridge is NOT universal from M alone. M sets the
cosmic scale (and, with hbar, the Planck scale); it does NOT, by itself, place
the particle. A second input — the particle's own mass, or whatever the
cavity+angular structure derives in its place — is required.**

---

## 6. Native legacy check (r_*~6.99, cos(pi/5), C=4pi^2 m_e r_*) — **NO (does not re-emerge).**

- Legacy `r_* = 6.9875` is a DIMENSIONLESS Dirac cavity boundary (banked-dead
  template), NOT a length or a depth. `cos(pi/5) = 0.809017` is the legacy
  central depth `|phi0|`. `C = 4pi^2 m_e r_* = 140.96 MeV` is a calibration in
  which **m_e is the SOLE dimensionful INPUT** — i.e. the legacy already used a
  PARTICLE mass as the anchor, not M_universe.
- The corpus itself flags `r_*_micro = 6.9875 ~ ln(1101) = 7.004` as a **0.6%
  COINCIDENCE** (conflating them was error CR-07, udt_canonical_geometry.md:1844).
  Our bridge confirms they are different objects: r_* dimensionless cavity radius;
  phi_CMB a dilation depth.
- The cosmic<->particle bridge LOGS land at `ln(R/lambda_C) ~ 89-98` and
  `ln(M_u/m) ~ 184-192` — i.e. the cosmic-to-particle SEPARATION, ~90-185, NOT
  the matter-cell depth ~7 or ~0.809. Nothing in the M-anchored scaling produces
  6.99 or cos(pi/5) natively.
- One honest-but-not-load-bearing near-coincidence: `ln(R/lambda_C)/13` lands
  6.88 (electron) to 7.51 (tau), straddling 7. The 13 is the legacy `mu_g = pi·mu/13`
  divisor (udt_canonical_geometry.md §12.8) — so dividing the size-ratio log by 13
  lands near 7 for several probes. This is NOT a derivation: it imports the legacy
  13, varies by probe, and is a TEST-B-failing soft hit. Recorded, not banked.

**Legacy re-emergence verdict: NO.** The legacy matter scale does not fall out of
the cosmic<->particle scaling. (Consistent: the legacy anchored on m_e, not M.)

---

## NET VERDICT — is M-as-universal-scale ALIVE?

**Scale-setting from M alone is NOT yet alive as a UNIVERSAL bridge.** M fixes
one length (the horizon R = cosmic size) and, with hbar, the Planck length —
both probe-independent and neither particle-sized. The cosmic->particle ~10^40
demonstrably **cannot** come from the dilation depth (off by ~100x in the
exponent) and **cannot** come from a single universal geometric factor on M (the
only candidate, `sqrt(M_u/m)`, carries m^(3/2), proven probe-dependent). So as a
plain geometric/dimensional bridge, **M alone is insufficient; a second input
(the particle mass, or a structure that derives it) is required.**

This does NOT kill the synthesis — it sharpens its real burden. The synthesis
(DYNAMIC_SCALE_SYNTHESIS.md "bridge crux") already states the bridge "cannot be a
plain dimensional formula; it must run THROUGH the cavity + angular structure."
STEP 0 CONFIRMS that necessity quantitatively and rules out the trivial routes:
the bridge is **not** the dilation depth, **not** an exact Dirac square across
probes, and **not** a single universal factor on M. If M is to set the particle
scale, the cavity+angular (ingredients 1+2) must supply a per-particle selector
that picks discrete sizes out of the continuum — and the ~10^40 must emerge as
the RATIO between the M-anchored ruler and the discretely-selected cavity, not as
any function of phi. The make-or-break for "M sets ONE universal scale" is
therefore: does the angular charge q=1/3 / N=3 selection produce a DISCRETE set
of cavity sizes whose ratio to R reproduces the ~10^40 without re-inserting m?
STEP 0 says nothing in the metric+dimensional content does this yet.

**Honest status: the absolute scale-setting is OPEN, leaning insufficient-as-stated.**
M is a genuine universal RULER (one cosmic length), but the cosmic->particle
bridge it must drive is missing — it lives in the (still-unbuilt) cavity+angular
selection, not in any dimensional or dilation-depth relation.

---

## What the blind verifier should attack

1. **The closed-form `m^(3/2)`** (the universality-killer). Re-derive
   `(R/lambda_C)/sqrt(M_u/m)` independently; confirm it is not probe-independent.
   This single algebraic fact carries the make-or-break verdict.
2. **The dilation-depth shortfall.** Check `ln(1e40) ~ 90` vs `|phi0| ~ 0.8`;
   confirm no plausible re-reading of the depth (e.g. cumulative over many cells,
   or e^{-2phi} stacking) closes a 100x exponent gap without invention.
3. **The `ln(R/lambda_C)/13 ~ 7` soft hit.** Attack as numerology: does it pass
   TEST-B (does it generalize, is it N-specific, does it survive without importing
   the legacy 13)? Predicted: fails. Make sure it is not silently load-bearing.
4. **Anchor sanity.** M_universe = c^2 R/(2G) = 1.90e53 kg / 1.14e80 protons —
   verify against R = 9.164 Gpc; confirm provenance is the corpus value, not a
   back-of-envelope.
5. **Frame guard.** Confirm no Dirac import crept in (the legacy r_*, C, cos(pi/5)
   are reported as legacy facts, never used to compute the bridge) and the lepton
   ratios were never touched.
