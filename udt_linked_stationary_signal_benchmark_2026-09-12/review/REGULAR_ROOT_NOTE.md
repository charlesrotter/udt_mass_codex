# Bounded endpoint-root regularity check

Reviewer contribution, 2026-09-12 23:37 UTC, after the initial source-first review
and independent finite ODE replay. The parent checked the argument and supplied
the rational final bound below. This is same-premise hypothesis verification for
the nine diagnostic geometries, not a general-family uniqueness theorem, new
physical premise, amended numerical freeze, or independent review of this note
by an additional context. Original candidate, contract and code remain unchanged.

The initial finite code checked a sign bracket, simple radial turn and absence
of an intermediate radial barrier. Those checks alone would not, for an arbitrary
scalar endpoint equation, prove a nonzero derivative at its root. The exact theorem
already assumes a regular chosen branch. This note supplies a direct derivative
bound on the reviewer bracket and avoids confusing a simple radial turn with a
regular endpoint boundary map.

Fix only the diagnostic endpoints r_A=6, r_B=8, p in [2,5.5], b in [-0.4,0.4].
The permitted lapse parameter a cancels from the endpoint angular evaluator.
In each leg set theta=acos(p/r). Direct substitution in candidate (7) gives

    Phi_R(p,b) = integral_0^acos(p/R) [1+(b/p)K(theta)]^(-1/2) dtheta,
    K(theta)=(1-cos(theta)^3)/(1-cos(theta)^2)
            =cos(theta)+1/(1+cos(theta)),
    1 <= K(theta) <= 3/2 for 0 <= theta <= pi/2.

The removable value at theta=0 is 3/2. Since |b|/p<=1/5, the integrand
denominator is at least 7/10. Differentiation is justified on the entire compact
interval. Let theta_R=acos(p/R). Then

    d Phi_R/dp = -[1+(b/p)K(theta_R)]^(-1/2)/sqrt(R²-p²)
                +(b/(2p²)) integral_0^theta_R
                    K(theta)[1+(b/p)K(theta)]^(-3/2) dtheta.

For b<=0 both terms are nonpositive and the endpoint term is strictly negative.
For 0<=b<=2/5, p>=2, the two-leg derivative has the conservative upper bound

    d(Phi_6+Phi_8)/dp
      <= -(1/6+1/8)/sqrt(13/10) + 3*b*pi/(4*p²)
      < -49/192 + 33/140
       = -131/6720 < 0.

The first estimate uses sqrt(R²-p²)<=R and 1+(b/p)K<=13/10. The integral
estimate uses denominator>=1, K<=3/2 and theta_R<pi/2 on both legs. The rational
last bound follows from 1/sqrt(13/10)>7/8 (640>637 after squaring) and pi<22/7.
Thus on this exact bracket the angular endpoint equation is strictly decreasing,
and any root is regular and unique within that bracket. This does not establish
that every supplied family member has a root, or classify additional roots outside
the bracket, winding paths, general caustics, horizons or arbitrary endpoints.

The saved independent replay records a sign change on [2,5.5] and all nine numerical
roots in [3.2111,4.0822]. These are floating-point root locations,
not interval certificates. The analytic derivative bound covers their bracket
without relying on derivative sampling. For this supplied non-antipodal endpoint
layout (separation 2 radians), the equatorial plane is fixed by spherical symmetry;
this check makes no separate universal claim about out-of-plane conjugacy.
