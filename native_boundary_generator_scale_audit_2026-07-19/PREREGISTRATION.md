# Native boundary-generator and scale-selection audit preregistration

Date: 2026-07-19

Base: `ad9e9bd5c27e4bfe40defcc225f81f2806a1c9f9`

Branch: `codex/native-boundary-generator-scale-audit-2026-07-19`

Compute: bounded CPU-only exact algebra and evidence audit; no GPU

## Whole question

Does the UDT metric supply enough native structure to promote the exact WR-L wall lapse flux
`Phi_N(X)=-2*pi*X` into a normalized conserved gravitational charge, and does that charge—together
with the accepted observational anchors `c_E,G_obs`, finite-cell closure, Common-Scale Neutrality,
and bootstrap—select absolute `M_tot` and `X_max` rather than only their ratio?

This is a **metric-led observing audit**. It is not licensed to choose EH, `C^2`, an auxiliary
field, a carrier, a source, a time slice, a boundary primitive, or a mass formula in order to obtain
closure.

## Premise ledger

| datum | status | not supplied |
|---|---|---|
| UDT core is scale-free | `pinned-by-THEORY/OWNER` | no physical common scale |
| ordinary-regime finite `c_E` | `pinned-by-OBSERVATION/OWNER` | no varying fundamental constant |
| measured `G_obs` | `pinned-by-OBSERVATION/OWNER` | no action or charge normalization |
| WR-L representative `A=1-r/X`, `N=sqrt(A)` | `DERIVED_CONDITIONAL` within WR-L axioms | no global selection of this branch or `X` |
| raw spherical lapse flux | `DERIVED_METRIC_LIMIT` | no conservation law or mass interpretation |
| global frame-shared `X_max` | `pinned-by-OWNER` as unknown output | no equality to WR-L `X` |
| native total mass | `OPEN` | no functional, source, generator, or normalization |
| finite cell and bootstrap closure | `pinned-by-THEORY` at structural/admissibility level | no boundary action or numerical selection equation |
| CSN | `pinned-by-THEORY` | no claim that it breaks global homothety |

The recorded static slice includes a curvature-singular WR-L seat under global extrapolation and is
not assumed to be the complete matter-bearing universe.

## Exact tests

1. Recompute from the metric, independently of archived scripts:
   - `Phi_N(r)` and `Phi_N(X)`;
   - `d Phi_N/dr`;
   - the static-slice Laplace-Beltrami equation for `N`;
   - its weighted curvature-volume identity;
   - all scaling under `r=X y`.
2. Determine whether the raw flux is radially conserved. A nonzero bulk divergence forbids calling
   it a Gauss charge without an additional constraint/source equation.
3. Audit every operation required to turn a raw flux into mass: action, presymplectic potential,
   symmetry generator, boundary primitive/counterterm, reference, orientation, and normalization.
4. Exercise two action-independent ambiguity tests:
   - overall action rescaling leaves stationary solutions unchanged while rescaling canonical
     charges;
   - adding an exact boundary derivative leaves bulk Euler equations unchanged while shifting
     boundary momenta/generators.
5. Construct the noncircular equation/unknown rank for `M_tot,X_max` with known `c_E,G_obs` and a
   dimensionless coefficient. Test the common homothety `M,X -> lambda M,lambda X` explicitly.
6. Ask whether CSN, finite-cell existence, or current bootstrap wording supplies a scale-breaking
   equation. Absence in the registered text is an `OPEN` result, not a no-go against a future
   complete matter-bearing solution.

## Candidate-source freeze

Before substantive adjudication, freeze all tracked base-tree sources containing any of:

- `lapse flux`;
- `boundary charge`;
- `normalized charge`;
- `Hamiltonian boundary`;
- `presymplectic`;
- `Noether`;
- `Komar`;
- `Xmax=alpha` or `X_{\max}=\alpha`;
- `homothety`;
- `Common-Scale Neutrality`; or
- `bootstrap`.

Also include the immediately controlling asymptotic-boundary package, the final A/B/C action
adjudication, the founding CSN/bootstrap/Xmax records, and the archived WR-L solution-space and
finite-cell boundary audits. Generated reorganization records and duplicate snapshots do not
become physics sources. The July-1 provenance firewall remains binding.

## Falsification and certification

The proposed native-charge closure fails at the current premise set if any of these occurs:

- `Phi_N(r)` is not radially conserved and no native constraint/source restores conservation;
- charge normalization changes under action scaling or an allowed boundary primitive;
- `c_E,G_obs` plus the proposed mass-radius relation retain a common one-parameter homothety;
- WR-L `X` must be supplied to compute the claimed output;
- a GR/EH, Misner-Sharp, Komar, or Wald formula is used affirmatively without a native action; or
- bootstrap/CSN supplies only admissibility or scale neutrality, not a second independent equation.

A positive closure requires all of:

1. a native off-shell action or equivalent variational law;
2. a differentiable finite-cell boundary completion;
3. a normalized conserved generator whose value is native total mass;
4. a globally selected metric/domain identifying `X=X_max` without circular input; and
5. an independent scale-breaking condition producing an isolated positive solution.

Every load-bearing calculation must be independently recomputed and mutation-tested. Historical
formulas may be used as negative controls or conditional readouts only.

## Maximum conclusion

At most this audit may establish one of:

- `NATIVE_BOUNDARY_CHARGE_AND_SCALE_SELECTOR_DERIVED`;
- `UNIQUE_CONDITIONAL_ON_EXPLICIT_ACTION_AND_BOUNDARY_PREMISES`;
- `RAW_METRIC_CURVATURE_BUDGET_DERIVED; CONSERVED_CHARGE_AND_ABSOLUTE_SCALE_OPEN`; or
- `OPEN_OR_CONFLICTED`.

It may not derive a numerical `X_max`, total mass, complete action, source, carrier, cosmology, or
canon entry. No time-live matter solve, GPU work, repository reorganization, or follow-on action
selection is authorized.
