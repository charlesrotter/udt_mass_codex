# UDT full time-live characteristic and boundary-flux audit

Date: 2026-07-21

Base: `21cfeb8f25fe18afe5a5a924ea073a9cfc24238b`

Preregistration: `0624a56`

Mode: CPU-only exact symbolic and finite-dimensional boundary-phase-space audit; no evolution solve.

## Result first

Time dependence adds real structure, but it does **not** close the boundary-selector seam.

The classification is:

```text
TIME_LIVE_REDUCES_BUT_DOES_NOT_SELECT_BOUNDARY_DATA
```

The exact conditional propagation results are:

| lane | regular metric characteristic | order/multiplicity | status |
|---|---|---|---|
| L01 pre-scale `C^2` | metric null cone | double | `DERIVED / CONDITIONAL` |
| L02 post-scale EH | metric null cone | simple | `DERIVED / CONDITIONAL` |
| L03 two-stage bridge | undefined | no operator | `OPEN` |

The two named bulk lanes therefore agree on the local cone but not on characteristic multiplicity.
That cone controls principal propagation. It does not say that the finite-cell seal lies on the cone,
and it does not select a boundary polarization.

All ten symmetric metric components were retained in each principal matrix. At exact timelike,
spacelike, and null covectors, the ungauge-fixed flat-point ranks are:

| lane | timelike rank/nullity | spacelike rank/nullity | null rank/nullity |
|---|---:|---:|---:|
| L01 Bach | 5/5 | 5/5 | 1/9 |
| L02 Einstein | 6/4 | 6/4 | 4/6 |

The non-null kernels reproduce the four diffeomorphism directions and, for Bach, the common-Weyl
direction. The null rank drop is the ungauge-fixed signature of the characteristic cone. These are
local principal-symbol statements, not a physical gauge, a well-posedness theorem, or a global
solution.

## The time-live seal identity

For the registered reciprocal representative with arbitrary positive angular block,

```text
ds^2 = -c^2 exp(-2 phi) dt^2 + exp(2 phi) dr^2 + q_AB dx^A dx^B,
```

the exact first-jet norm is

```text
g^-1(dphi,dphi)
 = -exp(2 phi) phi_t^2/c^2
   +exp(-2 phi) phi_r^2
   +q^AB phi_A phi_B.
```

If, as a **conditional exploratory extension**, the time-live seal is a regular level surface
`phi=0`, then its normal is `dphi`. Its causal type is therefore not fixed by the reciprocal metric:
exact first jets exist with negative, zero, and positive norm. CSN rescales the norm by the positive
factor `Omega^-2`; it preserves these classes but selects none.

For the radial moving subcase `r=r_b(t)`, level-set tangency gives

```text
phi_t + v phi_r = 0,        v = dr_b/dt,
g^-1(dphi,dphi)|seal = phi_r^2 (1-v^2/c^2).
```

Thus a regular radial seal is null exactly when `v=+c` or `v=-c`. This is a useful conditional
identity, but neither `v` nor nullness is supplied by Reciprocity. The static canonical subcase has
`v=0`; when `phi_r` is nonzero its normal is spacelike and its boundary worldtube is timelike, hence
non-characteristic. If `phi_r=0`, `phi=0` does not define a regular level surface at that point.

The static canon does not itself authorize the global time-live level-set extension, so the branch
in which no moving seal has yet been defined remains explicit.

## Characteristics are not polarization

The characteristic cone answers where principal disturbances can propagate. Boundary polarization
answers which canonical half of the boundary data is fixed or allowed to vary. The former does not
mathematically choose the latter.

For the L02 non-null comparison completion, the canonical flux has the familiar structural form

```text
omega_boundary = delta pi^ij wedge delta gamma_ij.
```

The scalar seal fixes one reciprocal-ratio coordinate tangent. Two exact six-dimensional flux-free
subspaces still survive:

1. fix every induced-metric variation and leave its momenta free;
2. fix only the reciprocal-ratio coordinate plus the transverse momenta, leaving the reciprocal
   momentum and transverse induced metric free.

They are inequivalent and both preserve the supplied scalar seal clause. This use of canonical EH
data is a conditional comparison; it does not adopt GHY or Dirichlet data as UDT.

For L01 the exact parent non-null flux is

```text
n.Theta = -8 epsilon E^ij delta K_ij
          + Pi_h^ij delta h_ij
          + corner divergence,
P_K^ij = -8 epsilon E^ij,
h_ij P_K^ij = 0.
```

