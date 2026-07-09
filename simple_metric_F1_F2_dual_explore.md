# Dual explore — F1 and F2 under the \(c\)-analogy (simple metric)

**Date:** 2026-07-08 · **Mode: OBSERVE both forks** (Charles: try both).  
**Metric:** \(ds^2=-e^{-2\phi}c^2dt^2+e^{2\phi}dr^2+r^2d\Omega^2\) only.  
**Test:** `simple_metric_c_analogy_MAP.md`.  
**Prior:** `simple_metric_c_analogy_rederive_results.md`.  
**Status:** PROVISIONAL dual characterization — **no invented edge term**, free \(D_A\) quarantined.

---

## Fork definitions

| Fork | R1 meaning | Bulk dynamics |
|------|------------|---------------|
| **F1** | Shift \(\phi\to\phi+\mathrm{const}\) is an **exact symmetry of the bulk action** | Only shift-weight **0** densities; vacuum EL ⇒ Coulomb |
| **F2** | R1 fixes the **metric form** (differences enter \(g_{tt},g_{rr}\)); bulk may break shift if **derived** | Shift-breaking allowed; current \(\mathcal{K}\) is one try (fails \(c\)-test by self-quench) |

---

# Part A — Fork F1 (R1 exact on bulk)

## A1. What the bulk theory is

Shift-weight **0** local pieces on the simple metric (CAS inventory):

