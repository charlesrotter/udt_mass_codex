# ND1 direct adversarial review

Date: 2026-09-09. Reviewer: `/root/native_response_step1_review`.
Exact model: UNKNOWN. Verdict: **VERIFIED-WITH-CAVEATS at the stated scope**.
No load-bearing defect or required repair was found in the frozen initial
candidate. This is a fresh-context review of a conditional mathematical
candidate, not scientific promotion, new physical authority, or canon.

## Exact target and independence

Candidate `step_01/CANDIDATE.md` SHA-256:
`5b20cb544d5a1630201be50eb3ee3ce513cf1a4801a278bd5e6f2101fd9bf838`.
All eight SOURCE_SHA256SUMS pins and all five CANDIDATE_SHA256SUMS pins were
checked with `sha256sum -c` and matched. The candidate and source bytes, rather
than a moving branch label, are the scientific targets of this review.

The source-first reconstruction is preserved without rewriting in
`SOURCE_FIRST.md`, SHA-256
`911bcd13a2e23e47a1c91cef5eefa6cf46f9d7e9f350e0b102d9ce5ef1b2373a`.
It identifies accepted results, current authority, missing joins, and duplication
risks. It was written before direct candidate exposure. The reviewer independently
sent the pencil identity Q=(R/2)S and the scalar-flat family before seeing the
author candidate; the author subsequently reported matching exploratory algebra.
That concurrence is disclosed, not counted as additional independence.

The independently implemented `independent_tensor_check.py` was written before
direct candidate exposure. It imports no author or historical scientific code.
After the source-first stage, the reviewer read the frozen candidate proof,
source/candidate manifests, author run receipt, shared run-capture utility,
roadmap/work order, and six current-document diffs. Author scientific code,
author numerical stdout, and G260 scientific implementation were not read.
The G260 implementation's hash was checked because it is in the source manifest.
The shared capture utility only records execution and limits; it supplies no
scientific formulas. Historical source audit reports exposed historical verdict
summaries, as recorded in SOURCE_FIRST; this is not blind re-review of G260–G312.

Independence axes:

| Axis | Actual status |
|---|---|
| Context | Fresh separate reviewer context |
| Different model | UNKNOWN / UNTESTED |
| Implementation | Independently written full metric Taylor-jet to Ricci calculation; shared capture utility only |
| Argument | Source-first reconstruction, then direct attack on the candidate; additional scalar-ODE non-switching argument below |
| Author result exposure | Author reported 299 checks/27 cases and supplied receipt before direct review; no author scientific code/output read |

Initial checked HEAD was `d0fe8b3e5f95c3963dc8702bb4a31485678bd1e3` on grok.
During review the parent preserved the roadmap/startup record at HEAD
`07932b402976606355571a8a15269c9a80bcc4ee`; the reviewer did not run git mutations.
The candidate source hashes and reviewed document hashes remained the fixed
targets. Remote synchronization was parent-owned, not independently asserted.

## Claim-by-claim attack and surviving conclusions

### ND1-IDENTITY: verified

The covariant Q definition equals G312's `TF_g(Ric_ac Ric_b^c)` because M is
g-self-adjoint and `g M²` is exactly that contraction. For mixed Ricci
diag(A,A,B,B), its trace is 2(A+B), and the mixed trace-free Ricci eigenvalues
are `(A-B)/2,(A-B)/2,(B-A)/2,(B-A)/2`. Squaring and removing the mean therefore
gives Q=(A+B)S=(R/2)S. The signs agree with G260's curvature convention.

The independent raw-coordinate calculation below recomputes all Ricci components,
including off-diagonal zeros, from the complete metric two-jet. It confirms the
candidate A/B formulas and factorization. The identity requires the two-plus-two
spectrum. No arbitrary-metric factorization follows, and the candidate says so.

### ND1-CLASS: verified, including no branch switching

The author's proof considers the open set U={A!=B}. On each connected component,
the scalar-flat Euler equation gives f=1+b/r+d/r² with d!=0. At a finite positive
radius endpoint inside I, continuity would require A-B to vanish, whereas its
component limit is -2d/r⁴, which is nonzero. Thus a nonempty component has no
relative boundary and must be all of connected I. If U is empty, the E Euler
equation holds everywhere. This is valid for f in C2 because A,B are continuous;
the two Euler equations are ordinary linear equations on r>0. One cannot splice
different d values or insert an E interval at a zero of A-B. Positivity and the
one-function chart restrict the domain; they are not inferred from this argument.

