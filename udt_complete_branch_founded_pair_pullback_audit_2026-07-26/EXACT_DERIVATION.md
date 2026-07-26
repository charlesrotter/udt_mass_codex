# Exact complete-branch pullback derivation

## 1. Registered universe versus actual metrics

The global assembly atlas contains twelve completion classes `FC01`–`FC12`. They describe possible
boundary, cap, quotient, monodromy, stratified, and distributional completions. A compatibility rule
or topology class is not itself a solved metric.

The frozen concrete-configuration registry contains four rows:

- round `S^3` / B19: conditionally complete and on shell only in its recorded `C^2`/Bach scope;
- homogeneous squashed `S^3`: a complete off-shell configuration;
- WR-L: a local static spherical profile without all-observer global completion; and
- the physical `Xmax` join: absent.

The first two both occupy the determinant-one two-cap `S^3` completion class `FC04`. No other
completion class has a registered actual complete metric representative. `FC12` is a particularly
important near miss: it is a reciprocal-toric metric ansatz with free profiles and endpoint data,
not a selected completed metric.

## 2. Homogeneous complete control

Both concrete complete configurations can be represented by an ultrastatic product with a round or
Berger spatial `S^3`. Write a global left-invariant orthonormal spatial coframe as

```text
de1 = p e2 wedge e3,
de2 = p e3 wedge e1,
de3 = q e1 wedge e2.
```

The round locus is `p=q`; nonround homogeneous squashing has `p!=q`. Let the conditional pair be

```text
u = global ultrastatic time direction,
n = vector dual to e3,
screen = span(e1,e2).
```

Solving the torsion-free Cartan equations with

```text
omega12=A e3, omega13=B e2, omega23=C e1
```

gives

```text
A=p-q/2, B=-q/2, C=q/2.
```

The only derivatives of the pair are

```text
nabla_e1 n = +(q/2)e2,
nabla_e2 n = -(q/2)e1,
nabla_n n = 0,
nabla u = 0.
```

Thus the pair has pure constant screen twist and no acceleration, expansion, shear, or pair boost.

## 3. Does the metric select the spatial line?

Direct curvature contraction gives the spatial Ricci eigenvalues

```text
Ric_screen = p q - q^2/2,
Ric_Hopf   = q^2/2,
gap        = q(q-p).
```

At `p=q`, all three eigenvalues coincide. The round metric therefore does not distinguish the chosen
Hopf line: global Hopf fields exist, but selecting one is extra structure.

At `p!=q`, the Hopf direction is the simple Ricci eigendirection. The nonround metric therefore does
select an **unoriented line**. It does not select its sign or a screen orientation, and the branch
remains an off-shell control.

This cleanly separates three propositions:

1. a smooth global vector field exists;
2. a metric intrinsically distinguishes its line; and
3. UDT derives that line as the founded reciprocal ruler direction.

Only proposition 1 holds for the round control. Propositions 1 and 2 hold for the nonround control.
Proposition 3 holds for neither.

## 4. Pullback of all 22 first-jet motifs

For the conditional oriented Hopf pair, 20 of the 22 one-forms vanish. The only nonzero forms are

```text
N07 = q u_flat,
N08 = q n_flat.
```

Their span has rank two. Their exterior derivatives are

```text
dN07 = 0,
dN08 = q^2 e1 wedge e2,
```

so exterior-derivative rank is one.

`N07` is exact on the ultrastatic product with global time `t`:

```text
u_flat=-dt, therefore N07=-q dt.
```

This is not the missing result. Its potential is ordinary coordinate/proper time, not the founded
reciprocal group coordinate `phi`, and its existence uses a screen orientation. `N08` follows the
Hopf fiber and is not closed; its nonzero exterior derivative is precisely the twist.

When screen orientation is not supplied, both `N07` and `N08` are unavailable and the realized
orientation-free motif rank is zero. If only ruler-sign invariance is imposed while orientation is
retained, `N07` survives and rank is one. Imposing both removes both.

Because the geometry is homogeneous, these ranks persist throughout the complete `S^3` cell. The
Hopf pair is smooth through coordinate axes and cap charts. Antipodal geodesic nonuniqueness affects
path readouts, not the global field calculation.

## 5. Branch rulings

### Round B19

The conditional complete metric and global ultrastatic time direction exist. A Hopf pair can be
chosen, but round isotropy does not select it. Even after that choice and an orientation, the only
closed line is ordinary time. It fails the pair-selection and founded-normalization gates.

### Squashed `S^3`

The complete off-shell metric distinguishes an unoriented Hopf line by its Ricci eigensplitting.
This is a genuine metric-emergent structure. Without adding screen orientation its first-jet motif
space is nevertheless zero. With orientation the exact line is still ordinary time, and the branch
is not on shell. It fails orientation, on-shell, and founded-normalization gates.

### WR-L

WR-L retains its exact local clock-depth profile but has no complete all-observer metric. Attaching
that lapse to B19 or the squashed control would splice branches and is forbidden.

### Other completion classes

They remain registered possibilities or conditional ansatz families. They do not contain the
metric, pair, profiles, and global joins needed for a pullback calculation.

## 6. Exact boundary

No registered representative passes all eight preregistered gates. The result is therefore

```text
NO_REGISTERED_COMPLETE_PULLBACK_WITNESS.
```

This is not a universal no-go for UDT. A complete non-ultrastatic or clock/angular-coupled branch
could reduce the 22 local motifs differently. Such a branch is not presently in the registered
solution library.
