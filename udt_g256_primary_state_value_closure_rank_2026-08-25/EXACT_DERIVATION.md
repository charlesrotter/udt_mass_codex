# G256 exact derivation — primary-state value-closure rank

## Landing

`FUNCTION_VALUED_PRIMARY_STATE_REMAINS__ANGULAR_INTERLOCK_IS_TOMOGRAPHIC_NOT_PROPAGATING__NO_ODE_GPU`

This is a bounded negative closure result, not a negative result for the UDT metric or reciprocal
kernel. The native equations tested here are mutually coherent and strongly reconstructive. They do
not, by themselves, generate the values of the primary profile across different observer events.

## 1. Primary metric and completed radial pair

In calibrated radial variables \(\tau=c_Et\), the declared primary metric is

\[
g=-e^{-2\phi(r)}d\tau^2+e^{2\phi(r)}dr^2+r^2d\Omega^2.
\]

On the radial observer-pair plane,

\[
h=-T^2d\tau^2+L^2dr^2,
\qquad T=e^{-\phi},\qquad L=e^{\phi}.
\]

The G176 completed-pair rule therefore gives, conditionally on that supplied calibrated pair,

\[
\Phi=-\log T=\phi,
\qquad m=TL=1.
\]

Thus the scalar whose network values are being tested is not an added kernel field: it is the
primary metric profile itself on this pair family.

## 2. Exact connected-network rank

Choose one orientation for each edge of a connected graph with \(N\) event vertices and incidence
matrix \(B\). For vertex values \(\Phi=(\Phi_1,\ldots,\Phi_N)^T\), the matched-clock scalar descent is

\[
\delta=B\Phi,
\qquad \delta_{ij}=\Phi_j-\Phi_i.
\]

Every connected incidence matrix has

\[
\ker B=\operatorname{span}\{(1,\ldots,1)^T\},
\qquad \operatorname{rank}B=N-1.
\]

After fixing one reference value, the compatible vertex-state dimension is therefore exactly

\[
\nu(N)=N-1.
\]

For \(E\) edges, the number of independent cycle relations is

\[
E-N+1.
\]

Those cycle relations enforce actual composition. They do not reduce the \(N-1\) anchored vertex
values because they annihilate \(B\) identically. On the complete graph, an explicit basis is

\[
\delta_{0i}+\delta_{ij}-\delta_{0j}=0,
\qquad 1\le i<j<N.
\]

The exact sweep covers path, star, cycle, and complete graphs for \(2\le N\le12\). The arbitrary-
\(N\) kernel argument above supplies the general proof.

## 3. Angular interlock is exact tomography

For

\[
p=r\phi'(r),\qquad q=r^2\phi''(r),
\]

the two primary angular amplitudes are

\[
A_{\parallel}=e^{-2\phi}(2p^2+p-q),
\qquad
A_{\perp}=1-e^{-2\phi}(1+p).
\]

At fixed finite real \(\phi\), their Jacobian with respect to \((p,q)\) is

\[
\det\frac{\partial(A_{\parallel},A_{\perp})}{\partial(p,q)}
=-e^{-4\phi}\ne0.
\]

The inverse is exact:

\[
p=e^{2\phi}(1-A_{\perp})-1,
\]

\[
q=2p^2+p-e^{2\phi}A_{\parallel}.
\]

This is a substantive native interlock: the angular response and reciprocal profile are not
independent instruments. But when \(A_{\parallel}\) and \(A_{\perp}\) are outputs of the same
metric—not externally prescribed data—the inverse reconstructs the local profile jets and supplies
no residual equation among them. It is tomography, not propagation.

## 4. Arbitrary finite radial jets have exact smooth realizations

Let \(r_1,\ldots,r_N>0\) be distinct, and prescribe arbitrary finite values

\[
(\phi_i,p_i,q_i).
\]

These specify ordinary jets

\[
\phi(r_i)=\phi_i,
\qquad
\phi'(r_i)=\frac{p_i}{r_i},
\qquad
\phi''(r_i)=\frac{q_i}{r_i^2}.
\]

There is a unique polynomial of degree below \(3N\) matching all \(3N\) conditions. To prove
invertibility without assuming an interpolation package, observe that a homogeneous solution would
have a triple zero at every \(r_i\). It would therefore be divisible by

\[
\prod_{i=1}^N(r-r_i)^3,
\]

which already has degree \(3N\); a polynomial of degree below \(3N\) must be zero. The square
confluent evaluation map is therefore injective and hence bijective.

Moreover, adding any nonzero multiple of that product preserves all registered value, first-, and
second-derivative data while changing higher germs. Thus even complete finite angular-jet samples
do not reduce the primary state to a finite global family.

The production and independent implementations verify exact rational examples for
\(2\le N\le8\), with no tolerance or floating-point comparison.

## 5. Time-live carry has the same rank ceiling

For event-clock potentials, reversal and actual composition remain

\[
\delta_{ji}=-\delta_{ij},
\qquad
\delta_{ik}=\delta_{ij}+\delta_{jk}.
\]

They again express \(\delta_{ij}=\Phi_j-\Phi_i\). Consequently the anchored event-state dimension is
\(N-1\). The same exact Hermite construction realizes arbitrary finite event values and local first
and second germs, while the cubed-node product changes higher time-live germs invisibly to those
finite constraints.

This does not say that dynamics are impossible. It says the tested carry laws are consistency and
reconstruction laws, not a currently owned evolution residual.

## 6. Owner and solver gates

The exact 18-source frozen manifest was classified before result banking. No source owns a natural,
nonidentity value law that rejects one registered regular valuation while retaining another.
Consequently no finite-family propagation equation, ODE, PDE, or GPU initial-value problem is yet
defined by this bounded source universe.

Observations could reconstruct or calibrate values at sampled events, but using them now would fit a
free function. Under the preregistered rules, calibration is scientifically licensed only after a
finite native family or an independently owned global law exists.

## 7. Exact scope

What is established:

- the primary reciprocal scalar network has \(N-1\) anchored degrees of freedom for arbitrary
  connected \(N\)-event graphs;
- angular modes exactly reconstruct the first two radial profile jets at finite \(\phi\);
- arbitrary finite radial and event-clock jets have exact smooth realizations;
- no frozen source in the 18-file bounded universe owns a nonidentity value-propagation law;
- ODE/PDE/GPU work remains gated because no residual has been derived.

What is not established:

- that no future UDT-native value law exists;
- that the metric, completed pair kernel, angular interlock, or time-live carry is defective;
- a physical observer population, boundary completion, matter/source law, topology, or singular
  behavior;
- any observational fit, calibration, \(X_{\max}\), or preferred profile.
