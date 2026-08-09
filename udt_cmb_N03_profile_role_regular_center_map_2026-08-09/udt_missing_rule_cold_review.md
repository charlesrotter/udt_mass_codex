# Cold review of the missing UDT observer-pair rule

**Primary landing:** `TYPE_OR_EXISTENCE_FAILURE` on the full complete-arrow arena as presently typed.  
**Conditional constructive result:** a reciprocal-root cocycle exists and is uniquely selected within a natural flag-character class after one explicit observer-query/Reciprocity premise is added.

This review treats the supplied document as an external-review problem statement, not as a UDT result.

---

## 1. Executive finding

There are two separate missing objects:

1. **The comparison arrow:** the metric at two endpoints does not by itself produce an invertible map
   \(A:T_pM\to T_qM\). A path plus Levi-Civita transport does produce one, but it is an isometry and therefore has trivial strain \(A^\dagger A=I\).
2. **The scalar extractor:** even when an arbitrary complete arrow \(A\) is supplied, no real function of the arrow alone can be both exactly additive on the full general-linear comparison groupoid and recover the reciprocal subgroup depth.

The second claim has a short exact proof. If an additive depth \(\Delta\) is defined on all invertible loops, then it vanishes on commutators. But

\[
D_t=\operatorname{diag}(e^{-t},e^t,1,1)
\]

is itself the commutator

\[
D_t=S_tJ S_t^{-1}J^{-1},\qquad
S_t=\operatorname{diag}(e^{-t},1,1,1),\quad
J=\begin{pmatrix}0&-1\\1&0\end{pmatrix}\oplus I_2.
\]

Hence every arrow-only additive scalar on the full isotropy group gives \(\Delta(D_t)=0\), contradicting the required \(\Delta(D_t)=t\) for \(t\ne0\).

The missing law therefore cannot live on the full, untyped set of invertible arrows. The observer objects must be enriched so that the isotropy group is reduced from \(GL(4)\) to a subgroup carrying a nontrivial reciprocal character.

A minimal and mathematically natural enrichment is an **ordered causal two-flag**

\[
F=(L_t\subset P_{tr}\subset V),
\]

where \(L_t\) is the observer clock line and \(P_{tr}\) is the Lorentzian clock–ruler comparison plane. On the action groupoid of such flags, an exact candidate is

\[
\boxed{\delta_{\mathrm{RF}}(A,F)=\tfrac12 b_2(A,F)-b_1(A,F)}
\]

with \(b_1\) the logarithmic one-volume expansion of the clock line and \(b_2\) the logarithmic two-volume expansion of the clock–ruler plane. This is the reciprocal-root component of a flag/Iwasawa-type cocycle.

It is:

- endpoint-frame invariant;
- exactly additive when the flag is transported through the intermediate observer;
- sign-reversing under arrow inversion;
- equal to the founded depth on \(D_t\);
- sensitive to off-block mixing whenever that mixing changes the transported clock line or comparison plane; and
- singular precisely when the transported causal flag becomes null or degenerate.

It is not metric-selected until the observer query supplies the causal flag and the physical comparison process supplies the arrow carrying that flag.

---

## 2. Type-check of the proposed arena

### 2.1 Metric data do not identify different tangent spaces

A Lorentz metric supplies \((T_pM,g_p)\) and \((T_qM,g_q)\). It does not supply a distinguished map between them. Such a map requires at least one of:

- a path and a connection;
- a global or local frame with a declared physical identification rule;
- an observer-measurement protocol; or
- an independently supplied comparison arrow.

Levi-Civita parallel transport along a chosen path is metric-canonical, but it obeys

\[
g_q(P_\gamma u,P_\gamma v)=g_p(u,v),
\]

so

\[
P_\gamma^\dagger P_\gamma=I.
\]

Therefore every strain-eigenvalue depth obtained from Levi-Civita transport is zero. Levi-Civita transport cannot by itself be the nontrivial reciprocal comparison.

### 2.2 A coframe is either gauge or extra physical data

If a complete coframe is merely an orthonormal representative of the metric, independent endpoint Lorentz changes are gauge and no formula may depend on that representative. If the coframe is physical, the allowed gauge group is smaller and this must be stated. The two interpretations cannot be used simultaneously.

An orthonormal coframe also gives an isometric endpoint identification if equal internal components are identified. Thus a nontrivial reciprocal strain still requires a comparison rule beyond the orthonormal coframe itself.

