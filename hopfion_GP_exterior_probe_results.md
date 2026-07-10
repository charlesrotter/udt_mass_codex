## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-10 |
| **Mode** | OBSERVE — bounded exterior probe on the REAL H3 field, per the FROZEN MAP `hopfion_GP_exterior_probe_MAP.md` (T1–T3 pre-registered before the run). |
| **Object** | H3 Q_H=1 hopfion ONLY (`prod_an256.npz` → shell-projected `h4_scripts/stress_rtheta_h3.npz`; r_tex≈3.9). NEVER the f2d π₂ hedgehog. |
| **Observing or targeting?** | OBSERVED the exterior readout class (plateau vs drift). NOT "show a mass." A drift/boxy outcome is a first-class result, not a patch target. |
| **Verifier status** | Built-in Branch-G control (source OFF) + **independent blind adversarial pass (agent af8aa37501f59c58c, 2026-07-10)**: CONFIRMED, drift is analytically-grounded, G plateau machine-exact, non-tautological, branch not decided. Two nuances folded in (§4). |
| **Build-on grade** | **BANKED (scoped characterization + clean negative on the static frame producing a localized mass).** Does NOT decide the branch; does NOT claim a mass. |

### Premise ledger

| Item | Tag |
|------|-----|
| Native Branch-P φ-eq Z(r²φ')' = 4e^{−2φ} + S(r) (round vacuum P-source ON) | **NATIVE** (2𝒦→φ; no G=8πT) |
| Branch-G control: same eq, vacuum source OFF (Z(r²φ')'=S) | **CONTROL** (source-free exterior) |
| S(r) = real H3 shell-projected transverse trace τ(r) | **REAL-FIELD PROXY** (exact −2𝒦 needs backreaction; result shown independent of S's shape — drift is vacuum-driven) |
| Z_φ ∈ {1,8}; φ_amb ∈ {0.3 … 12} | **FREE**, swept (regime table) |
| Regular core u(r_c)=0; r_c=0.05, r_max=80 (blind ext. to 1e5) | NATIVE regularity / category-A |

---

# H3 hopfion G/P exterior probe — RESULTS

## T1 — exterior readout class: **BOXY-P (drift) natively; PLATEAU only in Branch-G**

The SAME regular-core forward-integration, differing only by whether the round vacuum P-source is ON:

| Branch (vacuum source) | exterior flux q(r)=Z r²φ' | class |
|---|---|---|
| **P (4e^{−2φ} ON — native)** | **DRIFTS** monotonically (q(20 r_tex) ≈ 3–8× q(r_tex); →∞) | **boxy-P — no localized flux** |
| **G (source OFF — control)** | **PLATEAUS** (conserved to 13 sig figs) | localized conserved flux |

- **The P-drift is a theorem, not a numeric artifact:** dq/dr = 4e^{−2φ} (verified to ratio 1.00000 at
  r=50,200,1000), and φ stays finite (ψ grows only logarithmically) ⇒ the round vacuum source **never
  vanishes** ⇒ q grows without bound. This is the native "Branch-P has no asymptotic vacuum."
- **The test is NON-TAUTOLOGICAL** (unlike the retired q≡q): the same integrator gives machine-precision
  conservation for G and robust drift for P; the outcome is the exact ODE consequence of the source, not baked in.
- **The probe does NOT decide the branch.** It establishes the CONDITIONAL: P ⇒ drift (whole-cell), G ⇒
  plateau (localized). Which branch the hopfion occupies is the **underived G/P switch** — NOT inferred from
  topology (T3), NOT settled here.

## T2 — regime sensitivity (φ_amb, Z_φ)

- **Depth-INVARIANT drift:** every φ_amp (shallow 0.3 → deep 12) and Z_φ∈{1,8} DRIFTS in P; the relative
  drift q(5000)/q(80)≈62 is the same at φ_amb=3,5,8,12. Deeper ambient only shrinks the MAGNITUDE (via
  e^{−2φ_amb}), never restores a plateau. **No regime self-quenches to a clean flux.**
- Branch-G control plateaus in every regime (magnitude ~e^{−2φ_amb}).
- (Ambient depth is the real "background coupling" knob; here it moves the magnitude, not the class.)

## T3 — no topology→branch: satisfied
Classification is by large-r flux convergence (plateau vs drift), a property of the integrated ODE. Q_H is
never used to infer the branch. (STOP tripwire respected.)

## 4. Verifier nuances (folded in; neither breaks the conclusion)

1. **Finite-cell canon STRENGTHENS the whole-cell reading.** The drift is integrated over an unbounded
   exterior; per canon the physical exterior terminates at a finite wall/mirror. Capping at a wall does NOT
   restore a plateau — q climbs monotonically up to any finite wall — so "no localized mass" survives, and
   the finite-cell picture makes the whole-cell language sharper (q accumulates across the interior; a
   branch-honest readout evaluates q at the wall, still no plateau).
2. **The delocalization is a VACUUM-source property, not the soliton smearing.** In P, the soliton's OWN
   inner flux q(r_tex) is finite and localized; what spoils the plateau is the added distributed vacuum
   contribution 4e^{−2φ} on top. Read "non-localizable" as a statement about the total flux q, NOT "the
   hopfion itself smears out."

---

## What it means

- **The hopfion-mass question IS the G/P branch question — now measured, cleanly and non-tautologically.**
  In native Branch-P the exterior flux DRIFTS (whole-cell, cell-size/wall-dependent — the same "not a
  localized invariant" that CF2's box-control saw, now derived from a clean forward-integration on the real
  field rather than the parked transverse frame or a tautology). A clean, conserved, localized flux exists
  ONLY in Branch-G (source off).
- **The static reciprocal frame does not by itself produce a clean branch-honest mass.** It gives either
  boxy-P (native source on) or requires the underived G switch (source off) for a localized flux.
- **Consistent with the bedrock:** matter mass is not derivable from the static metric alone; here the static
  metric's own vacuum P-source is exactly what delocalizes the flux. Per the charter, the mass lane now routes
  to the SECONDARY (fixed-Q isorotation + metric DOFs beyond reciprocal / time structure) OR to settling the
  G/P switch — NOT to more static reciprocal probing.

## NOT claimed
- NOT: a mass, a sign, or a branch verdict. The probe shows P⇒drift, G⇒plateau; it does NOT decide which the hopfion is in.
- NOT: that the hopfion is massless (Branch-G would give a clean flux; the branch is undecided).
- NOT: that the hopfion smears out (its own inner flux is localized; the drift is the vacuum source).
- NOT: topology→branch (T3). NOT: a cherry-picked inner cutoff (classification is by large-r convergence). NOT: G=8πT.
