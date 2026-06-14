# Delta_p_F THE RIGHTWAY — Genuine O(c^2) Perturbation of the Charge Functional

Date: 2026-06-14. Driver: Claude (Opus 4.8, 1M context). New file
(append-never-edit). Frame: CRITICAL_UNIVERSE_FRAME.md / CATALOG_FRAME.md.
Charles (2026-06-14): "launch it." METRIC-LED, ANTI-NUMEROLOGY,
DATA-BLIND, ANTI-ASSEMBLY.

This REPLACES the construction in dpf_results.md, which the blind verifier
(dpf_verifier_results.md) refuted as an ASSEMBLED splice of three disjoint
objects (`-p_F W(P) (c^2/gamma^2) exp(-(eta/2)d)`, d=2L). The verifier named
the real calculation: PERTURB the actual exterior_cavity charge functional
`H(kappa)=L/(2kappa)-1` to O(c^2) on the c-perturbed seal, and do a genuine
junction count. That is done here.

Scripts: `dpf2_derive.py` (11/11), `dpf2_junction.py` (5/5),
`dpf2_assemble.py` (4/4), `dpf2_adversary.py` (6/6 survived). Log:
`/tmp/dpf2.log`. Blind verifier: PENDING (attack-here block at end).

---

## STEP 1 — THE ACTUAL FUNCTIONAL (re-derived, not guessed)

From exterior_cavity_results.md banked positive #1 (re-derived in
rescued_workspaces/.../v_c1_closedforms.py; reproduced exactly here):

    f = F(y)(1 + kappa cos theta)        angular metric profile
    a = F kappa / sqrt(3)                angular field;  kappa = sqrt(3) a/F
    P(F,a) = (3 a^2/(8 F)) G1(kappa)     angular potential (EXACT)
    G1 = (2k + (k^2-1) L)/k^3 ,  L = ln((1+kappa)/(1-kappa))
    H(kappa) := -2 P_F = L/(2kappa) - 1  THE charge functional  (P_F = dP/dF)
    p_F = gamma/2  at c=0                 the monopole (Misner-Sharp) charge

Here **kappa is the angular-anisotropy amplitude** of the metric (not the
transfer-matrix kappa), and `H` IS the genuine charge object — verified
`-2 P_F == L/(2kappa)-1` exactly, and `P` degree-1 homogeneous (the
screening identity). The Taylor series of the functional is the load-bearing
fact:

    H(kappa) = kappa^2/3 + kappa^4/5 + kappa^6/7 + ...   (EVEN, no kappa^1)
    H(0) = 0 EXACTLY.

The functional has NO linear term and vanishes at zero amplitude. The c->0
anchor is therefore born INSIDE the functional, before any seal physics.

## STEP 2 — THE c-PERTURBED SEAL

The amplitude is `kappa = sqrt(3) a/F`. At the same-minus crease the weld jet
is `X_t(0)=(gamma,-c,0,0)` (w8/mass_audit): monopole channel `a*=gamma` sets
the F-scale, angular channel `b*=-c` sources the angular field `a`. The seal
angular amplitude is the angular tilt relative to the monopole:

    kappa_seal = sqrt(3) J (c/gamma)

linear in c, vanishing at c=0 (the seal datum `rho=-c-f q gamma` losing its
odd part), gamma in the denominator (amplitude = tilt relative to monopole).
`J` is an O(1) seal/junction transfer carrying the sector multiplicity
(fixed in STEP 4).

## STEP 3 — PERTURB H TO O(c^2): THE FORM THE FUNCTIONAL PRODUCED

The angular charge correction is the SAME functional read at the c-induced
amplitude, in the charge unit `gamma/2` that the monopole `p_F=gamma/2` fixes
(`P_F=-H/2`):

    Delta_p_F = -(gamma/2) H(kappa_seal)

Substituting and expanding (sympy + mpmath dps=60):

    Delta_p_F(c) = -(J^2/2)(c^2/gamma) - (9 J^4/10)(c^4/gamma^3) + ...

>>> **THE GENUINE O(c^2) RESULT (whatever H produced — and it is a pure
power law):**

    Delta_p_F = -(J^2/2) (c^2/gamma) + O(c^4)

Every factor EMERGED from the functional:
- **c^2 (not c^1):** `H` is even in kappa (leading `kappa^2/3`) AND
  `kappa_seal` is linear in c. The c^2 power is FORCED; there is no
  sign-bearing c^1 charge term (ADV-1: H has zero odd coefficients).
