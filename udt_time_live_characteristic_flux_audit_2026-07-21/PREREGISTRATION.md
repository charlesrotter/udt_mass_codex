# UDT full time-live characteristic and boundary-flux audit — preregistration

Date: 2026-07-21

Base: `21cfeb8f25fe18afe5a5a924ea073a9cfc24238b`

Branch: `codex/udt-time-live-characteristic-flux-audit-2026-07-21`

Mode: CPU-only exact symbolic audit. No numerical evolution is authorized.

## Whole question

Given the exact current UDT finite-cell, Reciprocity, Common-Scale Neutrality (CSN), static-seal,
co-presence, complete-coframe, and bootstrap statements, together with each of the two separately
authorized conditional P05 metric bulk lanes, does allowing the complete metric to be time-live
derive all of the following without adding a boundary choice?

1. the causal/characteristic type and motion of the finite-cell seal;
2. a complete allowed boundary variation class (polarization);
3. vanishing or integrable symplectic flux, including the angular and reciprocal sectors;
4. the required boundary and corner functional; and
5. constraint-preserving propagation sufficient to open P06.

The audit is **metric-led / observing**. It will not require a particle, smooth lump, familiar GR
boundary prescription, or desired selector outcome.

## Exact bounded arena

The positive local reciprocal representative is

```text
ds^2 = -c^2 exp(-2 phi) dt^2 + exp(+2 phi) dr^2 + q_AB dx^A dx^B,
q_AB positive definite,
```

with arbitrary time, radial, and angular dependence retained in `phi` and in the complete metric
perturbation. The displayed block is not promoted to a complete diagonal ansatz: off-diagonal,
angular-shape, lapse/shift, and full-coframe completions remain counted as open fields or branches.

Exact covariant or local principal-symbol statements will be made for regular four-dimensional
Lorentzian points. Degenerate/type-changing points will be retained as an explicit unclassified
branch rather than inferred from an inverse-metric calculation.

The conditional bulk lanes are kept separate:

- **L01:** pre-scale metric-only `C^2 + beta E4`, Bach bulk equation, fourth order;
- **L02:** post-scale metric-only `EH + Lambda + beta E4`, Einstein-Lambda bulk equation, second
  order; and
- **L03:** two-stage bridge, retained as `NO_OPERATOR`, not varied.

All seven P03/P04 field realizations remain in the completeness census. Only the metric-only
realization has a P05 bulk operator. No characteristic equation is invented for an independent
`phi`, coframe, projector, multiplier, bridge, or connection.

## Premise ledger

| object | status in this audit | source or limit |
|---|---|---|
| positional dilation, Reciprocal-c, dual Reciprocity, CSN | `FOUNDING` | `UDT_NATIVE_ACTION_COLD_PACKET.md` |
| reciprocal exponential comparison | `DERIVED / CONDITIONAL` | composition plus registered regularity |
| positive local reciprocal Lorentzian representative | `POSIT / CHOSE / CONDITIONAL` | cold packet; not a selected global metric |
| arbitrary positive `q_AB` and all time/angular dependence | `free-and-explored` | no roundness or staticity imposed |
| full ten-component metric perturbation `h_ab` | `free-and-explored` inside L01/L02 | unrestricted P05 metric variation |
| static seal `phi=0`, `delta phi=0`, normal derivative free | `CANONIZED / SCOPED` | static `phi` sector only |
| time-live seal as a regular level surface `phi=0` | `CONDITIONAL EXPLORATORY EXTENSION` | not promoted to canon |
| fixed, moving, null, timelike, spacelike, and type-changing seal branches | `free-and-explored` | none selected in advance |
| L01 and L02 actions/operators | `CONDITIONAL` | P04/P05 owner-authorized comparison lanes |
| L03 bridge | `OPEN / NO_OPERATOR` | no functional or matching map supplied |
| Levi-Civita connection in L01/L02 | `CHOSE / CONDITIONAL` | part of each P05 lane |
| local covariance and locality | `CHOSE / CONDITIONAL` | part of each P05 lane |
| diagnostic harmonic or de Donder-plus-trace quotient | `COMPARISON_ONLY` | not a physical UDT gauge |
| EH GHY/Dirichlet, Neumann, mixed, and characteristic completions | `COMPARISON_ONLY` | no completion adopted |
| C2 Ostrogradsky boundary pairs | `DERIVED STRUCTURE / CONDITIONAL LANE` | existing exact boundary variation |
| Euler coefficient `beta`, exact-divergence and potential improvements | `FREE / OPEN` | preserve bulk equations; may change boundary data |
| complete coframe lift and time-on/angular seal action | `OPEN` | multiple inequivalent parent witnesses |
| bootstrap | `WORKING / ON-SHELL` | no off-shell functional supplied |
| carrier, source, matter action, mass, scale, charge | `OPEN / EXCLUDED` | not used |
| `c` | `FOUNDING observational conversion anchor` | retained symbolically; `c=1` only as a reversible algebra unit check |
| GPU, PDE relaxation, time integration | `EXCLUDED` | no numerical solve in this audit |