The trace-free electric-Weyl momentum and CSN null direction make this a constrained
presymplectic system. The audit therefore does **not** assign it twelve unconstrained canonical
pairs or a final reduced rank. Nevertheless two exact differentiable classes remain:

1. `delta h=0`, every `delta K` free, with the natural trace-free `E=0` equation;
2. only the scalar seal component of `delta h` fixed, transverse `delta h` and every `delta K` free,
   with natural `E_TF=0`, projected `Pi_h=0`, and corner-flux equations.

Both preserve the canonically free normal reciprocal jet. They are inequivalent. Time dependence
does not eliminate either.

## Angular-sector flux survives the scalar seal

The scalar wire `delta phi=0` does not constrain every transverse metric perturbation. Exact local
canonical-pair witnesses give nonzero angular/off-diagonal flux in both lanes while the reciprocal
variation vanishes.

The stronger on-principal-shell witnesses use the transverse-traceless angular-shape polarization

```text
h_22 = -h_33 = q(t,x),
```

which is annihilated by each null principal matrix. With `Box=-partial_t^2+partial_x^2`:

- L02: `q1=t-x`, `q2=(t-x)^2` obey `Box q=0` and have normalized boundary symplectic flux
  `j^x=-1` at `(t,x)=(1,0)`;
- L01: `q1=x^2+t x`, `q2=t-x` obey `Box^2 q=0` and have normalized fourth-order flux `j^x=-2`
  at the same point.

“Normalized” removes only the common nonzero conditional lane coefficient. These are local
principal solutions, not nonlinear global UDT solutions. Their role is decisive but narrow: time
dependence can carry flux through an unsealed angular channel, so the scalar seal alone cannot make
the complete boundary variational problem differentiable.

## Constraints do not choose incoming data

The exact identities

```text
nabla^a B_ab=0,       g^ab B_ab=0,
nabla^a(G_ab+Lambda g_ab)=0
```

provide diffeomorphism and, in L01, Weyl constraint propagation once an evolution split, gauge,
initial data, and compatible boundary data have been chosen. An identity that propagates a
constraint is not a rule selecting one constraint-preserving boundary subspace. The explicit
multiple flux-free subspaces prove the distinction here.

## Why the boundary functional remains open

None of the following ambiguities is removed by the characteristic calculation:

1. overall action normalization;
2. the free Euler-density coefficient `beta`, which changes boundary/corner data but no regular 4D
   metric bulk equation;
3. exact bulk divergences;
4. `Theta -> Theta + delta Y + dZ` improvements;
5. boundary Legendre transforms exchanging coordinate and momentum polarization;
6. orientation, reference, and generator normalization; and
7. moving-embedding and joint/corner terms.

A null seal would add rather than remove the still-open generator, auxiliary-null, normalization,
cross-section, and joint data. The non-null Gaussian split cannot be silently carried onto it.

## Completeness and stop

Eight causal/domain branches were retained, including no time-live seal extension, fixed non-null,
moving timelike/null/spacelike, type-changing, the distinct WR-L null horizon, and
quotient/crossing/internal matching. None is selected.

All 21 lane/field-realization pairs were counted. Only L01/C01 and L02/C01 have conditional metric
principal operators. Every realization with an independent `phi`, coframe, projector, multiplier,
bridge, or connection still lacks that field's characteristic equation and flux. L03 has no
operator. Zero pairs are P06-ready.

The maximum conclusion is:

```text
TIME_LIVE_CHARACTERISTIC_AND_BOUNDARY_FLUX_SELECTOR_STATUS_CLASSIFIED
```

No action, boundary functional, coframe, carrier, source, mass, scale, charge, global solution, or
time-live numerical solve was selected.

## Four evidence gates

1. **Preregistered:** yes, commit `0624a56` before algebra.
2. **Full or bounded scope:** complete for the current-authority regular local metric principal
   symbols, all ten metric components, the exact non-null parent boundary channels, all 21 field
   pairs, and eight causal/domain branches. It is not a nonlinear global solution-space census.
3. **Independently verified:** a non-importing implementation reconstructed 28 algebraic checks and
   rejected 45 deliberate corruptions. A fresh adversarial-context scientific review has not been
   completed, so the package remains `LEAD_PENDING_FRESH_ADVERSARIAL_REVIEW`.
4. **Premises audited:** yes. The time-live level-set seal, both bulk lanes, non-null canonical
   decompositions, diagnostic quotient, and normalized TT witnesses are explicitly conditional.
