# Projector deformation-neighborhood audit — preregistration

Date: 2026-08-01  
Frozen base: `4fa6de0d52b0be976cb39a5b91ab49cd33164c66`  
Mode: CPU-only, metric-led configuration-space geometry

## Question frozen before outcome calculation

Do the intrinsic clock line, twist-selected ruler line, rank-one ruler projector, global descent,
and nonzero relative projector curvature found at the six complete off-shell configurations C01--C06
persist on genuine neighborhoods after releasing the already-registered profile and complete screen
degrees of freedom?  Where do the exact certificate, metric, slice, twist, and response walls occur?

This is an observing question.  It does not ask for a particle, lump, mass, action, stable object, or
preferred branch.

## Frozen complete-family frame

On the registered global left-invariant coframe of `S3`, retain

```text
theta0 = exp(-phi) (dt + a sigma3),
theta1 = exp(+phi) sigma3,
(theta2,theta3)^T = P(q) (sigma1,sigma2)^T,
g = -theta0^2 + theta1^2 + theta2^2 + theta3^2.
```

The six centers have the frozen generic profile `phi0=F_GENERIC/50`, `a=1/64`, and
`P0=exp(lambda phi0) I` for `lambda in {-2,-1,0,1/2,1,2}`.  Around every center release:

- arbitrary stationary smooth `C3` profile perturbations needed by the curvature-fingerprint gate;
- arbitrary stationary smooth invertible `GL(2,R)` screen perturbations, equivalently the area and
  both metric shears plus the local `O(2)` coframe-gauge direction near the center;
- the continuous equal-screen `lambda` direction and the registered one-/two-shear subfamilies as
  exact lower-dimensional charts.

The twist amplitude remains the registered nonzero constant for the primary neighborhood theorem.
Twist-off is retained as a boundary control.  No action or field equation restricts the deformations.

## Frozen gates

1. **Clock certificate:** three complete-metric scalar-curvature gradients have rank three at one
   regular event.  This is a sufficient certificate for a unique continuous Killing line inside the
   stationary family, not a necessary characterization of every intrinsic clock.
2. **Ruler:** the twist of that same intrinsic clock is nonzero and spans one global unoriented
   spacelike line.
3. **Projector:** the ruler gives a rank-one projector in the positive clock-orthogonal rank-three
   bundle and a unique rank-two complement.
4. **Global configuration:** `phi` and `P` are smooth on `S3`, `det(P)` never vanishes, and the
   four-metric is Lorentzian.  The positive displayed-slice stratum is recorded separately.
5. **Response:** the relative projector curvature is nonzero at at least one regular event.

Each gate is classified separately.  A zero of the selected curvature component is not called a
zero-response wall unless the complete relative-curvature endomorphism vanishes.  A zero of the
rank-three fingerprint determinant is only a certificate wall; it is not automatically failure of
intrinsic clock uniqueness.

## Certification and falsification contract

The primary conclusion passes only if:

- all six frozen centers are reconstructed exactly;
- every center has nonzero clock-certificate determinant and nonzero relative-curvature witness;
- continuity is applied in the correct finite-jet topology and proves an open functional
  neighborhood for every center;
- the full registered screen tangent contains area and both shears, with coframe gauge not counted as
  an additional metric degree of freedom;
- smooth `P:S3->GL(2,R)` and finite smooth `phi` give exact global descent, while `det(P)=0`, twist-off,
  slice-null, clock-certificate, and complete-response walls remain visible;
- exact finite-dimensional subfamilies are reported without being promoted to the full functional
  neighborhood;
- a separate implementation reconstructs every load-bearing local algebra result without importing
  the production module; and
- mutation catches fail on a missing center, omitted shear, false gauge metric mode, erased wall,
  zeroed response, certificate/property conflation, action/bootstrap injection, or on-shell wording.

The result is falsified or narrowed if any center is isolated, any claimed open gate is not
continuous in the stated topology, any global line/projector fails to descend, or any positive
conclusion depends on inserting the `S2` carrier or `L2+L4` action.

## Maximum allowed conclusion

At most:

```text
DERIVED_CONDITIONAL_ON_THE_REGISTERED_STATIONARY_COMPLETE_OFFSHELL_FAMILY:
EACH_C01_C06_CENTER_LIES_IN_AN_OPEN_CONFIGURATION_NEIGHBORHOOD_WITH_THE_NAMED
INTRINSIC_PROJECTOR_GATES_AND_NONZERO_RELATIVE_CURVATURE.
```

No profile, screen, `lambda`, topology, action, coefficient, source, boundary, bootstrap law,
matter family, stability, or mass may be selected.  Fresh external semantic review remains open and
is not authorized by this audit launch.
