# S²-vs-S³ OBJECT IDENTITY (facet B) — Results

Date: 2026-06-19. Driver: Claude (Opus 4.8, 1M context). NEW file
(append-never-edit). Mode: **OBSERVE / DERIVE (symbolic-exact)** — the metric-led
algebraic settle of facet (B). **DATA-BLIND** — no particle mass, ratio, or wall
number loaded, computed, or compared (grep-confirmed: 0 hits). Governing MAP:
`S2_S3_OBJECT_IDENTITY_MAP.md`. **NOT canon.** Blind verifier: **PARTIAL — Part 2/3
independently re-derived and CONFIRMED by a blind agent (below); a fresh full blind
pass is invited in the ATTACK block.**

THE QUESTION (facet B, MAP §0): does the native L2+L4 action **SOURCE a 4th field
component** (⇒ the matter object is S³/π₃/SU(2)-Skyrme), or not (⇒ S², a unit
3-vector)? Facet (A) — the CHARGE carrier = S²/π₂ area form — is SETTLED (CANON
C-2026-06-14-1, #61) and is NOT re-opened.

THE TRIPWIRE (MAP §1, the prior failure): the earlier settle
(`fourth_component_sourced_results.md`) inflated "the EOM **permits** Θ=π/2 const"
into "the object **is** S²", and its verifier killed it. **Every "is" below rests on
a DEMANDS (necessity), shown explicitly; PERMITS-only steps are flagged.**

Scripts (commit-grade, this push; immutable):
- `s2_s3_identity_derive.py` — Part 1 (provenance fork: native cross-product L4 vs
  Lagrange-identity L4, per target dim) + Part 2/3 (n_4 EOM + source under the
  native action) + Part 4 (contrast under the non-native L4).
- `s2_s3_identity_stability.py` — L2/L4 decomposition of the n_4 source + the
  X-direction potential V(X) and its curvature (the DEMANDS test).
- `s2_s3_identity_texture.py` — texture (intrinsic vs embedding artifact) + the
  4-index/π₃ invariant audit.

---

## 1. THE VERDICT on (B): **S²** — the native action does NOT source a stable 4th component

The native matter object is the **unit 3-vector (S²)**. Stated as DEMANDS, three
independent necessity arguments, each sympy-exact:

### (i) STRUCTURAL necessity — the native L4 is intrinsically 3-component (a theorem)
The canonized native four-derivative term (`native_skyrme_derive.py`, CANON
C-2026-06-14-1) is built from the **3-vector cross product**
`S_mn = d_m n × d_n n` / `F_mn = n·(d_m n × d_n n) = eps_abc n_a d_m n_b d_n n_c`.
The cross product / `eps_abc` is defined for **exactly 3 internal components**; it is
STRUCTURALLY BLIND to any n_4 (n_4 appears nowhere in F or S). This is a theorem of
the operation, not a configuration choice.

Exact (`s2_s3_identity_derive.py` Part 1): the native (cross-product) L4 equals the
Lagrange-identity L4 **on a 3-vector** (`native − Lagrange = 0`, d=3), and for a
4-vector the native cross product is **undefined** (eps_abc is a 3-index symbol).
The ONLY L4 that "sees" n_4 is the **non-native Lagrange-identity form**
`(d_m n·d_p n)(d_n n·d_q n) − (d_m n·d_q n)(d_n n·d_p n)` — and even that, evaluated
with an n_4 added ORTHOGONALLY at fixed 3-vector amplitude, has `∂L4/∂n_4 = 0`
(verifier task D, confirmed): L4 only ever feels n_4 through the cos-X amplitude of
the 3-vector it acts on, never as an independent direction.

### (ii) DYNAMICAL necessity — no native source holds a finite n_4; the only n_4 motion DESTROYS the object
Write the most general unit 4-vector with a fully-live 4th-component angle X(r):
`n = (cosX·sinθ cos mψ, cosX·sinθ sin mψ, cosX·cosθ, sinX)` (X=0 ⇒ pure S²; X live ⇒
S³). Derive the X (= n_4) Euler-Lagrange equation from the angular-integrated native
radial action (`s2_s3_identity_derive.py` Part 2, `..._stability.py`):

- The **non-gradient source** (the X'=X''=0 part of EL[X]) is
  `∝ (2κ m² cos²X + ξ r²(m²+1))·e^{A+B}·sinX cosX / r²` — it VANISHES at X=0 (so X=0
  is a constant-X solution) but is NONZERO for X≠0.
- The X-direction **potential** is `V(X) = 2π(κm²cos²X + ξr²(m²+1))·e^{A+B} cos²X /r²`,
  with `dV/dX|_{X=0}=0` and **`d²V/dX²|_{X=0} = −4π(2κm² + ξr²(m²+1))·e^{A+B}/r² < 0`**
  (all of ξ,κ,m,r,e^{A+B} > 0). So **X=0 is a potential MAXIMUM**, and
  **`d²V/dX²|_{X=π/2} = +4π ξ(m²+1)·e^{A+B} > 0`** is the MINIMUM.

THE DEMANDS-LEVEL READING (this is the tripwire crux, and it cuts AGAINST naive S²
"it permits X=0" too — so I state it carefully): X=0 being an *unstable* maximum does
NOT mean n_4 is a sourced new DOF. The downhill direction is X: 0 → π/2, at which
`n = (0,0,0,1)` — the **trivial constant map**: the 3-vector amplitude is `|cosX|`,
which → 0, so the (θ,ψ) winding COLLAPSES TO A POINT and the S² winding charge
(density ∝ cos³X, integral 4πm → **0**, verifier task C, exact) is DESTROYED. This is
the textbook global-monopole / O(4) σ-model **unwinding instability**: the only way
the action moves n_4 off zero is to ANNIHILATE the object's own charge, not to
nucleate a stable S³ soliton. **A charge-preserving deformation to a finite-n_4 (S³)
object is NOT sourced; the action DEMANDS that any charged matter live at n_4 = 0
(S²), and holding a finite n_4 requires IMPOSING it externally (a boundary
condition).** Necessity, not permission: there is no native term that stabilizes a
finite n_4 against either rolling back to S² or collapsing to vacuum.

### (iii) SYMMETRY necessity — the metric supplies no S³ isometry / no π₃-protecting field
`#50` (su3_field_test, blind-verified): the metric connection is U(1)×SO(3)×SO(3,1).
The only internal rotation the METRIC supplies is the **SO(3) = Isom(S²)** acting on
the 3-vector. There is NO metric-supplied SU(2) = Isom(S³). So even the symmetry that
would protect/source a π₃ object is natively absent.

> **VERDICT: facet (B) = S².** Three independent necessities (structural, dynamical,
> symmetry) each DEMAND the unit 3-vector. There is NO fork: the action does not
> admit a stable S³ branch — the apparent S³ "branch" is the unstable unwinding to
> vacuum, not a particle. P2's matter field is S² (a unit 3-vector n_a).

---

## 2. PROVENANCE (OI-import): is S³ ever NATIVE? — **No. S³ is ALWAYS imported.**

Every place "S³ / π₃ / SU(2) / Skyrme / baryon" enters the matter sector is an
import, traced exactly (this push + the prior provenance audit
`theta_bc_provenance_results.md`, blind-verified STANDS):

- **The native current is uniquely S²/π₂.** `F_mn = eps_abc n_a d_m n_b d_n n_c` uses
  a **3-index** epsilon ⇒ a 3-vector target (h1_types, CANON C-14-1). A π₃/baryon
  current needs a **4-index** `eps_abcd` (the Wess–Zumino/baryon 3-form). The native
  field has only 3 independent internal directions (the 4th is unsourced, §1(ii)), so
  `eps_abcd` has no native field to act on — it is identically zero on the native
  field (`s2_s3_identity_texture.py` Part B). There is NO native 4-index / π₃
  invariant; only the 3-index area form. (CANON addendum and #47c/hopf_spinor agree:
  L2+L4 contains no native WZW/Hopf π₃ term.)
- **The S³ "DERIVED" tag was unearned (#61).** The catalog's S³ carrier and its
  m=1,2,3 index come ENTIRELY from the radial Skyrme BC `Theta(core)=m·π,
  Theta(seal)=0` (`spectral_radial_soliton.py:141`, the only m-dependence in the
  radial solver), self-tagged "CHOSE / the charge-1 hedgehog choice"
  (`native_stabilizer_results.md:244-249`), and NOT derived from the seal/junction
  (which constrains metric/dilation only — the dpf "Theta" is the metric 2-form, a
  resolved naming collision). The Lagrange-identity L4 "valid for any target dim" is
  arithmetic, not a sourcing argument (§1(i)).
- The S³ object therefore exists ONLY when the non-native Lagrange-identity L4 is
  paired with the imported `Theta(core)=m·π` BC. Both are imports.

> **PROVENANCE: S³ is never metric-derived; it is always carried in via (a) the
> Lagrange-identity L4 and (b) the Skyrme baryon BC. The native target is uniquely
> S²/π₂.**

---

## 3. TEXTURE (OI-texture): **the cos θ texture is an ARTIFACT of the non-unit mψ embedding, not intrinsic.**

`s2_s3_identity_texture.py` Part A, sympy-exact:
- The embedding that produced the texture,
  `n = (sinΘ sinθ cos mψ, sinΘ sinθ sin mψ, cosΘ)`, is **NOT a unit field**:
  `|n|² = cos²θ cos²Θ − cos²θ + 1 ≠ 1` off the equator. Its `T^θ_θ` carries cos θ —
  but it is not even a map to S² (the amplitude varies with θ). The texture is an
  artifact of this non-unit chart.
- The genuine native UNIT deg-1 hedgehog (the CANON pure topological carrier,
  `n = x/r = (sinθ cos mψ, sinθ sin mψ, cosθ)`, `|n|² = 1` EXACTLY for all θ) has:
  `T^θ_θ = (κm² − m²r²ξ + r²ξ)/(2r⁴)` — **NO θ-dependence** (texture-free), and
  `T^t_t = T^r_r` EXACTLY (the CANON C-14-1 B=1/A relation holds).

> **TEXTURE: an embedding artifact (non-unit mψ chart), not intrinsic to the native
> S² object. The genuine unit S² hedgehog is texture-free and B=1/A-consistent.**

---

## 4. r→0 (OI-core): **honestly SCOPED — does not change the (B) verdict.**

The strict-origin reach is UNRESOLVED at the level of a committed derivation
(`theta_bc_provenance_results.md`: `r_core=0.05` is `[CHOSEN]`; CANON C-2026-06-10-2's
φ→−∞ core is never reached by the finite-depth solves). HOWEVER, per the prior blind
verifier's sharpened Axis C, r=0 regularity forces only `sin Θ(0)=0` — a NODE
satisfied by Θ(0)∈{0,π,2π,…} EQUALLY; it selects neither the value nor an m-ladder.
Crucially for facet (B): the r→0 argument is about whether a RADIAL Θ-sweep is forced
for regularity of the *non-unit / S³* texture; it does NOT manufacture a native
**independent** n_4 DOF, and the native UNIT hedgehog (§3) has `T^t_t=T^r_r` finite
structure with no r→0 texture pathology of its own. So r→0 affects only the m=1
endpoint of the (already-imported) Skyrme profile; it does not rescue S³ and does not
disturb the S² verdict of §1.

> **r→0: scoped open as a physical fact, but DECOUPLED from facet (B). It can only
> affect the imported Skyrme profile's endpoint, never source a native n_4.**

---

## 5. TRIPWIRE SELF-CHECK (every "is" rests on a DEMANDS)

| Assertion | Rests on | DEMANDS or PERMITS? |
|---|---|---|
| native L4 is 3-component | cross product / eps_abc is a 3-index operation (theorem) | DEMANDS (structural necessity) |
| L4 blind to n_4 | `∂L4/∂n_4 = 0` exactly, n_4 orthogonal at fixed amplitude | DEMANDS |
| no stable finite-n_4 object | `d²V/dX²|_{X=0}<0` AND the only downhill (X→π/2) DESTROYS charge (4πm→0) | DEMANDS (no native term stabilizes finite n_4; necessity, not "X=0 permitted") |
| object is S² | (i)+(ii)+(iii) jointly: no native 3rd-DOF source, no S³ isometry, no 4-index invariant | DEMANDS |
| texture is artifact | the mψ embedding is non-unit (`|n|²≠1`); the unit hedgehog is texture-free | DEMANDS (exact) |
| S³ always imported | no native eps_abcd; the BC self-tagged CHOSE; seal derives metric only | DEMANDS (absence-of-derivation, exhaustive over candidate routes) |

**Flag (honesty):** the ONE place I cannot reach pure necessity is the PHYSICAL r→0
fact (§4) — but it is decoupled from (B) (it cannot source a native n_4), so the (B)
verdict does not depend on it. I explicitly did NOT repeat the prior inflation: the S²
verdict is NOT "the EOM permits X=0" (that alone would be a PERMIT); it is "no native
term sources or stabilizes a finite n_4, and the only n_4 motion annihilates the
object" (a DEMANDS).

**Anti-inflation note (the symmetric guard):** I also checked the OPPOSITE inflation —
"X=0 is unstable ⇒ n_4 IS sourced ⇒ S³." That is REFUTED: the instability is the
charge-destroying σ-model unwinding to the trivial vacuum, not the nucleation of a
stable S³ DOF (verifier task C, charge 4πm→0 exact). Neither inflation survives;
the clean reading is S².

---

## 6. HONEST AUDIT

- **Imported algebraic object?** YES — and NAMED as the import, not used as native:
  the S³/π₃/Skyrme structure (Lagrange-identity L4 + `Theta(core)=m·π` BC). The native
  objects used (eps_abc area form, L2, the 3-vector cross-product L4) are all CANON /
  blind-verified native. I did NOT bank any S³ object as native.
- **Shortcut / slice?** The angular (θ,ψ) integral was done EXACTLY (sympy), not
  approximated; no linearization (Principle 2 clean — the curvature signs are exact).
  The "whole" of facet (B) was addressed: I did not declare from one corner — I tested
  the fully-general live 4th component, both L4 forms, both embeddings, and both
  inflation directions.
- **Data-blind?** CONFIRMED (grep: 0 mass/ratio/wall numbers in any script or this
  doc; sizes only in L = √(κ/ξ) units, and even those not numerically evaluated).
- **Metric-led?** YES — the question asked "what target space does the native action
  DEMAND?", answered from the action; not catalog-driven, not verdict-hunted.

---

## PREMISE LEDGER (this settle)

| # | Choice | CHOSE / DERIVED | Note |
|---|---|---|---|
| native action L2+L4 | the cross-product (eps_abc) L4 of CANON C-14-1 | DERIVED (canon) | the genuinely native L4; the Lagrange-identity form is the import, shown ≠ native for d>3 |
| metric form | ds² = −e^{2A}dt² + e^{2B}dr² + r²dΩ², A,B free (B=1/A NOT pre-imposed) | DERIVED (relativistic-foundation CANON C-18-1) | B=1/A emerges (§3), not assumed |
| field ansatz | unit 4-vector with X(r) live | DERIVED-general | most general 4th-component sweep; not a slice |
| static / round | static, axisymmetric hedgehog | CHOSE (scope) | facet (B) is a target-space question, settled at the round level where the carrier is defined; the time-live solve does not re-open which TARGET the field maps to |
| r_core | finite cutoff in committed solves | CHOSE (flagged) | §4: decoupled from (B) |

---

## ATTACK HERE (for a fresh blind verifier)

1. **Re-derive the n_4 EOM source independently** (your own parametrization of the
   live 4th component — e.g. n_4 = Y(r) added orthogonally rather than the X-angle).
   Confirm/refute: (a) no native term sources an INDEPENDENT n_4; (b) the X-direction
   potential has `d²V/dX²|_{X=0} < 0` and `|_{X=π/2} > 0`; (c) the downhill roll
   X→π/2 sends the S² charge 4πm → 0 (charge-destroying), so the instability is
   unwinding-to-vacuum, NOT S³-nucleation. (A prior blind agent confirmed all three —
   re-do from scratch.)
2. **Attack the structural claim** that the native L4 (cross product) is blind to
   n_4. Exhibit ANY native four-derivative term built from the metric + the unit field
   that DOES source an independent n_4 without importing the Lagrange-identity form or
   a WZW/Hopf π₃ term. If none exists, §1(i) stands.
3. **Attack the texture verdict.** Confirm the mψ embedding `(sinΘ sinθ cos mψ, …)` is
   non-unit (`|n|²≠1`) and that the genuine unit hedgehog `n=x/r` has θ-independent
   `T^θ_θ` and `T^t_t=T^r_r`. If a UNIT S² embedding carries an intrinsic θ-texture,
   the artifact verdict is wrong.
4. **Attack the provenance.** Find ANY committed line where a native eps_abcd / π₃ /
   WZW invariant is DERIVED from the metric (not imported). If one exists, S³ may be
   native after §1's dynamical argument and the verdict moves to FORK.
5. **Tripwire double-check (both directions).** Confirm the S² verdict rests on
   DEMANDS (no native source/stabilizer for finite n_4 + charge-destroying roll), NOT
   on "EOM permits X=0". AND confirm I did not commit the OPPOSITE inflation
   ("unstable ⇒ S³"). Was S² steered, or derived from absence-of-source?
