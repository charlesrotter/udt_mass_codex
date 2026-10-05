# OJM1 parent controls, frozen before execution

Question: do the two Jacobi factors follow the original metric ray variations,
and does the actual b_*=0 clock history retain its optical-distance pole?
Analytic proof owns the asymptote. Finite checks are illustrative regression and
independent ray-variation corroboration, not interval or global certification.

Exact SymPy: both affine Jacobi residuals, both unit vertex slopes, original EF
screen Gram/null conditions, and rejection of both deliberately reversed tidal
signs. Numerical mpmath at40 and70digits: m1,a10,Lambda.0001, fixed E1 and10,
R1e3,1e4,1e5,1e6 on original u_infinity=phi_0=0 incidences. Actual b and t_e
solved together through the reduced equation; original two residuals saved and
required<10^(-dps+8). Internal stop10^(-dps+6), bracket[0,.99 bmax], cap100.
Two precision results must agree to scaled1e-25. R1e6 endpoint and pole residue
relative errors<1%; this tolerance is not a theorem or observational accuracy.

Three additional supplied ray controls at each precision: (a10,H=sqrt(.0001/3),
R50,b2), (a10,sameH,R1000,b-3), and prior OAA strong (a3.001,H.18,R10000,
b=-.999 bmax). Finite central impact variations at delta=min(.001,.001 times
source margin) and delta/2 reconstruct the in-plane map from original U,P
integrals and EF projection. Independent finite plane rotations at.001 and.0005
reconstruct the perpendicular map. Relative errors<1e-5 and second error<.4
times first+1e-30. Wrong zero-tide/isotropic B=L must disagree by>1e-8 in these
nonradial controls. Store all estimates, errors and caustic indicators, whether
or not a ray is conjugate; do not reject a legitimate ray for focusing.

Conservative accounting:16 incidences+6 central ray controls+48 finite neighbor
evaluations=70, plus the finite exact control set, below100. Root iterations and
adaptive quadrature samples are work within a fixed case, not new physical
preparations. CPU2GiB1BLAS/noGPU/no wall/CPU timeout through the existing capture
wrapper. No desired numeric curve or CAUSTIC/PASS outcome is inserted as a
physical input. Preserve initial code, all stdout/stderr and failure receipts.
