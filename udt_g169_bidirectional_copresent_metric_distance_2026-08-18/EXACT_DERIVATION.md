# G169 exact derivation — conditional two-ended reversal quotient

Date: 2026-08-18

## 1. Type the supplied relation before naming any distance

Let a supplied oriented physical pair relation be denoted by

\[
\mathcal R_{AB}
=
\bigl(\mathcal P_{A\to B},\mathcal P_{B\to A},C_{BA}\bigr),
\]

where each endpoint object \(\mathcal P\) contains its calibrated clock/separation germ and
metric-derived G168/G167 pullback, while \(C_{BA}\) denotes any genuinely arrow-valued endpoint
identification required by the declared relation. This notation does not assert that the current
founding record derives those data.

Define reversal on supplied typed relations by

\[
\tau\mathcal R_{AB}
=
\mathcal R_{BA}
=
\bigl(\mathcal P_{B\to A},\mathcal P_{A\to B},C_{BA}^{-1}\bigr).
\]

Then \(\tau^2=1\). The unoriented reversal quotient of the supplied relation is

\[
\boxed{
\mathfrak Q(A,B)
=
[\mathcal R_{AB}]_{\tau}
=
\{\mathcal R_{AB},\mathcal R_{BA}\}.
}
\]

It is symmetric by construction:

\[
\mathfrak Q(A,B)=\mathfrak Q(B,A).
\]

This is a quotient of supplied relation data. It is not currently a physical UDT distance, because
the existing founding semantics do not supply the relation being quotiented.

Under endpoint reparameterizations \(P_A,P_B\), a carry transforms as

\[
C_{BA}\mapsto C'_{BA}=P_B^{-1}C_{BA}P_A.
\]

The reversed carry transforms as

