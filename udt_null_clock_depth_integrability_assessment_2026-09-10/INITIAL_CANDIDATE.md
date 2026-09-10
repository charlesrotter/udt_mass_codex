# NCI1 — when null-clock depth admits one endpoint scalar

Frozen candidate, 2026-09-10. **CONDITIONAL MATHEMATICAL APPLICATION; UNPROMOTED; review pending.**
Source snapshot: `a62f3cc52b94b1029092227b5feda7b7ee154486`.
This is an application/reconstruction of a known geometric criterion, not a new mathematical discovery
or a UDT response law. Preserve this initial text if a repair is needed.

## 1. Exact question and inputs

Supply a smooth time-oriented Lorentzian four-manifold of signature `(-,+,+,+)`, a connected open
domain O, and a smooth future metric-unit timelike vector field U on O. Its integral curves are the
supplied observer family; they need not be geodesic, hypersurface orthogonal, or physically populated.
Use units in which proper-clock tangent normalization is `g(U,U)=-1` (no choice of a physical scale).

For each sufficiently short future affinely parametrized null geodesic segment gamma:A→B wholly
within O, set `omega=-g(U,k)>0`. The G220 clock query has

```
r_AB = d tau_B / d tau_A = omega_A / omega_B,
delta_AB = -log r_AB = log(omega_B/omega_A).
```

Each segment is considered on its own regular local branch, with endpoint observers integral to U.
All future null directions at every event and arbitrary sufficiently short subsegments are included.
This is a quantifier in a property being tested, not an assertion that Nature realizes all queries.

**Property P:** there is one smooth real scalar Psi on O such that, for every such segment,

```
delta_AB = Psi(B)-Psi(A).
```

Psi belongs to this supplied `(g,U)` and is not an independently adjustable scalar for each edge.
The general UDT pair kernel need not satisfy P. For a supplied single edge G220 already evaluates
delta without P, a new coefficient, or a new law. Choosing an observer family/path is ordinary query
data; requiring all geometries to possess P would be an additional restriction, not adopted here.

## 2. Criterion

Put `f=exp(-Psi)>0`, `xi=f U`. Property P is equivalent to

```
nabla_(a xi_b) = psi g_ab                         (CK)
```

for a smooth scalar psi; parentheses include division by two. Thus the observer direction must admit
a positive multiplier making it conformal Killing. This is not the condition that the metric be flat
or that U itself be Killing.

For a directly computable version define

```
h_ab = g_ab + U_a U_b,
a_b = U^a nabla_a U_b,
H = (nabla_a U^a)/3,
sigma_ab = h_a^c h_b^d nabla_(c U_d) - H h_ab,
alpha = a_flat - H U_flat.
```

Then the exact **global** criterion on O is

```
sigma=0 and alpha is exact;    d log f = alpha,    d Psi = -alpha.       (I)
```

The exact **local** criterion in a neighborhood of each point is `sigma=0, d alpha=0` there.
On a simply connected O, closed alpha is sufficient for global exactness. In general all periods
must vanish as well; closed is not silently substituted for exact. If it exists, Psi is unique up
to one additive constant on connected O. No zero-vorticity requirement is inserted.

## 3. Argument, independent of a metric field equation

P says precisely that `f omega` is constant along every included null segment. Metric compatibility
and `nabla_k k=0` give

```
d[g(xi,k)]/d lambda = k^a k^b nabla_(a xi_b).
```

Consequently CK implies P. Conversely P makes the displayed quadratic contraction zero for every
future null tangent at every point. Here the all-direction quantifier is essential.

For completeness, take an orthonormal frame and a symmetric matrix S with `S(k,k)=0` for all
`k=(1,n)`, `|n|=1`. The directions `n=+/-e_i` give `S_0i=0` and `S_ii=-S_00`.
The directions `n=(e_i+e_j)/sqrt(2)` then give `S_ij=0`, i≠j. Hence S is proportional to eta.
Applied to `S=nabla_(a xi_b)`, this proves CK without assuming Einstein dynamics or a matter action.

To establish I, use the unit-congruence identity

```
nabla_a U_b = -U_a a_b + H h_ab + sigma_ab + vorticity_ab.
```

With `b=d log f`, its symmetric part gives

```
f^-1 nabla_(a(f U_b)) = H h_ab + sigma_ab + U_(a(b_b)-a_b)).
```

Spatial trace-free projection of CK forces sigma=0; spatial trace gives `psi=f H`.
The time-space and time-time projections then give `b=a_flat-H U_flat=alpha`.
Conversely these conditions substitute back to CK. They fix d log f; integration proves the local,
global and additive-constant claims above. Smooth regularity suffices for the differentiations and
local null-geodesic existence used here; no analyticity, PDE development or stability is asserted.

