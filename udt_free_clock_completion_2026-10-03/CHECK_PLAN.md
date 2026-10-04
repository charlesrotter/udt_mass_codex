# FCL1 parent controls, frozen before execution

One short SymPy script, three families. These exact finite controls check
algebra and hypotheses, not the general endpoint theorem by sampling.
All metrics/data are supplied comparison objects, not native UDT solutions,
selected physical parameters or fits. c_E=1 is a unit convention.

1. Nonuniform Lorentz4 g=x^-2 diag(-N^2,a1^2,a2^2,a3^2), N depending on every
coordinate, ai depending on x and its spatial coordinate. Compute physical
Christoffels directly. At three rational points and two rational orthonormal
spatial velocities (six cases), check unit norm and all three spatial momentum
equations against the independently computed acceleration. Omitting the force
must fail in every case. This checks signs, x factors and spatial variation.
2. In supplied g=x^-2 eta, an exact moving free receiver and fixed interior
emitter at y=0. Check unit norm, original geodesic residual, actual ray incidence,
proper-time derivative ratio and limit xZ=1. The receiver moves at finite x.
3. Same metric, explicitly accelerated receiver with rapidity log x. Check
unit norm, nonzero proper acceleration squared x^-2, actual ray incidence and
clock derivative ratio, and finite Z->1. This refutes only a statement without
the free-receiver hypothesis, not FCL1.

The last two use 0<x<1/4, with emitter x_e in [1,3/2], away from the boundary.
Conformal future rays point (-1,1,0,0), consistently normalized by 1/x_e.
No independent endpoint normalizations, fitted function, cutoff, Einstein
equation, GPU, floating tolerance or numerical extrapolation.

Acceptance: claimed exact residuals vanish, omitted force does not, free xZ
limit1 and nonfree finite Z limit1. Preserve any failure and diagnose finitely.
2GiB/process,oneBLAS,no elapsed/CPU cutoff; one parent script,three families,
eight cases total, below the authorized two-script/six-family/500-case budget.
Freeze candidate/code/plan hashes before executing the capture.