## Boundary and time-live branches

The audit must retain at least:

1. no time-live extension of the static seal has yet been selected;
2. fixed non-null mirror/fold comparison;
3. moving timelike seal;
4. moving null/characteristic seal;
5. moving spacelike seal;
6. type-changing or degenerate seal;
7. null WR-L causal horizon, without identifying it with the finite-cell/CMB fold; and
8. quotient, crossing, or internal-match interpretations.

For the conditional level-set branch, differentiating `phi(t,r_b(t),x^A_b(t))=0` will be used only
as kinematics. It may relate boundary velocity to the first jet of `phi`; it may not be counted as
an equation selecting either quantity.

## Exact algebra to be attempted

1. Reconstruct

   ```text
   g^-1(d phi,d phi)
   = -exp(2 phi) phi_t^2/c^2 + exp(-2 phi) phi_r^2
     + q^AB phi_A phi_B
   ```

   and its seal specialization. Produce exact witnesses for every regular sign class and prove
   conformal preservation of the sign/zero set.
2. Derive the fixed/moving level-set tangency relation and compare the seal normal with the metric
   characteristic cone. Do not assume that the seal is null.
3. Build the full ten-component flat-point principal matrices for the linearized
   Einstein-Lambda and Bach operators from their covariant principal formulae. Verify generic
   gauge/Weyl kernels, null-rank changes, and the simple versus double metric-null factors. The
   flat-point calculation is a local principal-symbol check, not a global background solution.
4. Carry the exact Noether identities into a time split and classify what they do and do not imply
   about constraint propagation at a boundary.
5. Reconstruct the non-null canonical boundary symplectic structures:

   ```text
   L02: Omega_boundary = delta pi^ij wedge delta gamma_ij,
   L01: Omega_boundary = delta Pi_h^ij wedge delta h_ij
                           + delta Pi_K^ij wedge delta K_ij,
   ```

   including the scalar seal tangent and all residual angular/off-diagonal slots. These formulae
   classify canonical pairs; they do not adopt their normalization as UDT physics.
6. Construct at least two inequivalent maximal flux-free boundary polarizations compatible with
   every supplied seal clause, or prove that the time-live identities eliminate all but one.
7. At principal level, build explicit time-dependent reciprocal-sector and angular-sector wave
   packets/first jets showing whether flux can survive while `delta phi=0`. These are local
   counter-witnesses, not global solutions.
8. Re-audit the Euler, exact-divergence, potential-improvement, Legendre-transform, orientation,
   generator, and corner ambiguities after the time split.
9. Census all 21 lane/field pairs and every registered boundary type for P06 readiness.

## Candidate outcomes

Exactly one final selector classification will be used:

- `TIME_LIVE_UNIQUE_BOUNDARY_SELECTOR_DERIVED`;
- `TIME_LIVE_REDUCES_BUT_DOES_NOT_SELECT_BOUNDARY_DATA`;
- `TIME_LIVE_DOES_NOT_REDUCE_STATIC_UNDERDETERMINATION`;
- `TIME_LIVE_EXTENSION_INCONSISTENT_WITH_CURRENT_FOUNDATION`; or
- `AUDIT_BLOCKED_BY_MISSING_OPERATOR_BEFORE_SELECTOR_TEST`.

The first outcome requires one and the same complete polarization and integrable functional across
every retained compatible causal branch, with no free Euler/improvement/corner ambiguity and no
unvaried extra field. A unique characteristic cone alone is insufficient. A stable or convenient
numerical evolution is also insufficient.

## Falsification and certification contract

The unique-selector hypothesis fails if any one of the following survives current UDT premises:

- two regular causal types for the seal;
- two inequivalent complete flux-free polarizations;
- a nonzero angular/off-diagonal symplectic flux compatible with the scalar seal wire;
- a free boundary functional improvement changing momenta/corners;
- an unselected coframe or extra-field characteristic;
- or a boundary branch for which the operator/polarization is undefined.

Required mechanical gates:

- exact rational/symbolic equality only; no floating tolerances;
- all 10 symmetric metric components included in each principal matrix;
- gauge and Weyl kernel witnesses checked by direct multiplication;
- at least one timelike, one null, and one spacelike seal-normal witness;
- both L01 and L02, all 21 field pairs, and every boundary branch counted exactly once;
- at least two explicitly distinct seal-compatible zero-flux polarizations tested;
- deliberate corruptions must be rejected by a non-importing verifier;
- parent source hashes and repository frozen-manifest gates must replay.

## Maximum allowed conclusion

```text
TIME_LIVE_CHARACTERISTIC_AND_BOUNDARY_FLUX_SELECTOR_STATUS_CLASSIFIED
```

Even a positive result would be conditional on the exact lane and time-live seal premises. This
audit cannot select a native bulk action, physical coframe, carrier, source, mass, scale, charge, or
global universe. No P06 solve, numerical evolution, GPU work, canonization, or startup-control edit
is authorized.

