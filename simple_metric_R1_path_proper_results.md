## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 |
| **Mode** | OBSERVE / DERIVE |
| **Slice scope** | static SSS; hyp φ=arctanh(ξ/X); χ²-blind |
| **Observing or targeting?** | OBSERVE — pre-registered no Pantheon ranking of joins |
| **Comparator scaffolds** | NONE |
| **Verifier status** | SELF-SCRIPT `python3 simple_metric_R1_path_ops_observe.py` |
| **Build-on grade** | **LEAD** |
| **Re-run commands** | `python3 simple_metric_R1_path_ops_observe.py` |

### Premise ledger

| Item | Role | Tag | Enters claim? |
|------|------|-----|---------------|
| Simple metric elements | dℓ, null dt | THEORY | Y |
| xmax + tanh rapidity | PATH form | POSTULATE+DERIVED | Y |
| Join candidates | J1, P_ell, radar | CHOSE set | Y as options |

### What is NOT claimed

- Uniqueness of path=proper.
- Physics canon. SNe ranking.

### Do not build on

- Freezing P_ell from this tile alone.

---

# R1 RESULT — Is path = proper forced?

**Script/JSON:** `simple_metric_R1_path_ops_observe.py` · `simple_metric_R1_path_ops_out.json`  
**MAP seed:** `simple_metric_R1_path_proper_MAP.md`

---

## Lay summary

We asked: when we say “max distance” and “compose distances,” is that **forced** to mean the length static rulers measure (proper length)?

**Answer: not forced by the metric alone.**  
The metric **does** define several different 1D lengths. Which one is the composition coordinate \(x\) is still a **choice** — but the choices are no longer vague: they behave differently at the bound, so the xmax story **filters** them.

---

## What the metric forces (no choice)

On the simple metric:

| Object | Formula (sketch) | Role |
|--------|------------------|------|
| **Proper radial** | \(d\ell = e^{\phi}\,dr\) | What a static rod measures between nearby spheres |
| **One-way radar / optical** | \(R=\int e^{2\phi}\,dr\) | Light travel (coord time × \(c\)) |
| **Areal radius** | \(D_A=r\) | Sphere size / angle distance (chart origin) |
| **Rapidity** | metric \(\phi\) additive under dilation composition | Already in frame |

None of these by themselves says “composition chart \(x\) equals ___.”

---

## Candidate joins (all CHOSE)

| Join | Identification | At the xmax bound \(\phi\to\infty\) |
|------|----------------|-------------------------------------|
| **J1** | \(x=r\) (path label = areal) | Finite \(r\to X\); **proper \(\ell\to\infty\)** |
| **P_ell** | \(x=\ell\) (path = proper) | Finite \(\ell\to X\); areal \(r\to X(\pi/2-1)\); **radar \(R\to\infty\)** |
| **Radar as path** | \(x=R\) | Bound typically **not** at finite radar if \(\phi\to\infty\) on finite \(r\) or finite \(\ell\) |

Near the observer (small stretch) **all agree** to leading order: \(r\sim\ell\sim R\sim x\).  
Linear low-\(z\) does **not** pick a winner.

---

## Consistency filters (structure, not SNe)

These are **honesty filters** for the xmax narrative — still not uniqueness proofs.

| Desire from xmax story | J1 | P_ell | Radar-as-\(x\) |
|------------------------|----|-------|----------------|
| Finite composition bound \(X\) with \(\phi\to\infty\) | yes (\(r=X\)) | yes (\(\ell=X\)) | hard (radar often diverges) |
| Finite **proper** reach to bound | **no** (\(\ell\) diverges) | **yes** | depends |
| Finite **areal** saturation | yes | yes (\(r_{\max}=X(\pi/2-1)\)) | — |
| “Always farther, never a town” in **proper** rods | fails (infinite rod-stack to wall) | bound at finite rod-sum \(X\) | — |
| Local Hubble seed \(d\sim z\) | yes | yes | yes |

**Important nuance:** Under P_ell the bound sits at **finite proper distance** \(X\). That is more like “you can stack only so much ruler length before \(\phi\) blows,” not “infinite proper trek to an unreachable shell.” Whether that matches the poetic xmax line is a **ponder** with Charles — not settled here.

Under J1, the areal chart hits \(r=X\) while proper length to that wall **diverges** (more horizon-like in the proper sense).

---

## Verdict (hygiene-clean)

| Claim | Grade |
|-------|--------|
| Metric forces several distinct 1D ops | **DERIVED** |
| Metric forces \(x=\ell\) | **NO** |
| P_ell remains **motivated** for “composition of static rod displacements” | **CHOSE / LEAD** |
| J1 remains possible but **conflicts** with finite proper distance to \(\phi=\infty\) wall | **scoped tension** |
| Affine parameter unique as path distance | **NO** (normalization freedom) |
| χ² used to pick join | **NO** (pre-registered blind) |

**Build-on:** Keep P_ell as **working explore join** with eyes open; do **not** upgrade to DERIVED.  
Next refine can use the **filter table** above when Charles prefers “finite proper bound” vs “infinite proper to wall.”

---

## One-line

**Path=proper is not forced; it is one clean CHOSE among operational 1D lengths, favored if xmax means finite rod-sum and disfavored if the bound should cost infinite proper distance — J1/radar/affine are different, locally equivalent, globally distinct.**