### 2.3 The groupoid object determines whether reciprocal scaling is possible

For the general-linear groupoid of a vector bundle, the isotropy at an object is the full general-linear group of that fiber. A real multiplicative function restricts on every isotropy group to a group homomorphism. Consequently the choice of object is load-bearing:

- If an object is only a point or tangent space, the isotropy is too large and the full-GL no-go below applies.
- If an object includes a clock line, ruler plane, or full flag, the isotropy is reduced to a parabolic subgroup with nontrivial logarithmic characters.

The current phrase “appropriately typed observer/event/coframe queries” does not yet decide between these cases.

---

## 3. Exact no-go theorem on the full complete-arrow groupoid

### Theorem 1 — full-GL reciprocal-character obstruction (`DERIVED`)

Let \(V\) be four-dimensional and suppose \(\Delta:GL^+(V)\to\mathbb R\) obeys

\[
\Delta(BA)=\Delta(B)+\Delta(A).
\]

Then \(\Delta(D_t)=0\) for every

\[
D_t=\operatorname{diag}(e^{-t},e^t,1,1).
\]

#### Proof

Every homomorphism to an abelian group vanishes on commutators. Define

\[
S_t=\operatorname{diag}(e^{-t},1,1,1),\qquad
J=\begin{pmatrix}0&-1\\1&0\end{pmatrix}\oplus I_2.
\]

Direct multiplication gives

\[
S_tJ S_t^{-1}J^{-1}
 =\operatorname{diag}(e^{-t},e^t,1,1)
 =D_t.
\]

Therefore

\[
\Delta(D_t)=\Delta(S_t)+\Delta(J)-\Delta(S_t)-\Delta(J)=0.
\]

This contradicts \(\Delta(D_t)=t\) unless \(t=0\). ∎

This proof needs no continuity, differentiability, frame covariance, or spectral assumption. It only needs the displayed arrows and their composites to be admissible loops. Therefore either:

1. the full general-linear arrow arena is not the physical groupoid; or
2. no required cocycle exists on that arena.

For smooth characters, the same obstruction appears in the standard classification: every smooth homomorphism \(GL^+(4)\to\mathbb R\) is a constant multiple of \(\log\det\), and \(\det D_t=1\).

### Corollary — the object must carry a reciprocal flag

To obtain nonzero depth on \(D_t\), the isotropy group must be reduced to a subgroup whose abelianization contains the reciprocal dilation. An ordered clock/ruler flag does exactly this.

---

## 4. Transitive-groupoid classification and the endpoint-potential ambiguity

### Theorem 2 — every cocycle is an endpoint term plus an isotropy character (`DERIVED`)

Let \(\mathcal G\) be a transitive groupoid, choose a base object \(o\), and choose one connector \(r_x:o\to x\) for every object \(x\). For a real cocycle \(c\), define

\[
f(x)=c(r_x),\qquad \chi(h)=c(h)\quad(h\in\mathcal G_o^o).
\]

Then every arrow \(g:x\to y\) satisfies

\[
\boxed{c(g)=f(y)-f(x)+\chi(r_y^{-1}gr_x).}
\]

#### Proof

Set \(h=r_y^{-1}gr_x\), so \(g=r_yhr_x^{-1}\), and use additivity and inversion. ∎

This theorem sharpens the type issue:

- If \(D_t\) is an isotropy loop in a full-GL object, Theorem 1 forces its depth to vanish.
- An endpoint potential can give nonzero depth only if reciprocal calibration changes the object label.
- Thus a calibration line or flag is not optional bookkeeping; it changes the groupoid cohomology in exactly the needed way.

---

## 5. Why the strain eigenvalue is invariant but not compositional

For composable complete arrows \(A:V_p\to V_q\) and \(B:V_q\to V_r\),

\[
C_A=A^\dagger A,
\qquad
C_{BA}=(BA)^\dagger(BA)=A^\dagger C_BA.
\]

There is no general relation

\[
\operatorname{spec}(C_{BA})
 =\operatorname{spec}(C_B)\operatorname{spec}(C_A).
\]

The intermediate orientation of the strain axes is missing from the spectra. Therefore an arrow-by-arrow choice of the timelike eigenline is not functorial under concatenation.

This explains the exact status of the regular-stratum extractor

\[
-\tfrac12\log\lambda_t(C_A):
\]

- frame invariant: yes;
- inversion odd: yes on the regular stratum;
- mixing sensitive: yes;
- exactly additive: no in general.

