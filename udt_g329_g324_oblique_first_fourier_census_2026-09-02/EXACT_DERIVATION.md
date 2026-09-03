# G329 exact derivation — primitive oblique Fourier tile

Date: 2026-09-02

## 1. Bounded question and provenance

This tile asks only for the complete first variation of the G324 conditional background under the
owner-adopted provisional trace-free response equation. It neither changes nor rederives either
object.

After the constant coordinate rescaling `x=C1 X`, `ybar=C_perp y`, write

\[
g_0=-dT^2+T^{-2/3}dx^2+T^{4/3}(dy^2+dz^2),
\]

and

\[
\alpha=\frac{k_X}{C_1}>0,
\qquad
\beta=\frac{k_y}{C_\perp}>0.
\]

Every perturbation below carries the same factor
`exp(i(alpha x + beta y))`. The real field also contains its complex conjugate.

The only active equation is

\[
\delta\!\left(R_{ab}-\frac14R g_{ab}\right)=0.
\]

That equation remains conditional on Universal Reciprocity / DDR and the two G312 premises. No
action, source, matter model, observation, fit, scale, history, population, or physical
`X_max` enters this derivation.

## 2. All ten components and the exact parity split

The reflection `z -> -z` divides the ten normalized amplitudes into

\[
\begin{aligned}
\text{odd: }& h_{0z}=T^{2/3}N,\quad
h_{xz}=T^{1/3}H,\quad h_{yz}=T^{4/3}Q,\\
\text{even: }& h_{00}=-2A,\quad h_{0x}=T^{-1/3}B,\quad
h_{0y}=T^{2/3}C,\\
&h_{xx}=2T^{-2/3}U,\quad h_{xy}=T^{1/3}V,\quad
h_{yy}=2T^{4/3}W,\quad h_{zz}=2T^{4/3}Z.
\end{aligned}
\]

Production constructs every upper-triangle component of the four-dimensional first-variation
Ricci tensor from these unrestricted functions. [RAW_RESIDUALS.json](RAW_RESIDUALS.json) preserves
the complete symbolic result. No tensor, scalar, lapse, shift, or mixed component is omitted.

The background is Ricci-flat. The exact linearized identity is

\[
\nabla^a\delta S_{ab}=\frac14\nabla_b\delta R.
\]

On shell, either nonzero spatial component gives `i alpha delta R=0` or
`i beta delta R=0`, hence

\[
\delta R=0.
\]

This implication is false at the spatial zero mode; G329 does not use it there.

## 3. Complete periodic gauge quotient

For a same-mode periodic vector `(P,G_x,G_y,G_z)`, the exact Lie image is

\[
\begin{aligned}
A_g&=P',\\
B_g&=T^{-1/3}G_x'-i\alpha T^{1/3}P,\\
C_g&=T^{2/3}G_y'-i\beta T^{-2/3}P,\\
U_g&=-\frac{P}{3T}+i\alpha G_x,\\
V_g&=\frac{i\beta}{T}G_x+i\alpha T G_y,\\
W_g&=\frac{2P}{3T}+i\beta G_y,\qquad
Z_g=\frac{2P}{3T},\\
N_g&=T^{2/3}G_z',\qquad
H_g=i\alpha T G_z,\qquad Q_g=i\beta G_z.
\end{aligned}
\]

For `alpha beta != 0`, the conditions

\[
U=V=Z=Q=0
\]

have gauge determinant

\[
-\frac{2i}{3}\alpha^2\beta\ne0.
\]

They therefore define one complete periodic representative on every compact interval in `T>0`.
The associated gauge-invariant orbit amplitudes are

\[
\boxed{
\mathcal E=
W-Z-\frac{\beta}{\alpha T}V
+\frac{\beta^2}{\alpha^2T^2}\left(U+\frac Z2\right)
}
\]

and

\[
\boxed{
\mathcal O=H-\frac{\alpha T}{\beta}Q.
}
\]

In the complete representative, `mathcal E=W`, `mathcal O=H`.

## 4. Odd physical master

Put

\[
D=\alpha^2T^2+\beta^2.
\]

The odd constraint uniquely reconstructs the shift:

