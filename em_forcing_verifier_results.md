# BLIND ADVERSARIAL VERIFIER — em_forcing_results.md

Verifier: Claude (Opus 4.8, 1M context), agent id `em-forcing-verifier`.
Date: 2026-06-14. Mode: independent re-derivation, DATA-BLIND. The doc's own
scripts (`em_forcing.py`, `em_forcing2.py`) were NOT read or run. All results
below come from independently written scripts:
`em_forcing_verify.py` … `em_forcing_verify6.py` (sympy 1.13.1, CPU).

Background re-derived from the prompt/CANON metric directly:
`ds^2 = -e^{-2phi} c^2 dt^2 + e^{2phi} dr^2 + r^2 dOmega^2`, phi taken FULLY
general phi(t,r,theta) so no cancellation is smuggled. sigma = (t -> -t).

---

## Metric sanity (independent)

- `g^tt g^rr = -1/c^2` (exact). The doc's "g^tt g^rr = -1" is the c=1 unit
  convention; the phi-cancellation it relies on is the c-carrying version.
  CONFIRMED.
- `sqrt(-g) = r^2 |c sin theta|` — phi GONE from the volume element.
  CONFIRMED.

---

## CLAIM 1 — Maxwell/Proca time-row stress; Poynting; electric-only zero

Independently computed `T_{mu nu} = F_{mu a} F_nu^{ a} - 1/4 g_{mu nu} F^2`
with `F = dA`, axisymmetric `A=(A_t,A_r,A_theta,0)`, general phi(t,r,theta):

    T_tr     = (1/r^2)(d_theta A_r - d_r A_theta)(d_theta A_t - d_t A_theta)
    T_ttheta = e^{-2phi}(d_t A_r - d_r A_t)(d_theta A_r - d_r A_theta)

EXACT match to doc Task 1. Each is (a time-carrying field-strength factor
F_{t.}) × (the spatial magnetic factor F_{r theta}) — the Poynting E×B
momentum-flux structure. CONFIRMED.

- ELECTRIC-ONLY (A_t alone, A_r=A_theta=0): `T_tr = 0` and `T_ttheta = 0`
  IDENTICALLY (rebuilt from scratch, not substituted). CONFIRMED — a static
  Coulomb-type field carries no time-row flux.
- PROCA extra (L += -1/2 m^2 A^2): `dT_tr = m^2 A_r A_t`,
  `dT_ttheta = m^2 A_t A_theta` (the e^{±2phi} cancel exactly). EXACT match
  to doc Task 1 Proca. CONFIRMED.
- SIMULTANEOUS SUPPLY: a SINGLE field supplies BOTH components. Numeric check
  with the doc's own config (A_t=cos t/r, A_r=sin t cos th, A_th=sin t·r,
  phi=0.3 cos th·r) at (t,r,th,c)=(0.4,1.4,0.6,1):
    Maxwell  T_tr=+0.4009, T_ttheta=-0.3747
    Proca    T_tr=+0.4537, T_ttheta=-0.2850
  Reproduces the doc's +0.401/-0.375 and +0.454/-0.285 to all printed digits.
  CONFIRMED.

**CLAIM 1: CONFIRMED.** (Sign of overall T is a convention; the zeros,
ratios, and Poynting structure are convention-independent.)

---

## CLAIM 6 / parity (P3)

Under sigma: t->-t with A_t even, A_r/A_theta odd, both T_tr and T_ttheta are
sigma-ODD (`T(sigma) + T = 0` verified symbolically on the concrete config).
CONFIRMED — the supplier sits on the odd channel; no even source is smuggled
onto an odd equation.

---

## CLAIM 2 — static-limit Coulomb (EXACT)

Source-free static Maxwell, A_t=f(r), static phi(r), independently:

    sqrt(-g) F^{rt} = -(r^2 |c sin th|/c^2) f'(r)     [phi ABSENT]
    Maxwell eq d_r( sqrt(-g) F^{rt} ) = 0  =>  r f'' + 2 f' = 0
    dsolve  =>  f(r) = C1 + C2/r   ==  A_t = c0 + Q/r

