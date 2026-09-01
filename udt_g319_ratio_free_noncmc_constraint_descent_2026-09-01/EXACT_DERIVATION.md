# G319 exact derivation — ratio-free non-CMC constraint descent

Date: 2026-09-01  
Grade: `EXTERNALLY_ACCEPTED_BOUNDED`

## Bounded landing

```text
RATIO_FREE_REGULAR_STRATUM_HAS_EXACT_QUADRATURE_AND_ARBITRARY_POSITIVE_PERIODIC_PSI__B_ZERO_REMAINS_A_COMPATIBILITY_STRATUM__G318_POWER_OBSTRUCTIONS_ARE_ANSATZ_SCOPED__NO_PHYSICAL_DATA_SELECTION
```

This is a theorem only inside the chosen flat marked-`T^3`, diagonal-TT, one-coordinate,
sign-definite diagnostic slice registered in `PREREGISTRATION.md`. It is not a classification of
the full non-CMC constraint surface and not a physical-history theorem.

## 1. Registered conformal data

Use

\[
\bar\gamma_{ij}=\delta_{ij},\qquad \psi=\psi(x)>0,
\]

and

\[
\bar A_{TT}+\bar L W
=\operatorname{diag}\!\left(\frac{2v}{3},-\frac v3+d,-\frac v3-d\right).
\]

The exact vacuum constraints inherited conditionally from G315--G316 are

\[
v'=\psi^6\tau'
\tag{1}
\]

and

\[
-8\psi''-\left(\frac23v^2+2d^2\right)\psi^{-7}
+\left(\frac23\tau^2-2\Lambda\right)\psi^5=0.
\tag{2}
\]

G318 imposed the extra constant-ratio ansatz
\(v=k\psi^6\tau\). G319 removes that assumption. The seed, torus, diagonal form, one-coordinate
dependence, positivity, and sign choice remain chosen diagnostic restrictions.

## 2. Ratio-free variables

Define

