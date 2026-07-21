# Reciprocal-plane projector frame-principle audit — preregistration

Date: 2026-07-21

## Frozen question

Is preservation of the spacetime reciprocal clock/radial **two-plane projector**, rather than a
full four-axis reciprocal involution, the minimal complete frame structure compatible with founding
UDT Reciprocity and Common-Scale Neutrality?

This audit tests the mathematical content and scope of that candidate. It does not assume that the
internal founding pair has already been globally realized as a spacetime plane, and it may not adopt
projector parallelism merely because it avoids the full-pair obstructions.

## Base and scope

- base: `ec8250935d74a2218f31a09f5611bd0e5e4f40e0`;
- computation: CPU-only exact symbolic and independent rational algebra;
- connection class: torsion-free Weyl/conformal connections of a supplied conditional
  four-dimensional Lorentzian conformal metric;
- geometric data: a supplied metric-orthogonal rank-two Lorentzian projector `P`, its positive
  rank-two complement, and the founding reciprocal character inside `im(P)`;
- complete local integrable class: block-orthogonal `2+2` metrics with unrestricted intrinsic base
  and screen metrics and unrestricted cross-dependence before the projector equation is imposed;
- additional witnesses: arbitrary reciprocal radial profile, arbitrary angular curvature, round
  screen, trace-free base/screen shear, nonintegrable shift/twist, and all eight registered constant
  nonzero-cross metrics.

Not covered: torsionful or general non-Weyl connections, a derivation of the global spacetime plane
realization, global singular/degenerate distributions, action or field equations, boundary
functional, topology, carrier, matter source, mass, scale, GPU work, or canonization.

## Premise ledger

| Item | Stamp | Role |
|---|---|---|
| Founding reciprocal internal clock/ruler pair and exponential character | `pinned-by-THEORY` | Pointwise internal structure |
| CSN conformal class | `pinned-by-THEORY` | Connection must be representative-covariant |
| Spacetime rank-two reciprocal plane/projector | `CONDITIONAL_REALIZATION` | Supplied object under transport audit |
| Metric-orthogonal positive complement | `DERIVED_PER_SUPPLIED_METRIC_AND_PLANE` | Complete screen projector |
| Torsion-free Weyl connection | `pinned-by-HABIT / CONDITIONAL_COMPARISON` | Exact bounded connection class |
| Projector parallelism `nabla P=0` | `free-and-explored` | Candidate frame principle, not current authority |
| Individual generator parallelism `nabla L=0` | `NOT_ASSUMED` | Stronger parent condition retained only for comparison |
| Integrability, zero mixed twist, and umbilicity | `TO_BE_DERIVED_OR_REFUTED` | Possible existence consequences |
| Round screen, Hopf/toric structure, carrier, action | `EXCLUDED_AS_SELECTOR_INPUT` | Downstream diagnostics only |

## Preregistered mathematical candidates

For an adapted local split

```text
g = h_ij(x,y) dx^i dx^j + q_AB(x,y) dy^A dy^B,
P = diag(I2,0),
```

derive rather than assume:

1. uniqueness or residual freedom of a torsion-free Weyl connection satisfying `nabla P=0`;
2. necessary and sufficient conditions on `partial_A h_ij` and `partial_i q_AB`;
3. the Weyl one-form in every compatible case;
4. behavior under `g -> exp(2 sigma)g`;
5. whether arbitrary reciprocal depth `phi` inside `h` is allowed;
6. whether intrinsic angular connection and curvature inside `q` are allowed;
7. whether trace-free cross-shear or nonintegrable twist is allowed; and
8. what holonomy remains inside each preserved plane.

## Required exact witnesses

- arbitrary static reciprocal warped product
  `h=diag(-exp(-2phi),exp(2phi))`, `q=R^2 q0(y)`;
- a curved/round angular screen with arbitrary `phi` and `R`;
- a nonzero trace-free `partial_i q` shear obstruction;
- a nonzero trace-free `partial_A h` shear obstruction;
- a nonintegrable horizontal-shift/twist obstruction;
- all eight constant nonzero-cross lift metrics at `mu=4,9`;
- two inequivalent `phi` profiles sharing the same projector-compatible screen, proving the
  projector law does not select `phi`; and
- a comparison showing `nabla P=0` does not imply `nabla L=0`.

## Preregistered falsifiers

The projector principle is not a complete unconditional UDT frame law if:

- the spacetime plane itself remains unrealized or degenerates without a continuation rule;
- torsion-free projector parallelism silently removes allowed twist/shear sectors;
- existence requires an unselected warped/product restriction;
- the law freezes or selects `phi` only by importing generator parallelism;
- CSN representative changes alter the affine connection rather than shift its Weyl one-form;
- angular curvature is removed rather than retained inside the screen connection;
- uniqueness is mistaken for existence or physical authority; or
- the result is used to infer an action, topology, carrier, source, or mass.

## Certification contract

Acceptance requires:

1. exact full-tensor derivation of the projector equation, not selected components;
2. necessary and sufficient existence conditions in the declared integrable block class;
3. a Frobenius/torsion proof for nonintegrable distributions;
4. the full witness and countermodel list above;
5. independent standard-library rational reconstruction and exercised overclaim catches;
6. source/status review separating internal Reciprocity, plane realization, connection comparison,
   and physical authority; and
7. repository, frozen-manifest, navigation, tests, and dirty-checkout gates.

## Maximum allowed conclusion

`UDT_RECIPROCAL_PLANE_PROJECTOR_FRAME_STATUS_CHARACTERIZED`.

The strongest permissible result is
`UNIQUE_TORSION_FREE_CSN_CONNECTION_IF_AND_ONLY_IF_INTEGRABLE_UMBILICAL_SPLIT`, with all realization,
transport-authority, omitted-sector, and physical-conclusion qualifications retained.
