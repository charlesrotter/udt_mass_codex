# Follow-up audit of the reciprocal-root causal-flag cocycle

## Primary landing

`CONDITIONAL_UNIQUE_READOUT__ARROW_SELECTION_NONUNIQUE`

**Definition of this landing.** On the maximal causal `(1,1,2)` flag-transport groupoid, the reciprocal-root expression

\[
\delta_{\mathrm{RF}}(A,F)=\frac12 b_2(A,F)-b_1(A,F)
\]

is a globally defined smooth cocycle. After imposing a *new formal exchange involution on the abstract clock/ruler graded channels*, it is the unique universal order-zero, endpoint-frame-natural real cocycle normalized by the pure reciprocal subgroup. It is not, however, the unique smooth cocycle on the underlying groupoid, the exchange involution is not induced by a causal Lorentz transformation or supplied by the founding two-channel algebra on the complete flag, and the metric does not select a unique non-isometric comparison arrow. Thus this is a strong conditional readout of a supplied arrow and transported flag, not the missing physical observer-pair rule.

This report treats the source as an external-review problem statement rather than as a banked UDT result.

---

## 1. The groupoid, exactly

### 1.1 Fixed geometric input

Fix a smooth four-manifold `M`, its tangent bundle `E=TM`, and a smooth Lorentz metric `g` of signature `(-,+,+,+)`. The construction below also works for any rank-four Lorentz vector bundle.

Let

\[
\operatorname{Fl}_{1,2}(E)
 =\{(p,L,P):L\subset P\subset E_p,\ \dim L=1,\ \dim P=2\}
\]

be the smooth partial-flag bundle. Define its causal open subbundle

\[
\mathscr C_g
 =\{(p,L,P)\in\operatorname{Fl}_{1,2}(E):g_p|_L<0\}.
\]

A two-plane containing a timelike line is automatically nondegenerate of signature `(-,+)`: if `u` spans the timelike line, then `u^\perp` is positive definite, and a vector in `P\cap P^\perp` must lie in `u^\perp` and be null, hence must vanish. Therefore no separate nondegeneracy condition on `P` is needed.

The timelike-line condition is open in the projective line bundle, so `\mathscr C_g` is an open submanifold of the flag bundle.

### 1.2 The general-linear groupoid and its flag action

The general-linear groupoid of `E` is

\[
GL(E)\rightrightarrows M,
\]

whose arrows are triples `(q,A,p)` with `A:E_p\to E_q` an invertible linear map. Its source and target are `p` and `q`; multiplication is composition.

It acts smoothly on the full flag bundle by

\[
A\cdot(p,L,P)=(q,AL,AP).
\]

The full transformation groupoid is

\[
GL(E)\ltimes \operatorname{Fl}_{1,2}(E)
 \rightrightarrows \operatorname{Fl}_{1,2}(E).
\]

The causal subset is not invariant under the full action: a general invertible map can send a timelike line to a spacelike or null line. The correct causal groupoid is therefore the open restriction

\[
\boxed{
\mathcal G_g
 =\left(GL(E)\ltimes\operatorname{Fl}_{1,2}(E)\right)|_{\mathscr C_g}
 \rightrightarrows \mathscr C_g .
}
\]

Equivalently, its arrow manifold is

\[
\mathcal G_g^{(1)}
 =\{(A,F):F\in\mathscr C_g,\ s(A)=\pi(F),\ A F\in\mathscr C_g\}.
\]

The endpoint metrics are part of the typing through the fixed field `g`: an arrow

\[
(A,F):(p,g_p,L,P)\longrightarrow(q,g_q,AL,AP)
\]

is not required to be an isometry.

### 1.3 Structure maps

For `F=(p,L,P)`:

\[
\begin{aligned}
s(A,F)&=F,\\
t(A,F)&=AF,\\
(B,AF)\circ(A,F)&=(BA,F),\\
(A,F)^{-1}&=(A^{-1},AF),\\
1_F&=(I_{E_p},F).
\end{aligned}
\]

### 1.4 Topology and smooth structure

