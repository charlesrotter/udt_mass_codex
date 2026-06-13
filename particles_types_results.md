# Particles: Types, Formation, Properties — Topological-Sector Assembly

Status: working assembly + extension, NOT canonical. Created 2026-06-13.
Scripts: `particles_topology_types.py`, `particles_coeff_structure.py`.
Logs: `/tmp/particles_types.log`, `/tmp/particles_coeff.log`.
Method: exact sympy/mpmath assembly of ALREADY-DERIVED boundary/topological
objects toward the particle GOAL. No new bulk solve, no parameter scan.
Data-blind: structure derived first; the six lepton wall numbers loaded only
for the final comparison.

This push deliberately works the BOUNDARY/TOPOLOGY/FORMATION sector (HANDOFF
THE GOAL), not the interior (dead end, registry #34).

## What this push assembled (all from banked, re-verified exact here)

- N from the area form: the two-form lock `C(N^2,2)=4N^2 -> N^2-1=8 -> N=3`,
  and the epsilon-singlet `dim Lambda^3 V_N = C(N,3)` unique only at N=3.
- C1 boundary units from `q = 1 - 2/N` at N=3: q=1/3, eta=q/6=1/18,
  eta/2=1/36, S_C1/R=q^2/(4(1-2q))=1/12, s=q(1-q)/2=1/9.
- alphabet End(H1)=1+3+5, T8=A3+S5, W(P)=Tr(P)/12 -> W(A3)=1/4, W(S5)=5/12,
  W(T8)=2/3.
- mass: p_F=gamma/2 (Misner-Sharp public charge), Q=gamma; transfer factor
  g = N*exp(-eta/2) = 3 e^{-1/36} = 2.91781343134904518.
- formation: c* = chat*gamma^2, chat=0.498912 (NOT 1/2); gamma shapes, c
  seals; Delta p_F (the off-bare mass shift) is 100% phi-angular-sourced
  (c=0 => Delta p_F = 0 EXACTLY).

## (i) TYPES — three generations from the alphabet's odd SO(3) tower

CLAIM (hypothesis-grade, structural): the generations are the proper active
odd SO(3) sectors carried by the operator alphabet End(H1) (dim 9). The odd
dimensions `2L+1 <= 9` are {1,3,5,7,9}. Excluding the trace (1, the reference
anchor) and the whole alphabet (9), the PROPER ACTIVE odd sectors are exactly

        A3 (dim 3),   S5 (dim 5),   L7 (dim 7).

The 7 is native as the Hodge-complement grade of the two-form sector
(`*Lambda^2 End(H1) = Lambda^7`, spectrum-doc sec 5). Three generations
because the tower has exactly three proper active odd grades inside the 9-dim
alphabet. This is the SAME area-form alphabet that forced N=3; the count "3
generations" rides on the same topological object as the charge q=1/3.

The TOPOLOGICAL DATA distinguishing the types: the angular sector dimension
(3,5,7) = the cell's exterior odd-grade fingerprint. The electron sits on the
trace/scalar anchor (the reference cell, depth 0).

NOTE on prior fragments now unified: the lepton-ladder contract froze "muon
depth 5, tau depth 7" by hand; here 5 and 7 are NOT free — they are dim S5 and
dim L7. The depths ARE the sector dimensions.

## (ii) FORMATION — how a type comes into being

Banked (exterior_cavity, w8): a cell condenses from the universe-side medium.
gamma (monopole dilation gradient) SHAPES the f>1 cavity; c (angular momentum
flux) SEALS it via the same-minus mirror fold (D=0 crease, w6). Threshold to
form a deep cell: c* = 0.498912 gamma^2; formed depth diverges at threshold.

What SELECTS which types exist: the angular sector. The public charge is
p_F=gamma/2 at bare order, but the realized charge is shifted by Delta p_F,
which is 100% angular-sourced. Each generation is a cell sealed by a DIFFERENT
active odd angular sector (A3/S5/L7), and the seal sector sets both the
transfer depth (its dimension) and the off-bare mass correction (its W weight /
attenuation). The electron = trace-sealed (scalar, no odd angular seal).

## (iii) PROPERTIES — angular numbers extended + masses + data-blind wall

Angular numbers (already topological outputs, re-confirmed exact): q=1/3,
eta=1/18, s=1/9, N=3. Extended: the generation ladder dims 3,5,7 and the
readout weights W(A3)=1/4, W(S5)=5/12, W(T8)=2/3 with W(S5)-W(A3)=q/2=1/6.

Masses: lepton ratios read as transfer ladders r = C * g^d with depths
d(e,mu,tau)=(0,5,7) and g=3 e^{-1/36}. The bare ladder (C=1) and all single
alphabet candidate coefficients MISS the wall numbers — reproducing the
registry's FALSIFICATION PRESSURE verdict (the required corrections fall
BETWEEN the eta/2 ~ 2.78% vocabulary rungs). Recorded honestly, not
dramatized.