The right way to restore additivity is not to reselect an eigenline separately for every arrow. It is to carry a line or flag coherently through the comparison groupoid.

---

## 6. A minimal viable law: the reciprocal-root causal-flag cocycle

### 6.1 Domain

An object is

\[
x=(V,g,F),\qquad F=(L_t\subset P_{tr}),
\]

where:

- \(L_t\) is a timelike line;
- \(P_{tr}\) is a nondegenerate two-plane of signature \((-+)\);
- \(L_t\subset P_{tr}\).

An arrow \((A,F)\) is admissible when

\[
A(L_t)\text{ is timelike},\qquad A(P_{tr})\text{ remains nondegenerate of signature }(-+).
\]

Its target flag is \(AF=(A L_t\subset A P_{tr})\). This is an action groupoid, not the untyped full-GL groupoid.

### 6.2 Logarithmic flag expansions

Choose any nonzero \(u\in L_t\) and any \(r\in P_{tr}\) such that \(u\wedge r\ne0\). Define

\[
b_1(A,F)
 =\log\frac{\sqrt{|g_q(Au,Au)|}}{\sqrt{|g_p(u,u)|}},
\]

and

\[
b_2(A,F)
 =\log
 \frac{
 \sqrt{\left|\det\big(g_q(Av_i,Av_j)\big)_{i,j=1}^{2}\right|}
 }{
 \sqrt{\left|\det\big(g_p(v_i,v_j)\big)_{i,j=1}^{2}\right|}
 },
\qquad (v_1,v_2)=(u,r).
\]

These are independent of the chosen representative \(u\), of the chosen basis of \(P_{tr}\), and of endpoint orthonormal coframes.

They satisfy

\[
b_k(BA,F)=b_k(B,AF)+b_k(A,F),\qquad k=1,2.
\]

Define the graded clock and ruler log scales

\[
\ell_t=b_1,
\qquad
\ell_r=b_2-b_1.
\]

The reciprocal-root depth is

\[
\boxed{
\delta_{\mathrm{RF}}(A,F)
 =\frac{\ell_r-\ell_t}{2}
 =\frac12 b_2-b_1.
}
\]

### 6.3 Exact properties (`DERIVED` on the stated domain)

1. **Composition**
   \[
   \delta_{\mathrm{RF}}(BA,F)
   =\delta_{\mathrm{RF}}(B,AF)+\delta_{\mathrm{RF}}(A,F).
   \]
2. **Reversal**
   \[
   \delta_{\mathrm{RF}}(A^{-1},AF)=-\delta_{\mathrm{RF}}(A,F).
   \]
3. **Frame covariance** — all quantities are Gram-volume ratios.
4. **Pure reciprocal reduction** — for
   \(D_t=\operatorname{diag}(e^{-t},e^t,1,1)\) on the standard clock/ruler flag,
   \[
   b_1=-t,\qquad b_2=0,\qquad \delta_{\mathrm{RF}}=t.
   \]
5. **Mixing sensitivity** — screen components of \(Au\) or of \(AP_{tr}\) alter the Gram volumes.
6. **Null/degenerate strata** — the law ceases to be real and finite when the clock line becomes null or the comparison plane becomes degenerate. Those are explicit branch boundaries rather than hidden eigenvalue failures.

### 6.4 Relation to the strain extractor

For the clock line alone,

\[
\frac{g_q(Au,Au)}{g_p(u,u)}
 =\frac{g_p(u,C_Au)}{g_p(u,u)}.
\]

If \(u\) is the timelike eigenline of \(C_A\) with eigenvalue \(\lambda_t\), then

\[
-b_1=-\tfrac12\log\lambda_t.
\]

Thus the strain formula is the clock-line cocycle evaluated on an arrow-specific eigenline. It loses composition because that eigenline is reselected rather than transported. The causal-flag law retains the missing state.

---

## 7. Exact value on the document's lower-mixing example

For

\[
A=
\begin{pmatrix}
1/2&0&0&0\\
0&2&0&0\\
1/4&0&1&0\\
0&0&0&1
\end{pmatrix},
\qquad
F=(\langle e_0\rangle\subset\langle e_0,e_1\rangle),
\]

with \(g=\operatorname{diag}(-1,1,1,1)\),

\[
A e_0=\tfrac12e_0+\tfrac14e_2,
\qquad
|g(Ae_0,Ae_0)|=\frac{3}{16},
\]

