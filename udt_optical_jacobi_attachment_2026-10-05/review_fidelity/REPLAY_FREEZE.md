# Independent replay freeze

Exposed to INITIAL_CANDIDATE and NUMERICAL_FREEZE, not to parent implementation
or numerical outcomes. Additional seven named cases only, bringing the executed
case count to 23 if all succeed, with the same hard total cap 100. CPU, 2GiB
address-space limit, one BLAS thread, no timeout. Fixed 60 decimal digits.

Four actual incidences: m1,a10,H=sqrt(.0001/3), E1 and10, R1000 and1000000,
u_infinity=phi_0=0. Three fixed rays exactly match the parent's frozen controls:
(a10,H=sqrt(.0001/3),R50,b2), (a10,same H,R1000,b-3), and
(a3.001,H.18,R10000,b=-.999 a/sqrt(f(a))). All use m1.

Reconstruct original integrals in reciprocal radius, solve incidence from the
source/receiver histories, and independently calculate both signed B factors,
J, D_A, D_o and Z. Require source regularity, real root and original residual
<1e-45. Expected parent comparison tolerance scaled 1e-24, reflecting the
parent's 40-digit lower-precision records. Preserve discrepant and failed values.
Read parent saved JSON only after writing this implementation's records.
Root iterations and quadrature points are not separate physical cases.
