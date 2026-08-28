# G286 exact derivation — compatibility is not complete-state propagation

Date: 2026-08-28

## 1. Type clarification used for this gate

G285 is used provisionally, not canonized: the tested complete local separation state is the
completed calibrated pair together with neighboring-relation variation sufficient to recover the
screen tidal matrix. Scalar reciprocal depth is only one component of that state.

This removes the false requirement that transverse response must be a function of scalar `phi`
alone. It does not imply that the values of successive complete local states are already fixed.

## 2. Frozen complete-metric family

Use G283's externally reviewed exact metric family

\[
g_T=-2\,du\,dv+dx^2+dy^2-x^iT_{ij}(u)x^j\,du^2,
\]

where \(T(u)\) is any smooth symmetric screen matrix. Along the central null relation,

\[
R_{uiuj}=T_{ij}(u),
\]

and the same matrix drives the path-labelled Jacobi equation. G283 already verifies that every
smooth symmetric \(T\) in this family satisfies the registered metric, Cartan/Bianchi, screen,
symplectic, composition, reversal, overlap, and frame-carry identities.

## 3. Same-prior, distinct-future witnesses

Define the standard smooth flat switch

\[
b(u)=
\begin{cases}
0,&u\le 0,\\
e^{-1/u^2},&u>0,
\end{cases}
\]

and set

\[
T_0(u)=0,
\qquad
T_1(u)=\frac15 b(u)
\begin{pmatrix}
1&0\\
0&-1
\end{pmatrix}.
\]

For every nonnegative integer \(n\), the positive-side derivative of \(e^{-1/u^2}\) has the form

\[
\frac{d^n}{du^n}e^{-1/u^2}=P_n(1/u)e^{-1/u^2}
\]

for a polynomial \(P_n\). Exponential decay dominates every power as \(u\to0^+\), so every
positive-side derivative tends to zero. Consequently \(b\) is smooth and flat at \(u=0\).

It follows exactly that:

1. \(g_{T_0}=g_{T_1}\) throughout the entire region \(u\le0\);
2. every metric, connection, curvature, and higher derivative jet agrees at \(u=0\);
3. the complete past relation networks and all joining-surface local data agree;
4. both metrics are smooth and Lorentzian, with determinant \(-1\);
5. both pass the inherited G283 identity layer.

For every \(u>0\), however, \(T_1(u)\ne0\). In particular,

\[
R_{uxux}[g_{T_1}]=\frac15e^{-1/u^2},
\qquad
R_{uyuy}[g_{T_1}]=-\frac15e^{-1/u^2},
\]

while the entire Riemann tensor of \(g_{T_0}\) vanishes. The futures are therefore geometrically
inequivalent. In G285's provisional, noncanon shorthand, they carry distinct future `L2` values and
distinct `L3` network extensions despite having the same complete prior network. This shorthand is
not used in the proof.

## 4. Transfer diagnostic

The production implementation integrates the supplied path-labelled first-order Jacobi transfer
with fourth-order Runge--Kutta. The independent implementation uses an implicit-midpoint Cayley
step. They are diagnostic evaluators, not candidate physical evolution laws.

The preregistered checks returned:

```text
production symplectic defect                    1.4210854715202004e-14
independent symplectic defect                    6.721290191080698e-13
production/independent final transfer difference 3.866140740882429e-11
active/flat future transfer difference           3.2701305e-2
```

All thresholds passed. The exact nonzero curvature tensor, rather than the numerical transfer,
carries the scientific separator.

## 5. Exact logical consequence

Overlap descent, frame carry, causal reconstruction, Cartan realization, and Jacobi composition
all continue to do substantial work: they reject inconsistent assignments and faithfully evaluate
a supplied continuation. But they accept both registered continuations from the same complete
prior region.

Therefore, on this bounded smooth complete-metric family,

```text
SAME_WHOLE_PRIOR_METRIC_REGION_AND_ALL_JOIN_JETS_ADMIT
__GEOMETRICALLY_INEQUIVALENT_FUTURE_CONTINUATIONS
__CURRENT_IDENTITY_EVALUATOR_LAYER_IS_NOT_UNIQUE_PROPAGATION
```

In G285's explicitly provisional, noncanon vocabulary, these futures have distinct `L2` values and
extend the same prior `L3` network differently. That vocabulary is secondary; the metric and
curvature statement above carries the result.

This is not a theorem that UDT can have no native propagation law. It proves that no such law is
contained in the tested identity/evaluator layer.

## 6. Scope caveat

The joining surface in this witness is null. G286 does not adjudicate the well-posedness of a future
candidate Cauchy or characteristic field law; none is adopted here. The stronger fact relevant to
the bounded question is that the two complete metrics agree on the entire prior region and that all
current owned identities admit both.