A second proof exposes the same obstruction without assuming a preselected
branch. Put y=rf'+f-1. Then y is C1 and

    E1=(r/2)y',          Q=0 iff (r y'/2)²=y².

On any compact interval with r bounded away from zero, |y'|<=C|y|. If y vanishes
at one point, the integral inequality/Gronwall argument in each direction forces
y=0 throughout connected I. Otherwise y never vanishes; the continuous function
r y'/(2y) takes only the values +1 and -1, hence has a constant sign. Integrating
gives y=k r² or y=k r^-2, followed by f=1+(k/3)r²+b/r or f=1+b/r-k/r².
The y=0 case is the common f=1+b/r branch. This proof uses no derivative of
curvature and therefore does not hide a C3 Bianchi requirement.

The converse follows by direct substitution. Equality of the two families on an
open interval implies `a r⁴+(b_E-b_Z)r-d=0` identically, so a=d=0 and the b values
agree. These are exactly the claimed union and intersection. Finite sampling
does not establish any of these exhaustion statements.

### ND1-FILTER: verified as a declared analytical test

On E, S=Q=0 and C_ang=0. On Z, Q=0, R=0 and C_ang=2d/r², so adding C_ang=0 removes
exactly the d!=0 Z metrics and leaves all E. This says that this filter constrains
solution metrics within the chart. It does not distinguish S from Q on their
shared E backgrounds or select a=0. Q-DDR alone permits the additional Z branch.

The potentially dangerous missing join has been kept open: C_ang is a native
geometric readout, while DDR balances the specified tensor response. They cannot
be equated for arbitrary responses merely by using the word “angular.” Current
authority supplies neither this filter as a universal vacuum law nor full GR
principal-response equivalence. The candidate adopts neither. Its d coefficient
has no identified charge/source/content interpretation.

### ND1-PAIR: verified

In an orthonormal frame covariant Ricci is diag(-A,A,B,B). The reciprocal tangent
normalization from G310 is exactly twice the sum of the two squared covectors.
Thus the time/radial contraction is 2(-A+A)=0 for every f, while time/angular is
2(B-A)=2 C_ang/r². Trace subtraction cannot change these contractions because
the reciprocal tangent has zero metric trace. On Z, the time/angular value is
4d/r⁴, nonzero if d!=0. Q itself is zero on Z, so all its pair contractions vanish.
The candidate accurately separates these statements and does not mistake radial
blindness for all-pair DDR. Full all-pair span is inherited from G310/G311; this
review did not rerun their rank certificates or global population questions.

## Exact computational evidence

The new implementation represents the supplied diagonal metric through order two
with rational Taylor coefficients in radial displacement and angular displacement
from an equatorial event. In particular `sin²(theta)=1-dtheta²+O(dtheta⁴)` supplies
the sphere's angular second derivative. Truncated polynomial inversion constructs
inverse-metric jets. Ordinary coordinate Christoffel and Christoffel-derivative
formulas then produce the full Ricci tensor before S or Q is formed. No reduced
Ricci formula is used to construct that tensor; the source formulas are compared
to this independent result afterward. All arithmetic is exact Fraction arithmetic.

Actual launch, from repository root:

```bash
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py /home/udt-admin/udt_mass_codex/udt_native_response_discrimination_2026-09-09/step_01/review/independent_tensor_run /home/udt-admin/udt_mass_codex python3 -B udt_native_response_discrimination_2026-09-09/step_01/review/independent_tensor_check.py
```

Python 3.10.12; 512 MiB address-space cap; 60-second CPU/wall cap; no GPU.
Parent confirmed no competing check at launch. Observed return code 0,
0.217859 seconds, peak child RSS 11,712 KiB, empty stderr.

- 54 arbitrary positive-f two-jet cases check every Ricci component, Q=(R/2)S,
  radial/angular contractions, and the pointwise zero-set disjunction.
- 18 E/Z witnesses check nonzero R with S=0 versus R=0 with S!=0, while Q=0 in both.
- A separate sphere-derivative corruption on the Ricci-flat f=1+1/r witness
  changes its Ricci tensor from zero to nonzero. The full-sphere test detects it.
- 1,955 exact assertions passed in total. This count records implementation
  coverage, not a theorem probability or completeness certificate.

The deformation is a narrow negative control for dropping angular second
derivatives, not a full mutation census. No floating-point approximation,
unreported convergence claim, or shared scientific implementation is involved.
The script does not import source/author results. Formula agreement is supported
by different construction; accepted definitions are necessarily shared.

