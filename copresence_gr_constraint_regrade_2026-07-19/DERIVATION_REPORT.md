# Co-Presence Regrade of GR Constraints

## Result

`PRIOR_ALGEBRA_SURVIVES_CONSTRAINT_ROLES_RECLASSIFIED_NO_NATIVE_GR_CONSTRAINT_SELECTED`

Some earlier work needed to be reinterpreted, but none of its load-bearing exact algebra needed to be
discarded. The co-presence framework changes the order in which GR-style constraints may be judged:

> First derive or specify the complete whole-solution law. Then determine which equations appear as
> global admissibility, gauge identities, foliation projections, initial-data restrictions, boundary
> conditions, or material response conditions.

Co-presence does not select a native Hamiltonian constraint, momentum constraint, lapse, shift,
multiplier, field census, action, or bridge.

## 1. The word “constraint” was carrying too many meanings

The audit separates eighteen roles in `ROLE_TAXONOMY.tsv`. Only a subset are constraints. A soft
penalty, symmetry premise, spacetime-domain premise, field census, scaling selector, calibration
rule, selection map, existence witness, and parent-law dependency must not be forced into a
constraint category. Four constraint distinctions are especially important.

### Whole-solution admissibility

A rule

\[
\mathcal B[S]=0,
\qquad S=(M_S,g,\Phi,\ldots),
\]

can filter completed candidate universes. This is the natural current reading of bootstrap closure.
It does not enter the local Euler equations unless an additional variational rule says it does.

### Varied multiplier constraint

If instead

\[
I_{\rm aug}=I_0+\eta\mathcal B
\]

is varied with respect to all declared variables, the equations include `B=0` and a generally
nonzero normal reaction proportional to `eta delta B`. It can also change the finite-cell boundary
variation. This is a different theory-space choice from after-solution filtering.

### Restricted variation

Imposing `B=0` before varying restricts variations to the tangent space of the constraint surface.
It can reproduce a constrained tangent root while omitting the normal equation. Co-presence does not
make that restriction equivalent to unrestricted parent variation.

### Projection or identity

A Noether identity relates complete Euler equations because of a symmetry. A Hamiltonian- or
momentum-like constraint is instead a projection of a parent tensor equation relative to a chosen
foliation. Neither role supplies the missing parent UDT law.

## 2. The prior multiplier algebra survives exactly

For

\[
I_0=x^2+y^2,
\qquad C=x+y-1,
\]

unrestricted variation gives `(x,y)=(0,0)`, where `C=-1`. Varying

\[
I_0+\eta C
\]

gives

\[
(x,y,\eta)=\left(\frac12,\frac12,-1\right).
\]

Restricting first to `y=1-x` gives the same tangent coordinate `x=1/2`, but it is still not the
unrestricted metric-only problem. The reaction vector at the constrained root is `(-1,-1)`.

The aligned example retains `(1,2,0)`, proving only that a multiplier may be redundant at one root.
For finite positive penalty `alpha`, the exact residual remains

\[
C=-\frac{1}{\alpha+1}\ne0.
\]

Thus the earlier reactive/redundant and finite-penalty conclusions remain valid. Co-presence changes
their interpretation, not their algebra.

Hard substitution is separate again. Substituting `y=1-x` before variation restricts the variation
to the tangent of `C=0`; the prior `REFUTED_GENERICALLY` conclusion that this is unrestricted parent
variation remains unchanged. A finite penalty is instead a soft enforcement approximation and is
neither hard substitution nor a restricted variation domain.

## 3. A Noether identity is not a new constraint law

The finite gauge analogue

\[
I=(u-v)^2
\]

is invariant under a common shift of `u` and `v`. Its Euler derivatives obey

\[
E_u+E_v=0
\]

identically, while neither derivative vanishes identically by itself. This shows why a gauge/Noether
identity cannot choose metric-only versus auxiliary fields. It follows from the parent symmetry and
equations; it is not an independently imported physical restriction.

## 4. Hamiltonian and momentum constraints are conditional projections

