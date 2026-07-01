# G↔P Matching at the Seal — junction conditions (dilation-flux + transverse-momentum)

**Date:** 2026-07-01. **Provenance:** driver derivation; CAS anchors (`verify_seal_matching.py`); Charles
corrected the parity section (see below); blind-adversarial verifier recorded below. **Status:** JC1 + JC2
DERIVED; the seal-parity section is a CLASSIFICATION (two seal classes), NOT an adjudication. NOT canon.
**Builds on:** `native_geometric_action_results.md` (the native action + G/P weight `W_χ`).

## Setup
The seal `S` at `r=r_s` joins **interior `r<r_s` = Branch P** (χ pinned — the seal's fixed transverse area √A is
the pinned angular scale that switches on P) to **exterior `r>r_s` = Branch G** (χ free). Same native skeleton
`S_geo=∫c√h[(Z_φ/2)φ'² + R^{(2)} + W_χ𝒦]`, with `W_χ=e^{2φ}` (G) / `1` (P). Junction conditions from
`δ(S_P + S_seal + S_G)=0` including on `S` (Category-A: GR junction/Israel formalism, transformed).

## JC1 — dilation-flux continuity (DERIVED)
The only φ'-term is the kinetic, so δφ gives the boundary momentum `Π_φ = √h Z_φ φ'`. Source-free matching:

    [ √h Z_φ φ' ] = 0     (continuous across the seal)

For round `h=r²Ω`, constant `Z_φ`, and the exterior-G solution `φ = φ_∞ − q/r` (so `r²φ' = q`):

    q = (r²φ')|_seal          [round-specific: √h∝r²; general-h needs a redefined charge]

(Operative fact for the G-exterior `(r²φ')'=0`: `e^{2φ}𝒦` is φ-INDEPENDENT so it drops from the φ-variation — the
`R^{(2)}+e^{2φ}𝒦=0` cancellation is the h-sector on-shell statement, sufficient but not what the φ-equation needs.)

**The exterior public charge q IS the interior dilation flux through the seal.** (Native realization of the canon
public charge Q = Misner–Sharp mass = 2p_F.)

## JC2 — transverse-momentum continuity (DERIVED, modulo sign convention)
The momentum conjugate to `h_AB` from the `𝒦` term:

    π^{AB} = c√h W_χ e^{-φ} (K^{AB} − K h^{AB})          [K_AB = ½e^{-φ}∂_r h_AB]

Source-free matching `[π^{AB}]=0`; with `h_AB`, φ continuous and `W_χ: 1→e^{2φ}`:

    (K^{AB} − K h^{AB})_P = e^{2φ_s} (K^{AB} − K h^{AB})_G       (at the seal, source-free)

With a seal surface stress:  `[π^{AB}] = S^{AB}_seal`  (Israel condition). The `e^{2φ}` weight-jump is the G/P
interface signature. **Assumption (stated):** the clean `e^{2φ_s}` relation needs φ AND h continuous across the seal
(so the common `c√h e^{-φ}` cancels) — the standard junction posture (values continuous, normal derivatives may jump).

## Seal parity — TWO SEAL CLASSES (a classification, NOT "Neumann true / Dirichlet false")
Corrections (Charles 2026-07-01) to the driver's first pass:
- **Time reversal `t→−t` does NOT impose radial Neumann.** It only says `g_tt=−e^{-2φ}c²` is even under `t→−t`
  (already true); it does not determine RADIAL parity of φ. (Driver error: conflated time-reversal with radial parity.)
- **The charge is the NORMAL DERIVATIVE flux `q=r_s²φ'(r_s)`, not the value `φ(r_s)`.** So Dirichlet `φ(r_s)=0`
  PERMITS `q≠0` but does NOT force it (driver overclaim "Dirichlet ⇒ charged" retracted).

The two source-doc positions on φ(seal) are therefore two distinct PHYSICAL SEAL CLASSES, not rival answers:
- **Class A — smooth source-free spatial mirror fold.** A genuine smooth reflection in the radial normal imposes
  EVEN radial parity → `φ'_n(r_s)=0` (Neumann) → by JC1, `q=0` → **CLOSED cell** (no exterior field).
  (This is the `seal_junction_condition_results.md:69` even→Neumann reading.)
- **Class B — pinned / charged seal.** Dirichlet `φ(r_s)=0` (or another constraint) + nonzero seal flux
  `φ'_n(r_s)≠0` → `q≠0` → **CHARGED cell** (exterior Coulomb tail). The nonzero flux requires a seal source, a
  boundary constraint permitting `φ'_n≠0`, or a non-smooth/non-reflection junction. (This is the
  `D1_FIX_DESIGN.md` odd/Dirichlet reading — a *different physical setup*, not a contradiction of Class A.)

**Safe banked statements:**

    smooth source-free mirror fold  ⇒  Neumann φ'_n=0  ⇒  q=0  (closed cell)
    charged public cell             ⇒  Π_φ ≠ 0        ⇒  seal source / constraint required

Do NOT bank "Neumann true, Dirichlet false." Which cell type is which (universe vs matter) is a physics/canon call
(Charles holds) — NOT adjudicated here.

## Physical interpretation (banked)
**External mass/charge `q` is NOT bulk matter — it is SEAL FLUX.** The native chain:

    n → h_AB → 𝒦 → φ → Π_φ|_seal → q_exterior

Matter shapes the transverse geometry and the seal; the cell's externally-visible charge is the dilation flux the
seal emits. (φ-blind bulk matter + seal-flux charge — consistent with the field-eq result that matter doesn't
directly source φ.)

## Premise ledger
| item | status |
|---|---|
| JC1: [√h Z_φ φ']=0; round → q=(r²φ')_seal | DERIVED (CAS) |
| JC2: π^{AB}=c√h W_χ e^{-φ}(K^{AB}−K h^{AB}); [π^{AB}]=0 (or =S_seal) | DERIVED (CAS + chain rule) |
| smooth mirror fold ⇒ Neumann ⇒ q=0 (Class A) | DERIVED (given smooth radial reflection) |
| charged cell ⇒ Π_φ≠0 ⇒ seal source/constraint (Class B) | DERIVED |
| time-reversal ⇒ radial Neumann | **RETRACTED** (does not follow) |
| Dirichlet ⇒ q≠0 | **RETRACTED** (Dirichlet permits, not forces) |
| which cell (universe/matter) is Class A vs B | OPEN — physics/canon (Charles) |
| seal location r_s / χ-pinning by the seal | inherited (finite-cell canon) |

## VERIFIER
- **CAS (driver, `verify_seal_matching.py`):** Π_φ=√h Z_φφ'; round q=(r²φ')_seal; π^{AB} form + e^{2φ} weight-jump;
  the parity/flux consequences. Confirmed (parity section then corrected per Charles as above).
- **Blind-adversarial (agent `ae23eafbea66d9a34`, 2026-07-01, independent sympy on explicit 2×2 h + fresh logic):**
  ALL claims **CONFIRMED, none refuted** — including the two RETRACTIONS (time-reversal⇏Neumann; Dirichlet⇏charged,
  the latter "conflated temporal and radial normals" / "a non-sequitur"). π^{AB} form matches on all 3 independent
  components; 𝒦∝e^{-2φ} identically. Scope flags folded in above: (i) G-exterior needs e^{2φ}𝒦 φ-INDEPENDENT (not the
  =0 per se); (ii) JC2 needs φ+h continuous; (iii) q=(r²φ')_seal is round-specific; (iv) Class A's q=0 rests on the
  even-parity fold being the physical seal topology (a modeling input, the load-bearing A/B distinguisher).

## OPEN (next)
- Which physical cell (universe vs matter) realizes Class A (closed) vs Class B (charged); the seal source that
  charges a matter cell (couples through the seal's transverse geometry — the φ-angular structure).
- Then a constrained-two-player SOLVER (interior P + exterior G + these junctions), gated behind the Z_φ fork.
