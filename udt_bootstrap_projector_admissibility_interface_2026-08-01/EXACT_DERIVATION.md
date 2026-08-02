# Exact derivation — bootstrap/projector admissibility interface

## 1. Three different objects

Let `X` be a complete configuration argument and `O` independent global data.  The externally
reviewed projector audit supplies a bounded off-shell open set

```text
N_projector subset X.
```

The working bootstrap architecture separately requires a return relation and a forward readout,

```text
A(X,O)=0,
O=R[X].
```

An actual on-shell bootstrap intersection would be

```text
N_projector intersection Sol(E_native)
intersection pi_X[ Z(A) intersection Graph(R) ].
```

This expression is a type declaration, not a solution.  The current record defines the first
factor only in the registered stationary complete off-shell family.  `E_native`, complete `R`, and
`A` remain open.

## 2. Why a forward graph does not select

In a one-dimensional exact control,

```text
o-r x=0
```

has Jacobian rank one and nullity one on the two-variable `(x,o)` space.  Its projection contains
every `x`: it assigns an `o` to each supplied state but does not decide which state is realized.
Adding an independent local constraint, an independent global constraint, or a genuinely coupled
constraint can raise the rank to two, but those are distinct added relations.  The readout graph
does not choose among them.

## 3. Density-range hypothesis: useful but precisely scoped

The provisional statement

```text
rho_minus < O_rho < rho_plus
```

is a legitimate global survival window once a native same-solution density readout exists.  Before
substituting `O=R[X]`, however, it has no `X` dependence.  It is therefore a one-way on-shell filter,
not by itself the full two-way tuning operation.

Combining a local predicate `P(X)` with the window,

```text
P(X) and O_rho in I,
```

does depend on both arguments.  But its nonempty local fiber is the same set `P` everywhere inside
the window.  This is a separable mutual filter; it does not show that changing the global state
changes the shape or parameters of the local admissible family.

The stronger chicken-and-egg tuning picture begins when

```text
F_O = {X : A(X,O)=0}
```

has different nonempty fibers for different independent `O`.  Differentiable response is stronger
again and requires a nontrivial `D_O A`.  Neither stronger level is inferred merely from the word
“bootstrap.”

The finite four-state/three-readout control in `ALGEBRA_RESULT.json` makes these distinctions exact:
the readout graph projects to all four states; a global window and a separable window-plus-local
predicate each retain one nonempty fiber shape; a modulated relation has three distinct nonempty
fiber shapes.  These controls prove implications only; they are not UDT physical models.

## 4. What the projector result contributes

The new projector result materially fills one slot.  It shows that the intrinsic clock, ruler,
projector/screen, global configuration gates, and nonzero local relative curvature are not balanced
on six isolated points.  They persist on real functional neighborhoods.

It does not supply `A` because it has no independent `O` argument.  Setting its response to zero or
nonzero is a local configuration predicate.  It does not supply `E_native` because the family is
off shell.  It does not supply a native matter density because neither an unconditional mass-energy
functional nor the same-solution density exists.  It must not be renamed a carrier or stability
condition.

## 5. Candidate rulings

- `C01`: projector geometry alone is an off-shell local filter.
- `C02`: the readout graph recomputes but does not return.
- `C03`: a density interval is a coherent working one-way survival-filter type; its native density,
  interval, domain, and on-shell ownership are absent.
- `C04`: `W(X)` and `Omega_rel(X)` have no independent global argument and cannot be the bootstrap
  return alone.
- `C05`: metric curvature readouts may fill components of `R`; readouts do not create `A`.
- `C06`: the Hopfion basin remains conditional on the posited carrier/action and cannot define
  native membership.
- `C07`: the two-arrow diagram is the correct type but not an operation.
- `C08`: the full same-solution intersection is presently uncomputable, not observed empty.

## 6. Exact missing joint

The smallest missing bootstrap object remains a metric-native observer-natural family of
global-to-local membership fibers `F_O`, together with a complete same-solution readout for the
claimed channels.  To intersect it with the stability program one additionally needs the native
on-shell equation/domain and boundary/global-modulus completion.  An action is one possible later
realization, not logically required at this interface stage.

Maximum conclusion:

```text
PROJECTOR_ANTECEDENT_ROBUST__BOOTSTRAP_INTERSECTION_OPEN_MISSING_E_NATIVE_R_AND_A.
```