## 4. What direction dependence tests

Write each future null tangent `k=omega(U+n)`, with n a unit spatial vector. Direct contraction yields

```
(1/omega) d log omega/d lambda = -H - a·n - sigma(n,n).                 (D)
```

A scalar endpoint gradient has only `U(Psi)+n·D(Psi)` on the same directional sphere. The shear term
is a trace-free quadratic directional contribution; it cannot be represented by a single scalar
gradient for all n unless sigma=0. The remaining assignments are `U(Psi)=-H`, `D(Psi)=-a`;
alpha-exactness is what makes these assignments derivatives of one scalar throughout the domain.
Small or vanishing shear at one event alone does not prove a neighborhood/global potential.

## 5. Controls and a cosmological scope distinction

These are analytical checks of the criterion, not new physical choices or a statistical sample.

1. **Original static metric:** for `g=-exp(-2 phi(r)) dt^2+exp(2 phi(r)) dr^2+r^2 dOmega^2`,
   static `U=exp(phi) partial_t` and arbitrary smooth phi, take `f=exp(-phi)`. Then xi=partial_t
   is Killing and `Psi=phi` recovers G220/G271. Work on the regular finite-radius chart. No field
   equation or phi profile is selected. Nonzero transported screen mismatch can still occur (G271).
2. **Conformal time dependence:** for `g=A(t)^2 eta`, A>0, `U=A^-1 partial_t`, take f=A.
   Then xi=partial_t is conformal Killing and `Psi=-log A`. Time dependence and expansion alone
   do not obstruct P. This is a supplied metric control, not a cosmological evolution law.
3. **Shear in exactly flat geometry:** take Minkowski g and
   `U=cosh(kappa x) partial_t+sinh(kappa x) partial_x`, with kappa≠0.
   At x=0, `a=0`, `H=kappa/3` and spatial sigma has diagonal `(2,-1,-1) kappa/3`.
   The directional clock-depth slope is `-kappa n_x^2`. No scalar gradient fits all directions.
   The same flat metric with constant U does satisfy P; this is observer-dependent, not UDT failure.
4. **Shear-free is insufficient:** on a positive-lapse open patch take
   `g=-(1+t x)^2 dt^2+dx^2+dy^2+dz^2`, `U=(1+t x)^-1 partial_t`.
   This metric is flat (verify its full Riemann tensor), sigma=H=0, but
   `alpha=t/(1+t x) dx` and `d alpha=(1+t x)^-2 dt wedge dx !=0`.
   P therefore fails even without shear. This is a supplied accelerating observer family in flat
   geometry, not a proposed metric law, source model or counterexample to UDT.

In the broader supplied diagonal homogeneous family
`g=-dt^2+sum_i A_i(t)^2 (dx^i)^2`, U=partial_t, put `H_i=A_i'/A_i`.
Here a=0, `H=(H_1+H_2+H_3)/3`, and sigma has orthonormal diagonal `H_i-H`.
Thus P holds locally exactly when all three H_i agree, equivalently `A_i=c_i A(t)` on a connected
time interval. The positive constants c_i are legitimate supplied spatial normalizations, not a
selected scale; no Einstein equation is used. Otherwise the depth remains a valid directional/path
query and cannot universally be compressed into one endpoint scalar for these comoving observers.
This is a criterion for a representation, not a requirement of isotropic expansion in UDT.

## 6. Source join and maximum conclusion

- G176 supplies the provisional completed-pair typing, not a universal physical null protocol.
- G215's supplied shared comparison-clock trivialization is a stronger antecedent than unit U.
- G216–G217 give the invariant proper-clock slope/first jet; no additional clock coefficient.
- G220 derives that slope for each supplied regular null branch.
- G138's graph cycle criterion and G247's path-labelled chain semantics remain intact.
- NCI1 tests when all these particular local null slopes can share one endpoint scalar. It does not
  repair accepted science, impose that compression, eliminate full frame/screen carry, select a
  congruence, determine a metric history, or identify physical light/carried content.

No claim of novel mathematics: Dirmeier, Plaue and Scherfner, *On Conformal Vector Fields Parallel
to The Observer Field*, arXiv:0802.3642v2, propositions 3.1–3.2, treat the related classical
redshift-potential criterion. We give the local/global distinction and the complete direct proof in
the repository's sign conventions; no parallax or physical-light conclusion is imported.
Primary method source: https://arxiv.org/pdf/0802.3642v2 .

**Maximum conclusion:** a conditional geometric compatibility criterion connecting existing
null-query depths to a single endpoint scalar, with necessary-and-sufficient conditions for the
declared supplied `(g,U)` class. It is neither native dynamical closure nor evidence that new physics
is required. The metric and observer data remain free; physical query realization remains open.
