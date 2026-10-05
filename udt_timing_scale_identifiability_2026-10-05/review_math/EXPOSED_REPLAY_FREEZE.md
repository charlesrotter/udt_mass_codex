# Exposed candidate review and saved-output replay freeze

After SOURCE_FIRST_SEAL, reviewer read parent INITIAL_CANDIDATE,
NUMERICAL_FREEZE, check_timing_scale.py and CONSTRUCTION_RESULT. Parent's code
and output exposure now applies; no subsequent blind claim. The substantive
candidate agrees with the independent source-first derivation. A1 additionally
follows directly because at b*=0 the limiting incidence derivative is1/a,
d_x=1/H^2, hence b_x(0)=Omega a/H^2 and theta=x[Omega a/H+O(x)] with positive
coefficient. Unit radial/azimuthal frame transport follows from radial geodesic
motion, the normalized Lorentz2 orthogonal complement and spherical warped
product connection; the code's explicit metric connection check is regression.
T2 is a valid branch-dependent bound, not a finite-observation error forecast.

Freeze independent SciPy float64 quad+Brent replay of six saved60-digit central
R=100000 cases (E1,10; b*=0,2,-3), three saved homotheties, and four saved
finite-difference endpoints. Each of the nine central/scaled points gets two
additional relativeR+-1e-4 solves and an integrated receiver proper-time
interval; thus31 new solves and cumulative67/100 cases. Compare b,A,Z,theta,
K_length, angular_rate and optical factors using scaled absolute tolerance1e-7,
and additionally require nonzero rate relative error<1e-5 and relative
homothety errors<1e-7. Original normalized incidence residual<=1e-10.

Different root algorithm/library and finite proper-time derivatives are used;
no parent implementation imports. Common equations and exposure are disclosed.
If a check fails preserve the failed output and freeze diagnosis before repair;
remaining33 cases bound any repair/replay. CPU2GiB,1BLAS,no wall/CPUtimeout,
noGPU, existing capture utility. No broader source/metric premise.
