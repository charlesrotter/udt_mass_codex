# MAP — P2: the native matter equation, 3-D and off-diagonal-aware

**Mode:** MAP (no compute). **Status:** for Charles's steer; the build is GATED on his go.
**NOT canon.** **Driver:** claude-opus-4-8[1m]. **Date:** 2026-06-19 (LATE+).
Parent: EVERYTHING_ON_SOLVER_BUILD_MAP.md (P2 = §III). Carries the P1 verifier's caveats
(p1_VERIFIER.md). Frame stated whole + premise ledger so a smuggled physics-choice is caught cheap.

---

## 0. WHAT P2 IS — and is NOT

It IS: making the **matter equation** (the Θ profile's Euler-Lagrange equation) (a) live in full
3-D — Θ(r,θ,ψ), not just Θ(r) — and (b) **vary on the FULL metric including the off-diagonals**
P1 turned on (today it is blind to them). Then re-take the P1 shear observation cleanly.

It is NOT physics yet, and NOT a catalog hunt. It closes the gap P1 left and removes a freeze; the
observing comes after. It does NOT turn on a(φ) (P3) or time (P4) — those stay frozen this phase.

The honest one-liner: P1 let the **geometry** see the off-diagonals; P2 lets the **matter** see
them too, so the two sectors are finally consistent. Until P2, "static matter sources no shear"
(the P1 observation) is only half-tested — the matter couldn't feel the shear it was supposedly
not sourcing.

## I. THE TARGET

- The native **S² area-form (π₂) carrier**, profile **Θ(r,θ,ψ) FREE**, native **L2+L4**, with the
  matter EL derived by varying the action on the **full off-diagonal-aware metric**.
- The ONLY core condition stays the **native regularity node** (sin Θ(0)=0, value free) — **no
  Skyrme BC** (#61). a=−1 baseline (P3), time row zeroed (P4).
- **Re-take the observation** P1 left scoped: with the matter EL now seeing the off-diagonals, does
  static native matter source spatial shear (e_rp, e_tp), and is the e_rt ~1.3e-2 a grid artifact
  (→0 at higher Nth) or a genuine geometric response? (The P1 verifier explicitly deferred this.)

## II. FOUNDATION (what we build ON — already mostly clean)

- `whole_metric_3d_matter.py` — general 4×4 L2+L4 Hilbert stress for a unit field on a full metric,
  all off-diagonal momentum/shear pieces, exact (verified 4.2e-17). The general stress already
  exists; P2 wires the **matter EL** (the variation w.r.t. Θ) to be consistent with it on the full
  metric.
- `coupled_tl_s2_derive*.py` — sympy-exact S² carrier stress + EL + the node core condition (1-D
  radial; the symbolic shape to generalize).
- `gen_matter_el_3d.py` / `matter_el_3d` — 3-D matter EL by direct variation; carries Θ(...)
  dependence; today varied on the DIAGONAL metric (the P1 gap to close).
- `p1_residual_general_einstein.py` — the P1 general-Einstein residual (the off-diagonals it now
  carries are what the matter EL must couple to).
- `divT_excised.py` — the divT identity gate (∇·T=0 ⇔ matter EOM): the correctness check for the EL.

## III. THE BUILD SUB-STEPS (incremental; validate each)

- **P2a — 3-D native S² EL.** Generalize the Θ-free node EL from Θ(r) to Θ(r,θ,ψ) on the S² carrier.
  Validate: round/axisym limit recovers the P1/P0 soliton; node core only (grep no m·π).
- **P2b — couple the EL to the full metric.** Make the matter EL vary on the off-diagonal-aware
  metric (close the P1 gap). Validate: **the divT identity** (∇·T=0 ⇔ EOM) holds to floor on a
  non-diagonal test config — the decisive correctness gate for matter–metric consistency.
- **P2c — re-take the observation (OBSERVE, not target).** Static native matter, EL now seeing the
  off-diagonals: do e_rp,e_tp stay ~0? does e_rt converge with Nth (artifact) or persist (genuine)?
  Report what is there. NOTE the prior expectation (Birkhoff/#62-64 + P1): static matter likely
  sources little/no shear — but P1 couldn't trust this because the matter was blind. Do NOT
  manufacture; "they stay zero" is a clean, reportable result.

## IV. PREMISE LEDGER — every choice that could smuggle physics

| # | Choice | Default | CHOSE / DERIVED | Risk / guard |
|---|---|---|---|---|
| **P2-carrier** | **S² 3-vector**, unit hedgehog n=x/r | **RESOLVED = S² (DEMANDS-level, blind-verified 2026-06-19; s2_s3_identity_results.md + _VERIFIER.md)** | *** Settled before P2 (was the one to watch). *** The native L2+L4 action sources NO stable 4th component (n_4=0 is the only interior critical point; the unstable direction destroys the charge → vacuum, not an S³ soliton); S³ is never native, always imported (Skyrme BC #61). The cos θ "texture" was an ARTIFACT of a NON-UNIT embedding (|n|²≠1); the genuine unit hedgehog n=x/r is TEXTURE-FREE with T^t_t=T^r_r (B=1/A-consistent). => P2 builds the matter EL on the clean S² unit 3-vector; no S³ drift, no Skyrme BC. |
| P2-coreBC | Θ core BC in 3-D | regularity node sin Θ(0)=0, value free | DERIVED (node) — DANGER | Generalizing to (r,θ,ψ) must NOT re-import Θ(core)=m·π (#61). Grep-verify; node only. The deg-1 sector pins the π node (homotopy choice, not the m-ladder) — keep that distinction. |
| P2-varies-on | what the EL varies on | the FULL off-diagonal-aware metric | DERIVED-necessary (the whole point of P2) | If it stays diagonal, P2 did nothing. The divT gate (P2b) is the proof it genuinely couples. |
| P2-Nth | angular resolution | high enough that the off-diag observation is Nth-converged | category-A (tractability) | The P1 e_rt~1.3e-2 was Nth-ambiguous (verifier: flat vs Nth for resolved l=2). P2c MUST report the Nth-convergence of any off-diagonal it sees, or the observation is not trustworthy. |
| P2-freezes | a(φ), time | a=−1 (P3), time zeroed (P4) | declared scope | The only declared freezes; everything else live. State them. |
| P2-box | cell size | scan / R-independence verified | DERIVED-gate | Box-control standing scar. |
| P2-divT | the correctness gate | divT identity to floor | DERIVED-gate | P1 saw the gate read O(0.1) in r,θ from its OWN Nth=6 spectral inaccuracy — so P2 must use sufficient Nth for the gate itself, and not mistake gate-inaccuracy for a physics failure (or vice versa). |
| P2-observe | observe vs target | report what's there | binding | The re-taken shear observation is OBSERVE — do not seed or want a particular answer. |

The one that needs YOUR eye, Charles: **P2-carrier** — the S² angular texture / the open
S²-vs-S³ object-identity reconciliation. Everything else is engineering I'll own.

## V. THE COMPLETENESS BAR FOR P2 (when the re-taken observation may mean something)

The P2c shear observation is trustworthy only when: (1) the EL genuinely varies on the full metric
(divT identity holds to floor — P2b); (2) the round/axisym limit recovers P0/P1; (3) any off-diagonal
the matter sources is **Nth-converged** (resolves the P1 e_rt ambiguity); (4) cross-checked (≥2
grids / an independent EL derivation). Until then a non-zero shear is "not yet resolved," not a result.

## VI. RISKS (ranked)

1. **The S² carrier texture / object-identity (P2-carrier).** The genuine physics-content risk: the
   3-D S² embedding's tangential structure is where the open S²-vs-S³ reconciliation lives. Getting
   the EL right here is the load-bearing correctness item. (Not a numeric risk — a derivation risk.)
2. **Solver throughput.** The ~1700s/solve (broken-NVML no-cache allocator) makes 3-D Nth-convergence
   scans slow; P2c may be Nth-limited on the dense-Newton (P5's upgrade is the real fix). If so,
   report Nth-limited / INCONCLUSIVE on the shear, not a forced verdict.
3. **divT gate's own Nth inaccuracy** (seen in P1): must separate gate-inaccuracy from physics.
4. **Re-import of a BC** in the 3-D generalization (P2-coreBC). Grep + node-only.

## VII. SMUGGLED-FRAME CHECK

Is P2 a clean step? Yes — it closes a gap P1 explicitly left (removes the matter-EL freeze) and is
exactly the consistency the solver needs; the recon shows the general stress already exists, so it
is wiring + one careful derivation (the S² EL), not invention. The honest caveats: (a) infrastructure,
not an answer — the physics is downstream; (b) the S² texture / object-identity is a real open
reconciliation P2 surfaces (it does not by itself settle S² vs S³ — it derives the EL for the
canonical S² carrier and reports what that carrier does); (c) it does not touch a(φ) or time. None
blocks the step; all stay visible.

## VIII. WHAT IT TAKES (scoping)

- P2a (3-D S² EL) + P2b (couple to full metric + divT gate): assembly + one careful symbolic
  derivation on existing primitives — days, anchor-validated, tractable on the dense-Newton at
  small/moderate grids.
- P2c (re-take observation, Nth-converged): the Nth-convergence scan is the slow part on the current
  driver; may be Nth-limited until P5. Report honestly if so.
- Validation throughout against the divT identity + the P0/P1 round anchor.
