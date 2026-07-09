# RESULT — Lorentz / Doppler clue for the full light rule


## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-09 (header retrofit / original work date may differ) |
| **Mode** | DERIVE |
| **Slice scope** | static SSS light count; self-script verify_lorentz_light_clue.py |
| **Observing or targeting?** | OBSERVE |
| **Comparator scaffolds** | NONE |
| **Verifier status** | SELF-SCRIPT or NONE — see body; not blind-pass unless stated |
| **Build-on grade** | **CONDITIONAL** |
| **Re-run commands** | see body / associated `*.py` if any |

### Premise ledger

| Item | Role | Tag | Enters claim? |
|------|------|-----|---------------|
| See body of this document | full ledger in sections | mixed — re-read body | Y |

### What is NOT claimed

- Physics canon (Charles only). Hygiene grade ≠ nature proof.
- Claims wider than **Slice scope** above.

### Do not build on (if any)

- Anything tagged CHOSE/explore in the body without re-stating premises.

---

**Date:** 2026-07-09 · **Mode: DERIVE (validator)**  
**Script:** `verify_lorentz_light_clue.py` (all asserts PASS)  
**Companion:** `verify_luminosity_distance_n2.py` (re-run OK)  
**Status:** PROVISIONAL derivation tile — **not** a SNe win; not a profile claim.

---

## Lay summary (read this first)

In ordinary special relativity, when a light source recedes, two things happen together:

1. each photon is **weaker** (redder), and  
2. photons **arrive less often** (clocks / crest rate).

Brightness feels **both**. Counting only one is a half-relativistic mistake.

On our **static** UDT metric the same pair appears for stationary source and observer: energy stretch and arrival-rate stretch are **the same factor**. Putting them together (plus area geometry) is the **full light rule**. The old SNe formula kept only **one** of those stretch hits — that is the **root** error, in Lorentz language.

This tile **does not** fix the sky fit. It only **secures why** the full rule is the relativistic one.

---

## What was validated (CAS)

### Part 1 — SR longitudinal Doppler

- \(1+z = \sqrt{(1+\beta)/(1-\beta)}\) (recession).  
- Energy factor \(=1/(1+z)\).  
- Rate factor \(=1/(1+z)\) (frequency = crest rate).  
- Product \(=1/(1+z)^2\).  
- Half-count \(=1/(1+z)\) only.

### Part 2 — UDT static simple metric

Same structure as banked n=2 derive:

| Hit | UDT result |
|-----|------------|
| Energy | \(1/(1+z)\) |
| Arrival rate | \(1/(1+z)\) **identical** |
| Product | \(1/(1+z)^2\) |
| + area reciprocity | \(d_L=(1+z)^2 D_A\) **full rule** |
| Half rule | \(d_L=(1+z)D_A\) **old SNe** |

**Lorentz clue on UDT:** energy factor **equals** rate factor (static metric); cannot drop one without dropping the redshift law itself.

### Part 3 — Dictionary

| Name | Formula | Meaning |
|------|---------|---------|
| Full light rule | \(d_L=(1+z)^2 D_A\) | energy × rate × area reciprocity |
| Half light rule | \(d_L=(1+z)D_A\) | old SNe validator |
| Root | half on a full theory | missing one stretch hit |
| Lorentz clue | SR already needs energy×rate; UDT static same | root = half-Doppler flux |

### Part 4 — Weak stretch

Both SR (small \(\beta\)) and UDT (\(1+z=e^{h}\), small \(h\)):

\[
\text{energy}\times\text{rate} = 1 - 2h + O(h^2).
\]

Same leading Lorentz structure.

### Part 5 — Pedagogy only (fixed \(D_A=1\))

| \(z\) | half \(d_L\) | full \(d_L\) | full/half |
|------:|-------------:|-------------:|----------:|
| 0.01 | 1.01 | 1.02 | 1.01 |
| 0.10 | 1.10 | 1.21 | 1.10 |
| 0.50 | 1.50 | 2.25 | 1.50 |
| 1.00 | 2.00 | 4.00 | 2.00 |
| 2.00 | 3.00 | 9.00 | 3.00 |

Ratio full/half \(=1+z\). Farther out, the missing factor hurts more — why a half-rule fit can look fine nearby-ish and still be wrong in principle.

---

## What this does / does not claim

| Claims | Does not claim |
|--------|----------------|
| Full rule matches SR’s double hit on flux | New SNe χ² victory |
| Root = half of that double hit | Profile \(\phi(r)\) is known |
| Weak field same \(1-2h\) structure | Ball-center / relational settled |
| Old SNe short by exactly one \((1+z)\) in \(d_L\) | Etherington can be dropped |

---

## How to re-run

```bash
python3 verify_lorentz_light_clue.py
python3 verify_luminosity_distance_n2.py
```

---

## One-line

**The root is a half-Lorentz light count: SR and static UDT both require energy×rate (product \(1/(1+z)^2\)); the old SNe rule kept only one factor; full light rule restores both (plus area) as \(d_L=(1+z)^2 D_A\).**
