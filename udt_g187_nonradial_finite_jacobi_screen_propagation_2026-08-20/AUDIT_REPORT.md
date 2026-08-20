# G187 audit report — finite nonradial Jacobi screen propagation

Date: 2026-08-20

## Primary landing

```text
FINITE_NONRADIAL_JACOBI_MAP_DERIVED_CONDITIONALLY
__G186_LOCAL_SCREEN_SEEDS_TWO_METRIC_FIXED_MODES
__NONRADIAL_SHEAR_EMERGES_WITHOUT_EXTRA_COEFFICIENT
```

Current grade: `EXTERNALLY_REVIEWED_VERIFIED_WITH_CAVEATS`.

## What was learned

For one supplied regular nonradial null query in the primary static-spherical metric, G186's local
orthogonal screen is not an isolated local construction. It supplies the initial screen of a
finite, exactly propagated Jacobi map.

The complete metric fixes two different screen-tidal functions:

\[
\mathcal T_\perp=\frac{L^2(rf'-2f+2)}{2r^4},
\qquad
\mathcal T_\parallel=\frac{L^2(rf''-f')}{2r^3},
\]

and their cross term vanishes in the natural orbital/reflection basis. The resulting finite map is
\(\mathcal D=\operatorname{diag}(D_\parallel,D_\perp)\), with both entries fixed by the metric,
the ray, and unit vertex data. One entry has the exact rotational-Killing form

\[
D_\perp=\frac{r\sin(\varphi-\varphi_o)}{\sin\alpha_o}.
\]

This is the first bounded bridge in the current clean kernel from the completed local pair screen
to finite nonradial angular propagation. It produces generic anisotropic screen response without a
fitted angular factor or a post-readout orchestra term.

## Internal evidence

- preregistered before implementation at commit `573d7ff0`;
- 20/20 production symbolic checks;
- 10,000 independent exact-Fraction metric jets;
- 220,000 independent exact assertions;
- independent connection and Riemann reconstruction with no production imports;
- exact flat-space and Schwarzschild controls;
- 15/15 repaired algebraic mutation catches;
- 14/14 separately labelled artifact-scope mutation guards;
- 6/6 frozen source hashes;
- 171-row premise audit with 754 historical dispositions;
- repository regression: 130 passed, 1 expected xfail.

## Caveats

The metric history, source event, initial nonradial null direction, affine normalization, and one
smooth regular branch are supplied. G187 does not select the physical ray population or derive an
emission law. The Jacobi map is not itself flux, luminosity, an observed sky pattern, or a native
electromagnetic theory. Strict radial rays, nonspherical and time-live ambient metrics, global
branching, and cut-locus aggregation remain outside this bounded theorem.

Fresh external gpt-5.4 review returned `G187_ACCEPTED_WITH_STATED_BOUNDS` after replaying the full
package and performing an additional off-script curvature check. It retained the caveat that the
Fraction replay is engine-independent rather than fully ansatz-independent. A fresh repair-only
follow-up then returned
`G187_CERTIFICATION_REPAIR_ACCEPTED__SCIENTIFIC_LANDING_UNCHANGED` after verifying all 31 sealed
payloads and rerunning the repaired catch layer and full package. The certification defect is
closed; the bounded scientific caveats remain unchanged.
