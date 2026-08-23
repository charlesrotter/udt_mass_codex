# G230 preregistration — first nonlinear neighboring-tile obstruction

Date: 2026-08-23
Status: `PRE_OUTCOME__METRIC_LED__EXACT_FINITE_DIMENSIONAL`

## Frozen question

Determine whether the G227 algebraic-curvature and G228 differential-Bianchi conditions suffice
for the second curvature derivative of one smooth Lorentz metric. If not, identify the first exact
nonlinear overlap obstruction and test whether the complete compatible target is realized by a
metric 4-jet in geodesic normal coordinates.

## Frozen convention and tensors

Use the G229 curvature convention

```text
R^rho_(sigma mu nu)
 = partial_mu Gamma^rho_(nu sigma)
 - partial_nu Gamma^rho_(mu sigma)
 + Gamma^rho_(mu lambda) Gamma^lambda_(nu sigma)
 - Gamma^rho_(nu lambda) Gamma^lambda_(mu sigma).
```

At a locally inertial origin fix `g_ab=eta_ab`, `g_ab,c=0`, with

```text
H_ab,cd   = g_ab,cd,
K_ab,cde  = g_ab,cde,
L_ab,cdef = g_ab,cdef,
E_feabcd  = (nabla_f nabla_e R)_abcd.
```

`H` and `K` are the G229 normal representatives of supplied compatible `(R,nabla R)`. The new
fourth metric derivative `L` is symmetric in `(ab)` and in `(cdef)`.

The Ricci commutator is frozen as

```text
E_feabcd - E_efabcd
 = - R^p_(a f e) R_pbcd
   - R^p_(b f e) R_apcd
   - R^p_(c f e) R_abpd
   - R^p_(d f e) R_abcp.
```

The direct metric calculation is the sign authority if this displayed identity disagrees with the
frozen G229 Riemann convention.

## Whole arenas

- `R`: all 20 algebraic-curvature components;
- `D=nabla R`: all 60 G228-compatible components;
- `E`: all `16*20=320` ordered derivative-pair/algebraic-curvature slots;
- `L`: all `10*35=350` metric fourth-derivative coefficients;
- differentiated differential-Bianchi rows: every outer derivative applied to the complete G228
  cyclic family;
- commutator rows: every antisymmetric derivative pair and all 20 curvature slots;
- quintic identity-linear coordinate changes: all `4*56=224` coefficients;
- normal-coordinate rows: the full `L_i(j,klmn)=0` family, without deleting dependent rows.

## Maps to construct

1. The linear highest-derivative map `C4:L -> E` obtained directly from the second derivative of
   the G229 curvature formula.
2. The complete affine metric map

   ```text
   E = C4(L) + Q(H),
   ```

   where `Q(H)` contains all connection-product and covariantization terms quadratic in the lower
   metric 2-jet.
3. The intrinsic affine constraint system consisting of differentiated Bianchi plus the Ricci
   commutator.
4. The quintic coordinate-gauge and fourth-order normal-coordinate maps.

No term may be discarded because it vanishes in a flat or constant-curvature control.

## Preregistered numerical expectations to test, not assume

The full metric source has dimension 350. The complete quintic fixed-lower-jet coordinate domain
has dimension 224. If the standard finite-order jet picture closes, the new compatible target has
dimension `350-224=126`.

Production must explicitly determine rather than insert:

- rank and kernel of `C4`;
- rank of the combined homogeneous intrinsic constraints on 320 `E` slots;
- rank of the quintic gauge image;
- rank of the fourth-order normal rows and the restricted normal-slice map;
- whether `Q(H)` satisfies the affine intrinsic equations for the complete quadratic curvature
  polynomial, not merely random samples.

## Preregistered alternatives

```text
A_FIRST_NONLINEAR_OBSTRUCTION_AND_FULL_4JET_REALIZATION
  The Ricci commutator supplies a nonzero R-times-R obstruction not implied by G227/G228 alone;
  the combined affine differentiated-Bianchi plus commutator target has translation dimension 126;
  C4 has rank 126/kernel 224; quintic gauge equals the kernel; the normal slice is 126-dimensional
  and maps isomorphically; Q(H) satisfies the complete affine identities.

B_NO_NEW_SECOND_ORDER_OBSTRUCTION
  The commutator is identically zero or already follows from the G227/G228 data in the declared
  full arena, so independently assigned second changes introduce no new overlap condition.

C_EXTRA_FOURTH_ORDER_OBSTRUCTION
  Differentiated Bianchi plus the Ricci commutator leave a target larger than the metric 4-jet image,
  or the affine lower-jet term fails their claimed sufficiency.

D_TYPING_SIGN_OR_GAUGE_FAILURE
  The ordered derivative convention, affine offset, normal slice, or coordinate kernel is defective;
  no realization theorem is banked.
```

## Certification contract

Production must use exact arithmetic and save all ranks, hashes, nonlinear identity checks, and a
specific nonzero commutator witness. Polynomial completeness of the quadratic check must be
certified by coefficient comparison or an exact polarization basis covering every quadratic
monomial in the 20 curvature coordinates.

An independent implementation must not import the production derivation. It must rebuild the
linear maps from index definitions, reproduce all load-bearing ranks, verify the commutator sign on
at least one direct polynomial-metric witness, and confirm that a zero-`E` assignment can pass the
G227/G228 lower-order gates while failing G230.

Hostile tests must catch at least:

1. deleted connection-product terms in `Q(H)`;
2. deleted covariantization terms;
3. reversed commutator sign;
4. symmetrizing the ordered derivative pair before applying the affine condition;
5. omitting differentiated Bianchi rows;
6. truncating the quintic coordinate gauge;
7. promoting pointwise fourth-order realization to a finite-region field or physical history.

## Maximum conclusion

G230 may at most close the metric fourth-jet realization problem and identify the first nonlinear
necessary compatibility of neighboring local tiles. It may not prove smooth realization of an
arbitrarily prescribed finite-region curvature field, convergence of an infinite formal jet,
generate curvature values, populate observer/null relations, select transport, derive dynamics,
action, source, matter, bootstrap, boundary, `X_max`, transfer, observation, mass, signalling, or a
physical/global history.
