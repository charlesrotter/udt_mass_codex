# Fresh external adversarial review of G350

Date: 2026-09-05

## Review boundary and procedure

I reviewed only the sealed material mounted at `/intake`. Before opening any scientific payload, I copied the complete intake to the fresh writable directory `/work/g350_external_review.wbj9gO` and performed all execution there. I did not use a repository, protected package, network lookup, download, package installation, or external scientific source. I did not modify `/intake` or select any physical carried quantity, conservation principle, spacetime, source, population, scale, or canonical status.

The report distinguishes three different propositions that must not be conflated:

1. the internal byte consistency of the sealed package;
2. the historical claim that a particular Git commit and push preceded all outcome execution;
3. the mathematical truth of the bounded character theorem and its stated ownership limits.

The first and third can be checked from this intake. The second is supported only by documentary material in the intake and cannot be independently authenticated from the permitted evidence.

## 1. Intake authentication

The read-only mount was confirmed as an ext4 mount with `ro,nosuid,nodev` options. The source contained 39 regular files in five payload directories, with no symbolic links or other nonregular filesystem entries. The copied tree had exactly the same relative file set and every copied file had the same SHA-256 digest as its `/intake` counterpart.

The control-file digests computed from the sealed bytes were:

| File | SHA-256 |
|---|---|
| `REVIEW_SCOPE.json` | `2f057a29de3eeee3ba246bc983a404d8660648783284c5d720a4eb8178cd8b9c` |
| `REVIEW_MANIFEST.tsv` | `cd3cda040f934f2ab22c0b456b6bfada834d74bc45d8597b3116fce5628eb2d2` |
| `REVIEW_MANIFEST.sha256` | `4f2e1c34c2e05668e41290ad25820b8b883fe03a2528f49a4cb4999d0f1a3029` |

`REVIEW_MANIFEST.sha256` correctly authenticates the manifest digest. The manifest has 37 unique payload rows. `REVIEW_SCOPE.json` declares `payload_count: 37`; its ordered `files` array is identical to the manifest path column. Every declared size and SHA-256 digest matches. The actual file set is exactly those 37 declared files plus the two manifest control files, `REVIEW_MANIFEST.tsv` and `REVIEW_MANIFEST.sha256`. There are no missing declarations and no undeclared files.

This is a complete internal consistency and tamper-detection result relative to the supplied digest. It is not external provenance authentication: the digest file has no signature, trusted timestamp, or independently supplied root hash. An actor able to replace the whole intake could replace the manifest and digest together. The package itself acknowledges this documentary-seal limitation in prior accepted material, and G350 should retain the same qualification.

## 2. Preregistration and chronology

The current bytes of all nine entries in `FROZEN_PREREGISTRATION_HASHES.tsv` match their frozen digests:

- `MAP.md`
- `PREREGISTRATION.md`
- `PREMISE_LEDGER.tsv`
- `COMPLETENESS_MAP.md`
- `SOURCE_SCOPE.tsv`
- `COMMANDS.md`
- `derive_carried_content_ownership.py`
- `verify_carried_content_ownership_independent.py`
- `run_catch_proofs.py`

Those frozen documents jointly contain the complete bounded question, the four primary alternatives, all registered secondary alternatives, the continuous positive two-ratio candidate class, identity and sewing requirements, the six named counterfamily witnesses, the `2e-11` numerical tolerance, seeds and minimum check counts, observer/conservation/source/coboundary/caustic/label tests, prohibited imports, and the maximum conclusion. The three outcome-bearing scientific scripts are included in the frozen hash list. Thus the sealed current artifacts are consistent with the claim that all scientific choices requested for preregistration were frozen together.

`GIT_PREREGISTRATION_PROOF.txt` reports full commit `2b050a38521cf311a1c833555a47f47de9a364fa`, dated 2026-09-05 09:11:28 -0400, and says it was pushed before first execution. `PREREGISTRATION_EXECUTION_NOTE.md` and `RUN_RECORD.md` repeat the chronology. No Git object database, commit object, parent tree, signed tag, remote-ref receipt, transparency record, or pre-execution external timestamp is present in the intake. Accessing an outside repository was prohibited. Consequently I can confirm that the sealed documents consistently record the chronology, but I cannot independently prove that the named commit existed with these contents or reached the stated remote before execution.

