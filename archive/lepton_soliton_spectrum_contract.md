# PRE-REGISTRATION — Lepton soliton spectrum / scale-free mass ratios

Falsification contract. Committed 2026-06-14 BEFORE the derivation runs
(Self-Hardening: pre-register before testing; no retuning after). Authorized
by Charles 2026-06-14 ("go for it"); candidate map + tolerance LOCKED by
Charles (P primary; W reported; <=1% per ratio).

## Frozen model (no changes after this commit)

- Lagrangian: the settled NATIVE angular Lagrangian L = L2 + L4,
  L2 = -(xi/2) g^{mn} d_m n_a d_n n_a, L4 = -(kappa/4)|omega_H1 current|^2_g
  (the native winding-current / Skyrme term, CANON C-2026-06-14-1 refinement;
  blind-verified a1f2213b6410a6f35). Unit 3-vector n, |n|=1, target S^2.
- Background: the finite inside-out matter cell; metric
  ds^2 = -e^{-2phi}c^2 dt^2 + e^{2phi}dr^2 + r^2 dOmega^2.
- BCs (native, from recon): CORE regular turning point (depth-parametrized);
  SEAL same-minus mirror fold (Neumann for the sigma-even static shape);
  self-adjoint measure r^2 sin theta BARE.
- ONE dimensionful scale: kappa/xi (sets the soliton size sqrt(kappa/xi)).
  It CANCELS in all mass RATIOS. No second tunable dial permitted.

## The families (candidates)

- (P) PRIMARY — radial-excitation tower. The charge-1 (degree-1) hedgehog
  soliton Theta(r) solved as a nonlinear EIGENPROBLEM on the cell, ground
  state (0 nodes) + radial excitations (1 node, 2 nodes). Masses E_0<E_1<E_2,
  SAME angular charge (N=3, q=1/3).
- (W) SECONDARY (reported, NOT substituted) — winding tower, degree B=1,2,3
  hedgehogs. Masses M_1<M_2<M_3.

## Locked candidate -> particle map (Charles, no post-hoc reordering)

- (P) radial modes n = 0, 1, 2 in INCREASING mass  ->  (e, mu, tau).
- (W) reported alongside; a (W) hit is EXPLORATORY (look-elsewhere debited),
  never substituted for (P) if (P) misses.

## Observables (scale-free; kappa/xi cancels)

- R1 = E_1/E_0  (predicts m_mu/m_e)
- R2 = E_2/E_0  (predicts m_tau/m_e)
- Koide  Q = (E_0+E_1+E_2) / (sqrt E_0 + sqrt E_1 + sqrt E_2)^2
- Also REPORT: the level-spacing pattern (O(1) vs exponential) — informative,
  not itself a pass/fail.

## Targets (PASS/FAIL only; never evidence). DATA-BLIND: the derivation does
## NOT load or compute toward these; revealed/compared only AFTER + verifier.

- T1: R1 within <=1% of m_mu/m_e (the empirical lepton ratio, contract 26fc757).
- T2: R2 within <=1% of m_tau/m_e (contract 26fc757).
- T3 (Koide): Q within <=1% of 2/3 = 2q (q=1/3). PASS/FAIL, never evidence.

## Honest prior (stated before the run, not a target)

The empirical lepton ratios are HUGE (m_mu/m_e ~ 2e2, m_tau/m_e ~ 3e3); a
generic overtone tower gives O(1) ratios, so T1/T2 PASS requires the level
spacing to be EXPONENTIAL (the external-input exponential-hierarchy claim) —
a strong test the overtone picture may FAIL. T3 (Koide) is an O(1) relation
among roots and is the cleaner test for an O(1) tower. Both are pre-registered;
a FAIL on T1/T2 with the spacing reported is a first-class result.

## Look-elsewhere accounting (pre-set)

Combinations tried = {family P (primary), family W (secondary)}; the map is
pre-locked (increasing mass -> e,mu,tau), NO reordering. A PASS is registered
ONLY for (P) on the locked map; (W) results and any spacing coincidences are
debited as exploratory. Any near-miss requiring a reorder or a second scale =
FAIL.

## Protocol

derive DATA-BLIND -> blind adversarial verifier -> THEN reveal & compare to
T1/T2/T3 -> record PASS/FAIL with premises. Contract 26fc757 untouched during
the derivation.
