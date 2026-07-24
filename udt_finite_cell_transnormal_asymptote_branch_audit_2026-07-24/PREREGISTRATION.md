# Finite-cell transnormal/asymptote branch audit — preregistration

Date: 2026-07-24

Base: `a8501885fea2c2a7ff2ba9d08797f76b71a1f9c1`

Mode: metric-led exact CPU branch adjudication

Status: `PREREGISTERED_BEFORE_BRANCH_CALCULATION`

## Whole question

Apply the newly derived metric-native test

```text
B = h_u^-1(dphi,dphi),
dD/dphi = 1/sqrt(B(phi)),
X_phi = integral dphi/sqrt(B(phi))
```

to every registered finite-cell completion family and every current equation
family that could supply a complete finite-cell `(g,phi)` witness.

For each row determine separately:

1. whether it is a topology/completion type or an explicit field solution;
2. whether it supplies a physical metric/coframe;
3. whether it supplies a reciprocal clock leg with
   `T_clock=exp(Delta phi)`;
4. whether its `phi` is clock depth, angular reciprocal depth, another
   scalar, or unsoldered;
5. whether the observer-rest geometry `h_u` and event pairing are defined;
6. whether `B` is calculable and single-valued on `phi` levels;
7. whether the infinite-depth integral is finite;
8. whether the complete global pair diameter is calculable; and
9. whether any equality between depth reach and global `X_max` is derived.

No branch will be favored for resembling the desired universe.

## Frozen candidate universe

### U1 — completion taxonomy

All 12 rows, exactly once, from:

```text
udt_finite_cell_reciprocal_survival_density_audit_2026-07-23/
FINITE_CELL_BRANCH_ATLAS.tsv
```

They are `FC01` through `FC12`. Prefixes and topology labels may not be used
to promote a row to a solved field branch.

### U2 — equation/evidence families

All 28 rows, exactly once, from:

```text
udt_involutive_exchange_branch_availability_audit_2026-07-24/
BRANCH_EQUATION_FAMILY_REGISTRY.tsv
```

Every family is screened against the transnormal data contract. A family
with local equations, local jets, numerical relaxation, topology, or an
empirical profile is not a complete finite-cell branch unless all required
data coexist in one witness.

### U3 — exact calculable controls

The following are retained separately and must not be spliced:

1. conditional local WR-L clock-depth profile;
2. conditional reciprocal-toric angular-depth metric with arbitrary
   `A(phi),Omega(phi)`; and
3. conditional round capped toric `C^2`/Bach solution.

## Data contract

Each candidate receives one value for every gate:

| gate | required object |
|---|---|
| G01 | explicit nondegenerate physical metric/coframe |
| G02 | supplied observer clock leg/congruence |
| G03 | explicit `phi` field and profile |
| G04 | derived join `T_clock=exp(Delta phi)` |
| G05 | complete observer-rest spatial geometry |
| G06 | full global domain, cap/glue/boundary data |
| G07 | observer domain and event pairing |
| G08 | calculable `B=h_u^-1(dphi,dphi)` |
| G09 | transnormal `B=B(phi)>0` on the tested region |
| G10 | evaluable infinite-depth integral |
| G11 | valid global pair distance and diameter |
| G12 | one witness selected/on shell under its stated operator |

`YES`, `CONDITIONAL`, `OPEN`, `NO`, and `NOT_APPLICABLE` remain distinct.

## Exact derivations frozen

### D1 — conditional WR-L

Replay:

```text
B=exp(2phi)/(4X^2),
D=2X[1-exp(-phi)],
D(infinity)=2X.
```

Test whether any source closes the local-`X`/global-diameter join.

### D2 — reciprocal-toric angular-depth control

For

```text
g=-dt^2+A(phi)^2 dphi^2
  +Omega(phi)^2[exp(-2phi)dxi1^2+exp(2phi)dxi2^2],
```

derive `B`, `D`, and the endpoint convergence condition. Separately test
whether this `phi` is soldered to clock dilation.

### D3 — round capped toric control

For round spatial radius `b` in Hopf coordinates and the conditional map

```text
tan(eta)=exp(2phi),
```

derive:

- `B(phi)`;
- neutral-level-to-cap depth;
- full round spatial diameter; and
- their ratio.

Do not identify angular reciprocal depth with clock depth unless the metric
contains the required lapse relation.

### D4 — static/time-live distinction

- A smooth real static scalar on a compact boundaryless slice has a critical
  point, so `B>0` cannot hold globally.
- A pure time-live scalar `phi=t` can have nonnull spacetime gradient while
  its observer-rest spatial `B` is zero.

These statements constrain a global `D(phi)` but do not reject compact
geometry or mixed time-space profiles.

## Primary branch classifications

Each row receives exactly one:

- `FULL_GLOBAL_XMAX_EVALUABLE`;
- `CONDITIONAL_GLOBAL_DIAMETER_ONLY`;
- `CONDITIONAL_DEPTH_EVALUABLE_NOT_CLOCK_SOLDERED`;
- `LOCAL_CLOCK_DEPTH_ONLY_NO_GLOBAL_COMPLETION`;
- `FORMULA_ONLY_PROFILE_OR_ENDPOINT_OPEN`;
- `TOPOLOGY_ONLY_NO_COMPLETE_G_PHI_WITNESS`;
- `OBSTRUCTED_SMOOTH_GLOBAL_TRANSMORMAL_CLOCK_DEPTH`;
- `INELIGIBLE_NO_COMMON_WITNESS`;
- `OPEN_INSUFFICIENT_DATA`.

The misspelling `TRANSMORMAL` is forbidden in generated outputs; the
required label is `TRANSNORMAL`.

## Falsification contract

The verifier must reject:

- a missing or duplicate FC row or evidence-family row;
- a completion taxonomy row promoted to a field solution;
- a local WR-L `X` promoted to global `X_max`;
- angular reciprocal `phi` labeled clock depth without the lapse solder;
- a pure `phi=t` branch labeled as nonzero spatial distance depth;
- a smooth compact static scalar labeled globally `B>0`;
- omission of caps, angular scale, event pairing, or clock leg;
- a conditional action witness labeled native/unconditional;
- a finite depth integral labeled a global diameter without proof;
- a source identity change; or
- use of mass, density, `G_obs`, empirical fitting, or desired topology as a
  selector.

## Maximum allowed conclusion

At most:

```text
THE_REGISTERED_BRANCH UNIVERSE HAS BEEN COMPLETELY SCREENED FOR THE
METRIC-NATIVE TRANSNORMAL/ASYMPTOTE DATA CONTRACT; EXACT CONDITIONAL
DEPTHS MAY BE CALCULATED, BUT GLOBAL X_MAX IS PROMOTED ONLY IF ONE
COMPLETE CLOCK-SOLDERED PAIR-DIAMETER WITNESS PASSES ALL GATES.
```

No action, source, carrier, matter, mass, density, boundary charge,
canonization, navigation edit, GPU work, or repository reorganization is
authorized.
