# NGD1 fixed comparison arena and choice ledger

This is conditional Ric(g)=0 under G312's GR FILTER ONLY restriction. R9's
native balance does not identify its response E with Ricci. The following
evolution system is consequently a comparison/testbed, never a native UDT
selection. It extends the explicitly supplied NE1 two-Killing arena (central
R12); an unpolarized field Q is now released. The symmetry, orthogonal
transitivity, periodic topology, vacuum branch, Lambda=0, chosen areal foliation
and marking remain supplied restrictions. No source or X_max is used.

For t>0 and periodic x of length L=2pi/k, write

    g = N²(-dt²+dx²) + t[exp(P)(dy+Q dz)² + exp(-P)dz²],
    N = exp(lambda/4) t^(-1/4).

All P,Q,lambda depend on t,x. In this class the conditional vacuum equations are

    Ptt = Pxx - Pt/t + exp(2P)(Qt²-Qx²),
    Qtt = Qxx - Qt/t - 2(Pt Qt-Px Qx),
    lambdat = t[Pt²+Px²+exp(2P)(Qt²+Qx²)],
    lambdax = 2t[Pt Px+exp(2P)Qt Qx].

Independent derivation/original Ricci check is a pilot gate, not inferred from
the solver passing its own RHS check. Spatially periodic lambda requires zero
mean momentum Pt Px+exp(2P)Qt Qx. Initial P=Q=0 satisfies it for every chosen
velocity profile. Later nonzero profiles are admitted by subtracting alpha Px
from Pt, with alpha=<Pt Px+exp(2P)Qt Qx>/<Px²>, when the denominator is nonzero.
This projection enforces a constraint; it does not tune a readout. Lambda is the
spectral primitive of the zero-mean lambdax with supplied mean4log(.75).

Native readout, conditional geometry: for two actual supplied fixed-(x,y,z)
clocks linked by a longitudinal null branch with positive dx/dt=1, separation
d>0 gives to=te+d, and Z=d(tau_o)/d(tau_e)=N(to,xo)/N(te,xe). N is integrated
proper-time conversion from this metric. This is not a universal redshift law,
not an assertion of mutual slowing for this observer family, and not selected
cosmological observers. The same marked clocks exist on the homogeneous control.

## Numerical method and choices

P,Pt,Q,Qt,lambda evolve by classical RK4, Fourier collocation in x, float64,
without artificial viscosity/filtering, de-aliasing or relaxation. Nonpolynomial
products are evaluated pointwise; Fourier-tail and independent spatial refinement
must bound aliasing/truncation effects. Step refinement is separate. A spectral
tail is a diagnostic, not proof of continuum convergence. Saved time windows
allow independent differentiation of the original metric and Ricci contraction.

Conditional equations/signature: pinned-by-THEORY **within this stated branch**.
Symmetry, topology, areal coordinate and mean lapse normalization: supplied,
pinned-by-HABIT and progressively challenged where feasible. Finite modes,
phases, amplitudes, initial profiles: free-and-explored; fixed before survey.
Resolution/timestep/precision are numerical controls, not physical premises.

Sources: central R9-R12; G312 AUTHORITY_RECORD; NE1 INITIAL_CANDIDATE and
REVIEWED_RESULT (source hashes in SOURCE_PINS). Primary comparison literature:
Hernandez and Nettel, *A family of exact solutions for unpolarized Gowdy models*,
https://arxiv.org/abs/gr-qc/9810068 (method provenance only). Independent reviewers
own their equation checks and may identify additional checked method sources.
