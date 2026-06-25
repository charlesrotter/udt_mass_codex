# BLIND VERIFIER — Nonstationary Cell / sigma-ODD (Spinor) Forcing

Verifier agent: **verifier-2026-06-14** (Opus 4.8, 1M ctx), blind adversarial.
Date: **2026-06-14**. Target: `fermion_forcing_results.md`.
Discipline: independent re-derivation from scratch. I did NOT read or run any
authored script (`fermion_forcing*.py`, `winding_stress.py`, `ff_*.py`). All
results below are from my own scripts, listed at the end. DATA-BLIND (no masses).

## VERDICT IN ONE LINE

The doc **STANDS on its CORE physics but is SCOPED MORE TIGHTLY than it states,
and one structural fact it deferred as "open" I have now CLOSED** — in the
direction that WEAKENS, not strengthens, the spinor case. Specifically: the
forced sigma-ODD source **VANISHES AT THE SEAL** identically (I computed it; the
doc only conjectured the sign). That makes the doc's "favoured-but-not-forced"
verdict for the spinor correct in letter, but its named "open hinge" is in fact
ALREADY DECIDED against C-strong by the Einstein tensor itself.

---

## Claim-by-claim

### Claim 1 — sigma-ODD Einstein components nonzero iff arm nonzero. **CONFIRMED, with a caveat.**

Independent exact sympy (`ffv_einstein.py`, `ffv_tdphi.py`) + independent numeric
finite-difference (`ffv_numeric.py`, a fully separate code path: build g(x)
numerically, FD Christoffel/Ricci/G):

- STATIC limit (arm=0, **phi static**): `G_tr = 0`, `G_ttheta = 0` EXACTLY
  (sympy) and 0.000e+00 (numeric). CONFIRMED.
- Nonzero **arm** with phi static: `G_tr`, `G_ttheta` NONZERO; sympy shows the
  closed form genuinely contains `A_t`, `A_r`, `B_t`, ... CONFIRMED.

CAVEAT (a real correction): the doc's reduction reported `A_tt=False, B_tt=False`
in the FULL G time-row. My full unsimplified G_tr/G_ttheta **do** contain `A_tt`,
`B_tt` before cancellation. This is a presentation difference (post-simplify the
leading time-row forcing is first-order in the arm velocity), not a physics
error, but the doc's flat "A_tt absent" is not what the raw tensor shows.

### Claim 5 / static limit — **CONFIRMED.** G_tr = G_ttheta = 0 identically at arm=0
(phi static). The static negatives #43–#45 are SCOPED, not contradicted. Clean.

### Claim 2 / P4 ATTACK (time-dependent phi) — **PARTIALLY REFUTED AS STATED; physics survives.**

This is the load-bearing attack the doc flagged. I ran it (the authored general
run "did not finish"; mine did, exact sympy `ffv_tdphi.py` + numeric).

