# External Adversarial Review: G336 Bounded Silent Second Jet

## Scope and authentication

I treated `/intake` as sealed read-only evidence and inspected nothing outside that tree until after authentication. I then copied the intake to `/work/g336_review_20260903` and ran all executable checks only there.

Authentication results:

1. `REVIEW_MANIFEST.tsv` matched `REVIEW_MANIFEST.sha256`.
2. The sealed file set under `/intake` contained 36 files total: 34 manifest payloads plus the two top-level manifest files intentionally outside the payload list.
3. Every manifest payload matched its declared byte count and SHA-256 exactly.
4. The copied intake passed `python3 -B -S verify_review_intake.py /work/g336_review_20260903`, returning `G336 intake PASS: 34 payloads`.

## Findings

1. Minor repair only: [EXACT_DERIVATION.md](/work/g336_review_20260903/package/EXACT_DERIVATION.md:132) states the inherited zero surface for `0<mu<=1` while the same document and the sealed repair exclude `mu=1` from the strict family. The strict/boundary separation is nevertheless correctly restored at [EXACT_DERIVATION.md](/work/g336_review_20260903/package/EXACT_DERIVATION.md:160) and [PREREGISTRATION_SCOPE_REPAIR.md](/work/g336_review_20260903/package/PREREGISTRATION_SCOPE_REPAIR.md:17). This is a wording-scope defect, not a mathematical defect.

No refuting mathematical finding survived attack.

## Mathematical review

1. ADM sign and retained terms.
With the source convention `K = -(1/2)L_n gamma` and ADM evolution `nK_ij = Ric3_ij + tau K_ij - 2 K_i^k K_kj - Lambda gamma_ij`, exactly as stated at [EXACT_DERIVATION.md](/work/g336_review_20260903/package/EXACT_DERIVATION.md:58), inherited Lie carry gives
`s1 = (1/2)n^2[gamma(v,v)] = -nK(v,v)`.
On the silent set `q0 = gamma(Hv,v) = -K(v,v) = 0`, the `tau K(v,v)` term vanishes, leaving
`s1 = Lambda - Ric3(v,v) + 2 K_i^k K_kj v^i v^j`.
This sign is correct. Flipping the ADM sign or dropping either the Ricci term or the `K^2` term changes the answer and is caught by `run_catch_proofs.py`.

2. Three forms of `s1` on the exact first-order-silent set.
From G332,
`K = ((C-b)/2)gamma + b eta tensor eta`,
so `K^sharp` has eigenvalues `((C-b)/2, (C-b)/2, (C+b)/2)`. Silence gives
`q0 = (b-C)/2 - b mu = 0`, hence `C = b(1-2mu)`.
Then
`k_horizontal = -b mu`,
`k_vertical = b(1-mu)`,
and
`K^2(v,v) = b^2 mu(1-mu)`.
Using G331,
`Ric3(v,v) = (R-2)/2 + (6-R)mu/2`.
Using the G332 constraint,
`(b+C)^2 = 2(R+2C^2-2Lambda)`,
the silent relation yields
`Lambda = R/2 - 2b^2 mu + 3b^2 mu^2`.
Substituting gives the exact agreement
`s1 = Lambda - Ric3(v,v) + 2K^2(v,v)`
`   = 1 + (Lambda-3)mu + 3b^2 mu^2(1-mu)`
`   = 1 + (R-6)mu/2 + b^2 mu^2`.
This rederivation matches [EXACT_DERIVATION.md](/work/g336_review_20260903/package/EXACT_DERIVATION.md:88).

3. Equal-quarter-weight `R=0` control and sign triplet.
I independently reimplemented the weighted metric coordinate curvature calculation and confirmed:
`R=0` at `w1=w2=1/4` for both `x=1/3` and `x=2/3`.
For `C=0`, `mu=1/2`, the constraint gives `Lambda = -b^2/4`, and the reduced formula gives
`s1 = 1 - 3/2 + b^2/4 = -1/2 + b^2/4`.
Hence the exact triplet is:
`b^2=1 -> Lambda=-1/4 -> s1=-1/4`,
`b^2=2 -> Lambda=-1/2 -> s1=0`,
`b^2=4 -> Lambda=-1 -> s1=1/2`.
The sign triplet is exact and both root signs `b = ±sqrt(b^2)` remain present.

4. Finite-boost matrix and terminal `Phi`.
For `U = cosh(z)n + sinh(z)v` and `S = sinh(z)n + cosh(z)v`, with inherited carry and `q0=0`, only the `vv` entry contributes a second jet. Therefore
`n^2 h_pair = 2s1 [[sinh^2 z, sinh z cosh z], [sinh z cosh z, cosh^2 z]]`.
With `Phi = -(1/2)log(-h00)`, `h00(0)=-1` and `n h00(0)=0`, so
`n^2 Phi = (1/2)n^2 h00 = s1 sinh^2 z`.
At zero boost this vanishes identically even when the spatial second jet is nonzero. That is a real blindness of terminal `Phi`, not of the full pair matrix.

