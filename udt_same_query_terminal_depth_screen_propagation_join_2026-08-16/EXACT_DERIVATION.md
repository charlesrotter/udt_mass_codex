# Exact derivation — same-query terminal depth closes the local screen parameter

Date: 2026-08-16
Status: `INTERNALLY_VERIFIED_WITH_CAVEATS__EXTERNAL_REVIEW_PENDING`

## 1. Bounded question

G108 derives the screen-volume rate

\[
a_{\rm eff}=\frac{\operatorname{tr}(\dot W W^{-1})}{2\dot\delta}
\]

when a supplied observer query identifies the complete pair-screen block `W=Q(SY+Z)` with its
regular Jacobi screen map. It left `delta(lambda)` supplied. This audit asks whether the same
query's already-derived terminal reciprocal coordinate supplies that map without an extra
coefficient or law.

The audit does not select the metric history, query, branch, initial screen, or a global relation
family.

## 2. Unique terminal coordinate

On the regular terminal stratum

\[
h_{00}<0,\qquad \det h<0,
\]

the complete pair metric has the unique positive decomposition

\[
h=-T^2(dy^0+\beta dy^1)^2+L^2(dy^1)^2,
\]

with

\[
T^2=-h_{00},\quad
\beta=\frac{h_{01}}{h_{00}},\quad
L^2=h_{11}-\frac{h_{01}^2}{h_{00}}.
\]

Writing

\[
T=e^{\kappa-\phi_{\rm pair}},\qquad
L=e^{\kappa+\phi_{\rm pair}}
\]

gives the exact terminal readout

\[
\boxed{
\phi_{\rm pair}=\frac12\log\frac LT
=\frac14\log\frac{-\det h}{h_{00}^2}.
}                                                     \tag{1}
\]

Every retained coframe and pair-realization channel has already entered `h` before (1).

## 3. The endpoint transition contains the founded character

The positive upper-triangular terminal coframe is

\[
B_i=
\begin{pmatrix}
T_i&T_i\beta_i\\
0&L_i
\end{pmatrix}.
\]

For two literally matched states of one calibrated family,

\[
R_{ij}=B_jB_i^{-1}.
\]

Its diagonal entries are

\[
(R_{ij})_{11}=\frac{T_j}{T_i}
=e^{\Delta\kappa_{ij}-\Delta\phi_{ij}},
\]

\[
(R_{ij})_{22}=\frac{L_j}{L_i}
=e^{\Delta\kappa_{ij}+\Delta\phi_{ij}},
\]

where

\[
\Delta\phi_{ij}=\phi_j-\phi_i.
\]

Therefore its diagonal part factors exactly as

\[
e^{\Delta\kappa_{ij}}
D(\Delta\phi_{ij}),
\qquad
D(\rho)=\operatorname{diag}(e^{-\rho},e^{+\rho}).
\]

Equivalently,

\[
\boxed{
\Delta\phi_{ij}
=-\frac12\log\frac{(R_{ij})_{11}}{(R_{ij})_{22}}.
}                                                     \tag{2}
\]

Equation (2) is not similarity by appearance alone: it is the founded reciprocal representation
with the sign and unit fixed by the pure reciprocal reduction. The common-scale and shift channels
remain present in their own parts of `R_ij`.

For three literally matched states,

\[
R_{jk}R_{ij}=R_{ik},\qquad R_{ji}=R_{ij}^{-1},
\]

so

\[
\boxed{
\Delta\phi_{ik}=\Delta\phi_{ij}+\Delta\phi_{jk},\qquad
\Delta\phi_{ji}=-\Delta\phi_{ij}.
}                                                     \tag{3}
\]

Thus one coherent calibrated pair family realizes the founded supplied-depth character by an
endpoint potential difference. This is conditional endpoint descent, not a theorem that every
path or independently constructed tape is equivalent.

## 4. `c_E` normalization

The terminal reciprocal calibration is

\[
\frac{c_{\rm eff}^{(\rm pair)}(i)}{c_E}=\frac{T_i}{L_i}=e^{-2\phi_i}.
\]

Consequently

\[
\boxed{
\frac{c_{\rm eff}^{(\rm pair)}(j)}{c_{\rm eff}^{(\rm pair)}(i)}
=e^{-2\Delta\phi_{ij}}.
}                                                     \tag{4}
\]

On `h=diag(-e^{-2\rho},e^{+2\rho})`, equation (1) returns `phi_pair=rho` exactly. No new scale,
sign, or coefficient enters. This remains an inter-observer pair calibration, not a local signal
speed.

## 5. Continuous same-query ownership

Let `h(lambda)` be a smooth regular family belonging to the same query and fix a reference
`lambda_0`. Define

\[
\boxed{
\delta(\lambda;\lambda_0)
=\phi_{\rm pair}(\lambda)-\phi_{\rm pair}(\lambda_0).
}                                                     \tag{5}
\]

Then

\[
\dot\delta=\dot\phi_{\rm pair},
\]

where the complete time-live terminal derivative is

\[
\boxed{
\dot\phi_{\rm pair}
=\frac14\operatorname{tr}(h^{-1}\dot h)
-\frac12\frac{\dot h_{00}}{h_{00}}.
}                                                     \tag{6}
\]