DATA-BLIND comparison (wall numbers, contract 26fc757):
  required   C_M1 = 0.97767908763602  C_E1 = 1.93121474778948  ratio = 1.97530536575
  best single-candidate dev:
    C_M1: exp(-eta/2) at -0.52%
    C_E1: 35/18 = 2(1-eta/2) at +0.68%
    ratio: 2 at +1.25%   (all MISS at the 0.01% bar; reproduces registry)

STRUCTURAL refinement (hypothesis-grade, NEW this push, NOT banked — flag for
blind verifier): the required coefficients are consistent with a
DEPTH-ACCUMULATING phi-angular SEAL ATTENUATION, not a free constant. With
two natural bases (base_mu=1 = A3/trace-anchored; base_tau=2 = S5 doubled
active image), a per-rung rate `C_d = base_d * exp(kappa * d * eta)` recovers
  kappa(from muon) = -0.0813,  kappa(from tau, base 2) = -0.0900
i.e. a SINGLE small negative seal rate fits both to ~11% — consistent in sign
and magnitude with the banked angular Delta p_F ~ -2.5% (also negative,
angular-sourced). The native rate kappa = -eta = -1/18 predicts both
coefficients data-blind to +0.72% (C_M1) and +1.35% (C_E1) — the best NATIVE
single-rate, still outside the 0.1% LEAD bar. This says the missing object is
the type-by-type angular seal correction to p_F, which the program has NEVER
computed (it was treated as a free constant). It is NOT a match and is banked
as a structural pointer only.

## Solid vs hypothesis-grade

SOLID (re-derived exact here, all previously banked):
  - N=3 area-form lock; q=1/3, eta=1/18, s=1/9; alphabet 1+3+5; W(P)=Tr(P)/12;
    p_F=gamma/2; c*=0.498912 gamma^2; Delta p_F is 100% angular-sourced.
HYPOTHESIS-GRADE (new framing this push; needs blind verifier + Charles):
  - generations = proper active odd sectors {3,5,7} of End(H1) (the "why 3
    generations" candidate);
  - depths 5,7 = dim S5, dim L7 (not free);
  - the wall residual = a depth-accumulating angular seal attenuation at rate
    ~ -eta, with bases 1 and 2.
FALSIFIED/UNCHANGED: bare and single-coefficient ladders MISS the wall numbers
  (registry FALSIFICATION PRESSURE stands).

## The single sharpest next object

DERIVE the phi-angular SEAL CORRECTION to the public charge, type-by-type:
Delta p_F as a function of the seal's odd angular sector (A3/S5/L7) and the
transfer depth. It is the ONLY missing object between the proven
(p_F=gamma/2, c*, Delta p_F 100% angular) and the wall numbers, and the
structure probe says it is a per-rung accumulating attenuation of order eta,
NOT a free constant. Compute it from the w6 mirror-fold crease BC
(rho = b - f q a) + the formation flow weld data with the angular drive c on,
sector by sector. This is a boundary/seal calculation (where the physics is),
not an interior solve.
