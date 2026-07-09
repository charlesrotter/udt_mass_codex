# ⚠ PRINCIPLE-7 / join note (2026-07-09)

Mass-lock faces that quote \(M\leftrightarrow X\) via Misner–Sharp \(2GM/c^2\) are **GR-form conditional** — see  
`simple_metric_mass_xmax_cascade.md` banner + `simple_metric_WR_L_external_triple_blind_audit_results.md`.  
Do not present as native UDT prediction. WR-L selects residual form \(A=1-r/X\), not this mass packaging.

---

## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 |
| **Mode** | DERIVE / OBSERVE |
| **Slice scope** | Charles J1 posture; static SSS; full light; N=1580 Pantheon+ STAT+SYS |
| **Observing or targeting?** | OBSERVE residual under **fixed** model — no retune, no P_ell switch |
| **Comparator scaffolds** | LCDM Om=0.3 residual **reference only** — not target |
| **Verifier status** | SELF-SCRIPT: `python3 simple_metric_hyperbolic_J1.py` · `python3 simple_metric_J1_R2_characterize.py` |
| **Build-on grade** | **CONDITIONAL** (on J1 CHOSE + full light DERIVED + MS form for mass) |
| **Re-run commands** | same as Verifier status |

### Premise ledger

| Item | Role | Tag | Enters claim? |
|------|------|-----|---------------|
| J1 \(D_A=r=x\) | sphere size = composition distance | **CHOSE (Charles intuition)** | Y |
| \(x=X\tanh\phi\), \(1+z=e^{\phi}\) | hyp form | POSTULATE + DERIVED form | Y |
| \(d_L=(1+z)^2 D_A\) | full light | DERIVED (static) | Y |
| \(X=2GM/c^2\) | mass lock | CONDITIONAL (J1+MS GR-form) | Y as relation |
| Absolute \(X\) from SNe+\(M_B\) | scale pin | CALIBRATION / CHOSE \(M_B\) | Y as labeled |
| LCDM Om=0.3 | residual yardstick | SCAFFOLD | N as theory |

### What is NOT claimed

- Physics canon. Beat LCDM. Multi-tension already solved.
- P_ell as live model. Half light. Free \(D_A\).

### Do not build on

- Treating Pantheon-calibrated \(X\) as pure metric prediction.
- Switching join for χ².

---

# Build: live hyperbolic model under J1 + full light

**Code:** `simple_metric_hyperbolic_J1.py` (canonical maps)  
**R2:** `simple_metric_J1_R2_characterize.py` · `simple_metric_J1_R2_characterize_out.json`

---

## Learning notes (short)

| Symbol | Plain meaning |
|--------|----------------|
| \(\phi\) | How deep dilation is (adds when dilations compose) |
| \(x\) / \(r\) under J1 | Same number: “how far” **and** sphere-size label |
| \(X=x_{\max}\) | Ceiling on that sphere-size distance (like \(c\) for speed) |
| \(1+z=e^{\phi}\) | Stretch of light / clocks |
| \(d_L=(1+z)^2 x\) | Brightness distance = sphere size × **two** stretch factors |
| \(M_{\mathrm{tot}}=c^2 X/(2G)\) | Total mass tied to that ceiling **if** J1+MS form |

---

## What was built

### 1. Canonical module API

```text
x_of_z(z, X)      → sphere/composition distance
DA_of_z = x_of_z  → J1
dL_of_z(z, X)     → full light (1+z)² DA
DM_of_z           → (1+z) DA  (Etherington name only)
M_tot_of_X / X_of_M_tot
HyperbolicJ1Model(X_Mpc)
```

Self-check: identities + low-\(z\) series feel \(d_L/X \approx z+\tfrac32 z^2\).

### 2. R2 residual (fixed model, 1 offset)

| Model | χ²/dof | RMS |
|-------|-------:|----:|
| **J1 + full light** | **2.17** | 0.307 |
| LCDM ref (not theory) | 0.88 | 0.154 |

**Trend (characterize):** low \(z\) mean residual \(+\); high \(z\) more negative → model **over-distances** at high \(z\) under full light (same scar as earlier hyp J1 tile).

**Shape vs LCDM ref (norm \(z=0.05\)):** \(\Delta\mu \sim +0.07\) at \(z=0.1\) → \(+1.4\) at \(z=2\) (J1 larger \(d_L\)).

### 3. Scale pin (calibration, not pure derive)

With conventional \(M_B=-19.25\) (CHOSE):

| | |
|--|--|
| \(X\) | \(\approx 3600\,\mathrm{Mpc}\) |
| \(M_{\mathrm{tot}}\) (J1 lock) | \(\sim 3.8\times 10^{22}\,M_\odot\) |

Label: **Pantheon-calibrated under J1 + full light + \(M_B\) convention.**

---

## Status vs success bar

| Bar | Status |
|-----|--------|
| One geometric story (J1 + hyp + full light) | **Building** |
| Multi-tension demonstrated | **Not yet** |
| Must beat LCDM SNe | **Not required** — residual is known homework |
| Hygiene | J1 CHOSE by Charles; residual not used to flip join |

---

## Next build steps (same posture)

1. Multi-probe: \(D_A=x\), \(D_M=(1+z)x\) under this stack vs BAO **transverse** products (careful with survey conventions).  
2. Local/weak-field feel of \(\phi\sim x/X\).  
3. Tension list (what this stack *can* speak to) — MAP, not claims.  
4. Optional: commit module tests in `tests/` for identities only.

---

## One-line

**Live code + R2 baseline under Charles J1: full light hyperbolic with \(D_A=x\); SNe shape residual still stiff at high \(z\) (χ²/dof~2.17); scale \(X\sim 3.6\,\mathrm{Gpc}\) is calibration; refine under this posture, don’t join-shop.**
