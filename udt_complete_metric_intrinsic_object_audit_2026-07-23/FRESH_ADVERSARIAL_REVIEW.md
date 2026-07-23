PASS-WITH-CAVEATS

1. The local theorem is correct. For nonzero, nonnull \(\alpha=d\phi\),

\[
P=\frac{\alpha^\sharp\otimes\alpha}{g^{-1}(\alpha,\alpha)}
\]

satisfies \(P^2=P\) and has rank one. The induced map on two-forms is a real rank-three projector:

\[
\Lambda^2T^*=(L^*\wedge L^\perp{}^*)\oplus\Lambda^2L^\perp{}^*,
\qquad
\Pi=(1,0)
\]

on these two three-dimensional summands. Exact timelike and spacelike recomputations both passed.

2. With signature \((-+++)\) and \(\epsilon_{0123}=+1\),

\[
*E_i=-B_i,\qquad *B_i=E_i,\qquad *^2=-I,\qquad *^{-1}=-*.
\]

Consequently

\[
*\Pi*^{-1}=I-\Pi
\]

for both timelike and spacelike \(d\phi\). Reversing orientation sends \(*\mapsto-*\) and leaves the conjugation identity unchanged. An ordinary global Hodge star nevertheless requires orientation; nonorientable completions require the orientation-line-valued formulation.

3. The defined operator

\[
D=e^\phi\Pi+e^{-\phi}(I-\Pi)
\]

is real and tensorial. Under \(g\mapsto\Omega^2g\), \(\alpha^\sharp\mapsto\Omega^{-2}\alpha^\sharp\) and \(g^{-1}(\alpha,\alpha)\mapsto\Omega^{-2}g^{-1}(\alpha,\alpha)\), so \(P,\Pi,D\) are CSN invariant with the registered CSN-neutral reciprocal depth \(\phi\). Exactly,

\[
D^{-1}=e^{-\phi}\Pi+e^\phi(I-\Pi),\qquad
*D*^{-1}=D^{-1}.
\]

However, assigning \(e^\phi\) specifically to the \(\Pi\) sector rather than its complement is one of two inverse compatible solderings. It is not selected as physical ownership.

4. At nonzero null \(d\phi\), \(N=\alpha^\sharp\otimes\alpha\) has rank one and \(N^2=0\). Its induced two-form derivation is nonzero, rank two, and also squares to zero. Thus the normalized semisimple \(3+3\) projector has no continuation through the null stratum. At \(d\phi=0\), neither the line nor the projector exists. Causal-type change therefore obstructs a smooth global semisimple split unless the selected branch excludes null and zero strata. The null line and flag remain intrinsic local data, but not a reciprocal eigensplitting.

5. The metric-only commutant result is correct only with its exact qualification: for the connected orientation-preserving Lorentz algebra/group,

\[
\operatorname{End}_{SO^+(1,3)}(\Lambda^2_{\mathbb R})=\operatorname{span}_{\mathbb R}\{I,*\}.
\]

For the full orientation-reversing Lorentz group, \(*\) is not equivariant and the commutant reduces to scalar \(I\). After complexification, \(i*\) has rank-three chiral eigenspaces, but conjugation exchanges them; unequal reciprocal weights therefore fail real descent.

6. No overlooked native Hopf object was found. The nonnull-\(d\phi\) split gives a local reduction and, on a timelike stratum, an \(S^2\) direction fiber—not a selected section or \(S^2\)-valued map. Primary characteristic classes classify supplied bundles, not a Hopf secondary invariant. The only exact Hopf bundle datum remains the conditional toric \(|c_1|=1\) result with periods, circle action, caps, orientation, quotient, and normalization supplied.

7. Read-only reruns reproduced:

- 33/33 production checks;
- 24/24 standard-library checks;
- 58 manifest entries, all hashes valid;
- 30 unique census rows;
- 20/20 declared mutations caught;
- raw frozen counts \(5{,}376+768=6{,}144\);
- zero bivector-eigenplane rows;
- twelve completion rows;
- repository baseline: 70 passed, 1 xfailed.

8. Required corrections before banking the package:

- Qualify every unqualified “Lorentz commutant is \(I,*\)” statement as connected, orientation-preserving Lorentz symmetry.
- State explicitly that \(D\) versus \(D^{-1}\) is compatible reciprocal soldering, not physically selected ownership.
- Add the instrument-atlas source supporting the claimed \(d\phi\) census \(3072/2304/768\) to the 58-source manifest and verifier, or remove that census from the report. The present scripts do not derive or verify it.
- Scope the standard-library verifier correctly: it independently recomputes the local linear algebra, but merely hash-checks/hard-codes the frozen \(6{,}144\)-row and twelve-family claims.
- Replace or supplement the payload-only mutation catches with operator-level mutations covering projector normalization, Hodge exchange, CSN scaling, complex real descent, and null two-form nilpotence.
- Add the induced null two-form nilpotence/rank-two check and an explicit full-\(D\) CSN check.

Optional future extension: test whether any selected complete branch keeps \(d\phi\) everywhere nonzero and nonnull and supplies a global section or toric join. This is not required to validate the scoped local theorem.