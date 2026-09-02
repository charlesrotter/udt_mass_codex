# G327 exact derivation — primitive axial Fourier tensor modes

Date: 2026-09-02
Status: `INTERNAL_VERIFIED_PENDING_EXTERNAL_REVIEW`

## 1. Bounded question

Classify the complete transverse-tracefree tensor first variation in the primitive nonzero axial
Fourier eigenspace of every registered G324 compact Taub quotient. The active bounded equation is

\[
S_{ab}:=R_{ab}-\frac14R g_{ab}=0.
\tag{1}
\]

This equation is active only through Charles's provisional adoption of Universal Reciprocity/DDR
and the G312 premises. It is not a derived or canonized UDT equation.

In proper time and fixed quotient coordinates the background is

\[
g_0=-dT^2+C_1^2T^{-2/3}dX^2+C_\perp^2T^{4/3}(dy^2+dz^2),
\qquad T>0.
\tag{2}
\]

If `L_X` is G323's primitive axial period, define

\[
k_1=\frac{2\pi}{L_X},\qquad \nu=\frac{|k_1|}{C_1}>0.
\tag{3}
\]

No numerical wavelength or new physical scale is chosen: both quantities in (3) belong to the
supplied quotient background.

## 2. Complete declared tensor ansatz and gauge

Let `e(X)` be either `cos(k_1 X)` or `sin(k_1 X)`. For transverse indices `A,B` in `{y,z}`, write

\[
\delta g_{AB}=2C_\perp^2T^{4/3}H_{AB}(T)e(X),
\qquad
H_{AB}=
\begin{pmatrix}
h_+&h_\times\\
h_\times&-h_+
\end{pmatrix}.
\tag{4}
\]

Both polarizations and both real phases are retained. Every other perturbation component is zero
in this declared invariant sector.

For a periodic infinitesimal vector in the same Fourier eigenspace,

\[
\xi^a=\xi^a(T)e^{ik_1X},
\]

all transverse spatial derivatives vanish. The transverse part of `L_xi g_0` receives only the
time-shift contribution

\[
(\mathcal L_\xi g_0)_{AB}
=\xi^0\partial_T(C_\perp^2T^{4/3})\delta_{AB},
\tag{5}
\]

which is pure trace. Its transverse-tracefree projection is exactly zero. The plus and cross
amplitudes in (4) are therefore invariant under every legal periodic gauge vector in this Fourier
sector. Synchronous presentation was chosen, but the two tensor amplitudes are not synchronous-
gauge artifacts.

## 3. Direct first variation and constraint closure

Production reconstructs the background Christoffel symbols and differentiates the connection and
Ricci tensor directly. The implementation-distinct verifier instead constructs the full
epsilon-dependent metric, inverts it exactly, forms its full Christoffel/Ricci tensors, and only
then differentiates at `epsilon=0`.

Both routes obtain

\[
\delta R=0
\tag{6}
\]

and zero for every `00`, `0i`, `11`, `1A`, and transverse-trace component. Thus the Hamiltonian and
momentum constraints and all components outside the declared tensor block vanish; they were not
discarded.

The only nonzero residual coefficients are

\[
\frac{\delta S_{yy}}{C_\perp^2T^{4/3}e}
=-\frac{\delta S_{zz}}{C_\perp^2T^{4/3}e}
=\ddot h_++\frac1T\dot h_++\nu^2T^{2/3}h_+,
\tag{7}
\]

\[
\frac{\delta S_{yz}}{C_\perp^2T^{4/3}e}
=\ddot h_\times+\frac1T\dot h_\times+\nu^2T^{2/3}h_\times.
\tag{8}
\]

Therefore each polarization and spatial phase obeys the same closed equation

\[
\boxed{
\ddot h+\frac1T\dot h+\nu^2T^{2/3}h=0
}.
\tag{9}
\]

The zero-wave-number limit of (9) is `h=constant+constant log T`, matching the transverse constant
lattice mode and local Kasner-shear time behavior found independently in G325/G326. That is a
regression check, not an input to (9).

## 4. Exact time basis

Set

\[
z=\frac34\nu T^{4/3}.
\tag{10}
\]

Then `dz/dT=nu T^(1/3)`, and (9) becomes

