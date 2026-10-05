# OAA1 parent finite controls, frozen before execution

Question: on actual CPR1 b_*=0 incidence, do independently contracted endpoint
frequencies and affine lengths obey the candidate relation and approach its
predicted finite endpoint/residue? Separately check static radial radar versus
slice-length asymptotics. Neither calculation identifies the native distance.

Same free-and-explored metric values m1,a10,Lambda0.0001. Source/receiver
preparation u_infinity=phi_0=0; E fixed separately1 and10. R=1000,10000,100000,
1000000. At40/70decimaldigits:16 actual incidence solves. Save every solved
ray's b,te,U,P,receiver tail,residual,affine integral and derived quantities.
Newton bracket[0,0.99*bmax], max100iterations; internal stop10^(-dps+6),
original incidence acceptance10^(-dps+8). No chart-horizon cancellation in
the frequency. Subtract the affine integral's constant asymptotic integrand
analytically, then use a rationalized regular integrand in x=1/r.

Exact symbolic checks cover grad r/norm and a rational endpoint Lorentz boost.
Direct original-EF contraction must agree with A at10^(-dps+8); affine
renormalization and D_e=Z D_o use the same tolerance. These latter identities
are controls, not independent proof or native-selection tests.

Each frozen ray must obey domain positivity and D_o<1/H in these particular
examples. At R1e6 require relative endpoint, leading-deficit and residue errors
<0.01; analytic proof, not this loose asymptotic illustration, owns the limit.
Cross-precision differences for all central load-bearing values normalized by
max(1,reference magnitude) must be<1e-25. No global monotonicity is inferred.

Find the simple outer root in bracket170,175; check original f residual.
For delta0.01,0.0001,0.000001 integrate between r_c-delta and r_c-delta/2.
Radar and slice increments must match their analytic leading coefficients to
relative0.001. These are a separately labeled static radial clock/relay control,
not CPR1's orbiting source. Six interval cases plus two root computations.

CPU2GiB1BLAS, no GPU/grid, no wall/CPU timeout; <=100 total finite cases
including repairs, package<100MiB. Actual parent plan has16 incidences,6 paired
interval cases,2 roots plus exact symbolic identities. No observations, fitted
parameter, source model, angular-map or interval certification. Preserve all
failures before a bounded diagnostic/repair; do not relax acceptance silently.