The second derivative needed by the reparameterized Riccati equation is

\[
\ddot\phi_{\rm pair}
=\frac14\operatorname{tr}
\left(h^{-1}\ddot h-h^{-1}\dot h h^{-1}\dot h\right)
-\frac12\left[
\frac{\ddot h_{00}}{h_{00}}-\left(\frac{\dot h_{00}}{h_{00}}\right)^2
\right].                                             \tag{7}
\]

Equations (5)--(7) remove `delta(lambda)` as an independent input **inside this same supplied
query family**.

## 6. Join to Jacobi/Riccati propagation

When the same query identifies `W=Q(SY+Z)` with its regular Jacobi map,

\[
\ddot W+\mathcal R_{\perp}W=0,
\qquad
L_{\rm opt}=\dot W W^{-1}.
\]

On any interval where `dot(phi_pair) != 0`, equations (5) and G108 give

\[
\boxed{
a_{\rm eff}(\phi_{\rm pair})
=\frac12\frac{d\log|\det W|}{d\phi_{\rm pair}}
=\frac{\operatorname{tr}L_{\rm opt}}{2\dot\phi_{\rm pair}}.
}                                                     \tag{8}
\]

Define

\[
K_\phi=\frac{L_{\rm opt}}{\dot\phi_{\rm pair}},\quad
f_\phi=\frac{\ddot\phi_{\rm pair}}{\dot\phi_{\rm pair}^2},\quad
\mathcal T_\phi=\frac{\mathcal R_\perp}{\dot\phi_{\rm pair}^2}.
\]

Then the exact depth-parameterized Riccati equation is

\[
\boxed{
\frac{dK_\phi}{d\phi_{\rm pair}}
+K_\phi^2+f_\phi K_\phi+\mathcal T_\phi=0.
}                                                     \tag{9}
\]

The complete metric and supplied initial data determine the expansion and shear contained in
`K_phi`; equation (8) is only its trace character.

## 7. Invariances and non-invariances

- A common terminal rescaling `(T,L)->(Omega T,Omega L)` changes `kappa` and leaves `phi_pair`
  unchanged.
- A passive orthonormal screen rotation leaves both `h` and `|det W|` unchanged.
- The shift `beta` is retained in `h` and `R`; it is not appended to or deleted from (1).
- An independent reciprocal endpoint recalibration changes `phi_pair`. It is not gauge after the
  A-calibrated clock/ruler tape is fixed; it defines a different query calibration.

## 8. Middle resets and path scope

If an `A-B` tape ends at `B_in` and an independently built `B-C` tape begins at `B_out`, the correct
composition contains

\[
M_B=B_{B_{\rm out}}B_{B_{\rm in}}^{-1}.
\]

At scalar level,

\[
\Delta\phi_{AC}
=\Delta\phi_{A,B_{\rm in}}
+\Delta\phi_{B_{\rm in},B_{\rm out}}
+\Delta\phi_{B_{\rm out},C}.                       \tag{10}
\]

Omitting the reset creates the exact error

\[
\phi_{B_{\rm in}}-\phi_{B_{\rm out}}.
\]

The same-query closure therefore cannot be promoted to arbitrary independently rebuilt observer
tapes or to route independence in the presence of holonomy.

## 9. Degenerate strata

- If `dot(phi_pair)=0`, endpoint differences (2)--(5) remain defined, but `phi_pair` is not a valid
  local propagation coordinate and equations (8)--(9) must be replaced by affine propagation.
- At a turning point, depth parameterization is piecewise branch-local.
- If `det W=0`, the Jacobi screen reaches a caustic and the log-area/Riccati chart fails.
- If `h00=0` or `det h=0`, the terminal decomposition itself leaves its regular chart.

None of these loci is identified here with `X_max`, a material boundary, or a physical branch
selection rule.

## 10. Verification

Production SymPy checks prove the terminal decomposition, transition factorization, composition,
reversal, derivative identities, nonlinear joined rate, Jacobi/Riccati equations, passive screen
rotation invariance, middle-reset correction, and explicit turning/caustic type boundaries. The
turning control uses `phi_pair(z)=z^2` and regular `W(z)=exp(z) I`; the caustic control uses
`W(z)=z I`, whose optical trace is `2/z`.

An independent implementation uses exact `Fraction` endpoint matrices and a separate nonlinear
finite-difference replay. Its maximum residuals are:

```text
endpoint character/composition/reversal   2.78e-17
terminal phi recovery                     1.11e-16
joined nonlinear finite difference        3.05e-11
independent saved-atlas replay             2.78e-17
```

## 11. Maximum conclusion

The bounded result is

```text
CONDITIONAL_SAME_QUERY_DEPTH_JOIN_DERIVED
__TERMINAL_PHI_PAIR_OWNS_G108_LOCAL_DEPTH_MAP
__G108_LOCAL_DEPTH_MAP_NO_LONGER_INDEPENDENT
__MATCHED_CALIBRATION_AND_REGULARITY_REQUIRED
__PHYSICAL_HISTORY_QUERY_BRANCH_INITIAL_SCREEN_AND_GLOBAL_DESCENT_OPEN
```

This joins previously separate exact results. It does not select the physical history or query and
does not turn a conditional pair calibration into a universal spacetime scalar.
