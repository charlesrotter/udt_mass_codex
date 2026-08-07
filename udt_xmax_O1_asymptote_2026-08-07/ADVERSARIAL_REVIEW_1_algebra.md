# ADVERSARIAL REVIEW 1 (algebra) — independent recompute + escape hunt

Date 2026-08-07 | reviewer: fresh-session adversarial agent (same-session caveat travels) |
Method: fresh sympy/mpmath recompute; `derive_o1.py` NOT opened; ground read at source
(`udt_complete_pair_phi_orchestra_audit_2026-08-05/EXACT_DERIVATION.md`,
`udt_mixing_channel_lane_2026-08-06/DERIVATION_NOTES.md`). Scripts:
scratchpad `review1_part1.py`, `review1_part2.py`, `review1_part3.py` + inline chain runs
(all checks True; not committed). Contract: `PREREGISTRATION.md`.

## Claim 1 — THE COMPOSITE TRACE LAW: **CONFIRMED (exact)**

Re-derived from scratch in the 2x2 Lorentz block (eta = diag(-1,1); D_x = diag(e^-x, e^x);
L_w the rapidity-w boost; leg B = L_w D_q L_w^-1; composite M = B D_p; C = eta^-1 M^T eta M):

    tr(C)/2 = cosh^2(w) cosh(2(p+q)) - sinh^2(w) cosh(2(p-q))
            = cosh(2(p+q)) + 2 sinh^2(w) sinh(2p) sinh(2q)      [symbolic identity, exact]

exactly the notes' form; det C = 1 exact; leg B's own strain charpoly is w-free (twist does
not change leg depth). Same-sign legs (p,q > 0): correction >= 0, zero iff w = 0 (or a zero
leg) — SUPER-additive, equality iff collinear. Unbounded in twist: limit w -> oo is +oo with
sign factor (e^p-1)(e^p+1)(e^{2p}+1)(e^q-1)(e^q+1)(e^{2q}+1)e^{-2q} > 0 — algebraically
equal to the notes' (e^{4p}-1)(e^{2q}-e^{-2q}) > 0.

**Rational witness CONFIRMED exactly**: e^p = e^q = 2, cosh w = 5/4 (sinh w = 3/4, rational
boost): half-trace = 6137/512 > 257/32 = cosh(4 log 2); lambda_t = 6137/512 -
sqrt((6137/512)^2 - 1) < 1/16; the small-root eigenline has eta-norm < 0 (timelike), exact.

**Causal-label check (the attack the prompt ordered): the labeling CANNOT switch.** On the
same-sign family, h - 1 = 2 sinh^2(p+q) + 2 sinh^2(w) sinh(2p) sinh(2q) > 0 for all real w
(symbolic): eigenvalues stay real, distinct, positive over the ENTIRE twist range — no
collision, no complexification, so the causal label is constant in w; at w = 0 the small
root's eigenline is e_0 (timelike). For eta-self-adjoint 2x2 with distinct real eigenvalues
the two eigenlines are eta-orthogonal and neither can be null (a null line is its own
1D orthogonal complement), so exactly one is timelike. Grid check (30 points, w up to 15):
small-root eigenline eta-timelike everywhere. The claim does not break anywhere in w.

## Claim 2 — ADDITIVITY vs SUPER-ADDITIVITY: **CONFIRMED; NO real tension; exact partition stated**

The apparent tension dissolves: the notes' (a)-scope twist is a SPATIAL ROTATION (compact,
angle theta); the notes' (b)-twist is a relative BOOST (non-compact, rapidity w). Both
re-verified independently:
- Rotation twist, symbolic general theta (4x4): C_M e_0 = e^{-2(p+q)} e_0 EXACTLY — e_0 is
  a timelike eigenvector, so lambda_t factorizes: ADDITIVE for arbitrary theta. Different
  spatial axes (0-1 then 0-2 squeeze): composite strain diagonal, lambda_t = e^{-2(p+q)}: ADDITIVE.
- **Exact partition:** a chain is depth-ADDITIVE iff every leg and twist preserves the shared
  timelike eigenline e_0 — i.e. twists in the e_0-stabilizer (spatial O(3), compact).
  Any twist with a NON-COMPACT component (boost OR null rotation) moves the timelike
  eigenline and gives STRICT super-additivity for same-sign nonzero legs.
