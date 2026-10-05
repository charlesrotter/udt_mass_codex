# Exposed clarification and ceiling-counterexample re-review

CLARIFICATIONS.md resolves the exact section3 quantifier objection without
changing the frozen candidate. Its eventual-tail language matches the proof.
The surviving b_*=0 result is unchanged; no earlier-history no-crossing claim
is accepted. Verdict remains VERIFIED-WITH-CAVEATS for the reviewed conditional
attachment, with this wording objection now CLOSED.

After explicit parent exposure, read AFFINE_CEILING_COUNTEREXAMPLE.md,
check_ceiling_exact.py, CEILING_CHECK_FREEZE.json, CEILING_EXACT_RESULT.json,
checks/ceiling_exact.json and METHOD_REFERENCES.md. The additional conditional
counterexample is sound: a=3.001,m=1,H=.18,E=1 and strict negative b_* near its
source bound satisfy a>3m, f(a)>0, Omega²>0 and outward escape. Defining the
source phase/receiver retarded origin from the limiting U/P values supplies
that limiting incidence; its Jacobian remains nonzero. This is a conditional
construction, not selection of physical histories.

For S=sqrt(1+H²b_*²), w²=s²/S² satisfies
d(w²)/dr=2b_*²(r-3m)/(S²r^4)>0 for r>=a. Therefore 1/w decreases, and each
exact rational right-endpoint q with q²w²<=1 is a valid lower bound on its
whole subinterval. The omitted integrand1/w-1 is strictly positive. The
certificate gives J=S C>341133/100000 and S>14/5, whence

    B=J/H-E/(H² S)>8991379/1134000>0.

Thus sufficiently late D_o lies ABOVE1/H while converging to it. This refutes
a universal ceiling interpretation within this declared conditional family.
It does not overturn the positive-deficit b_*=0 tail, prove an earlier
crossing/reversal, or refute a different physical separation definition.
The orbit is not certified stable or observationally appropriate; no solar
recovery or complete GR-filter admission is inferred from source existence.

Independently reconstructed the saved exact certificate using Fraction,
without the parent's bound-generator or integer-square-root code. Verified
every saved w², interval coverage, source restriction, lower sum and final
rational B bound. A deliberately doubled first q failed its exact bound,
as required. CERTIFICATE_RESULT.json and raw stdout/stderr retain the result;
actual exit0, empty stderr. With2 conservative exact-control cases, total
attempted count is73 including the initial finite-domain failure. No additional
floating-point solve or timeout was used.

METHOD_REFERENCES keeps mathematical definitions separate from imported physics.
I independently inspected Bolos's source and convex-normal-neighborhood caveat
before OAA exposure. I did not independently inspect the second paper's full
passages; no result here relies on its dynamics or an unverified equality of
distance types. The counterexample proof and endpoint definition stand on their
displayed arguments, with literature as method attribution only.

No mathematical or fidelity objection remains unresolved in the exposed
candidate-plus-clarification-plus-counterexample at this scope. Final central
integration, descendant coverage, version bindings and banking are still to
be reviewed on their actual files; this is not that final attestation.