phi cancels (via g^tt g^rr = -1/c^2); the equation and the 1/r solution are
EXACT and scale-independent. Cross-checked at a NONTRIVIAL phi=a/r
(`em_forcing_verify6.py`): the Maxwell static eq is STILL r f''+2f'=0 and the
solution STILL C1+C2/r — phi genuinely drops out, not just at phi=const.

**CLAIM 2: CONFIRMED, EXACT.**

---

## CLAIM 3 — massless suffices; Proca neither forced nor forbidden

The F·F Poynting terms are nonzero at m=0, so the massless field alone closes
the sigma-odd time row (CONFIRMED). The Proca pieces are an additive
correction requiring BOTH an even (A_t) and an odd (A_r/A_theta) potential;
the match does not require m≠0, nor does it forbid it at the level of the
time-row supply. CONFIRMED as scoped ("allowed, neither forced nor
forbidden").

Note for strengthening (not a refutation): the doc flags but does not prove
that the EXACT Coulomb requires m=0. I confirm the *massless* static limit is
1/r; a Proca mass would add an m^2 A_t term to the static Maxwell equation
(Yukawa-type), breaking exact 1/r. So masslessness IS forced *if* one demands
the exact-Coulomb static limit — consistent with, and slightly stronger than,
the doc's cautious "allowed." Not a correction; an available upgrade.

---

## CLAIM 4 (THE ATTACK) — is "EM native" honest or over-claimed?

### Step A: does a sigma-ODD scalar ALSO supply the bare time row? YES.
Independently, `T_{mu nu}[S] = d_mu S d_nu S - 1/2 g_{mu nu}(dS)^2`:

    T_tr[S] = S_t S_r ,   T_ttheta[S] = S_t S_theta

Nonzero for a time-varying sigma-odd scalar. So the BARE structural match
(nonzero sigma-odd T_tr, T_ttheta) does NOT distinguish gauge from scalar.
The doc's "honest negative against uniqueness" is CONFIRMED — the gauge field
is NOT uniquely forced by the time-row match alone. The doc does not hide
this; it states it plainly (Task 5, Verdict 4).

### Step B: is the Coulomb-matching a GENUINE selector or circular aesthetics?
This is the load-bearing question. I solved the massless static scalar (box
S = 0) on the UDT background independently (`em_forcing_verify6.py`):

    general phi(r):   r S'' + 2 S' - 2 r S' phi' = 0   [phi' PRESENT]
    phi = a/r:        scalar  =>  S = C1 + C2 exp(2a/r)/a   [NOT 1/r]
                      Maxwell =>  f = C1 + C2/r            [exact 1/r]

The scalar's static profile is phi-DEFORMED (carries phi'); the gauge field's
is phi-CANCELLED and universally 1/r. They are genuinely DIFFERENT functions.
So "the gauge field matches UDT's own Coulomb and the scalar does not" is a
REAL structural discriminator, not a circular preference: UDT_REBUILD §3's
Coulomb is an independently-banked result, and only the closed 2-form
reproduces it because only it gets the g^tt g^rr=-1 cancellation. The scalar
uses g^rr alone and cannot.

**VERDICT on claim 4: HONESTLY SCOPED — NOT over-claimed.** The doc's
"NATURAL-BUT-NOT-UNIQUE + Coulomb-selected" is exactly right:
- "EM is forced" in the bare-time-row sense is correctly REFUSED (scalar
  competitor named and confirmed).
- "EM is selected" is correctly AFFIRMED via an independent structural fact
  (the exact phi-cancelled Coulomb), which I confirm distinguishes the gauge
  field from the scalar.
The verdict is calibrated, not dramatized. It is "between" (a) and (b) in the
prompt's framing, and the doc lands it there explicitly.

One honesty caveat the doc already owns: the selection is "the supplier that
ALSO closes the pre-existing Coulomb skeleton," and the Coulomb skeleton
(UDT_REBUILD §3) is itself a *conditional* derivation. So "native" rests on
two banked facts (forced odd source + conditional Coulomb), not one
unconditional theorem. The doc says exactly this. No overreach found.

---

