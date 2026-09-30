# CCR1 controlling precision repair

This controls INITIAL_CANDIDATE.md and the interpretation of its initial checks.
Both direct reviews preserve the mathematical result subject to these precision
changes. The initial candidate, code, outputs and freezes remain unchanged.

1. **Tube coordinates.** “Smooth injective map” in section1 must explicitly mean
   a smooth rank-four embedding/diffeomorphism onto its image on a neighborhood
   of the relevant buffered compact shell. Its inverse coordinate functions are
   smooth, using ordinary sphere charts as needed. Smooth injectivity alone does
   not suffice (x↦x³ is a counterexample to that implication). “Regular tube” was
   intended as actual coordinates; the stronger description is the hypothesis
   required to make h a smooth spacetime tensor. One crossing, no returning
   intersection and support separation remain separate requirements. This
   limits the theorem to its intended regular coordinate sector, not caustics or
   rank-degenerate maps. Small-laboratory persistence includes C1 stability of a
   buffered compact embedding, in addition to regular geodesics and arrivals.

2. **Actual scope of initial checks.** The producer's conformal-control item in
   checks/check_curved.py takes the normalized shell delay α/a_e as an input and
   checks reduced interception/proper-clock algebra. It does not itself integrate
   an explicit original null ODE. The original label “original-null-ODE anchor”
   must be read with this limit. Its actual curvature computation and remaining
   identities remain valid; none is retroactively called an independent ODE solve.
   The mathematical reviewer supplies the actual independent supplement in
   review/math/direct_checks.py: original null residual and linearized RHS,
   explicit normalized polynomial integral, proper arrival and nonconstant drift
   in g=t²η, and direct clock-geodesicity/curvature checks. The polynomial is an
   algebra control, not the proof's smooth compact bump. The fidelity review also
   gives an independent conformal quadrature control. These are supplied curved
   mathematical comparisons, not CES1-prepared stationary UDT solutions. Reuse
   those actual checks; do not duplicate them to inflate independence or counts.

3. **Notation.** In the proof's support/cutoff sentences, use K_em=supp(w) for
   the compact emission-weight support; reserve K for the normalized null tangent.
   This resolves the initial overloading without changing any object or equation.

The curve/arrival equations, physical preparation, weights, score, sign proof
and separate all-laboratory quantifier are unchanged. No physical premise is
adopted or fitted. Both final reviewers must inspect this controlling repair
and the actual integrated central argument before final byte acceptance.
