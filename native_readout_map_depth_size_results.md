# Native Readout-Map — the Depth/Size Node (Branch P) results

**Date:** 2026-07-06 · **Driver:** Claude Opus 4.8 (1M) · **Mode:** MAP → OBSERVE (armchair/CAS + bounded cheap ODE
shooting, DATA-BLIND, no coupled solve). · **Frame:** the ONE cosmic cell (no private particle cell/seal), hopfion as
content, ξ FREE. Second node of the general native readout-map problem (the first — target-channel selection —
CLOSED as B in `native_readout_map_selector_audit_results.md`).

## The question (pre-registered by Charles, 2026-07-06)

The channel-selector (q=1/3) route is closed. NEW, orthogonal axis: **does the native φ-angular sector produce
discrete allowed depth/size/mass readouts?** Working hypothesis: the φ-angular coupling is not a target-channel
selector (it lives in physical/cell geometry, not internal S²), but it may still enforce finite-size/depth
discreteness through the exact nonlinear scalar/flux equation + whole-cell boundary structure. Rules: exact nonlinear
operator (NO linearizing e^{−2φ}); no private cell/seal; no SM charge; no mass fitting; ξ NOT pinned; keep Q_H /
size-depth / public charge distinct; q=1/3 closed for this node; **check the exact operator before any shorthand.**

**Pre-registered outcomes:** A = native depth/size discreteness found; B = discreteness only in the cosmic depth
ladder, not particle size/mass (bank the separation); C = equations leave ξ/size continuous ⇒ Branch P does not pin
particle size without N5d; D = a non-perturbative solve is required (define the minimal gated solve, stop).

## Result — PRIMARY = C, with a banked B-separation and a sharp D-pointer

**As currently posed (round metric + perturbatively-coupled hopfion), the native Branch-P φ-angular sector leaves
particle SIZE and DEPTH CONTINUOUS — it does NOT pin ξ/size. The native discreteness that DOES exist (the topological
label Q_H∈ℤ and the D2b depth-N ladder) is a LABEL/depth structure ORTHOGONAL to the continuous mass-scale. The ONE
structural route to size/mass discreteness — a sign-changing off-round 𝒦 source — is a currently-FROZEN degree of
freedom (the transverse shear h_AB), reachable only by the gated non-perturbative N5d solve.** This is a
solver-completeness verdict (a frozen DOF), NOT a mechanism claim.

### Foundation (certified, established + premise-compared before analysis)

- **Exact operator** = `∂_r(√h Z_φ φ') = −2√h·e^{−2φ}·𝒦̂[h]`, round shorthand **`Z_φ(r²φ')' = 4e^{−2φ}`** — source =
  the GEOMETRIC uncompensated extrinsic-curvature invariant 𝒦=K_AB K^AB−K² (NOT matter; NOT the archived `e^{+2φ}`
  scalar-tensor potential — that is a superseded different equation, rejected). Matter enters only indirectly,
  n→h_AB→𝒦→φ. The shorthand keeps e^{−2φ} EXACT (not a linearization) but is a ROUND (h_AB=r²Ω frozen) reduction.
- **Whole-cell BCs** (one cosmic cell): even core `φ'(r_c)=0, ρ'(r_c)=0` (values free); odd flux seal `φ(r_s)=0`
  (Dirichlet, canon C-2026-07-04-1), `ρ'(r_s)=0`, `φ'(r_s)` FREE ⇒ `q=Z_φρ_s²φ'(r_s)` an OUTPUT; flux budget
  Q_seal=2p_F=M is a co-varying IDENTITY. φ_c=−ln(1101) is z_CMB DATA = OUT OF SCOPE (kept free, not imported).
- **BULK equation is exactly SCALE-INVARIANT** (r→μr maps it to itself) ⇒ absolute size is a free modulus; any
  discreteness must live in the whole-cell closure or in dimensionless ratios, NOT in a bulk spectrum.
