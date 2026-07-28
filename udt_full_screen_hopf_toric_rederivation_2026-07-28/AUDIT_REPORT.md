# Full-screen Hopf/toric rederivation

Date: 2026-07-28

Base: `ace0699fc145c935c16cd283f393c18e654d5b74`

Preregistration: `005c2a8`; narrowing pre-verdict clarification: `137ce6f`

## Result first

The complete angular screen does not invalidate the conditional Hopf route. It reveals a stronger
conditional bridge inside the chosen twisted `S3` coframe:

```text
theta1=exp(phi)sigma3
therefore
exp(-phi) theta1=sigma3.
```

The right-hand side is the standard Maurer–Cartan Hopf connection on the registered global `S3`.
Explicitly, `sigma3=cos(eta)^2 dxi1+sin(eta)^2 dxi2`, each phase has period `2 pi`, the diagonal
fiber has integral `2 pi`, and the normalized curvature flux is `plus_or_minus 1`. It is independent
of the common screen scale and both screen shears. Thus a supplied global twisted `S3` coframe with
the founded ruler extension carries a unit Hopf principal bundle for every smooth invertible screen
`P`.

This is not strong local CSN: no common metric factor is declared gauge. It is algebraic inversion
of the already-founded ruler dilation.

The exact maximum ruling is:

```text
FULL_SCREEN_ROBUST_CONDITIONAL_HOPF_BUNDLE_ON_CHOSEN_DEPTH_NORMALIZED_S3_COFRAME;
GENERAL_SCREEN_DOES_NOT_SELECT_TORIC_SYMMETRY, GLOBAL S3, CAP CLASS, FIBER,
METRIC DESCENT, ROUND TARGET, CARRIER, OR ACTION.
```

## The important correction to the tempting interpretation

The unnormalized ruler form `theta1` is contact for every invertible `P`, but contact does not imply
closed orbits. An exact smooth positive rescaling has Reeb slope `3-2sqrt(2)` on the Clifford torus,
so its orbit is nonperiodic. The unit bundle follows from the founded-depth-normalized form on the
chosen Maurer–Cartan `S3`, not from contact alone.

Three scopes must remain separate:

1. **Coframe conditional:** `sigma3` is a free Hopf connection on the chosen global `S3` for all
   full screens.
2. **Metric-intrinsic overlap:** existing C01–C06 configurations already let the complete metric
   identify the reciprocal ruler line; on a positive spatial slice, its normalized spatial metric
   dual gives `sigma3`. Persistence after both shears are freed is not yet proved.
3. **Metric quotient:** an arbitrary `P` may depend on the Hopf fiber and break its isometry. The
   full screen descends to a quotient metric only on the fiber-equivariant/invariant subfamily.

## What the full toric calculation says

For a separately supplied effective cohomogeneity-one `T2` action, its invariant positive
torus-orbit block `h`, and a primitive generator `w`, the orbit component of the normalized
metric-dual connection in the registered orthogonal interval gauge

```text
A_w=h(w,.)/h(w,w)
```

is exact and common-positive-factor independent. The two shears act collectively: an off-diagonal
mode changes the connection, while the complementary shape mode can change the quotient metric
without changing that connection. A basic radial term may occur outside the orthogonal gauge; it
does not alter the cap/Euler class. Screen shape does not change the Chern class after the global
bundle is fixed.

For primitive cap cycles `v_minus,v_plus`, assuming two smooth caps and no extra exceptional orbit,
the free-circle condition is

```text
|det(v_minus,w)|=|det(v_plus,w)|=1,
```

Choosing a unimodular companion `u`, writing `v_i=a_i w+b_i u`, and using freeness
`b_i=plus_or_minus 1` gives the clutching degree directly, and hence

```text
|c1|=|det(v_minus,v_plus)|.
```

The `S3` class has `|c1|=1`, but it is only one member. The exact exchange-symmetric family

```text
v_minus=(k+1,k), v_plus=(k,k+1), w=(1,1)
```

has a free circle and `|c1|=2k+1`. General `L(p,1)` examples also realize every positive `p`.
Therefore full-screen shear, smoothness, mirror exchange, and quotient freeness do not select unit
topology over the registered global completion space.

## N22 regrade

Prior status:

```text
PROMISING_STRONGER_CONDITIONAL_ROUTE.
```

Full-screen status:

```text
STRONGER_CONDITIONAL_DEPTH_NORMALIZED_CONTACT_HOPF_BUNDLE_ROUTE__NATIVE_CARRIER_OPEN.
```

The old aligned reciprocal-toric seed remains exact in its subfamily. The normalized-ruler route is
more robust because its unit bundle survives arbitrary screen shear on the chosen `S3`. But a
principal bundle projection supplies one canonical `S3->S2` map, not the independent
`Map(S3,S2)` deformation space, round target metric, `L2+L4` action, source, boundary, or mass.

## T18 regrade

Prior status:

```text
TWO_STAGE_OPEN_GATE_CHAIN.
```

Full-screen status:

```text
REFINED_CONTACT_OR_TORIC_GLOBAL_REGULARITY_AND_DESCENT_GATE_CHAIN__NO_SELECTION.
```

The old wording treated transverse reciprocal torus realization as the only first gate. It is not.
There are now two conditional routes:

- a general toric route requiring global `T2` symmetry, cap lattice, a free circle, and screen
  descent; and
- a normalized-contact route requiring the selected twisted `S3` coframe, founded ruler ownership,
  and screen descent.

Current Reciprocity supplies neither global branch. Current finite-cell structure supplies no cap
lattice or fiber-equivariance law. Current bootstrap is on-shell admissibility and supplies no
topology-ranking map. The route is rederived and sharpened, not closed.

## What remains unchanged

- founded `phi` and its reciprocal pair action;
- the observer-pair and Lorentz algebra;
- registered WR-L/SNe evidence and `Xmax` status;
- conditional static finite-box Hopfion stability;
- the `POSIT` status of the round `S2` carrier;
- `C2`/Bach unique-conditional and EH conditional status; and
- open complete action, source, boundary charge, carrier emergence, unconditional mass, and
  dynamics.

No GPU, ODE/PDE, time-live, density, action, source, matter, fitting, or canonization work occurred.

## Evidence gates

1. **Preregistered:** yes, `005c2a8`. The positive-slice/metric-descent distinction was recorded as
   the narrowing clarification `137ce6f` before final verification.
2. **Full or bounded:** complete for the full interior `GL(2,R)` screen in the chosen stationary
   block-screen `S3` control and the registered toric cap/fiber taxonomy; not the generic spacetime
   metric, other unconstructed completions, or any on-shell solution space.
3. **Independent:** 34 exact production identities are reconstructed by a non-importing
   standard-library `Fraction` matrix/exterior/lattice implementation with 11,197 passing checks and
   32 exercised mutations of actual evidence fields, tables, classifications, provenance, and
   repository gates. A fresh zero-context adversarial semantic review is recorded separately.
4. **Premises:** 23 rows separately stamp founded, observed, free, chosen-control, dropped, and open
   inputs. Countermodels remain in the census and no desired physical result is an acceptance gate.

The 38-source fixed-base manifest has identity SHA-256
`5c9b9d0e6ca284513ab85afacda01c948f087f979fee5f5362fd1300961ba11f`.

Grade: `VERIFIED-WITH-CAVEATS_BOUNDED_STATIC_GLOBAL_REDERIVATION`.
