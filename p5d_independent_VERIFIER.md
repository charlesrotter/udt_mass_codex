# P5d — INDEPENDENT Blind Adversarial Verifier Pass (second, independent of build agent)

**Verifier agent:** claude-opus-4-8[1m] (INDEPENDENT blind verifier, distinct from the build
agent and from the build agent's own `p5d_VERIFIER.md`). **Date:** 2026-06-20.
**Branch:** `p5d-timelive`. **Target:** `p5d_timelive.py` + `p5d_timelive_results.md`.
**Mandate:** TOP PRIORITY — decide whether M=0 (the d_t^2 inertia at machine floor) is a
genuine round-specific BIRKHOFF cancellation or a WIRING BUG (the d_t^2 content not reaching
M). Apply P4's off-round-survival template (the test the build agent DEFERRED). DATA-BLIND.
Anti-hang held (Nr<=16, single sequential process per call, no background poll; each call
5-15 s, all <6 min). Probe scripts were scratch in the repo dir, deleted after running
(NOT committed). All numbers below are mine.

---

## HEADLINE

**(a) THE DECISIVE TEST — GENUINE BIRKHOFF, CONFIRMS P5d.** The d_t^2 inertia operator M IS
wired and DOES reach the residual rows P5d uses; it cancels round and SURVIVES off-round.

Per-row K/C/M of P5d's OWN residual rows (Gtt, Grr, EL, Gtr), the same `time_rows` /
`assemble_KCM` pipeline, with a non-round c1 theta-warp amplitude added (the P4 template):

| row | ROUND ||M|| | OFF-ROUND (c1=0.05) ||M|| | round ||M||/||K|| | off-round ||M||/||K|| |
|---|---|---|---|---|
| **Gtt** | 1.62e-9 (floor) | **8.46e-2** | 2.3e-9 | **0.120** |
| **Grr** | 1.55e-9 (floor) | **6.09e-2** | 2.2e-9 | **0.087** |
| EL  | 0 | 0 | — | — |
| Gtr | 0 (this is the C/omega^1 channel, ||C||=0.61) | 0 | — | — |

The omega^2 (d_t^2) inertia in the Gtt and Grr rows jumps from **machine floor (~1e-9) round
to ~0.06–0.08 off-round** — a factor of ~5e7. The d_t^2 content is genuinely present and
WIRED INTO THE RESIDUAL ROWS M is built from; it simply CANCELS IDENTICALLY on the round
diagonal (Birkhoff). This is exactly P4's verifier template (turn on a non-round amplitude ->
a diagonal that cancelled round now SURVIVES), applied to P5d's actual M assembly. **The
"never-reached-M / wiring-bug" branch is ruled out.**

Corroborating diagonal-Einstein probe (live-time delta in each diagonal G^mu_nu, P4 style):
- ROUND: omega^2 content in G^t_t = 2.8e-14 (floor) BUT in **G^th_th = G^ps_ps = 3.5e-2
  (NONZERO even round)** — the d_t^2 a/b amplitude already produces surviving inertia in the
  ANGULAR diagonals; only the G^t_t diagonal Birkhoff-cancels. (P5d's rows happen to use
  G^t_t/G^r_r, which is why P5d reads ~0 round.)
- OFF-ROUND (c1!=0): G^t_t omega^2 content = 1.2e-3 (was 1e-14 round) and G^ps_ps = 6.9e-2 —
  the cancelling diagonal now carries inertia. Matches P4's c1!=0 -> surviving-diagonal result.

So the d_t^2 inertia is demonstrably computed, reaches dGamma[T]->Riemann, lands NONZERO in
G^th_th/G^ps_ps round and in G^t_t/G^r_r off-round, and the round G^t_t/G^r_r = floor is a
true cancellation. **NET on (a): GENUINE round-specific Birkhoff cancellation. CONFIRMS P5d.**