**Finding A (NEW — the doc's static-limit statement is incomplete):** with
**arm = 0** but phi = phi(t,r,theta), the time row is NOT zero:

    G_tr     (arm=0, phi t-dep) = 2*phi_t / r
    G_ttheta (arm=0, phi t-dep) = -2*phi_t*phi_theta - phi_{t,theta}

So "G_tr, G_ttheta vanish identically when the arm vanishes" is FALSE in general
— it is only true when phi is static. A time-dependent diagonal (even) phi
sources the time row by itself. The doc's Section 1/3/6 over-state arm=0 ⇒ 0.

**Finding B (the rescue, and it is the SAME mechanism the doc uses elsewhere):**
under the SEAL involution, phi is EVEN in t, so at the fixed surface t=0,
phi_t = phi_{t,r} = phi_{t,theta} = 0, and the phi-sourced time row VANISHES at
the seal. AND the arm-sourced forcing SURVIVES: away from the seal the arm's
contribution to G_tr, G_ttheta adds on top of the phi_t contribution and is
NUMERICALLY EQUAL to the phi-static+arm value (I isolated it:
dG_tr ≈ 4.16e-2, matching the phi-static+arm 4.08e-2). So:

> **The arm forcing SURVIVES time-dependent phi (P4 does NOT collapse Claim 1).
> A time-dependent EVEN phi cannot cancel it — phi_t and the arm enter as
> INDEPENDENT, additive sources of the time row.** Claim 1's PHYSICS holds; its
> arm=0⇒0 WORDING needs the qualifier "for static phi (or at the seal)".

### Claim 3 / bosonic insufficiency — **CONFIRMED.**

Independent winding stress `ffv_winding.py`,
T = Lambda[d_mu n . d_nu n - 1/2 g (dn)^2], hedgehog n:

- STATIC hedgehog: `T_tr = 0`, `T_ttheta = 0` EXACTLY. T_tt, T_rr match the
  doc's printed expressions verbatim.
- Time-dependent winding: `T_tr = Lambda Theta_r Theta_t`,
  `T_ttheta = Lambda Theta_theta Theta_t`. For an EVEN-in-t Theta, Theta_t=0 at
  the seal ⇒ T_tr=T_ttheta=0 at the seal. CONFIRMED.
- I add: even an ODD-in-t winding SCALAR gives T_tr=0 at the seal, because
  Theta odd ⇒ Theta(0)=0 for all r ⇒ Theta_r(0)=0 ⇒ Theta_r Theta_t = 0.

The seal-node argument is NOT smuggled: t=0 is the fixed surface of the named
involution sigma:t->-t, and "even function ⇒ odd t-derivative is 0 at t=0" is a
theorem, not a chosen seal location. CONFIRMED honest.

### P3 / parity assignment — **CONFIRMED.** Requiring ds^2 invariant under the
named seal involution sigma: t->-t forces the arm (g_tr, g_ttheta multiply
dt·dx, picking up one sign) to be ODD and phi (g_tt multiplies dt^2) to be EVEN.
Analytic, not a free choice. A different involution (P×T) would regrade, but
that is a DIFFERENT seal than the w6/#42 same-minus time reversal.

### Claim 4 / THE HONESTY CHECK (spinor favoured-but-not-forced) — **CORRECTLY SCOPED IN LETTER, but the doc's "open hinge" is ALREADY CLOSED against C-strong.**

The doc keeps (C-weak: odd content forced) and (C-strong: T^2=-1 spinor forced)
apart and refuses C-strong, naming the open hinge as: *"is the seal-VALUE of the
forced odd source required nonzero? If yes ⇒ single-valued odd boson is
Dirichlet-pinned to 0 there ⇒ spinor forced; if it may vanish at the seal ⇒
single-valued odd boson suffices ⇒ no spinor forced."*

**I COMPUTED the seal-value the doc deferred.** With seal parities (phi even,
arm odd), the forced odd Einstein source AT the seal is IDENTICALLY ZERO:

- Exact sympy (`ffv_survive.py`): G_tr|seal = G_ttheta|seal = 0, even with the
  surviving arm velocities A_t, B_t present.
- Numeric scan (`ffv_hinge.py`): over 40 random admissible seal jets (generic
  even phi + odd arm) at 3 spatial points, worst |G_tr|,|G_ttheta| at t=0 =
  0.000e+00; away from the seal (t=0.4) the same fields give G_tr ~ -5e-1.

The reason is exactly the prompt's Task-4(b) suspicion: the arm is sigma-ODD ⇒
arm = 0 ON the fixed surface ⇒ G_tr=0 there ⇒ (G=kappaT) T_tr=0 there. **The
forced odd source vanishes at the seal.** Therefore, by the doc's OWN
dichotomy, the "if it may vanish at the seal ⇒ single-valued odd boson suffices,
no spinor forced" branch is the one that obtains.

**Consequence for the verdict:** the doc's headline "T^2=-1 spinor
FAVOURED-AND-NATURAL BUT NOT YET FORCED" is still TRUE (the spinor is indeed not
forced), but the doc's reason — "open pending a junction-condition computation"
— is WRONG: it is not open; the Einstein tensor already shows the source the
single-valued boson would need to carry through the seal is zero AT the seal, so
a Dirichlet-pinned single-valued odd boson is NOT excluded. The doc thus
UNDER-resolves toward the spinor (it leaves a door open that the geometry has
already shut). It does NOT over-claim a forced spinor — good — but its stated
"hinge to C-strong" is not live.