## CLAIM (4'/coupled) — conservation consistency vs the forced source

The doc DEFERS full coupled Einstein-Maxwell on the off-diagonal background
(P5) and asks the verifier to at least check Bianchi/conservation.

- dF = 0 (F=dA closed): identically zero (all 4 independent components).
  CONFIRMED.
- Covariant conservation identity `nabla_mu T^{mu}_{ nu} = F_{nu a} J^a` with
  `J^a = nabla_mu F^{mu a}`: verified to machine zero (residual ~1e-122 to
  1e-125) on flat, flat-spherical, AND the UDT background by independent
  numeric substitution (`em_forcing_verify5.py`). A first symbolic pass
  returned a spurious nonzero due to a sympy Piecewise/tan simplification
  failure (sin theta = 0 branch), NOT physics; the numeric test settles it.
  => On-shell (source-free, J=0), `nabla_mu T^{mu}_{ t} = 0`. The Maxwell
  stress is a properly CONSERVED source, compatible with the contracted
  Bianchi identity nabla_mu G^{mu nu}=0 that the forced Einstein time-row
  must satisfy. CONFIRMED (consistency only).

- LIMIT OF THIS CHECK (the doc's standing gap): this is a *consistency* check
  on the DIAGONAL background (P5: matter stress sources the arm; matter does
  not itself live on the off-diagonal metric). It does NOT prove the FULL
  coupled system G_tr[arm] = kappa T_tr[A] has a self-consistent solution
  with A_mu back-reacting onto the arm. That stronger closure remains OPEN,
  exactly as the doc flags (Verdict 5, attack item 2). No obstruction found,
  but no closure proof either. Correctly deferred, not over-claimed.

---

## SUMMARY TABLE

| Claim | Verdict |
|---|---|
| 1. Maxwell T_tr,T_ttheta = Poynting; electric-only zero; one field both | CONFIRMED |
| 1. Proca extra m^2 A_r A_t, m^2 A_t A_theta | CONFIRMED |
| 2. static Coulomb r f''+2f'=0 => c0+Q/r, phi cancels EXACT | CONFIRMED (and at nontrivial phi) |
| 3. massless suffices; Proca allowed not forced/forbidden | CONFIRMED (+ available upgrade: exact-Coulomb forces m=0) |
| 4. scalar competitor T_tr[S]=S_t S_r also supplies bare source | CONFIRMED |
| 4. gauge SELECTED by Coulomb static limit (scalar gives phi-deformed, not 1/r) | CONFIRMED — genuine discriminator, not circular |
| 4. "EM native" = NATURAL-BUT-NOT-UNIQUE + Coulomb-selected | HONESTLY SCOPED, not over-claimed |
| 6. parity: T_ti sigma-ODD; A_t even, A_r/A_theta odd | CONFIRMED |
| dF=0; Maxwell stress conserved (Bianchi-compatible) | CONFIRMED (consistency) |
| FULL coupled off-diagonal closure | OPEN — correctly deferred, no obstruction found |

## OVERALL

**STANDS.** Every computed claim reproduces independently (exact symbolic
forms and the doc's own numerics to all digits). The pivotal "EM is native"
claim is HONESTLY SCOPED, not over-claimed: the doc itself refuses the strong
"gauge uniquely forced," names and confirms the sigma-odd scalar competitor,
and rests the selection on an independent structural fact (the exact
phi-cancelled Coulomb) that I independently confirm the scalar does NOT
reproduce. The targeting check (attack item 7) passes: the verdict stops at
natural-but-not-unique and names the competitor rather than narrating "EM is
forced." The single genuine gap — full coupled Einstein-Maxwell on the
off-diagonal background — is explicitly deferred by the doc, and my Bianchi/
conservation check finds it consistent with no obstruction (but no closure
proof). Recommend banking with the coupled-closure check logged as the open
next step, and the optional upgrade "exact Coulomb => masslessness forced"
noted.

Scripts saved: em_forcing_verify.py, em_forcing_verify2.py,
em_forcing_verify3.py, em_forcing_verify4.py, em_forcing_verify5.py,
em_forcing_verify6.py (all in repo root).
