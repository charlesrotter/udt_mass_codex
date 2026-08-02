# Exact branchwise projector derivation

## 1. Typed object

On each frozen complete twisted-`S3` configuration C01--C06, the parent metric audit derives an
unoriented timelike clock line `u` and, from the nonzero twist of that same intrinsic line, an
unoriented spacelike ruler line `n`.  Their signs cancel from the projectors.  The clock-orthogonal
bundle

```text
E = u perpendicular,             rank(E)=3, positive metric,
P = n tensor n_flat,             rank(P)=1,
Q = I_E-P,                       rank(Q)=2
```

is therefore intrinsic to each named configuration.  It is not the conditional celestial `S2`
fiber and it is not the posited particle carrier.

The metric supplies the projected connection on `E`; write it as `D`.  The relative curvature of
the rank-one reduction is

```text
Omega_rel(X,Y) = Q [(D_X P),(D_Y P)] Q.
```

This is kept separate from the ambient term `Q R_D Q` in the curvature of the induced connection.

## 2. Exact north-event reconstruction

The frozen profile has left-invariant north-event derivatives `(1,2,3)/50`.  In the registered
coframe ordering,

```text
p1=3/50, p2=1/50, p3=2/50,
twist=1/64, kappa=-2,
lambda in {-2,-1,0,1/2,1,2}.
```

`derive_branchwise_projector_gates.py` independently reconstructs the Cartan structure coefficients,
the exact Levi-Civita matrices, `D_a P=[Gamma_a|_E,P]`, and every two-direction commutator.  For the
screen `Q=diag(0,1,1)`, one nonzero exact component is:

| configuration | `lambda` | `(Omega_rel(E2,E3))_12` |
|---|---:|---:|
| C01 | -2 | `634/625` |
| C02 | -1 | `2509/2500` |
| C03 | 0 | `1` |
| C04 | 1/2 | `10009/10000` |
| C05 | 1 | `2509/2500` |
| C06 | 2 | `634/625` |

One nonzero component at one regular event proves only that the relative projector curvature is not
identically zero on that complete configuration.  It does not establish an integral, an extremum,
stability, or an equation of motion.

The independent verifier reconstructs the same Cartan and commutator algebra using only standard-
library `Fraction`; it imports neither SymPy nor the production module.  All six fractions agree
exactly.

## 3. Transport versus holonomy

The projector is a smooth tensor field and the metric supplies its projected covariant derivative.
That is the positive transport statement.  It is not ambient-parallel: the already registered
twisted configurations have full sampled `so(1,3)` holonomy, and

```text
(nabla_E0 X_lambda)^0_1 = -3/25
```

for every frozen `lambda`.  Thus the full reciprocal grading remains path-labelled under ambient
transport.  The nonzero relative curvature is compatible with, and partly expresses, this changing
projector geometry; it must not be rewritten as reduced ambient holonomy.

## 4. Controls

- On the `lambda=+1`, constant-depth, twist-free round product, the clock-versus-space projector is
  parallel under spatial `so(3)` holonomy.  There `DP=0` and the relative term vanishes.
- For nonnull `dphi`, `v tensor dphi / g^{-1}(dphi,dphi)` is an exact local rank-one projector.  At
  null `dphi`, the numerator is nonzero nilpotent and is not a projector; at `dphi=0`, no line exists.
- A toric shortest-line pair descends as an unordered set through an exchange; no member is selected
  at the tie.
- A simple spectral line loses uniqueness at an eigenvalue wall.
- Full Lorentz holonomy preserves no real proper line.  Flat/full-isotropy controls make arbitrary
  lines available but select none.

## 5. Relation to the previous conditional response theorem

The previous audit proved, conditional on a supplied rank-one projector, that path strain and
relative loop curvature give the geometric `L2`- and `L4`-shaped responses.  The present audit closes
one antecedent on a named complete **off-shell configuration family**: C01--C06 supply the projector
intrinsically and its relative curvature is nontrivial.

It does not close any of the following:

- why an on-shell UDT universe occupies this family;
- which profile, `lambda`, topology, or completion is selected;
- why the response must be integrated as the physical `L2+L4` action;
- the relative coefficient or physical scale;
- a carrier section, source, boundary law, mass, or stability theorem.

The maximum new statement is therefore

```text
DERIVED_CONDITIONAL_ON_NAMED_REGISTERED_COMPLETE_OFFSHELL_CONFIGURATION
```

for the intrinsic projector and nonzero relative-curvature gates only.