- **Novelty (registry discipline):** FRESH, not a re-tread. Every banked "one continuum / no depth selector" negative
  (#34/#39/#52/#54, #66) rode a DIFFERENT operator (EH "vacuum=GR", or the superseded scalar-tensor `e^{+2φ}`), an
  imported S³ baryon, a pinned X=−2e5 kluge, or a PRIVATE particle cell. The native S²/hopfion on the derived
  `e^{−2φ}`-𝒦 operator under the whole cosmic-cell BCs, ξ-free, had NEVER been solved. Registry principle P-B
  ("closures allow a discrete set while absolute size stays free") is the affirmative anticipation this node tests.

### Node A — the round vacuum closure is a CONTINUUM (rigorous core)

Autonomous form (t=ln r) of the EXACT equation: **`φ_tt + φ_t = A e^{−2φ}`, A=4/Z_φ>0** — a unit-friction particle in
the MONOTONE runaway potential V(φ)=(A/2)e^{−2φ} (force −V'=Ae^{−2φ}>0 ∀φ; e^{−2φ} kept exact). Whole-cell BCs:
even-core = "start at rest" at φ_c; seal = "reach φ=0". Since the force is **sign-definite positive** and the particle
starts at rest, **φ rises MONOTONICALLY** — it never turns around, so:
- a regular solution exists for a **continuous range of φ_c<0** (no quantization condition);
- **radial node count ≡ 0** and **turning-point count of φ ≡ 0** for all states — no node/turning ladder exists to
  index states; the seal-energy closure with φ'(r_s) FREE merely DEFINES q (adds no equation), and the flux budget is
  a co-varying identity ⇒ **no closure condition remains to pin φ_c or the size.**
- Family = {absolute size R} × {core depth φ_c}, both CONTINUOUS. Confirmed numerically (exact nonlinear ODE, two
  independent integrations agree to all digits, rtol 1e-11): r_s/r_c and q vary smoothly with φ_c (r_s/r_c is even
  FOLDED/non-injective ⇒ cannot serve as a label). **The sign-definiteness ⇒ monotone ⇒ no-node argument is rigorous
  and solve-independent** for the round source.

### Node B — the hopfion RIDES; mass = flux = a CONTINUOUS whole-cell response

- **Q4 (select vs ride): RIDES.** The hopfion's own size λ*~√(κ/ξ) is a continuous function of the FREE couplings —
  `solve(E₂=E₄, ξ) → ∅` (the virial balance holds identically ∀ξ,κ; CAS, blind-verified in N5a). It RELABELS the free
  modulus, it does not quantize it. All three armchair selection channels fail: whole-cell criticality = ONE relation
  with R unpinned (N5a); flux closure = Gauss's-law IDENTITY, Z_φ cancels, `solve(…,ξ)→∅` (N5b); depth-resonance =
  the D2b ladder, which is orthogonal (below). λ* sets the free scale, does not break the bulk scale-invariance.
- **Q5 (mass carrier): mass = flux = M = q = Z_φρ_s²φ'(r_s), a CONTINUOUS whole-cell response.** Candidates (a)
  read-surface flux and (b) whole-cell response are the SAME quantity two ways — the native transverse operator
  L_bare=r²f''−2rf'+2f has roots {1,2}, both growing ⇒ NO decaying homogeneous mode ⇒ a compact hopfion stress
  sources a cell-FILLING shear, not a localized halo (a localizing wall = the retired private seal). (d)
  non-perturbative backreaction (ε≫1) fixes the MAGNITUDE and the (positive-mass LEAN) SIGN, does not discretize. (c)
  depth/fold matching = the D2b ladder = a real discrete DEPTH/node-count structure, but ORTHOGONAL to the mass-scale.
- The hopfion **couples to the D2b depth ladder only inside the gated N5d solve** (at O(amp²) via shear-modulation);
  at armchair the size modulus and the depth ladder are decoupled.

### The convergence — one door

Both nodes are solve-independent for what they assert and point at the SAME single frozen DOF: **the off-round
transverse shear h_AB**, frozen (=r²Ω) in both the round reduction and the perturbative hopfion coupling. The round
source `−2√h·e^{−2φ}𝒦̂` is **sign-definite** (round: 𝒦=−K²/2<0 ⇒ source>0), which is exactly why the phase portrait
is a monotone runaway with no well — so **no discreteness can arise while h_AB is frozen.** Turning that DOF on is the
route to a discrete closure; there are (at least) two candidate MECHANISMS within it, neither yet proven necessary:
(i) **a sign-changing source** — off-round `𝒦=−2 det(K^A_B)=−2k₁k₂` can flip sign (principal expansion rates of
opposite sign, k₁k₂<0 ⇒ 𝒦>0 ⇒ source<0), injecting an effective restoring region → a well → turning points/nodes in
φ; and (ii) **the transverse-traceless h_AB tensor eigenproblem** (the E^{AB} sector the scalar equation cannot hold),
whose compact-cell tensor modes generically carry a discrete spectrum — which could quantize even with 𝒦 sign-definite.
The DOF is exclusive; the mechanism is not settled (and settling it is not needed here). So the negative is a
**frozen-DOF (solver-completeness) verdict, not a metric verdict and not a mechanism claim**:
per the solver-first protocol — (1) left out = the off-round shear / finite-amplitude 𝒦; (2) numeric? no, round is
analytically closed; (3) frozen DOF? YES (h_AB=r²Ω); (4) whole space explored? no, only the round + perturbative
corner.

### Discrete-vs-continuous ledger (Q6)

| quantity | status |
|---|---|
| absolute size R | CONTINUOUS / FREE (bulk scale-invariance) |
| core depth φ_c | CONTINUOUS / FREE (round closure pins nothing) |
| native size λ*~√(κ/ξ) | CONTINUOUS (rides free ξ,κ; `solve(E₂=E₄,ξ)→∅`) |
| r_s/r_c | CONTINUOUS OUTPUT of φ_c (folded, not a label) |
| radial node count / turning-point count | fixed = 0 (round) — degenerate, no ladder |
| q = M = mass | CONTINUOUS OUTPUT (whole-cell flux; NOT ∝Q_H) |
| **Q_H ∈ π₃(S²)=ℤ** | **DISCRETE** — topological linking LABEL, orthogonal to mass-scale, size-independent |
| **D2b depth-N ladder (N=0..22)** | **DISCRETE** — depth/profile label; absolute anchor = z_CMB (data); NOT size/ξ |

**Net: native discreteness exists as LABELS (Q_H, depth-N), the mass-scale/size is a CONTINUUM** — this is the banked
B-separation. Off-round size/mass discreteness is UNDECIDED (frozen DOF, N5d).

### D-pointer — the minimal gated solve (defined, then STOP)

The only surviving route to size/mass discreteness: the **non-perturbative, fully-coupled (φ + transverse h_AB)** solve
on the RESOLVED hopfion source, with the exact 𝒦-source retained at FINITE AMPLITUDE (no frozen h_AB=r²Ω, no Dirichlet
wall, no perturbative L⁻¹), on the TRUE running ambient φ_amb(r)≈½ln((8/Z_φ)ln r), reading δq on a bulk read-surface.
Question it answers: does the off-round shear DOF open a discrete r_s/r_c or node-count closure — via a sign-changing
𝒦 (a well) and/or the transverse-traceless h_AB tensor eigenproblem — that pins ℓ_hopf/ρ_c (hence ξ) to a rung,
coupling the hopfion size to the depth ladder? ANTI-HANG
binding: bounded grid (Nr≤16–24), ONE clean process, no background-poll; use a CORRECT L_bare inverse (the prior
`n4rev_pipeline` did not invert L_bare — magnitudes from it are unreliable; the sign survived). **H4 compute remains
STOPPED — N5d stays GATED behind Charles's go.**

## Provenance ledger (load-bearing)

- Exact operator + BCs + scale-invariance + novelty comparison — certified by the foundation node (built on, not re-derived).
- Round autonomous ODE `φ_tt+φ_t=Ae^{−2φ}`, monotone/no-node — DERIVED this node (analytic + bounded numeric, exact e^{−2φ}).
- Hopfion RIDES; `solve(E₂=E₄,ξ)→∅`; flux-closure residual≡0; mass=flux=M=whole-cell (L_bare roots {1,2}) — DERIVED (N5a/N5b/N4rev, blind-verified priors).
- Q_H∈ℤ topological label — NATIVE (conditional on the local-ball crux); D2b depth-N ladder — NATIVE (depth, not size; anchor z_CMB=data).
- ξ, κ, Z_φ, φ_c, absolute R — FREE/CHOSE (not pinned); q — DERIVED OUTPUT (not ∝Q_H); φ_c=−ln(1101) = z_CMB DATA, OUT OF SCOPE.

## Scope / caveats

- The CONTINUUM verdict is **SCOPED to the round (frozen-transverse-h_AB) + perturbatively-coupled-hopfion corner.**
  Its rigorous, solve-independent part is the ROUND-source sign-definiteness ⇒ monotone ⇒ no-node argument. The
  off-round finite-amplitude regime is UNENTERED (frozen DOF) — the negative does NOT extend there.
- This does NOT re-confirm the banked continuum negatives (#34/#39/#52/#54, #66): they rode a different operator /
  imported matter / pinned X / private cell. This is the first characterization on the correct native operator + whole
  cosmic-cell BCs, and it converts the vague "continuum" into a sharp claim: round is provably continuum; discreteness,
  if any, is exactly the off-round shear closure (N5d).
- ξ remains a FREE family parameter (consistent with the N5 arc); Branch P does not pin particle size without N5d.

## Verifier

**Blind adversarial pass — VERIFIED-WITH-CAVEATS → edit applied (verifier ae3142d4ba6d9e825, Claude Opus 4.8 (1M),
fresh zero-context, 2026-07-06).** Independently re-derived the autonomous form (SymPy: `d/dr(r²φ')≡φ_tt+φ_t` ⇒
`φ_tt+φ_t=(4/Z_φ)e^{−2φ}`, e^{−2φ} exact) and re-ran the exact-nonlinear shooting (rtol 1e-11): every φ_c gives
monotone φ, node-count 0, turning-points 0, seal reached; a **2000-sample random hunt found NO** non-monotone /
node / turning-point case ⇒ Claim 1 (round continuum) is rigorous and could not be broken. Mounted the sharpest
hidden-closure attack (ρ' at two points as a Sturm–Liouville over-determination) — fails in the round corner (h_AB
frozen ⇒ ρ passive, the two ρ' conditions vacuous; the quantizing shear dynamics turn on only off-round = the frozen
DOF routed to N5d). Node-B identities pass CAS (L_bare indicial m²−3m+2, **roots {1,2}** both growing ⇒ no decaying
mode ⇒ whole-cell response; virial λ*=√(E4/E2) exists ∀ξ ⇒ ξ unpinned). Both 𝒦-sign facts confirmed (round
𝒦=−K²/2≤0 sign-definite; off-round −2k₁k₂ can flip). B-separation judged HONEST (Q_H size-independent homotopy
invariant; D2b depth-not-size), scoping + solver-first framing correct (frozen DOF, not "Branch P period", not a
mechanism), no smuggle (e^{−2φ} exact; z_CMB anchor NOT imported; q not ∝Q_H). **ONE required edit** — soften Claim
2's "sign-changing 𝒦 is the ONLY route" (an unproven mechanism-uniqueness claim, mildly inconsistent with the
frozen-DOF discipline; the transverse-traceless h_AB tensor eigenproblem is a second sub-route within the same DOF).
**Edit APPLIED** (the "convergence" + D-pointer paragraphs above now name h_AB as the exclusive DOF and both candidate
mechanisms; DOF-exclusivity unaffected). Classification: PROVEN-to-symmetry-of-argument for the round continuum
(rigorous), SCOPED to the round+perturbative corner, off-round UNENTERED (gated N5d).
