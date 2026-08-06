# Adversarial Review 2 — is COUPLING-TRANSMITS a real law route or illusory?

Reviewer: independent adversarial pass (zero-context re-derivation), 2026-08-06, branch grok.
Target: `MAP_AND_PREREG.md` + `DERIVATION_NOTES.md` (landed class COUPLING-TRANSMITS, with caveat).
Not committed. Small symbolic checks run independently (scratchpad `absorb.py`, `loopmix.py`).

## VERDICT: ENTANGLES-ONLY → downgrade to COUPLING-INERT-IN-EFFECT.
mu is native-PERMISSIBLE and genuinely non-gauge (gate real), but UNFORCED/unselected. The C2
closure obstruction does NOT constrain the depth profile phi; it is absorbed by the free mixing
field k. "COUPLING-TRANSMITS" is over-credited — it conflates "the coupling is real" (true, and is
exactly COUPLING-INERT's own premise) with "transmits a CONSTRAINT to phi" (false).

## ATTACK 1 (the crux) — does the obstruction CONSTRAIN phi, or RELATE it to free k?

The driver's O(t^2) loop obstruction was evaluated at FIXED k (the third slot values 1/3,1/2,-1/4)
and found phi-dependent (d/dphi != 0). I re-ran it with k SYMBOLIC (free), phi/R fixed generic:

- **o2 is homogeneous degree-2 in (kP,kQ,kR)** (confirmed: total degree 2, all monomials degree 2).
- **The quadratic form has eigenvalues {0, 0, 11.3}** — RANK 1, positive-semidefinite. So
  `o2 = C(phi)·ℓ(k)^2` for a SINGLE linear form ℓ(k). Closure (o2=0) ⟺ ℓ(k)=0: a 2-dimensional
  plane of k, and phi enters ONLY as the amplitude coefficient C(phi) of the violation.
- **k=0 makes o2=0 for EVERY phi.** This is not fragile: at k=0 each leg depth is exactly
  -(1/2)log(a^2)=phi_j−phi_i, so the loop sum telescopes to 0 identically for all phi (this IS the
  driver's own O(t^0)=0, O(t^1)=0). t is literally the k-scale (script comment), so the entire
  series being O(t^2) is the statement "mixing-off closes for all phi."

CONSEQUENCE: the closure demand EXCLUDES NO phi profile — it is satisfiable for any depth profile by
turning mixing off (k=0), and generically by a 2-parameter cone of nonzero k as well. Therefore
closure imposes NO relation on phi. The obstruction relates phi to the free field k exactly as the
adversary's hypothesis (obstruction)=F(phi,R,k)=0 with k free; k absorbs it. This is COUPLING-INERT
in effect, NOT COUPLING-TRANSMITS.

Extra: the net loop-composed arrow for a coboundary mixing is EXACTLY the identity (net a=1, s=1,
residual m0≡0 — confirmed symbolically). So the composite's depth is exactly zero; the nonzero
"loop sum" is purely the NON-ADDITIVITY of the nonlinear eigenvalue extractor delta_t, not a
connection holonomy. The doc's phrase "the depth acquires loop holonomy — no longer a pure potential
difference" over-reads a generic non-additivity of a nonlinear functional as curvature.

## ATTACK 2 (faithfulness / import) — where does mu come from?

From `udt_complete_pair_phi_orchestra_audit_2026-08-05/EXACT_DERIVATION.md` sec.4: mu is the
off-diagonal entry of the "REGISTERED lower-triangular form" of the complete comparison arrow A.
The comparison between two observers is a general linear map, so an off-diagonal clock-screen entry
is metric-PERMITTED — not a foreign mechanism grafted on. So this is NOT a hard F-IMPORT.

BUT it is equally NOT a derived/forced native feature. The audit itself stamps: "current premises do
not identify them", "none is selected here", "OPEN: which strain/cocycle... is the physical UDT pair
depth." The founded/derived structure is DIAGONAL reciprocal; mu is an UNSELECTED, UNFORCED degree of
freedom. Q2 (this lane) confirms consistency does NOT quantize or select mu (continuous elliptic
family). So mu-on is a FREE CHOICE with a FREE value. Exercising it to OBSERVE is legitimate; but
presenting mu-on as native structure is unwarranted — it is a permitted DOF the metric neither
requires nor pins. "Is mu native?" → PERMISSIBLE, not forced; unselected.

## ATTACK 3 (F-STEER / scope) — honest or over-credited?

- Q0 gate (mu non-gauge INVARIANT): HONEST and real. mu enters conjugation-invariants (trace,
  Inv2), det(C)=s^2 is mu-independent; an O(1,2) endpoint boost conjugates C_A and cannot remove mu
  without changing the invariant spectrum. Gate genuinely passed. ✓
- O(mu^2) onset: HONEST (verified O(t^0)=O(t^1)=0; obstruction is degree-2). ✓
- Q2 mu-not-quantized (NO): HONEST (continuous rotation angle in m0). ✓
- Model/scope stamps (reciprocal-lock + one screen, free-kinematic): present and honest. ✓
- **The single over-credit = the OUTCOME CLASS.** The driver's own caveat ("entangles phi with the
  free field k; tune k for any phi; not yet a profile-pinning law") already states the ENTANGLES-ONLY
  fact — yet the class was stamped COUPLING-TRANSMITS, the pre-registered owner-favorable /
  "ATTACK HARDEST" bin. Naming the honest caveat but keeping the favorable label is exactly the
  F-STEER slippage the prereg warned against. The pre-committed COUPLING-INERT bin ("mu invariant but
  transmits NO depth constraint: coupling is real but not the law route") is the precise fit.

## Bottom line
Real, non-gauge coupling (single-arrow depth depends on mu, R). No transmitted constraint on phi:
mixing-off satisfies closure for every phi; phi is only the amplitude of an absorbable violation.
Honest class = COUPLING-INERT. No discreteness, no depth-law. Not a step toward a profile-pinning law.
