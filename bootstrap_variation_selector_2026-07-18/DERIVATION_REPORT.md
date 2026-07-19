# Bootstrap variation-domain selector derivation

Date: 2026-07-18  
Branch: `codex/bootstrap-variation-selector-2026-07-18`  
Preregistration commit: `851b8f3`  
Authority: bounded research-status result; not canonization

## Ruling

The existing UDT bootstrap principle does **not** select whether fundamental variation occurs before
or after physical scale is selected, and it does **not** derive a two-stage bridge. Its exact recorded
role is global and on shell: the realized universe is self-consistent, and matter-bearing realized
solutions occupy a narrow proper-total-density window. That filters or closes solutions after a
dynamical problem has been defined; it does not specify the off-shell fields, action, admissible
variations, representative-selection map, or matching law.

The preregistered top-level outcome is therefore `UNDERDETERMINED`. This is a logical
non-implication result scoped to the present bootstrap statement, not a negative verdict on bootstrap
closure and not a proof that a future off-shell bootstrap law cannot select a domain.

The accepted scientific statuses remain unchanged:

- reciprocal kinematics: `DERIVED`;
- pre-scale `C^2`/Bach bulk: `UNIQUE_CONDITIONAL` inside its named class;
- post-scale EH/Lovelock: `CONDITIONAL` inside its named class;
- representative selection, complete action, native source, carrier emergence, boundary charge,
  unconditional mass, and the two-stage bridge: `OPEN`.

## T1 — semantic and off-shell audit

The affirmative bootstrap source contains four relevant kinds of statement:

| Recorded content | Classified role | Consequence |
|---|---|---|
| The realized universe is a self-consistent global solution | On-shell/global closure | A completed realization must close globally. |
| Matter-bearing solutions exist only in a narrow total proper-density window | On-shell admissibility | The physical solution set is a narrow subset once total charge and proper volume exist. |
| Local mathematical carrier solutions may exist outside the window | Explicit separation of local solutions from realized universes | The window is not itself a local field equation. |
| Global density may not be inserted as a fitted local coupling or cutoff | Anti-insertion constraint | A future influence must arise through solved geometry, boundary data, or a separately derived global variational condition. |

No source clause declares bootstrap to be varied, gives a functional `B`, defines a map
`Sigma:[g]_CSN -> g_*`, orders representative selection relative to variation, or maps a pre-scale
operator to a post-scale one. The last clause explicitly leaves a separately derived global
variational condition as a future possibility rather than silently supplying it.

## Logical non-selection theorem

Let `Q` denote the pre-scale CSN quotient, let `R -> Q` be its family of metric representatives, and
let a chosen dynamical package `(D,E)` consist of an off-shell variation domain `D` and equations
`E`. The present bootstrap statement constrains a subset of the realized solution set:

```text
W_B subset Sol(D,E) x R,
```

where membership includes global closure and the narrow density condition. The mapping

```text
(D,E) -> W_B
```

is not injective. A condition on realized roots cannot reconstruct which off-shell domain or
equations generated those roots. The explicit T3 models witness that non-injectivity while keeping
the global density out of both local actions.

This proves only the selector-level implication: **B01 does not entail a unique variation
placement.** It does not claim that the toy models are complete UDT universes.

## T2 — variation and representative restriction do not commute automatically

For a general action `S(x,y)` and a selected section `y=f(x)`, the exact chain rule is

```text
d S(x,f(x))/dx = S_x(x,f(x)) + S_y(x,f(x)) f'(x).
```

Restrict-then-vary retains the second term. Vary-then-restrict followed by keeping only the tangent
`x` equation does not. Equality of those two tangent equations requires an explicit condition such
as `S_y f'=0`. Equivalence to the full unrestricted variational problem additionally requires the
normal equation `S_y=0` or a theorem proving it redundant. The runnable symbolic test uses a generic
quadratic polynomial and obtains the nonzero normal term

```text
b*p*x + 2*c*p**2*x + 2*c*p*r + e*p.
```

Bootstrap would have to choose the domain and prove this normal condition; representative selection
alone does neither.

## T3 — explicit selector countermodels

Use `q` for a CSN-invariant shape coordinate and `sigma` for common scale. Let global closure return
`sigma_star` and define

```text
B = sigma - sigma_star,
rho_tot = rho_star + kappa B,
matter admissible only if |rho_tot-rho_star|/rho_star < epsilon.
```

The shared preregistered regime is `0 < epsilon << 1`; neither its center nor its width is fitted or
assigned numerically.

`sigma_star`, `rho_star`, and the fractional width are outputs/conditions of global closure, not
primitive local couplings. Neither action below contains `rho_tot` or its window.

### Model P — vary the quotient before global closure

```text
S_P(q) = (q-q_star)^2,
dS_P/dq = 2(q-q_star),
then impose B=0 on the realized global solution.
```

### Model S — select a section, then vary

```text
bootstrap selects sigma=sigma_star,
S_S(q; sigma_star) = sigma_star^2 (q-q_star)^2
                       + lambda (q-q_star)^4,
dS_S/dq = 2 sigma_star^2(q-q_star) + 4 lambda(q-q_star)^3.
```

Both have the common realized root `(q_star,sigma_star)`, both give `rho_tot=rho_star`, both use the
same narrow-window predicate, and their off-shell actions and variation placement differ. They are
complete relative to the selector implication being tested, not relative to the ten-criterion UDT
theory space. Consequently they refute the claim that the current bootstrap clauses alone choose
one placement.