`GL(E)` is the open submanifold of invertible elements in the vector bundle of cross-fibre homomorphisms over `M\times M`. The full action-groupoid arrow manifold is a fibre product over `M`. The conditions `F\in\mathscr C_g` and `AF\in\mathscr C_g` are open; hence `\mathcal G_g^{(1)}` is an open submanifold of the full action-groupoid arrow manifold. Source and target remain submersions, and all structure maps are restrictions of smooth maps. Thus `\mathcal G_g` is an ordinary Lie groupoid.

It has three equivalent descriptions:

1. an **open Lie subgroupoid** of the full flag action groupoid;
2. the **restriction** of that action groupoid to an open object set; and
3. the groupoid of the **partial action** of `GL(E)` on `\mathscr C_g`.

It is not a global action groupoid of `GL(E)` on `\mathscr C_g`.

### 1.5 Closure

If `(A,F)` and `(B,AF)` are arrows, then `F`, `AF`, and `BAF` are causal flags. Hence `(BA,F)` is an arrow. If `(A,F)` is an arrow, then both `AF` and `A^{-1}(AF)=F` are causal, so the inverse is an arrow. The identity preserves every causal flag. This proves closure under composition, inversion, and identities on the stated domain.

For arbitrary full-linear arrows the groupoid is transitive: any causal flag in one Lorentz fibre can be carried to any causal flag in another by some invertible map. If orientation or coorientation labels are added and arrows are restricted to preserve them, the same analysis applies separately on each transitive component.

---

## 2. The cocycle and the exact graded-volume system

### 2.1 Metric densities

For a nondegenerate `k`-plane `S\subset(E_p,g_p)`, define its positive metric density

\[
\nu_{g_p,S}(v_1,\ldots,v_k)
 =\sqrt{\left|\det(g_p(v_i,v_j))\right|}.
\]

For an arrow `(A,F)` with `F=(L\subset P)` define the positive expansion factors

\[
\rho_1(A,F)
 =\frac{\nu_{g_q,AL}(Au)}{\nu_{g_p,L}(u)},
\]

\[
\rho_2(A,F)
 =\frac{\nu_{g_q,AP}(Au,Av)}{\nu_{g_p,P}(u,v)},
\]

and

\[
\rho_4(A)
 =\frac{\nu_{g_q,E_q}(Ae_0,Ae_1,Ae_2,Ae_3)}
        {\nu_{g_p,E_p}(e_0,e_1,e_2,e_3)}.
\]

The ratios are independent of the chosen nonzero `u\in L`, of the completion `v\in P`, and of the basis of the full fibre. Set

\[
b_k=\log\rho_k,\qquad k=1,2,4.
\]

### 2.2 Exact telescoping

For every composable pair,

\[
\rho_k(BA,S)=\rho_k(B,AS)\rho_k(A,S),
\qquad k=1,2,4,
\]

because the intermediate metric density cancels. Hence

\[
b_k(BA,F)=b_k(B,AF)+b_k(A,F).
\]

Define the three associated-graded logarithmic scales

\[
\ell_t=b_1,
\qquad
\ell_r=b_2-b_1,
\qquad
\ell_s=b_4-b_2.
\]

They are respectively the scale characters of the clock line `L`, the one-dimensional ruler quotient `P/L`, and the two-dimensional screen quotient `E/P`. Each is a smooth real groupoid cocycle.

The proposed readout is

\[
\boxed{
\delta_{\mathrm{RF}}
 =\frac{\ell_r-\ell_t}{2}
 =\frac12b_2-b_1.
}
\]

Therefore

\[
\delta_{\mathrm{RF}}(BA,F)
 =\delta_{\mathrm{RF}}(B,AF)+\delta_{\mathrm{RF}}(A,F),
\]

\[
\delta_{\mathrm{RF}}(A^{-1},AF)=-\delta_{\mathrm{RF}}(A,F),
\qquad
\delta_{\mathrm{RF}}(I,F)=0.
\]

Independent Lorentz changes of endpoint coframes preserve the metric densities, so the expression is endpoint-frame invariant.

### 2.3 Pure reciprocal reduction

For the standard flag `L=\langle e_0\rangle`, `P=\langle e_0,e_1\rangle` and