The initial attempt to summarize JSON with jq failed because jq is absent.
This was a read-only presentation command after the successful scientific run;
the output was subsequently read with Python's JSON parser. It neither reran nor
altered evidence. Both manifest checks had already completed successfully.

## Novelty and documentation fidelity

G260 already owns C_ang cancellation and its E family. G310/G311 already own the
full-pair response-shape theorem and conditional S=0 restriction. G312 already
owns the quadratic response's Ricci-flat overlap and zero flat first variation.
ND1 correctly reuses those facts. The candidate adds the complete restricted
Q-zero-set union, no-switching proof, and exact filter intersection. No claim of
general mathematical novelty or selection by all UDT structure is supported.

The roadmap and work order preserve DDR/locality as provisional and GR as filter
only; they explicitly distinguish conditional development from physical law and
bound the campaign to at most three reviewed steps/four hours with review/repair
and return conditions. The six startup edits only replace the previous stop gate
with the authorized bounded campaign and a roadmap pointer. In the reviewed diff
they do not alter scientific grades, reinstate stronger GR authority, reopen
parked routes, weaken guards/tests, or authorize promotion. This is a proportionate
**FIDELITY_REVIEWED** assessment of those exact edits, not proof of the roadmap's
future scientific ambitions or independent authentication of conversation history.

The parent startup-test receipt/stdout were inspected: 353 passed, 1 deselected,
return code 0, with the excluded test being the full foundational verifier path.
This is parent-run regression evidence, not an independently repeated suite. The
actual full365 receipt still reports the unchanged G325 failure. The candidate
cannot be scientifically banked by citing the startup regression alone.

## Limits and omitted checks

No historical full-package replays, full365 rerun, G325 diagnosis, external model
review, general static-spherical two-function metric classification, time-live
extension, general curvature response census, PDE well-posedness, stability,
physical source identification, empirical GR tolerance, or cosmological conclusion
was undertaken. Source grades remain unchanged. Protected payloads, archives,
canon, registry, manuscript, and unrelated work were not modified. These are
scope limits; no adverse conclusion about excluded classes is inferred.

Strongest surviving result: on a connected positive-radius interval in the
supplied C2 positive one-function spherical metric class, quadratic-response DDR
has exactly E union Z, and the declared G260 cancellation test reduces that union
to E. The all-pair versus angular-readout distinction remains explicit. There is
no required repair and no unresolved load-bearing review disagreement.

## Evidence and document hashes

Additional exact pins (source pins are in SOURCE_FIRST and SOURCE_SHA256SUMS):

```text
6a3228db7b9e652dc158d47b08531d53dbc7cd70a169a38d82d9e484abdd172d  step_01/review/independent_tensor_check.py
eb1d40033df7a78a70c6c198d5c17101632eee9d14a36db0da01d6ffab90ed8d  step_01/review/independent_tensor_run.json
e4f66260864513578341fd441b9485eb38fcf93ebc0c90edbd6bce099ba3f897  step_01/review/independent_tensor_run.stdout
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  step_01/review/independent_tensor_run.stderr
8ff5469ace76bdfc84188915242abbf3baff35516f9ee3f9ba4b1cbfeb2573ef  udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py
0e26ba9cf2c1d801bb9abc9ded55d78dd9a17d75628361d4fc02dbfa33645580  LIVE.md
e3774fcc6f832fd5c4595b41dbb557337aabbe4b48d1cf3b93c6a6730502ec4e  HANDOFF.md
771b797b4714a2768fc39d21bbb8ea83183abd532a2e18cd98cbb67e6aeadb55  CURRENT_RESEARCH_PROGRAM.md
ff4f82837afe140b168a81f379273bcd89950b3f255fc8167d8553de2ef2a8c6  CURRENT_SCIENTIFIC_PREMISES.md
f113391bd9e194301c7b98b8e9ef54fbacb7318907d0770ec30f93e39e8d7551  INDEX.md
f9c98ec1885e1b87922a1d57b2ae184024865b68236d4bb917b669309b304060  MEMORY.md
048721aa6aaa30c50946fe46d9b0ca95ee438f4631168b017ee52e6304dae636  roadmap_startup_tests.json
02f1c8d8b8dec62ce966bc2380b3f3d0dfd877848288d3ba7345fd27054f48ff  roadmap_startup_tests.stdout
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  roadmap_startup_tests.stderr
```

Paths beginning `step_01/` or `roadmap_startup_tests` are relative to this campaign
package; the other paths are repository-relative. Hashes certify correspondence,
not truth or chronology. The roadmap/work-order pins are unchanged from SOURCE_FIRST.