**(b) M ASSEMBLY + OMEGA-POWER SEPARATION — CORRECT.** Reproduced baseline (Nr=12,cell=14):
||K||=4.480, ||C||=0.6133, ||M||=2.242e-9 -> ||M||/||K||=5.0e-10 (matches doc bitwise to
shown digits). The omega-power separation is genuinely exact: K + wC - w^2 M reconstructs the
TRUE time_rows Jacobian at an INDEPENDENT omega (w=0.83, NOT one of the {0, +-0.5} fit
points) to **rel err 3.5e-10** (Nr=12) / 1.3e-10 (Nr=16). M is therefore genuinely the
omega^2 coefficient — not mislabeled, not an omega^1 leakage; the HB form is exactly
quadratic and the extraction is correct. Nr=16: ||M||=2.93e-9 (matches doc; not a single-grid
artifact). Containment reproduced: ||time-rows(x=0,omega=0)|| = 3.16e-10.

**(c) C / CONTAINMENT / INTERPRETATION — SOUND.** C is confined to the Gtr row (||C||=0.613,
||C||/||K||=0.137 round; K=0 and M=0 in that row) = the G^t_r momentum channel, linear in
omega, exactly P4c's "G^t_r linear in omega". Containment (omega->0 == static) holds. The
interpretation — "round ground state carries no classical oscillator on the diagonal channel;
the surviving live channel is the first-order G^t_r momentum flux; a diagonal d_t^2 inertia
lives only off-round (l>=2), deferred to P5e" — is CORRECT and now DIRECTLY DEMONSTRATED (the
inertia I exhibited off-round is precisely the P5e channel). The "reproduces #65 + reveals the
Birkhoff reason" claim is FAIR.

---

## NET VERDICT: P5d STANDS. GENUINE PHYSICS, NOT A WIRING ARTIFACT.

The round ground state carries **no classical oscillator** because the diagonal d_t^2 inertia
M Birkhoff-cancels on the round metric — and this is GENUINE physics, decisively shown by the
off-round survival test the build agent had deferred: the identical M-assembly rows go from
~1e-9 (round) to ~0.06–0.08 (off-round, c1!=0). The d_t^2 content is computed, wired, and
reaches M; it cancels round and survives off-round. M is correctly the omega^2 coefficient
(independent-omega reconstruction 3e-10). C is the linear G^t_r momentum channel. Containment
holds. R- and resolution-independent.

**What quantization / P5e correctly inherits:**
- The round channel has NO classical frequency ladder to quantize (M=0, K rank-deficient) —
  discreteness cannot come from a round classical resonance. Correct, and consistent with the
  catalog reframe.
- The classically-surviving structure is the first-order G^t_r momentum channel (odd in omega)
  + K's flat directions — that is what a quantization postulate acts on.
- **P5e (off-round l>=2) is where a NONZERO classical inertia M genuinely lives** — this
  verifier exhibited it explicitly (||M||/||K|| ~ 0.09–0.12 at c1=0.05). The off-round time-
  live solve is therefore not a formality; it is where a classical oscillator, if any, exists.
  Whether it TOWERS or box-controls is the open P5e question (NOT decided here; this pass only
  proved the inertia is nonzero off-round, confirming the wiring is genuine).

## DISCIPLINE / CAVEATS
- Observe-not-target HELD: no tower hunt; I only tested wiring genuineness, did not chase a
  frequency. Data-blind: only operator norms, omega-scalings, rel-errs — nothing banked.
- The build agent's own `p5d_VERIFIER.md` is NOT independent (same agent lineage). It echoes
  the doc and did NOT run the decisive off-round M-survival test (the load-bearing one) — it
  re-confirmed dtt_g nonzero and round-G^t_t cancel, but left "does M reach nonzero off-round"
  to assertion. THIS pass closes that gap by direct numerical exhibition. The build agent's
  sub-verifier should be treated as a self-check, not a second opinion; this is the second
  opinion.
- SCOPE (unchanged): verdict is for the ROUND ground state's diagonal channel in this stack.
  Off-round l>=2 dynamics (does the nonzero M produce a bound/box mode) is genuinely untested
  and is the real P5e question.
- Inherited (not re-litigated): P1 pole-stable hybrid small-shear conditioning at large
  omega/steep off-round shear (P4 caveat) — my off-round probe used small c1=0.05 (well inside
  the well-conditioned regime), so the qualitative round->off-round jump is robust; a large-
  amplitude / steep off-round quantitative M is a P5e accuracy task.