\[
D_t=\operatorname{diag}(e^{-t},e^t,1,1),
\]

one has

\[
\ell_t=-t,\qquad \ell_r=t,\qquad \ell_s=0,
\]

and consequently

\[
\delta_{\mathrm{RF}}(D_t,F)=t.
\]

A common clock-ruler dilation has `\ell_t=\ell_r`, so it is neutral under `\delta_{\mathrm{RF}}`.

### 2.4 Mixing sensitivity and its exact limitation

The lower-mixing example in the source gives

\[
\rho_1^2=\frac{3}{16},\qquad
\rho_2^2=\frac34,
\]

and therefore

\[
\delta_{\mathrm{RF}}
 =\frac14\log\frac{64}{3}
 \approx0.76506769867289.
\]

Thus mixing that changes the metric norm of the transported clock line or the area of the transported comparison plane can change the readout.

However, no smooth real character of the full flag stabilizer can detect its unipotent radical or the `SL(2)` part of screen deformation. Pure flag-preserving shear, twist, and area-preserving screen mixing are invisible to every order-zero additive scalar in this groupoid. This is not an implementation defect of `\delta_{\mathrm{RF}}`; it follows from the isotropy-character classification below. If the physical rule must respond to those channels even when all graded volumes are fixed, either the object must retain a finer flag/state, the target must be nonabelian or multidimensional, or exact scalar additivity must be weakened.

---

## 3. Clock-ruler exchange is not a causal exchange

### 3.1 What the founding two-channel algebra proves

On the abstract reciprocal channel space, let

\[
K=\begin{pmatrix}0&1\\1&0\end{pmatrix},
\qquad
D(t)=\operatorname{diag}(e^{-t},e^t).
\]

Then

\[
D(t)^T K D(t)=K,
\qquad
K D(t)K=D(-t).
\]

This proves sign reversal under exchange of the two *abstract reciprocal labels* in the founding representation.

It does not prove a causal Lorentz exchange. With the physical two-plane metric

\[
\eta_{1,1}=\operatorname{diag}(-1,1),
\]

one has

\[
K^T\eta_{1,1}K=-\eta_{1,1}.
\]

Moreover `K` sends the standard timelike line to the standard spacelike line. It is an anti-isometry between the two sign assignments, not an element of the causal Lorentz group and not an automorphism of the causal-flag object space.

### 3.2 Precise complete-flag extension

The causal flag has associated graded dimensions

\[
\operatorname{gr}_F(E)=L\oplus(P/L)\oplus(E/P),
\]

with graded logarithmic scale coordinates

\[
(\ell_t,\ell_r,\ell_s).
\]

A precise formal exchange can be defined on the *coefficient/character space* by

\[
\sigma(\ell_t,\ell_r,\ell_s)
 =(\ell_r,\ell_t,\ell_s).
\]

Exchange oddness then means

\[
\delta\bigl(\sigma\ell\bigr)=-\delta(\ell).
\]

This is an involution on abstract channel labels or on the character lattice of the parabolic stabilizer. It is not an involution of physical causal subspaces. There is no canonical vector-space isomorphism `L\cong P/L`, no causal map that swaps them, and no canonical automorphism of `\mathcal G_g` implementing `\sigma`.

To realize `\sigma` geometrically one would have to add one of the following:

- a chosen calibration isomorphism between the two positive density lines;
- a doubled object space containing both the causal flag and an opposite/sign-swapped flag;
- an abstract reciprocal-channel bundle separate from the physical tangent flag; or
- another explicit coefficient local system carrying the involution.

### 3.3 Status

Exchange oddness is **derived on the supplied two-channel representation**. Its extension to the complete causal flag is an **additional observer-query/measurement or Reciprocity-extension postulate**. It must not be called derived unless the extra bundle and its involution are exhibited.

---

## 4. Classification of all smooth real cocycles

### 4.1 Transitive-groupoid decomposition

Let `\mathcal G\rightrightarrows X` be a transitive Lie groupoid and fix `x_0\in X`. Restrict a smooth cocycle `c` to the isotropy group `H=\mathcal G_{x_0}^{x_0}`:

