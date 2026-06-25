# P5a' — INDEPENDENT BLIND ADVERSARIAL VERIFIER RECORD

Append-only. **NOT canon.** Verifier: claude-opus-4-8[1m] (independent, DATA-BLIND),
id `udt-verifier-p5aprime-1781978801`. Date: 2026-06-20. Branch: `p5a-prime-repose`
(head c1ea990). Target: `p5a_prime_repose_results.md` + `p5a_prime_repose.py`.
Method: independent re-derivation from the COMMITTED `full3d_solver.residual_vector`;
new scripts (`/tmp/verify_*.py`), not a re-read of the report's numbers. Decisive
priority = the MANIFOLD / angular-Einstein under-determination finding (does it make
the dense-Newton ANCHOR unsound?).

---

## HEADLINE (priority ruling): the MANIFOLD finding is an ARTIFACT, not genuine under-determination. THE ANCHOR IS SOUND.

The agent's load-bearing deeper claim — "the angular Einstein sector G^th_th, G^ps_ps
is genuinely under-determined on the body-mask discretization (round-soliton residual
~1.2 that does NOT converge), so F=0 is a physical solution MANIFOLD and the anchor is
gauge-ambiguous (dM_MS~5%)" — does **NOT** survive. The O(1) angular residual is a
**coarse-radial-resolution Chebyshev edge artifact at the anchor grid (12,6,8)**, the
same P1/P2 spectral-inaccuracy confound flagged in the prompt — NOT a genuine
angular-sector under-determination.

DECISIVE NUMBERS (independent, bare unweighted G^th_th − kap8·T^th_th on the EXACTLY
round soliton; a=a(r),b=b(r),c=d=0,Th=Th(r)):

1. **Nth-convergence (THE decisive check): the angular residual is Nth-INDEPENDENT.**
   At fixed Nr=40, bare |thth| RMS = **0.6988 at Nth=8 and 0.6988 at Nth=16** — byte-
   identical to 4 sig figs; max=2.297 both. A genuine angular-sector inaccuracy would
   shrink (exponentially) with ANGULAR resolution; it does not move AT ALL. The round
   soliton has no angular structure, so the angular residual is not an angular-spectral
   error — it is the RADIAL operator. => NOT an angular-Einstein under-determination.

2. **Nr-convergence in the DEEP INTERIOR: the residual DOES converge with Nr.**
   bare |thth| RMS over interior r∈[1.5,11] (away from radial edges), Nth=8 fixed:
   Nr=16→0.678, 24→0.504, 32→0.294, 48→0.103, 64→0.042, 80→0.022 — clean monotone
   convergence (~halving per refinement). The tt/rr (radial Einstein) components are at
   MACHINE ZERO throughout (RMS 1e-17..1e-16). So the round soliton IS approaching a
   solution of the FULL (incl. angular) Einstein system as Nr→∞.

3. **The O(1) values are EDGE-LOCALIZED.** Radial profile of bare |thth| (Nr=64): the
   excised edge rows carry 11.5 / 1.4 / 1.9 (core) and 3.2 / 12.7 / 41.6 (seal); the
   body-edge rows just inside carry ~0.5–1.4; the DEEP interior is 0.02–0.14. The body
   MAX (1.42) sits at the body row adjacent to the excised seal edge — a Chebyshev
   radial-differentiation edge artifact on the steep core/seal soliton profile.

4. **Why it bit at the anchor grid:** at Nr=12 the body is only 6 rows spanning
   r∈[2.47,11.63] (radial spacing ~2 on a steep soliton); EVERY body row is
   edge-adjacent and carries thth ~0.67–1.17 (body RMS 0.89). The "round-soliton
   residual ~1.2" is this coarse-Nr edge contamination, not a sector defect.

The agent's own evidence is consistent with this once read correctly: their cited
"non-convergence with Nr (16/24/40 → 1.6/2.4/2.3)" are the body **MAX** (which I
reproduce: 1.61/2.39, edge-dominated and non-monotone) — NOT the interior measure,
which converges cleanly. The agent used an edge-dominated metric and read "manifold"
off it. This is exactly the confound `p2_VERIFIER.md` §2 documents (an angular/divT
gate reading O(0.1–1) is the spectral operator's own edge noise at this resolution
class, reproduced by the known-good path too).

