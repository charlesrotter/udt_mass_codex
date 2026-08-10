# Exact derivation — branch-local non-isometric calibration transition

Date: 2026-08-10

Mode: metric-led, exact analytic/CPU

Current grade: **VERIFIED-WITH-CAVEATS — CONDITIONAL ASSEMBLY, NOT BRANCH-OWNED**

## 1. Result first

One frozen complete branch contains enough owned ingredients to define a lawful four-slot,
path-carried, non-isometric calibration-transition family **after a comparison-law choice**.

On the named twisted `S3` configurations C01--C06, prior independent audits derive from the same
complete metric:

1. one intrinsic global timelike Killing line `K`;
2. a twist-selected intrinsic global spacelike ruler line;
3. their clock/ruler projectors `P_u,P_n` and screen complement `H`;
4. the basis-free branch grading

   ```text
   X_lambda=-P_u+P_n+lambda H;
   ```

5. the endpoint depth

   ```text
   delta_K(p,q)=log[N(p)/N(q)]=phi(q)-phi(p),
   N=sqrt(-g(K,K));
   ```

6. Levi-Civita path transport `U_gamma`, including its full clock/ruler/screen mixing and
   nontrivial holonomy.

For a path-labelled comparison state whose source grading is `X_p`, the audited conditional
assembly is

```text
A_gamma=U_gamma exp[delta_K(p,q) X_p].
```

Its target grading is the carried state

```text
X_q^gamma=U_gamma X_p U_gamma^-1.
```

This arrow is non-isometric when `delta_K` is nonzero, is complete across all four slots, and
composes exactly on matched carried states. The fresh external review found—and the adjudication
accepts—that these facts do not make the formula branch-owned. The branch derives each ingredient
but does not select this multiplication as the physical observer-pair law. It also does not choose
one physical path, identify the carried target grading with the separately reconstructed intrinsic
grading at `q`, or prove that the linear arrow integrates to one global pair surface.

## 2. Source configuration and ownership

The frozen family has complete coframe

```text
theta_0=exp(-phi)(dt+a sigma_3),
theta_1=exp(+phi)sigma_3,
theta_2=exp(lambda phi)sigma_1,
theta_3=exp(lambda phi)sigma_2,
g=-theta_0^2+theta_1^2+theta_2^2+theta_3^2.
```

The Maurer--Cartan forms are global on `S3`. The prior curvature-invariant rank certificate proves
that C01--C06 have exactly one continuous Killing line, rather than merely a convenient stationary
coordinate. The twist of that same line spans `theta_1`, so the clock and ruler are recovered in
one metric. Their signs cancel from `P_u,P_n,H`.

The finite-cell reduction audit then derives the basis-free finite metric lift

```text
exp(phi X_lambda)
 =exp(-phi)P_u+exp(+phi)P_n+exp(lambda phi)H.
```

`lambda` is not selected across the family. It is part of each named configuration. The theorem
below therefore applies branch by branch at the configuration's supplied `lambda`; it is not a
`lambda`-selection theorem.

## 3. Correct conditional path-carried groupoid type

An object is a regular enriched calibration state

```text
Q=(p,X,F),
```

where `p` is an event, `X` is a causal self-adjoint grading in the path orbit of the branch's
intrinsic `X_lambda`, and `F` is its clock-line-inside-clock/ruler-plane flag. For a declared smooth
path `gamma:p->q`, Levi-Civita transport gives an isometry

```text
U_gamma:(T_pM,g_p)->(T_qM,g_q).
```

The arrow has source and target

```text
s(A_gamma)=(p,X_p,F_p),
t(A_gamma)=(q,U_gamma X_p U_gamma^-1,U_gamma F_p).
```

The exponential factor changes densities but not the flag subspaces, so this typing is exact.
Paths are retained as arrow labels; no one path is postselected.

This is not an endpoint atlas of the intrinsic `X_lambda(q)` field. Conditional on the semidirect
assembly, it is a coherent path-carried calibration-state groupoid. A reset from the carried target
state to a separately rebuilt local intrinsic state is a different arrow `M_q` and remains open.

## 4. Exact composition, reversal, and loops

For composable paths `gamma:p->q` and `beta:q->r`, put

```text
X_q=U_gamma X_p U_gamma^-1,
A_gamma=U_gamma exp(delta_pq X_p),
A_beta=U_beta exp(delta_qr X_q).
```

Conjugation gives

```text
exp(delta_qr X_q)U_gamma
 =U_gamma exp(delta_qr X_p).
```

Therefore

```text
A_beta A_gamma
 =U_beta U_gamma exp[(delta_pq+delta_qr)X_p]
 =U_(beta o gamma) exp[delta_pr X_p]
 =A_(beta o gamma).
```

The second equality uses the already derived endpoint coboundary
`delta_pq+delta_qr=delta_pr`. Reversal returns the inverse and coincidence returns identity.

On a closed loop, `delta_pp=0`, so

```text
A_loop=U_loop.
```

Nonidentity Lorentz holonomy survives. Composition therefore does not impose path independence or
zero angular transport.

## 5. Non-isometry and complete mixing

`X_p` is self-adjoint with respect to `g_p`, while `U_gamma` is an isometry. Hence