\[
\frac{d^2h}{dz^2}+\frac1z\frac{dh}{dz}+h=0.
\tag{11}
\]

This is the order-zero Bessel equation. Its complete basis is

\[
\boxed{h(T)=A J_0(z)+B Y_0(z)}.
\tag{12}
\]

Production substitutes both functions into (9) exactly. The standard Bessel Wronskian transforms
to

\[
T\left(J_0\frac{dY_0}{dT}-\frac{dJ_0}{dT}Y_0\right)
=\frac8{3\pi}\ne0,
\tag{13}
\]

so neither solution may be discarded.

## 5. Complete real mode census

There are:

- two transverse tensor polarizations, plus and cross;
- two real spatial phases, cosine and sine, representing the `n=+1,-1` reality pair;
- two independent time solutions, `J_0` and `Y_0`.

Hence the declared real solution space has exactly

\[
\boxed{2\times2\times2=8}
\tag{14}
\]

integration constants. These are local spatially varying tensor modes, not the homogeneous
lattice/frame moduli counted by G325/G326.

## 6. Local curvature witness

The direct Riemann calculation gives the same on-shell transverse-tracefree tidal coefficient for
either polarization amplitude `h`:

\[
\boxed{
\delta\mathcal E_{\rm TF}[h]
=-\frac{\dot h}{3T}+\frac{4h}{9T^2}+\nu^2T^{2/3}h
}.
\tag{15}
\]

For plus this is the normalized `0y0y-0z0z` component; for cross it is the normalized `0y0z`
component. It is not the zero differential operator on the solution space. Together with the exact
gauge result (5), this separates the modes from both gauge and locally curvature-free quotient
deformations.

## 7. Compact-time norm and endpoint classification

No endpoint boundary condition is imposed. On any compact interval
`I=[T_-,T_+]` strictly inside `T>0`, use the declared metric-relative diagnostic

\[
\|H\|_{I,1}=\sup_{T\in I}
\left(\|H\|_F+\frac{\|\dot H\|_F}{\nu T^{1/3}}\right).
\tag{16}
\]

The divisor is the instantaneous metric norm of the axial Fourier covector. It makes (16)
dimensionless and converts the derivative term exactly to a Bessel derivative. It is a diagnostic,
not an action, energy, acceptance filter, or new physical postulate. Since `z>0` on `I`, every
solution (12) has finite norm there.

As `T` approaches zero, `z` approaches zero. The `J_0` branch tends to a finite constant. The
`Y_0` amplitude has the independent logarithmic behavior required by the repeated indicial root.
The latter's derivative part in (16) diverges more strongly; it is recorded, not rejected. The
past endpoint is not part of the G324 manifold.

As `T` tends to infinity, both Bessel functions and their `z` derivatives have envelope
`z^(-1/2)`. Since `z` is proportional to `T^(4/3)`,

\[
\boxed{\|H\|_{\text{relative phase space}}=O(T^{-2/3})}
\tag{17}
\]

with increasingly rapid oscillation. This is future decay in the declared relative first-order
mode norm. It is not a statement about second-derivative curvature norms, arbitrary Fourier
directions, the complete perturbation system, or nonlinear stability.

## 8. Bounded landing

```text
PRIMITIVE_AXIAL_TENSOR_MODE_CLOSES_AS_TWO_GAUGE_INVARIANT_POLARIZATIONS
__BESSEL_ZERO_TIME_BASIS__FINITE_AND_LOGARITHMIC_PAST_BRANCHES
__OSCILLATORY_T_MINUS_TWO_THIRDS_FUTURE_DECAY__NO_FULL_STABILITY_CLAIM
```

Status: `INTERNAL_VERIFIED_PENDING_EXTERNAL_REVIEW`.

Still open: scalar/vector inhomogeneous sectors, wavevectors in the transverse plane or oblique to
the axial direction, higher harmonics, the full Fourier spectrum, endpoint-uniform control of the
complete system, nonlinear coupling, full stability, other backgrounds/topologies, physical
occupancy, history selection, scale, observation, matter/mass, and physical `X_max`. No UDT metric,
reciprocal-kernel, angular-sector, or adopted equation formula changed.