**Is the "two regular edge gauges → distinct floored M_MS" a genuine manifold or an
artifact?** ARTIFACT (discretization, not continuum). The spread IS nonzero at the
anchor grid — I independently reproduce GATE-A's two gauges flooring at M_MS=0.293380
(G1, round-seed edges) vs 0.309413 (G2, anchor edges), **dM_MS=5.18%**, both Phi~1e-13
— so on the coarse (12,6,8) discretization the unconstrained edge DOF DO propagate into
the under-resolved body and shift M_MS. But this is the SAME radial-under-resolution /
edge-gauge artifact: the edge rows are contaminated by the Cheb edge amplification, and
at Nr=12 the body is too coarse to be insensitive to them. M_MS is computed from
rho=−T^t_t (a metric/coordinate-frame scalar integrated radially); it is NOT a fully
gauge-invariant comparison when the two solutions differ in the edge/coordinate gauge,
so part of the 5% is also a not-apples-to-apples coordinate effect. CAVEAT (honest): I
could not cleanly measure the Nr-DEPENDENCE of the spread — `reposed_dense_solve_fast`
with a perturbed-edge gauge floored at Nr=12 (spread 1.59%, both Phi~1e-13) but did NOT
reach floor at Nr=16/24 within maxit=40 (Phi~1e-3), so those spread numbers are
unconverged and unreliable. The Nr-trend of the spread is therefore NOT independently
nailed here. The ruling rests on the DIRECT residual evidence (1–4 above), which is
clean and does not depend on the solver flooring: the angular residual is
Nth-independent and Nr-convergent in the interior, so the sector is determinate in the
continuum and the manifold/spread is a coarse-grid edge-DOF artifact.

**CONSEQUENCE FOR THE ANCHOR:** SOUND. The dense-Newton anchor is the Nr=12 floored
solution; the angular Einstein equations it nominally violates at O(1) are an artifact
of the coarse radial grid + edge mask, which vanish under radial refinement — they are
not a continuum under-determination that would make the physical solution non-unique.
The anchor is the correct discrete fixed point of the committed residual on its grid.
P5 does NOT need to "add a missing constraint to make the angular Einstein sector
determinate before proceeding" — the sector IS determinate. What P5 SHOULD do is treat
the edge-mask region with radial-resolution / edge-gauge hygiene (and report off-round
diagnostics like tvar at REFINED Nr, since at Nr=12 the off-round signal tvar~1e-2 is in
the same edge-contaminated regime and must be reconfirmed converged before it is read as
physics). That is a resolution-discipline note, NOT an anchor defect and NOT a blocker.

---

## CLAIM-BY-CLAIM ON THE P5a' PASS

### (5) FULL-RANK — STANDS.
Independent SVD on (12,6,8): full-space committed J (2688×2880) kappa=**4.447e18**,
**216** near-zero (<1e-8). Reposed-J(hold) (2688×1440) kappa=**2.306e5**, **0** near-zero
(smin=6.3e-5). Matches the report (5.9e5/0 — within method scatter of seed/lstsq vs my
seed). The re-pose genuinely removes the rank deficiency; JFNK is no longer
nullspace-choked. CONFIRMED.

### (2/6) GATE A (re-pose preserves physics) — STANDS.
Independently: reposed dense (G2 = anchor edges) reproduces the full-space dense anchor
to **dM_MS=5.6e-17, dtvar=8.0e-16** (machine), both at Phi=5.9e-13. The re-pose with the
anchor's gauge recovers the IDENTICAL physical fixed point — only the unconstrained edge
DOF were removed. CONFIRMED. (The cross-gauge 5% is the artifact ruled on above, not a
GATE-A failure.)