so

\[
b_1=\log\frac{\sqrt3}{4}.
\]

The source clock–ruler plane has absolute Gram determinant \(1\), while the image plane has absolute Gram determinant \(3/4\), so

\[
b_2=\log\frac{\sqrt3}{2}.
\]

Therefore

\[
\boxed{
\delta_{\mathrm{RF}}
 =\frac14\log\frac{64}{3}
 \approx0.7650676987.
}
\]

This differs from both values already identified in the problem statement:

\[
\delta_{\mathrm{quotient}}=\log2\approx0.6931471806,
\]

and

\[
\delta_{\mathrm{strain}}\approx0.6481668896.
\]

The example therefore supports nonuniqueness, but it also demonstrates that a mixing-sensitive exact cocycle is possible once the observer flag is carried as part of the object.

---

## 8. Nonuniqueness before the missing Reciprocity selector

Let the clock and ruler graded log scales be \(\ell_t\) and \(\ell_r\). Every expression

\[
\delta_{a,b}=a\ell_t+b\ell_r
\]

is an exact cocycle on the flag action groupoid. Pure reciprocal normalization gives only

\[
-a+b=1.
\]

This leaves a one-parameter family. Equivalently, using direct clock and ruler depth readouts,

\[
\delta_\kappa=(1-\kappa)\delta_t+\kappa\delta_r
\]

agrees with the founded \(D_t\) depth for every real \(\kappa\).

For the lower-mixing example,

\[
\delta_t=\log\frac4{\sqrt3},
\qquad
\delta_r=\log2,
\]

so the candidates are genuinely different.

### The smallest selector inside this class

Add the following explicit clarification of dual Reciprocity:

> **Clock–ruler exchange oddness.** Interchanging the two graded reciprocal channels sends physical depth to its negative, while leaving screen-only graded channels unchanged.

For a continuous character of the graded log scales, this requires

\[
(a,b)\mapsto(b,a),\qquad
\delta(b,a)=-\delta(a,b),
\]

so \(b=-a\). Together with \(-a+b=1\),

\[
a=-\tfrac12,\qquad b=\tfrac12.
\]

This uniquely gives

\[
\delta_{\mathrm{RF}}=\frac{\ell_r-\ell_t}{2}.
\]

If a full four-step flag is used, the same exchange-odd condition forces the coefficients of screen-only graded dilations to vanish. Screen geometry still affects depth through mixing into the transported clock/ruler flag, but a pure screen deformation that leaves that flag unchanged lies in the kernel.

This is a **possible clarification of Reciprocity** and an **observer-query/measurement condition**. It is not supplied by the Lorentz metric alone.

---

## 9. Why fixed-arrow characters cannot detect unipotent mixing

The lower-mixing example factors exactly as

\[
A=UD_0,
\]

where

\[
U=I+\tfrac12E_{20},
\qquad
D_0=\operatorname{diag}(1/2,2,1,1).
\]

In a triangular comparison group, every elementary unipotent shear lies in the commutator subgroup. For a diagonal \(H\),

\[
H(I+xE_{ij})H^{-1}=I+\frac{h_i}{h_j}xE_{ij},
\]

so an appropriate commutator realizes any desired shear. Consequently every additive arrow-only character obeys

\[
\chi(U)=0,
\qquad
\chi(A)=\chi(D_0).
\]

This proves a sharp incompatibility:

- an arrow-only exact character can recover reciprocal diagonal depth, but it cannot see unipotent mixing;
- a spectral strain extractor can see the mixing, but it is not exactly additive;
- a mixing-sensitive exact law must carry additional state, such as a moving flag, path lift, or central-extension coordinate.

---

## 10. Candidate-space classification