There is a further precision point. The aggregate `verify_package.py` is a registered command in the hash-frozen `COMMANDS.md`, but its own source is not listed in `FROZEN_PREREGISTRATION_HASHES.tsv` and necessarily changed during the recorded documentary repair. The defensible statement is therefore that the three outcome-bearing scientific routes and their question/specification were frozen. It is not defensible, from this intake alone, to say that the final aggregate verifier source was itself frozen before outcomes.

The reported first aggregate result is `21/23`, with two failures: an obsolete exact phrase expected in the lay report and a raw count of `UDT_NO_WRITE=1` that included prose. The present `COMMANDS.md` has five raw occurrences but exactly four command lines. The current observer check recognizes the unchanged lay statement. Reconstructing the two documented former conditions gives exactly two false documentary checks and therefore `21/23`; the current narrow conditions give `23/23`. This strongly corroborates the stated repair mechanism. It does not authenticate the historical first run because neither the former verifier bytes, a patch, nor its raw output is included.

## 3. Registered replay

All commands were run in the writable copy with `PYTHONDONTWRITEBYTECODE=1`, `UDT_NO_WRITE=1`, and `python3 -B -S`.

| Route | Fresh result |
|---|---|
| Aggregate `verify_package.py` | PASS `23/23` |
| Production | PASS `120010/120010`; maximum normalized error `4.537593487734792e-15` |
| Exact-log verifier | PASS `35295/35295` |
| Hostile route | PASS `25/25` reported mutations |

The regenerated JSON objects exactly equal the three recorded result files. The aggregate landing equals the recorded landing. A complete before/after comparison showed no changed bytes, and no `__pycache__` directory or `.pyc` file appeared. The copied tree remained byte-identical to `/intake` after all runs. Inspection of all four Python sources found only standard-library imports and only local subprocess invocations of the three registered scripts; no network operation or outside package access was present.

## 4. Independent character theorem

Let $G=(\mathbb R_{+}\times\mathbb R_{+},\cdot)$, with componentwise multiplication, and suppose the declared candidate

\[
T:G\longrightarrow\mathbb R_{+}
\]

is continuous and satisfies

\[
T(R_2R_1,A_2A_1)=T(R_2,A_2)T(R_1,A_1).
\]

Define

\[
f(x,y)=\log T(e^x,e^y).
\]

The componentwise exponential is a topological-group isomorphism from additive $\mathbb R^2$ to $G$, and positivity makes the final logarithm defined. Thus

\[
f(z+w)=f(z)+f(w),\qquad z,w\in\mathbb R^2.
\]

Write $p=f(1,0)$ and $q=f(0,1)$. Additivity gives $f(r,0)=rp$ and $f(0,r)=rq$ first for integers and rationals. Continuity extends both identities to every real number. Since

\[
f(x,y)=f((x,0)+(0,y))=f(x,0)+f(0,y),
\]

one obtains

\[
f(x,y)=px+qy
\]

and hence

\[
T(R,A)=R^pA^q,\qquad (p,q)\in\mathbb R^2.
\]

Conversely, every such function is positive, continuous, normalized, and multiplicative. This proves completeness for exactly the declared continuous positive character class.

Identity is not a selector. In fact multiplicativity and positivity already imply $T(1,1)=T(1,1)^2$, hence $T(1,1)=1$. Reversal is not a selector either:

\[
1=T(1,1)=T(R,A)T(R^{-1},A^{-1}),
\]

so reciprocal reversal follows for every character. Sewing is the character condition that produces the two-dimensional family; it does not choose a member of that family.

The parameter pairs `(0,0)`, `(1,0)`, `(0,1)`, `(0,-1)`, `(1,-1)`, and `(2,-1)` define six distinct functions. Evaluating on the two logarithmic basis directions separates any two unequal parameter pairs, independently of whether one particular supplied spacetime realizes the numerical demonstration `(1.7,2.3)`. The intake’s numerical witness also separates the six values, but it is an abstract group-domain witness rather than a demonstrated pair from a specified geometry. This does not weaken the functional-equation result; the prose should avoid calling that numerical pair realized metric data unless a realization is supplied.