5. Strict radicand versus vertical boundary.
On the silent set,
`C = b(1-2mu)` and `(b+C)^2 = 4b^2(1-mu)^2`.
For strict silent data `b != 0`, the radicand is positive exactly when `mu < 1` and vanishes at `mu=1`. So `mu=1` is not a strict two-branch G332 datum. It is only the branch-meeting closure boundary. This is correctly repaired at [PREREGISTRATION_SCOPE_REPAIR.md](/work/g336_review_20260903/package/PREREGISTRATION_SCOPE_REPAIR.md:21) and respected in the status ledger at [STATUS_LEDGER.tsv](/work/g336_review_20260903/package/STATUS_LEDGER.tsv:6).

6. Inherited carry versus general unit-direction carry.
For a general smooth unit direction, let `W = nabla_n v` with `gamma(W,v)=0` at the event. Then
`n q(W) = n q(Lie) + 2 gamma(Hv, W-Hv)`,
because inherited Lie carry has `[n,v]=0`, so `W=Hv` in Gaussian presentation.
Also
`|Hv|^2 = b^2 mu(1-mu)`.
Therefore:
`0<mu<1` implies `Hv != 0`, so choosing `W = k Hv` changes the sign of `nq(W)` and the classification is carry-dependent in the interior.
`mu=0` implies `Hv=0`, so the first-carry correction vanishes and `s1=1` is carry-independent at this order on the strict horizontal endpoint.
`mu=1` also gives `Hv=0`, but only on the non-strict closure boundary.
The interior/endpoint split is therefore real, and the category distinction at [EXACT_DERIVATION.md](/work/g336_review_20260903/package/EXACT_DERIVATION.md:227) is necessary.

7. Double silence and conclusion ceiling.
The equal-quarter-weight control with `b^2=2`, `C=0`, `mu=1/2`, `Lambda=-1/2` gives `q0=0` and `s1=0`. This is a lawful exact double-silent datum. The package does not illegally discard it. The sealed status and exact derivation keep the next question at the third jet open, and they explicitly refuse finite-time development or stability claims at [EXACT_DERIVATION.md](/work/g336_review_20260903/package/EXACT_DERIVATION.md:248) and [STATUS_LEDGER.tsv](/work/g336_review_20260903/package/STATUS_LEDGER.tsv:7).

8. Premise stamps and forbidden imports.
The premise ledger is consistent with the claimed ceiling:
`Universal_Reciprocity_DDR` is only `OWNER_ADOPTED_PROVISIONAL_POSTULATE`,
`Ric_equals_Lambda_g` is only `DERIVED_CONDITIONAL_IN_BOUNDED_ARENA`,
the G332 family and G333/G334/G335 chain are bounded imported inputs,
Gaussian normal gauge and inherited Lie carry are declared presentation controls,
general carry is explored but not selected,
topology, matter, mass, observations, scale, `X_max`, and higher jets remain omitted or open.
See [PREMISE_LEDGER.tsv](/work/g336_review_20260903/package/PREMISE_LEDGER.tsv:2).
I found no hidden appeal to topology, observation, scale, history, `X_max`, matter, or canonization in the G336 claim.

## Executed checks

I ran the registered commands from [COMMANDS.md](/work/g336_review_20260903/package/COMMANDS.md:5) in the writable copy:

1. `derive_silent_second_response.py` passed 48,375 checks, with 576 strict silent cases, 48 vertical-boundary cases, and 9,792 strict boost cases.
2. `verify_silent_second_response_independent.py` passed 3,860 implementation-distinct randomized checks.
3. `run_catch_proofs.py` caught all 14 hostile mutations.
4. `verify_package.py` passed 87 aggregate gates.

## Conclusion

The bounded G336 second-normal-jet result survives adversarial rederivation. The ADM sign is correct, the Ricci and `K^2` contributions are retained, the three silent-set formulas agree exactly, the finite-boost matrix and terminal `Phi` second jet are correct, the strict family excludes `mu=1` exactly because the radicand collapses there, the interior carry dependence versus endpoint carry cancellation is real, the double-silent stratum is lawful, and the conclusion ceiling stays at the initial second jet.

The only repair I require is textual: keep the zero-surface statement strictly on `0<mu<1`, reserving `mu=1` only for the closure-boundary diagnostic already sealed elsewhere in the package.

ACCEPT_WITH_REPAIRS__G336_BOUNDED_SILENT_SECOND_JET_RETAINED
