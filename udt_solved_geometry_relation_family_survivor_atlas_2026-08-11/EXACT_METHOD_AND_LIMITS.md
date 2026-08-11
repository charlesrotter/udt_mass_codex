# Exact method and limits

## What was solved

For every preregistered metric witness, the production implementation solved the affinely
parameterized Levi-Civita geodesic equation

```text
d2 x^a/ds2 + Gamma^a_bc (dx^b/ds)(dx^c/ds) = 0
```

together with parallel transport

```text
dP^a_b/ds + Gamma^a_cd (dx^c/ds) P^d_b = 0.
```

The differential of the exponential map at the registered endpoint was approximated by centered
shooting in all four initial-velocity directions. This is a numerical Jacobi/geodesic-deviation
propagator. The R17 normal connection was independently integrated on the same declared paths.

The production method used complex-step metric derivatives and adaptive DOP853. The independent
method duplicated both coframe families, used centered finite differences, and used fixed-step RK4.
It did not import the production solver.

## Metric families

The stationary family is the source-owned R17 coframe on `R x S3`, with all three registered
`lambda` strata and symmetric field perturbations. Its global topology is source-owned, but the
smooth `phi` profile used here is a `free-and-explored` kinematic witness; it is not certified as a
solution of a missing native field equation.

The time-live family is the complete local factorized coframe

```text
E = [[B, 0], [Q S, Q]],
B = [[exp(kappa-phi), exp(kappa-phi) beta], [0, exp(kappa+phi)]],
```

with `kappa`, `phi`, `beta`, both independent `Q` deformations, all four entries of `S`, all four
coordinates, and the symmetric perturbation active. It is deliberately `LOCAL_OFFSHELL_ONLY`.

## Pair readout and path data

On R17, the registered clock-ruler two-plane gives

```text
phi_pair = (1/4) log[(-det h)/(h00^2)] = phi.
```

The numerical identity defect is at most `1.67e-16`. This certifies the algebraic readout on these
witnesses. It does not select a physical observer path.

Endpoint coframe transitions form an exact atlas coboundary, so their triangle composition defect
is roundoff-sized. Path-labelled Levi-Civita and R17 normal transport are separate data. Their
nonzero loop returns do not contradict the endpoint scalar; the channels can coexist.

The R17 normal-orientation sign was fixed to the declared positive coframe orientation. Reversing
that presentation reverses the reported normal angle but does not change its identity/nonidentity
class. No physical orientation is selected by this choice.

## What was not solved

No native field evolution, action, source, matter carrier, boundary completion, density/bootstrap
law, `X_max` value, observational fit, or physical pair-map selector entered the computation.
Accordingly:

- “survivor” means only persistence as a regular solved geometry in this bounded witness set;
- no result is dynamical or physical stability;
- no branch is selected as the physical UDT relation;
- the local time-live family is not a global completion;
- absence of a cut or conjugate point by affine parameter `0.4` says nothing beyond that interval;
- the witness set is not the complete UDT metric solution space.
