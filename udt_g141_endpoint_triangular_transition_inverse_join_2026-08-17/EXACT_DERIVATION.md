# G141 exact derivation — shared-carrier calibration comparison has an ordered inverse

## 1. Regular endpoint pair states

Let a supplied compatible co-present relation family provide, at each endpoint `i`, one regular
calibrated complete pair metric after the full angular/screen/mixing pullback has been formed:

\[
h_i=R_i^T\eta_2R_i,
\qquad
\eta_2=\operatorname{diag}(-1,1).
\]

On `h_{i,00}<0` and `det(h_i)<0`, the positive triangular factor is unique:

\[
R_i=
\begin{pmatrix}
T_i&T_i\beta_i\\
0&L_i
\end{pmatrix},
\qquad
T_i=\sqrt{-h_{i,00}},
\quad
\beta_i=\frac{h_{i,01}}{h_{i,00}},
\quad
L_i=\frac{\sqrt{-\det h_i}}{T_i}.
\]

Define the endpoint reciprocal and common-scale potentials

\[
\Phi_i=\frac12\log\frac{L_i}{T_i},
\qquad
\kappa_i=\frac12\log(T_iL_i),
\qquad
q_i=\frac{T_i}{L_i}=e^{-2\Phi_i}.
\]

These are conditional endpoint readouts, not universal point fields. Their comparison requires the
endpoint states to carry the same calibrated two-dimensional pair-coordinate carrier, clock/ruler
channel typing, and calibration local system. The triangular factor is unique in those supplied
calibrated coordinates; it is not invariant under an arbitrary `GL(2)` reparameterization.

Indeed, under independent positive-triangular endpoint changes

\[
h_i'=P_i^Th_iP_i,
\qquad
R_i'=R_iP_i,
\]

the endpoint value shifts by

\[
\Phi_i'=\Phi_i+\frac12\log\frac{(P_i)_{11}}{(P_i)_{00}}.
\]

Therefore `Phi_B-Phi_A` is invariant only when the calibration local system supplies the matched
endpoint carry. This is a load-bearing query premise, not a metric-only gauge theorem.

## 2. The shared-carrier calibration transition

Let `V` be the supplied common pair-coordinate carrier and `W` the common model Lorentz plane.
Regard each `R_i:V->W` as the positive triangular calibration map determined by `h_i`. Then

\[
C_{BA}=R_BR_A^{-1}:W\to W
\]

is a well-typed relative calibration automorphism. It obeys

\[
C_{CB}C_{BA}=C_{CA},
\qquad
C_{AB}=C_{BA}^{-1}.
\]

Since every `R_i` is positive upper triangular, every `C_BA` is in the positive upper-triangular
group `B^+(2)`. Its diagonal entries are

\[
(C_{BA})_{00}=\frac{T_B}{T_A},
\qquad
(C_{BA})_{11}=\frac{L_B}{L_A}.
\]

The ordered depth of B relative to A within this supplied compatible family is therefore the
grading character of the calibration comparison:

\[
\boxed{
\delta_{AB}
=\frac12\log\frac{(C_{BA})_{11}}{(C_{BA})_{00}}
=\Phi_B-\Phi_A.
}
\]

Reversal and composition now follow rather than being separately imposed:

\[
\delta_{BA}=-\delta_{AB},
\qquad
\delta_{AC}=\delta_{AB}+\delta_{BC}.
\]

The common-scale character is distinct:

\[
\frac12\log\det C_{BA}=\kappa_B-\kappa_A.
\]

The upper-right entry retains the relative shift. It does not affect either diagonal character.

## 3. A-normalized relative terminal metric

Expressing B's pair metric on the A-normalized model carrier gives

\[
h_{B|A}^{\rm rel}
=R_A^{-T}h_BR_A^{-1}
=C_{BA}^T\eta_2C_{BA}.
\]

For any positive triangular matrix `C=[[a,u],[0,d]]`,

\[
\frac{-\det(C^T\eta_2C)}{(C^T\eta_2C)_{00}^2}
=\left(\frac da\right)^2.
\]

Hence

\[
\boxed{
\phi_{\rm pair}(h_{B|A}^{\rm rel})
=\frac12\log\frac{(C_{BA})_{11}}{(C_{BA})_{00}}
=\Phi_B-\Phi_A
=\delta_{AB}.
}
\]

This is the precise endpoint meaning of the banked A-calibrated terminal formula. Reversing an
affine strip while keeping the same calibration does not construct this comparison; swapping the
ordered endpoint calibrations does.

For completeness, the distinct map

\[
D_{BA}=R_B^{-1}R_A:V\to V
\]

matches the endpoint metrics on the supplied pair carrier:

\[
D_{CB}D_{BA}=D_{CA},
\qquad
D_{AB}=D_{BA}^{-1},
\qquad
D_{BA}^Th_BD_{BA}=h_A.
\]

Its negative diagonal grading equals the same endpoint difference. `C_BA` and `D_AB` share that
diagonal grading but generally not their upper shift. Neither two-dimensional map is identified
with G123's full four-dimensional common-event chart differential. That stronger identification
would require the actual endpoint immersions and their derivatives.