The theorem requires the sewing equation for all pairs of elements of $G$. If sewing were required only for the subset of ratio pairs actually realized by a particular supplied ray and its cuts, the conclusion would classify only the subgroup generated by that realized subset unless an attainability or density statement were added. The present request explicitly asks for the character problem on all of `R_+ x R_+`, and the preregistration describes that as the chosen candidate domain, so the theorem is valid as reviewed. The universal quantifier should nevertheless be made explicit in the final mathematical statement.

Without continuity, additive non-linear Cauchy maps constructed using a Hamel basis would give discontinuous positive characters after exponentiation. They do not refute G350 because continuity is a frozen hypothesis. Likewise, functions involving endpoint invariants, nonlocal data, additive interactions, or additional fields lie outside the deliberately bounded class. The intake consistently refuses to claim physical exhaustiveness.

As a fresh executable cross-check, I performed 145,439 exact rational log-coordinate assertions without importing any intake code. They covered three-cut composition, identity, reversal, independent endpoint transformation factors, the conditional invariant, arbitrary endpoint coboundaries, separation of seven parameter choices, nonlinear quadratic failures of sewing, and the three elementary area-limit signs. All passed. These assertions are corroboration only; the proof above is dispositive.

## 5. Typing of the ratio cocycles

For one fixed retained label and three cuts on one common positive-Jacobian stratum,

\[
R_{ji}=\frac{\omega_j}{\omega_i},\qquad A_{ji}=\frac{J_j}{J_i}
\]

are quotient cocycles by cancellation:

\[
R_{kj}R_{ji}=R_{ki},\qquad A_{kj}A_{ji}=A_{ki}.
\]

Their identity and inverse laws are equally immediate. This is pointwise algebra. It does not require the more elaborate stationary sewing law for directional angular-area maps in G346–G348; G350 is taking ratios of endpoint state values (J_i), not composing bilocal Jacobi blocks. The distinction is important and the intake maintains it.

