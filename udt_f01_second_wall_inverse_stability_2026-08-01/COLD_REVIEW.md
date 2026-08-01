# Cold adversarial review — F01 inverse wall-stability surface

Date: 2026-08-01  
Agent: `/root/f01_inverse_cold_verifier`  
Frozen base: `46c763770f3f71376a0e57338c276ed3981ce36b`  
Historical verdict: **`PASS-WITH-CAVEATS`**  
Mathematical status after the registered finite-`beta` repair: **`PASS`**

## Scope and independence

This review covers the unique conditional F01 massive crease root, both owned `p` endpoint
domains, and only the declared trace-aligned `beta/tau` plus direct-`eta` wall-Hessian slice. It
does not cover the unrestricted wall Hessian, a native variation law, a physical boundary, an
action, carrier, source, global solution, time persistence, mass, or bootstrap return.

Reproduction command, from the repository root:

```bash
python3 udt_f01_second_wall_inverse_stability_2026-08-01/cold_verify_inverse_surface.py
```

The cold verifier imports and executes no primary package module. It independently:

1. reconstructs the preregistered source set from the frozen Git tree and checks every Git blob,
   byte count, SHA-256, working-tree payload, inventory row, and manifest row;
2. solves the `u=-A0^-1 ell` and `phi=A0^-1 g` boundary problems by first-order DOP853 shooting,
   using separate particular and homogeneous integrations rather than the primary closed-response
   substitution;
3. evaluates `n` both as `ell(phi)` and as `-integral u/w`, and evaluates `m` both from the
   shot response and the analytic overlap formula;
4. assembles a separate piecewise-linear finite-element field form with five-point Gauss element
   quadrature and checks the inertia below, immediately below, immediately above, well above, and
   at the R06 endpoint; and
5. compares only the resulting cold data—not code paths—with the repaired primary intervals.

Versions: Python 3.10.12, NumPy 2.2.6, SciPy 1.15.3, SymPy 1.13.1, and mpmath 1.3.0. The full
machine-readable record is `COLD_RAW.json`; the compact verdict is `COLD_RESULT.json`.

## Source identity

The independently selected source universe contains exactly 135 paths and 1,585,986 bytes. All
135 Git blobs, byte counts, SHA-256 digests, and current working-tree payloads match frozen base
`46c7637`. `SOURCE_INVENTORY.tsv` and `SOURCE_MANIFEST.sha256` reproduce that same set exactly.

The preregistration commit `1e6130f` is the direct child of the frozen base. No source conflict was
found.

## Re-derivation

For an aligned nonnegative angular trace-difference Hessian `beta`, direct angular minimization
gives

```text
tau(beta) = s^2 beta/(1+beta J),
beta(tau) = tau/(s^2-tau J),
tau_infinity = s^2/J.
```

Thus `beta=0` is R05, finite `beta>0` fills the open intermediate interval, and only
`beta->infinity` reaches the R06 zero-trace limit. Penalizing a trace difference is essential:
with a derivative-only angular block, an absolute one-wall trace could otherwise be removed by a
free constant shift. The repaired primary derivation now carries this distinction and agrees with
the cold symbolic checks.

For `g=1/w`, the exact overlap formulas are

```text
m_D = -J/s^2 - 2/[s^2(s-1)],
m_F = -J/s^2 - 2(4s^2-3s+1)/[s^2(2s-1)w(1)],
tau_critical = -1/m,
t_critical = tau_critical/tau_infinity.
```

With `u0=-A0^-1 ell`, self-adjointness gives

```text
n = <ell,A0^-1 g> = -integral u0/w dx.
```

Away from the field crossing, Sherman-Morrison gives

```text
S_nu(tau) = S0 + tau n^2/(1+tau m),
eta_critical(tau) = -S_nu(tau).
```

For the representative `a_F=a_Fprime=2`, `nu=(1/2)mu`, so the direct `mu^2` curvature is
`eta_mu=eta/4`. This factor is representational, not a physical normalization.