\[
\chi(h)=c(h).
\]

Then `\chi:H\to(\mathbb R,+)` is a smooth group homomorphism. If `c_1` and `c_2` have the same isotropy character, their difference vanishes on isotropy. For any arrow `q:x_0\to x`, define

\[
u(x)=(c_1-c_2)(q).
\]

This is independent of `q`, because two such arrows differ by isotropy. It is smooth in local groupoid sections and satisfies

\[
(c_1-c_2)(g)=u(tg)-u(sg).
\]

Thus, after selecting one representative for each isotropy character, every cocycle is an endpoint coboundary plus an isotropy-character representative.

### 4.2 The isotropy group

At the standard flag in `\mathbb R^{1,3}`, the isotropy group is the parabolic

\[
P_{1,1,2}
 =\left\{
\begin{pmatrix}
a&u&\xi\\
0&b&\eta\\
0&0&C
\end{pmatrix}
:
 a,b\in\mathbb R^\times,
 C\in GL(2,\mathbb R)
\right\}.
\]

Its unipotent radical consists of the off-diagonal blocks. The Lie-algebra commutator has codimension three. The three abelianized directions are the traces on the `1`, `1`, and `2` diagonal blocks.

Every smooth homomorphism `\chi:P_{1,1,2}\to\mathbb R` is therefore

\[
\boxed{
\chi(A)
 =\alpha\log|a|
 +\beta\log|b|
 +\gamma\log|\det C|.
}
\]

The finite sign components contribute no homomorphism to the torsion-free additive group `\mathbb R`.

The global metric-density representatives are precisely

\[
\alpha\ell_t+\beta\ell_r+\gamma\ell_s.
\]

### 4.3 Full smooth classification on the declared groupoid

On each transitive component of `\mathcal G_g`, every smooth real cocycle has the form

\[
\boxed{
 c(A,F)
 =u(AF)-u(F)
 +\alpha\ell_t(A,F)
 +\beta\ell_r(A,F)
 +\gamma\ell_s(A,F),
}
\]

where `u\in C^\infty(\mathscr C_g)` is arbitrary and `\alpha,\beta,\gamma\in\mathbb R` are constants.

This formula is not an ansatz and does not assume linearity in `b_1` or `b_2`. It follows from transitivity and the complete character classification of the isotropy group.

Consequences:

- **Arbitrary invariant coboundaries survive** in the literal smooth class.
- **Curvature-dependent endpoint terms survive** if higher metric jets are allowed: for example `u=R`, or a scalar formed from curvature and the flagged directions.
- **One screen-area character survives** before exchange is imposed.
- **Nonlinear arrow invariants** can occur only inside the endpoint coboundary `u(t)-u(s)`; they do not create new isotropy characters.
- **Pure unipotent/shear or `SL(2)` screen characters do not survive**, because those subgroups lie in the commutator kernel of every real character.

### 4.4 What “order zero” must mean to remove the coboundary

There are two inequivalent readings:

1. **Fixed-manifold reading.** Any preassigned scalar `u(p,L,P)` is order zero as a function on the object manifold. Then infinitely many coboundaries remain and uniqueness fails.
2. **Universal natural reading.** The formula must be a diffeomorphism-natural algebraic construction from only one Lorentz vector space `(E_p,g_p)` and its flag `(L,P)`, with no external scalar field and no derivatives of `g`. The Lorentz group acts transitively on causal `(1,2)` flags, so there is no nonconstant pointwise scalar invariant. Then `u` is constant and its coboundary vanishes.

Only the second, stronger reading reduces the class to the three graded-volume characters. It must be stated explicitly; endpoint-frame invariance alone is not enough.

### 4.5 Normalization and formal exchange

For

\[
c=\alpha\ell_t+\beta\ell_r+\gamma\ell_s,
\]

pure reciprocal normalization gives

\[
-\alpha+\beta=1.
\]

The formal exchange `\sigma:(\ell_t,\ell_r,\ell_s)\mapsto(\ell_r,\ell_t,\ell_s)` and oddness give

\[
\beta=-\alpha,
\qquad
\gamma=0.
\]

