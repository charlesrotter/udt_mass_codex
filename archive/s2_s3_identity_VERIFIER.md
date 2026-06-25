# BLIND ADVERSARIAL VERIFIER — S²-vs-S³ object identity (facet B)

Verifier: claude-opus-4-8[1m] (independent blind adversarial). Date: 2026-06-19.
DATA-BLIND (no lepton/mass/ratio/wall numbers loaded or computed; grep-confirmed
the only hits in the target files are the meta-word "mass/ratio/wall" in prose).
Target: `s2_s3_identity_results.md` + scripts `s2_s3_identity_derive.py`,
`s2_s3_identity_stability.py`, `s2_s3_identity_texture.py`. All three scripts run
and reproduce their documented output. Independent re-derivation done from my own
sympy (different parametrization where possible: n_4 = Y(r) orthogonal, amp=√(1−Y²)).

NET VERDICT: **the S² settle STANDS. "No fork" is correct.** No stable finite-n_4
(S³) configuration exists in the physical domain under the native (or even L4-only)
action; the only n_4 motion is charge-destroying unwinding to vacuum. ONE secondary
sub-claim is FALSE (a sympy assumptions bug, Part-1 d=4 print) but it is NOT
load-bearing — see below. No imported algebraic object is banked as native.

---

## TRIPWIRE RULING (both directions)

- **Direction 1 (permits→is inflation):** AVOIDED. The S² verdict is a genuine
  DEMANDS, not a dressed-up permit. I independently confirmed (a) no native term
  sources an independent n_4 (source vanishes at n_4=0), (b) the n_4=0 point is a
  potential MAXIMUM, and (c) the ONLY critical points off zero lie at |Y*|>1
  (OUTSIDE the unit ball |n_4|≤1) — so inside the physical domain Y∈[−1,1] the only
  critical point is Y=0, and V decreases monotonically toward the boundary |Y|=1,
  i.e. toward the trivial vacuum n=(0,0,0,±1). There is genuinely NO stable interior
  S³ minimum. "Charged matter must sit at n_4=0; finite n_4 only by imposed BC" is
  forced, not merely allowed.
- **Direction 2 (unstable→S³ inflation):** ALSO AVOIDED. The instability at n_4=0 is
  correctly read as decay to vacuum: I confirmed the winding charge Q = 4πm·cos³X
  (= 4πm·amp³) → 0 as the field rolls to the |n_4|=1 pole. The downhill direction
  annihilates the charge; it does not nucleate a stable S³ soliton. No suppressed S³.

---

## CLAIM-BY-CLAIM

**1. Structural blindness of native L4 — STANDS (with one false footnote).**
- (a) The native L4 IS the cross-product/eps_abc form (confirmed in
  `native_skyrme_derive.py`: `dot(n, cross(dn[m],dn[k]))`), not a 3-restriction of a
  4-capable form. STANDS.
- (b) ∂L4_native/∂(d_μ n_4) ≡ 0 for all μ — verified independently on generic
  4-vector gradients (all four derivatives identically 0). Genuine structural
  blindness. STANDS.
- L2 contains n_4 derivatives (kinetic), correctly handled via the EOM/potential
  (Claim 2). STANDS.
- **FALSE SUB-CLAIM (not load-bearing):** Part-1 d=4 prints "Lagrange-identity L4
  depends on d_μ n_4? **False**", and results.md lines 50–52 repeat that the Lagrange
  L4 "has ∂L4/∂n_4 = 0". This is WRONG: my clean generic re-derivation gives **True**
  — the Lagrange-L4 genuinely depends on n_4. The agent's `False` is a sympy
  assumptions-mismatch artifact: `vec()` builds symbols with `real=True`, but the test
  differentiates w.r.t. `Symbol('d{m}n3')` (no assumption), and
  `Symbol('x',real=True) != Symbol('x')`, so `diff` spuriously returns 0 (I
  reproduced the exact bug). IMPACT: none on the verdict — the verdict rests on the
  NATIVE L4's blindness (verified true, Claim 1b) and on the native-action EOM
  (Claim 2). The mistaken footnote actually *understated* the import: the Lagrange
  (non-native) form does see n_4, exactly as one expects of the imported S³ route.
  Recommend correcting the doc footnote; it does not change STANDS.