## T4 — conformal-weight anchor

Under constant common scaling in four dimensions,

```text
sqrt(|g|) -> Omega^4 sqrt(|g|),
R         -> Omega^-2 R,
C^2       -> Omega^-4 C^2.
```

Therefore `sqrt(|g|) C^2` has weight zero while `sqrt(|g|) R` has weight two. This reproduces the
necessary pre/post-scale distinction. It is only a constant-weight anchor; it is not the full local
Weyl, variation, or finite-boundary theorem.

## T5 — selecting scale does not lower principal differential order

At the principal-symbol level, a fourth-order pre-scale branch and a second-order post-scale branch
have schematic transverse polynomials

```text
P_4(k) = alpha k^4,
P_2(k) = beta M^2 k^2.
```

Requiring equality for every Fourier `k` gives `alpha=0` and `beta M^2=0`; there is no nontrivial
polynomial identity. Choosing `M` through global closure supplies a scale but does not remove the
`k^4` principal term or create the `k^2` law. A genuine bridge may still arise through a separately
derived singular limit, integration-out procedure, symmetry breaking, or effective expansion, but
that procedure and its controlled errors are additional dynamics, not representative selection.

This test does not claim a full nonlinear C2-to-EH no-go. It refutes only **scale selection as a
sufficient bridge**.

## T6 — three inequivalent bootstrap placements

The current wording admits three mathematically distinct future implementations:

1. **After-solution predicate:** solve `E=0`, then retain roots satisfying `B=0` and the density
   window. `B` does not enter the local Euler equations.
2. **Varied global constraint:** add a multiplier term `eta B` and vary all declared variables. This
   introduces a multiplier equation and contributions proportional to `eta delta B`.
3. **Selection before post-scale variation:** first derive a section `Sigma([g])=g_*`, then define
   and vary a post-scale action on that section. The T2 chain-rule condition controls whether this is
   equivalent to any unrestricted parent variation.

The symbolic model exposes equation counts `2`, `3`, and `1`, respectively. Coincidence at one root
does not prove off-shell equivalence.

## T7 — strongest two-stage bridge contract

A future bridge must satisfy all seven gates below. None may be replaced by familiarity with GR or
by the fact that a representative exists.

1. **Bootstrap role:** derive whether `B` is a predicate, varied constraint, or selection map.
2. **Selection theorem:** if a map is claimed, prove existence, uniqueness (or classify branches),
   covariance, differentiability, and compatibility with the finite mirrored cell.
3. **Pre-scale dynamics:** state fields, locality/covariance class, invariant inventory, variation
   domain, boundary/corner action, and source before selection.
4. **Field and variation map:** identify which pre-scale degrees of freedom survive, become gauge,
   are constrained, or are integrated out.
5. **Controlled matching:** derive the post-scale principal operator and action in a stated regime,
   with error bounds. In particular, explain any fourth-to-second-order change.
6. **Boundary/source matching:** map finite-cell boundary data, differentiable generators, source
   variation, reference, orientation, and charge normalization.
7. **Solution closure:** prove a compatible nontrivial solution, stability in the claimed regime,
   and the bootstrap density/root conditions without inserting their center or width.

This is a `CONDITIONAL_CONTRACT_ONLY`. It is the strongest bridge statement supported by the current
record.

## Smallest genuinely missing object

The immediate missing item is not another action ansatz. It is the **off-shell role and placement of
bootstrap**:

```text
after-solution admissibility
vs varied global constraint
vs representative-selection map before variation.
```

If the third role is derived, the next concrete object is the selection map `Sigma` with its
existence/uniqueness/differentiability theorem. Even that would not derive the bridge: the dynamical
matching theorem remains independently missing.

## Completeness map — this result is one logical tile

| Criterion | Covered here | Still open |
|---|---|---|
| 1. Fields | Countermodel coordinates are explicit | Native metric/coframe/scalar/matter census |
| 2. Action terms | Conditional C2/EH classes and toy actions are distinguished | Complete native invariant inventory and coefficients |
| 3. Full equations | Every toy variable/placement equation is shown | Complete UDT field variations |
| 4. Domain/coordinates | Off-shell placement is the tested object | Native time-live domain and charts |
| 5. Boundary/regularity | Finite-cell compatibility is a bridge gate | Differentiable boundary/corner action |
| 6. Topology | Not used | Native sector census |
| 7. Dynamical character | Principal-order distinction only | Static/stationary/dynamic native theory |
| 8. Branches | Selection-map uniqueness is explicitly required | Global solution branches |
| 9. Stability | Not used | Stability of any completed global solution |
| 10. Regime | Exact selector logic plus necessary symbolic anchors | Any physical bridge regime and controlled errors |

The uncovered criteria can host emergent structure. Nothing here closes the complete action.

## Evidence and authority boundary

The derivation is preregistered, CPU-only, carrier-free, and uses no fitted density or GPU work. The
July 1 provenance firewall is preserved. Runnable algebra is in `derive_bootstrap_selector.py` and
its machine-readable result; an independent implementation verifies the load-bearing identities and
exercises corrupt fixtures before this result is banked.

No frozen package, scientific artifact, `CANON.md`, action status, particle result, or R1H registry
is modified. Repository reorganization remains paused. This branch does not update `grok`.