The unique solution is

\[
\alpha=-\frac12,
\qquad
\beta=\frac12,
\qquad
\gamma=0,
\]

hence

\[
c=\delta_{\mathrm{RF}}.
\]

### 4.6 Exact uniqueness theorem—and its boundary

**Conditional order-zero uniqueness theorem.** Fix the causal `(1,1,2)` flag groupoid above. Restrict to universal, smooth, diffeomorphism-natural cocycles that depend only on the order-zero fibre data `(g_p,g_q,F,A)`, contain no external endpoint scalar, and obey the formally posited channel involution that swaps `\ell_t` and `\ell_r` while fixing `\ell_s`. Then pure reciprocal normalization selects `\delta_{\mathrm{RF}}` uniquely.

This theorem is stronger than uniqueness inside a preselected two-dimensional `b_1,b_2` ansatz: it starts from all smooth order-zero natural cocycles and finds a three-dimensional character space before exchange removes the screen character.

It is not uniqueness in the full smooth groupoid class. It also changes if the object is refined—for example, a complete screen flag produces additional diagonal characters—or if path labels, curvature jets, calibration fields, or observer metadata are admitted.

---

## 5. Foundation ownership of the flag

The two founding reciprocal postulates supply the two-channel representation once an ordered depth has been supplied. They do not, by themselves, identify the following tangent-space data for every observer-pair query:

| Datum | Status from the stated foundation |
|---|---|
| Timelike clock line `L_t\subset T_pM` | Not supplied as a canonical tangent subspace. It can be added by defining an observer with a worldline/velocity or clock axis. |
| Spacelike ruler direction | Not supplied. A clock line leaves a three-dimensional rest space; selecting one direction requires pair/path/measurement data. |
| Lorentzian plane `P_{tr}` | Exists only after the clock line and ruler direction are selected. |
| Orientations/coorientations | Not supplied. They are unnecessary for the absolute-density version of the cocycle. |
| Intermediate transport/update of the flag | Not supplied. It is essential for exact composition. |

The reciprocal coframe displayed on the bare branch gives a conditional local realization, not a proof that every complete observer query carries a globally selected physical flag.

A pair-relative flag does not require a global preferred congruence. It may be carried as comparison state along one ordered query. But composability requires a state-update law: the target flag of the first comparison must be exactly the source flag used by the second. Independently reselecting a “best” ruler plane for each pair destroys the cocycle identity.

Thus the flag and its transport are additional kinematic/measurement typing, not consequences of the two reciprocal equations alone.

---

## 6. Audit of the missing comparison arrow

The scalar readout accepts an invertible non-isometric map

\[
A:T_pM\to T_qM.
\]

The metric is pointwise; it does not identify distinct tangent fibres without a path-functor, connection, frame identification, or other comparison rule.

### 6.1 Candidate matrix

| Candidate | Exact concatenation | Endpoint covariance | Mixing/strain | Cut/conjugate behavior | Metric-derived? | Verdict |
|---|---:|---:|---:|---|---|---|
| Levi-Civita transport | Yes | Yes | Can rotate/mix frames, but all metric volumes are preserved | No cut-locus issue for a supplied path; path choice/holonomy remain | Yes, from `g` and a path | Gives `\delta_{RF}=0` |
| Endpoint orthonormal coframe comparison | Yes | Not under independent endpoint gauge changes | Isometric if coframes are orthonormal | No cut issue | Requires a selected coframe identification | Trivial or gauge-dependent |
| `d\exp_p|_v` | No | Yes | Curvature, shear, focusing sensitive | Singular at conjugate points; branch ambiguity at cut locus | Yes, after selecting `v`/geodesic | Not a groupoid functor |
| Full Jacobi propagator | Yes on doubled state space | Yes | Fully curvature/mixing sensitive | Full propagator remains invertible; projection blocks caustic | Yes, along selected geodesic | Wrong type: `8D`, not a canonical `4D` map |
| Cartan/affine development | Yes as an affine map | Yes | Translation records development; linear part is isometric | No cut issue for a supplied path | Yes, from connection/path | Linear part gives zero depth |
| Strain or polar map | Only after an `A` is already supplied | Conditional | Sensitive on regular strata | Spectral/Jordan/polar branches | No independent `A` | Extractor, not arrow generator |
| Higher-order natural connection transport | Yes | Yes | Generically non-isometric and mixing sensitive | No cut issue for supplied path; causal flag can leave domain | Yes after choosing a natural rule | Infinite unselected family |

