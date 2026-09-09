# LG2 — exact localized vacuum geometry, restricted symmetric data

Initial candidate, UNPROMOTED; author/root context,2026-09-09. Question and
method scope recorded in ../CAMPAIGN_LOG.md before construction. LG1 is used
only at its reviewed conditional scope, not as an accepted registry grade.

## Statement and quantifiers

Fix any supplied G324 compact split-translation quotient and T0>0. Work in
constant orthonormal spatial coordinates on an embedded ball, with
gamma0=I, K0=diag(a,-2a,-2a), a=1/(3T0)>0. Fix concentric radii

    0<r_in<r_-<r_+<r_out<the embedded-chart/injectivity bound.

Fix a smooth radial cutoff chi that equals1 near and inside r_- and0 near
and outside r_+, and a prescribed sufficiently high finite regularity norm.
These domains, coordinates, cutoff and witness symmetry are freely supplied
mathematical data/controls, not physical boundaries or additional UDT laws.

Conditional on the smooth local-deformation and local-development methods
specified below, there exists u_*>0 such that for every real
0<|u|<min(u_*,1/10) there are smooth global vacuum initial data (gamma_u,K_u)
on the SAME compact slice, with all four constraints satisfied and Lambda=0,
equal to (gamma0,K0) outside r_+, and equal to (I,K_in(u)) inside r_-.
The data are close to background in the chosen finite regularity norm and
gamma_u is positive definite. A justified smooth local vacuum development
exists; it is not locally isometric everywhere to the original Taub spacetime.
The modification is supported in an embedded THREE-dimensional ball, not
an axially periodic slab or a topology-changing neck.

The threshold depends on T0, the chart/radii, cutoff and the chosen norms.
No explicit numerical threshold, uniformity as radii shrink/T0 approaches0,
all-data matching, uniqueness of completion, genericity or stability is claimed.
This is an existence statement for a declared sufficient data family, not a
claim that reflection symmetry is necessary or physically selected.

## 1. Lawful interior and a deliberately nonlawful interpolation

Set c=(1-u^2)/(1+u^2), s=2u/(1+u^2) (so c^2+s^2=1) and define

    k1=a(-1+2c), k2=a(-1-c+sqrt(3)s), k3=a(-1-c-sqrt(3)s),
    K_in=diag(k1,k2,k3).

Then sum k_i=-3a and sum k_i^2=9a^2. With gamma=I these constant data obey
H=0 and M=0 exactly. They are ordinary nearby anisotropic Kasner data, not a
new response law; at u=0 they reduce to the supplied exterior datum.

On the annulus Omega={r_-<r<r_+}, start with
bar_gamma=I, bar_K=K0+chi DeltaK, DeltaK=K_in-K0. Since trace DeltaK=0,

    H(bar_gamma,bar_K)=chi(1-chi)|DeltaK|^2,
    M_i(bar_gamma,bar_K)=Delta k_i partial_i chi.            (3)

The errors are smooth, small with u, and supported strictly away from both
annulus boundaries. They are generally NONZERO. A cutoff alone is not a
lawful completion and is explicitly excluded as evidence of one.
No mean-curvature, flat-metric, or conformal ansatz is imposed on the corrected
collar. Both initial tensors may change there.

## 2. Actual projected-deformation interface

Mathematical source: Chrusciel--Delay, gr-qc/0301073v2,
Theorem5.9 and Corollary5.11; the fixed-reference-kernel and local inverse
construction are in Proposition3.3/Theorems3.6,3.9. We use the projected
constraint theorem, NOT a no-KID theorem or a topology-changing construction.

For precision let C=(J,H), with J=-2 M raised by the spatial metric, matching
the source's zero set. P is its linearization and P* its metric L2 adjoint.
Choose a reflection-invariant defining function d on Omega, e.g.
d=(r^2-r_-^2)(r_+^2-r^2), and a fixed weight parameter sigma>0. Write
phi=d^2, psi=exp(-sigma/d), Phi(Q,h)=(phi Q,phi^2 h).
The theorem supplies a small correction of the form

    (deltaK,deltagamma)=psi^2 Phi^2 P*_(bar_K,bar_gamma) w,
    projection_(Kref-perp) [psi^-2 C(bar_K+deltaK,bar_gamma+deltagamma)]=0. (4)

Kref is the kernel of Phi P* at the FIXED background (K0,I), not the kernel
at the interpolated/corrected data. The complement/projection uses the
source's weighted metric inner product. The small potential w in that
complement is unique in the inverse-function neighborhood; the full space
of all constraint completions is not claimed unique.

Here is the applicability check, as a theorem interface rather than a
machine-certified PDE proof:

- Omega has smooth compact closure and two smooth boundary components, with
  no change of topology. d>0 inside and dd is nonzero at each boundary.
- Background gamma0,K0 are smooth up to both boundaries and gamma0 is positive.
  The source's limits d^4|Ric(gamma0)|, d|Hess d|,
  d^2|K0|+d^4|D K0| tend to0. Derivatives and weighted norm requirements hold
  since the tensors are constant and d is smooth. The weighted scaling and
  boundary estimates are those established by the cited theorem, not an
  additional unverified no-KID hypothesis.
- For fixed cutoff/radii, bar_K-K0 and its required finite derivatives tend
  to0 with u; bar_gamma=gamma0. The constraint error is supported where d is
  bounded away from0. Hence it is small in every required FIXED finite
  weighted norm and belongs to all the smooth exponentially weighted spaces.
