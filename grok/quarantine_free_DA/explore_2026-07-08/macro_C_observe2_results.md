# OBSERVE-C2 — Matter ball → vacuum exterior (fallback C)

**Date:** 2026-07-08  
**Lock:** `macro_FE_LOCKED_C.md`  
**Script / data:** `macro_C_observe2.py`, `macro_C_observe2_data.json`  
**Prior:** C1 (throats pinch; expanding+matter open).  
**Status:** PROVISIONAL characterization. OBSERVE, not sky-fit.

---

## Premise ledger

| Item | Tag |
|------|-----|
| C packaging | CHOSE |
| ρ compact on \([0,R_m]\), zero outside | FREE profile shape |
| Near-center seed: \(r_0=0.05\), \(D_0=r_0\), \(v_0=1\), \(u_0=0\), \(\phi_0=0\) | FREE IVP (regular-ish polar start) |
| Z scan | FREE |
| Observing or targeting? | **Observing** |

---

## Setup

Integrate outward through a **matter ball**, then into **vacuum**:

- Inside: dilated source builds \(G = D^2\phi'\)  
- Outside: \(G\) must stay **constant** (C vacuum law)  
- Ask: do we get clean exteriors? pinch? what do \(D,\phi\) do?

---

## Main results

### 1. Clean ball → exterior in the whole scanned grid

| Count (this script) | |
|---------------------|--|
| ok | 31 |
| pinch | **0** |
| reached vacuum ext | 31 |
| G conserved in ext (tag) | 30 (+1 tiny drift 3e−6) |

**G drift** in exterior typically \(10^{-9}\)–\(10^{-8}\) (numerics).

**Plain:** under C with this seed class, a compact dilated ball **does** produce a vacuum exterior with the conserved flux C promises. No B-style pinch epidemic.

### 2. Matter loads the exterior “charge” \(G|_{R_m}\)

For \(Z=1\), \(R_m=2\):

| ρ₀ | \(G(R_m)\) | \(D(R_m)\) | φ(end r=40) |
|----|------------|------------|-------------|
| 0 | 0 | 2.00 | 0 |
| 0.5 | 1.24 | 2.21 | 0.88 |
| 1 | 1.91 | 2.34 | 1.31 |
| 2 | 2.65 | 2.48 | 1.80 |
| 5 | 3.49 | 2.67 | 2.46 |
| 10 | 3.91 | 2.78 | 2.94 |
| 20 | 4.10 | 2.85 | 3.39 |

More matter → larger exterior \(G\) (monotonic in this box), larger φ rise. Saturating trend at high ρ₀.

### 3. Exterior kinematics (what it is — and isn’t)

In vacuum exterior: \(\phi' = G / D^2\), \(D'' = -(Z/4) D (\phi')^2 = -(Z/4) G^2 / D^3\).

In **all** successful runs here:

- \(D\) **keeps growing** through the exterior (e.g. to \(r=100\), \(D\sim 120\)–\(130\))  
- \(\phi'\) **shrinks** as \(D\) grows (\(G\) fixed)  
- \(\phi\) approaches a **slow climb / near-floor**, not a pinch  

**Not observed:** asymptotic constant \(D\) (Schwarzschild-like areal freeze), nor Coulomb-in-\(r\) with frozen \(D=r\).  
**Scoped:** free-\(D\) C exterior with this seed is an **opening geometry** carrying constant \(G\), not a static star exterior template.

### 4. \(Z\) effect (\(R_m=2\), ρ₀=5)

Larger \(Z\) → milder φ end, larger \(D\) growth (stiffer kinetic / weaker φ response for same G loading pattern). \(G(R_m)\) non-monotone mild (2.86→4.50→4.08 across Z=0.5…8).

### 5. Vacuum control ρ=0

\(G\equiv0\), \(\phi\equiv0\), \(D \approx r\) from the seed — pure expanding chart, no dilation. Matter is what turns φ on (C’s design).

---

## Contrast to B and to C1 throats

| Setup | Typical fate |
|-------|----------------|
| B vacuum throat | hard/soft weirdness |
| B dilated on throat | worse pinch |
| C vacuum throat | both signs pinch |
| **C ball → exterior (this tile)** | **stable open runs, G conserved outside** |

C2 is the first tile that looks like a **coherent division of labor**: matter ball sets \(G\); vacuum carries it out; no angular self-sourcing of φ.

Still **not** “the observational universe” — especially while \(D\) runs away outward.

---

## What this does *not* say

- Not a mass–redshift law or SNe fit  
- Not uniqueness of ρ profile or center seed  
- Not that growing \(D\) is physical cosmology (could be chart / missing BC / missing pressure / wrong continuum)  
- Not that B is false forever — only parked  

---

## Solver-first note (growing D vs “want static exterior”)

If one *wanted* a static-looking exterior and didn’t get it:

1. Left out: outer BC, pressure, different \(L_m\), time dependence, gauge of \(r\)  
2. Numeric: unlikely (G conservation clean)  
3. Frozen: FREE seed \(v_0=1\), \(D_0=r_0\) **imposes expansion** — may dominate exterior  
4. Not whole space: one IVP class  

**Next honest probe:** vary center seed (\(v_0\), \(D_0\)) — can exterior \(D\) level or turn? **C3** candidate.

---

## Incremental next

1. **C3:** seed scan (\(v_0\), \(D_0/r_0\)) for fixed ball — when does exterior \(D\) grow / plateau / fall?  
2. Analytic vacuum exterior quadrature with fixed \(G\).  
3. Only later: data — if ever, after exterior class is understood.

---

## Plain summary

Under C, a ball of dilated matter with a simple open center seed **does** what it says on the tin: it charges up a conserved exterior flux \(G\), then empty space carries that flux outward without pinching off in our scans. Sphere size keeps opening, so this is not yet a static “star in a calm cosmos,” but it **is** the first setup where matter and vacuum play clear, non-weird roles — Mozart still not on the radio, but the band is at least playing in time.
