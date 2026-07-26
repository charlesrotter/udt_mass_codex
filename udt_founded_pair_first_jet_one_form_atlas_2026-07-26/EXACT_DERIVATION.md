# Exact derivation

## 1. Complete first-jet decomposition

For a unit timelike `u` and orthogonal unit spacelike `n`, define the screen projector `s`. Unit norm
and orthogonality imply

```text
nabla_a u = omega_a n + U_(aA) e_A,
nabla_a n = omega_a u + N_(aA) e_A.
```

Here `A` is a screen index and

```text
omega_a=n dot nabla_a u=-u dot nabla_a n.
```

The component count is exact:

```text
omega: 4,
U:     4 x 2 = 8,
N:     4 x 2 = 8,
total: 20.
```

This is the tangent space of a smooth orthonormal ordered pair field. It is not a count of UDT
propagating modes.

## 2. Why there are exactly 22 one-form motifs

Under screen `SO(2)`, spacetime covectors decompose into two scalar axes `(u,n)` plus one screen-vector
representation.

The pair-boost covector `omega` supplies:

- four maps between its two scalar components and the two scalar output axes; and
- two screen maps, identity and the screen Hodge rotation.

That gives six.

Each of `U` and `N` decomposes into two screen vectors, one screen trace, one screen twist, and a
spin-two part. The two input screen vectors each map to the output screen by identity or Hodge
rotation, giving four maps. Trace and twist each multiply either `u_flat` or `n_flat`, giving four
more. The spin-two component has no linear map to a covector without extra screen data. Thus each
sector gives eight:

```text
6 + 8 + 8 = 22.
```

The explicit 80-by-22 map matrix has exact rank 22.

If screen orientation is not supplied, the Hodge and twist maps are unavailable. The `O(2)` count is

```text
5 + 4 + 4 = 13.
```

If one also requires invariance under ruler-axis reversal `n -> -n`, 11 of the 22 `SO(2)` maps remain.
Requiring both orientation freedom and ruler-axis invariance leaves six:

```text
W02, W03, U01, U05, N03, N06.
```

These reductions classify conventions. Current UDT has not selected either convention as the global
physical rule, and neither reduction leaves a unique form.

## 3. No zero-jet scalar supplies the depth

Every algebraic scalar made only from the normalized pair Gram data is a function of

```text
u dot u=-1,
n dot n=+1,
u dot n=0.
```

Their differentials vanish identically. Consequently no nonconstant scalar potential can be obtained
at zero derivative order from `g,u,n` alone.

## 4. Generic closure test

Every first-jet candidate can be integrated along a path and then reverses sign when the path is
reversed. The decisive additional question is whether its exterior derivative vanishes identically,
so that it supplies an endpoint depth without further equations or branch restrictions.

The test uses exact valid pair fields in flat metric:

```text
F(x)=exp(K(x)),
K(x)=x^a A_a + 1/2 x^a x^b B_ab,
u(x)=F(x)e_0,
n(x)=F(x)e_1,
```

with `A_a` and symmetric `B_ab` in `so(1,3)`. These fields obey both unit norms and orthogonality
through the tested second jets; they are not arbitrary inconsistent derivative tables.

For each candidate one-form, compute all six components of its exterior derivative at the origin.
Four production witnesses give a 24-by-22 exact matrix of rank 22. Six independently generated
rational witnesses give a 36-by-22 matrix of rank 22. Therefore the common nullspace is zero:

```text
no nonzero linear combination of the 22 maps is closed for every smooth orthonormal pair field,
even within this flat-metric witness class.
```

This is a bounded universal-identity refutation. A field equation, special branch, or global reduction
may still make a particular combination closed.

## 5. The tempting boost connection

The complete pair-boost one-form is

```text
omega = -W01 + W04 + W05.
```

If the pair varies only by boosts in its own `SO(1,1)` plane,

```text
F(x)=exp(chi(x) K_01),
```

then

```text
omega=dchi.
```

This is a genuine conditional exact line. But `K_01` is metric-skew: it is observer-frame rapidity.
The founded reciprocal generator is metric-self-adjoint: it changes the calibrated clock/ruler
readout reciprocally. Prior audits explicitly distinguish these objects. Current UDT supplies no
identity `chi=phi`, and general pair fields activate the angular terms that make `omega` nonclosed.

The boost-only result is therefore a useful control, not the missing founded law.

## 6. Historical conformal-connection route

The July 21 GR-subtraction audit found an exact conditional route in which a torsion-free conformal
connection, a complete reciprocal realization, and a full two-pair angular extension give a unique
Weyl one-form and, in the tested diagonal class, `A=dphi`.

That algebra remains valid in its recorded premises. It is not active authority now:

- strong local CSN is `CHALLENGED_OWNER_POSTULATE_NOT_DERIVED` and inactive;
- the complete two-pair reciprocal realization is conditional and unselected; and
- torsion-free conformal compatibility is comparison structure, not a currently founded UDT physical
  connection.

The historical route is therefore `CONDITIONAL_INACTIVE`, not a current first-jet selector.

## 7. Current selector rank

Reciprocity derives the pair character and its composition, but supplies no current tensor operation
selecting one coefficient vector in the 22-dimensional atlas. Observed `c_E` calibrates clock and
length units, while `G_obs` is a scalar anchor; neither chooses a one-form direction or enforces
closure. Finite-cell and bootstrap records do not supply the missing global pair field or differential
condition.

Thus the local first-jet vocabulary is fully mapped but not selected. The next honest test is global
and branch-conditioned: determine whether an already registered complete branch actually supplies a
smooth founded pair field and reduces this vocabulary to a closed line across its full finite cell.