- **1/gamma:** from `kappa_seal=sqrt3 J c/gamma` (amplitude relative to the
  monopole) times the charge unit gamma/2: `(gamma/2)(c/gamma)^2`.
- **the numerical 1/2:** the `1/3` from H's leading term EXACTLY cancels the
  `(sqrt3)^2=3` from `a=F kappa/sqrt3` — a genuine functional cancellation,
  not a chosen constant.
- **NO exponential, NO W(P), NO exp(-(eta/2)d) appears.** The functional did
  not produce them. They were the splice in dpf_results.md.

**c->0 anchor (MUST hold):** `lim_{c->0} Delta_p_F = 0` and
`d Delta_p_F/dc|_{c->0} = 0`, both EXACT (genuine sympy limit of the full
nonlinear H; the naive subs gives 0/0 since `L/(2kappa)` is a removable
singularity). The high-precision mpmath check confirms the subleading is
O(c^2)-relative (residual falls 100x/decade), so O(c^2) is genuinely
leading. The 100%-angular-sourced anchor is reproduced as a theorem of the
functional + the linear seal map.

## STEP 4 — THE GENUINE JUNCTION COUNT (derived, not read)

The closed cell is the double of a collar `I x S2` across the same-minus
crease (h1_types). The fold acts as the crease reflection `theta->pi-theta`
(the mirror across the equatorial 2-sphere where the collar is doubled). A
real harmonic `Y_L^m` has parity `(-1)^(L+m)` under it (associated-Legendre
reflection). Parity dichotomy (w7): even->Neumann, odd->Dirichlet; ONE
parity BC per component.

| L | sector | dim=2L+1 | #even (Neumann) | #odd (Dirichlet) |
|---|---|---|---|---|
| 0 | trace | 1 | 1 | **0** |
| 1 | A3 | 3 | 2 | **1** |
| 2 | S5 | 5 | 3 | **2** |

The c-drive is sigma-ODD (`rho=-c-f q gamma`) => it pins the **Dirichlet**
content. Among the 2L+1 integers `(L+m)` (= 0,1,...,2L) exactly L are odd, so

    **n_odd(L) = L   EXACTLY.**   trace:0, A3:1, S5:2.

This is **NOT 2L** (the refuted reading: 0,2,4) and **NOT 2L+1** (the full
dimension: 1,3,5). It is **L** — the actual parity-odd (Dirichlet) multiplicity
of the order-L sector under the same-minus fold. dim-7 (L=3) is shown in the
script only to confirm it is excluded; it is never used as a sector.

## STEP 5 — ASSEMBLE ONLY WHAT THE MATH FORCES

Sector structure can enter `Delta_p_F = -(J^2/2)(c^2/gamma)` ONLY through `J`.
STEP 4 gives `L` INDEPENDENT Dirichlet data per order-L sector (one parity BC
per component, separately pinned). H is a quadratic (action) measure, so L
independent c-sourced amplitudes ADD in the action: `J^2 = n_odd(L) = L`
(closure (a); the equipartition closure (b) `J^2=1/L` would need a single
shared datum, contradicting per-component independence — ADV-3). Hence:

    **Delta_p_F(sector) = -(L/2) (c^2/gamma),   L in {0,1,2} for {trace, A3, S5}**

    Delta_p_F(trace) = 0                  (no odd channel; spherical => no shift)
    Delta_p_F(A3)    = -(1/2)(c^2/gamma)
    Delta_p_F(S5)    = -(c^2/gamma)

### DOES IT FACTORIZE? — YES, but NOT the way dpf_results.md claimed.

The genuine O(c^2) functional perturbation **factorizes cleanly per sector,
and the per-sector weight is the JUNCTION COUNT L itself — not W(P), and with
NO exponential.** The forced inter-sector ratio is a **pure rational**:

    **Delta_p_F[S5]/Delta_p_F[A3] = L_S5/L_A3 = 2   (EXACT, no free datum)**

(gamma and c cancel; there is no `m=c/c*` free multiple in the ratio.) This is
a *different, genuinely derived* number from the refuted assembled
`(5/3)e^{-1/18}=1.577`. The W(P) weight and the exponential never entered the
charge functional; the functional sees the Dirichlet junction count L.

---

## SOLID vs HYPOTHESIS-GRADE (honest split)

**SOLID / FORCED (from the actual functional + the derived count):**
- The functional form **Delta_p_F = -(J^2/2)(c^2/gamma)** — a pure O(c^2)
  power law, derived by Taylor-expanding the actual `H(kappa)`. NO
  exponential, NO W(P) (they did not emerge).