| Density | Weight | Role |
|---------|--------|------|
| \((\phi')^2\) (R1 kinetic after factors) | 0 | dynamics |
| \(R^{(2)}=2/r^2\) | 0 | no φ |
| \(e^{2\phi}\mathcal{K}=-2/r^2\) | 0 | cancels \(R^{(2)}\); no φ |
| bare \(\mathcal{K}\propto e^{-2\phi}\) | **−2** | **excluded** under F1 |
| \(e^{\pm 2\phi}(\phi')^2\) without R1 cancel | ≠0 | **excluded** under F1 |

**Vacuum F1 action (unique in this class up to \(Z\)):**

\[
L = \frac{Z}{2} r^2 (\phi')^2
\quad\Rightarrow\quad
(r^2\phi')'=0
\quad\Rightarrow\quad
\phi = \phi_\infty - \frac{q}{r}.
\]

**Matter under F1:** continuum must also be shift-clean **or** tagged as explicit break.  
Dilated dust \(\propto e^{-2\phi}\) is weight **−2** → **not F1-clean**.  
φ-blind dust does not couple to φ.  
So **F1 vacuum is Coulomb; F1 does not naturally include our dilated \(L_m\).**

## A2. Does F1 give a bulk \(c\)-edge?

| C1–C2 (\(c\)-like \(\phi\to\infty\) at finite \(r\), unattainable) | **FAIL** (exact) |
| Redshift out for \(q>0\), observer at finite \(r_0\) with chart \(\phi(r_0)=0\) | **YES** to finite \(z_{\max}=e^{q/r_0}-1\) |
| Open \(r\to\infty\) | **YES** |

**Conclusion F1:** Bulk EL **cannot** be the \(c\)-analog engine. If F1 is true, the \(c\)-analogy must live **outside** “bulk source runs \(\phi\) to \(\infty\).”

## A3. Where the \(c\)-analog *can* live under F1 (explore, not invent)

### F1-α — Redshift-as-\(\gamma\) (kinematic)

Identify **positional “gamma”** with the dilation factor:

\[
\gamma_{\mathrm{pos}} \sim e^{\Delta\phi} = 1+z.
\]

- As \(\Delta\phi\to\infty\), \(\gamma_{\mathrm{pos}}\to\infty\) — **same shape as SR**.  
- Under F1 vacuum, **accessible** \(\Delta\phi\) for a given solution is **bounded** (\(\le q/r_0\)).  
- So: the **formula** is \(c\)-like in \(\phi\)-space; the **Coulomb solution** does not open infinite \(\Delta\phi\) along outward reach.

**Score:** analogy holds for the **redshift law**; fails for **unbounded approach along outward paths** in F1 vacuum.

### F1-β — Horizon kinematics (metric only, profile not solved)

If **any** context produces \(\phi\to+\infty\) at finite \(r_*\) (matter singularity, different sector, junction), then on the simple metric:

- \(g_{tt}\to 0\), \(d\ell = e^{\phi}dr\to\infty\) per chart step for large \(\phi\),  
- profiles with \(\phi\sim -a\ln(1-r/R)\), \(a\ge 1\), have **divergent proper distance** to \(r_*\).

Under **strict F1 bulk**, vacuum EL **do not** produce those profiles. F1-β only says: **if** \(\phi\to\infty\) appears, **unattainability is automatic from the metric** — the \(c\)-shape is **kinematic**, not from bulk SQ source.

**Score:** metric supports \(c\)-like unattainability; F1 bulk does not generate the needed \(\phi\).

### F1-γ — Relational / observer edge (frame-relation)

Each observer sets \(\phi=0\) at themselves; law \(1+z=e^{\phi(r)}\) in their chart.

- No preferred center.  
- “Edge” = limit of **communicable / redshifted** content in that chart, not a global bag.  
- Under Coulomb, each observer who can set a local expansion of \(\phi\) still sees **finite** max outward \(z\) for that global \(q\) (chart-dependent presentation of one solution).

**Score:** good for **no preferred center**; does **not** by itself create infinite asymptotic depth.

### F1-δ — Matter without SQ weight (only if derived)

Under F1, matter that couples to \(\phi\) while preserving shift is tightly constrained (essentially hard).  
**Not explored by inventing \(V(\phi)\).**  
**Result:** F1 + continuum coupling is **mostly empty** unless a shift-clean coupling is derived later.

## A4. F1 bottom line

| Deliverable under F1 | Status |
|----------------------|--------|
| Unique vacuum bulk (up to \(Z\)) | Coulomb — **derived under F1** |
| Bulk \(c\)-edge \(\phi\to\infty\) | **Impossible** |
| \(c\)-like **redshift formula** | **Yes** (\(e^{\Delta\phi}\)) |
| Path forward | Treat \(c\)-analogy as **kinematic / relational / law-form**, not bulk SQ EL; **or** abandon F1 for macro edge |

---

# Part B — Fork F2 (R1 on metric only; bulk may break shift)

## B1. What is allowed

- Metric still from R1–R3 (differences → exponential factors).  
- Bulk densities may carry shift weight ≠ 0 **if derived** (angular geometry is the known example).  
- **Still forbidden:** hand \(x_{\max}\), free \(D_A\), BB fluids, random \(V(\phi)\).

## B2. What we already tried (and why it fails \(c\))

| Break | Weight | EL effect as \(\phi\to+\infty\) | \(c\)-test |
|-------|--------|----------------------------------|-----------|
| Uncompensated \(\mathcal{K}\) | −2 | source \(\propto e^{-2\phi}\to 0\) | **FAIL (SQ)** |
| Dilated dust | −2 | same | **FAIL (SQ)** |

**CAS:** \(c\)-like profiles \(\phi=-a\ln(1-r/R)\) do **not** solve these EL.

## B3. What a non-self-quenching break would need

For an EL of schematic form

\[
\frac{d}{dr}\bigl(Z r^2\phi'\bigr) = S[r,\phi,\phi',\ldots],
\]

to drive \(\phi\to+\infty\) at finite \(r_*\) (or keep sourcing as \(\phi\) grows), \(S\) must **not** die as \(e^{-2\phi}\).

| \(S\) behavior as \(\phi\to+\infty\) | Class |
|-------------------------------------|--------|
| \(\propto e^{-2\phi}\) | SQ — **current** |
| \(\to\mathrm{const}\neq 0\) or grows | **non-SQ** — needed for bulk-driven \(c\)-edge |
| weight 0 pure derivative constraints | may force profiles without “source” language |

**No non-SQ bulk density has been derived yet** on the simple metric from angular flatness:

- Uncompensated \(\mathcal{K}\): weight −2 (forced shape of extrinsic curvature with unit normal \(\sim e^{-\phi}\partial_r\)).  
- Compensating with \(e^{2\phi}\): weight 0, φ-independent on \(D_A=r\).  
- That is why the geometric-action path **structurally** lands on SQ or empty vacuum.

## B4. Shift-weight table (simple metric, CAS)

| Object | Weight under \(\phi\to\phi+\lambda\) |
|--------|--------------------------------------|
| \((\phi')^2\) | 0 |
| \(e^{2\phi}(\phi')^2\) | +2 |
| \(e^{-2\phi}(\phi')^2\) | −2 |
| \(\mathcal{K}\) | −2 |
| \(e^{2\phi}\mathcal{K}\) | 0 |
| \(R^{(2)}\) | 0 |
| Full \(R\) | mixed (not pure exp) |
| EH bulk | empty (total \(r\)-derivative) |

**Route B note (longitudinal completion, corpus):** mixing \(\sim e^{\phi}K\phi'\) on \(D_A=r\) reduces to \(\sim \phi'/r\) (weight 0).  
Leads to a **modified first integral**, still **not** checked to give \(\phi\to\infty\) at finite \(r\); not a free invention — if used, must re-derive fully on simple metric and re-test \(c\)-profiles. **Optional follow-up tile**, not activated as “the fix.”

## B5. F2 bottom line

| Deliverable under F2 | Status |
|----------------------|--------|
| Shift-breaking allowed | Yes (in principle) |
| Current derived break (\(\mathcal{K}\), dilated dust) | **SQ — fails \(c\)** |
| Derived **non-SQ** break on simple metric | **Not found** in inventory |
| Free shopping for weight +2 density | **Forbidden** (mechanism) |
| Path forward | Re-derive from metric **without** assuming the old action is complete; only bank non-SQ if **forced**; or conclude geometric-action completeness **blocks** bulk \(c\)-edge |

---

# Part C — Comparison (both tried)

| Question | **F1** | **F2** |
|----------|--------|--------|
| Vacuum bulk EL | Unique Coulomb (up to \(Z\)) | Coulomb **or** SQ uncompensated (old) |
| Bulk-driven \(c\)-edge | **No** | **Not with known derived terms** |
| Metric allows \(c\)-profiles | Yes | Yes |
| \(e^{\Delta\phi}\) as \(\gamma_{\mathrm{pos}}\) | Natural | Natural |
| Self-quench problem | N/A (no SQ source) | Central failure of current F2 tries |
| Risk | \(c\)-edge not bulk | Open-ended search / import risk |
| Risk | Underpowered macro | Overcounting incomplete action as final |

**Shared agreement of both forks:**

1. Simple **metric** is fine for a \(c\)-like *geometry of dilation*.  
2. Present **packaged EL** (geometric \(W\cdot\mathcal{K}\) ± dilated dust) **do not** implement bulk \(c\)-edge.  
3. **Do not** hand-set \(x_{\max}\) or free \(D_A\).  
4. \(1+z=e^{\Delta\phi}\) remains the elegant redshift law.

**Where they differ:**

- **F1:** stop asking bulk vacuum to make \(\phi\to\infty\); develop **kinematic/relational** \(c\)-reading on Coulomb (+ later derived matter that respects F1).  
- **F2:** keep bulk-edge hope; **refuse** SQ sources as the exterior engine; only accept a **new derived** non-SQ structure if the metric forces it (not found yet).

---

# Part D — What to do next (without forcing your pick)

Run **both** as thin parallel threads:

| Thread | Concrete next tile |
|--------|-------------------|
| **F1-next** | Write the **F1-complete simple theory**: Coulomb vacuum + relational redshift + explicit statement that \(c\)-analog is \(\gamma_{\mathrm{pos}}=e^{\Delta\phi}\) with solution-dependent max \(\Delta\phi\); check multi-observer consistency notes against canon frame-relation (no new FE). |
| **F2-next** | One **closed** derivation pass: list every curvature component of the simple metric; extract all **local** second-order action candidates with definite shift weight; prove completeness under stated class (no free \(D_A\)); show none non-SQ **or** exhibit one **forced** non-SQ density. |

Neither thread invents an edge field.  
Either can **falsify** “bulk geometric action as we wrote it is the macro \(c\)-edge.”

---

## Plain summary

**Fork F1 (strict shift in the action):** the field equation is basically Coulomb. Clean and unique. It will **never** run dilation to infinity for a \(c\)-like wall; the \(c\)-story has to live in the **redshift law / kinematics / observers**, not in that bulk EL.

**Fork F2 (shift only in the metric):** we *may* break shift in the bulk, but the break we actually derived **shuts itself off** as dilation deepens — so it also fails the \(c\)-test. We have **not** yet found a derived bulk piece that gets **stronger** as you approach the edge.

**Both say:** metric OK; **current operators wrong for a bulk \(c\)-edge**; no free \(D_A\); no hand wall.

**Next:** run **F1-next** and **F2-next** tiles above (can do F1-next immediately as a short closed writeup; F2-next is the heavier completeness pass).
