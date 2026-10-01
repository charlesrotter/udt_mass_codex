# PSW1 comparison addendum — clock reconstruction versus response identification

Verdict: **ACCEPT WITH EXPLICIT LIMITS as a subsection of Route A**, not a new
route or a native field-law derivation. The proposed conditional implication is
correct. Its useful addition is an ideal clock-record interpretation of the
already known Ricci response; the physical identification and completeness remain
UNADOPTED, as in FE1. No scientific CPU calculation was needed or performed.

Reviewer `/root/psw_fidelity`, 2026-10-01, same inherited model and exposed context
as CROSS_REVIEW.md. Parent supplied the proposed comparison before this review.
SOURCE_FIRST.md and CROSS_REVIEW.md remain unchanged. Branch/head independently
rechecked: grok, 4953c9ae806d42f0042d4fac14682db12c93143c.

## Mathematical implication

For the same geometric preparation and local regularity as Route A, define the
ideal record for each future unit timelike U by

    c(U) = -6 lim_(L->0) [(1/3) sum_i log p_L(e_i)] / L^2.

The proved coefficient gives c(U)=Ric(U,U), independently of the chosen
orthonormal rest triad. This is an exact coefficient recovered in the limit;
it is not equality of a finite noisy estimator with Ricci. The local remainder
bounds may depend on U. No uniform limit over the noncompact unit hyperboloid,
observer population or invariant observer probability measure is required.

These records determine a symmetric tensor C uniquely **when the records arise
from one such smooth metric**, because existence is then supplied by C=Ric.
For uniqueness, if a symmetric difference B vanishes on every unit timelike U,
homogeneity makes B(v,v)=0 on the open future timelike cone. A quadratic
polynomial vanishing on an open set is identically zero, hence B=0. Arbitrary
empirical records need not satisfy this quadratic consistency; their existence,
coverage and measurement errors cannot be skipped by calling C reconstructed.
This also reconstructs Ricci, not the full Riemann/Weyl tensor or metric history.

Now explicitly propose, without adopting,

    E_response = a C + q g,      a != 0.

Here q is a scalar trace contribution and a is a declared nonzero normalization
(a constant suffices; pointwise nonzero a has the same algebraic consequence).
The identification must describe the **complete trace-free response**, not just
one leading term of a potentially richer response. Under DDR's actual specified
symmetric-response/full-pair hypotheses,

    TF(E_response)=a TF(Ric)=0
    iff Ric=(R/4)g.

Contracted Bianchi in dimension four then gives dR=0 and Ric=Lambda g on each
connected smooth solution region. No separate off-shell conservation of
E_response or Ricci has been assumed. If a vanishes anywhere the pointwise
equivalence there is lost; that is why the nonzero domain qualification matters.
Lambda's sign/value is not determined, and Weyl/initial/global data remain free
at the inherited conditional scopes. This is exactly the existing conditional
Einstein branch, not a new equation or prediction.

## FE1 comparison and strongest objection

I inspected FE1's controlling files directly:

| Path under udt_field_equation_principle_design_2026-09-13/ | SHA-256 |
|---|---|
| DECISION_PACKET.md | f7e915dd01b4ffc803c6a55ab76310f5efc802971b060fbf9c4897c01c4118c5 |
| CANDIDATE.md | 8215f1aea8a272dbb869bee96f322517f7495ba636dcd5946c376f363d8dab17 |
| DERIVATION.md | cf8234d7835c917ac343a22e45796c2df84e42095a1b7141f6ae526a4374d47c |

FE1's reviewed UNADOPTED proposal defines a geodesic-volume Hessian with exact
value Ric, then proposes putting that tensor into DDR's response slot. It already
retains nonzero normalization/pure-trace freedom and obtains the same
trace-free-Ricci/Bianchi conclusion. Its decision packet explicitly separates
physical response identification from the further choice that the infinitesimal
coefficient exhausts the response. PSW1 does not repair those missing premises.

The difference here is an ideal prepared-clock record map for the same tensor,
rather than a tangent-volume-density coefficient. This is a useful operational
interpretation and cross-link between existing conditional results. It is not a
newly selected response, new solution class, stronger empirical case or independent
derivation of the Einstein branch from the founded premises.

**Strongest objection:** learning how a tensor can be reconstructed does not
show that physical reciprocity balances that tensor, that it is the complete
response, or that the selected laboratory coefficient is the additional positional
effect. Higher derivatives, other curvature information and other response
constitutions have not been excluded. DDR's adoption does not adopt the proposed
identification by substitution. No preferred observer is introduced by ideal
all-U reconstruction, but the reconstruction quantifier is not physical
population selection or proof that every such laboratory is realized.

**Survivor:** given the explicit identification, the familiar consequence is
exact and immediately testable by the prepared-clock coefficients. Without it,
the record reconstruction remains useful conditional geometry. J1 stays open.

**Smallest required presentation guard:** place “UNADOPTED complete trace-free
response identification” before the displayed response equation; immediately
state that the consequence repeats FE1/the existing conditional Einstein branch.
Use “ideal coefficient reconstruction” rather than suggesting demonstrated
experimental measurement or full response completeness. Do not recommend adopting
the identification merely to obtain a nonzero angular mean or Lambda>0.

With those limits, the subsection improves decision utility: it identifies the
exact extra physical step that would recycle the familiar branch and explains
why measuring/reconstructing Ricci alone does not close that step. The substantive
recommendation should remain the justified physical-attribution question, not a
larger vacuum survey or an automatic FE1 revival.
