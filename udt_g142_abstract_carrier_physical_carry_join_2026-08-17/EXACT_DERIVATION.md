# G142 exact derivation — founded model carrier, query-supplied physical carry

## 1. Four objects that must not be collapsed

The founding comparison uses a dimension-matched ordered clock/ruler model space

\[
W\cong\mathbb R^2,
\qquad
q=(c_Edt,dr)^T,
\qquad
K=\begin{pmatrix}0&1\\1&0\end{pmatrix}.
\]

This representation space and its ordered channel labels are supplied/chosen in the founding
setup; they are not derived as a physical tangent carrier. `c_E` is the observed
unit conversion, `K` is the posited dual pairing, and Reciprocity plus regular composition derive

\[
D(\delta)=\operatorname{diag}(e^{-\delta},e^{+\delta})
\]

after ordered depth `delta` has been supplied.

That abstract carrier is not yet any observer's physical tangent plane. A complete comparison uses
four distinct types:

1. `W`: the founded model clock/ruler carrier;
2. `V_i`: the calibrated pair-coordinate carrier at endpoint `i`;
3. `R_i:V_i->W`: the terminal positive-diagonal triangular calibration factor derived from the
   supplied complete pair metric in its ordered calibrated coordinates;
4. `M_BA:V_A->V_B`: the flag-preserving carry belonging to the supplied observer relation.

The pair-first theorem supplies `V_i` conditionally from a supplied regular pair realization. It
does not make `V_i`, its soldering, or `M_BA` follow from bare endpoints or co-presence.

## 2. The fully typed total transition

The model-space comparison from A to B is

\[
\boxed{C_{BA}=R_BM_{BA}R_A^{-1}:W\to W.}
\]

For three observers, if the supplied carries compose,

\[
M_{CB}M_{BA}=M_{CA},
\]

then

\[
C_{CB}C_{BA}
=R_CM_{CB}R_B^{-1}R_BM_{BA}R_A^{-1}
=C_{CA}.
\]

For an independently supplied direct carry `M_CA`, the converse obstruction is exact:

\[
R_C^{-1}(C_{CB}C_{BA}-C_{CA})R_A
=M_{CB}M_{BA}-M_{CA}.
\]

Thus total-transition closure is equivalent to carry closure, not an independent selector. With
`M_AB=M_BA^-1`, one also has `C_AB=C_BA^-1`.

## 3. Endpoint gauge covariance

Let independent endpoint carrier gauges `P_i` preserve the positive-diagonal triangular flag:

\[
R_i'=R_iP_i,
\qquad
M_{BA}'=P_B^{-1}M_{BA}P_A.
\]

Then

\[
C_{BA}'
=R_BP_BP_B^{-1}M_{BA}P_A(R_AP_A)^{-1}
=C_{BA}.
\]

This repairs the G141 gauge boundary. The endpoint factors and `Phi_i` values are presentation
dependent, but the total carried comparison is invariant when the carry transforms with them. In
particular,

\[
\chi(M_{BA}')=\chi(M_{BA})+\chi(P_A)-\chi(P_B),
\]

so carry neutrality is not preserved by arbitrary independent endpoint gauges. Its presentation
shift cancels the corresponding endpoint shifts inside `chi(C_BA)`.

## 4. Reciprocal grading

For a positive-diagonal upper-triangular matrix `A`, define

\[
\chi(A)=\frac12\log\frac{A_{11}}{A_{00}}.
\]

This is a character of `B^+(2)`. Since

\[
\Phi_i=\frac12\log\frac{(R_i)_{11}}{(R_i)_{00}},
\]

the total depth is

\[
\boxed{
\chi(C_{BA})
=\Phi_B-\Phi_A+\chi(M_{BA}).
}
\]

It composes and reverses exactly. The determinant character remains separate and carries the common
scale contribution.

This formula does not bolt path physics onto an endpoint law. It states that endpoint factors and
carrier carry are gauge-dependent pieces of one total comparison. Only the total is invariant.

## 5. Exact scalar relation to G141 in a fixed matched presentation

G141 used identity carry. In a fixed matched `B^+(2)` presentation, its scalar grading equation is
recovered on the broader locus

\[
\chi(M_{BA})=0
\quad\Longrightarrow\quad
\chi(C_{BA})=\Phi_B-\Phi_A.
\]

Identity carry is necessary to recover G141's entire transition `C_BA=R_BR_A^{-1}`. It is not
necessary merely to recover G141's scalar grading equation. A nonidentity carry

\[
M_{BA}=\begin{pmatrix}s&n\\0&s\end{pmatrix},
\qquad s>0,
\]

may retain common scale and unipotent shift while being reciprocal-neutral in that fixed matched
presentation. Therefore G141's endpoint-difference scalar law is compatible with a nonempty
transport sector; this is not a gauge-invariant physical classification of carries.

If `chi(M_BA)` is nonzero, the endpoint difference alone is not the total ordered depth. Moving
reciprocal grading between `R_i` and `M_BA` is a presentation choice; `chi(C_BA)` is unchanged.

## 6. What the founding and co-presence own

The source entailment is sharp:

- the founding supplies/chooses the abstract two-channel representation and ordered labels, uses
  observed `c_E` calibration and posits `K`; only the reciprocal character on supplied depth is
  derived;
- a supplied calibrated pair realization owns its local pair carrier and complete pullback;
- a supplied composable observer relation owns its carry;
- co-presence says events belong to one supplied complete solution;
- neither abstract carrier nor co-presence constructs endpoint solderings, event pairing, or
  numerical carry.

The word “observer query” therefore should not be asked to mean a universe selector. An experiment
may legitimately supply which observers and comparison protocol are used, just as coordinates do
not have to be selected by a field equation. But if UDT claims one unique depth from bare endpoints,
then a physical carry rule is still missing. The current metric evaluates a typed supplied relation;
it does not make all such relations identical.

## 7. Exact nonselection countermodel

Take the same endpoint factors and co-present metric data,

\[
R_A=R_B=I.
\]

Two flag-preserving carries are

\[
M^{(0)}=I,
\qquad
M^{(1)}=\operatorname{diag}(1/2,2).
\]

They give

\[
\chi(C^{(0)})=0,
\qquad
\chi(C^{(1)})=\log2.
\]

Both lie in the supplied flag-preserving `B^+(2)` comparison arena. Co-presence and endpoint metrics
are unchanged. This is a formal underdetermination witness, not evidence that both are physically
realized carries. Together with G130's independent ownership result, it shows that those premises
do not select the physical carry or its grading.

## 8. Maximum conclusion

The apparent “missing shared carrier” splits cleanly. An abstract reciprocal two-channel
representation was already supplied in the founding. The physical endpoint soldering and carry belong to the typed observer
relation. Once supplied, the total transition is gauge invariant and compositional, and G141 is its
identity-carry transition; in a fixed matched presentation its scalar grading also survives the
broader reciprocal-neutral-carry locus.

No physical restriction to `B^+(2)` is derived here. This does not derive a unique physical query,
carry, pair family, metric history, or `X_max`. It
does remove the false demand for another scalar formula and identifies the exact invariant that any
future physical or operational query semantics must supply.