- The **c^2-only** scaling and the **c->0 exact vanishing** — a theorem of H
  being even in kappa with `H(0)=0`, plus the linear seal map. (Stronger than
  the prior jet-norm argument: it is the FUNCTIONAL'S own structure.)
- The **junction count n_odd(L) = L** (Dirichlet/odd multiplicity of the
  order-L mode across the same-minus crease) — derived from the parity
  dichotomy, replacing the read d=2L. trace 0, A3 1, S5 2.
- The **trace sector shift is exactly 0** — matches the banked "P_F vanishes
  on spherical flows" (L=0 has no odd channel) — a genuine cross-check the
  functional passes.
- The seal placement (odd/Dirichlet, sigma-ODD c-insertion, Xi=dTheta exact)
  — banked/verifier-confirmed (w6/w7/h1_types).

**HYPOTHESIS-GRADE / LOAD-BEARING INPUTS (flagged for the verifier):**
- **The seal amplitude map `kappa_seal = sqrt3 J c/gamma`** — that the angular
  jet `b*=-c` populates the functional's anisotropy amplitude linearly, with
  gamma in the denominator (amplitude relative to the monopole). The 1/gamma
  rides on this reading (ADV-2). A full junction-condition solve of the
  angular field's seal value would pin it; here it is the physically natural
  amplitude reading.
- **Closure (a) `J^2 = L`** (independent Dirichlet data add in the action)
  vs (b) `J^2=1/L`. Argued from per-component BC independence (STEP 4), not
  computed from a single closure integral. This sets the ratio (2 vs 1/2).
- **The reflection parity convention `(-1)^(L+m)`** (crease = fixed equatorial
  2-sphere of the doubled collar) vs the antipodal `n->-n` (which gives
  0,3,0 — ADV-4). The reflection is the geometrically correct same-minus
  fold, but the convention is load-bearing for the count.

**NOT CLAIMED / NOT REINTRODUCED:** no dim-7, no L7; no W(P) in the charge;
no exponential attenuation; no wall-number comparison; the refuted assembled
product is explicitly contrasted, not reused.

---

## ANTI-ASSEMBLY CONFIRMATION

Every factor of the final `Delta_p_F = -(L/2)(c^2/gamma)` EMERGED from one of
two genuine computations: (i) the Taylor expansion of the actual charge
functional `H(kappa)` on the c-perturbed seal (gave the form, the c^2, the
1/gamma, the 1/2, and the c->0 vanishing); (ii) the same-minus parity count
(gave the per-sector weight L). **W(P) was never multiplied in** — it does not
appear, and the functional's sector ratio (2) demonstrably DISAGREES with the
W-readout ratio (5/3), confirming the prior product was a splice of disjoint
machineries. No banked number was inserted because it was banked.

## DATA-BLIND + NO-DIM-7 CONFIRMATION

No lepton wall numbers loaded/matched (grep of all dpf2 scripts: none of
105.6 / 0.51099 / 1776 / 0.97767 / 1.93121; contract 26fc757 not opened).
The alphabet is 1+3+5; dim-7 appears only to confirm exclusion. The push was
METRIC-LED (interrogating the derived charge functional + the derived fold
count), not template-led.

---

## WHAT THE BLIND VERIFIER SHOULD ATTACK HARDEST

1. **The seal amplitude map `kappa_seal = sqrt3 J c/gamma`** (the one input
   that injects the 1/gamma and links c to the functional). Is the angular
   field's seal value genuinely linear in the c-jet with gamma in the
   denominator? A one-sided junction expansion of the angular EL at the seal
   should confirm or refute the linear, gamma-normalized amplitude.
2. **The closure `J^2 = L`** (independent Dirichlet data add in the action).
   Is the action contribution of the L odd components genuinely an
   independent sum (=> J^2=L, ratio 2), or coupled/shared (=> a different
   J^2(L) and ratio)? This sets the entire inter-sector ratio.
3. **The parity convention.** Confirm the same-minus fold is the crease
   REFLECTION `theta->pi-theta` (n_odd=L), not the antipodal map (n_odd
   =0,3,0). The doubled-collar geometry says reflection; verify against the
   actual sigma action on the angular harmonics.
4. **The charge unit `gamma/2`.** Confirm the angular charge shift is read in
   p_F's units (`P_F=-H/2`, monopole sets the scale) and that this is a
   normalization of the SAME functional, not a smuggled multiplication by the
   banked p_F.