### 6.2 Levi-Civita transport

For a supplied path `\gamma`, parallel transport satisfies

\[
P_{\gamma_2\circ\gamma_1}
 =P_{\gamma_2}P_{\gamma_1},
\qquad
P_{\bar\gamma}=P_\gamma^{-1}.
\]

Metric compatibility gives

\[
g_q(P_\gamma u,P_\gamma v)=g_p(u,v).
\]

Consequently

\[
b_1=b_2=b_4=0,
\qquad
\delta_{\mathrm{RF}}=0.
\]

Holonomy may rotate the flag, but a real graded-volume character cannot turn an isometry into nonzero reciprocal depth.

### 6.3 Endpoint coframe comparison

For orthonormal coframes `\theta_p,\theta_q`, the component-identification map

\[
A_{pq}=\theta_q^{-1}\theta_p
\]

composes exactly. It is also an isometry. Under independent endpoint Lorentz gauge changes it changes unless a gauge transporter or a physically fixed coframe is supplied. Thus it is either trivial for the cocycle or imports extra frame structure.

### 6.4 Differential of the exponential map

Away from conjugate points, `d\exp_p|_v` is an invertible Jacobi map and can carry focusing, shear, and mixing. It does not compose under segmented geodesics because each exponential differential resets the Jacobi initial conditions.

In constant curvature `+1`, the transverse factor is

\[
j(r)=\frac{\sin r}{r}.
\]

For `r=s=\pi/6`,

\[
j(r+s)=\frac{3\sqrt3}{2\pi}
\ne
\frac9{\pi^2}=j(r)j(s).
\]

At a conjugate point the differential is singular. At the cut locus the inverse exponential is multivalued or nonsmooth even when a chosen branch has nonsingular differential. Thus this construction fails the required arrow functoriality and global inversion tests.

### 6.5 Jacobi propagators

The Jacobi equation is second order. The full state

\[
(J,\nabla_{\dot\gamma}J)
\]

has an invertible fundamental propagator on an eight-dimensional phase space, and these propagators compose exactly. The `d\exp` map is one block of this matrix. Individual blocks do not compose because matrix multiplication introduces cross terms.

To turn the full propagator into a four-dimensional tangent map, one must choose a Lagrangian graph, congruence, optical initial condition, or Riccati datum. That is additional structure. At caustics the selected graph can leave its coordinate chart even though the full propagator remains regular.

### 6.6 Cartan development

Affine or Cartan transport has the form

\[
\xi\longmapsto P_\gamma\xi+\Delta_\gamma.
\]

It composes in an affine semidirect-product group. The homogeneous linear part is ordinary parallel transport and therefore isometric; the inhomogeneous development vector is not a linear map of the type accepted by `\delta_{\mathrm{RF}}`.

### 6.7 Strain and polar constructions

`C_A=A^\dagger A` and any polar factor require a prior cross-fibre map `A`. Endpoint metrics alone do not define one. A coordinate or frame identification can be inserted, but then the result depends on that insertion. In indefinite signature, square-root and polar branches can also fail or become nonunique at spectral degeneracies. These methods can analyze an arrow; they do not own it.

### 6.8 The sharp natural-connection result

There is a genuine first-order theorem: in dimension four, a diffeomorphism-natural connection depending only on the first jet of a pseudo-Riemannian metric is the Levi-Civita connection. Therefore a local, first-order, metric-natural path functor gives only isometric transport and zero reciprocal-root depth.

That theorem does **not** extend to arbitrary finite order. Let

\[
S=\operatorname{Ric}^{\sharp},
\qquad
\alpha=dR,
\]

and for any real constant `c` define

\[
\boxed{
\nabla^{(c)}_X Y
 =\nabla^g_XY
 +c\bigl[\alpha(X)S(Y)+\alpha(Y)S(X)\bigr].
}
\]

