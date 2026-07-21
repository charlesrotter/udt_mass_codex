# P02 formulae, conventions, and scope

## Indices and signature

Coordinate indices are `a,b,c,d = 0,1,2,3`. The exact regular witness metric is
`eta=diag(-1,1,1,1)`. In a supplied `2+2` chart, base indices are `i,j=0,1` and screen indices are
`A,B=2,3` (stored internally as `0,1`). This assignment is conditional bookkeeping, not a selected
UDT reciprocal plane.

The Riemann convention is the P01 convention:

`R^rho_(sigma mu nu) = partial_mu Gamma^rho_(nu sigma) - partial_nu Gamma^rho_(mu sigma)
                       + Gamma^rho_(mu lambda) Gamma^lambda_(nu sigma)
                       - Gamma^rho_(nu lambda) Gamma^lambda_(mu sigma)`.

## Zero jets and the supplied split

For base `h`, screen `q`, and vertical-by-base shift matrix `A`,

`g = [[h + A^T q A, A^T q], [q A, q]]`.

With `L=[[I,0],[A,I]]`, this is the exact congruence

`g = L^T diag(h,q) L`.

Consequently, inertia and rank add and `det(g)=det(h)det(q)`, including degenerate closure strata.
The regular P01 split branch is Lorentzian `h` and positive-definite `q`; the other 35 products are
retained as supplied-split type-change closures, not promoted physical signatures.

## First jets

For the independent signed local field witness, `p_a=(dphi)_a` and its causal scalar is

`s_phi = g^(ab) p_a p_b`.

The nonzero null stratum `s_phi=0` is separate from `p=0`. Horizontal/vertical support is meaningful
only relative to the supplied split.

Define horizontal fields

`H_i = partial_i - A_i^A partial_A`.

Their vertical Frobenius curvature is

`F^A_ij = H_i(A_j^A) - H_j(A_i^A)`.

The supplied horizontal distribution is locally integrable exactly when `F^A_01=0` for both screen
components. This does not derive the distribution or a global product.

The screen deformation tensor along `H_i` is

`B_iAB = (1/2)(L_Hi q)_AB`,

with

`(L_Hi q)_AB = H_i(q_AB) - (partial_A A_i^C)q_CB - (partial_B A_i^C)q_AC`.

Its expansion and shear are

`theta_i = tr(q^-1 B_i)`,

`sigma_iAB = B_iAB - (theta_i/2)q_AB`.

Under positive common rescaling `q -> Omega^2 q`, the exact point transformation is

`theta_i -> theta_i + 2 H_i(ln Omega)`,

`q^-1 sigma_i -> q^-1 sigma_i`,

while `A` and `F` are unchanged. Thus expansion is representative data; shear-map rank and twist
rank are pre-scale invariant relative to the supplied split.

## Normal-coordinate second jets

At a regular point, coordinates may be chosen so `g=eta` and `partial g=0`. For any algebraic
curvature tensor in the declared convention, the exact metric second jet is

`g_(mu nu),ab = -(1/3)(R_(mu a nu b)+R_(mu b nu a))`.

Direct substitution reconstructs the original Riemann tensor. This makes every exact curvature
witness a genuine local metric two-jet rather than an abstract matrix detached from geometry.

The 150 raw components split as 10 metric values, 40 first derivatives, and 100 symmetric second
derivatives. Normal-form use of the coordinate Jacobian, second coordinate derivatives, and third
coordinate derivatives removes `10+40+80=130` components, leaving the 20 algebraic Riemann
components. Six residual local Lorentz transformations still act on those tensor components.

## Exact Weyl plus Schouten direct sum

In four dimensions,

`R_abcd = C_abcd + g_ac P_bd - g_ad P_bc - g_bc P_ad + g_bd P_ac`,

where

`P_ab=(1/2)(Ric_ab-(R/6)g_ab)`.

`SECOND_JET_DIRECT_SUM_BASIS.tsv` gives ten exact symmetric-Schouten basis tensors and ten exact
Weyl basis tensors. Their combined 21-by-20 upper-bivector component matrix has exact rank 20;
every prefix increases rank. This proves that arbitrary continuous coefficients in the two sectors
cover the complete algebraic curvature space and that their intersection is zero. The rank and
Petrov tables are marginal discriminant strata inside this continuous direct sum; they are not an
assumption that every marginal label combines independently.

Under `g -> exp(2 sigma)g`, at a point with `sigma=0` and `d sigma=0`,

`P'_ab = P_ab - partial_a partial_b sigma`.

The symmetric Hessian has ten independent components and acts with exact rank ten on `P`. It can set
the Schouten tensor to zero at one point without changing Weyl. This is local CSN bookkeeping, not a
global representative selection and not an EH or vacuum equation.

## Weyl/Petrov convention

Use the bivector order `(01,02,03,23,31,12)` and bivector metric
`diag(-1,-1,-1,1,1,1)`. A complex symmetric trace-free self-dual operator is `Q=E+iB`. The exact
real Weyl bivector bilinear is

`[[E,B],[B,-E]]`.

The invariants are

`I=(1/2)tr(Q^2)`, `J=-(1/6)tr(Q^3)`, and `Delta=I^3-27J^2`.

Types `I`, `D`, and `II` are separated by `Delta` and the minimal polynomial; `III`, `N`, and `O`
are separated by `Q^3=0`, `Q^2=0`, and `Q=0`. Petrov type is invariant under local Lorentz frame
change and positive CSN. Each type retains continuous moduli where applicable.

## Scope boundary

Every formula above is local differential geometry. No quantity is set to zero by an EOM. No action,
source, carrier, mass, finite-cell boundary, global topology, physical representative, physical
history, or branch preference is supplied.
