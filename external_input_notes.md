# External LLM Input — Notes (2026-06-14)

Charles ran the LLM.md "fresh eyes" spec past outside models (compile mode;
work next session). This records the DISTILLED, honestly-graded takeaways
so they survive into the next session. Grades: **[verified]** (computed +
re-derived here), **[direction]** (well-reasoned, not yet computed),
**[fork]** (a premise to settle), **[caution]**.

## The one VERIFIED computed result

**The UDT metric forces the equation of state p_r = -rho.** For ANY
phi(r), the one-function metric (g_tt g_rr = -c^2) gives G^t_t = G^r_r
IDENTICALLY, i.e. radial pressure = minus energy density (p_theta free).
Independently re-derived (external_source_analysis.py + our own check:
p_r + rho = 0 exactly). **[verified]** Everything else in the external
scripts/answers (the hedgehog 1/r^2 core, the negative MS mass, the
"discrete tower") was ARGUMENT or HAND-BUILT TOY, not computed — the toy
spectrum used a hand-drawn Gaussian + an inserted mass gap and found one
level; the real test needs OUR angular Lagrangian (below).

## Convergent DIRECTION (two independent models + our own findings agree)

- The discreteness CANNOT come from the static radial metric alone
  (Birkhoff: spherical vacuum = Schwarzschild, continuous mass) — both
  models re-derived our bulk no-go independently. This corroborates that
  our eliminations were real, not myopia. **[verified-elsewhere]**
- A PLAIN SCALAR cannot source the metric: p_r=-rho needs p_r+rho=0, but a
  canonical scalar has p_r+rho = e^{-2phi}phi'^2 > 0 (zero only where
  phi'=0). So phi alone is not the matter. **[direction; sound argument,
  not yet a full computation]**
- THE INVERSION: the ANGULAR / TOPOLOGICAL sector (N=3, q=1/3) is the
  plausible SOURCE of matter; phi is the RESPONSE (slaved via p_r=-rho).
  A particle = a topological knot in the angular sector, dressed by a phi
  cavity; the mass ladder = that knot's normalizable mode-tower (a
  nonlinear angular-radial soliton boundary-value problem). This CONVERGES
  with our deepest result (#40 / the GOAL: structure lives in the
  angular/boundary sector). **[direction]**
- KEY NUANCE (Gauss-Bonnet; aligns with #40): the BARE topological invariant
  N=3/q=1/3 LABELS sectors but does NOT by itself GENERATE energy or a
  ladder — integrated curvature is a fixed topological number. So the
  angular sector must enter as a DYNAMICAL FIELD (its gradients /
  off-diagonal coupling / a radial hedgehog profile) to affect the radial
  equations. This is exactly why #40 found the cohomology RIGID: the energy
  is in the FIELD's dynamics, not in the invariant. Precedent that this
  works: Bartnik-McKinnon — gravity + a nonlinear angular sector yields a
  DISCRETE soliton family even though neither piece alone does. **[direction]**
- AIM FOR RATIOS, not absolute masses (a classical geometry carries one
  irreducible scale). Matches our Step 0. **[direction]**
- THE HIERARCHY IS EXPONENTIAL: m_e/M_Pl ~ 4e-23 cannot come from algebraic
  factors (1/3, N=3) but CAN from an exponential of a dilation depth/action
  (e.g. m ~ M_Pl e^{-Gamma}, Gamma ~ angular-rational x dilation-depth).
  Matches our Step 0 (the depth can't bridge linearly). **[direction]**

## Three FORKS to settle (foundational premises; two touch our CANON)

1. **B = 1/A inside matter — keep or relax?** The two models split. Model B:
   KEEP it -> p_r=-rho is forced -> the source must be TOPOLOGICAL (a scalar
   can't). Model A: RELAX it (it is a VACUUM result; the postulate only
   fixes A=e^{-2phi}) -> a two-function interior lets a scalar source. Our
   CANON (C-2026-06-10-1) asserts B=1/A as the areal reading — but is that
   true INSIDE matter or only in vacuum? This is the cleanest, most
   load-bearing premise; settle it first. **[fork]**
2. **Mass = Misner-Sharp (our frame) vs mass = hbar*omega (Model B).** Model
   B: the MS mass of a particle-sized region is its tiny GRAVITATIONAL
   self-energy (the thing that goes negative — our sign trouble), NOT the
   inertial mass; the particle mass is hbar*omega of the bound mode
   (positive by construction), and reading it that way DISSOLVES the
   negative-mass problem. They differ by (M_Pl/m_e)^2. This challenges
   LLM.md sec 3 / our MS-mass framing. **[fork]**
3. **Matter = negative phi (our CANON, inside-out cell) vs positive phi
   (Model B).** Model B argues POSITIVE phi gives positive mass AND the
   exponential hierarchy for free (m=M_Pl e^{-phi}, electron at phi~51).
   Negative phi gives negative gravitational mass and would blueshift. The
   phi-SIGN is now load-bearing for the whole hierarchy. Contradicts
   "matter is the negative-phi cell." **[fork]**

## Anchors (Charles, 2026-06-14)

hbar is a SOLID anchor, on par with c and G (it is REQUIRED: with only
G,c you can build lengths and gravitational masses but not a quantum
particle mass — that map IS hbar, via lambda=hbar/mc). So m_P=sqrt(hbar c/G)
is a legitimate scale and the exponential-hierarchy line is well-founded.
DISCIPLINE: count independent dimensionful DIALS — ONE overall scale (the
m_e anchor, for ratios) is allowed/irreducible; a SECOND tunable scale
(an adjustable coupling) means the spectrum is FITTED, not emerging. hbar
should enter only through Planck units. **[caution]**

## The make-or-break NEXT computation (needs OUR input)

Obtain/derive the ACTUAL angular-sector Lagrangian behind N=3, q=1/3 (the
target-space + winding term). Then solve the hedgehog/soliton radial
profile in the UDT background (regular core, decay to vacuum) as a
nonlinear SHOOTING eigenvalue problem -> a PARAMETER-FREE set of mass
RATIOS. Test against the lepton ratios and the **Koide target 2/3 = 2q**
(q=1/3) — which both models flag as a PASS/FAIL target the spectrum must
hit BEFORE looking, NEVER as evidence. **[caution]** The "hedgehog/global
monopole" is a TEMPLATE-IMPORT to verify against our real angular sector,
not adopt blindly; the 22/3 ~ gamma numerology is direction, not result.

Files: external_source_analysis.py (the run; only p_r=-rho is computed).
