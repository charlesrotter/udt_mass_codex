# CF1 post-seal exposure and bounded review notes

This file is post-exposure and cannot revise the source-first designation or
the sealed original argument. The source-first seal SHA-256 is
`e36ffe8e69b94d56676008be64bc3ce1aaf173c4dbb46245318857210b6c4a0a`.

First author exposure occurred in the tool read at
`2026-09-08T20:35:53.807256+00:00`, after verifying that both
review/SOURCE_FIRST_SEAL.md and step_01/CANDIDATE_FREEZE.md existed. That read
opened the freeze only. Candidate, checker and saved outputs were opened
subsequently. The candidate's own freeze time is an author statement; the
reviewer does not independently authenticate the author's prefreeze exposure.

Exact first-exposed freeze:
`5276ee4859ca0ca0bf3758c122c498a1897f6a58bd397cb8aeddcbae29bf0b8e`.
The three frozen candidate/checker/baseline hashes matched their files:

- CANDIDATE_INITIAL.md:
  `35263178061ec4ad2e65add33b43e8f66c008a6447a76bf2fb1263f8f42b92ea`.
- check_cf1.py:
  `3272d699a432c86f4137505a99e44af18588e942fcf310d375acde35ee7367c9`.
- check_baseline.stdout:
  `ac9d854ced7c7b0daf46e66f7a888083a9dc8e1958902062346907083a1c4d41`.

No campaign log, other review, or advisory file was opened. Post-exposure
literature access was attempted only for the candidate's ancillary terminology
citation: https://arxiv.org/pdf/2102.08142v2 and
https://arxiv.org/abs/2102.08142v2. Both web tool calls returned a cache-miss
fetch failure. No paper text was received. Its section-specific attribution
is therefore NOT independently verified. The source-first elementary proof
does not rely on this paper or on any general Seifert classification theorem;
its unavailability blocks only that ancillary citation check.

## Analytical adversarial checks

1. Global smoothness and nonvanishing follow from Cartesian rotations and
   `(1-s)+r(s)^2*s>0`, including both collapsed axes. The author explicitly
   defines smoothness on the closed interval through a neighborhood extension.
2. Periodicity requires simultaneous integer angular turns. Nonclosure for
   irrational slopes follows from this exact return equation, without a
   numerical irrationality decision or a density theorem.
3. All-leaf closure forces r((0,1)) contained in Q; continuity and the
   intermediate-value theorem force constancy, including endpoint values.
4. The primitive axis loops have periods 2*pi and 2*pi/r, so their transverse
   rotations are p/q and q/p, of orders q and p. For p=1 or q=1 exactly one
   axis can be exceptional; both are regular only when p=q=1 in lowest terms.
   The candidate's phrase 'exceptional axes' is read with these explicit
   orders, not as a claim that both axes are always exceptional.
5. Regular circle-bundle holonomy is trivial. General smooth diffeomorphisms
   conjugate holonomy germs and carry maximal leaves to maximal leaves.
   Orientation reversal takes inverses, leaving the obstruction intact.
   Thus the argument covers the full equivalence allowed by the work order.
6. A smooth family starting at Hopf has the strong property iff r stays 1.
   All-time closure has the same consequence by continuity into Q in time.
   Isolated rational weighted fibrations remain a strictly weaker possibility.
7. For an actual jointly smooth family, let f(t)=partial_s r(t,s0).
   Since f(0)=0, f'(0)!=0 gives f(t)=t*f'(0)+o(t), nonzero for all sufficiently
   small nonzero t. This proves the candidate's conditional mixed-derivative
   implication. It does not construct the actual family, symmetry reduction,
   lawful initial data or vacuum development. Those remain CF2's separate job.
8. All finite checks are supporting arithmetic. Neither the author's
   `cancel(3*r/3)==r` nor the reviewer's rational-rescaling identity is evidence
   for global equivalence under an arbitrary smooth nowhere-zero multiplier.
   That statement follows analytically from the unchanged line distribution.
   No finite fixture set certifies all smooth r or the topological theorem.

## Executed failure and repair-probe history

The initial source-first run passed before author exposure. After exposure,
all five author modes were rerun through the required capture utility. The
baseline passed 29/29; each of the four declared function mutations exited 1
on exactly the corresponding saved failed-guard list. Every replay stdout
matched the author's saved stdout bytes. These are same-code regression checks.

An additional review-only mutation changed the regularity decision from
`axis_orders(r)==(1,1)` to `1 in axis_orders(r)`. On the author's original five
fixtures this scientifically wrong rule actually passed 29/29 with exit 0.
This false pass is retained in false_pass_either_axis.{stdout,stderr,json}.
The missing cases are one-exceptional-axis slopes such as 2 and 1/2.

A second separately captured run kept the same wrong rule but added those two
fixtures in memory. It exited 1 with precisely `regular_2` and `regular_1/2`
false (37 checks passed, 2 failed). Evidence is in
catch_either_axis.{stdout,stderr,json}. No author file was edited. This is a
focused catch demonstration, not an author repair or repaired author release.
The sealed independent checker already covered both cases and rejected the
same false principle before author exposure.

This fixture omission limits the author's finite harness, not the direct
proof: the source and independent proof both require BOTH holonomy orders to
be one. Smallest optional author repair is to add these two fixtures and the
either-axis mutation, preserving original files and false-pass evidence. The
author owns that decision and the one allowed repair/re-review allocation.
There is no unresolved load-bearing mathematical objection at CF1 scope.

No checks were overwritten or discarded. No scientific candidate repair was
performed by this reviewer. Fresh model comparison, human specialist review,
formal theorem checking, and actual CF2 development checks remain unperformed.
