# Coupled Cell + Angular-Soliton on the Finite Matter Cell — Results

Date: 2026-06-14. Driver: Claude (Opus 4.8, 1M context). NEW file
(append-never-edit, Self-Hardening discipline). Mode: **OBSERVE** (the
project's primary mode). Frame: CRITICAL_UNIVERSE_FRAME.md / CATALOG_FRAME.md /
CANON C-2026-06-14-1. **DATA-BLIND, foundation-scoped** — NOT the gated
spectrum calculation. No mass/ratio extracted; no lepton/hadron wall number
loaded, matched, or consulted.

THE QUESTION (observe, not target): what makes UDT's angular knot a FINITE,
localized particle — the finite cell, the phi back-reaction, or both — and what
structure emerges from solving the coupled angular-source + dilation system on
the finite matter cell?

Scripts (commit-grade, this push; all V100 float64):
- `coupled_cell_soliton_B1.py` — CELL ONLY (phi fixed background).
- `coupled_cell_soliton_B2.py` — PHI ONLY (back-reacting phi, unbounded domain).
- `coupled_cell_soliton_B3.py` — BOTH (coupled cell + phi; + radial-profile shoot).
- `coupled_cell_soliton_derrick.py` — Derrick/scaling backing for B3b.

Blind verifier: **PENDING** (verifier-before-record; attack-here block at end).

DERIVED inputs (cited as given, from CANON C-2026-06-14-1 /
angular_lagrangian_results.md):
- Metric ds^2 = -e^{-2phi}c^2 dt^2 + e^{+2phi}dr^2 + r^2 dOmega^2; sqrt(-g)=c r^2 sin th.
- Hedgehog n=x/r: T^t_t=T^r_r=-xi/r^2, T^th_th=0 => rho=xi/r^2, p_r=-xi/r^2,
  p_theta=0, **p_r=-rho EXACT and phi-independent**.
- Radial twist Theta(r): p_r+rho = xi e^{-2phi}(Theta')^2 >= 0 (CANON D7).
- Back-reaction (t-eq): e^{-2phi} = 1 - kappa8 xi - rs/r (solid-angle deficit).
- Misner-Sharp: m(r) = (c^2 r/2G)(1 - e^{-2phi}) (macro_sector_fork_resolution.md:33).
- Native BCs: core regular turning point (depth p the integration parameter);
  seal mirror-fold (static sigma-EVEN -> NEUMANN, sigma-ODD -> DIRICHLET); bare
  measure r^2 sin th, stiffness K_r=e^{-4phi}, K_th=e^{-2phi}/r^2
  (wcc_results.md:50-51, offdiag_scan_results.md:61,64-65); cell size = FREE
  dimensionful input (#39 / STATE.md:66-69).

---

## B1 — CELL ONLY (phi fixed background, no back-reaction)

The hedgehog rho = xi/r^2 against the bare measure 4pi r^2 dr gives a
**CONSTANT integrand**: the 1/r^2 of the source is exactly cancelled by the r^2
of the measure. Hence

  **E_coord = INT_{r_core}^{r_int} (xi/r^2) 4pi r^2 dr = 4 pi xi (r_int - r_core).**

GPU-confirmed to machine precision over the scan (xi=0.01,0.1; (r_core,r_int) =
(1e-3,1),(1e-6,1),(1e-3,10),(0.1,1)): E_coord matches 4pi xi (r_int - r_core) to
all digits, and |p_r + rho|_max = **0.0e+00** (EOS stays exact, no radial
profile). The proper-volume energy (extra e^{+phi} weight) on a deep log
background phi = -p ln(r_int/r) is ALSO finite (integrand ~ (r/r_int)^p -> 0 at
the core for p>0): e.g. p=1 gives E_proper = 0.6283 = E_coord/2, convergent as
r_core -> 0.

FINDING B1: **The cell delivers finiteness.** E_coord is finite for any finite
cell, **continuous (linear) in the cell width**, with no pinned value — the
scale is set by xi (coupling) and the width (r_int - r_core), both free dials.
Notably there is **no 1/r_core divergence even as r_core -> 0**: the hedgehog's
1/r^2 is integrable against the r^2 measure. So the cell finitizes by
truncation, and the mass is **continuous in cell size** (no discreteness). The
EOS p_r = -rho stays exact (no radial profile is introduced).

## B2 — PHI ONLY (back-reacting phi, unbounded domain, NO cell wall)

Solving the Einstein t-equation self-consistently gives the closed-form
global-monopole metric e^{-2phi} = 1 - delta - rs/r with delta := kappa8 xi.
The Misner-Sharp mass (c^2/2G = 1 units) is

  **m(r) = r(1 - e^{-2phi}) = delta * r + rs.**

GPU scan (delta = 0.001, 0.01, 0.1; rs=0): m(r=1), m(r=1e3), m(r=1e6) track
delta*r exactly, and m(r)/r -> delta to all digits at r=1e6. The coordinate
energy integral independently diverges: E_coord(R) = 4 pi xi R -> infinity
(confirmed delta=0.01,0.1 at R=10,1e3,1e6). The source rho = xi/r^2 is scale-
free (no intrinsic length): e^{-2phi} -> 1 - delta = CONSTANT at large r (a
conical/deficit geometry), not a decaying localized lump.

FINDING B2: **phi back-reaction ALONE does NOT finitize.** M(r) = delta r + rs
**DIVERGES LINEARLY** without bound. phi supplies the solid-angle DEFICIT (the
B=1/A EOS, the conical geometry) but **not finiteness** — the global monopole is
a long-range angular defect, not a finite particle.

## B3 — BOTH (knot + self-consistent phi ON the finite cell)

**B3a (pure-hedgehog coupled cell, Theta=theta exact, p_r=-rho exact).** The
Einstein t-eq integrates to r(1-e^{-2phi}) = delta(r-r_core) + r_core(1-e^{-2p}),
with core depth e^{-2phi}(r_core) = e^{-2p} (p the integration parameter) and
interface BC phi(r_int)=0.

- **The interface BC does NOT close to phi=0 with rs=0:** m_areal(r_int) =
  delta(r_int-r_core) + r_core(1-e^{-2p}) is STRICTLY POSITIVE (both terms
  positive for delta>0, p>0), so phi(r_int) < 0, not 0. Hitting phi=0 at the
  interface **requires a negative Schwarzschild constant rs = -m_areal(r_int)<0**
  (a mass DEFECT). [OBSERVED, premise-attached: this is the seal-closure
  condition; it FIXES rs but does not pin (p, delta, r_int).]
- **Realized MS mass and scaling:** M_total = M_core + M_deficit, with
  M_core = r_core(1-e^{-2p}) and M_deficit = delta(r_int - r_core). The scan
  (p=0.5,1,2; delta=0.01,0.1; cells (1e-3,1),(1e-3,10),(1e-6,1)) shows M_total
  is **CONTINUOUS in every parameter** — a FREE FAMILY. The deficit piece scales
  ~ delta*r_int (cell-size-set); the core piece ~ r_core(1-e^{-2p}) (depth-set).
  **Nothing discrete appears.** The seal/interface BC fixes the closure constant
  rs but leaves (p, delta, r_int) a free 3-parameter family. (Consistent with
  #39: cell size unpinned; and with single-cell mode-discreteness being banked-
  exhausted — no eigenvalue ladder emerged, as expected.)

**B3b (radial-profile n-field: does a regular-core -> seal soliton EXIST without
Skyrme/potential?).** The minimal O(3) sigma hedgehog EOM in the UDT background,
d/dr[e^{-phi} r^2 Theta'] = e^{phi} sin(2 Theta), shot from a regular core
(Theta(r_core)=0) for initial slopes dTheta0 = 0, 0.1, 1, 5, 20:
- Theta=0 (trivial north pole) is the only smooth bounded solution; nonzero
  slopes give Theta that either relaxes to a constant (seal Neumann met
  TRIVIALLY by Theta->const) or runs away. No non-trivial regular-core ->
  seal profile with a selected size appears.
- **Derrick/scaling backing** (`coupled_cell_soliton_derrick.py`): under radial
  rescaling Theta(r)->Theta(r/lambda) on the scale-free background, BOTH energy
  terms scale as lambda^{+1} (gradient term and transverse term each ~ lambda^1,
  GPU-confirmed: each doubles when lambda doubles). E(lambda) is **monotone
  increasing**, dE/dlambda = const > 0 — no interior stationary point, the
  classic **Derrick collapse**: the minimal radial-twist lump shrinks to zero
  size. A finite size would require a term scaling DIFFERENTLY (Skyrme ~
  lambda^{-1}, or a potential ~ lambda^{+3}).

FINDING B3: the realized finite particle is the **pure ANGULAR hedgehog
(Theta=theta, p_r=-rho exact)** sourcing a deficit phi, **finitized by the
cell**. The structure is a **FREE FAMILY** in (p, delta, r_int): the seal/
interface BC fixes the closure constant rs but **pins NO discrete depth or
size**. **No radial soliton exists in the minimal model** — Derrick collapse —
so a radial-profile particle would FORCE a stabilizer term (Skyrme/potential).
The phi-angular interaction is present but PASSIVE here: the angular knot sets
rho=xi/r^2, phi responds with the deficit (slaved by p_r=-rho), and the cell
truncates. The interaction does not, by itself, manufacture a length or a
discrete set.

---

## CROSS-CUTTING VERDICT — which ingredient finitizes?

| Ingredient | Finitizes? | Why |
|---|---|---|
| **Cell alone (B1)** | **YES** | Truncation; E_coord = 4pi xi (r_int-r_core), finite, continuous in size, no 1/r_core divergence. |
| **phi alone (B2)** | **NO** | Deficit geometry; M(r)=delta r DIVERGES linearly. phi gives the EOS/conical defect, not localization. |
| **Both (B3)** | **YES, via the cell** | Finiteness is delivered by the cell; phi supplies the deficit EOS and the back-reacted profile, but the cell is what bounds the mass. |

**The math requires the CELL for finiteness; phi is NOT sufficient and (for
finiteness) NOT necessary** — the hedgehog energy is already finite on the cell
with phi frozen (B1). phi is necessary for the PHYSICS (the B=1/A EOS, the
deficit geometry, the realized back-reacted profile and its MS mass), but it is
the **finite cell** that finitizes the particle. This SHARPENS Charles's "both
may be needed but possibly only one" hypothesis: for FINITENESS specifically,
the answer is **the cell (one ingredient)**; for the particle's STRUCTURE
(EOS, geometry, mass value) both play together.

Honest caveat against over-reading "cell alone": the cell is the **mirror of the
CMB boundary** (C-2026-06-10-2), i.e. it is physical structure, not a hand-placed
wall — but its SIZE is a free dimensionful input (#39), so the cell finitizes
without selecting a scale. The phi-angular interaction (the prime-suspect
discreteness channel, MEMORY hunch) is OBSERVED here to be real but PASSIVE in
the static minimal model: it does not pin a size or generate a discrete ladder.
This is a static-single-cell observation and does not bind the nonstationary /
ensemble sectors (C-2026-06-10-3).

## EMERGENT STRUCTURE OF THE REALIZED PARTICLE (B3)

- **Source:** pure angular hedgehog n=x/r (Theta=theta); rho=xi/r^2, p_r=-xi/r^2,
  p_theta=0; p_r=-rho EXACT everywhere (no radial twist; the minimal model admits
  no stable radial profile — Derrick).
- **phi profile:** e^{-2phi}(r) = 1 - m_areal(r)/r with m_areal(r) =
  delta(r-r_core) + r_core(1-e^{-2p}) + rs; a solid-angle-deficit cell, deep
  (depth p) at the core, closing to phi=0 at the interface only via a negative
  closure constant rs = -[delta(r_int-r_core)+r_core(1-e^{-2p})] (a mass defect).
- **Misner-Sharp mass:** M_total = r_core(1-e^{-2p}) + delta(r_int-r_core),
  FINITE, CONTINUOUS in (p, delta, r_core, r_int).
- **What is pinned / what is free:** the seal/interface BC PINS the closure
  constant rs; everything else — core depth p, coupling/deficit delta, cell size
  r_int — is **FREE** (a 3-parameter continuous family). **No discreteness, no
  eigenvalue condition, no selected size emerged.**

---

## PREMISE LEDGER (chose vs derived)

DERIVED (forced by CANON / the metric / the angular Lagrangian):
- rho=xi/r^2, p_r=-xi/r^2, p_theta=0, p_r=-rho exact (hedgehog). [C-2026-06-14-1]
- Back-reaction e^{-2phi}=1-kappa8 xi - rs/r. [angular_lagrangian_results.md T6]
- MS mass m(r)=(c^2 r/2G)(1-e^{-2phi}). [macro_sector_fork_resolution.md:33]
- p_r+rho=xi e^{-2phi}(Theta')^2 for radial twist. [CANON D7]
- E_coord = 4pi xi (r_int-r_core) [the constant-integrand fact; this push].
- Minimal O(3) sigma EOM d/dr[e^{-phi}r^2 Theta']=e^{phi}sin 2Theta [EL of L].
- Derrick lambda^{+1} scaling of both terms (no-go). [this push, GPU+analytic]
- Seal BC parity dichotomy (Neumann/Dirichlet), bare measure, stiffness K_r,K_th.
  [wcc_results.md:50-51, offdiag_scan_results.md:61,64-65]

CHOSE (modeling choices, flagged):
- C1. **MINIMAL model: NO Skyrme term, NO potential** (the whole point — to test
  if cell+phi suffice). Load-bearing for B3b's "no radial soliton" finding.
- C2. **Core depth e^{-2phi}(r_core)=e^{-2p}, p the integration parameter** —
  the regular-turning-point parametrization (DERIVED-role from #39/sweep, but
  the specific e^{-2p} normalization is a chosen reading).
- C3. **Interface BC phi(r_int)=0** (the phi=0 interface = mirror of CMB
  boundary, C-2026-06-10-2). Chosen as the physical seal; it forced rs<0.
- C4. **rs=0 in B2** (pure monopole, no extra point mass) — chosen to isolate
  the monopole's own finiteness behavior.
- C5. **Fixed backgrounds in B1** (phi=0 and phi=-p ln(r_int/r)) — chosen probe
  profiles to test sensitivity; B1's verdict is background-robust.
- C6. **delta, xi, r_core, r_int dimensionless dials** scanned, not fixed (no
  scale chosen; consistent with data-blind + #39).
- C7. **Derrick probe profile** (regular-core bump Theta=pi(s/w)e^{1-s/w}) — a
  representative localized twist; the lambda^1 scaling is profile-independent
  (it is the dimension count), so this choice is not load-bearing.

NOT CLAIMED: no mass, no ratio, no wall comparison; no discrete type/ladder
asserted (none emerged); the nonstationary weld and ensemble sectors untouched
(C-2026-06-10-3); the Skyrme/potential sectors deliberately not added.

---

## HONEST ONE-PARAGRAPH SUMMARY

On the finite matter cell, the UDT angular hedgehog is finitized by the **CELL**,
not by phi. The hedgehog's energy density rho=xi/r^2 against the bare r^2 measure
gives a constant integrand, so the energy 4pi xi (r_int-r_core) is finite for any
finite cell and even stays finite as the core shrinks — the cell finitizes by
truncation (B1). phi back-reaction ALONE does the opposite: it produces the
global-monopole solid-angle deficit, whose Misner-Sharp mass M(r)=delta r grows
linearly and DIVERGES on the unbounded domain (B2) — phi supplies the EOS and the
conical geometry but not localization. With BOTH together on the cell (B3) the
realized particle is the pure angular hedgehog (p_r=-rho exact) sourcing a deficit
phi, finitized by the cell; its structure is a CONTINUOUS, FREE family in core
depth p, deficit delta, and cell size r_int — the seal/interface BC fixes only a
closure constant (a negative mass defect rs), pinning no discrete depth or size,
and no eigenvalue ladder appears (consistent with banked single-cell mode-
discreteness exhaustion). The minimal model admits NO stable radial-twist soliton
(Derrick collapse: both energy terms scale as lambda^1), so any radial-profile
particle would FORCE a stabilizer (Skyrme/potential) — reported as the honest
finding, not patched. Net: for FINITENESS the math requires the cell (one
ingredient); for the particle's structure cell and phi play together, with the
phi-angular interaction present but PASSIVE in the static minimal model (it sets
the EOS and geometry but manufactures neither a length nor discreteness).

---

## WHAT THE BLIND VERIFIER SHOULD ATTACK HARDEST

1. **B1's "cell alone finitizes" via the constant integrand.** Re-derive that
   rho 4pi r^2 = 4pi xi is genuinely constant (the 1/r^2 vs r^2 cancellation) and
   that E_coord = 4pi xi (r_int-r_core) — and check whether the PROPER-volume
   measure (e^{+phi} weight) or the CURVATURE energy (vs the bare integral)
   changes the finiteness verdict at deep core. Is "finite by truncation" the
   right reading, or does a deep-phi proper-volume term reintroduce a divergence?
2. **B2's linear divergence M(r)=delta r.** Confirm independently that the global-
   monopole MS mass diverges (delta r, not converges), i.e. phi truly does NOT
   localize. Check the sign/normalization of the deficit (E2 erratum in CANON)
   doesn't flip divergence to convergence.
3. **B3a's seal-closure forcing rs<0 (mass defect).** The claim that phi(r_int)=0
   cannot be met with rs=0 (m_areal(r_int)>0 strictly) and so forces a NEGATIVE
   closure constant. Is rs<0 physical (a mass defect / the inside-out cell's
   negative-phi sign), or does it signal the interface BC should be something
   other than phi=0? This is the load-bearing structural claim.
4. **B3b's Derrick no-go (the FORCED-stabilizer finding).** Verify the lambda^{+1}
   scaling of BOTH terms independently (analytic dimension count + a different
   probe profile), and that the deficit-log background does not introduce a
   length that evades Derrick. If a stabilizer is genuinely forced, that is a
   significant structural finding (the minimal model is insufficient for a radial
   particle) — attack whether the cell+seal BCs themselves could provide the
   missing scale (a boundary-induced stabilization the bulk Derrick misses).
5. **"FREE FAMILY, nothing pinned."** Confirm no discrete condition was missed:
   re-examine whether imposing BOTH core-regularity AND seal-Neumann
   simultaneously on the FULL coupled (phi + any admitted twist) system
   overdetermines and selects a discrete (p, delta, r_int) set. The shoot found
   none, but the verifier should test the self-adjoint eigenproblem framing
   (measure r^2 sin th, stiffness K_r,K_th) directly for any hidden quantization.

---

## DATA-BLIND CONFIRMATION

No lepton/hadron wall numbers loaded, matched, or consulted in any script or in
this document. No count or ratio imported. xi, delta, r_core, r_int, p were
treated as free dimensionless dials and SCANNED; no scale was fixed. The push was
METRIC-LED (interrogating what the derived hedgehog source + back-reacting phi do
on the finite cell), not template-led — and where a template question arose (does
a radial soliton exist?), its NEGATIVE was reported as a forced-stabilizer
finding, not buried. No Skyrme term or potential was added.

---

## VERIFIER-CLEARED (appended 2026-06-14; supersedes the PENDING line)

Blind adversarial verifier (Claude Opus 4.8, agent ad93954b78525b33e,
2026-06-14; coupled_cell_soliton_verifier_results.md + verifier_scripts_
coupled_cell/v_*.py) independently re-derived all five claims (own sympy /
mpmath dps=50 / V100 float64; constructor scripts NOT run). VERDICT: the
study STANDS — nothing refuted, nothing unreproducible.
- CELL FINITIZES: CONFIRMED (rho*4pi r^2 = 4pi xi constant; E=4pi xi(r_int-
  r_core); no 1/r_core divergence; proper-volume energy finite to p=50).
- PHI ALONE: does NOT finitize — CONFIRMED (M(r)~delta*r linear divergence).
- HIDDEN DISCRETENESS: the verifier BUILT the simultaneous core+seal self-
  adjoint eigenproblem on the GPU specifically to find quantization the shoot
  missed, and found NONE that is particle-discreteness (bounded-domain modes
  move smoothly with delta, r_int; pure 1/r_int^2 Laplacian scaling, no
  intrinsic length). "All free, nothing discrete" CONFIRMED + correctly
  scoped (static, single-cell, minimal-model).
- rs<0 (mass defect): CONFIRMED but BC-tied (forced under phi(r_int)=0; under
  the Neumann/mirror-fold seal rs=r_core(delta-1+e^{-2p}), generically <0 but
  flips for shallow core + large deficit; with no interface pin rs=0). Real,
  load-bearing, premise-attached — not an artifact.
- DERRICK NO-GO: CONFIRMED (both energy terms scale lambda^1; E(2L)/E(L)~2.0
  on three probe profiles; conical background doesn't change the exponent;
  the seal does NOT select a size). No stable radial-twist soliton in the
  minimal model => a stabilizer (Skyrme/potential or a native equivalent) is
  FORCED for an internal-profile particle.
