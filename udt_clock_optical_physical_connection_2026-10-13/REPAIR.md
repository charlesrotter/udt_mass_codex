# COC1 first source-preserving clarification

The initial coordinator candidate and researcher proof/check bytes remain
unchanged. Both actual direct reviewers independently identified this wording
defect before seeing each other's findings.

INITIAL_CANDIDATE C1 says, “An affine relabeling with the same first derivative
changes its cubic calibration.” That is incorrect if it means a change between
affine parameters. The vertex origin and source normalization -g(k,U)=1 fix the
affine parameter. An affine-to-affine transformation is linear.

The intended statement, already correct in researcher B's proof, is:

> An otherwise unspecified range label s=lambda+b(n)lambda^3+O(lambda^4),
> agreeing with normalized affine distance only to first order, changes the
> quadratic normalized-area coefficient. Such a cubic relabeling is generally
> non-affine. The geodesic round-trip clock preparation determines the needed
> cubic conversion instead of assuming it from tangent calibration alone.

No equation, sign, acceptance criterion, physical premise or computation changes.
The source-normalized affine parameter remains a unique geometric proof tool;
the operational question is how actual timing/area data determine its leading
relation to the chosen range, not whether its normalized definition is ambiguous.

## Scope of the scalar-averaging obstruction

The fidelity reviewer also identified overbroad prose in researcher_a/CANDIDATE.md
section4.2: “Scalar tomography necessarily uses signed combinations or optical
information.” The preceding proof excludes only nonnegative linear averaging
of the specified actual net leading PSW clock coefficients in its ultrastatic
control. It does not classify nonlinear reconstruction, other protocols or
finite records. Signed combinations and additional optical data are useful
examples outside that restricted averaging class, not an exhaustive theorem.

Read that sentence with this narrower scope. The parent initial candidate C3
already states the bounded averaging result correctly; no formula or test changes.
Neither the positive scalar reconstruction nor the adverse physical-attribution
conclusion is extended to an impossibility claim about all measurements.

The repaired central account must use these scopes. Actual re-review and final
version attestations, rather than the existence of this note, control acceptance.

## Maintained-summary precision in the same repair round

The first integration read required the compressed orientation to say
“nonpositive, including zero,” rather than imply every adverse coefficient is
strictly negative. It also states that timing together with the independently
measured clock tide supplies the cubic range conversion; duration alone does
not determine that tide. Both compressed summaries explicitly retain the same
physical metric connection for the scalar-complement Bianchi claim. The full
proof already contains those scopes. No new physical or mathematical result
is introduced by these clarifications.