More precisely, identifying `D_BA` with a restriction of a physical G123 transition requires the
two query maps to identify one ambient pair plane, preservation of that plane and its ordered
clock/ruler flag, and the same matched carrier calibration. Endpoint metrics alone cannot supply
this: if `h_A=h_B=eta_2`, then `R_A=R_B=I` gives constructed `D_BA=I`, while the nonidentity boost

\[
\Lambda=
\begin{pmatrix}5/4&3/4\\3/4&5/4\end{pmatrix},
\qquad
\Lambda^T\eta_2\Lambda=\eta_2,
\]

is an equally valid metric-preserving transition. The physical transition is therefore not
recoverable from `h_A,h_B` alone.

## 4. Reciprocal and bounded position laws

The endpoint reciprocal ratio is

\[
\boxed{
q_{AB}=e^{-2\delta_{AB}}=\frac{q_B}{q_A}.
}
\]

Therefore

\[
q_{AB}q_{BC}=q_{AC},
\qquad
q_{BA}=q_{AB}^{-1}.
\]

The G137 working position becomes

\[
\frac{x_{AB}}{X_{\max}}
=\tanh\delta_{AB}
=\frac{1-q_{AB}}{1+q_{AB}},
\]

and composes by the native Mobius law. No preferred endpoint potential zero is selected because a
common shift `Phi_i -> Phi_i-lambda` leaves every difference invariant.

If the endpoint `q_i` are the banked conditional pair `c_eff/c_E` readouts on the same carried
family, then `q_AB=q_B/q_A` is their inter-endpoint ratio. If A is chosen as the calibrated reference
with `q_A=1`, this reduces to the familiar A-rooted formula `q_AB=q_B`. This does not redefine
`c_eff` as a local material signal speed.

## 5. Why the full-GL no-go does not apply conditionally

A real additive character on the full `GL(4)` comparison group cannot recover the determinant-one
reciprocal squeeze. G141 does not contradict that theorem. After the ordered clock/ruler basis and
matched calibration local system are supplied, the regular pair metric admits a unique triangular
factor in `B^+(2)`, whose positive diagonal ratios do have logarithmic characters. The unipotent
shift lies in their kernel.

This reduction is pair-local and query-relative. It is not a global preferred congruence or aether.
It depends on the supplied common two-dimensional carrier and calibrated clock/ruler ordering
already required by the terminal pair formula. The metric alone has not been shown to supply that
carrier for arbitrary observer endpoints.

## 6. Complete all-instruments endpoint-state witness

The preregistered rational complete coframe has nonzero base shift, nonspherical screen entry, and
all four mixing entries. It is invertible with

\[
\det E=5,
\qquad
\det g=-25,
\qquad
g=E^T\operatorname{diag}(-1,1,1,1)E.
\]

All three rational endpoint differentials have rank two. Their complete pullbacks have negative
`h00`, negative determinant, positive terminal ratios, and unequal shifts. Exact removal controls
show that base shift, screen shear, mixing, and angular endpoint embedding each change at least one
pullback. Thus “all instruments” means channel sensitivity in these independently supplied endpoint
states, not physical selection of one history.

The three ambient image planes are pairwise distinct:

\[
\operatorname{rank}[J_A\ J_B]
=\operatorname{rank}[J_B\ J_C]
=\operatorname{rank}[J_A\ J_C]=4.
\]

Consequently this finite witness is **not** a realized common-event transition, and no `2x2` map
satisfies `J_BD=J_A`. It verifies endpoint-metric and calibration algebra only. The exact endpoint
invariants `rho_i=exp(4 Phi_i)` are stored in `DERIVATION_RESULT.json`. Their ratios obey

\[
\rho_{CB}\rho_{BA}=\rho_{CA},
\qquad
\rho_{AB}\rho_{BA}=1.
\]

Production passes 65/65 exact checks. A separate stdlib/Fraction implementation passes 40/40; its
triangular transition reconstruction is numerical, while its metric, rank, sensitivity, and source
checks use exact rational arithmetic.

## 7. Relation to G140

G140 assigned one unoriented terminal scalar directly to each independently supplied affine strip.
Those edge magnitudes were not constructed as differences of compatible endpoint potentials; no
sign assignment could repair them. G141 does not overturn that result. It identifies the correct
ordered object: a relative endpoint calibration transition. Networks generated from endpoint
potentials close identically, while arbitrary independent pair magnitudes need not belong to one
physical congruent family.

## 8. Scope ceiling

G141 derives the algebraic inverse, sign, and composition of a **constructed calibration depth
within a supplied compatible regular calibrated endpoint family on one shared pair carrier**. It
does not establish that this depth is the physical observer-pair depth. Physical inverse/query
ownership remains `OPEN`, as do derivation of the carrier and family, a universal observer
incidence relation or full chart transition, metric-history selection, singular/null strata,
`X_max`, proper length, light/EM, action, source, bootstrap, matter, mass, observations, and
dynamics.
