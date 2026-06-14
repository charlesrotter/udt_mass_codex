# dyn1 — Dynamic Cavity-Stability Test (Phase 1): the discrete-vs-continuum verdict

Driver: Claude (Opus 4.8, 1M ctx). Date 2026-06-14. New files only (dyn1_*).
Frame: DYNAMIC_SCALE_SYNTHESIS.md, CATALOG_FRAME.md, CRITICAL_UNIVERSE_FRAME.md.
Canon: C-2026-06-13-1 (the metric propagates; motion never sources shape).
DATA-BLIND (no lepton wall numbers loaded). HYPOTHESIS-GRADE pending blind
verifier + Charles canonization. Append-only research record.

## THE QUESTION (make-or-break)

Does a DISCRETE set of dynamically-stable matter cavities exist (= a particle
spectrum, whose dimensionless mass RATIOS we could then test), or is the
stable set a CONTINUUM (no native discreteness from the dynamic sector)?
Scale-free; ratios only. STEP A = the discrete static candidate set (the
nodal family). STEP B = the dynamic stability filter. STEP C = the verdict.

## THE VERDICT (direct answer)

**NO discrete stable spectrum. The cavity family is a CONTINUUM, and the
WHOLE continuum is (linearly) stable.** Both the static structure (Step A)
and the dynamic stability filter (Step B) return a CONTINUUM, not a discrete
set. The dynamic discretizer is **exhausted** on the radial sector: dynamics
does not carve a discrete stable subset out of the continuous cavity family.
This is a first-class negative, consistent with and strengthening registry
#33/#34/#39 (nodeless bulk continuum) and #40 (boundary cohomology rigid,
continuous mass).

The nodal family is NOT the discrete structure (Step A.2/A.4 below).

## STEP A — the discrete candidate set (static)