Honest two-sided result the prompt demanded:
- (i) Can C-strong be CLOSED (seal-value forced nonzero ⇒ spinor)? **NO** — seal
  value is provably 0.
- (ii) Can a single-valued sigma-ODD boson supply the BULK forcing while
  vanishing at the seal (Dirichlet-compatible)? **YES, not excluded** — the
  bulk source is nonzero, the seal source is zero, exactly a Dirichlet odd
  field's profile. (Whether a specific Proca configuration matches the full
  tensor is a separate constructive question, but nothing in the seal data
  forces two-valuedness.)

So: **the spinor is NOT secretly forced and NOT secretly excluded as a
candidate, but the specific argument the doc reserved for forcing it (nonzero
seal value) is refuted.** Spin-1/2 gets NO geometric foothold at the seal from
this computation.

### Targeting check — the doc did NOT steer to "spinor." It honestly stops at
C-weak. If anything it is slightly too GENEROUS to the spinor by leaving the
hinge "open" when the tensor closes it negatively.

---

## SUMMARY (for relay)

- **sigma-ODD matter forced, survives time-dependent phi?** YES (the arm sources
  G_tr,G_ttheta independently of phi_t; a time-dependent even phi cannot cancel
  it). BUT: the doc's "arm=0 ⇒ time row =0" is only true for STATIC phi or AT
  the seal — a t-dependent even phi alone gives G_tr=2 phi_t/r in the bulk.
  Wording correction needed; physics intact.
- **Bosonic insufficiency confirmed?** YES, exactly (static hedgehog T_tr=
  T_ttheta=0; even time-dep winding pinned to 0 at seal; odd winding scalar
  also 0 at seal). Independently reproduced, seal-node argument is sound.
- **Spinor favoured-but-not-forced correctly scoped?** The CONCLUSION (not
  forced) is correct, but the REASON is wrong: the doc's named open hinge
  ("is the seal-value nonzero?") is NOT open — I computed it = 0 identically.
  The forced odd source VANISHES at the seal, so a single-valued Dirichlet odd
  boson is NOT excluded and the spinor gets no seal-level forcing. The doc
  UNDER-resolves (leaves a closed door open); it does not over-claim.
- **Static limit clean?** YES — G_tr=G_ttheta=0 at arm=0/static phi; #43–#45 scoped.

**OVERALL: STANDS with required corrections.** Core forcing of sigma-ODD content
and bosonic insufficiency are CONFIRMED and survive the time-dependent-phi
attack. TWO corrections to bank: (1) "arm=0 ⇒ time row=0" holds only for static
phi/at the seal — state the qualifier; (2) the spinor "open hinge" is decided
NEGATIVELY by the Einstein tensor (seal-value of the forced source = 0), so
the route to C-strong via a nonzero seal value is closed, not deferred.

---

## Scripts (this verifier, independent, committed)

- `ffv_einstein.py` — exact sympy Christoffel→Ricci→G, static-phi; static limit.
- `ffv_tdphi.py` — exact sympy time-dependent phi; arm=0 time row = 2 phi_t/r etc.; seal reduction.
- `ffv_survive.py` — exact sympy full G(phi(t,r,th),A,B), seal-parity substitution ⇒ G_tr|seal=G_ttheta|seal=0.
- `ffv_numeric.py` — fully independent numeric finite-difference Einstein (separate code path); static/stationary/time-dep arm; time-dep even phi.
- `ffv_winding.py` — exact sympy winding (hedgehog) stress; T_tr,T_ttheta static and time-dep.
- `ffv_hinge.py` — numeric scan of 40 random admissible seal jets ⇒ seal-value of forced odd source = 0 (machine).