The definition of (A_{ji}) is meaningful only after all (J_i) are evaluated from the same source celestial presentation, on the same intrinsic neighboring ray family, and at the same retained label. G349 supplies precisely that finite source-to-cut map setup. Under a change of the common finite source observer that presents the same intrinsic ray set and endpoint assignment, G349 gives (J_i' = D(n)^2J_i) for every cut on the fixed direction, while the sky coordinates are correspondingly re-presented. The common factor cancels from (A_{ji}). Changing an observer only at a target cut changes the representative of the intrinsic quotient screen by an isometry and therefore does not alter (J_i). These are correctly typed statements.

They are not statements that (A_{ji}) is an intrinsic two-point observable independent of the supplied common family and presentation. If different source skies, different directions, different endpoint assignments, or different labels are used in numerator and denominator, cancellation is unavailable. The G350 text explicitly imposes the common presentation and label, so no contradiction was found.

The affine statement is also sound: a common positive rescaling of the generator multiplies all endpoint frequencies by the same factor, leaving (R) unchanged. The (J_i) used by G349 is a metric area per source-sky area and is invariant when the same endpoint map is maintained under the reciprocal cut reparameterization. Independent affine normalizations at different cuts would not describe one common affine ray and are outside scope.

## 6. Endpoint-observer covariance

Under independent finite timelike observer replacements at the cuts,

\[
\omega_i'=D_i\omega_i,\qquad R_{ji}'=\frac{D_j}{D_i}R_{ji},\qquad A_{ji}'=A_{ji}.
\]

For any already chosen exponent (p), assigning the carried one-dimensional quantity the transformation rule

\[
C_i'=D_i^pC_i
\]

makes

\[
C_j=T_{p,q}(R_{ji},A_{ji})C_i
\]

covariant. Direct substitution cancels (D_i^p) and produces (D_j^p). This works for every real (p). Therefore covariance alone supplies no equation that selects (p); it states the transformation type associated with a choice already made. Setting (p=0) would be the additional choice of observer invariance, not a result of covariance.

For terminological precision, `C_i` should not be called an observer-independent scalar in the same sentence in which it is assigned nonzero observer weight. It is better described as a scalar-valued component, density, or section of a one-dimensional weight representation. This is a wording repair, not a change in the algebra or conclusion.

## 7. Conditional area conservation

Metric geometry supplies (J_i); it does not supply an object (C_i) or assert that a product involving (C_i) is constant. If one separately assumes

\[
\frac{C_iJ_i}{\omega_i^p}=K
\]

along the retained label, then taking the ratio at cuts (j) and (i) gives

\[
\frac{C_j}{C_i}
=\left(\frac{\omega_j}{\omega_i}\right)^p\frac{J_i}{J_j}
=R_{ji}^pA_{ji}^{-1}.
\]

Thus that additional statement forces (q=-1) within the character family. It still does not select (p). The reverse implication also holds on the positive stratum: a transfer with (q=-1) preserves the displayed combination. The equivalence makes especially clear that inverse area is not derivable from the existence of metric area alone; it is exactly the consequence of the new invariance statement. The intake consistently marks that premise as not adopted.

## 8. Source normalization, endpoint coboundaries, caustics, and labels

### Source normalization

Every regular-stratum character is finite and positive. Hence the homogeneous relation (C_j=T_{ji}C_i) maps zero to zero, and multiplying an entire solution by any positive constant produces another solution. No multiplier can determine a nonzero initial normalization or a distribution over source directions. This is algebraic freedom, not a sampled claim. It would fail only if an inhomogeneous source term or a normalization condition were added, both of which are outside the class.

### Endpoint coboundaries

For any finite positive weight (W_i) assigned consistently to each endpoint on a label, independently of which comparison is being formed,

\[
\widetilde T_{ji}=\frac{W_j}{W_i}R_{ji}^pA_{ji}^q
\]

obeys identity, reversal, and sewing because the intermediate (W_j) cancels. This proves that allowing further endpoint data enlarges the admissible cocycle class and that the two-ratio theorem cannot establish physical exhaustiveness.

The consistency clause is essential. A quantity called (W_i) cannot secretly depend on the other endpoint or on the whole ordered pair in a way that changes between the two factors in a sewn path. The phrase “endpoint-local ... constructed from additional metric or pair data” is too loose if “pair data” permits that dependence. The statement should require a globally endpoint-assigned positive zero-cochain on the retained label, or else require the more general pair factor itself to satisfy the one-cocycle law. With that clarification the argument is exact.

### Zero-area boundary

If (J_i>0), (J_j\to0^+), and (R_{ji}) stays finite and nonzero, then (A_{ji}\to0^+) and

\[
R_{ji}^pA_{ji}^q\to
\begin{cases}
0,&q>0,\\
R_{ji}^p,&q=0,\\
+\infty,&q<0.
\end{cases}
\]

No character with nonzero area weight extends as a finite strictly positive invertible character to an element with zero area, because zero has no multiplicative inverse. Reversal exchanges the two one-sided limiting behaviors; it is not an equality evaluated at a zero-area group element. The positive group chart therefore ends at the caustic boundary. A pushforward of a separately supplied measure through the complete G349 map is mathematically available, including critical points and repeated preimages, but that does not provide a physical measure, a continuation law, or a rule for combining labels.

This limit classification is conditional on one denominator Jacobian remaining positive and on a finite nonzero frequency ratio. If numerator and denominator Jacobians vanish together, the ratio depends on their relative orders and is not classified by the displayed trichotomy. The report should retain that narrower statement and avoid suggesting that every simultaneous zero-area approach has been classified.

### Per-label boundary

All ratio and transfer equations use the same label at both endpoints. They imply no relation between different labels. G349 can form a mathematical disjoint-union multiplicity census, but choosing a population, weights, signs, or another cross-label operation requires additional data. G350 correctly makes no such choice. Per-label composition therefore does not entail aggregation.

## 9. Evidence-quality audit

The computational evidence is reproducible, deterministic, dependency-free, and useful for catching arithmetic or serialization regressions. It must not be credited beyond that role.

First, production defines the asserted character formula and verifies identities generated from that same formula. This is a normal regression test but is partly circular as evidence for the classification theorem. It does not range over arbitrary continuous functions.

Second, the “implementation-distinct exact-log” route does not reconstruct the theorem from an unknown additive function. It defines `log_transfer(p,q,x,y) = p*x + q*y` and exactly checks that linear expression. It is genuinely code-distinct from production and avoids floating error, but it verifies the proposed family and ancillary identities, not completeness of the family. The report’s analytic proof supplies completeness. Claims of implementation distinction are supportable; claims of premise-independent or theorem-independent verification would not be.

Third, the hostile route is vacuous as a mutation test. `valid(record)` is exact equality with a hard-coded baseline. Each “mutation” changes one field, so every mutation is rejected by construction without exercising the derivation, documents, or production behavior. The `25/25` result establishes only that 25 baseline fields were enumerated and compared. It does not demonstrate that the package would detect a corresponding scientific defect. This is the most significant evidence-quality caveat, though it does not refute the analytic theorem.

Fourth, production’s function named `relative_error` divides by `max(1, abs(left), abs(right))`. This is a conventional mixed absolute/relative normalized error, not relative error near zero. Given the sampled log ranges and exponents, valid values can be below `2e-11`, where even a zero result could pass the absolute branch. No such failure occurred and the exact-log route removes roundoff from the core algebra, so the theorem is unaffected. The metric should be named accurately and supplemented with log-domain or symmetric relative checks if numerical evidence near zero is intended to be probative.

Fifth, many aggregate gates are documentary substring checks. Result reproduction compares scripts with result files generated by the same scripts. These are valid integrity and reproducibility guards, but not evidence for mathematical truth. The package itself describes them that way, so there is no hidden promotion in the maximum conclusion.

Sixth, the standard-library import audit recognizes static `import` syntax only; in principle it would not detect dynamic imports or all network-capable behavior. Direct inspection of the short frozen sources found no dynamic imports or network calls, so this is a limitation of the general guard rather than a hidden import in G350.

The scope scan found references to excluded physical notions only in prohibitions, open-boundary statements, conditional examples, or hostile baseline labels. No excluded physical law or interpretation is used to choose (p), (q), a source normalization, a caustic continuation, or an aggregation rule. No text claims that the two-ratio class exhausts general physical transfer. The bounded result is consistently presented as a chosen functional-equation classification.

## 10. Required repairs and final assessment

No repair is required to the central bounded theorem (T(R,A)=R^pA^q), to its nonuniqueness conclusion, to the observer-covariance algebra, or to the conditional derivation of (q=-1).

The following repairs are required for fully precise evidence and wording:

1. Qualify manifest authentication as internal checksum consistency unless a trusted external signature or root digest is supplied.
2. Qualify commit/push chronology as documentary. To claim independent authentication, include a verifiable Git bundle containing commit `2b050a38` and its parent/tree plus an independently trusted pre-execution timestamp or remote-ref receipt.
3. Include the pre-repair `verify_package.py`, its raw `21/23` output, and the exact patch if the historical narrow-repair claim is to be independently reproduced rather than reconstructed from prose.
4. State that the three scientific routes were hash-frozen; do not imply that the final repaired aggregate verifier itself was outcome-unseen and frozen.
5. Relabel `run_catch_proofs.py` as a tautological contract-enumeration guard, or replace it with mutations of executable/documentary behavior that are rejected by independent semantic assertions.
6. Relabel the exact-log route as an implementation-distinct exact verification of the proposed formulas, not an independent proof that all continuous characters are linear.
7. Rename the floating error metric as mixed absolute/relative normalized error and, if numerical behavior near zero matters, add log-domain or scale-sensitive checks without weakening the frozen tolerance.
8. Explicitly quantify the sewing equation over all of `R_+ x R_+`; otherwise restrict the conclusion to the subgroup of realized ratios.
9. Define endpoint coboundary weights as consistently endpoint-assigned zero-cochains, not comparison-dependent pair quantities.
10. Describe (C_i) as a weighted scalar-valued component or one-dimensional representation when (p\ne0), rather than an observer-independent scalar.
11. State caustic reversal as an exchange of one-sided limits and retain the assumptions (J_i>0), (J_j\to0^+), and finite nonzero (R_{ji}); simultaneous numerator/denominator zeros remain outside that trichotomy.
12. Treat `(1.7,2.3)` as an abstract group-domain witness unless an actual supplied geometric realization is exhibited.

These caveats lower the evidence grade and require precision repairs, but none supplies a counterexample to the declared continuous positive character theorem or to the ownership boundary. The mathematical conclusion remains bounded, conditional, pointwise, regular-stratum, and per-label. It does not choose any excluded physical attachment or claim exhaustive transfer physics.

ACCEPT_WITH_CAVEATS_G350_FREQUENCY_AREA_OWNERSHIP_BOUNDARY