### A.0 The object, reconciled to the validated machinery
The metric's OWN radial field equation. The VALIDATED canonical cell
(#34/#39, wint_cell2d.py, anchor L(E=3,Phi=1)=1.67427938129) lives in the
FLOW CHART v(m):

    v_mm = S(v) = e^{-2v} - e^{v} = -dU/dv,   U(v) = (Phi/2)e^{-2v} + Phi e^{v}

sealed by TWO turning points v_m=0 (the W6 regular mirror-fold seals). U has
ONE minimum at v=0 (U_min=1.5 Phi); a cell is ONE bounce of a particle of
"partition energy" E in the convex well U. The half-period L(E) (the cell's
chart width) is a SMOOTH continuum in E (registry #33, reproduced — anchor
matched to 1e-9). c=G=1, Phi=1; ratios are scale-free here as required.

(My first Step-A pass used the Dirichlet-shoot form v_mm+(2/r)v_m-2v_m^2 =
1-e^{3v} from neg_sweep/sweep_radial_backbone. That is a DIFFERENT chart and
its static reduction does NOT match the canon dynamic equation's static limit
[sign]; the recon there found only damped relaxation oscillations [amplitude
~1/r decay, NOT standing] and no regular nodal seal. Both passes agree:
no discrete static catalog. The flow-chart pass below is the canonical one.)

### A.1 One-bounce family: a CONTINUUM in E (dyn1_cell_catalog.py)
    E      L(half-per)   amp=vhi-vlo
    1.6      1.80375       0.5145
    2.0      1.76425       1.1336
    3.0      1.67430       1.8953
    6.0      1.47780       3.0066
    9.0      1.34915       3.6283
L(E), amplitude, depth all vary SMOOTHLY and monotonically with E. One
parameter (E), one smooth family. No gaps, no selection.

### A.2 Multi-bounce ("nodal") orbits are NOT distinct cells
At fixed E=3, integrating n=1,2,3 full bounces gives total chart length =
n × (single-bounce length) with IDENTICAL amplitude (1.895334) and IDENTICAL
E. A multi-bounce orbit is the SAME one-bounce cell traversed n times — a
period multiple, not a new sealed configuration. There is ONE convex well, so
every bounded orbit is a slice of the same one-parameter family.
**There is no discrete nodal catalog.**

### A.4 No regular nodal seal at any depth (dyn1_regular_seal.py)
In the Dirichlet-shoot chart, the slope at every interior zero g_n(D) =
phi'(R_{n+1}) has a FIXED SIGN and NEVER vanishes across the whole depth
range (-0.75..-0.05): g0>0, g1<0, g2>0 always, no root. A regular mirror-fold
seal needs phi=0 AND phi'=0; it never occurs at a node. The "nodal members"
are the relaxation passing through zero, not smoothly-sealed cavities.

### A.5 Ground-state (nodeless) mass curve — also continuous
n=0 cell core MS content |m(p)|=(1/2)(e^{-2p}-1) is a smooth continuum in
depth p; r*(p)->2.54593 asymptote (matches neg_sweep). No discreteness.

## STEP B — dynamic stability filter

### B.0 The dynamic equation (flow chart, corrected to be canon-consistent)
The flow-chart dynamic equation whose STATIC limit reproduces the validated
cell (v_mm = S) is

    v_TT = e^{-4v} ( v_mm - S(v) ),     c_eff^2 = e^{-4v} > 0  (canon wave speed)

strictly hyperbolic / well-posed (canon C-2026-06-13-1). Linearizing v=v0+u:

    u_TT = e^{-4v0} ( u_mm - S'(v0) u ),   Jacobi potential -S'(v) = 2e^{-2v}+e^{v} = U''(v)

### B.1 The stability backbone — ANALYTIC (the load-bearing result)
U''(v) = 2e^{-2v} + e^{v} has its minimum at v = ln(4)/3, value **2.38110 > 0**:
**U is STRICTLY CONVEX everywhere — no inflection, no concave region.** Hence
the second-variation (Jacobi) operator J = -d^2/dm^2 + U''(v0(m)) is strictly
positive on every member (its potential is bounded below by 2.381 > 0), in
the weighted inner product set by c_eff. Therefore:
- every static cell is a strict ENERGY MINIMUM => linearly STABLE;
- all perturbation omega^2 > 0 for EVERY member of the continuum;
- multi-bounce orbits stay in the same convex well => also no negative mode.
This is the legitimate stability SIGN-TEST (NOT a mass; per the banked-dead
resonator template, masses are the cavity DEPTHS/MS content, not omega).

### B.2 Numerical confirmation (dyn1_cell_catalog.py, dyn1_final_stability.py)
Jacobi generalized eigenproblem J phi = omega^2 W phi (W=e^{4v0}), Neumann
(turning-point seal) BC, across the E-continuum:

    E      L         min omega^2     lin max|u|/amp (T=80)   verdict
    1.55   1.80875    2.01932         1.2522                 STABLE
    1.8    1.78380    0.75444         1.2673                 STABLE
    2.0    1.76424    0.45628         1.1896                 STABLE
    2.5    1.71751    0.18557         1.0759                 STABLE
    3.0    1.67427    0.09647         1.0080                 STABLE
    4.0    1.59798    0.03685         1.0359                 STABLE
    6.0    1.47777    0.01017         1.0184                 STABLE
    9.0    1.34912    0.00291         1.0057                 STABLE
    15.0   1.18465    0.00061         (Jacobi only; evolve   STABLE
    30.0   0.97185    0.00008          slow at deep v)       STABLE

min omega^2 is POSITIVE for every member and decreases smoothly toward 0^+ as
E grows (the soft translational/breathing mode of an ever-wider cell) — never
crossing zero. STABILITY IS A BAND (the whole continuum), NOT a discrete set.

### B.2b Mass-content table (Misner-Sharp diagnostics) — a CONTINUUM
Masses = cavity DEPTH/MS content per CATALOG_FRAME, NOT eigenfrequencies.
    E      L         core_depth   X_core    ms_aspect   ratio(asp / E=3)
    1.55   1.80875   0.1767       -0.424    -0.01506    0.0375
    2.0    1.76424   0.5159       -1.806    -0.14497    0.3609
    3.0    1.67427   0.8162       -4.116    -0.40172    1.0000
    4.0    1.59798   0.9910       -6.258    -0.62372    1.5526
    6.0    1.47777   1.2172      -10.408    -0.99712    2.4821
    9.0    1.34912   1.4317      -16.522    -1.44852    3.6058
    15.0   1.18465   1.6944      -28.633    -2.14689    5.3442
    30.0   0.97185   2.0450      -58.741    -3.38720    8.4317
Core depth and MS content vary CONTINUOUSLY and MONOTONICALLY with E. The
mass "ratios" form a CONTINUUM (any value attainable), so there is no
discrete spectrum to take ratios of — the ratio question is ill-posed on a
continuum, which is itself the answer. (CONTROL concave well: Jacobi min
omega^2 = -56.78 < 0, instability correctly detected.)

### B.3 Energy-conserving LINEAR evolution (persistence, T<=200)
Stoermer-Verlet of u_TT=e^{-4v0}(u_mm - U''(v0)u), several modes, amp=1e-3:
max|u|/amp stays 1.1–1.8 over T=200 (~120 chart light-crossing times), energy
drift ~1e-3. Perturbations PERSIST bounded => the cells HOLD. (dyn1_evolve2.py)

### B.4 Instability-DETECTION control (validates the test is live)
Sign-flipping U'' (an artificial CONCAVE well) gives Jacobi min omega^2 =
-56.8 (< 0) and the SAME linear evolver blows up (max|u|/amp = 2.4e6). So a
"STABLE" verdict is a real detection, not a dead/over-damped scheme.

## Convergence / scope / honesty

- Step A anchor L(E=3)=1.67427938058 vs banked 1.67427938129 (1e-9). On the
  validated object.
- Static cell residual machine-zero (v_mm - S ~ 2.7e-11 on grid).
- Jacobi min omega^2 grid-converged (N=600/1200/2400 agree to printed digits).
- Linear evolution: energy-conserving, instability-detection validated.
- **SCOPE LIMIT (honest): the fully NONLINEAR time evolution is NOT clean.**
  Both an explicit Stoermer/leapfrog and an A-stable implicit (trapezoidal,
  Newton-per-step) evolver suffer a SEAL-REGION boundary-layer numerical
  instability: c_eff^2 = e^{-4v} diverges at the deep core v=vlo (e^{-4v} ~
  e^{6} at E=3), a stiff boundary layer at the turning-point seal; the
  unperturbed cell (machine-exact equilibrium) escapes by T~0.5–60 depending
  on scheme. This is a numerical-PDE stiffness at the core, NOT a physical
  instability (the static residual is machine-zero and the LINEAR dynamics
  about the same cell is bounded). The nonlinear nonlinear-saturation cross-
  check is therefore INCONCLUSIVE; the trustworthy stability evidence is the
  linear analysis (analytic convexity + Jacobi gen-eig + conserving linear
  evolution + concave control). A core-resolving (logarithmic chart / implicit
  flux-form) nonlinear evolver is the recommended follow-up.
- SECTOR SCOPE: radial sector only (canon: motion never sources SHAPE, so the
  angular charge q=1/3 is CARRIED, not dynamically generated — bringing it in
  cannot create discreteness the radial dynamics lacks). The angular sector
  was banked RIGID for type-discreteness (#40); an ensemble/multi-cell
  discretizer is a separate, untested route (the orchestra).

## What this means for the program

The dynamic radial sector does NOT discretize. Combined with #40 (boundary
cohomology rigid) and #33/#34/#39 (bulk continuum), the SINGLE-CELL routes to
discreteness are now exhausted across static structure, boundary cohomology,
AND dynamic stability. If a particle spectrum is native to UDT, it is NOT a
single-cell stability catalog — it must come from the GLOBAL condition
(critical-M, DYNAMIC_SCALE_SYNTHESIS phase 2–4) and/or multi-cell ensembles,
not from which lone cavities hold together. The mass RATIOS cannot be read
off this sector because there is no discrete set to take ratios of.
