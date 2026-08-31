# G308 exact derivation — coherence fixes a global sector, not its handedness

Date: 2026-08-31
Grade: `EXTERNALLY_REVIEWED__REPAIRS_INTERNAL_PASS__FOLLOWUP_PENDING`

## Bounded landing

```text
BOTH_G307_CHIRAL_MEMBERS_EXTEND_GLOBALLY_AND_CAUSALLY_ON_G305
__CONNECTED_REGULAR_CARRY_FORBIDS_LOCAL_CHIRALITY_SWITCHING
__TRANSVERSE_ORIENTATION_REVERSING_ISOMETRY_EXCHANGES_THE_TWO_SECTORS
__METRIC_ONLY_PHYSICAL_SELECTION_REMAINS_OPEN
```

This is preregistered candidate B. “Causally” means that both fields live smoothly on the same
causal G305 spacetime and leave its metric and light cones unchanged. It does not mean that Hopf
fibers are signals or four-dimensional causal trajectories.

## 1. Exact arena

The positive G305 standard completion is

\[
g=-dT^2+a(T)^2\gamma_1,
\qquad
a(T)=X\cosh(T/X)>0,
\]

on \(\mathbb R_T\times S^3\), where \(\gamma_1\) is the unit-round metric. For one supplied regular
directed germ \((p,v)\), G307 reconstructs one orthogonal complex structure in each G306 chirality.
Choose an oriented screen \((w,z)\) so \((p,v,w,z)\) is positively oriented. The two structures are

\[
J_+
=v\otimes p-p\otimes v+z\otimes w-w\otimes z,
\]

\[
J_-
=v\otimes p-p\otimes v-z\otimes w+w\otimes z.
\]

They agree on the route plane and act oppositely on the screen:

\[
J_\pm p=v,
\quad J_\pm v=-p,
\quad J_+w=z,
\quad J_-w=-z.
\]

## 2. Both candidates are global

For every \(q\in S^3\subset\mathbb R^4\), define

\[
K_\pm(q)=J_\pm q.
\]

Since \(J_\pm^T=-J_\pm\) and \(J_\pm^2=-I\),

\[
q\cdot K_\pm(q)=0,
\qquad
|K_\pm(q)|=1.
\]

Thus both are smooth, nowhere-zero global tangent fields. On a radius-\(a\) slice their unit fields
are \(V_\pm=K_\pm/a\), and their spatial integral curves are the complete closed circles

\[
q(s)=\cos(s/a)q(0)+\sin(s/a)J_\pm q(0),
\]

of period \(2\pi a\). Global existence therefore rejects neither chirality.

## 3. Exact time carry and its limit

For a time-independent lifted spatial field \(K\) on a warped product,

