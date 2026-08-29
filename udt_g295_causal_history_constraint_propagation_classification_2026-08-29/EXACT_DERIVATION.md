# G295 exact derivation — causal history constraint and propagation

Date: 2026-08-29

## 1. Bounded landing

```text
ONE_COVARIANT_HISTORY_CONDITION_IS_THE_MINIMAL_TYPE
__SLICE_CONSTRAINT_AND_CAUSAL_UPDATE_ARE_A_REPRESENTATION
__FORMULA_AND_REALIZED_HISTORY_REMAIN_OPEN
```

This is a type simplification, not equation-count reduction. A vector- or tensor-valued covariant
history condition may contain the same functional rank as several slice equations. G295 does not
derive its formula or coefficients.

## 2. Why the G294 pair can be one whole-law type

Let a complete UDT relational history be denoted by \(\mathcal N\), including the metric and all
physical pair, frame, screen, and carry data. The foliation-free missing object can be typed as

\[
\boxed{\mathscr E[\mathcal N]=0},
\]

where \(\mathscr E\) must be nonidentity, diffeomorphism- and gauge-natural, orchestra-compatible,
and possess a well-posed response whose support is metric-causal.

If an integrable time slicing is later supplied, the same whole-history condition may separate
into a constraint on one slice and an update between slices. That split is representational; it is
not evidence for two independent mechanisms or a preferred foliation: the covariant type requires
no global now.

Conversely, any sliced pair can be stacked into one residual,

\[
\mathscr H(x,x')=
\begin{pmatrix}
A x\\
x'-U x
\end{pmatrix}=0.
\]

This stacking alone proves no physical minimality. Its role is only to show that “constraint plus
update” need not be two ontological additions.

## 3. Exact constraint-propagation theorem

Let \(A:V\to W\) have full row rank and let \(U:V\to V\) be a linear update. The constraint
surface \(\ker A\) is preserved by \(U\) if and only if there exists \(R:W\to W\) such that

\[
\boxed{AU=RA}.
\]

If \(AU=RA\), then \(Ax=0\) implies \(AUx=RAx=0\). Conversely, if \(U\ker A\subseteq\ker A\),
then \(AU\) vanishes on \(\ker A\) and therefore factors uniquely through
\(V/\ker A\simeq W\), producing \(R\).

For a nonlinear regular constraint \(\mathscr C(x)=0\) and update \(\mathscr U\), the direct
condition is

\[
\mathscr C(\mathscr U(x))=0
\quad\text{whenever}\quad
\mathscr C(x)=0.
\]

Its tangent version is the displayed factorization of the linearized residual. G295 proves only
the exact linear theorem and uses the nonlinear statement as the defining compatibility type.

## 4. Causality is an independent gate

Choose a declared finite causal order and require \(U_{ij}=0\) whenever input \(j\) is not in the
causal past allowed for output \(i\). In the three-component control,

\[
A=(-1,1,0),
\qquad
U=
\begin{pmatrix}
\alpha&0&0\\
\alpha-\gamma&\gamma&0\\
p&q&s
\end{pmatrix},
\]

the update is causal in the declared lower-triangular order and

\[
AU=\gamma A.
\]

Every choice of \((\alpha,\gamma,p,q,s)\) preserves the same nonidentity constraint. The current
architecture therefore does not select the update coefficients.

A causal diagonal update can fail \(AU=RA\), so causal support does not imply constraint
propagation. Conversely, the orthogonal simultaneous projection onto \(x_0=x_2\),

\[
P=
\begin{pmatrix}
\tfrac12&0&\tfrac12\\
0&1&0\\
\tfrac12&0&\tfrac12
\end{pmatrix},
\]

obeys \(AP=0\) and \(P^2=P\), but has both \(P_{02}\ne0\) and \(P_{20}\ne0\). It is a dense
same-slice adjustment and violates the declared causal support mask. Thus a global projection may
enforce a constraint while failing W6 as a controllable response.

The finite mask is a mathematical classifier, not a derivation of the UDT response operator. In a
physical completion the support relation must come from the completed metric cone.

## 5. Why current network identities still do not become the law

For three vertex potentials, take

\[
B=
\begin{pmatrix}
-1&1&0\\
0&-1&1\\
-1&0&1
\end{pmatrix},
\qquad
z^T=(1,1,-1).
\]

Then \(z^TB=0\), and for every vertex update \(V\),

\[
z^TBV=0.
\]

Triangle composition survives arbitrary updated vertex values. This is exactly why reversal,
cycle, overlap, and reconstruction remain identity layers: they certify a coherent valuation but
do not propagate its numerical content.

## 6. The screen sector cannot be hidden in a scalar law

Extend the state by two independent screen variables. Two block updates can share the same depth
block and obey the same scalar constraint while differing in their screen block. Both pass the
scalar propagation test. Therefore a physical whole-history law must act on the complete metric and
pair/screen state—or derive its screen evolution from that complete state. It cannot treat
\(\phi\), \(\delta\), or one longitudinal constraint as the full law.

This retains G274 path-labelled frame carry and the G290/G292 distinction between a topological
screen sector and its continuously varying local connection/flux.

## 7. A law family is not one realized history

One fixed causal, constraint-preserving update admits multiple initial states in \(\ker A\). Exact
iteration produces different histories while every state remains on the constraint surface. Thus:

\[
\boxed{\text{law} + \text{admissible data} \longrightarrow \text{one realized history}.}
\]

It is generally too strong to demand that founding laws alone select one complete universe. The
scientific closure target is first a nonidentity, well-posed physical solution family. Initial or
boundary data—and later observational anchors—may identify our realized member only after that
family exists. Data alone cannot replace the law by selecting an unrestricted function.

This retypes a recurring ambiguity in “history selection.” G286 still requires a genuine future
restriction: a candidate law must reject at least one of its inequivalent continuations or assign
them to distinct admissible data. But uniqueness of the entire universe from premise-free algebra
is not the acceptance standard.

## 8. Exact architecture classification

1. `IDENTITY_DESCENT_ONLY` is reconstructive and nonselective.
2. `INSTANT_GLOBAL_PROJECTION` can be nonidentity but fails W6 when it has controllable off-cone
   response.
3. `SLICE_CONSTRAINT_PLUS_CAUSAL_UPDATE` is viable only when the constraint propagates and the
   update is cone-supported; it also requires a supplied lawful slicing.
4. `WHOLE_HISTORY_COVARIANT_CONDITION` is the least-foliation-dependent missing-law type. Its
   slice decomposition is optional representation.
5. `INITIAL_OR_BOUNDARY_DATA_ONLY` may choose a member of an existing solution family but cannot
   create that family.

## 9. What W6 does and does not add

W6 excludes literal off-cone controllable response and permits non-propagating relational
membership. It thereby removes instantaneous global projection as the default reading and points
to a causal whole-history law. W6 does not choose \(\mathscr E\), its differential/integral order,
its state domain, coefficients, data, physical relation population, or observation map.

## 10. Maximum conclusion

The smallest clean target is one covariant nonidentity condition on complete metric/relation
histories with metric-causal well-posed response. “Constraint plus causal update” is its possible
slice representation, not necessarily two new mechanisms. This is a meaningful simplification of
the missing law's type. The formula and realized history remain `OPEN`.
