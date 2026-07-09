## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 |
| **Mode** | MAP + OBSERVE (CAS); DERIVE only forced ledger |
| **Slice scope** | simple metric; bulk action candidates; R1 / angular / EH; no SNe |
| **Observing or targeting?** | **OBSERVE** what is forced vs free — not targeting package glue or edge |
| **Comparator scaffolds** | none |
| **Verifier status** | SELF CAS session (EL identities; shift weights) |
| **Build-on grade** | **LEAD** (honesty map) — native package still OPEN |
| **Re-run commands** | re-run CAS blocks in `simple_metric_S9_native_action_honesty.py` |

### Premise ledger

| Item | Tag | Forced? |
|------|-----|---------|
| Simple metric (R1–R3 + areal \(r\)) | THEORY | yes (frame) |
| \(\sqrt{-g}\propto r^2\) (indep. of \(\phi\)) | DERIVED | yes |
| R1 kinetic \(\propto r^2(\phi')^2\) | shift-clean candidate | **candidate**, not sole bulk |
| \(W\) on \(\mathcal{K}\): \(e^{2\phi}\) vs \(1\) | FORK | **no** |
| \(Z\) overall scale | FREE | no |
| \(L_m=-\rho r^2 e^{-2\phi}\) | CHOSE probe | no |
| 4D EH on ansatz | GR-form mine | **not** forced by R1 |
| Preferred package E vs A | OPEN | no |

### What is NOT claimed

- Native UDT bulk is R1-only, or EH-only.
- Packages glued.
- \(c\)-edge solved.

### Do not build on

- “EH EL for φ picks cosmology” (see §3 — EL≡0).
- Mechanism to merge R1 and Einstein maps.

---

# S9 — Native action honesty on the simple metric

**Prior:** zoom-out — two solution maps (E / A) from two packages.  
**Ask:** what does the **metric + UDT principles** actually force in the bulk action, and what is still a fork?

---

## Lay summary

We asked a boring, necessary question:

> On this metric, what pieces of an action are **forced**, and what did we only **choose**?

**Forced (or nearly):**  
the metric form; the volume factor; if you want “only differences of depth matter,” the clean kinetic for \(\phi\) is the R1 one.

**Not forced:**  
whether angular mismatch is compensated or not; the overall kinetic strength \(Z\); the matter coupling; and whether you work as a **φ-only variational theory** or as **Einstein equations on the metric**.

**Surprise (important):**  
if you take the ordinary curvature action (Einstein–Hilbert), **restrict to this metric**, and try to vary only \(\phi\), the bulk equation is **empty** (identically zero).  
So the geometry/continuum map (E-primary) is **not** “the EL of φ from EH.” It is “**Einstein’s equations on this ansatz**” — a different kind of package.  
The thin R1 theory **is** a genuine φ EL package.

That is honesty, not a fix. Native UDT still has to say which package (or what third) the positional-dilation principle actually wants.

---

## 1. MAP — whole action question

**Arena (forced by frame):**
\[
ds^2=-e^{-2\phi}c^2 dt^2+e^{2\phi}dr^2+r^2 d\Omega^2
\]

**Candidate bulk (from SIMPLE_METRIC_MACRO):**
\[
S\supset\int\sqrt{-g}\Big[\tfrac{Z}{2}e^{2\phi}g^{rr}(\phi')^2 + R^{(2)} + W(\phi)\,\mathcal{K} + L_m\Big]
\]

| Piece | Origin | Shift \(\phi\to\phi+c\) | Status |
|-------|--------|------------------------|--------|
| Measure \(\sqrt{-g}\propto r^2\) | metric | invariant | **DERIVED** |
| R1 kinetic \(\propto(\phi')^2\) | shift-clean dilation kinetic | **invariant** | **candidate forced if bulk R1 exact** |
| \(R^{(2)}=2/r^2\) | sphere | invariant | geometric |
| \(\mathcal{K}\propto -e^{-2\phi}/r^2\) | angular mismatch | weight \(e^{-2c}\) | geometric |
| \(W=e^{2\phi}\) | compensation | \(\Rightarrow W\mathcal{K}\) invariant; cancels \(R^{(2)}\) | **FORK** |
| \(W=1\) | uncompensated | bulk \(\propto e^{-2\phi}\) | **FORK** |
| \(Z\) | scale | — | **FREE** |
| \(L_m\propto -\rho e^{-2\phi}\) | dilation-weighted matter probe | weighted | **CHOSE probe** |
| 4D \(R\) (EH) | full curvature | not pure shift | **GR mine**, not R1-forced |

---

## 2. CAS observations (vacuum)

### Shift weights
- R1 kinetic density: **invariant**  
- \(\mathcal{K}\): \(\times e^{-2c}\)  
- \(e^{2\phi}\mathcal{K}\): **invariant** (cancels with \(R^{(2)}\) pointwise)  
- \(e^{-2\phi}\): \(\times e^{-2c}\) (uncompensated / SQ tendency)

### EL for φ (reduced \(\int dr\,L\))

| Bulk \(L\) | EL character | Vacuum solutions (known) |
|------------|--------------|---------------------------|
| R1 only | \((r^2\phi')'=0\) | **Coulomb** \(\phi=a-q/r\) |
| R1 + uncomp \((-2e^{-2\phi})\) | \(Z(r^2\phi')'=4e^{-2\phi}\) | self-coupled; not Coulomb |
| Compensated angular | same as R1 only | Coulomb |
| **\(\sqrt{h}\,R_{4D}\) (EH reduced)** | **EL \(\equiv 0\)** | **no bulk φ equation from vary-φ only** |

### Reading the EH≡0 fact

On the **simple metric family**, pure Einstein–Hilbert reduced to \(\phi(r)\) is a **total-derivative / constraint** object for φ-variation: it does **not** generate a φ field equation.

So:

| Package | What it actually is |
|---------|---------------------|
| **A-primary (R1)** | True **variational** theory for \(\phi\) on this chart |
| **E-primary (Einstein/MS)** | **\(G_{\mu\nu}=8\pi T_{\mu\nu}\)** imposed on the ansatz (one free function \(A=e^{-2\phi}\)); continuum map S5–S6; identity \(p_r=-\rho\) |

They were never “two EL’s of one action with different ρ.”  
They are **different problem types**. Dialing critical mass cannot turn one into the other.

---

## 3. What UDT principles force vs leave open

| Principle (elegant frame) | Pressure on action |
|---------------------------|-------------------|
| Positional dilation in **metric** | Metric box forced; redshift \(e^{\Delta\phi}\) |
| R1 “only differences of depth” | Favors **shift-clean bulk** ⇒ R1 kinetic + compensated angular (or no angular bulk) |
| Reciprocity R3 | Already in metric \(A\cdot g_{rr}=1\) |
| \(c\)-like edge / dilation barrier | **Tensions with** pure shift-clean vacuum (Coulomb, no outer wall) — known; not solved by fudge |
| “Don’t import GR form” | EH/MS is **allowed as mine/reference**, not auto-native |
| Continuum matter | \(L_m\) and \(T_{\mu\nu}\) still **OPEN** (dilated dust was probe) |

**Honest fork table (still open):**

1. **Bulk shift exact?** yes → A-primary Coulomb vacuum; edge not from that vacuum EL.  
2. **Bulk may break shift** (uncompensated / other weight)? → different EL; must be **derived**, not shopped for edge.  
3. **Work in Einstein constraint language** on the metric? → E-map; walls + critical mass; \(p_r=-\rho\); native status OPEN.  
4. **Something else** (full metric free, different matter sector, dynamics)? unentered in this static simple cut.

---

## 4. Link to solution spaces already mapped

```
                 simple metric (forced)
                        |
        +---------------+----------------+
        |                                |
  vary φ in R1(+forks)           impose G=8πT on ansatz
        |                                |
   A-primary map (S7)              E-primary map (S5–S6)
   Coulomb vacuum                  critical walls, p_r=-ρ
   ρ_EL catalog                    continuous p/α map
        |                                |
        +-------- not the same EL -------+
```

**Critical matter** lives cleanly on the **right** branch (closes sphere).  
**R1 residual on ceiling** is the statement that the ceiling is an **E-branch** object, not an A-branch solution.

---

## 5. What is *not* next (red)

- Add a term so R1 hosts \(A=1-r/X\).  
- Fit \(p\) or \(W\) to Pantheon.  
- Declare EH native because SNe residual looked soft.  
- Declare R1 native because shift is pretty — without facing edge tension.

---

## 6. What *is* next (green)

1. **Ponder with Charles:** is macro work **φ-variational (A)** , **Einstein-on-ansatz (E)**, or a **native third** (derive bulk weight from dilation principle more tightly)?  
2. If E: continue continuum **census only** (already strong); continuum \(T_{\mu\nu}\) meaning of \(p_r=-\rho\).  
3. If A: derive **which** shift-breaking (if any) is forced — not shop uncompensated for edge.  
4. If third: MAP full free metric / nonstatic before freezing simple static.

---

## One-line

**Native honesty: metric and shift-clean kinetic are solid; angular weight and matter are forks; EH reduced to φ has empty EL so E-primary is Einstein-on-ansatz not “φ from EH”; A-primary is real φ-variational R1 space — packages differ by problem type; native choice still OPEN, no glue.**
