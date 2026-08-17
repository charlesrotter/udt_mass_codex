# G129 exact derivation — co-present pair-network faithfulness

Date: 2026-08-16

## 1. Type correction

Let `V` be one four-dimensional tangent space and let `g` be a Lorentzian symmetric bilinear form.
A calibrated observer-pair query at the event supplies an injective pair differential

\[
A_a:\mathbb R^2\longrightarrow V
\]

and the complete pair metric

\[
h_a=A_a^TgA_a.
\]

The terminal reciprocal kernel then reads

\[
\phi_a=\frac14\log\frac{-\det h_a}{(h_a)_{00}^2},\qquad
\frac{c_{{\rm eff},a}}{c_E}=e^{-2\phi_a}.
\]

The network-reconstruction question must use the full `h_a`, not only its terminal scalar.

## 2. Pointwise faithfulness theorem

For a declared family `A={A_a}`, define

\[
\mathcal M_A:\operatorname{Sym}^2(V^*)
\longrightarrow
\bigoplus_a\operatorname{Sym}^2((\mathbb R^2)^*),
\qquad
\mathcal M_A(k)_a=A_a^TkA_a.
\]

### Theorem

The complete pair-metric network determines `g` uniquely at the event if and only if

\[
\ker\mathcal M_A=\{0\}.
\]

In four dimensions this is equivalent to rank ten for any matrix representation of
`mathcal M_A`.

### Proof

If two metrics `g` and `g_tilde` give the same pair pullbacks, then

\[
\mathcal M_A(g-\widetilde g)=0.
\]

Injectivity therefore gives `g=g_tilde`. Conversely, if nonzero `k` lies in the kernel, then

\[
A_a^T(g+\epsilon k)A_a=A_a^TgA_a
\]

for every declared pair plane. Lorentz signature is an open condition, so sufficiently small
nonzero `epsilon` leaves `g+epsilon k` Lorentzian. The network is then nonfaithful. This proves both
directions.

The criterion is frame independent: an invertible ambient basis change conjugates `g` and all
`A_a` while leaving every pullback unchanged, and it composes `M_A` with invertible linear maps on
its domain. Its rank cannot change.

## 3. Six clock–ruler planes suffice

Choose a clock vector `e0` and spatial basis `e1,e2,e3`. Use ruler directions

\[
e_1,\ e_2,\ e_3,\ e_1+e_2,\ e_1+e_3,\ e_2+e_3.
\]

The first three pair metrics directly return

\[
g_{00},\quad g_{0i},\quad g_{ii},\qquad i=1,2,3.
\]

For each `i<j`, the ruler-ruler entry on the sum direction gives

\[
g(e_i+e_j,e_i+e_j)=g_{ii}+2g_{ij}+g_{jj},
\]

so

\[
g_{ij}=\frac12\left[g(e_i+e_j,e_i+e_j)-g_{ii}-g_{jj}\right].
\]

All ten components are therefore reconstructed. The executable design matrix has exact rank ten,
and a generic rational Lorentz metric is recovered without approximation.

This six-plane set is a sufficiency witness, not a theorem that six is the unique or globally
minimal physical query family.

## 4. Exact rank-deficient counterexample

The three axial clock–ruler planes `span(e0,ei)` have rank seven. Their kernel is exactly

\[
\operatorname{span}\{e^1\odot e^2,\ e^1\odot e^3,\ e^2\odot e^3\}.
\]

Thus they miss the three spatial cross terms.

The failure is not merely pointwise bookkeeping. On coordinates `(t,x,y,z)`, compare Minkowski
space with

\[
g_a=-dt^2+dx^2+dy^2+dz^2+2az^2\,dx\,dy,
\qquad |az^2|<1.
\]

Every axial clock–ruler pullback is identical to the Minkowski pullback, because no axial plane
contains both `dx` and `dy`. But direct Christoffel and Ricci reconstruction gives at `z=0`

\[
R_{xy}=R_{yx}=-a,
\qquad
R_{\mu\nu}R^{\mu\nu}=2a^2.
\]

