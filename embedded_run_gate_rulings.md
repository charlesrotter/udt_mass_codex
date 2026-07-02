# Ruling — embedded-run gate questions (mini-MAP 2026-07-02)

**From:** claude.ai session, 2026-07-02. **Status:** analytic rulings; items 1–2 carry hand/CAS
derivations that OWE a blind adversarial pass on the workstation before the run banks anything
against them. Counting table in the mini-MAP must be corrected per Ruling 1 before implementation.

## Ruling 1 — P4: C2 is redundant for GEOMETRY only; it survives as ONE matter condition

CAS (this session): Legendre inversion of the geometry sector is nondegenerate and gives
`H_geo = π_φ²/(2Zρ²) − π_ρ² e^{2φ}/8 − 2` — a function of (φ, ρ, π_φ, π_ρ) ONLY. So field +
momentum continuity ⇒ [H_geo] = 0 automatically: the mini-MAP's redundancy intuition is right
for the geometry.

BUT H has a matter part. At the seal (natural BC f_r = 0) the cell side carries the winding's
angular energy `E_ang(r_s) = (ξ/2)(I_θ + N²I_s) + (κN²/2) I_4θ/ρ²`, which the ambient does not.
The Weierstrass–Erdmann corner condition [H] = 0 (forced because r_s is dynamical) therefore
reduces, given the four continuity matches, to ONE genuinely independent matter condition:

    E_ang,cell(r_s) = m_amb   — the ambient matter's H-contribution at the seal location.

Physical reading: the cell must impedance-match its skin's angular energy to the environment's
matter energy density — the ambient-density mechanism appearing a second time, now in the skin.

**Corrected count:** conditions = 2 (field) + 2 (momentum) + 1 (C2-matter) = 5.
- R_amb FREE: 4 unknowns vs 5 → over-determined by 1 → cells only at isolated ambient densities.
- R_amb FIXED: 3 vs 5 → over-determined by 2.
The mini-MAP's qualitative conclusion (Misner–Sharp band) SURVIVES AND STRENGTHENS, but the
mechanism is one notch stricter than the table stated. Consequence for the model ambient: it is
**five numbers, not four** — (φ_amb, ρ_amb, π_φ,amb, π_ρ,amb, m_amb); H_amb is then DERIVED as
H_geo(φ,ρ,π) + m_amb, never specified independently (over-specifying it is an inconsistency trap).

## Ruling 2 — Matched-boundary Derrick identity (adapted artifact filter)

The closed-cell scaling family violates the essential seal matches, so S_a = S_b does not carry
over. Evaluating dS/dλ|₁ on-shell against the boundary terms of the family
(φ_λ(r) = φ(r/λ), ρ_λ = λρ(r/λ), f_λ = f(r/λ,θ), endpoints → λr):

    S_a − S_b = −r_s H_s + π_ρ(r_s) ρ(r_s) + r_c H_c ,

with H conserved and matched (H_s = H_c = H_amb):

    **S_a − S_b + (r_s − r_c) H_amb − π_ρ(r_s) ρ(r_s) = 0.**

Check: closed cell (H = 0, π_ρ,s = 0) recovers S_a = S_b exactly. S_a, S_b as in Step-0 V6.
Tag: hand-derived, CAS/blind verification OWED on the workstation before use as a filter.

## Ruling 3 — Staging: model ambient FIRST (option ii), and the universe cell is not pre-doomed

Endorse (ii) → (i), with two riders:
1. **Scope note that dissolves the §4 alarm:** the N=1,2,3 negative is scoped to WINDING-matter
   cells. The universe cell is not one — it carries the theory's bulk matter content (N=0 /
   different matter sector) and sits at the F5 critical closure. The closed-cell runaway does
   NOT automatically apply to it; the universe solution is owed, not contradicted. The Machian
   reading stays: the universe may self-close precisely because its matter is not a winding knot.
2. **Model-ambient design:** scan ONE diagnostic axis — an ambient-density-like parameter —
   with the other four model numbers tied to it by a simple declared rule (a coarse P-interior
   profile), everything labeled MODEL. Deliverable plot: where cells exist along the axis, with
   the derived universe value marked later. Per Ruling 1, m_amb is part of the model data and
   part of the axis rule.

## Gate summary for implementation

1. Correct the mini-MAP count (over-by-1 free / over-by-2 fixed); model ambient = 5 numbers.
2. Blind-verify Rulings 1–2 (both are short CAS jobs) before the run banks against them.
3. Implement per mini-MAP §6 with the adapted Derrick identity above and the two-tier filter.
4. Report the closure structure along the ambient axis UNLABELED; isolated values, a continuum,
   or runaway-everywhere are all honest outcomes.
