# Adversarial Review 1 — MISSED-INVARIANT / CIRCULARITY attack. UNBANKED, do not commit.

Reviewer: fresh adversary (Opus). Date 2026-08-06. Branch grok. Method: independent sympy
recompute, NONE of the probe's code imported (rev_kin.py, rev_probe.py, scratchpad). Full 4D
metric ds^2=-e^{-2phi}c^2dt^2+e^{2phi}(dx^2+dy^2+dz^2), u^mu=(e^{phi}/c,0,0,0).

## Independent recompute (agrees with DERIVATION_NOTES, exact)
- a_mu=(0,-phi',0,0); a^mu=(0,-e^{-2phi}phi',0,0); a^2=e^{-2phi}(phi')^2.
- theta=0; sigma=0; omega=0; sigma^2=omega^2=0.
- a_mu-∇_mu ln V = 0 exactly, V=sqrt(-g_tt). CONFIRMED.
- R_{mu nu}u^mu u^nu = -e^{-2phi}phi'' (full 4D). [NOTE: the notes' "(2phi'^2-phi'')e^{-2phi}"
  and R=2(phi''-2phi'^2)e^{-2phi} are the 2D-CORE numbers transcribed into a 4D document; my
  4D values differ (R=-2(phi'^2+phi'')e^{-2phi}). Immaterial to the verdict — both are g-scalars.]

## FRONT 1 — missed invariant? NO. (attack on "trivial")
The reduction is STRUCTURAL, not an artifact of derivative order. u is a *metric functional*:
u = (h.o. timelike Killing vector)/|.|, and xi, its norm, and the normalization are all fixed by
g. Any scalar in (g,u,∇u,∇∇u,...) is therefore a scalar in g alone. Checked the four escape routes:
- (a) 2nd-derivative-of-u scalars: ∇∇u is still built from g ⇒ g-scalar. No escape.
- (b) transverse sector — added a DISTINCT warp e^{2psi}(dy^2+dz^2), psi≠phi, recomputed from
  scratch: theta=0, omega=0, a_mu=∇_mu ln V still hold. No escape.
- (c) a scalar separating u from a GENERIC unit timelike w: none on-solution — the very content
  that would distinguish w (its independent a/theta/sigma/omega data) is, for u, fixed by g.
- (d) "u h.o. AND shear/expansion-free is a nontrivial (g,u) condition": it is not — it is exactly
  the statement "g is static" (a pure g-property: existence of a h.o. timelike KV). Reduces to g.
CONCLUSION: no (g,u)-invariant exceeds the g-invariants, at ANY derivative order. Q1/Q2 "trivial"
is airtight. CT-PROFOUND-STATIC is FALSE.

### Precision catch (real, non-fatal): the "UNIQUE timelike Killing direction" claim (notes §2
line 38) is OVERSTATED. xi_b=∂_t+b∂_y is ALSO a Killing vector (verified L_k g=0) and is timelike
for small b — a whole boost family of timelike KVs exists. What actually pins u is
HYPERSURFACE-ORTHOGONALITY: xi_b has k∧dk = -4bc^2 phi' ≠ 0 (verified), so it is NOT h.o.; only
∂_t is. The load-bearing fact must read "unique h.o. timelike KV" (as the Q1 verdict line 61
correctly does), not "unique timelike KV." u stays metric-determined either way ⇒ verdict unchanged.

## FRONT 2 — is Q3 a real result of THIS metric, or imported generality? IMPORTED.
Q3 = "adding an independent unit timelike u to the field content enlarges the divergence-free-
2-tensor space beyond Lovelock's metric-only class." Adjudication:
1. "Promote u to independent" is a bare POSTULATE, not derived — the notes/prereg tag it
   SUPPLIED/CHOSE/foundational. Honest, but it means the enlargement is a *tautological*
   consequence of the postulate (add ANY field ⇒ larger law space).
2. Metric-independence test: Q3 is TRUE verbatim on Minkowski, Schwarzschild, de Sitter —
   it references nothing about phi, reciprocal-lock, or copresence. It is the generic
   Einstein-aether/Horava observation, cited as such in §4. It is NOT a property of this metric.
3. Non-circular AS A THEORY statement (it states what laws the field content admits, not a
   measurable) — granted. But it contributes ZERO metric-specific content, and the only positive
   it carries rides entirely on the SUPPLIED postulate. Leaning the RESULT's class on it
   over-weights a postulate-driven generic fact.
4. By the prereg's OWN CT-PROFOUND-DYNAMIC definition (§4), that class requires "physically
   distinct in moving/time-live regimes." The notes did NOT exhibit that: Q2 (moving frame)
   COLLAPSED to the Killing energy in this metric class. The DYNAMIC payoff is an explicit
   promissory note ("off this redundant solution", "requires a selected law + a regime where u
   is not metric-pinned"), i.e. UNREALIZED here. A promise is not a result.

The Q1("u metric-determined")/Q3("u independent field content") pair is not a formal contradiction
— a field can be an independent DOF whose on-shell value on a symmetric solution equals a metric
functional (cf. a scalar frozen by symmetry). So it is not sleight-of-hand. BUT the coherence is
purchased entirely by the postulate, and the enlargement it buys is metric-blind.

## VERDICT: TRIVIAL — honest class CT-TRIVIAL for THIS result.
No missed invariant exists (Front 1 airtight; structural reduction, all derivative orders). Q3 is
true but content-free for this metric: generic, metric-independent, postulate-driven, and it
realizes no invariant on this solution; the DYNAMIC clause of the prereg is unmet (Q2 collapsed).
The honest bankable class is CT-TRIVIAL, with Q3 recorded as a TRUE-but-generic theory-space note
(the aether/Lovelock fact) whose payoff is deferred to an unexhibited off-pinned regime + unselected
law. Labeling the landed outcome CT-PROFOUND-DYNAMIC over-credits an imported generality.
Correction owed: "unique timelike KV" → "unique hypersurface-orthogonal timelike KV."
