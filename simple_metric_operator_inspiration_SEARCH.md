# Exploratory search — operators that came close (repo mine)

**Date:** 2026-07-08 · **Mode: OBSERVE / mine** (inspiration only).  
**Frame:** elegant + simple metric + \(c\)-analogy.  
**Not:** re-activating free \(D_A\), cell seals, or hand \(x_{\max}\) as live FE.  
**Purpose:** find flawed-but-near operators that already pointed at \(c\)-like / \(\phi\to\infty\) structure.

---

## 1. What “came close” means here

Under the \(c\)-analogy we want something like:

- effect diverges as a bound is approached (\(\gamma\to\infty\) / \(z\to\infty\) / \(\phi\to\infty\)),  
- unattainable beyond,  
- preferably finite chart radius, infinite proper distance.

**Near-misses** = repo operators or kinematic laws that **produce or encode** that shape, even if derivation was flawed, wrong branch, or later demoted.

---

## 2. Leaderboard (inspiration rank)

### ★★★ A. Dilation-boost / \(x_{\max}\) kinematics (closest in *form*)

| | |
|--|--|
| **Where** | `archive/udt_xmax_boost_derivation_results.md`, `archive/udt_max_distance_invariance_FRAME.md`, `derive_xmax_boost.py`; frame notes in `macro_xmax_limit_FRAME.md` |
| **What it is** | Composition of radial displacements with finite invariant fixed point \(X=x_{\max}\): \(x_1\oplus x_2=(x_1+x_2)/(1+x_1x_2/X^2)\). Additive depth \(\phi=\mathrm{arctanh}(x/X)\). |
| **\(c\)-like content** | \(x=X\tanh\phi\); \(\phi:0\to\infty\) maps \(x:0\to X\) **asymptotically**; \(dx/d\phi\to0\) at edge; \(1+z=\sqrt{(X+x)/(X-x)}\) (Doppler form with \(\beta=x/X\)); \(A=(X-x)/(X+x)\to0\) at \(x=X\) (horizon). |
| **Flaw** | Postulates finite \(x_{\max}\) (like postulating finite \(c\)); “invariant *distance*” over-read → preferred-center / homogeneity traps; later demoted to **re-coordinatization of \(1+z=e^\phi\)** in part. |
| **Why still gold** | This is the cleanest **structural** \(c\)-twin in the repo: rapidity = \(\phi\), bound = \(X\), \(\gamma\)-like redshift. Live question: can the **metric/FE** *force* \(A\to0\) at finite \(x\), instead of *postulating* \(X\)? |

**Inspiration:** Treat \(\phi\) as **rapidity of position**; hunt operators whose solutions make a **bounded chart coordinate** conjugate to unbounded \(\phi\).

---

### ★★★ B. Unweighted / “self-consistent” vacuum (different vacuum family)

