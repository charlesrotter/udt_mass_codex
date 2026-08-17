# G143 exact derivation — what one calibrated pair domain already owns

## 1. One relation has one domain before it has two endpoints

A supplied regular pair realization is a map

\[
F:\Sigma\to(M,g),\qquad h=F^*g.
\]

If one ordered calibrated chart `y=(y0,y1)` covers the two parameter points `A,B`, tangent vectors
at both points are represented by coefficient columns in the same model `R^2`. This does not
canonically identify the geometric tangent fibers `T_A Sigma` and `T_B Sigma`; it is the
trivialization supplied by the chart. In that presentation the coefficient carry is

\[
M_{BA}^{(y)}=I,
\qquad
C_{BA}^{(y)}=R_B R_A^{-1}.
\]

Thus G141 identity carry is naturally available inside one supplied calibrated query chart. It is
not a new physical force or a coordinate-free transport theorem.

## 2. Reparameterization produces exactly the G142 carry law

Let `z=z(y)` be another flag-preserving chart with positive-diagonal upper-triangular endpoint
Jacobians

\[
J_i=\left.\frac{\partial z}{\partial y}\right|_i.
\]

Vector coefficients obey `v_z=J_i v_y`, so the coframe factors obey

\[
R_i^{(z)}=R_i^{(y)}J_i^{-1}.
\]

The old identity identification becomes

\[
M_{BA}^{(z)}=J_BJ_A^{-1}.
\]

Substitution into G142 gives

\[
\begin{aligned}
C_{BA}^{(z)}
&=R_BJ_B^{-1}(J_BJ_A^{-1})(R_AJ_A^{-1})^{-1}\\
&=R_BR_A^{-1}=C_{BA}^{(y)}.
\end{aligned}
\]

For three points,

\[
(J_CJ_B^{-1})(J_BJ_A^{-1})=J_CJ_A^{-1},
\]

so these query-domain carries compose exactly.

Their scalar gradings obey

\[
\chi(M_{BA}^{(z)})=\chi(J_B)-\chi(J_A),
\]

while the endpoint-factor shifts cancel it. Only `chi(C_BA)` is invariant. This is the concrete
same-query instance of G142's general endpoint-gauge formula.

## 3. Smooth nonidentity witness on the same query

On a strip `0<=s<=1`, use

\[
z^0=(1+s)t,\qquad z^1=s.
\]

Its Jacobian is

\[
J(t,s)=\begin{pmatrix}1+s&t\\0&1\end{pmatrix},
\qquad \det J=1+s>0.
\]

At `A=(0,0)` and `B=(0,1)`,

\[
J_A=I,\qquad J_B=\operatorname{diag}(2,1),\qquad
M_{BA}^{(z)}=\operatorname{diag}(2,1)\ne I.
\]

The map is smoothly invertible on the strip, with `t=z0/(1+z1)`. Exact substitution shows that
this nonidentity carry leaves `C_BA` unchanged. Therefore the carry matrix by itself is not a new
physical effect; it includes how one calibrated relation is presented.

## 4. What is and is not now owned

One supplied calibrated chart spanning both parameter points owns a lawful identity-carry
presentation. A supplied atlas owns transition Jacobians on its overlaps. The pair metric `h`
canonically owns its Levi-Civita connection, which gives isometric tangent transport along a
supplied path; a unique in-neighborhood geodesic can also be used where its local hypotheses hold.

But `h` on an unrestricted pair domain does not make coordinate identity between separated tangent
fibers meaningful or provide a universal path-independent carry. Generic endpoints do not select a
global path, and curved transport may retain route dependence. Nor does one pair domain identify
its carrier with a different query, branch, or realization. Such comparisons require an
overlap/gluing map, a common atlas, or path-labelled transport.

This sharply separates two questions:

1. **Inside one fully typed query:** no carry mechanism is missing; the domain calibration already
   provides it, and G142 makes changes of presentation cancel.
2. **Between different queries or branches:** the metric can evaluate a supplied identification,
   but current premises do not select one or prove that the two realizations are the same relation.

## 5. Maximum conclusion

The G141 identity carry is a natural presentation of one supplied calibrated pair chart, and G142
is exactly its chart-covariant form. This removes the carry as a missing physical ingredient for a
single fully specified query. It does not derive the query, pair realization, cross-query gluing,
physical restriction to `B^+(2)`, complete history, proper length, or `X_max`.
