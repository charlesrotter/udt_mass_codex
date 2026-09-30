# TRI1 direct mathematical review

Verdict on the initial candidate: **VERIFIED-WITH-CAVEATS; small source-preserving
scope repair required for the aggregate density formula.** The fixed-geometry
arrival theorem, normalization distinction and population counterexample survive.
This report does not yet certify the controlling repair or central integration.

## Actual context, exposure and versions

Reviewer `/root/tri_math` is a separate inherited-model context, not a
different-model review. The source-first report and Fraction implementation
were developed without reading the TRI1 candidate, parent science code or peer
report. Before its final freeze the parent did disclose that its candidate was
frozen and that a SymPy factorization failure had been repaired with28 controls
and7 rejected identities; that outcome/status exposure was omitted from the
source-first report's compact list and is explicitly added here. No claim of
complete outcome blindness is made. The independent argument and implementation
are separate from the producer code.

Source-first freeze was sealed2026-09-30T21:42:56 UTC, followed by its own exact
run. Then the initial candidate, CANDIDATE_FREEZE, both producer check versions,
plans/repair, failed stderr/receipt and repaired stdout/stderr/receipt were read.
The frozen initial candidate SHA256 is
`b1c9ab5d349463f9c27f1b719f85948f3afe949583c8aceea75cded7b1ae206e`.
The current central document was not used as a scientific source after parent
edits began; SOURCE_PINS binds the original git39126a76 central version.

The peer review directory's filenames were incidentally listed by a bounded
package file search; none of its content was read. After this reviewer reported
the domain issue independently, parent stated that the other reviewer had also
found it and that REPAIR.md existed. Neither that repair nor peer content was
read before sealing this direct report. Parent's report of agreement is not
used as mathematical evidence. No protected payload was accessed.

## Substantive argument audit

1. The family variation proves Z=A'=omega_e/omega_o on exactly the regular
   affine null-clock interface. Neither a population nor a moment criterion
   occurs. Candidate states correctly that actual endpoint clocks, geometry
   and branch are supplied; it does not infer them from bare g. Fixed parameter
   endpoints and arbitrary rescaling are correctly separated in section2.
2. The same ray's affine scale cancels in its endpoint ratio; intermediate
   observer cancellation changes no endpoint. Cadence normalization is a
   convention anchored by independently supplied source cadence, not an energy
   law. Future relay, branch switches and changed endpoints stay distinct.
3. Pushforward is the exact labelled-record statement. The finite-duration
   integral and nonconstant control defeat replacing it by one instantaneous Z.
   The candidate's conditional continuous density and phase give inverse-Z
   rates. No physical detection, luminosity or energy law is thereby derived.
4. The spectral example is algebraically correct: weights4:1 on unit beams
   have J=(5,3) and rest-moment velocity1/3; halving k+ gives J=(3,1) and equal
   effective moment weights1:1. This changes a population on nonzero null vectors
   while leaving each ray ratio invariant. Candidate explicitly disclaims
   physical gauge equivalence and unrestricted inverse-data nonidentifiability.
5. PRI1's positive observer theorem, criterion distinction and raw-moment DDR
   obstruction are preserved. Off-shell variation gates remain attached to
   the metric-response problem, not fixed-geometry clock comparisons. No
   native geometry selection, novelty or full UDT underdetermination is claimed.

## Defect, counterexample, survivor and smallest repair

Initial section3 Eq(5) and the denominator R write a sum of A_j^-1(t) without
restricting t to the arrival images. Let both emission intervals be[0,1],
A1(s)=s and A2(s)=2+s. Their pushforward measures are well defined. At t=1/2,
only stream1 has arrived; A2^-1(t) is not defined on its arrival image[2,3].
Extending its affine inverse algebraically to-3/2 silently evaluates a source
rate outside the declared emission domain. For unit source densities the actual
aggregate rate is1; the unqualified algebraic extension would return2.

The full measure formula survives. Smallest repair: either restrict Eq(5) and R
to the common arrival window, or sum over J(t)={j:t in A_j(I_j)} and zero-extend
each pushed-forward density outside its own window. For the latter use the
same active set in R and retain R>0. This is a domain clarification, not a new
physical recording rule or a change to the positive two-stream example.

Two associated precision improvements should accompany it. Generic measure
density identities hold almost everywhere (or pointwise after choosing the
displayed transported representative, with adequate regularity where claimed).
A literal discrete counting measure is atomic and is not nonzero absolutely
continuous; a continuous count/intensity measure or smooth phase is a separate
conditional model. The candidate's 'only if' wording points at this separation
but should say it directly. My source-first report used the same loose phrase
'counting measure' before an optional density case; this review explicitly
narrows that shorthand as well, without editing the sealed report.

## Independent checks, producer repair and omissions

Source-first run:85 exact Fraction controls, exit0,0.025584367 seconds,
11136 KiB maximum resident memory. It separately computes null incidence and
endpoint contractions for five rational rapidities, tests affine scales and
auxiliary observers, verifies moment eigenvectors/normalization, and realizes
two arrival maps at one Minkowski receiving clock. Its unchanged-Z aggregate
rates5/2 and7/2 and coincident tick multiplicities are independent controls,
not copied producer examples. No numerical tolerance is used.

Direct run: independent Fraction arithmetic verifies all initial candidate and
source-first frozen hashes, the candidate's exact moment/current numbers and
aggregate fractions, then executes the disjoint-window defect control. It
exits0 in0.017102137 seconds,14784 KiB. The explicit support counterexample is
an analytic defect witness; its passing test means the defect was reproduced,
not that the uncorrected Eq(5) passed. Exact command, stdout/stderr, versions,
resource bounds and receipts are preserved locally.

The producer failed receipt shows the claimed SymPy simplification failure,
not a false mathematical identity:1+4(s+s^2)=(2s+1)^2 and2s+1>0 on its domain.
Its repaired factorization is source-preserving. The prospective Boolean sum
change is honestly distinguished from the executed failure. Repaired producer
evidence reports28 controls and7 wrong identities rejected; I inspected it,
but did not rerun the same producer implementation or count it as independent.

I did not rerun the full406 audit, historical FSL1/PRI1 suites, native metric
dynamics, optical/detector theory or empirical data. Parent owns the final
fresh premise audit and both-reviewer integration gate. Finite exact checks
support the explicit controls; the argument above owns the general conditional
claim. This verdict adopts no premise and changes no source grade or canon.