| | |
|--|--|
| **Where** | `native_field_equations_constrained_two_player_results.md` §2–3; `verify_native_fieldeq.py` |
| **Operators** | **R1-weighted:** \((r^2\phi')'=0\) → \(\phi=\phi_\infty-q/r\). **Unweighted self-consistent:** \(\Box_g\phi+e^{-2\phi}(\phi')^2=0\) → \(e^{-\phi}=C_0+C_1/r\) → \(g_{tt}=-(C_0+C_1/r)^2\). |
| **Also** | Covariant \(\Box_g\phi=\frac1{r^2}\partial_r(r^2 e^{-2\phi}\phi')\). |
| **\(c\)-like content** | Squared-lapse form can hit **\(g_{tt}=0\)** when \(C_0+C_1/r=0\) i.e. **finite** \(r_*=-C_1/C_0\) if signs allow — a **chart-finite horizon** candidate, unlike Coulomb exponential. |
| **Flaw** | Unweighted kinetic **breaks** the R1 “density = φ-free” resolution of probe vs self-consistent; project retired it as less principled than R1 weight. |
| **Why still gold** | Only simple-metric vacuum family in the native FE doc that **naturally produces a finite-r zero of the lapse** without free \(D_A\). Worth re-checking residual vs \(c\)-criteria **as a flawed-but-near EL**, not as canon. |

**Inspiration:** Horizon = **zero of \(e^{-\phi}\) or \(\sqrt{-g_{tt}}\)**, not plateau of \(\phi\) at infinity.

---

### ★★ C. Branch-P “retained potential” \(U=e^{2\phi}-1\) (**non-self-quenching**)

| | |
|--|--|
| **Where** | `archive/branch_P_characterization_results.md` |
| **Operator (reduced)** | \(L_{\mathrm{red}}=(X-2)r^2(\phi')^2+2r\phi'+(e^{2\phi}-1)\) leading to e.g. \(\phi''=-2\phi'/r+(e^{2\phi}-1)/[(X-2)r^2]\). |
| **\(c\)-like content** | Potential \(U=e^{2\phi}-1\) has \(U'\propto e^{2\phi}\) — as \(\phi\to+\infty\), force **grows**, not dies. **Opposite of SQ** \(e^{-2\phi}\) sources. Document notes runaway toward \(\phi\to0\) in some regimes (preferred *value*, not edge). |
| **Flaw** | Packaging \(f=e^{2\phi}\) weight on curvature / scalar-tensor-like; later native geometric action **replaced** this with \(\mathcal{K}\) (weight −2). Scale-free; pins \(\phi\)’s value not a finite edge. |
| **Why still gold** | Proves the repo **already knew** a bulk ingredient that is **non-SQ** (weight **+2** on the potential). Our F2 completeness said “+2 not derived from \(\mathcal{K}\)” — this is the historical **alternate derivation path** (IBP survivor of weighted curvature). |

**Inspiration:** Re-open **whether** the \((e^{2\phi}-1)\) survivor is smuggled ST or a legitimate IBP remainder on the simple metric — as **inspiration for non-SQ**, not as automatic truth.

---

### ★★ D. Matter-sourced finite \(\phi\to\infty\) edge (reconcile finding)

| | |
|--|--|
| **Where** | `cosine_native_reconciliation_results.md` |
| **Claim** | Native two-player **vacuum** has **no** finite \(\phi\to\infty\) edge; the \(x_{\max}\) / \(\phi\to\infty\) edge is **matter-sourced**. |
| **Flaw** | Two-player often **cell-contaminated** / frozen \(h_{AB}\); macro never solved cleanly; we also saw dilated compact dust → finite \(\phi_\infty\), not \(\phi\to\infty\). |
| **Why still gold** | Correct **qualitative** lesson: vacuum geometric packages often **refuse** the edge; **matter** may be necessary — but the **form** of coupling matters (our dilated \(e^{-2\phi}\) dust was SQ). |

**Inspiration:** Edge may require **matter**, but with a **non-SQ** channel (contrast native “φ-blind channels, indirect source” vs dilated continuum).

---

### ★★ E. Misner–Sharp / seal \(f\to0\) (trapping = edge)

| | |
|--|--|
| **Where** | `archive/B1_mass_dilation_cost_results.md`, seal/weld docs; macro xmax frame |
| **Form** | \(m=(c^2 r/2G)(1-e^{-2\phi})\); seal limit \(f=e^{-2\phi}\to0\Rightarrow m=r/2\) (marginal). |
| **\(c\)-like content** | \(f\to0\) is \(\phi\to+\infty\); finite chart radius possible; “time stops.” Same horizon face as xmax boost \(A\to0\). |
| **Flaw** | GR-form mass / junction package; circular use of \(c^2=2GM/R\) as depth fit; cell seals. |
| **Why still gold** | Ties **infinite dilation** to a **geometric trapping condition** already in the corpus — a target identity for native FE to reproduce, not a knob. |

---

### ★ F. \(\Box_g\) / CG scalar operators (linearized & nonlinear)

| | |
|--|--|
| **Where** | `udt_canonical_geometry.md` §2–8; linearized \(\phi''+2\phi'/r-\mu^2\phi=-S\); nonlinear warnings \(e^{-2\phi}\sim5\) at hadronic depth |
| **\(c\)-like content** | Weak alone; sinh / sourced profiles; continuum negatives often used **wrong operator** (registry). |
| **Flaw** | Linearization invalid at depth; many CMB/cavity uses scaffolding. |
| **Why mine** | Shows **operator class matters**; banked negatives don’t kill a new operator. |

---

### ★ G. Hard-edge MAP asymptotics (HE1)

| | |
|--|--|
| **Where** | `macro_native_edge_HARD_MAP.md` |
| **Ask** | What balances EL as \(\phi\to\infty\) (Path A/B, vacuum + dilated)? BVP with \(\phi\to\infty\) at unknown \(r_*\). |
| **Result (session history)** | Path A/B vacuum IVP **refused** finite-\(r\) \(\phi\to\infty\) under those bulk forms. |
| **Why mine** | Correct **question**; confirms SQ bulk **refuses** the edge — consistent with current diagnosis. |

---

## 3. Pattern across near-misses

| Pattern | Operators that… | \(c\)-edge? |
|---------|-----------------|-------------|
| **SQ** \(e^{-2\phi}\) source | Geometric \(\mathcal{K}\), dilated dust, many native P | Refuse \(\phi\to\infty\) |
| **Non-SQ** \(e^{+2\phi}\) potential | Branch-P retained \(U=e^{2\phi}-1\) | Runaway / preferred φ value — not yet finite edge |
| **Kinematic bound** | \(x=X\tanh\phi\), \(A=(X-x)/(X+x)\) | **Closest form**; often postulated \(X\) |
| **Lapse zero** | Unweighted vacuum \(e^{-\phi}=C_0+C_1/r\); MS \(f\to0\) | Finite-\(r\) horizon candidate |
| **R1 kinetic only** | Coulomb | Finite \(\phi_\infty\), open \(r\) |

**Meta-lesson for live work:**  
Inspiration points to either  
1. **kinematic rapidity law** (xmax boost) made **dynamical**, or  
2. **lapse-vanishing** solutions (unweighted / MS / \(A\to0\)), or  
3. **non-SQ** bulk weight (+2) if it can be **re-derived** without ST smuggling —  
not to free \(D_A\) theater or more SQ sources.

---

## 4. Recommended inspiration order (still no invention)

1. **Re-read** xmax boost + frame-relation demotion: keep \(\phi=\mathrm{arctanh}(x/X)\) / \(A=(X-x)/(X+x)\) as **target structure**; ask what EL (if any) on the simple metric produces \(A\to0\) at finite \(x\).  
2. **Re-probe** unweighted vacuum \(\Box\phi+e^{-2\phi}(\phi')^2=0\) under \(c\)-criteria (flawed R1, but horizon-capable).  
3. **Re-open** Branch-P \(U=e^{2\phi}-1\) provenance: IBP of what weight? Can it be forced on simple metric without X kluge?  
4. **MS identity** \(f\to0\) as **diagnostic**, not as imported GR mass.  
5. **Do not** prioritize: free \(D_A\) explore pile, cell two-player as macro, φ-blind dust.

---

## 5. One-line

**Closest repo inspiration for a \(c\)-like edge: xmax rapidity kinematics and lapse-zero vacua; closest non-SQ bulk: historical \(e^{2\phi}-1\) potential; SQ geometric \(\mathcal{K}\)/dilated dust are the far misses — use the former as targets for re-derivation on the simple metric, not as copy-paste canon.**