\[
\lambda=v\psi^{-6},\qquad
A=\tau+\lambda,\qquad B=\tau-\lambda,
\qquad H=\frac{\psi'}{\psi}.
\]

Equation (1) gives

\[
\lambda'=\tau'-6H\lambda,
\]

so

\[
\boxed{B'=3H(A-B).}
\tag{3}
\]

Multiplying (2) by \(3\psi^{-5}/2\) and using
\(v^2\psi^{-12}=\lambda^2\) gives

\[
\tau^2-\lambda^2
=12\psi''\psi^{-5}+3d^2\psi^{-12}+3\Lambda.
\]

Therefore

\[
\boxed{AB=F[\psi]},
\qquad
F[\psi]=12\psi''\psi^{-5}+3d^2\psi^{-12}+3\Lambda.
\tag{4}
\]

No division has occurred.

## 3. Exact first integral

Multiplying (3) by \(2B\) and using (4),

\[
(B^2)'=6H(F-B^2).
\]

Thus

\[
(\psi^6B^2)'
=72\psi'\psi''+18d^2\psi^{-7}\psi'+18\Lambda\psi^5\psi'.
\]

Every solution therefore obeys

\[
\boxed{
J_0=\psi^6B^2-36(\psi')^2+3d^2\psi^{-6}-3\Lambda\psi^6,
}
\tag{5}
\]

where \(J_0\) is constant on the connected coordinate circle. Production verifies the derivative
of (5) exactly on 87,586 rational constraint jets. An implementation-distinct Christoffel and
physical-constraint calculation verifies the same result on 35,059 rational checks.

## 4. Nowhere-zero regular stratum

Solving (5) gives

\[
B^2=\psi^{-6}Z,
\]

with

\[
Z=36(\psi')^2-3d^2\psi^{-6}+3\Lambda\psi^6+J_0.
\]

On a connected component with \(B\ne0\), choose a fixed sign \(\epsilon=\pm1\):

\[
B=\epsilon\psi^{-3}\sqrt Z,
\qquad
A=\frac{F}{B}.
\tag{6}
\]

Then

\[
\tau=\frac{A+B}{2},\qquad
\lambda=\frac{A-B}{2},\qquad
v=\psi^6\lambda.
\tag{7}
\]

The physical mixed extrinsic-curvature eigenvalues are

\[
K^x{}_x=\frac{\tau+2\lambda}{3},
\]

\[
K^y{}_y=\frac{\tau-\lambda}{3}+d\psi^{-6},
\qquad
K^z{}_z=\frac{\tau-\lambda}{3}-d\psi^{-6}.
\tag{8}
\]

Direct substitution of (6)--(8) into the physical Hamiltonian and momentum constraints returns
zero. The independent verifier rebuilds the spatial Christoffels and Ricci scalar by index loops;
it does not import production functions or read the production output.

Finally, periodic descent into the registered TT-plus-longitudinal chart is

\[
\alpha=\frac23\langle v\rangle,
\qquad
w'=\frac12\bigl(v-\langle v\rangle\bigr).
\tag{9}
\]

The right side has zero mean, so a periodic \(w\) exists up to its translation kernel.

## 5. Arbitrary-positive-profile theorem

Let \(\psi\) be any smooth positive periodic function, and fix finite real \(d\) and \(\Lambda\).
On the compact coordinate circle, define

\[
G=36(\psi')^2-3d^2\psi^{-6}+3\Lambda\psi^6.
\]

Both \(-G\) and \(-G-\psi^6F\) are bounded. Choose

\[
J_0>sup_x\max\{-G(x),-G(x)-\psi(x)^6F(x)\}.
\tag{10}
\]

Then

\[
Z=G+J_0>0
\]

and

\[
B^2+F=\psi^{-6}\bigl(Z+\psi^6F\bigr)>0.
\]

Because

\[
\tau=\frac{B^2+F}{2B},
\]

the choice \(\epsilon=+1\) in (6) produces \(\tau>0\), while \(\epsilon=-1\) produces
\(\tau<0\). All reconstructed quantities are smooth and periodic.

Hence, in this registered regular stratum, the constraints admit **every** smooth positive
periodic \(\psi\) after a sufficiently large free constraint constant \(J_0\) is supplied. This is
an exact compactness argument, not a curve fit. The eight explicit Fourier controls in
`PROFILE_ATLAS.tsv` are only replay witnesses; they are not the proof of the universal statement.

The theorem says that these constraints do not select \(\psi\) inside this diagnostic slice. It
does not say that arbitrary constraint data are physical histories, that the evolution is
underdetermined, or that other slices cannot impose additional restrictions.

## 6. The zero/crossing stratum

Equation (5) remains valid when \(B=0\), but equation (6) does not. At a zero,

\[
\boxed{F=0}
\tag{11}
\]

is required by (4), while (3) still gives

\[
\boxed{B'=3HA.}
\tag{12}
\]

Thus a zero need not be stationary. Smooth sign-gluing depends on the vanishing order of the
radicand and compatible data for \(A\). G319 verifies 324 exact compatible zero-stratum germs, but
does not claim a global parameterization of every crossing. The correct grade is
`COMPATIBILITY_GLUE_STRATUM_NOT_GLOBALLY_PARAMETERIZED`.

## 7. What survives from G318

For the G318 ansatz

\[
\tau=C\psi^n,
\qquad
\lambda=\frac{n}{n+6}\tau,
\]

one has

\[
A=\frac{2(n+3)}{n+6}\tau,
\qquad
B=\frac6{n+6}\tau.
\]

Equation (4) then reproduces exactly the G318 scalar ODE, and (5) is constant along every G318
solution. Therefore:

- the G318 power-law interlock remains an exact theorem **under its constant-ratio ansatz**;
- the G318 \(n\le-3\) periodic obstruction remains valid **inside that ansatz**;
- the G318 positive periodic tidal family remains an embedded subfamily;
- none of those ansatz-specific restrictions applies to the broader ratio-free family.

This is a scope correction, not a refutation or deletion of G318.

## 8. Physical and premise status

- `DERIVED_CONDITIONAL`: equations (3)--(5) from the active bounded equation and chosen conformal
  chart.
- `DERIVED_CONDITIONAL`: regular reconstruction (6)--(9).
- `DERIVED_CONDITIONAL_IN_REGISTERED_SLICE`: arbitrary-positive-profile theorem (10).
- `OPEN`: global classification of the \(B=0\) crossing stratum.
- `CHOSE_BOUNDED_DIAGNOSTIC_SLICE`: flat marked torus, diagonal TT seed, one-coordinate dependence,
  positive \(psi\), sign-definite \(tau\).
- `OPEN_NOT_SELECTED`: physical initial data, complete history, topology, population, scale,
  observations, matter/mass, source, and physical \(X_{\max}\).

The UDT metric, completed-pair pullback, and reciprocal kernel are unchanged. G319 classifies a
conditional initial-data construction after the active response equation has already been adopted.
