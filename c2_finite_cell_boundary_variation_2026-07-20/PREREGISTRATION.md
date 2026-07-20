# Conditional C2 Finite-Cell Boundary-Variation Audit — Preregistration

Date: 2026-07-20  
Base: `eb06c7b5157ffb893ee3e6cd1d10de0816a07e3a`  
Branch: `codex/c2-finite-cell-boundary-variation-2026-07-20`  
Mode: CPU-only exact covariant variation, boundary decomposition, corner, and charge audit

## Whole question

For the frozen `UNIQUE-CONDITIONAL` four-dimensional metric-only `C^2` bulk, what exact boundary
symplectic potential, conjugate metric data, tangential corner flux, and unnormalized diffeomorphism
charge appear when the domain is a finite cell rather than a smooth boundaryless cap?

Does the bare conditional bulk supply a natural physical wall rule or break the CSN representative
freedom, or does it only expose the boundary phase space that a still-missing native selector must
complete?

This is an observing audit. It does not target a desired boundary condition, charge, mass, or
two-stage bridge.

## Whole frame

The pure problem varies the unrestricted four-metric on a finite four-dimensional region with
non-null boundary pieces and possible corners. The `C^2` bulk is retained only under the already
frozen pre-scale action-class premises. No static, toric, round, or reciprocal ansatz may be applied
before the covariant boundary potential is derived.

After the full potential is obtained, a Gaussian-normal non-null boundary decomposition may be used
as a coordinate/gauge diagnostic. It must retain both `delta h_ij` and `delta K_ij`, plus tangential
derivatives that become corner flux. A reduced reciprocal-toric sample may be used only as a
regression check.

Null wall limits, changing boundary location, unrestricted corner topology, and a complete source
sector remain separate layers unless derived.

## Premise and choice ledger

| Object | Status |
|---|---|
| Metric is the theory | `pinned-by-THEORY` |
| CSN pre-scale equivalence | `FOUNDING` |
| Four dimensions, metric-only, local covariance/locality, parity-even lowest curvature-square inventory, unrestricted variation | additional premises defining the frozen `UNIQUE-CONDITIONAL C^2` class |
| Bulk density `sqrt(|g|) C_abcd C^abcd` | `UNIQUE-CONDITIONAL`; overall coefficient not selected |
| Finite-cell ontology/static seal | `BINDING` in its named scope |
| Non-null smooth boundary piece | `pinned-by-HABIT / BOUNDED DECOMPOSITION`; null/degenerate pieces retained open |
| Boundary location and Gaussian-normal gauge in decomposition | fixed coordinate diagnostic, not a physical boundary condition |
| Boundary induced metric `h_ij` | free variation until candidate boundary classes are enumerated |
| Extrinsic curvature `K_ij` / normal derivative of `h_ij` | free variation until candidate classes are enumerated |
| Boundary/corner completion functional | `OPEN`; none inserted before the bare potential is recorded |
| Dirichlet, natural, Neumann, mixed, conformal, reflecting data | candidates to classify, not choices to impose |
| Primitive, reference, orientation, charge normalization | `OPEN` |
| GHY | GR/EH comparison object only; forbidden as a native `C^2` completion |
| Bootstrap | current on-shell requirement; no boundary functional supplied |
| `c`, `G`, electron mass | no numerical use; observational calibration excluded |
| Carrier/source/matter action | `OPEN`; excluded |

## Candidate boundary classes frozen before derivation

Retain separately:

1. clamped/metric-two-jet data fixing both `h_ij` and its normal derivative or `K_ij`;
2. induced-metric Dirichlet with a natural equation for the `delta K_ij` coefficient;
3. natural/free data setting both bare conjugate momenta to zero;
4. Neumann or mixed data after a separately declared Legendre/boundary functional;
5. conformal-class data and the common-scale null direction;
6. fixed trace versus trace-free extrinsic-curvature data;
7. tangential total divergences and their corner contributions;
8. conformally flat boundary/bulk strata where the bare potential degenerates;
9. non-conformally-flat strata with nonzero electric/magnetic Weyl boundary data;
10. null, signature-changing, singular, moving-wall, and alternative-corner branches as open;
11. normalized physical charge/mass as open even if an unnormalized Noether two-form is derived.

No class may be rejected because it looks unlike a reflecting wall or familiar GR boundary problem.

## Exact tests

1. Derive the curvature momentum `P^{abcd}=partial(C^2)/partial R_abcd` from
   `C^2=Riem^2-2 Ric^2+R^2/3`; verify `P=2C` with Riemann symmetries.
2. Derive the unrestricted covariant symplectic potential from integration by parts, rather than
   citing a boundary formula as UDT input.
3. Confirm that its bulk Euler-Lagrange tensor is proportional to the Bach tensor and record all
   convention/normalization freedoms.
4. In Gaussian-normal gauge on a non-null piece, decompose the normal flux into the coefficient of
   `delta K_ij`, the coefficient of `delta h_ij`, a tangential divergence, and corner flux. Track
   signs with the normal convention.
5. Prove which momentum is trace-free and evaluate the covariant potential on a pure common Weyl
   variation `delta g_ab=2 sigma g_ab`.
6. Evaluate the potential and Noether two-form on the conformally-flat round branch and on at least
   one nonzero-Weyl algebraic sample.
7. Enumerate which candidate boundary classes make the action differentiable without silently adding
   a completion. If an added Legendre term is discussed, keep it conditional and show its effect.
8. Derive the bare diffeomorphism Noether two-form and state why its coefficient, primitive,
   reference, integrability, and physical normalization remain open.
9. Verify common-homothety weights and whether the bare boundary objects can select an absolute scale.
10. Exercise catches against importing GHY, setting `delta K=0` without a status tag, equating
    conformal flatness with physical vacuum/masslessness, treating a vanishing bare charge as a mass
    theorem, or promoting a non-null decomposition to the complete UDT wall.

## Certification and falsification contract

`MATHEMATICAL_BOUNDARY_PHASE_SPACE_DERIVED_CONDITIONAL` requires an exact covariant potential,
non-null decomposition with both metric jets, corner term, pure-CSN null check, and independently
reconstructed load-bearing algebra.

`PHYSICAL_BOUNDARY_SELECTOR_FOUND` requires that one admissible class follow uniquely from existing
UDT premises without an inserted fixed datum, completion functional, reference, or normalization.
Multiple differentiable classes or a degenerate conformally-flat stratum falsify that conclusion.

If only the covariant potential is secure while the complete decomposition is convention-dependent,
bank the potential and mark the decomposition `VERIFIED-WITH-CAVEATS` rather than forcing a selector.

## Maximum allowed conclusion

At most this audit may derive the bare mathematical boundary phase space, corner flux, and
unnormalized Noether object inside the conditional `C^2` route, classify differentiable boundary
families, and identify the smallest still-missing physical boundary selector.

It cannot select the complete action, a physical boundary condition, a CSN representative, absolute
scale, `Xmax`, normalized mass/charge, source, carrier, EH bridge, or canon entry. No GPU solve,
repository reorganization, startup-control edit, or electron calibration is authorized.