\[
\nabla_{\partial_T}K=\frac{a'}aK.
\]

Consequently,

\[
\boxed{
\nabla_{\partial_T}\left(\frac Ka\right)=0.
}
\]

Both normalized fields carry smoothly through every finite G305 time. This is kinematic carry on a
supplied metric, not a field equation or physical evolution law.

Spatially, each Hopf fiber is geodesic within its round slice. It is not automatically a
four-dimensional spacetime geodesic: the warped-product connection gives

\[
\nabla^{(4)}_{V_\pm}V_\pm
=\frac{a'}a\,\partial_T,
\]

which vanishes only where \(a'=0\). G308 therefore does not reinterpret the spatial fibers as
signals or observer worldlines.

## 4. A global mirror fixes the route and exchanges the candidates

Define the orthogonal reflection

\[
S
=p\otimes p+v\otimes v+w\otimes w-z\otimes z.
\]

Then

\[
S^2=I,
\qquad
\det S=-1,
\]

\[
Sp=p,
\quad Sv=v,
\quad Sw=w,
\quad Sz=-z,
\]

and exactly

\[
\boxed{SJ_+S^{-1}=J_-.}
\]

The map

\[
\mathcal P:(T,q)\mapsto(T,Sq)
\]

is a global isometry of the entire G305 warped product for every positive \(a(T)\). It fixes the
supplied directed route plane, preserves the unoriented screen plane, reverses its orientation,
and pushes the \(+\) field to the \(-\) field. Therefore the two candidates lie in one orbit of the
full orientation-forgetting metric isometry group.

This does not erase G307's signed-screen discriminator. If a signed transverse screen is retained
as marked query data, \(\mathcal P\) is not query-preserving because it reverses that sign.

## 5. Why orientation-preserving coherence leaves two sectors

For a skew \(4\times4\) complex structure, let \(\operatorname{Pf}(J)=\pm1\) be its Pfaffian sign.
Under an orthogonal change of frame \(R\),

\[
\operatorname{Pf}(RJR^T)
=\det(R)\operatorname{Pf}(J).
\]

The two G307 candidates have opposite Pfaffian signs. Hence an `SO(4)` transformation preserves
chirality and cannot exchange them, while a determinant-minus-one transformation does exchange
them. With a supplied global orientation there are two distinguishable but symmetry-degenerate
sectors. With orientation forgotten there is one mirror-equivalence class. Neither statement
prefers a physical sign.

## 6. What connected coherence really adds

The chirality sign is a continuous map from the regular orthogonal-complex-structure arena to the
discrete set \(\{+1,-1\}\). It is therefore constant on every connected smooth regular family.
A direct interpolation between the two G307 representatives confirms the obstruction: at its
midpoint the screen action vanishes, the determinant is zero, and \(J^2=-I\) fails.

Thus a coherent regular spacetime cannot choose left in one region and right in another without
leaving the G306/G307 stratum through degeneracy, discontinuity, a boundary, singularity, or
topology change. Coherence reduces arbitrary local binary assignments to one global binary sector;
it does not select which sector.

## 7. Pair reversal does not choose chirality

Reversing the ordered germ sends \(v\mapsto-v\) and reconstructs \(J\mapsto-J\). In four real
dimensions,

\[
\operatorname{Pf}(-J)=\operatorname{Pf}(J).
\]

Equivalently, \(V\mapsto-V\) reverses fiber orientation while
\(\alpha\wedge d\alpha\) retains its sign. Pair reversal therefore remains inside the same
chirality component.

## 8. Causal and metric equivalence

For any tangent vector \((u,Y)\),

\[
g((u,Y),(u,Y))=-u^2+a(T)^2\gamma_1(Y,Y).
\]

Because \(S\) is orthogonal, this quadratic form is unchanged by \((u,Y)\mapsto(u,SY)\). Timelike,
null, and spacelike classes and every metric curvature invariant are identical. Orientation-even
field invariants also agree. Signed helicity distinguishes the two only after orientation is
supplied; it labels a sector but does not select one.

## 9. Ownership conclusion

Additional supplied germs can test whether a proposed network belongs to one single global Hopf
member. A mismatched set is rejected as incoherent. But every coherent `+` network has a mirrored
coherent `-` network unless signed transverse orientation is independently retained. The current
metric therefore supplies a consistency test, not a physical population or parity law.

No metric or reciprocal-kernel term changed. Physical query/route/screen population, parity-
sensitive dynamics, stability, matter, mass, scale, observation, history, and physical `X_max`
remain open.

## 10. Evidence

- preregistered and pushed at `aaea5c12` before any executable or outcome;
- 11,526 exact rational production assertions over 36 directed frames, 216 global points, both
  chiralities, five scale/rate controls, pair reversal, and the conjugating reflection;
- 79,200 non-importing constructive randomized cross-checks over 1,200 random oriented frames,
  maximum normalized error `2.020605904817785e-14`;
- 121,600 method-distinct Hodge/group-orbit checks over 1,600 random `SO(4)` frames, maximum error
  `1.7763568394002505e-15`, with no production import and no outer-product candidate construction;
- eight direct mathematical and fourteen semantic hostile mutations caught;
- current premise verifier and the 199-test repository regression passed after the result;
- fresh external review found no bounded scientific defect, one sealed-path portability defect,
  and one evidence-independence caveat; R1--R4 now pass internally and await repair-only follow-up.
