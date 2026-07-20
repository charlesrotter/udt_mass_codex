# Clock–Curvature Selector Audit

Date: 2026-07-19  
Preregistered base: `674641832fe449c6fbe4a1a8ae6e6d949fd686cc`  
Preregistration commit: `39b8e0a31a09f99fa2179a7c031d518de1e8e66e`  
Status: **VERIFIED-WITH-CAVEATS** — exact derivation and an independent direct-tensor replay pass; no fresh external-model review was authorized.

## Result first

The WR–L clock–curvature identity is real and mathematically strong, but it is not presently a native UDT field equation.

Within the complete static spherical reciprocal areal family tested here, **if** one supplies the equation

`D_h^2 N + (R4/6)N = 0`,

then a finite normalized seat and one finite wall select

`A(r)=1-r/X`

uniquely. That is `UNIQUE-CONDITIONAL`: the equation is the missing premise that performs the selection.

Current Reciprocity, CSN, finite-cell endpoints, and bootstrap do not supply it. A nearby reciprocal finite-cell metric satisfies the enumerated endpoint and wall properties while violating the equation, and a general local CSN transformation does not preserve the equation's zero set. The identity can therefore remain a **post-scale conditional selector candidate**, after a physical representative and static clock direction have been selected. It cannot yet be promoted to an unconditional pre-scale law.

## Exact general-family reduction

Take the bounded metric family

`ds^2=-A(r)c^2dt^2+A(r)^(-1)dr^2+r^2dOmega^2`, `N=sqrt(A)`.

Direct curvature calculation gives

```
R4 = -A'' - 4A'/r + 2(1-A)/r^2,
R3 =       - 2A'/r + 2(1-A)/r^2,
D_h^2 N = N(A''/2 + A'/r).
```

Consequently

```
D_h^2 N + (R4/6)N = (N/3) [A''+A'/r+(1-A)/r^2],
D_h^2 N + (R3/4)N = (N/2) [A''+A'/r+(1-A)/r^2].
```

The two forms are exactly equivalent in this family; the second is `3/2` times the first. Both vanish only when

`A''+A'/r+(1-A)/r^2=0`.

Its general solution is

`A=1-a r-b/r`.

A finite normalized seat removes `b/r`; placing one wall at `r=X` sets `a=1/X`. Thus the supplied clock–curvature equation selects WR–L. This does not derive the equation itself.

## Bounded non-entailment countermetric

The preregistered deformation is

`A_epsilon=(1-r/X)[1+epsilon(r/X)(1-r/X)]`.

For the explicitly tested member `epsilon=1/2`:

- the temporal and radial factors remain reciprocal;
- `A(0)=1` and `A(X)=0`;
- `A>0` throughout the open cell;
- the wall zero is linear with the same leading coefficient as WR–L;
- its `1/r` seat-curvature class is volume-integrable, as WR–L's is;
- no carrier, source, action, or imported GR equation is used.

But its profile residual is

`2 epsilon (4r-3X)/X^3`,

which is not zero. At `epsilon=1/2`, `r=X/2`, it is `-1/X^2`.

This proves non-entailment from the enumerated reciprocal representative plus finite-cell endpoint data. It is not called a complete-foundation counterexample: it does not satisfy the separate WR–L residual-recentering/profile axiom, and complete action, source, differentiable boundary completion, and bootstrap equations remain open. The exact lesson is that one of those additional structures would have to supply the profile equation.

## Common-Scale audit

Under the local common rescaling

`g' = exp(2 sigma) g`, `N'=exp(sigma)N`,

the four-dimensional clock–curvature residual transforms as

`E4' = exp(-sigma)[E4 + 2 grad(sigma).grad(N) + N |grad sigma|^2]`.

Therefore `E4=0` is preserved by a constant rescaling, but not by a general local CSN transformation. An explicit `sigma=k r/X` transformation of WR–L produces

`-k N/X^2 + k^2 N^3/X^2`,

which is nonzero generically.

Nor can a coefficient change repair the simple spatial form. For

`E_a=D_h^2N+a R3 N`,

the transformed expression contains the unavoidable term

`3 grad(sigma).grad(N)`.

No value of `a` removes it. This is a fail-closed result for this simple operator class, not a proof that no more elaborate weighted or compensated covariant operator exists. Inventing such an operator is not authorized.

## Covariant meaning and missing structure

After a physical static representative and its unit clock direction `u` are supplied, the equation is the scalar contraction

`(R_mu_nu - R g_mu_nu/6) u^mu u^nu = 0`.

This explains why the identity is geometrically meaningful and why it is not automatically a pre-scale law: the physical representative and clock congruence are part of what remains to be selected. The equation does not choose those structures by itself.

The smallest genuinely missing selector exposed here is therefore:

> a native rule that selects the physical CSN representative/static clock direction and supplies—or implies—the clock–curvature condition without importing an action equation.

Finite-cell endpoints constrain the selected solution but do not provide that interior rule. Current bootstrap is on-shell closure/admissibility and does not provide it either.

## Status rulings

- Reciprocal kinematics: `DERIVED` in its registered scope.
- WR–L clock–curvature identity: `DERIVED` on WR–L.
- Clock–curvature equation as WR–L profile selector: `UNIQUE-CONDITIONAL` in the static reciprocal spherical areal family.
- Reciprocity or finite-cell endpoints forcing the equation: `NOT_DERIVED`.
- Pre-scale local-CSN covariance of the equation as written: `REFUTED`.
- Post-scale physical-representative use: `CONDITIONAL_LEAD`.
- Bootstrap derivation of the equation/representative: `OPEN`.
- Complete action, native source, carrier emergence, differentiable boundary action, normalized charge, unconditional mass, and `X_max`: `OPEN`.

## Four banking gates

1. **Preregistered:** yes, commit `39b8e0a` before the derivation and countermetric evaluation.
2. **Full space or bounded scope justified:** complete arbitrary-`A(r)` static spherical reciprocal areal family; nonspherical, rotating, time-live, nonzero-shift, matter-coupled, and global topology sectors are explicitly not covered.
3. **Independently verified:** yes in-package, by a separate direct Christoffel/Ricci tensor implementation plus 12 exercised catch-proofs. Fresh external-model review was not authorized.
4. **Every premise audited:** yes for the bounded claim; unresolved complete-foundation premises prevent stronger countermodel and native-law language.

Maximum banked status: **VERIFIED-WITH-CAVEATS**.

