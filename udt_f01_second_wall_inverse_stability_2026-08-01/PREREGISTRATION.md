# F01 second-wall inverse-stability surface — preregistration

Date: 2026-08-01  
Frozen base: `46c763770f3f71376a0e57338c276ed3981ce36b`  
Mode: CPU-only; exact/validated inverse stability audit; no boundary selection

## Whole question

On each of the four exact conditional F01 domains, what trace-aligned quadratic wall response would
be required to remove the single negative direction found under the germ-Hessian-flat witness?

The audit studies the smallest two-parameter wall-Hessian slice that connects the banked trace
forks:

```text
tau = effective nonnegative angular-trace stiffness after angular-field elimination,
eta = direct quadratic curvature in the constant lambda/mu direction.
```

`tau=0` is the R05 free-angular reduction. The zero-angular-trace R06 limit is
`tau_infinity=s^2/J`, where `J=integral dx/w`. The audit will derive the field crossing
`tau_critical`, then the exact relaxed `lambda/mu` Schur surface and the minimum `eta` needed for a
nonnegative joint form.

This is not the full unrestricted wall Hessian. Cross-germs, independent per-wall matrices,
additional moduli, other trace channels, N4 data, and physical wall ownership remain open.

## Why this follows the bridge audit

The action/boundary bridge audit proved that C2/Bach, EH, and the proposed two-stage route do not
own F01's free second wall germ. The stability hypothesis can nevertheless be advanced as an
inverse problem: calculate what any future native closure law would have to supply, without
inventing or selecting that supply.

## Frozen source universe

At the exact base, freeze every tracked file under:

```text
udt_f01_lambda_schur_check_2026-08-01/
udt_p4_stability_slice_2026-07-30/
udt_p4_boundary_action_gate_2026-07-30/
udt_stability_derivation_closure_sweep_2026-08-01/
udt_stability_action_boundary_bridge_audit_2026-08-01/
```

plus:

```text
CURRENT_SCIENTIFIC_PREMISES.md
CURRENT_SCIENTIFIC_PREMISES.tsv
PONDER_MATH_ELEGANCE_2026-07-31.md
```

## Exact mathematical object

For each `p` endpoint domain, let `A0` be the R05 reduced field operator, `g=1/w`, `ell` the
dimensionless constant-`nu` cross functional, and `C` its diagonal. Define

```text
A_tau = A0 + tau |g><g|,
S_nu(tau) = C - <ell,A_tau^-1 ell>,
Q_tau,eta = Q_field,tau + 2 nu ell + nu^2(C+eta).
```

Here `nu=k mu`, `k=a_Fprime/a_F^2`; `eta` is dimensionless in the `nu` coordinate. For the
representative `a_F=a_Fprime=2`, a direct `mu^2` curvature is `eta_mu=k^2 eta=eta/4`.

The rank-one resolvent identity gives the preregistered target formula

```text
S_nu(tau) = S_nu(0) + tau n^2/(1+tau m),
m=<g,A0^-1 g>,
n=<ell,A0^-1 g>=-integral u0/w dx,
u0=-A0^-1 ell.
```

This formula must be derived and checked, not assumed from numerical matrices.

## Scope and premise ledger before calculation

| Item | Treatment |
|---|---|
| founded metric/coframe arena | `DERIVED` as typed off-shell background |
| P4 response and F01 joint Hessian | `CONDITIONAL`; exact tested object only |
| massive crease root and `ell=1` | `CONDITIONAL` / `CHOSE`; frozen |
| R05/R06 and p-endpoint forks | `SUPPLIED`; all four carried |
| `tau` | `FREE_AND_EXPLORED` in `[0,tau_infinity]`; not physical stiffness selection |
| `eta` | `FREE_AND_SOLVED_FOR_THRESHOLD`; not selected |
| other wall-Hessian components | `OPEN_NOT_COVERED` |
| C2/Bach | inactive counterfactual; not used |
| EH and two-stage action route | conditional/open; not used |
| bootstrap/global-local closure | `WORKING` hypothesis; supplies no coefficient |
| PONDER | motivation only; no authority |
| action, carrier, source, physical boundary, time persistence, mass | `OPEN` |

## Required derivation and certification

1. Freeze every source by base blob, bytes, and SHA-256.
2. Re-derive the angular-penalty interpolation and prove its endpoints are R05 (`tau=0`) and the
   R06 field-core limit (`tau=s^2/J`).
3. Re-derive `m` for both p domains and the exact crossing
   `tau_critical=-1/m`; prove which side has field index one, zero, or none.
4. Derive `n=-integral u0/w` from self-adjointness and verify it directly.
5. Derive the Sherman-Morrison Schur surface and handle the singular crossing explicitly.
6. Certify outward intervals over every root in `s in (1,3)`—using the existing all-root proof and
   bracket—at nested >=80/100 decimal-digit settings.
7. Before seeing values, freeze normalized sample nodes
   `t=tcrit+alpha(1-tcrit)` for `alpha={1/4,1/2,3/4,1}`, where
   `t=tau/tau_infinity`.
8. At every sample, certify the dimensionless `eta_critical=-S_nu(tau)` and representative
   `eta_mu_critical=eta_critical/4`.
9. Treat `tau=tcrit` separately: if the lambda cross couples to the field zero mode, no finite
   `eta` can make the joint form nonnegative at the crossing.
10. Independently recompute the load-bearing formulas and intervals without importing primary
    sign results.

## Exact outcome classes

Choose one primary class:

- `TWO_PARAMETER_CONDITIONAL_STABILITY_THRESHOLD_SURFACE_DERIVED`;
- `TRACE_KERNEL_NEGATIVE__NO_WALL_HESSIAN_IN_SLICE_CAN_STABILIZE`;
- `NO_STABILIZING_REGION_IN_TRACE_ALIGNED_SLICE`;
- `DEGENERATE_CROSSING_REQUIRES_SEPARATE_BRANCH`;
- `CERTIFICATION_FAILED__THRESHOLD_OPEN`;
- `SOURCE_CONFLICT_STOP`.

## Fail-closed catches

Reject any package that:

- calls `tau` or `eta` derived, selected, native, or physical;
- calls this two-parameter slice the complete wall-Hessian space;
- drops any R05/R06 or p-endpoint branch;
- uses the R06 negative witness as though it were a relaxed Schur value;
- crosses `tau_critical` through a singular inverse without a separate limit analysis;
- loses the `nu=k mu` versus representative-`mu` factor of four;
- assumes a positive wall Hessian because stability is desired;
- uses C2/Bach, EH, bootstrap, PONDER, or familiar boundary mechanics as coefficient authority;
- substitutes a finite Galerkin convergence for interval certification;
- promotes conditional energetic nonnegativity to time persistence, stable matter, or a global
  bootstrap result.

## Maximum conclusion

At most: an exact conditional threshold surface in the declared two-parameter trace-aligned wall
slice, stating what a future native boundary/closure law would have to supply. No wall response,
action, carrier, source, matter branch, mass, time evolution, or bootstrap law is selected.