The added term is a diffeomorphism-natural symmetric `(1,2)` tensor built from curvature jets. Hence `\nabla^{(c)}` is a globally defined torsion-free natural connection, generally non-metric. Its parallel transport is an exact path functor.

For

\[
g=-dt^2+(1+t^2)^2dx^2+dy^2+dz^2,
\]

one obtains

\[
R=\frac4{1+t^2},
\qquad
\operatorname{Ric}^{\sharp}
 =\operatorname{diag}\left(\frac2{1+t^2},\frac2{1+t^2},0,0\right).
\]

Along the `t`-curve from `0` to `1`, for the flag spanned by the clock `\partial_t` and ruler `\partial_y`, the transport gives

\[
\ell_t=6c,
\qquad
\ell_r=0,
\qquad
\delta_{\mathrm{RF}}=-3c.
\]

Every `c` gives a different metric-natural, compositional, non-isometric arrow rule on this example. For sufficiently short paths the transported timelike line remains timelike, so these are genuine arrows of the causal groupoid.

### 6.9 Sharp conclusion about `A`

The strongest justified statement is not that every metric-natural path functor is isometric. That statement is false.

The sharp result is:

1. **First-order, local, diffeomorphism-natural connection:** uniquely Levi-Civita, hence isometric and depth-trivial.
2. **Higher-order metric-natural connection:** infinitely many non-metric functors exist; naturality and composition do not select one.
3. **Nonlocal/path-history functor:** the source premises do not classify or select these either.

Therefore the metric does not own a unique physical non-isometric `A`. Choosing one of the higher-order connections is itself a new comparison law, not a derivation forced by the metric.

---

## 7. `c_eff` consistency

The reciprocal-root cocycle defines the positive multiplicative character

\[
\Lambda_{\mathrm{RF}}(A,F)
 =e^{-2\delta_{\mathrm{RF}}(A,F)}
 =\frac{\rho_1(A,F)^2}{\rho_2(A,F)}.
\]

On the pure reciprocal subgroup this gives `e^{-2t}`, exactly matching the required reduction.

As mathematics, `\Lambda_{\mathrm{RF}}` is a consistent transport multiplier or one-dimensional groupoid representation. It is not automatically a ratio of an ordinary scalar on the unscaled flag objects.

Indeed `D_t` preserves the standard flag, so it is an isotropy arrow. For any scalar `C` on objects,

\[
\frac{C\bigl(t(D_t,F)\bigr)}{C\bigl(s(D_t,F)\bigr)}=1,
\]

because source and target are the same object. But

\[
\Lambda_{\mathrm{RF}}(D_t,F)=e^{-2t}\ne1.
\]

Equivalently, `\delta_{\mathrm{RF}}` is not an endpoint coboundary because it has a nonzero isotropy character.

Therefore the mixed relation

\[
\frac{c_{\mathrm{eff}}(q)}{c_{\mathrm{eff}}(p)}
 =e^{-2\delta_{\mathrm{RF}}(A,F)}
\]

has the following status:

- **not derived from the complete metric;**
- **consistent as a definition of transport in a reciprocal calibration line/local system;**
- **not a literal endpoint-scalar ratio on the present flag object space;** and
- **physically open while the arrow and calibration state are unowned.**

To make it an endpoint ratio, one must enrich objects with a reciprocal calibration scale so `D_t` moves the object, restrict to a subgroupoid on which the character has zero isotropy periods, or choose a global trivialization of the associated line system when one exists. None of these is supplied by the current flag alone.

---

## 8. Global and degenerate strata

On its open domain the cocycle is smooth and finite. Write

\[
\delta_{\mathrm{RF}}
 =\frac12\log\rho_2-\log\rho_1
 =\frac12\log\left(\frac{\rho_2}{\rho_1^2}\right).
\]

### 8.1 Null clock line

When the transported clock line approaches null, `\rho_1\to0`. The arrow reaches the boundary of `\mathcal G_g`; the target is no longer a causal-flag object. If `\rho_2` tends to a nonzero value, `\delta_{\mathrm{RF}}\to+\infty`. If `\rho_2` also tends to zero, the outcome depends on the relative rate and may be finite, `+\infty`, `-\infty`, or path-dependent. There is no universal continuous extension across the null boundary.