The exact two-dimensional tensor counterexample captures the structural issue without adopting GR
dynamics. Let the background signature be `diag(-1,1)`, choose a boosted unit normal and tangent,

\[
n=(\cosh\zeta,\sinh\zeta),
\qquad
s=(\sinh\zeta,\cosh\zeta),
\]

and take the nonzero symmetric tensor

\[
E=\begin{pmatrix}0&0\\0&1\end{pmatrix}.
\]

Its normal-normal and normal-tangent projections are

\[
H(\zeta)=n^TEn=\sinh^2\zeta,
\qquad
M(\zeta)=n^TEs=\sinh\zeta\cosh\zeta.
\]

`H(0)=0`, even though the complete tensor is nonzero; for a boosted slicing `H` and `M` are nonzero.
Therefore one projected constraint can vanish in one foliation without representing a complete or
foliation-independent equation. Conversely, when the complete parent tensor `E` vanishes, every
projection vanishes in every slicing.

This yields the proper UDT ruling:

- a Hamiltonian-like projection is only a
  `PARENT_EQUATION_AND_FOLIATION_CONDITIONAL_COMPARISON` after a parent UDT tensor equation and
  slicing have been derived;
- the same holds for momentum constraints;
- neither may be imported separately as the native whole-solution law.

The toy does **not** prove that every zero-projection equation requires an already normalized
post-scale representative. Physical normalization of the normal, lapse, clocks, and charges may be
post-scale, while an analogous conformal projection can sometimes be stated pre-scale. Standard
ADM/EH constraints remain post-scale GR comparisons; the status of projections of a future native
UDT parent law is not decided in advance.

Positive CSN rescaling preserves the registered causal reachability relation, while physical
clock/ruler calibration remains open to representative selection and material transformation rules.

A projected equation is also not automatically an initial-data constraint. That stronger status
requires the parent differential equations, a decomposition showing the relevant highest normal
derivatives are absent, an admissible data class, and a propagation theorem.

In GR these projections have a precise parent theory. That GR fact is a comparison readout here, not
affirmative UDT physics.

## 5. Co-presence does not propagate constraints

Let `C(t)=u(t)-v(t)`. Under paired local histories

\[
u=u_0+at,
\qquad v=v_0+at,
\]

the constraint is constant. If `u_0=v_0`, it remains zero.

Under equally valid unpaired histories

\[
u=u_0+at,
\qquad v=v_0+bt,
\]

one instead has

\[
C(t)=u_0-v_0+(a-b)t.
\]

Zero initial `C` does not propagate unless the local law also gives `a=b`. Requiring `C(t)=0` for the
whole completed history imposes both `u_0=v_0` and `a=b`; that is a global admissibility filter on
histories. It does not derive which local equations produce or respond to those histories.

These two histories occupy the same co-present event domain but have different constraint
propagation laws. Likewise, the zero and nonzero tensors above occupy the same background geometry
but yield different projection equations. The pairs are explicit countermodels to the claim that
co-presence by itself selects a local or projected constraint law.

This distinction prevents a new mistake: co-presence may let UDT formulate a whole-history boundary
problem, but it cannot be described as a mechanism that moves constraints instantaneously between
events. Operational prediction still requires local or otherwise explicitly defined response laws,
data, coupling, and causal support.

## 6. A lapse-like multiplier is formal; shift remains uninstantiated

The generic canonical comparison

\[
L=p\dot q-N\mathcal H,
\qquad
\mathcal H=\frac12(p^2+q^2-1)
\]

gives `delta L/delta N=-H`. The multiplier also appears in the `q` and `p` equations. This is sound
constraint mathematics, but it does not prove that UDT fundamentally contains a lapse field, ADM
slicing, or a preferred time variable.

No shift-like canonical term was derived in this audit. Native shift ontology and its detailed
multiplier, gauge, or physical role therefore remain `OPEN`. If a future native covariant UDT law
admits a canonical decomposition, lapse and shift can then be classified from that law. Familiarity
with GR cannot make that decision in advance.

## 7. The finite-cell boundary problem remains unavoidable

For the exact boundary anchor

