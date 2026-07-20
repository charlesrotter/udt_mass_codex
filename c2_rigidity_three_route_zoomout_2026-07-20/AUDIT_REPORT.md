# Conditional C2 Rigidity — Three-Route Zoom-Out Audit

Date: 2026-07-20  
Base: `f68c51aa79d65805da23fc5845576f87ef310d4f`  
Preregistration commit: `c5c88a2`  
Mode: CPU-only dependency, homogeneity, countermodel, and information-gain audit  
Status: **VERIFIED-WITH-CAVEATS** — exact scale algebra, fourth-order boundary countermodel,
base-source replay, independent reconstruction, and 28 exercised fail-closed catches pass; no fresh
external-model review was authorized.

## Result first

The recent rigidity results are real but local to one conditional corner:

`smooth compact + conformally flat round branch + conditional pre-scale C^2`.

They tell us that angular distortion, an isolated positive lapse, and the first time/fiber Jacobi
connection do not provide nearby physical modes there. They do **not** choose the `C^2` action, select
a CSN representative, define the physical finite-cell wall, or establish nonlinear/global rigidity.

The three-route zoom-out gives this actionable ranking:

1. **Derive the conditional `C^2` finite-cell boundary variation next.**
2. Defer the expensive nonlinear stationary branch census until the domain and boundary data it must
   satisfy are explicit.
3. Keep the variation-domain/two-stage bridge as the highest conceptual issue, but do not repeat
   algebra against unchanged premises: the required off-shell selector is not presently supplied.

The exact verdict is:

`COMPACT_C2_RIGIDITY_IS_BRANCH_SCOPED; NO_SINGLE_CLOSING_SELECTOR;`
`IMMEDIATE_VARIATION_PLACEMENT_AND EXECUTABLE_OFFSHELL_REPRESENTATIVE_MAP_OPEN;`
`CONDITIONAL_C2_BOUNDARY_VARIATION_RANKED_NEXT`.

## What the rigidity means

The three calculations now constrain the tangent space around the round compact solution:

- the full compact product Bach equation selects round angular shape inside the registered toric
  family;
- an isolated nonconstant positive lapse produces Weyl curvature, while a common full-coframe factor
  is the same CSN class;
- the first time/fiber shift has only a constant coordinate zero mode at Jacobi order.

This is strong evidence that the chosen compact conformally-flat `C^2` branch is locally rigid. It is
one tile in the full theory map. A disconnected nonlinear solution can exist without a Jacobi zero
mode, and a physical boundary can support modes excluded by the compact integrations.

## Why the nonlinear solve is not first

A complete nonlinear `N,H,s,W` Bach solve is still scientifically legitimate and eventually needed.
But even its strongest positive outcome—an exact nontrivial solution—would leave four upstream facts
unchanged:

1. `C^2` remains conditional on its action-class premises;
2. Bach covariance leaves a common conformal orbit unless boundary/source structure breaks it;
3. the physical wall and admissible boundary data remain undefined;
4. time-live dynamics, source, and stability remain open.

Its strongest negative outcome would likewise apply only to the chosen stationary topology and
boundary domain. Running it before defining that domain risks another expensive, correctly computed
answer to the wrong boundary problem.

## Why boundary variation is informative but not magical

For the elementary fourth-order action

`S[y]=integral (y'')^2 dx`,

exact variation gives

`delta S = integral 2 y'''' delta y dx`
`          + [2 y'' delta y' - 2 y''' delta y]`.

The bulk equation is fixed, but several differentiable boundary problems remain possible:

- fix `y` and `y'`;
- impose the natural conditions `y''=y'''=0`;
- add a boundary term and fix a mixed conjugate pair.

This is not a model of UDT physics. It is a mathematical counterexample to the claim that a
fourth-order bulk automatically chooses its physical boundary data.

Deriving the actual `C^2` boundary variation is nevertheless valuable. It will expose the real metric
and normal-derivative conjugate pairs, corner terms, and flux whose absence currently limits both
compact rigidity proofs. It can show whether a natural condition follows from a precisely stated
variational domain. It cannot, by itself, tell us which data the UDT wall physically fixes.

## The two distinct missing selectors

The audit separates two questions that had been sliding together.

### Immediate action fork

Does fundamental variation act:

- on the pre-scale CSN equivalence class, or
- only after a physical representative has been selected?

This remains the smallest selector at the `C^2`/EH fork. Current UDT premises do not answer it.

### Executable representative bridge

Even choosing “after scale selection” does not perform the selection. A working bridge also needs an
off-shell global rule specifying:

- which fields and global quantities vary;
- which scale-bearing finite-cell quantity is held fixed;
- how the selected global scale joins the local complete coframe.

Current bootstrap is an on-shell demand on a completed universe. It supplies no such off-shell map.
Naming this missing object does not authorize inventing its form.

## Exact scale audit

Under `g -> lambda^2 g` in four dimensions:

- `integral sqrt(g) C^2` has weight zero;
- `integral sqrt(g) R` has weight two;
- a volume term has weight four;
- boundary area and proper volume are extensive outputs, not normalization rules.

EH being scale-sensitive does not mean EH selects scale. A bare contribution `A lambda^2` has no
positive stationary scale. Balancing it requires another term, constraint, boundary contribution, or
source with independently supplied sign and coefficient.

Likewise,

`GM/(c^2 Xmax)` and `G rho Xmax^2/c^2`

remain unchanged under

`M -> lambda M`, `Xmax -> lambda Xmax`, `rho -> rho/lambda^2`.

Thus `c` and `G` are legitimate observational anchors but do not determine total mass or `Xmax`
before native mass/source structure exists. A fixed electron mass could calibrate a completed matter
branch; it cannot create that branch or its dimensionless equations.

## Why representative selection is not the C2-to-EH bridge

Choosing one metric `g_*` does not transform the fourth-order Bach operator into the second-order
Einstein operator. Their leading symbols scale as `k^4` and `k^2`. A true two-stage theory still needs
a dynamical matching theorem explaining regime, degrees of freedom, boundary data, and source
matching.

Consequently there is no single known selector that closes everything. The dependency graph retains
independent open edges for:

- the pre/post-scale variation fork;
- the representative map;
- `C^2`/EH dynamical matching;
- finite-cell boundary completion and normalized charge;
- native source/mass;
- global bootstrap and `Xmax` closure.

## Lay interpretation

We have been testing rooms inside a building whose outer wall and construction rule are still partly
unknown. The rooms we tested are unusually rigid: when we push their walls or tilt their clocks, they
spring back to the same round design or to a mere change of coordinates.

That does not prove the whole building must be rigid. It tells us to inspect the actual outer wall
before searching every room for a hidden passage.

It also tells us that “pick a size, then use GR-like equations” is not yet a bridge. Picking a size,
choosing the post-scale law, and showing how that law follows from the pre-scale theory are three
separate jobs.

## Four evidence gates

1. **Preregistered:** yes, commit `c5c88a2` before adjudication.
2. **Full space or bounded scope:** all three registered routes and their current dependency closures
   are covered; no new field solution or future action class is claimed.
3. **Independently verified:** yes in-package through separate homogeneity and boundary-variation
   algebra plus base-source replay; no fresh external-model review.
4. **Every premise audited:** yes; conditional `C^2`, inherited 4D, compact-domain results, on-shell
   bootstrap, observational anchors, and excluded carrier/matter remain explicit.

The correct grade is **VERIFIED-WITH-CAVEATS**. This is a route decision, not canonization.