**2. Dynamical necessity (the crux) — STANDS (independently reproduced).**
Using my own orthogonal Y(r) parametrization (not the agent's X-angle):
- n_4 source (Y'=Y''=0): `4π(2κm²(Y²−1) − r²ξ(m²+1))·Y·e^{A+B}/r²`; vanishes at Y=0. ✓
- V(Y) = `2π(κm²(Y²−1) − r²ξ(m²+1))(Y²−1)·e^{A+B}/r²`.
- dV/dY|_0 = 0; **d²V/dY²|_0 = −4π(2κm² + r²ξ(m²+1))·e^{A+B}/r² < 0** — matches the
  doc's d²V/dX²|_0 exactly. Maximum. ✓
- Critical points: Y=0 and |Y*|²= 1 + r²ξ(m²+1)/(2κm²) **> 1** (outside |n_4|≤1). The
  would-be S³ minima are NON-PHYSICAL. Inside Y∈[−1,1], V is monotone decreasing in
  |Y| to the boundary. NO stable finite-n_4 minimum. ✓
- L4-only check (adversarial extra): V4 = 2πκm²(Y²−1)²·e^{A+B}/r², critical pts
  {−1,0,1}, Y=0 a maximum, minima at the |Y|=1 vacuum. Even L4 alone produces no
  interior S³ well. ✓
- Charge: Q = 4πm·cos³X = 4πm·amp³ → 0 at the downhill endpoint. Charge-destroying. ✓
Conclusion "stable charged matter sits at n_4=0 (S²); finite n_4 only by imposed BC"
is genuinely FORCED. STANDS.

NOTE on `s2_s3_identity_stability.py` VERDICT-LOGIC prose: the printed logic block is
written for the d²V>0 (minimum) case, while the computed value is d²V<0 (maximum).
The *script's printed boilerplate* therefore reads awkwardly against its own number,
but the RESULTS DOC narrative (§1.ii) handles the maximum case correctly via the
charge-destruction argument. Cosmetic mismatch in the script's print text only; the
math and the doc's reasoning are correct.

**3. Texture-as-artifact — STANDS (with a scope note).**
- (a) The coupled_tl_s2_derive embedding `(sinΘ sinθ cos mψ, …, cosΘ)` is NON-unit:
  |n|² = cos²θ cos²Θ − cos²θ + 1 ≠ 1 off the equator. Reproduced exactly. Its T^θ_θ
  carries cosθ — an artifact of the non-unit chart. ✓
- (b) The genuine unit hedgehog n = x/r (|n|²=1 exactly) has T^θ_θ =
  (κm² − m²r²ξ + r²ξ)/(2r⁴), θ-INDEPENDENT (texture-free), and T^t_t = T^r_r exactly
  (B=1/A consistent). Reproduced exactly. ✓
- SCOPE NOTE (not a break): texture-freedom is specific to the f(θ)=θ degree-1
  hedgehog. A generic unit map n=(sin f(θ)cos mψ, sin f(θ)sin mψ, cos f(θ)) carries
  θ-structure in T^θ_θ. But the CANON deg-1 carrier IS f=θ (n=x/r), which the agent
  used; the artifact verdict for the original motivating texture stands. The detour's
  original motivation (texture) genuinely dissolves.

**4. Provenance — STANDS.**
- eps_abcd n_a d_r n_b d_θ n_c d_ψ n_d ≡ 0 on the S² field (Y=const) — reproduced
  exactly (the 4th internal slot has no independent DOF to hit). ✓
- No native π₃/4-index/WZW invariant exists; the native current is the 3-index area
  form only. I found no committed line where eps_abcd/π₃/WZW is metric-DERIVED. S³
  enters only via the imported Lagrange-identity L4 + the Skyrme BC (Θ(core)=mπ,
  self-tagged "CHOSE"). S³ is never metric-derived. STANDS.

**5. #50 symmetry — STANDS (sanity).** `su3_field_test.py` confirms the metric supplies
U(1)×SO(3)×SO(3,1); the only internal rotation is SO(3)=Isom(S²); no metric-supplied
SU(2)=Isom(S³). Consistent with the absence of a π₃-protecting field. (Not
re-derived from scratch here; consistent with the cited blind-verified #50.)

---

## IMPORTED-AS-NATIVE AUDIT
None banked as native. The S³/Skyrme structure is explicitly named as the import
(Lagrange-identity L4 + Θ(core)=mπ BC). The native objects used (eps_abc area form,
L2, the 3-vector cross-product L4) are canon/blind-verified native and I confirmed
the native L4's n_4-blindness directly.

## DATA-BLIND
CONFIRMED. Zero mass/ratio/wall numbers; only κ,ξ,m,r symbols and L=√(κ/ξ) scale
language, none numerically evaluated.

## DEFECTS FOUND (none verdict-altering)
1. Part-1 d=4 print "Lagrange-L4 depends on n_4? False" — FALSE (sympy real-assumption
   symbol mismatch bug); the Lagrange-L4 does depend on n_4. results.md lines 50–52
   inherit this and should be corrected. Not load-bearing (native-L4 blindness, the
   actual claim, is verified true independently).
2. `s2_s3_identity_stability.py` VERDICT-LOGIC printed text is written for the
   minimum (d²V>0) case while the computed curvature is negative (maximum); cosmetic
   mismatch in the script print only — the doc §1.ii reasons correctly.

## BOTTOM LINE
S² settle STANDS as a genuine DEMANDS. No fork: no stable S³ branch exists in the
physical domain; the apparent S³ direction is charge-destroying unwinding to vacuum.
Texture is genuinely an embedding artifact. S³ is always imported. Recommend fixing
the two cosmetic/footnote defects above; neither disturbs the verdict.