\[
L=\frac12(q')^2+\lambda q',
\]

the endpoint momentum is

\[
\frac{\partial L}{\partial q'}=q'+\lambda.
\]

Thus a multiplier changes the boundary variation even when it has no independently propagating
ontology. Co-presence strengthens the importance of global finite-cell consistency but does not
supply the boundary/corner action, allowed data, generator, reference, or normalized charge.
Spatial infinity and its GR charges remain rejected as native input.

## 8. Mechanical regrade of the earlier work

The 27-item thematic overlay is in `RECLASSIFICATION_TABLE.tsv` and `STATUS_LEDGER.tsv`. It is not a
replacement for frozen scientific statuses. `SOURCE_CONCLUSION_CROSSWALK.tsv` preserves each
controlling source package/row and exact scientific status separately from this overlay's
`RETAINED`, `RECLASSIFIED_CONDITIONAL`, `OPEN`, or `REJECTED_AS_INFERENCE` disposition.

### Survives unchanged

- generic multiplier reactions;
- aligned versus reactive constraints;
- failure of finite penalties to impose exact hard constraints;
- the finite Noether identity;
- multiplier-induced finite-boundary terms;
- the earlier `BOTH_CONDITIONALLY_ADMISSIBLE` field-census result;
- unrestricted variation of declared fields as `RETAIN_TRIAL`;
- hard substitution as unrestricted parent variation remains `REFUTED_GENERICALLY`;
- covariance as a field-census selector remains `REFUTED_AS_SUFFICIENT`;
- CSN exclusion of a multiplier remains `REFUTED_AS_GENERIC_EXCLUSION`;
- the category-A bulk existence witness remains non-native;
- bootstrap's `ON_SHELL_CLOSURE_OR_ADMISSIBILITY` role and `UNDERDETERMINED` result;
- Common-Scale Neutrality remains `FOUNDING`;
- positive CSN rescaling preserves causal reachability in the registered Lorentzian class;
- the binding finite mirrored cell and rejection of spatial infinity as native input.

### Reclassified, not discarded

- bulk covariance remains a conditional parent-action class;
- Hamiltonian- and momentum-like equations become parent-equation-and-foliation-conditional
  projections; physical normalization may be post-scale, but that is not derived by the toy;
- the lapse-like term is a formal multiplier example, while native shift ontology and detailed role
  remain open.

### Still open

- the parent covariant UDT equation or action;
- the off-shell field census;
- local constraint propagation;
- bootstrap's predicate-versus-multiplier-versus-map role;
- physical clock/ruler calibration, representative selection, and material transformation;
- material no-signalling and finite-cell boundary completion.

### Rejected as inferences

- co-presence itself propagates constraints;
- standalone ADM constraints are native UDT laws;
- lapse or shift are native physical fields;
- a projected constraint is foliation-independent by itself;
- co-presence selects `C^2`, EH, derivative order, or a unique bridge.

## 9. What actually needs to be redone

No previous exact constraint calculation needs immediate recomputation. What needs replacement is the
workflow of trying familiar constraints one by one before identifying their parent role.

The next concrete physics object is earlier than an ADM constraint:

> a native whole-solution UDT law—covariant or otherwise—with an explicit field census, variation
> domain, finite-cell completion, and bootstrap role.

Only after that object exists is it meaningful to project it into Hamiltonian/momentum-like form,
determine from its principal part whether those projections are initial-data constraints, ask
whether they propagate, or compare its lapse/shift structure with GR.

This does not remove the earlier immediate bootstrap fork. If bootstrap is to do more than filter
realized solutions, UDT must still derive whether it is a varied global constraint or a
representative-selection map. A selection map would still not supply the missing dynamical matching
between conditional `C^2` and EH branches.

## 10. Final authority boundary

This is a reclassification overlay, not a new action or a rejection of GR. GR remains a useful
comparison and computational language. No concrete GR constraint has been adopted, solved, or tested
against data. Complete action, source, matter coupling, boundary charge, native mass, and bridge remain
open. Prior frozen packages and their historical conclusions remain byte-identical.
