# D1 — Charge-channel projection MAP: is q=1/3 the single-channel projection of Q_H=1 through the N=3 carrier? (and η=½q²?)

**Mode:** clean-room MAP that DERIVES-OR-REFUTES a specific hypothesis (armchair + CAS; NO PDE
solve; DATA-BLIND — no lepton masses, no observational numbers touched). This TESTS a hypothesis
Charles proposed (2026-07-05, post-hopfion) — per **hypothesis discipline** the confirming reading
is attacked HARDEST and **refutation is a welcome, first-class outcome**. Per the **anti-targeting
rule** the readout/normalization is derived NATIVELY from the carrier and REPORTED as-is; the
numbers 1/3 and 1/18 were NOT reverse-engineered or targeted.

**Driver:** Claude (Opus 4.8, 1M context), 2026-07-05.
**Status: BANKED — BLIND-VERIFIED (verifier a5cf5a27f637302df, 2026-07-05: OVERALL HOLDS, sound + honest +
non-targeted; verdict correct on all three prongs). Attack 1 (confirmation-flip) independently confirmed NO
native anisotropy-free charge functional returns 1/3 ⇒ hypothesis NOT confirmed, refutation honest (consistent
with the parent D1 audit). Attack 5 anti-targeting/data-blind PASS (CAS carries q,Z,ρ_s free; 1/3,1/18 only as
end-checks). Three sharpening corrections folded in — see the ★VERIFIER CORRECTIONS below and §2.1/§3/§7.**
CAS: `d1_charge_channel_projection_cas.py` (sympy, exact, bounded, no solve — all prints reproduced inline).

**Allowed current-framework inputs (each cited):** the native carrier n_a (|n|=1, target S²; winding
density ω_H1 = ε_abc n_a dn_b∧dn_c) — CANON C-2026-06-14-1, `angular_lagrangian_results.md:37-51`;
the Whitehead/Hopf identity Q_H=∫A∧dA ∈ π₃(S²)=ℤ — `node_H2_charge_ledger_results.md`; the End(H1)=1+3+5
algebra + its "ONE operator space, not a set of cells" caveat — `particle_spectrum_native_geometry.md`,
`archive/B2_phi_angular_spectrum_results.md:58`; the isotropy chain ⟨n_a n_b⟩=δ_ab/3 and the η chain
— `negative_phi_native_geometry.md` §§111,124,125; the derived seal energy U_seal=2−q²/(2Zρ_s²) —
`d1_angular_constants_native_rederivation.md:311` (verifier steel-man S2). The **D1 provenance audit**
(`d1_angular_constants_native_rederivation.md`) is the immediate parent: q=1/3 and η=1/18 there = IMPORT-DEPENDENT
via the COLLAR route (s=1/9 + superseded operator); this MAP tests a DIFFERENT route (channel projection).

---

## 0. THE HYPOTHESIS, STATED WHOLE (Charles, 2026-07-05)

The native hopfion has integer identity **Q_H = 1** (Hopf/Whitehead invariant) — established
(`node_H2`). The historical q=1/3 is NOT a Hopf topological charge. The hypothesis: q=1/3 MAY be the
**PUBLIC SINGLE-CHANNEL PROJECTION** of the unit Hopf identity through the native N=3 carrier —

>  Q_H = 1,  w₁ = w₂ = w₃,  Σᵢ wᵢ = 1   ⟹   q = wᵢ = 1/3,

and the historical η=1/18 MAY be the native **quadratic response** η = ½q² (since ½·(1/3)² = 1/18).

Three quantities are kept **DISTINCT throughout** (no back-solve from Q_H to q or η):
- **Q_H** — integer Hopf self-linking identity ∈ π₃(S²)=ℤ. Provenance: **DERIVED** (Whitehead integral, `node_H2`).
- **q** — possible public channel fraction. Provenance under test.
- **η** — possible quadratic response / boundary coupling. Provenance under test.

---

## 1. PRE-REGISTERED CLEAN FAILURES (FROZEN before the verdict)

- **CF-A:** q=1/3 requires CHOOSING a channel by hand (no native selector).
- **CF-B:** the native readout gives q=1 (the full unit), not 1/3.
- **CF-C:** the three-channel split is merely NOTATION (the End(H1) triplet), not a physical charge split.
- **CF-D:** η ≠ q²/2 under the exact UDT quadratic form (the ½ is not native).
- **CF-E:** q and η depend on an UNANCHORED normalization (not dimensionlessly forced).
- **CF-F (found here):** the equal-thirds partition exists but the SELECTION of one channel breaks the
  target SO(3) isometry the Lagrangian is invariant under — i.e. it needs the anisotropic potential
  V_ab n_a n_b (V ≁ δ) the corpus flags "explicitly not native yet" (`negative_phi:8496`).

