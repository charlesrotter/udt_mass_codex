# Exact derivation — same-branch orbit geometry and selector rank

## Premise stamps

```text
COPRESENCE = WORKING_INTERPRETIVE_FRAME
FOUNDED_PHI_IDENTITY_AND_PAIR_ACTION = DERIVED
PHI_REALIZED_PROFILE_AND_VARIATION_LAW = OPEN
STRONG_LOCAL_CSN = CHALLENGED_OWNER_POSTULATE_NOT_DERIVED
X_MAX = WORKING_GLOBAL_OBSERVER_PAIR_SCHEMA
BOOTSTRAP = WORKING_ON_SHELL_ADMISSIBILITY_HYPOTHESIS
COMPLETE_WHOLE_SOLUTION_LAW = OPEN
```

## 1. The unique time line defines an intrinsic quotient geometry

For the registered stationary twisted family,

```text
tau = c_E dt + a sigma_3,
g = -exp(-2phi) tau^2
    + R^2 exp(2phi) sigma_3^2
    + R^2 exp(2lambda phi)(sigma_1^2+sigma_2^2).
```

Let `K=partial_t`. On the certified unique-K stratum, the line of `K` is intrinsic. The tensor

```text
q = g - K_flat tensor K_flat/g(K,K)
```

annihilates `K`, is invariant under its flow, and therefore descends through the free proper
stationary action to the three-dimensional orbit space. This construction does not require the
orthogonal distribution to be integrable; nonzero twist is allowed.

In the Maurer-Cartan basis, the exact Schur complement gives

```text
q = R^2 exp(2lambda phi)(sigma_1^2+sigma_2^2)
  + R^2 exp(2phi) sigma_3^2.
```

The shift parameter `a` cancels. It instead remains in the normalized stationary connection

```text
eta = K_flat/g(K,K) = dt + (a/c_E)sigma_3,
d eta = (a kappa/c_E) sigma_1 wedge sigma_2.
```

The displayed coefficient uses the registered generator `K=partial_t` and Maurer-Cartan
normalization. A constant rescaling of the group generator rescales the connection form; the
invariant content is the horizontal distribution and whether its curvature/twist vanishes. Thus the
same metric cleanly separates orbit-space shape from clock-fiber twisting.

## 2. Exact branchwise volume and its response

With `mu_sigma=sigma_1 wedge sigma_2 wedge sigma_3`,

```text
det(q) = R^6 exp[2(1+2lambda)phi],
dV_q = R^3 exp[(1+2lambda)phi] mu_sigma,
V_q[phi,lambda,R]
 = R^3 integral_S3 exp[(1+2lambda)phi] mu_sigma.
```

Its complete fixed-domain first variation within this family is

```text
delta V_q = integral_S3 dV_q
  [3 delta R/R + (1+2lambda)delta phi + 2phi delta lambda].
```

There is no `delta a` term. At `lambda=-1/2`, the volume density is `R^3 mu_sigma` and the entire
`phi` response vanishes, although the orbit metric can still change anisotropically. Volume is then
exactly blind to `phi`.

For fixed generic `lambda`, the `phi` derivative is one weighted-mean functional. If two disjoint
regions have positive weights `w1,w2`, the perturbation amplitudes

```text
(delta phi_1,delta phi_2)=(w2,-w1)
```

give `w1 delta phi_1+w2 delta phi_2=0`. Refining disjoint regions produces infinitely many
independent volume-preserving perturbations.

## 3. Finite global outputs do not give local functional rank

More generally, let a differentiable map of `m` scalar global outputs have derivative

```text
D F_phi : C-infinity(S3) -> R^m.
```

Choose `m+1` smooth bump functions with disjoint support. Their images form an `m by (m+1)` matrix,
which has a nonzero null vector. Repeating the construction on disjoint groups gives an
infinite-dimensional kernel of `D F_phi`.

This is a **local derivative-rank theorem**. It does not say a specially selected singular positive
functional could never have an isolated zero. No such functional or target is currently derived.
It does prove that ordinary regular equalities fixing finitely many global scalar outputs cannot
determine a smooth profile locally.

The active metric conditions around the exact witness are themselves open:

```text
curvature-invariant rank determinant != 0,
strict quotient/slice inequality > 0,
a kappa != 0,
d phi != 0 somewhere.
```

They persist under sufficiently small `C3`, `C0`, parameter, and `C1` perturbations respectively.
Consequently the certified unique-K twisted stratum contains an open infinite-dimensional
neighborhood; it is not an isolated profile.

## 4. The quotient diameter is not yet X_max

The positive smooth `q` on compact `S3` has a finite metric diameter

```text
D_q = max_(p,r in S3) d_q(p,r).
```

The maximum is attained. Its first variation can be nonsmooth when maximizing pairs or controlling
geodesics are nonunique.

The current `X_max` premise is an **unattainable observer-pair maximum-separation schema** whose
operational distance readout remains open. Therefore there is currently

```text
no derived identification D_q equivalent_to X_max
```

They could be related only by a separately derived observer-pair readout
or asymptotic completion. The bounded smooth witness also has bounded `phi`, so it does not itself
realize an infinite-depth `phi -> infinity` endpoint.

This does not weaken `X_max` as a potentially strong future constraint. It identifies the precise
missing bridge required before it can constrain this branch.

## 5. Scale, mass, density, and bootstrap

For `c_E^alpha G_obs^beta`, the `(L,M,T)` exponents are

```text
(alpha+3beta, -beta, -alpha-2beta).
```

No `alpha,beta` produce a length or mass density. If a length such as a physically identified
`X_max` were separately supplied, `c_E^2 X_max/G_obs` and
`c_E^2/(G_obs X_max^2)` would be valid mass and density scales. They would still be dimensional
definitions, not a same-solution mass law.

The new quotient result supplies a branchwise geometric map that a future recomputation arrow could
choose to use:

```text
X -> q[X] -> {V_q[X], D_q[X], curvature[q], ...}.
```

The orbit volume is not the induced proper volume of a hypersurface when the stationary connection
has twist; no orthogonal rest slices exist. UDT would still have to select orbit-space volume as the
physical volume used in a density definition. Indeed, the supplied `t=constant` slice has

```text
dV_t = dV_q sqrt[1-(a^2/R^2)exp(-4phi)],
```

which is different and `a`-dependent. This slice is a configuration presentation, not an intrinsically
selected density domain. In addition, no native total mass or energy `M[X]` is defined on this
branch. Hence even the candidate interface

```text
rho_candidate = M[X]/V_q[X]
```

remains a doubly conditional interface rather than an executable total proper density. The working bootstrap
architecture

```text
A(X,O)=0,
O-R[X]=0
```

still has no selected `R[X]`: no premise chooses these orbit outputs as its components or targets,
and native matter components, the local admissibility map `A`, and the return from global outputs to
local variation are absent.

## 6. Rank verdict

Within the preregistered same-branch selector universe:

```text
active independent equality/PDE selector rank on phi = 0;
residual profile tangent space = infinite dimensional;
branchwise geometric outputs = newly strengthened;
bootstrap return map = OPEN.
```

This does not disprove or derive bootstrap, and it does not change bootstrap's controlling status as
a working on-shell admissibility hypothesis. It derives prerequisite orbit geometry that a future
closure map could choose to use. The smallest missing object is a covariant same-branch global-to-local
closure equation or response map. If density participates, that object must also derive native
mass/energy and a common domain; inserting a density value cannot substitute for it.
