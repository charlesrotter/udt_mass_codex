# G162 exact derivation

Date: 2026-08-18

## 1. Exact factorization

On the regular, oriented, future-clock pair stratum, write each calibrated pair metric as

\[
h_i=R_i^T\eta R_i,
\qquad
R_i=\begin{pmatrix}T_i&T_i\beta_i\\0&L_i\end{pmatrix},
\qquad T_i,L_i>0,
\]

with \(\eta=\operatorname{diag}(-1,1)\). Every compatible carry has the exact form

\[
M_{B\leftarrow A}=R_B^{-1}\Lambda_{BA}R_A,
\qquad \Lambda_{BA}\in SO^+(1,1).
\]

Indeed,

\[
M_{BA}^Th_BM_{BA}
=R_A^T\Lambda_{BA}^T\eta\Lambda_{BA}R_A
=h_A.
\]

Conversely, if a supplied \(M\) is compatible, define \(\Lambda=R_BMR_A^{-1}\). Then

\[
\Lambda^T\eta\Lambda
=R_A^{-T}M^Th_BMR_A^{-1}
=R_A^{-T}h_AR_A^{-1}
=\eta.
\]

Orientation and future-clock preservation put this factor in \(SO^+(1,1)\). The factorization is
therefore an equivalence on the declared stratum, not only a forward construction.

The endpoint-gauge-invariant joined transition is

\[
C_{BA}=R_BM_{BA}R_A^{-1}=\Lambda_{BA}.
\]

For three observers,

\[
M_{CB}M_{BA}=R_C^{-1}(\Lambda_{CB}\Lambda_{BA})R_A.
\]

Thus the route/frame channel composes in \(SO^+(1,1)\).

## 2. The exact endpoint section

Setting \(\Lambda_{BA}=I\) gives

\[
M^{\rm cal}_{BA}=R_B^{-1}R_A.
\]

It is metric-compatible and exactly composable:

\[
M^{\rm cal}_{CB}M^{\rm cal}_{BA}=R_C^{-1}R_A=M^{\rm cal}_{CA}.
\]

Its joined transition is identically \(I\). It therefore transports endpoint calibration, not an
independently supplied path or overlap. When \(h_A=h_B=\eta\), the endpoint section is \(I\), while
a genuine overlap may be any nonidentity \(\Lambda\in SO^+(1,1)\). Equal endpoint metrics cannot
reconstruct that overlap.

## 3. Why the scalar kernel forgets \(\Lambda\)

The complete pair metric and its first jet satisfy

\[
h_A=M_{BA}^Th_BM_{BA},
\qquad
\dot h_A=\frac{d}{d\lambda}(M_{BA}^Th_BM_{BA}).
\]

Every smooth \(\Lambda(\lambda)\) cancels in the first identity; differentiating the exact identity
also cancels \(\dot\Lambda\). Therefore all calibrated functions of \((h,\dot h)\) are independent
of residual tangent rapidity. In particular,

\[
T^2=-h_{00},\qquad
\beta=\frac{h_{01}}{h_{00}},\qquad
L^2=h_{11}-\frac{h_{01}^2}{h_{00}},
\]

\[
\kappa=\frac14\log(-\det h),
\qquad
\phi=\frac14\log\!\left(\frac{-\det h}{h_{00}^2}\right),
\]

and their first derivatives are \(\Lambda\)-independent.

The conditional reciprocal readout and working bounded position are consequently

\[
\frac{c_{\rm eff}}{c_E}=\frac{-h_{00}}{\sqrt{-\det h}}=e^{-2\phi},
\qquad
\chi=\tanh\phi,
\qquad
x=X_{\max}\chi,
\]

with the supplied status of \(X_{\max}\) unchanged. The metric volume-density coefficient and the
positive half-density coefficient are, respectively,

\[
\sqrt{-\det h}=TL,
\qquad
(-\det h)^{1/4}=\sqrt{TL}.
\]

Both are invariant. Because \(\det\Lambda=1\), the joined G156 character is

\[
\sigma_{BA}=\frac12\log|\det C_{BA}|=0.
\]

The distinct raw-carry grading is

\[
\frac12\log\det M_{BA}=\kappa_A-\kappa_B.
\]

Both are rapidity-independent; they must not be conflated.

## 4. What still remembers \(\Lambda\)

The joined transition and its rate are

\[
C=\Lambda,
\qquad
\Gamma=\dot C C^{-1}=\dot\Lambda\Lambda^{-1}.
\]

They remain nonzero for a live varying rapidity. A three-observer or loop defect compares
\(\Lambda_{CA}\) with \(\Lambda_{CB}\Lambda_{BA}\). The supplied rate
\(K_{BA}=\dot M_{BA}M_{BA}^{-1}\), finite defect \(F\), and defect rate \(K_F\) are likewise
route/frame objects. The split \(K=S_h(K)+A_h(K)\) is only a presentation split: \(A_h\) is
metric-skew and invisible to the pair first jet, while only the complete carried first jet is
covariant. Raw complete-coframe score components are also representative/gauge data, not path or
extrinsic observables.

Normal \(SO(2)\) holonomy, Jacobi transport, ambient transport, the second fundamental form, and
the conditional \(\mathcal C_{II}\) eigenflag live in different path, congruence, or extrinsic
bundles. They are not functions of tangent \(\Lambda\), and G162 does not collapse them into it.

## 5. Exact bounded conclusion

Residual tangent rapidity is not a missing input to the bounded scalar reciprocal kernel. It is a
separate route/frame-memory channel. The exact endpoint section is sufficient whenever only the
scalar quotient is requested, but it cannot be promoted to a physical path or overlap.

Nothing here selects the values or evolution of \(B,Q,S,Y,Z,\kappa\), a physical query, route,
carry, \(X_{\max}\), or global completion.