- The theorem works with nonzero Kref by projection. Smooth bootstrap and
  zero extension of the correction across both boundaries use Corollary5.11.
  Smallness controls positivity in a norm embedding into C0. Higher finite
  closeness may be obtained by choosing the corresponding theorem index;
  no single computed radius in the Frechet topology is asserted.

The mathematical boundary weights are analytic tools, not energy, physical
cutoffs, scale selection or a new UDT action. Compactly supported smooth data
are NOT asserted analytic. The source's underlying weighted inverse and
regularity theorems are imported conditionally; neither symbolic checks nor
review of this application re-proves that general analysis.

## 3. Removing the actual nonlinear residual

LG1 gives the full Kref: three translations and R=y partial_z-z partial_y,
all with zero lapse. Multiplication by phi is invertible on the open annulus;
these smooth fields are in the decaying-weight potential spaces, and no other
weak kernel fields arise by interior elliptic regularity and LG1's local
classification. In particular there is no scalar-lapse residual left hidden.

Let G be the eight coordinate reflections (x,y,z)->(sx x,sy y,sz z), each
s_i=+1 or-1. Omega,d,cutoff,background and interpolated tensors are invariant.
The four kernel basis characters under pullback are respectively

    sx, sy, sz, sy sz.                                    (5)

Each is nontrivial. Thus the G-fixed subspace of Kref is ZERO. Central parity
alone would leave the rotation and is insufficient; all three independent
coordinate reflections are used here as a sufficient witness construction.

The full constraint map, its metric adjoint, weight multiplications and the
fixed-kernel projection commute with these reflections. The weighted inner
product/complement is invariant. Apply any reflection to the small solution
potential w of (4): it gives another solution in the same small complement.
Local uniqueness of the inverse solution gives reflection invariance of w,
and therefore of the correction and the completed data. This is not an
assumption that arbitrary completions must be symmetric.

The full weighted nonlinear residual in (4) is consequently G-invariant.
Equation(4) places it in Kref. Equation(5) then forces that residual to be0,
not merely small or orthogonal to selected samples. Hence ALL pointwise
Hamiltonian and momentum constraints hold exactly. This is the load-bearing
new inference applying the cited projected method to this background/family.
It does not infer sufficiency from LG1's four finite balances alone.

The correction is flat to every order at the annulus boundaries, so extension
by zero gives globally smooth data on the original compact quotient. Inside
r_- and outside r_+ the respective initial tensors stay exactly unchanged.
The reflections are used only on the embedded annulus; they need not extend
to symmetries of a general supplied lattice marking.

## 4. Actual local development and non-gauge geometry

G303/G315's conditional smooth harmonic local-development method applies:
the completed slice is smooth compact and boundary-free, gamma positive,
K smooth symmetric, all constraints exact, Lambda=0 fixed, and Bianchi gives
the homogeneous gauge-constraint propagation equation in the full metric-wave
system. Thus each datum has an actual smooth local Ricci-flat development,
with geometric uniqueness in the usual marked local sense. We do not claim
to solve that evolution numerically or to re-prove the imported PDE theorem.
G321's explicit method-interface distinction is retained, not its special
G320 data claims imported as this result.

The interior agrees with ordinary homogeneous Kasner initial data having
p_i=-T0 k_i, sum p_i=sum p_i^2=1, and explicit local metric

    -dT^2 + sum_i (T/T0)^(2p_i) (dx^i)^2.

By local uniqueness it agrees with that metric in the interior's local domain
of dependence. In the orthonormal frame there, the magnetic Weyl part is0
and the electric Weyl eigenvalues at T0 are

    E_i=p_i(1-p_i)/T0^2 = tau k_i-k_i^2.

These are the eigenvalues of the complex self-dual Weyl endomorphism when
its magnetic part vanishes, up to a common convention factor/sign. Their
repeated-versus-distinct property is invariant under observer/frame changes.
E_i-E_j=(k_i-k_j)k_l for distinct i,j,l. For0<|u|<1/10, all k_i are nonzero
and pairwise distinct; hence all three E_i are distinct. At u=0 the Taub
background has E=(-4,2,2)a^2, with a repeated eigenvalue everywhere. The new
development is therefore not a coordinate change or a reslicing of Taub:
its interior Weyl endomorphism has a different algebraic multiplicity.
This tests spacetime geometry, not merely different marked K components.

Exterior agreement persists only where local domain of dependence/uniqueness
supports it. There is no claim of an eternally unchanged exterior, long-time
existence, geodesic completeness, physical dynamical stability or an isolated
object. Nor does this construction select initial content, a shape, a physical
size or an actual population. The given metric equation permits this family
conditionally; it does not require that nature instantiate it.

## Evidence and limits

author_check.py independently checks original interior constraints, the
unrepaired cutoff error, the full finite-group kernel action (including the
central-parity false pass), and exact Weyl eigenvalue discriminant. These
finite symbolic checks support algebra and reject shortcuts; they are NOT
the general weighted existence/regularity proof. Fresh source-first and direct
adversarial review is required; all review limits will control the result.
No same-premise repair has yet occurred. No registry, canon or fixed manuscript
change; full365 remains NOT_PASSED at the existing G325 replay gate.

Primary mathematical method: https://arxiv.org/pdf/gr-qc/0301073 (v2,
Theorem5.9,Corollary5.11; fixed-reference construction in section3).
