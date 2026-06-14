# dpf2 — BLIND ADVERSARIAL VERIFIER VERDICT: PARTIALLY DERIVED / SUBTLER ASSEMBLY

Verifier: independent main-loop blind adversarial pass (own sympy/mpmath,
own functional perturbation + parity recount; did NOT use the challenger's
dpf2_*.py as evidence — re-derived each load-bearing step). Agent id:
dpf2-blind-verifier. Date: 2026-06-14. Script: `/tmp/verify_dpf2.py`,
`/tmp/verify_count.py`, `/tmp/final_check.py`. Log: `/tmp/dpf2_verify.log`.
New file (append-never-edit).

DATA-BLIND HELD: no lepton wall numbers loaded; contract 26fc757 NOT opened
(grep of all dpf2 scripts: none of 105.6 / 0.51099 / 1776 / 0.97767 /
1.93121). The alphabet is 1+3+5; dim-7 appears only as excluded.

Prosecution stance: this is a PRIOR-CONFIRMING positive (a clean forced
rational from the seal — the program's hope). Per the charter's hypothesis
discipline I aimed the HARDEST attack here, default skeptical. The prior
sibling (dpf_results.md) was an assembled splice; this push claims to be the
GENUINE functional perturbation that fixes it. The question: genuine, or a
subtler smuggle?

---

## OVERALL VERDICT: PARTIALLY DERIVED. The functional perturbation (the c^2
## power, the c->0 vanishing, the absence of W(P) and the exponential) is
## GENUINE and now solidly banked — a real improvement over the refuted
## splice. But the RATIO 2 is NOT forced: it rides on THREE uncomputed
## conventions (the cross-sector seal map kappa_seal, the junction count
## n_odd=L, and the closure J^2=L), each individually load-bearing, each
## able to move the number. The assembly is gone; convention has taken its
## place. The "ratio = 2, EXACT, no free datum" headline overshoots.

---

## PER-KILL-SHOT VERDICT

**A. THE FUNCTIONAL PERTURBATION — GENUINE (banked).** Reproduced with my
own sympy: `-2 P_F == L/(2kappa)-1` exactly (residual 0); P degree-1
homogeneous; H Taylor `= k^2/3 + k^4/5 + k^6/7 + ...`, EVEN, H(0)=0, all odd
coeffs zero. `Delta_p_F = -(gamma/2) H(kappa_seal)` with `kappa_seal =
sqrt3 J c/gamma` gives `-(J^2/2)(c^2/gamma) - (9J^4/10)(c^4/gamma^3)+...`,
coeff(c^1)=0, c->0 limit 0, slope 0, mpmath residual drops 100x/decade. NO
exponential, NO W(P) emerge. This is the real calculation the prior verifier
DEMANDED and it was genuinely carried out. The c^2-only law and exact c->0
vanishing are a THEOREM of (H even, H(0)=0) + (kappa_seal linear in c) —
solidly banked, and stronger than the prior jet-norm argument. **A: FORCED.**

**B. kappa_seal = sqrt3 J c/gamma — CONVENTION (the crux smuggle).** The
1/gamma is load-bearing and NOT derived. My check: with `kappa_seal ~ c` (no
1/gamma) the result is `c^2*gamma`; with charge unit 1 (not gamma/2) it is
`c^2/gamma^2`. The advertised `c^2/gamma` needs BOTH the 1/gamma in
kappa_seal AND the gamma/2 unit. Worse, a SECTOR-MISMATCH hides here: the
exterior_cavity functional's `kappa` is the STATIC spatial anisotropy of
`f = F(1+kappa cos theta)`, and `a = F kappa/sqrt3` is the static angular
FIELD; but the c-jet `b*=-c` is `g_Ttheta`, a TIME-ROW (f_T-driven,
nonstationary) component. `kappa_seal = sqrt3 J c/gamma` ASSERTS that the
time-row jet populates the static-shape amplitude linearly with gamma in the
denominator. That cross-sector bridge (time-row -> static kappa) is exactly
the "physically natural amplitude reading" the doc flags — never a junction
solve. It is the SAME load-bearing convention dressed as a substitution. The
"1/2" is likewise the chosen gamma/2 unit (the 1/3-cancels-3 yields coeff 1;
the 1/2 is the separately-picked charge normalization), NOT a pure
functional cancellation as STEP 3 implies. **B: CONVENTION, the crux.**

**C. n_odd(L)=L — WRONG INVOLUTION (REFUTED as derived).** This is the
decisive finding. dpf2_junction.py asserts the same-minus fold acts as the
ANGULAR reflection `theta->pi-theta`, giving real-harmonic parity
`(-1)^(L+m)` and n_odd=L. But the banked source says otherwise: w6 defines
the same-minus involution as `(a,b)=(g_Tr,g_Ttheta)->(-a,-b)` — a fold on the
TIME-ROW JET COMPONENTS, with the angular `(r,theta)` sector EXPLICITLY
UNTOUCHED (w7:49). w7:53-54 states `sigma IS f_T->-f_T — sigma is TIME
REVERSAL on the crease`, and the even/odd (Neumann/Dirichlet) parity is along
the RADIAL-TIME spine `z in [-L,L]`, NOT along theta. There is no
`theta->pi-theta` anywhere in w6/w7/h1_types; it appears only in dpf2.
n_odd=L is obtained by importing a fabricated angular involution that
contradicts the actual sigma. Under candidate involutions I get L (axis-plane
m->-m sin-count), 2L+1 (full dim), or 0/3/0 (antipodal) — the count is
purely a choice of involution, and the chosen one is not the banked one.
**C: CONVENTION on a wrong involution — the ratio's load-bearing factor is
not derived from sigma.**

**D. J^2=L — CONVENTION (uncomputed closure).** Closure (a) J^2=L gives ratio
2; closure (b) J^2=1/L gives 1/2. The doc argues (a) from "per-component
independence," but no closure integral is computed; (b) is equally a "legal
closure of the same functional" by the doc's own admission. The choice that
lands on 2 (= L_S5/L_A3) is asserted, not solved. **D: CONVENTION.**

**E. RATIO = 2 — DATA-BLIND held; "forced" is FALSE.** No wall number entered
(verified). But "forced, no free datum" is conditional on B (cross-sector
map), C (n_odd=L from the wrong fold), and D (J^2=L). Flip C to the full
dimension (2L+1) -> ratio 3/2; flip D to (b) -> ratio 1/2. And the MASS ratio
`(p_F+Delta[S5])/(p_F+Delta[A3])` still carries `c/gamma` — so even the
"forced 2" is only the CORRECTION ratio, and `2 = L_S5/L_A3` is suspiciously
trivial (just the angular orders, reached via three choices that conspire to
that triviality). **E: NOT forced; trivial-by-construction.**

**F. ANTI-ASSEMBLY / ANTI-NUMEROLOGY — IMPROVED but SUBTLER CONVENTION.**
The genuine win: the multiplicative splice (p_F·W·floor·exp) is GONE; W(P)
and the exponential demonstrably do not emerge. That refutation is honest and
correct. But the load-bearing number has migrated from "splice of three
objects" to "three uncomputed conventions (B,C,D)" — each a single
plausible-but-unforced choice. This is NOT numerology (no fake dim-7, real
functional), but it is convention-driven, and the headline ("EXACT, no free
datum, FORCED ratio 2") oversells it the same way the prior headline did.

---

## WHAT IS SOLIDLY BANKED (survives)

- The GENUINE O(c^2) functional perturbation: `Delta_p_F = -(J^2/2)(c^2/gamma)
  + O(c^4)`, derived by Taylor-expanding the ACTUAL `H(kappa)=L/(2kappa)-1`.
  NO exponential, NO W(P) emerge — the prior splice is correctly retired.
- c^2-ONLY scaling and EXACT c->0 vanishing (value and slope) — a theorem of
  H even, H(0)=0, plus a linear-in-c seal map. Reproduced independently.
- trace (L=0) -> 0 — consistent with "P_F vanishes on spherical flows."

## WHAT IS CONVENTION / NOT FORCED

- `kappa_seal = sqrt3 J c/gamma`: the 1/gamma AND the cross-sector
  (time-row b* -> static kappa) bridge are uncomputed reading-grade choices
  driving the `1/gamma`. The `1/2` is the chosen gamma/2 unit, not a
  cancellation. (B)
- `n_odd(L)=L`: rests on a FABRICATED angular involution `theta->pi-theta`
  that CONTRADICTS the banked sigma (which is time-reversal on the jet, with
  the angular sector untouched). Not derived from the actual fold. (C)
- `J^2=L` (closure a): an uncomputed action-closure choice; (b) J^2=1/L is
  equally admissible and gives ratio 1/2. (D)
- Therefore the inter-sector ratio 2 is a CONSTRUCTION conditional on B+C+D,
  not a forced data-blind prediction. (E)

## RECOMMENDATION

Bank: (i) the genuine O(c^2) functional perturbation and its c->0 vanishing
(real, an honest fix of the splice); (ii) that W(P) and the exponential do
NOT emerge (the prior product is retired). Do NOT bank the ratio 2 as forced.
To force it requires: (a) deriving kappa_seal from a one-sided junction
expansion of the angular field at the seal (settling the time-row->static
bridge and the 1/gamma); (b) the parity count from the ACTUAL sigma
(`(a,b)->(-a,-b)`, time-reversal on the jet — w6/w7), NOT a substituted
`theta->pi-theta`; (c) an actual closure integral fixing J^2(L). Until then:
PARTIALLY DERIVED — the functional is genuine, the ratio is convention.