- **NEW TILE (gap in the probe's pocket hunt): parabolic (null-rotation) twist.** O(1,2)
  null rotation N_n (verified N^T eta N = eta): tr(C) grows as n^4 sinh(2p) sinh(2q) —
  super-additive and UNBOUNDED, like boost twist (samples: depth 1.10 -> 1.96 at n=2,
  4.88 at n=10 for p+q=1.1). The pocket claim survives the parabolic direction too.
- Pocket hunt, hardened: 1500 random VERIFIED-Lorentz twists (products of up to 5 random
  rotations/boosts, O(1,3), dps=40): ZERO sub-additive cases; rotation-only draws exactly
  additive (deviation ~1e-41). CAVEAT FINDING: an early buggy run with accidentally
  NON-Lorentz "twists" produced apparent sub-additive pockets — the Lorentz typing of the
  twist is load-bearing for the partition; a future completion admitting non-isometric frame
  changes would reopen the question. (Not a break: such twists are outside the banked type.)

## Claim 3 — Q1, the two-face boundary: **CONFIRMED (every piece)**

On diag(l, 1/l, s^2, s^2): e1, e2, e3 -> +oo as l -> 0+ (each carries 1/l); e4 = s^4 finite
nonzero. Along D_r = diag(1/r, r, 1, 1): det A = 1 and det C = 1 for all r; the r-entry
escapes to infinity; C/tr(C) -> diag(0,1,0,0), rank 1, with e_0 (eta-norm -1, eigenvector at
every r with eigenvalue 1/r^2 > 0) exactly the KERNEL of the limit — labeling survives to
the boundary, positivity fails only AT it. Reversal lambda_t(A^-1) = r^2 confirmed. The
reciprocal tie closes the singular face: lambda_t * lambda_r = 1 forces det C = s^4, bounded
away from 0, so lambda_t = 0 at finite entries is impossible on the lock — the only route is
escape to infinity (ideal face). The two-face reading is correct.

## Claim 4 — Q3 floor: **CONFIRMED exactly; STRENGTHENED**

Clock-screen block re-derived independently from A = [[1/r,0,mu],[0,r,0],[0,0,s]]:
T = 1/r^2 + s^2 - mu^2, d = s^2/r^2 (mu-free). Floor, both steps reduced to identities:
lam_min >= d/T  <=>  (T^2-2d)^2 - T^2(T^2-4d) = 4d^2 >= 0 (exact); d/T >= s^2/(1+r^2 s^2)
<=> mu^2 >= 0 (exact). So lambda_t >= s^2/(1+r^2 s^2) on the positive-real window: CONFIRMED.
STRONGER: d(lam_min)/dT < 0 on the window, and mu^2 only lowers T — so along the
mu-direction lam_min monotonically INCREASES toward sqrt(d) = s/r > 0: the mu-path moves
AWAY from the wall before elliptic domain loss. Elliptic-before-wall CONFIRMED (sample
r=2, s=1: onset mu = 1/2, exact). Minor addendum: past the elliptic window
(mu^2 >= 1/r^2 + s^2 + 2s/r) the exit is NEGATIVE-REAL spectrum, not elliptic — same
conclusion (extractor domain loss, never the wall).

## Claim 5 — the escape hunt, pushed harder: **(a) CONFIRMED total; (b) AMENDED (sharpening); (c) CONFIRMED**

(a) Opposite-sign law re-derived: cosh(2 delta) = cosh(2(p-q)) - 2 sinh^2(w) sinh(2p) sinh(2q)
(witness -1513/512 exact). The exit is REAL and TOTAL: h is linear DECREASING in sinh^2(w),
bounded ABOVE by cosh(2(p-q)) at fixed depths, and the wall is at h = +oo — so no near-exit
path sneaks wallward; the regular-stratum exit happens through h = 1, i.e. lambda = 1 =
DEPTH ZERO (the parabolic locus), the point maximally FAR from the wall. Once elliptic,
monotonicity forbids return. No sneak exists on this family.

(b) **INFINITE SUMMABLE-DEPTH CHAINS REACH THE WALL IN THE LIMIT — the "finite chain"
hypothesis is doing more work than the notes state.** Construction (direct matrix product,
dps=400, no recursion trusted): legs A_k = L(u_k) D(eps_k) L(-u_k), leg depths
eps_k = 2^-k (TOTAL depth < 1), twists u_k = k^2. Every truncation is regular with the
small root's eigenline eta-timelike; det C = 1 exactly (multiplicativity). Composite:
lambda_t ~ 4e-3 (n=2), 3.6e-7 (n=3), 1.8e-20 (n=5), 4e-84 (n=10). lambda_t -> 0 though the
summed leg depth is bounded by 1. NON-ATTAINMENT by finite chains is intact (each truncation
lambda_t > 0, matrices finite-invertible; the infinite product has no finite-matrix limit —
entries diverge, consistent with Q1's ideal face). But the SR disanalogy is sharper than the
notes say: in SR a summable-rapidity infinite chain stays strictly inside v < c; here
summable depth gives NO such protection — finiteness of CHAIN LENGTH, not of total depth, is
the load-bearing hypothesis. The theorem statement should carry this explicitly.

(c) Parabolic/null legs: a parabolic LORENTZ leg N has C_N = I — depth 0, acts purely as a
twist (n^4 amplification, see claim 2); non-Lorentz unipotent (mu-type) legs are floored
(claim 4); genuinely singular/null arrows (det = 0) attain the wall trivially but are
excluded by the banked INVERTIBLE typing — the notes' scope edge (s4/S4) is honest and
correctly placed. No escape found within the banked groupoid.

## VERDICT

Per-claim: (1) trace law CONFIRMED exact incl. labeling stability; (2) partition CONFIRMED —
no tension (rotation-vs-boost twist), exact partition = e_0-stabilizer (compact) additive /
non-compact twist super-additive, parabolic tile added; (3) Q1 CONFIRMED whole; (4) Q3 floor
CONFIRMED + monotonicity strengthening; (5a) exit total CONFIRMED, (5b) AMENDED — explicit
infinite-chain caveat owed (summable-depth chains accumulate to the wall; finite LENGTH is
the load-bearing hypothesis; SR analogy weaker than stated), (5c) CONFIRMED.

**OVERALL: O1-CONDITIONAL SUSTAINED, with amendments** — no load-bearing claim broken; three
additions owed to the notes before banking: (i) the infinite-chain/summable-depth caveat in
the theorem's scope sentence; (ii) the parabolic-twist n^4 law completing the pocket hunt;
(iii) Q3 monotonicity + negative-real far-exit note. The Lorentz-typing-of-twists dependence
(claim 2 caveat) should travel as a named scope edge alongside the singular-arrow edge.
Same-session caveat: this review is same-session relative to the probe; the external bar travels.