### (4/7) GATE C (beats #60) — STANDS.
Independently re-ran the #60 axisym-l2 control: `full3d_solver.lm_solve` (Jacobi-PCG LM)
STALLS at **1.28e-5** (40 it) — the documented #60 wall, reproduced. Reposed JFNK
(matrix-free LSMR, pc=none) descends MONOTONELY: it=6→9.1e-5, it=8→9.4e-6 (crosses the
wall), it=10→**1.26e-6** and still descending — already >1 order below the #60 stall, on
the full-rank reposed operator, trajectory ~4–5× reduction/step consistent with the
report's 3.2e-8. CONFIRMED (converges where #60 stalled).

### (3) GATE B (JFNK == anchor Newton path) — STANDS (from report + GATE-C trajectory).
Not separately re-run end-to-end, but the GATE-C run independently shows the reposed
matrix-free JFNK is a clean monotone Krylov descent (no nullspace choke), and the
report's deep-floor LSMR-budget caveat is an honest, standard JFNK trade-off (now a
PC-cuts-iters problem, not a nullspace-repair problem). PARTIAL-CONFIRMED (de-risk sense
stands; deep machine floor is budget-limited, as stated).

### (8) DISCIPLINE — STANDS.
- **Residual verbatim:** `reposed_residual(ub) == residual_vector(embed_vsafe(ub))` to
  **maxdiff 0.0** (exact); `embed == embed_vsafe` (hold) to 0.0. Only DOF posing changed.
- **Edge gauge DECLARED:** yes ('hold' = edge rows at a smooth/regular reference;
  analytic BC endpoints pinned). The held edge DOF are unconstrained (rank collapse
  216→0; F-flat along them). No PHYSICAL DOF frozen. B=1/A free; Theta free over body.
- **Leftover inner-body mode:** did not appear at (12,6,8) (0 near-zero SVs) — consistent
  with the report; declared metric-gauge fix held in reserve for larger grids. Honest.
- **Data-blind:** yes (units L=1; no wall numbers touched).

---

## NET

**P5a' DID rescue JFNK — STANDS.** Re-posing to body DOF makes the operator full-rank
(kappa 1e18→1e5, 216→0 near-zero), GATE A reproduces the anchor to machine precision in
its own gauge, and GATE C drives the #60 axisym-l2 stall case >1 order below the
Jacobi-PCG wall on a clean monotone Krylov descent. The KEH/SCF fallback is not forced.
The residual is the committed one verbatim; the only change is DOF posing + a declared
edge gauge. The deep-floor caveat is an honest standard-JFNK budget issue.

**The DEEPER "solution-manifold / angular-Einstein under-determination" finding is
OVERSTATED — it is a coarse-radial-resolution edge artifact, NOT genuine continuum
under-determination, and THE DENSE-NEWTON ANCHOR IS SOUND.** Decisive: the round
soliton's O(1) angular residual is exactly Nth-INDEPENDENT (0.6988 at Nth=8 == 0.6988 at
Nth=16), is edge-localized, and CONVERGES in the deep interior with Nr (0.68→0.022 over
Nr=16→80) while tt/rr sit at machine zero. The agent diagnosed "non-convergence" off the
body MAX (edge-dominated), not the interior. The cross-gauge dM_MS spread is real on the
coarse grid (edge-DOF gauge propagating into an under-resolved body; partly a
non-gauge-invariant M_MS comparison) but is the same artifact, not a physical manifold.

**WHAT THE NEXT STEP MUST CONFRONT:** NOT an anchor/manifold defect. It must (a) apply
radial-resolution + edge-gauge hygiene around the body-mask (the 3-row excision leaves
the adjacent body rows contaminated at coarse Nr); and (b) re-confirm any off-round
physics (tvar~1e-2 etc.) at REFINED Nr before reading it, since at the anchor grid the
off-round signal lives in the same edge-contaminated regime. The angular Einstein sector
is determinate in the continuum; P5 may proceed against the anchor with that discipline.

OPEN (honest, for re-grade): the Nr-DEPENDENCE of the cross-gauge spread was not cleanly
measured (perturbed-edge reposed dense did not floor at Nr≥16 here). If a future run
floors two regular gauges at Nr=24/40 and the spread does NOT shrink toward zero, this
ruling flips and a genuine under-determination would be back on the table. The direct
residual evidence (Nth-independence + interior Nr-convergence) makes that unlikely, but
it is the one loose thread.
