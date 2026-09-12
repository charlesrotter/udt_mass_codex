# Independent numerical replay freeze

Frozen 2026-09-12 23:29 UTC after INITIAL_CANDIDATE exposure, before any parent/reviewer
numerical outcomes. Parent disclosed intended K=[1.5,10], clock radii (2,4,8), endpoint radii
(6,8), angular separation 2 radians, a in {-0.002,0,0.002}, b in {-0.4,0,0.4}.
These are synthetic supplied controls, not estimates from observed data. No selected mass/source.
FLOAT64 CPU only, library threads one; one scientific subprocess in reviewer context,
<=180 seconds/2048 MiB through unchanged existing capture adapter; no GPU or grids.

Independent method: solve the affine geodesic IVP from periapse r=p with E=1, j=p/sqrt(f(p)),
v=dr/dlambda=0, T=phi=0 and

    r'=v, v'=j²(2r+3b)/(2r⁴), T'=1/f, phi'=j/r².

Integrate outgoing half-ray to r_B=8; record event r_A=6 along that same solution.
The two accumulated angular legs sum to the required 2. Root-find p in the predeclared
bracket [2,5.5]. No parent scientific code imported or copied; parent uses transformed
radial quadrature. Endpoints r_A/B are independently supplied; the return uses the
explicit instantaneous reversing relay. Read angle from atan2(k_hat_phi,k_hat_r),
clock normalization from f_A and accumulated T. Normalize proper time by L/c_E.

IVP method DOP853; lambda ceiling 100; terminal r_B event. Two controls:
coarse rtol=2e-10, atol=2e-12, max_step=0.1; fine rtol=2e-12, atol=2e-14,
max_step=0.05. Root brentq xtol=2e-12, rtol=1e-13, maxiter=100.
Record original null constraint (-1+v²+j² f/r²)/f at solver mesh and 201
uniform affine samples, endpoint radius errors, angular boundary residual, nfev.
The initial tangent, affine ODE and tetrad conventions derive from the supplied full metric.

Pass bounds: each bracket must strictly change sign; all IVPs succeed and reach endpoints
within lambda limit; positive f on K certified analytically by the conservative bound
1-|a|*10²-|b|/1.5 >= 8/15; both p and the full ray stay in K. At p>=2 and
|b|<=0.4, 2r+3b>=2.8>0, giving the exact regular-turn and no-barrier condition.
Original null residual <=2e-8; endpoint radius error <=2e-10; phi boundary residual
<=2e-8. Fine/coarse p, angle and normalized RTT agree within 2e-8*max(1,abs(value)).
Flat p, angle and RTT agree with Euclidean chord formulas by the same bound.
At fixed b, p varies across a by <=2e-8 and angle range exceeds 1e-5, supporting
only these finite witnesses; no universal numerical uniqueness claim.

When parent output becomes available, compare matching fine cases with the same 2e-8
scaled bound. If a check fails, retain all diagnostics and report the failure before a
bounded repair. No adaptive expansion of sample family, branch hunt or fitted tolerance.
This is a convergence-controlled floating-point cross-check with equation residuals,
not interval certification, empirical validation or proof of a global theorem.
