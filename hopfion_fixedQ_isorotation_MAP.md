## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-10 |
| **Mode** | MAP / CHARTER — next mass-lane step after G/P exterior probe |
| **Parent** | `hopfion_GP_exterior_probe_results.md` · `threadB_timelive_linear_nogo_and_finite_amp_MAP.md` · `hopfion_mass_background_coupling_MAP.md` |
| **Object** | H3 \(Q_H=1\) hopfion ONLY — never f2d hedgehog |
| **Observing or targeting?** | OBSERVE persistence / scale equilibrium under fixed target charge — not SM mass |
| **Build-on grade** | MAP — Phase 0 DEMO may bank as DEMO; Phase 1+ need verify |

### Premise ledger

| Item | Tag |
|------|-----|
| H3 field exists (FS flat, Outcome A) | BANKED |
| Native Branch-P exterior flux drifts (static reciprocal) | BANKED `hopfion_GP_exterior_probe_results.md` |
| S² carrier | POSIT |
| \(L_2+L_4\) minimal | CHOSE ( \(L_6\) open) |
| Target-space U(1) isorotation at fixed charge \(Q\) | WORKING ansatz (lead) |
| Collective scale \(R\) reduction | DEMO layer first |
| Full metric backreaction \(A,B,C\) | Phase 2 — not Phase 0 |
| G/P switch | Still underived — mass readout conditioned on exterior |

---

# Fixed-\(Q\) isorotation from H3 — phased program

## Why this is NEXT

G/P exterior probe: static reciprocal + native P ⇒ **boxy exterior flux**.  
Linear time-live on hedgehog ⇒ **no growing mode**.  

So the mass lane continues at **finite time structure that keeps \(\Sigma_\phi>0\)** without pretending static P has a Coulomb mass. Fixed target charge is the cleanest reduced route that:

- stays native to the carrier action,  
- can be stationary in the stress while \(\mathbf n\) rotates,  
- continues from **banked H3**, not a new object.

---

## Ansatz (Phase 0–1)

\[
\mathbf n(T,\mathbf x)=R_{\hat a}(\omega T)\,\mathbf n_\omega(\mathbf x),
\]

with \(\mathbf n_\omega\) in the \(Q_H=1\) sector (seed from H3).  
Conserved target charge \(Q\) (Noether of residual U(1)).

Collective scale (from \(\mathbf n_R=\mathbf n_0(\mathbf x/R)\)):

\[
E_Q(R)=E_2 R+\frac{E_4}{R}+\frac{Q^2}{2\bigl(I_2 R^3+I_4 R\bigr)}.
\]

H3 banked: \(E_2/E_4\simeq 0.9995\) (virial ~1%). Moments \(I_2,I_4\) from profile integrals (Phase 0b from field or seed).

---

## Phases (do not skip)

### Phase 0 — Collective DEMO (this session / CPU)

1. Normalize banked virial ratio; pick gauge \(\xi=\kappa=1\).  
2. Scan \(E_Q(R)\) for \(Q\in\{0,1,2,5\}\) (or continuous).  
3. Report \(R_Q=\mathrm{argmin}\,E_Q\), \(E_Q''(R_Q)\).  
4. **Grade: DEMO** — existence of finite-\(R\) minimum in the reduced energy, not a PDE solution.

### Phase 1 — Stationary isorotation PDE (flat FS first)

1. Freeze metric flat (\(N=0\) ambient as H3).  
2. Solve for \(\mathbf n_\omega\) at fixed \(\omega\) (or fixed \(Q\)) by continuation from H3 \(\omega=0\).  
3. Measure \(Q\), energy, localization, \(\langle\Sigma_\phi\rangle\) proxy from \(\partial_T\mathbf n\).  
4. Pre-register: holds \(Q_H\approx 1\); does not unwind; energy finite.

### Phase 2 — Metric backreaction

1. Drop pure \(B=1/A\) interior requirement if \(\rho+p_r>0\).  
2. Couple \(\phi\) (and needed metric DOFs) to \(\langle\Sigma_\phi\rangle\) / stress.  
3. Revisit exterior class (plateau vs drift) **with** time-averaged source — may differ from static P vacuum.

### Phase 3 — Exterior branch honesty

Only after Phase 1–2: re-ask G vs P with the self-consistent source, not the frozen static probe alone.

---

## Pre-registered tests (Phase 0)

| ID | Pass/fail (characterize) |
|----|---------------------------|
| **P0-T1** | For \(Q>0\), does \(E_Q(R)\) have a finite interior minimum? |
| **P0-T2** | Is \(E_Q''(R_Q)>0\) (stable against scale kicks)? |
| **P0-T3** | As \(Q\to 0\), does \(R_Q\to R_*\) of pure Derrick \(E_2=E_4\)? |

## Red

- Claim SM mass or lepton wall from \(R_Q\).  
- Use hedgehog f2d field.  
- Skip to Phase 2 without Phase 1.  
- Treat DEMO as full UDT solution.  
- Cherry-pick δm / G-control flux as the mass.

---

## One-line

**After boxy static P exterior: continue mass lane with fixed-Q isorotation from H3 — Phase 0 collective \(E_Q(R)\), then PDE, then metric; not more static reciprocal probes.**