| Candidate | Domain | Exact composition | Frame covariance | Mixing response | Main obstruction/free datum |
|---|---|---:|---:|---:|---|
| Timelike strain eigenvalue | Regular strain stratum | No | Yes | Yes | Eigenline is reselected; complex/Jordan/null crossings |
| Full determinant character | Full \(GL\) | Yes | Yes | No shear sensitivity | Vanishes on reciprocal \(D_t\) |
| Fixed-flag block/diagonal characters | Parabolic or triangular arrows | Yes | Only with flag included or flag-preserving gauge | Ignores unipotent radical | Several logarithmic weights remain |
| Levi-Civita transport | Path groupoid | Transport composes | Yes | Holonomy only; strain is zero | Does not produce nontrivial reciprocal strain |
| Endpoint potential \(f(q)-f(p)\) | Pair groupoid | Yes | If \(f\) is scalar-natural | Arbitrary | Infinite nonuniqueness; descent assumed |
| Integrated one-form \(\int\alpha\) | Path groupoid | Yes | If \(\alpha\) is natural | Depends on generator | Metric does not select \(\alpha\); periods obstruct endpoints |
| Reciprocal-root flag cocycle | Causal-flag action groupoid | Yes | Yes | Yes through transported flag | Flag, comparison lift, and Reciprocity weight must be supplied |
| Central-extension depth coordinate | Lifted groupoid | Yes | Depends on extension | Can encode mixing | A groupoid 2-cocycle/lift is extra structure |

Natural local metric constructions do not restore uniqueness. At higher differential order one can form many curvature scalars and their gradients, producing many exact endpoint/path candidates. A dynamical equation or measurement principle would be needed to select among them.

---

## 11. The \(X_{\max}\) gate is not yet a selector

The separation \(s(p,q)\) is explicitly still open. For any candidate signed depth \(\delta\), define

\[
s_\delta=X_{\max}\tanh|\delta|.
\]

Then every finite comparison has

\[
0\le s_\delta<X_{\max},
\]

and

\[
s_\delta\to X_{\max}^{-}
\quad\Longleftrightarrow\quad
|\delta|\to\infty.
\]

Conversely,

\[
|\delta|=\operatorname{artanh}(s/X_{\max}).
\]

Therefore the asymptotic condition cannot distinguish candidate cocycles until \(s\) is independently constructed from the geometry and observer query.

---

## 12. Smallest missing premise

The smallest premise that makes the problem both well typed and selectively solvable is:

> **Reciprocal causal-flag transport axiom.** Every ordered observer comparison supplies a timelike clock line and a Lorentzian clock–ruler comparison plane. Physical comparison arrows transport that causal flag through concatenation. Physical depth is the continuous graded-scale character that is odd under clock–ruler exchange and normalized by \(D_t\mapsto t\).

This premise is best classified as:

- primarily an **observer-query/measurement condition**;
- potentially a **clarification of Reciprocity**;
- not already a consequence of the metric alone; and
- not a dynamics/action premise.

It selects

\[
\delta_{\mathrm{RF}}=\tfrac12b_2-b_1
\]

within the natural flag-character class and removes:

- clock-only versus ruler-only weighting ambiguity;
- determinant and common-volume characters;
- pure screen-area weights unchanged by channel exchange; and
- arrow-by-arrow spectral eigenline reselection.

It does **not** yet supply the physical non-isometric comparison arrow \(A\) from the metric, path, and observers. If \(A\) is not part of the admissible comparison data, a separate comparison-transport premise remains unavoidable.

---

## 13. Primary landing

### `TYPE_OR_EXISTENCE_FAILURE`

The present statement does not define a physical groupoid on which the required law can be tested. On the maximal natural interpretation—objects are tangent spaces and arrows are all invertible comparison maps—the required cocycle provably does not exist because the reciprocal subgroup lies in the commutator subgroup.

After enriching objects by a causal observer flag, an exact mixing-sensitive candidate exists. Within the continuous graded flag-character class, clock–ruler exchange oddness and pure reciprocal normalization select it uniquely. Its physical status remains `CONDITIONAL` until the observer flag and the comparison transport are adopted as premises.

---

## 14. Runnable algebra

The companion script `verify_udt_missing_rule.py` verifies:

1. the exact commutator identity for \(D_t\);
2. the strain spectrum of the supplied lower-mixing example;
3. the factorization of that arrow into unipotent mixing and reciprocal diagonal parts;
4. the exact reciprocal-root flag value \(\tfrac14\log(64/3)\);
5. pure reciprocal reduction; and
6. the one-parameter pre-selector family.

### Mathematical references consulted

- H. Bursztyn and M. del Hoyo, **Lie Groupoids**, arXiv:2309.14105.
- Z. Chen, H. Lang, and Z. Liu, **Multiplicative Forms on Poisson Groupoids**, arXiv:2201.06242.
- Standard Iwasawa/Busemann flag cocycles, in which wedge-norm logarithms obey an action-groupoid cocycle identity; see the references cited in the review's research notes.
- A. Navarro and J. Navarro, **Lovelock's theorem revisited**, arXiv:1005.2386, for the natural-tensor framework.