For `a` nonzero this germ is not locally isometric to Minkowski space. A rank-deficient pair
network can therefore hide genuine curvature, not merely a coordinate representative.

## 5. Regular overlap descent

Let regular observer charts `F_i:U_i->M` have full pullback metrics `H_i=F_i^*g`. On a common-event
overlap define

\[
f_{ji}=F_j^{-1}\circ F_i,
\qquad D_{ji}=df_{ji}.
\]

The already banked G123 identities are

\[
f_{ki}=f_{kj}\circ f_{ji},
\qquad
D_{ji}^TH_jD_{ji}=H_i.
\]

Suppose each local pair network has rank ten. Section 2 reconstructs one and only one `H_i` on
each chart. Pullback covariance makes those tensors agree on every overlap, so the standard tensor
descent construction defines one Lorentz metric on the regular quotient manifold. Any second
realization of the same chart, transition, and pair-pullback data is related chartwise by the
identity data and hence by the induced global isometry.

This is conditional on a regular Hausdorff second-countable quotient. It does not classify
nontransverse incidence fibers, caustics, cut loci, topology change, or branch aggregation.

## 6. Terminal reciprocal depth is not faithful by itself

Consider

\[
h_1=\begin{pmatrix}-1&0\\0&1\end{pmatrix},
\qquad
h_2=\begin{pmatrix}-1&1/2\\1/2&3/4\end{pmatrix}.
\]

Both are regular Lorentzian pair metrics and both give

\[
\frac{-\det h}{h_{00}^2}=1,
\qquad \phi_{\rm pair}=0,
\qquad c_{\rm eff}/c_E=1,
\]

but `h1` and `h2` are distinct calibrated pair metrics even with the same `h00=-1` clock
normalization. The terminal reciprocal scalar forgets shift/common-scale allocations retained by
the complete pair metric. Thus a network of terminal `c_eff` values is not the complete relational
network.

## 7. Quiet overlap and endpoint behavior do not force continuation

Let `phi0(x)` be any smooth profile with the desired quiet region and registered asymptotic
behavior. Define the standard smooth bump

\[
b(x)=
\begin{cases}
\exp\!\left[-\dfrac1{(x-1)(2-x)}\right],&1<x<2,\\
0,&\text{otherwise}.
\end{cases}
\]

The standard limit `u^{-n}exp(-1/u)->0` as `u->0+` for every finite `n` proves that all derivatives
of `b` vanish at `x=1,2`; hence `b` is smooth. The executable checks its support and a nonzero
interior value as a sampled regression; the all-orders claim is this analytic proof. Then

\[
\phi_1=\phi_0+b
\]

agrees with `phi0` throughout the quiet interval `[-1,1]`, has the same behavior at both extremes,
and differs on `(1,2)`. The construction can be placed in any unpinned interval.

Therefore a GR-like quiet overlap plus reciprocal asymptotic behavior is a strong boundary pattern,
but not a unique-continuation theorem. Rigidity would require an additional already-owned equation,
analyticity condition, or global relational restriction. G129 introduces none.

## 8. Exact interpretation

The result removes one ambiguity and preserves another:

\[
\boxed{
\text{rank-complete compatible observer network}
\Longleftrightarrow
\text{one metric on the covered regular region, up to isometry}
}
\]

So an already complete co-present relation network does not need a separate history selector. Its
full pair data reconstruct the metric.

However, the founding reciprocal character and terminal kernel do not yet supply the numerical
values of that entire rank-complete network. They tell every supplied pair metric how to yield
`phi_pair` and `c_eff/c_E`; they do not make terminal scalar data faithful or prove a unique global
continuation from a quiet patch and endpoint limits.

The smallest remaining question is therefore not “which test history wins?” It is:

> Does the founding meaning of co-presence own a rank-complete, globally compatible family of full
> calibrated pair metrics and its values, or only require consistency once that family is supplied?

That is a premise-ownership/global-extension question, not a request for a new angular mechanism,
preferred path, scalar `mu`, or metaphysical universe selector.
