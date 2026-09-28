# CRV1 direct adversarial review

2026-09-28, reviewer `/root/crv1_review`. Verdict:
**VERIFIED-WITH-CAVEATS for the repaired conditional mathematical comparison.**
One density-sign convention defect was found and repaired without changing the
scientific premise, witness or conclusion. Physical response identification,
native off-shell conservation and scientific promotion remain OPEN/UNPROMOTED.

Source-first reconstruction was sealed in SOURCE_FIRST_PINS.json before direct
candidate exposure. That report records context/model limitations, sources,
independent argument and a different original exact metric witness. This direct
stage then read INITIAL_CANDIDATE.md, DISCOVERY.md, CANDIDATE_FREEZE.json,
check_conservation.py, checks/AUTHOR_EXACT.json and the premise-audit receipt.
It subsequently read REPAIR.md, REVIEWED_RESULT.md and DECISION_BRIEF.md.
DIRECT_REVIEW_PINS.json pins the exact versions and verifies the frozen evidence
and dispatched source hashes. The full406 premise pass is attributed to the
parent's recorded execution, not independently rerun here; the receipt discloses
that separate stderr and resource measurements were not captured/enforced.

## Argument assessment

1. The fixed-metric scalar-completion theorem is valid: metric compatibility
   gives div(S+qg)=j+dq; closedness of j is necessary and, on the stated
   contractible region, sufficient. The candidate correctly separates global
   exactness and the stronger natural-finite-jet primitive problem. In
   particular, passing curl tests on metrics does not construct a natural
   operator or prove variationality.
2. For constant a, contracted Bianchi gives j=(a/4)dR for
   S=a(Ric-Rg/4). Therefore E=aG+Cg follows under the added conservation
   requirement. Choosing universal constants a,C makes the exhibited action
   aR-2C consistent with the stated inverse-metric variation. DDR remains
   TF(E)=0, not E=0. Constant R on a connected DDR solution was already a
   consequence of the conditional Ricci class; conservation is not being
   incorrectly credited with selecting that class or selecting R.
3. S=TF(R Ric) is a legitimate smooth local natural comparison tensor. Direct
   differentiation gives j=Ric(grad R,·); the nonzero exterior derivative at
   the witness event excludes every smooth scalar completion near it. Its
   failed homothety/flat-linear-shape conditions and lack of UDT/GR-filter
   admission are disclosed. It neither defeats RMS1's full conditional route
   nor proves a physical no-go result.
4. The compact-support diffeomorphism variation has the stated inverse-metric
   sign and establishes the full Euler response's off-shell divergence.
   Assuming the action is a premise of this Noether direction, not a deduction
   from tensor covariance. Excluding extra independent fields is essential;
   otherwise their Euler expressions enter the identity.
5. The inverse-variational theorem is used conditionally, with order, naturality,
   symmetry, fixed signature, off-shell identity and the stronger smoothness
   hypothesis retained. It is not being used as an arbitrary-order converse or
   an assertion of unique action/native ownership. The Lovelock alternative
   retains its full natural smooth second-order metric-operator domain.

For the last point I inspected the primary texts, including the relevant
definitions and theorem statements:

- Anderson–Pohjanpelto, Theorem 1, arXiv:1202.5811v1:
  https://arxiv.org/html/1202.5811v1 . Fixed arbitrary signature is explicit;
  local variationality and the everywhere-smooth natural-Lagrangian conclusion
  must be distinguished. Four dimensions lie in the latter theorem's allowed
  dimension classes. The reference was parent-supplied during source-first work.
- Navarro–Navarro, Definition 1.1 and Theorem 2.6, arXiv:1005.2386v4:
  https://arxiv.org/html/1005.2386v4 . At dimension four its basis contains the
  metric and Einstein tensor after consistent raising/lowering. Smooth natural
  operators on the full prescribed-signature second-jet bundle are the relevant
  arena, not arbitrary formulas defined only on a special solution family.

These are literature-supported conditional applications, not independently
reproved classification theorems. No empirical or physical premise follows
from either citation.

## Defect, survivor and repair

Initial candidate section 5 says the conversion is T^{ab}=+sqrt(|g|) E^{ab},
after defining E by inverse-metric variation of I. For the SAME action, changing
to covariant-metric variation gives

    delta g^{ab}=-g^{ac}g^{bd} delta g_cd,
    T^{ab}=-sqrt(|g|) E^{ab}.

The plus density belongs to -I. This was a sign/convention defect, not a failure
of the inverse-existence argument: either overall sign satisfies the theorem's
assumptions, and reversing the constructed action restores the desired response.
The strongest survivor is the entire conditional existence/obstruction result.
The smallest repair is to match the same-action density and its divergence sign,
or explicitly associate the plus density with -I.

REPAIR.md makes exactly that correction, and REVIEWED_RESULT.md carries it.
The initial candidate and its freeze are preserved. **Repair 1 is accepted.**
No second repair is required. The action aR-2C, response aG+Cg and 16/3 curl
are unchanged. The reviewer independently checked a nontrivial matrix tangent:
the same-action inverse pairing is 154/9, and the erroneous plus-density
pairing differs by 308/9. Thus the sign control is not a zero/degenerate pass.

## Independent computations and false-pass checks

Source-first original witness: diagonal product metric
g=diag(-1,t^4,1,y^4), S=(Ric_ab Ric^ab)TF(Ric), gives (dj)_ty=-20 at t=1,y=2.
Twenty-one exact assertions passed, with nonzero omitted-gradient, wrong-sign
completion and reversed-curl controls. This supplied an obstruction before the
producer metric/formula was seen.

Direct producer-witness replay: `direct_exact.py` uses matrix-valued connection
curvature and mixed-index density divergence, rather than importing producer
formulas/code. It independently reproduces both displayed j components and
(dj)_xy=16/3 at x=y=1. Seventeen exact assertions passed, including nonzero
controls and covariant/inverse variation and tensor-density divergence checks.
Captured runtime: 0.413 seconds, 49,604 KiB peak RSS, under 60 seconds/512 MiB.
Both scripts use Python3.10.12/SymPy1.13.1; same library is explicitly not an
independence axis. There are no floating-point approximations or fitted values.

The author script was inspected for index contractions, trace factors, curl
orientation, regular metric domain and vacuous controls. Its 54 checks include
many componentwise identities; the nonzero curl and independently recomputed
curvature/divergence carry the central witness claim. A count of 54 does not
prove full four-dimensional field coverage. The reviewer did not rerun the
same author code because the independent computation and byte-verified output
already address the load-bearing claim; a same-code rerun would be regression.

## Summary fidelity and remaining limitations

The currently reviewed REVIEWED_RESULT and DECISION_BRIEF accurately distinguish
conditional geometric mathematics, the physical identification gap, and owner
authority. Their pending-review labels can be replaced with this exact scoped
verdict. They do not require a new physical premise, establish a native field
equation, or present the mathematical counterexample as an admitted UDT model.

Not repeated or established: full current premise audit; full GRS1/RMS1 source
replay; all-pair DDR proof; full Anderson–Pohjanpelto/Lovelock proofs; arbitrary-
order inverse problems; natural primitive classification; global cohomology;
empirical GR filtering; sourced/physical light interpretation; nonlinear
well-posedness or stability; human review; formal proof; different-model or
different-library validation. No source-first evidence was revised after
candidate exposure. Later maintained-pointer edits require their own final
proportional fidelity check; this review does not preapprove unseen bytes.