\[
P_A^{-1}C_{BA}^{-1}P_B=(C'_{BA})^{-1}.
\]

Therefore reversal commutes with the endpoint gauge action. The orbit is well typed on the quotient
once a two-ended relation and its allowed endpoint gauges are supplied.

## 2. What the metric derives at each endpoint

For a supplied endpoint germ \((u_A,s_{AB})\), G168 derives

\[
r_{AB}
=
s_{AB}
-\frac{g(u_A,s_{AB})}{g(u_A,u_A)}u_A,
\]

the Lorentzian plane

\[
E_{AB}=\operatorname{span}(u_A,r_{AB}),
\]

its positive screen, and the G167 pullback

\[
h_{AB}=J_{AB}^{T}g_AJ_{AB}.
\]

The same construction applies independently at B after \((u_B,s_{BA})\) is supplied. The metric
does not map \((u_A,s_{AB})\) into \((u_B,s_{BA})\). Full reversal changes tangent fibers, exactly as
G168 records.

Thus the metric is the evaluator of both ends; the current source record does not prove that one end
or two bare observer labels own the other end.

## 3. Founded reciprocal reversal is exact

On the pure founded branch,

\[
h(\delta)=
\begin{pmatrix}
-e^{-2\delta}&0\\
0&e^{2\delta}
\end{pmatrix}.
\]

The inverse orientation of the **same supplied reciprocal relation** has

\[
h(-\delta)=
\begin{pmatrix}
-e^{2\delta}&0\\
0&e^{-2\delta}
\end{pmatrix}.
\]

The exact endpoint identification

\[
K_\delta=\operatorname{diag}(e^{2\delta},e^{-2\delta})
\]

satisfies

\[
K_\delta^Th(\delta)K_\delta=h(-\delta),
\qquad
K_{-\delta}=K_\delta^{-1}.
\]

Consequently

\[
\boxed{
\delta_{BA}=-\delta_{AB},\qquad
q_{BA}=q_{AB}^{-1},\qquad
\chi_{BA}=-\chi_{AB}.
}
\]

This is derived on one supplied reciprocal relation. It is not a theorem that two independently
evaluated endpoint germs automatically realize this inverse pair.

## 4. Ordinary geometric reversal is not reciprocal inversion

Use G168's exact flat same-boundary family

\[
F_a(\tau,\sigma)
=
(\tau,\sigma,a\sigma(1-\sigma),0).
\]

At A, its separation tangent is \((0,1,a,0)\). At B, reversing the surface orientation gives
the reverse-directed tangent \((0,-1,a,0)\). Both have the same norm. The endpoint pullbacks are

\[
h_A=h_B^{\rm reversed}
=
\operatorname{diag}(-1,1+a^2).
\]

Therefore both terminal readouts are

\[
\phi_A=\phi_B^{\rm reversed}
=
\frac14\log(1+a^2).
\]

For \(a=1\), both equal \(\tfrac14\log2\), whereas reciprocal inversion would require the second
to equal \(-\tfrac14\log2\). Equivalently, both squared ratios are \(q^2=1/2\); they are equal,
not reciprocal.

This proves:

\[
\boxed{
\text{surface reversal or endpoint exchange alone does not generate UDT Reciprocity.}
}
\]

The two endpoint evaluations must be typed as inverse orientations of one reciprocal relation.
That is an ontological/ownership statement with mathematical consequences, not a path selection.

## 5. Scalar shadows of the reversal quotient

Any odd scalar on oriented relations gives an even magnitude on the reversal orbit. In particular,

\[
|\delta_{BA}|=|\delta_{AB}|,
\qquad
|\chi_{BA}|=|\chi_{AB}|,
\qquad
\chi_{BA}^2=\chi_{AB}^2.
\]

These are symmetric scalar readouts. They are not established physical metric distances. In the
same flat family, \(a=0\) gives two distinct boundary observers with terminal \(\delta=0\). Thus
\(|\delta|\) and \(|\chi|\) fail identity of indiscernibles on the admitted local pair arena.
They are at most pseudoseparation readouts unless additional complete response data or a stronger
global theorem restores separation.

The full reversal orbit retains both complete endpoint responses and need not compress their
angular, shift, or screen data to one number. Reversal swaps those endpoint responses; this audit
does not invent an odd/even law for every orchestra channel.

## 6. Matched reciprocal chains compose; arbitrary triangles need not add

For a matched one-dimensional reciprocal chain,

\[
D(\delta_{BC})D(\delta_{AB})
=
D(\delta_{AB}+\delta_{BC}),
\]

so

\[
\delta_{AC}=\delta_{AB}+\delta_{BC},
\qquad
q_{AC}=q_{AB}q_{BC},
\]

and

\[
\chi_{AC}
=
\frac{\chi_{AB}+\chi_{BC}}
{1+\chi_{AB}\chi_{BC}}.
\]

The absolute signed depth obeys the ordinary triangle inequality on this matched additive chain:

\[
|\delta_{AC}|
\le |\delta_{AB}|+|\delta_{BC}|.
\]

But three individually regular pair metrics do not automatically form one matched chain. The exact
positive values

\[
q_{AB}=\frac12,
\qquad
q_{BC}=\frac13,
\qquad
q_{AC}=\frac15
\]

are individually admissible pair readouts, while matched composition would require

\[
q_{AC}=\frac16.
\]

At a non-collinear middle observer, the B-to-A and B-to-C germs also define different pair planes.
Demanding arbitrary scalar additivity would silently identify those calibrations and directions.

Therefore arbitrary-triangle additivity is neither derived nor required by the conditional reversal
quotient. It is a category error to impose a one-dimensional reciprocal-chain law on every observer
triangle. When a sequential comparison is physically requested, its middle-state carry must be
matched or supplied.

## 7. Complete carry is stronger than scalar agreement

For supplied typed carries,

\[
M_{CA}=M_{CB}M_{BA}
\]

gives exact inverse, associative, metric-pullback, and first-jet composition, as G156/G160 derive.
Reversal commutes with endpoint reparameterization, so a supplied complete relation has a lawful
quotient-independent inverse.

Scalar closure cannot replace complete closure. Let

\[
M_{BA}=M_{CB}=I,
\qquad
M_{CA}=
\begin{pmatrix}1&1\\0&1\end{pmatrix}.
\]

The direct/staged matrix triangle fails, yet both determinant/common-scale and diagonal reciprocal
characters see zero defect. The shear remains in their kernel.

Hence a supplied complete bidirectional response is mathematically richer than signed depth. This
supports retaining the conditional reversal quotient while preserving the open physical relation
and carry problem.

## 8. Coincidence is a boundary stratum

At coincidence, \(s_{AA}=0\) and the G168 pair plane drops from rank two to rank one. The scalar
identity \(\delta_{AA}=0\) remains meaningful, but the regular complete pair response does not
contain its own identity arrow. A full global relation category must adjoin or derive the degenerate
identity stratum. This audit does not perform that boundary completion.

## 9. Epistemic landing

The exact landing is

```text
CONDITIONAL_REVERSAL_QUOTIENT_ON_SUPPLIED_TWO_ENDED_RELATION
__NOT_YET_PHYSICAL_UDT_DISTANCE
__PURE_RECIPROCAL_SCALAR_REVERSAL_DERIVED
__MATCHED_CHAIN_COMPOSITION_DERIVED
__ARBITRARY_TRIANGLE_ADDITIVITY_NOT_REQUIRED_OR_DERIVED
__PHYSICAL_TWO_ENDED_GERM_AND_CARRY_OWNERSHIP_OPEN
```

The mathematical definition

\[
\mathfrak Q(A,B)=[\mathcal R_{AB}]_{\mathcal R\sim\mathcal R^{-1}}
\]

is consistent on supplied regular two-ended reciprocal relations. It does not derive that physical
distance is such an object, because it cannot supply the relation on which the quotient acts.

What is **not** derived is that the present founding word “co-presence” already supplies
\(\mathcal R_{AB}\), both endpoint germs, or their physical inverse carry. Without that additional
ownership statement, the quotient is a conditional representation theorem and not a UDT definition
of distance.