### 8.2 Degenerate clock-ruler plane

A plane containing a timelike line cannot be degenerate. Therefore plane degeneracy can occur only at or beyond the boundary where the clock line loses timelikeness. It is not an independent interior stratum.

### 8.3 Ruler ambiguity

Given both `L` and `P`, the metric selects a unique spacelike ruler line

\[
R=P\cap L^{\perp_g}.
\]

The ambiguity is in selecting `P` from `L`: there is a sphere of possible ruler directions in the clock rest space. The cocycle does not resolve that choice.

### 8.4 Multiple paths and holonomy

If a path is part of the arrow, distinct paths are distinct arrows and may carry different flags and depths. Endpoint-only descent occurs exactly when the cocycle has zero value on every admissible loop. The reciprocal-root character is not automatically loop-trivial.

### 8.5 Coincidence

The identity arrow has depth zero. Any smooth local comparison law with `A\to I` and continuously transported flag has `\delta_{\mathrm{RF}}\to0` at coincidence. Coincidence alone does not force this if the selected arrow has discontinuous holonomy or calibration jump.

### 8.6 Cut locus

The algebraic causal-flag groupoid has no cut locus. Cut-locus behavior enters only when an arrow-selection rule chooses endpoint geodesics or an exponential inverse. At a cut point there may be multiple branches; at conjugate points `d\exp` becomes singular.

### 8.7 No global flag section

The groupoid exists globally over the total causal-flag bundle without any section. Assigning one flag to every observer/event is a reduction of the Lorentz frame bundle and need not exist globally, especially for the additional spacelike ruler line. A pair-relative or path-relative flag avoids a global preferred congruence but requires a compositional state-update rule and may acquire holonomy.

### 8.8 Causal exit under non-metric transport

A non-metric connection can transport a timelike line through the null cone. The corresponding path action is then only partial: it is defined until the first causal exit. To obtain a genuine path groupoid over causal flags, admissible path-state pairs must be restricted to those for which the transported line remains timelike at every subdivision point.

---

## 9. Final determination

The reciprocal-root formula survives the adversarial audit as a mathematically exact cocycle on a properly typed open causal-flag groupoid. Its strongest theorem is a conditional uniqueness result for universal order-zero natural cocycles after a formal clock/ruler channel involution is added.

It does **not** yet constitute the missing UDT observer-pair rule, for four independent reasons:

1. the physical observer query has not been shown to supply the causal flag;
2. the complete exchange involution is an added coefficient-system postulate, not a causal Lorentz exchange derived from `K`;
3. the metric does not select a unique non-isometric comparison-arrow functor; and
4. the proposed `c_eff` factor is a nontrivial transport character, not an endpoint scalar ratio on the unscaled flag objects.

The smallest remaining joint after accepting the readout is therefore a **typed comparison-state and arrow-selection premise**: specify the pair-relative flag, its functorial update through intermediate observers, the non-isometric metric/coframe/path rule that generates `A`, and the reciprocal calibration object on which the exchange and `c_eff` character act. This is kinematic/measurement structure. It need not be an action or matter model, but it is not contained in the two founding reciprocal equations as presently stated.

---

## 10. Runnable exact algebra

The companion script `verify_reciprocal_flag_followup.py` checks:

1. `D(t)^T K D(t)=K`, `KD(t)K=D(-t)`, and the anti-isometry of `K`;
2. the three-dimensional abelianization of the `(1,1,2)` flag parabolic;
3. graded-volume factors and exact telescoping;
4. the unique exchange-odd normalized coefficient vector;
5. the exact lower-mixing value `\frac14\log(64/3)`;
6. noncomposition of `d\exp` blocks and composition of the full Jacobi propagator;
7. the explicit higher-order natural-connection counterfamily; and
8. the `c_eff` endpoint-scalar obstruction.

Run with:

```bash
python verify_reciprocal_flag_followup.py
```

It requires only SymPy.