---

## 2. TASK 1 — Is there a NATIVE three-equal-channel structure? (the (i)-vs-(ii) distinction)

**The load-bearing distinction** (Charles's ★): are the "three channels"
- **(i)** three copies / SO(3) isotropy of the unit vector's COMPONENTS (⟨n_a n_b⟩=δ_ab/3) — a
  *physical* charge distribution, which WOULD support the projection; or
- **(ii)** merely the 3-piece of End(H1)=1+3+5 (the operator-space triplet) — a *different object*
  which makes the split "merely notation" (⇒ CF-C).

### 2.1 Result — reading (i) EXISTS and is native (CAS, exact)

**★ VERIFIER CORRECTIONS (a5cf5a27f637302df) folded in:** (1) the two computations below are NOT independent
— they are the **same object, two equivalent readings**: since for maps into S² one has ∂_θn×∂_φn = w·n with
w=sinθ the round measure, the per-axis winding share ∫ w n_a² dθdφ = ∫ n_a² dΩ, so (b) = 4π·(a). (2) The
equal-thirds is **STRONGER than hedgehog-specific: it is a TOPOLOGICAL INVARIANT of the whole degree-1 class**
(∫ w n_a² = deg·⟨n_a²⟩_target·4π = 4π/3 for ANY degree-1 map, verified on a squashed profile) — this
strengthens the confirming half. (3) The value 1/3 is itself **frame-INVARIANT** (each target axis carries
exactly 1/3 in every SO(3) frame — Monte-Carlo-confirmed); what lacks a native origin is a public COUPLING to
one axis, not the value — see the §3 wording fix.

One native object, read two equivalent ways, gives an **exact equal-thirds structure**:

**(a) SO(3) isotropic second moment** (round-S² forced, `negative_phi:7779`):
```
<n_a n_b> = ∫ n_a n_b dΩ / ∫ dΩ = diag(1/3, 1/3, 1/3),   trace <|n|²> = 1.
```
The unit constraint |n|²=1 distributes isotropically as **1/3 + 1/3 + 1/3 = 1** across the three
target components. This is w₁=w₂=w₃=1/3, Σ=1 — literally the hypothesis's arithmetic, forced by
isotropy (NOT a chosen label split; `negative_phi:7796`).

**(b) Per-target-axis partition of the UNIT WINDING** (new here — the sharper test). The winding
density n·(∂n×∂n)=sinθ (total 4π, degree 1) decomposes over the target axes as
n·(∂n×∂n) = Σₐ nₐ(∂n×∂n)ₐ. Each channel integrates to **exactly one third**:
```
∫ n_a (∂n × ∂n)_a  = 4π/3  for a=1,2,3   (each = degree 1/3),   Σ_a = 4π (= degree 1).
```
So the **degree-1 winding itself splits into three exactly-equal channels summing to the unit** —
not just the static second moment, but the topological winding density. This is a genuine
equal-thirds partition of Q_H's underlying π₂ degree.

### 2.2 Which reading is it — (i) or (ii)?

Both (a) and (b) are reading **(i)**: they are the SO(3) isotropy of the carrier's own unit VALUES /
winding density, forced by the round S² metric. They are NOT the End(H1) antisymmetric-triplet (ii)
(that "3" is operators on the carrier, the object the corpus flags as "a decomposition of ONE
operator space, not a set of distinct cells", `B2:58`). The η-chain the corpus actually uses rides
⟨n_a n_b⟩=δ_ab/3 (i), never the operator triplet.

**→ CF-C DID NOT FIRE.** The three-channel split is a physical isotropic charge distribution
(reading (i)), not the End(H1) notation. **This is the confirming half of the hypothesis: the native
equal-thirds structure Σ=1 is real.** Charles's proposed w₁=w₂=w₃, Σ=1 has a genuine native home.

---

## 3. TASK 2 — Does a public charge readout SELECT one channel (→1/3) or read the full Q_H=1?

This is the decisive task. Three native readouts (CAS TASK-A/E):

| Readout | Native object | Value | Character |
|---|---|---|---|
| Degree | (1/4π)∫ω_H1 | **1** | scalar, FULL unit |
| Hopf Q_H | ∫A∧dA (Whitehead) | **1** (integer) | scalar, FULL unit |
| Single channel | ∫nₐ(∂n×∂n)ₐ /4π | **1/3** | requires SELECTING one target axis |

The two genuinely-native *charge* readouts (degree, Hopf) are **SCALARS = the full sum = 1**. The
equal-thirds partition of §2.1(b) is a real *partition of that one unit* into three bookkeeping
shares — but the observable (total winding / self-linking) is the **sum**, which is 1. Nothing in the
readout structure forces the "public" charge to be one share rather than the sum.

To read q=1/3 you must **single out one of the three channels**. ★ **Wording fix (verifier):** the VALUE 1/3
is frame-INVARIANT (each axis carries 1/3 in every SO(3) frame — §2.1 correction 3), so "1/3" itself does NOT
break the isometry. What has no native origin is a **public field COUPLING to a single target axis**: by
isotropy no axis is distinguished (the three are related by the **target-SO(3) isometry the Lagrangian is
invariant under**, `angular_lagrangian_results.md:64`), and selecting one as "the public channel" requires an
**anisotropic selector** V_ab n_a n_b with V ≁ δ_ab, which the corpus states is "explicitly not native yet"
(`negative_phi:8496`). So the refutation is: no native coupling reads one channel; the observable is the
scalar sum = 1. The easy-axis form n₃=cosΘ(r) that would do it was already flagged a
"gauge/orientation choice … ansatz-dependent, not native" (`archive/n3_direction_distribution_results.md:265`).

**→ CF-B FIRED.** The natural/native readout gives **q = 1** (the full unit), not 1/3.
**→ CF-A FIRED.** Reaching 1/3 requires CHOOSING one of three isotropically-equivalent channels; no
native selector picks it.
**→ CF-F FIRED.** The selection breaks the target SO(3) the action respects (needs the non-native
anisotropic V_ab).

**Honest verdict on the readout:** the hypothesis's *structure* is native (§2, CF-C clear) but the
*projection to 1/3 is not forced* — the native scalar charge readout is **1**. q=1/3 is one chosen
share of a real equal-thirds partition, not a forced public charge.

---

## 4. TASK 3 — Is the ½ in η=½q² present in the EXACT native quadratic form?

Keeping every factor explicit (CAS TASK-D; Z, ρ_s kept symbolic — no anchoring assumed):

**Native ½ candidates (all real):**
- L2 kinetic normalization **ξ/2** in E=∫[(ξ/2)|∂n|²+(κ/4)F²] (`node_H3_hopfion_solve_results.md:48`) — native.
- Derived **seal energy** U_seal = 2 − **q²/(2Zρ_s²)** (`d1_...:311`, D1 verifier steel-man S2) — a
  DERIVED object, quadratic in q, carrying a **½**.
- The interface budget B = ΔK·R = **p/2** (`negative_phi:7796`).

So the **½ itself IS native** — it is not the postulated "quadratic action normalization ½" of the
legacy 1/(2N²) route in isolation; genuine native ½'s exist.

**But does the exact object equal ½q²?** Two routes:

*(a) Interface chain* (`negative_phi_native_geometry.md` §124): η = B·(isotropy) = (p/2)·(1/3). With p=q this is q/6, and
it equals **q²/2 only if the isotropy factor 1/3 is identified with q** (true at q=1/3, giving 1/18).
That identification IS the Task-2 channel question — so this route's ½ is real but its "=½q²" rides
q=1/3 being a channel share, which §3 showed is unforced.

*(b) Native seal energy*: the exact quadratic coefficient is **q²/(2Zρ_s²)**. CAS: this equals ½q²
**iff Zρ_s² = 1**. The normalization Zρ_s² is UNANCHORED — D1's verifier records U_seal spanning
0.052–0.671 across families (q and Zρ_s² both vary; `d1_...:311`). So the exact native quadratic-in-q
object is q²/(2Zρ_s²), which reduces to ½q² only under an unanchored normalization choice.

**→ CF-D DID NOT FIRE.** The ½ IS native (ξ/2 kinetic; U_seal's /2) — the ½ is not a bare postulate.
**→ CF-E FIRED.** η=½q² *exactly* requires Zρ_s²=1, an UNANCHORED modulus (q=Zρ_s²φ' is itself a
free OUTPUT, `d1_...:153`; charge normalization = unpinned modulus, `F7:196`). The identity is
conditional on a normalization the framework does not force to 1.

---

## 5. TASK 4 — Q_H / q / η provenance ledger (kept DISTINCT; no back-solve)

| Object | What it is | Provenance TAG | Value this MAP supports |
|---|---|---|---|
| **Q_H** | integer Hopf self-linking ∫A∧dA | **DERIVED** (Whitehead, `node_H2`) | **1** (integer, full) |
| **q** | public channel fraction | **REFUTED-as-forced / CONDITIONAL** — native equal-thirds partition EXISTS (reading (i)) but the readout gives the FULL 1; 1/3 needs a hand-chosen channel (CF-A/B/F) | native readout = **1**; 1/3 = one chosen share |
| **η** | quadratic response / boundary coupling | **CONDITIONAL** — the ½ IS native (CF-D clear); η=½q² rides Zρ_s²=1 UNANCHORED (CF-E) AND the q=1/3 channel identity (CF-A/B) | q²/(2Zρ_s²); = ½q² iff Zρ_s²=1 |

No step reads a value backward from Q_H into q or η: Q_H=1 is the scalar; the equal-thirds is a
partition of it; q=1/3 would be one share BUT is not forced; η rides q plus an unanchored modulus.

---

## 6. PER-CF VERDICTS (frozen list §1)

| CF | Verdict | Evidence |
|---|---|---|
| **CF-A** (channel chosen by hand) | **FIRED** | native readouts are isotropic; no selector picks one of three SO(3)-equivalent channels (§3) |
| **CF-B** (readout gives 1) | **FIRED** | degree=1, Hopf Q_H=1 — both scalar, FULL unit (CAS TASK-A/E) |
| **CF-C** (merely End(H1) notation) | **DID NOT FIRE** | the split is the SO(3) isotropy ⟨n_a n_b⟩=δ_ab/3 AND the per-axis winding 4π/3 (reading (i)), a physical distribution — NOT the operator triplet (§2.2) |
| **CF-D** (½ not native) | **DID NOT FIRE** | native ½ in ξ/2 kinetic and in U_seal=2−q²/(2Zρ_s²) (§4) |
| **CF-E** (unanchored normalization) | **FIRED** | q=Zρ_s²φ' is a free OUTPUT; η=½q² needs Zρ_s²=1, unpinned (§4) |
| **CF-F** (selection breaks target SO(3)) | **FIRED** | singling out one channel needs anisotropic V_ab ≁ δ, "not native yet" (§3) |

---

## 7. DERIVED-vs-OPEN-vs-REFUTED SUMMARY

**q (public channel fraction):**
- **DERIVED (native, new — and STRONGER than first stated, per verifier):** a three-equal-channel
  structure w₁=w₂=w₃=1/3, Σ=1 EXISTS natively — the round-S² isotropy ⟨n_a n_b⟩=δ_ab/3 and the
  per-target-axis partition of the degree-1 winding are ONE object (∫n_a²dΩ, via ∂_θn×∂_φn=w·n), and
  it is a **TOPOLOGICAL INVARIANT of the whole degree-1 class** (4π/3 per axis for ANY degree-1 map,
  not hedgehog-specific), with the value 1/3 **frame-invariant**. This is reading (i), physical, not
  End(H1) notation. **Charles's structural intuition is confirmed at this level — the equal-thirds
  partition of the unit is real, robust, and topological.**
- **REFUTED as a forced value / OPEN as a public charge:** q=1/3 is NOT what a native charge readout
  returns. The native scalar readouts (degree, Hopf) give the FULL **1**. Getting 1/3 requires
  selecting one of three isotropically-equivalent channels — a hand choice that breaks the target
  SO(3) isometry (CF-A, CF-B, CF-F fired). So **q=1 natively; 1/3 = one chosen share of a real
  equal-thirds partition, not a forced projection.** The missing native link is exactly a *selector*
  that makes one channel "public" without an imported anisotropy — none exists in the derived
  condition set (D1 verifier S3: "the isotropic share is native but no share-closure exists").

**η (quadratic response):**
- **DERIVED (native):** the ½ is native (ξ/2 kinetic; U_seal's /2) — CF-D cleared. A quadratic-in-q
  seal object with a ½ genuinely exists.
- **CONDITIONAL / not forced:** η=½q² *exactly* requires (i) the q=1/3 channel identification (which
  §3 shows is unforced) AND (ii) Zρ_s²=1, an UNANCHORED normalization (CF-E fired). The exact native
  quadratic coefficient is q²/(2Zρ_s²), not ½q², until the modulus is pinned.

**Bottom line:** the hypothesis correctly identified a REAL native structure (equal thirds, Σ=1, a
genuine isotropic partition of the unit charge — better than "mere notation", CF-C cleared, and
better than D1's collar route which needed s=1/9). But it does NOT close the gap: the native readout
gives **q=1**, and q=1/3 still requires a channel selector the metric does not natively supply, while
η=½q² additionally rides an unanchored modulus. **The projection is a real structure without a native
projector.** Q_H=1 stands; q=1/3 and η=1/18 remain not-natively-forced (a DIFFERENT, cleaner failure
mode than D1's import chain — here the *arithmetic* is native but the *selection/normalization* is not).

---

## 8. PREMISE LEDGER (chose / derived / import tags)

- Carrier class (unit-vector n_a, target S²): **THEORY** (C-2026-06-14-1; blind-verified anchor).
- Round/spherical S² frame (isotropy ⟨n_a n_b⟩=δ_ab/3): **CHOSE + canonized** (C-2026-06-18-1 four-choices).
- Hedgehog degree-1 map n=x/|x|: **DERIVED** (deg-1 representative, `angular_lagrangian_results.md:49`).
- Per-axis winding partition (4π/3 each): **DERIVED here** (CAS, exact; no target used).
- Whitehead Q_H=1 integer: **DERIVED** (`node_H2`; π₃(S²)=ℤ).
- Interface budget B=p/2; seal energy U_seal=2−q²/(2Zρ_s²): **DERIVED objects** cited from the seal
  machinery / D1 verifier — used to test the ½, NOT re-derived here.
- q=1/3, η=1/18 as VALUES: **NOT targeted** — the CAS carries q, Z, ρ_s as SYMBOLS; 1/3 and 1/18
  appear only as substitution CHECKS at the end, never as inputs to a solve.
- Z, ρ_s (seal normalization): **UNANCHORED modulus** (free output) — the CF-E hinge.

---

## 9. FOR THE VERIFIER / ATTACK SURFACE

Load-bearing steps, attack hardest (hypothesis discipline — attack the CONFIRMING readings first):

1. **The (i)-vs-(ii) call (§2.2) — is the equal-thirds really physical, or did I dress the End(H1)
   triplet as isotropy?** Attack: is ⟨n_a n_b⟩=δ_ab/3 (i) genuinely distinct from the 3-piece of
   End(H1) (ii)? Both are "3"; confirm the η-chain and the winding partition use the VALUE second
   moment / winding density, not operators on the carrier. If they secretly coincide, CF-C should
   re-fire.
2. **The per-axis winding partition (§2.1b) — is each channel really 4π/3, basis-independently?**
   The 4π/3 is computed in the standard target frame. Attack: is the *equality* of the three shares
   frame-independent (isotropy) while the *identity of a single share* frame-DEPENDENT? Re-run in a
   rotated target frame; confirm the three stay equal (isotropy, real) but no single one is
   distinguished (⇒ CF-A/F). If a native frame IS distinguished, CF-A could clear and the hypothesis
   would strengthen — this is the single most important attack.
3. **Does ANY native readout FORCE 1/3?** I claim degree and Hopf both give the full 1 and only a
   hand-selected channel gives 1/3. Attack: is there a native charge functional (a flux through one
   coordinate 2-cell, a per-generator holonomy, a projected Whitehead integral) that returns 1/3
   *without* an imported anisotropy? If yes, CF-B fails and the hypothesis is confirmed. Grep the
   derived seal/flux record for any single-component charge readout.
4. **The seal-energy ½ (§4) — is q²/(2Zρ_s²) the RIGHT exact object, and is Zρ_s²=1 truly unforced?**
   Attack: re-derive U_seal's quadratic coefficient from the junction conditions; check whether any
   derived condition pins Zρ_s² (if Zρ_s²=1 is forced, CF-E fails and η=½q² is native modulo the q
   question). Confirm the ξ/2 and U_seal ½'s are the SAME ½ or two different ones.
5. **Anti-targeting audit:** confirm the CAS carries q/Z/ρ_s as free symbols and that 1/3, 1/18 enter
   only as end-of-run substitution checks — never as inputs. Confirm data-blindness (no lepton/hadron
   number anywhere).