```text
A_gamma^dagger A_gamma=exp(2 delta_K X_p).
```

For nonzero depth this is not identity. The transition is therefore genuinely non-isometric; the
effect is not manufactured by coordinate identity or coframe mismatch.

The exact rational control uses `lambda=1/2`, `exp(delta)=4`,

```text
E=diag(1/4,4,2,2),
U=[[5/3,0,4/3,0],
   [0,1,0,0],
   [4/3,0,5/3,0],
   [0,0,0,1]],
A=U E.
```

`U^T eta U=eta`, while `A^T eta A` is not `eta`. The `0-2` entries of `A` are nonzero, so the
full arrow retains clock-screen mixing. A second independent rational Lorentz rotation is used in
the composition control; all entries agree exactly.

## 6. Terminal reciprocal readout

Restrict `A_gamma` to the carried clock/ruler flag. Isometry of `U_gamma` leaves its Gram matrix

```text
h_pair=diag[-exp(-2delta_K),exp(+2delta_K)].
```

Thus

```text
T=exp(-delta_K),
L=exp(+delta_K),
delta_RF=(1/2)log(L/T)=delta_K,
c_eff^(pair)/c_E=exp(-2delta_K).
```

This is exact compatibility with both the reciprocal-root character and the terminal pair-metric
evaluator on the supplied carried flag restriction. The angular/mixing transport remains present
in the full arrow and its path holonomy, but its isometric part does not alter this branch's scalar
density ratio.

That separation is a result, not a universal claim that the angular orchestra never modulates
reciprocal depth. Other complete arrows need not factor into this branch's isometric transport and
owned endpoint squeeze.

## 7. The open reset and physical-map seam

The branch also reconstructs an intrinsic grading `X_lambda(q)` directly at the endpoint. Full
ambient holonomy proves that generally

```text
U_gamma X_lambda(p) U_gamma^-1 != X_lambda(q).
```

Consequently two distinct B states coexist:

1. the calibration grading carried from A along `gamma`; and
2. the intrinsic grading rebuilt from the complete metric at B.

The transition

```text
M_B: X_B^carried -> X_B^intrinsic
```

is not supplied by the current branch evidence. Setting it to identity would erase the measured
holonomy and violate the three-observer audit. Inserting an arbitrary reciprocal reset changes the
composite and the scalar depth; an exact catch proof retains this obstruction.

Therefore the conditional theorem closes the chosen assembly on matched path-carried objects. It
does not close either ownership of that assembly or the physical rule deciding whether actual
observers carry, rebuild, or otherwise relate calibration states.

The arrow is also a complete linear comparison Jacobian. No current proof integrates every such
arrow into a global two-dimensional observer-pair surface through cut loci and seams. The terminal
algebra accepts a supplied comparison Jacobian, but physical pair-map realization remains open.

## 8. Other branch rulings

- W02 owns a genuine non-isometric clock-line endpoint scaling. It has no same-branch intrinsic
  ruler scale. Two exact completions with the same clock factor give different terminal depths, so
  it is `PARTIAL_CLOCK_SCALE_TRANSITION_OWNED`.
- W03 and the general-screen family own isometric path transport only; their metric strain is
  identity until an unowned reciprocal scale is supplied.
- The toric family owns an unordered projector set and its chamber/wall transport, not density
  scaling.
- Four branches require an unowned query, line, orientation, or presentation choice.
- FC04 is an aggregate containing the W01 conditional candidate, the W02 partial result, and open/zero/failure
  members; no class-wide transition is inferred.
- Nine entries lack typed metric evidence, four lack a complete regular branch, and FC12 requires
  current-premise rederivation.

The exact 24-row rulings are in `TRANSITION_OWNERSHIP_ATLAS.tsv`.

## 9. Maximum conclusion

```text
DERIVED_CONDITIONAL_CONSTRUCTION_ON_THE_NAMED_C01_C06_COMPLETE_OFFSHELL_CONFIGURATIONS:
AFTER_CHOOSING_THE_SEMIDIRECT_ASSEMBLY__THE_INTRINSIC_RECIPROCAL_GRADING__KILLING_ENDPOINT_DEPTH
AND_LEVI_CIVITA_PATH_GROUPOID_FORM_AN_EXACT_PATH_CARRIED_NONISOMETRIC_TRANSITION;
THE_BRANCH_DOES_NOT_SELECT_THIS_ASSEMBLY_AS_ITS_PHYSICAL_COMPARISON_LAW;
ON_THE_SUPPLIED_CARRIED_FLAG__ITS_RECIPROCAL_ROOT_AND_TERMINAL_PAIR_READOUT_EQUAL_DELTA_K;
ANGULAR_MIXING_AND_NONIDENTITY_HOLONOMY_REMAIN_IN_THE_FULL_ARROW;
THE_CARRIED_TO_REBUILT_ENDPOINT_TRANSITION__PHYSICAL_PATH_OR_RELATION_SELECTION__GLOBAL_PAIR_SURFACE
AND_UNIVERSAL_MIXED_GEOMETRY_SCALAR_LAW_REMAIN_OPEN.
```

No action, source, carrier, matter, mass, boundary, bootstrap return, `X_max` value, CMB spectrum,
signalling law, or on-shell branch selection follows.