\[
N=-\frac{i\alpha T^{2/3}}{D}\left(T\mathcal O'-\mathcal O\right),
\qquad Q=0.
\]

The remaining equations are equivalent to

\[
\mathcal O''
+\frac{\beta^2-\alpha^2T^2}{TD}\mathcal O'
+\left[
DT^{-4/3}+\frac{\alpha^2T^2-\beta^2}{T^2D}
\right]\mathcal O=0.
\]

For the normalized amplitude

\[
\Psi_o=\frac{\mathcal O}{\sqrt D},
\]

this becomes

\[
\boxed{
\Psi_o''+\frac1T\Psi_o'
+\left[
DT^{-4/3}
+\frac{\beta^2(2\alpha^2T^2-\beta^2)}{T^2D^2}
\right]\Psi_o=0.
}
\]

All sixteen matrix entries of the reconstructed four-dimensional residual vanish exactly on this
equation.

## 5. Even physical master

Put

\[
d=4\alpha^2T^2+\beta^2.
\]

In the complete representative only the spatial amplitude `W=mathcal E` remains. Define the two
orthogonal shift combinations

\[
L=\beta B-\alpha T C,
\qquad
M=\alpha T B+\beta C.
\]

The two momentum constraints, the `zz` equation, and the Hamiltonian constraint reconstruct

\[
A=\frac{3\alpha^2T^2(TW'+W)}{d},
\]

\[
L=\frac{2i\alpha T^{2/3}}{3\beta}(3TW'-4A+3W),
\qquad
M=iT^{2/3}(A'-W'),
\]

\[
B=\frac{\beta L+\alpha T M}{D},
\qquad
C=\frac{-\alpha T L+\beta M}{D}.
\]

The single even master is

\[
\boxed{
W''
+\frac{4\alpha^2T^2+5\beta^2}{T(4\alpha^2T^2+\beta^2)}W'
+\left[
DT^{-4/3}+\frac{4\beta^2}{T^2(4\alpha^2T^2+\beta^2)}
\right]W=0.
}
\]

Again, all sixteen reconstructed residual entries and the scalar residual vanish exactly. The
positive quantities `D` and `d` prove there is no hidden compact-time rank change in the strictly
oblique stratum.

## 6. Exact coupling classification

The two physical equations are scalar and exactly decoupled by `z`-reflection parity. This does
not freeze the physical propagation direction. Both equations retain `alpha` and `beta`, and the
orthonormal angle obeys

\[
\tan\theta(T)=\frac{\beta}{\alpha T}.
\]

The rational terms in both masters are precisely the terms lost by pretending this angle is
constant. Thus the result is decoupled in parity but not blind to obliquity.

## 7. Curvature witnesses

The complete representative is a unique function of each periodic gauge orbit. Its intrinsic
slice-Ricci perturbation therefore supplies mode-local gauge-invariant curvature witnesses:

\[
\widehat{\delta R}^{(3)}_{xx}=\alpha^2\mathcal E,
\qquad
\widehat{\delta R}^{(3)}_{xz}=\frac{\beta^2}{2T}\mathcal O.
\]

Each is nonzero for a nonzero family on an open set, so neither master is a periodic Lie
derivative. This is a witness inside the registered Fourier tile, not a claimed nonlinear
spacetime invariant.

## 8. Component limits

The strictly oblique derivation never sets either component to zero. Only afterward:

- `beta -> 0` gives both G327 axial order-zero equations;
- `alpha -> 0` gives the G328 odd equation directly;
- for the even transverse limit, the oblique gauge coordinate is singular, while the regular
  transverse polarization `E=T^2W` obeys exactly the G328 even equation.

This nonuniform normalization is a coordinate feature of the polarization basis, not a lost
physical branch.

## 9. Complete compact-time and endpoint census

Both master coefficients are smooth on every compact interval inside `T>0`. Their exact
Wronskians are

\[
\mathcal W_e=C\frac{(4\alpha^2T^2+\beta^2)^2}{T^5},
\qquad
\mathcal W_o=\frac{C}{T},
\]

and never vanish.

As `T -> 0+`, `E=T^2W` has repeated indicial root zero, while `Psi_o` has roots `+1,-1`. Hence all
independent leading branches are

\[
E\sim 1,\ \log T;qquad
W\sim T^{-2},\ T^{-2}\log T;qquad
\Psi_o\sim T,\ T^{-1}.
\]

As `T -> infinity`, both equations have leading frequency `alpha T^(1/3)`, phase

\[
\frac34\alpha T^{4/3},
\]

and relative amplitude envelope `T^(-2/3)`. These are classifications only; no endpoint branch is
discarded and no endpoint condition is adopted.

Each complex master has two independent time constants. Reality adds the conjugate `-q` mode, or
equivalently cosine and sine phases. Therefore

\[
2\ \text{masters}\times2\ \text{time constants}\times2\ \text{real phases}=8
\]

real physical constants for the registered primitive tile.

## 10. Landing and boundary

The preregistered landing is

```text
PRIMITIVE_OBLIQUE_FOURIER_SECTOR_CLOSES_MODULO_PERIODIC_GAUGE
__TWO_PHYSICAL_AMPLITUDES__EXACT_COUPLING_CLASSIFICATION__EXACT_COMPACT_TIME_CENSUS
__NO_FULL_STABILITY_CLAIM
```

The formulas extend algebraically to every registered `alpha beta != 0`, but G329 is only the
primitive `(1,1,0)` tile. Other lattice pairs, simultaneous modes, uniform mode estimates,
nonlinear coupling, endpoints, physical population, scale, and global history remain open.