## Independent central values

The cold root and common integral are

```text
s*          = 1.6810236226618487
J           = 2.3268113669274615
tau_infinity= 1.2144690627322612
```

| `p` domain | `S0` | `n` | `m` | `t_critical` | `tau_critical` |
|---|---:|---:|---:|---:|---:|
| Dirichlet | 8.352994332353710 | -4.164969240231057 | -1.862655449834444 | 0.4420597934885044 | 0.5368679430696008 |
| free right | 8.044385241164594 | -3.823446038489633 | -1.484707746225685 | 0.5545906833093931 | 0.6735332273588029 |

The direct/Green `n` discrepancies are below `9e-16`; the direct/formula `m` discrepancies are
below `2.5e-15`. All boundary residuals are zero at printed precision except the free-right `u`
residual, `-8.9e-16`.

Cold `eta_critical` values at the preregistered normalized samples are:

| `alpha` | Dirichlet `eta` (`eta_mu`) | free-right `eta` (`eta_mu`) |
|---|---:|---:|
| `1/4` | 30.475147930675902 (7.618786982668976) | 50.840891003488721 (12.710222750872180) |
| `1/2` | 15.717592520738240 (3.929398130184560) | 26.321356315627451 (6.580339078906863) |
| `3/4` | 10.798407384092350 (2.699601846023088) | 18.148178086340369 (4.537044521585092) |
| `1` | 8.338814815769403 (2.084703703942351) | 14.061588971696811 (3.515397242924203) |

All 25 comparisons against the current repaired primary controls and interval certificates pass.

## Inertia and the crossing obstruction

The analytic rank-one result is load-bearing:

- below `tau_critical`, the field restriction retains index one, so setting `nu=0` proves that no
  direct `eta` can make the joint form nonnegative;
- at `tau_critical`, `z=A0^-1 g` is the field zero mode and `ell(z)=n` is nonzero, so the coupled
  block has determinant `-n^2<0` for every finite `eta`; and
- above `tau_critical`, the field core is positive and the joint form is nonnegative exactly when
  `eta>=-S_nu(tau)`, with equality semidefinite.

The independent 600-element FEM corroborates the change from one negative field direction at
`0.999 tau_critical` to zero negative directions immediately above the analytic crossing in both
domains. It also gives zero negative field directions at the R06 endpoint. FEM convergence is
corroboration, not the crossing proof.

## Historical caveats and repaired-primary agreement

The initial package earned `PASS-WITH-CAVEATS` because it drew the intermediate effective `tau`
family without deriving a finite admissible aligned germ. Before this cold record was finalized,
the package registered and implemented the required repair:

1. the finite trace-difference elimination and `tau(beta)` map were added;
2. endpoint, monotonicity, hard-pin-limit, and inverse controls were added;
3. `beta` was premise-stamped as free-and-explored, not supplied, selected, native, or physical;
4. finite-`beta` promotion to the R06 endpoint and finite-`eta` crossing mutations were added; and
5. the conclusion ceiling remained unchanged.

The repaired primary evidence agrees with every cold central value and retains the correct scope.
The primary adaptive midpoint verifier is still best described as a separately coded same-formula
reconstruction; the DOP853 and FEM paths in this review supply the distinct-method check.

At the time of the cold return, the remaining steps before banking were bookkeeping only: link the
cold result from the final report, replace its future-tense review wording, and build/verify the
package manifest after every repair and cold artifact is final.

## Final ceiling

The mathematical result after repair passes within the declared conditional slice. The preserved
historical package grade is `PASS-WITH-CAVEATS` because the repair and cold evidence were required
after the initial primary result.

At most, the package derives a conditional inverse threshold target describing what a future
native closure law would have to supply in one trace-aligned wall-Hessian slice. It does not select
`beta`, `tau`, `eta`, a wall response, boundary, action, carrier, source, matter branch, mass,
time-persistent state, or bootstrap law.
