# NT1 initial direct adversarial review — before the one repair cycle

Date: 2026-09-09 UTC. Reviewer `/root/nt1_review`, fresh separate context.
Candidate SHA256 `79fe1d00a2c04bf0fa5e14c9c1ddfa38caa7de61256739f3d5cb6ca094435a88`.
Original checker SHA256 `92d38908a148caa2eaf5fc1612ad714e4ad87fcc96320136a930ca10fa4b3bda`.
Source pin `5ece4ae086cc9b0f93a5635867600ad92324d150`.

Scientific disposition: no defect found in the bounded argument; its necessary
first-neighborhood criterion and declared nonrealizable record assignment
survive direct review. The original baseline artifacts independently check.
Two actual implementation false passes are established below. Parent elected
the ONE grouped same-premise repair/re-review cycle for these guards. Final
NT1 handoff/conditional downstream use waits for that focused disposition.
This report remains unchanged as pre-repair history.

## Exposure and separate independence axes

Source-first notes, results, script and captures were sealed at
23:54:46.579969 UTC, before the author proof/code/results were opened. Seal
stdout SHA256 is `b5454ee8ae3a3a08cb0dec6ad2b36f351a1a06852ed8879f8b75f24069f26c4f`.
Parent reports its author freeze at 23:58:24 UTC before reading reviewer
findings. Phase B release arrived subsequently. Reviewer then read the whole
candidate and manifests, independently translated the WRITTEN div/curl
system into the generic bivector derivative space, and only afterward opened
author code, output/history and method-source notes.

A finite Lorentz-product derivative check was constructed after the first
source-first seal but before author proof/code exposure, and its baseline
started 23:58:40.907032 UTC. It differentiates an actual four-factor finite
frame transformation, independently of the author's action() subtraction.
The original source-first notes/results were not revised after their seal.

Fresh context: YES. Exact deployed model identifier: unavailable; instructions
describe Codex/GPT-6, but same/different model relative to parent is UNKNOWN.
Different-model, human and formal-proof axes: UNTESTED. Source-first argument:
YES. Independent scientific implementation: generic 21-coefficient symmetric
bivector elimination with SymPy, versus author's explicit E/B tensors and
Fraction row reduction reusing admitted G358 code. Direct candidate comparison
uses the independent source-first basis. Shared infrastructure: unchanged
run_capture.py only. Same-code author replays are regression, not independence.
The focused repair review will be this SAME now-exposed reviewer.

Historical verdicts of admitted sources were exposed as source provenance.
No NT2 proof/candidate/results, protected work, observations or archives read.
Current tracking changes made by parent after the pinned base are separate
from the authenticated unchanged admitted scientific sources.

## Load-bearing mathematical review

The premise boundary is correct: owner-provisional G310/G312 bounded smooth
vacuum Einstein arena, supplied Lorentz geometry/frame/query/derivative
registration, and G358's explicit Q slots. G348 owns the ideal geometric tide;
none supplies a detector law. G315 constrains lawful full initial data and
provides only conditional local-development methods. No equation, carrier,
source, normalization law or actual history is silently added.

The reconstruction uses C=E+Lambda I/3 and the already admitted mixed B.
W vanishes when E=-Lambda I/3 and B=0. Its first covariant derivative must
subtract connection action in all FOUR curvature arguments. There is no
fifth correction for the derivative-direction argument at first derivative
order: nabla_(e_mu)W is evaluated on those four arguments. Differentiated
null normalization and query-frame variation are accounted for by the smooth
registered tetrad, rather than falsely identifying the six directions with
one family of globally affine rays.

The full differential Bianchi identities reduce to

    div C = div B = 0,
    D0 C + curl B = 0,
    D0 B - curl C = 0,

with the candidate's epsilon orientation and symmetric curl. Independent
translation of the written equations has rank 16 on the 40-dimensional
Weyl-derivative space. Appending scalar derivatives gives rank 20 on 44
Einstein-derivative coordinates. Its stacked row space with FULL differential
Bianchi still has rank 20; the candidate equations annihilate the entire
independently computed Bianchi kernel, not just selected examples. A flipped
B-curl sign leaves its own rank unchanged but raises the stacked rank to 25
and produces residual 2 on the true kernel; hence the comparison genuinely
tests signs beyond dimension counting. Removing one divergence lowers ranks
to 15/19 and fails. Exact arithmetic plus the complete basis cover this
finite algebra; they do not prove a PDE realization theorem.

The analytic independence count also survives: the ten time components are
determined uniquely, and each C/B divergence map from arbitrary spatial STF
gradients onto three components is surjective by the stated compensated
diagonal construction. All four scalar derivatives are independently removed.
These are formal first-derivative dimensions, correctly not physical modes.

The obstruction has the correct universal quantifier over unknown connection
and extrinsic/initial-data extensions. At W(p)=0 all four connection-action
terms vanish, including for nonzero Lambda because its scalar tensor is
parallel. The prescribed E=x1 diag(1,-1,0)-Lambda I/3, B=0 record germ passes
every one-event relation with constant Lambda. With e_mu(p)=partial_mu, it
has div C=(1,0,0), and thus cannot arise from ANY smooth Einstein metric/frame
realization with those declared directional derivatives. Full Bianchi has
residuals -1,+1; the explicit C/B system also has curl residual 1/2. No
unmentioned time derivative can cure the divergence because the omitted
Q_000j slot vanishes identically. Changing the supplied first jet changes the
assignment; a passive relabeling transforms the nonzero tensor residual.

This conclusion does not demand K=0, a globally parallel frame, a flat
neighborhood, or selected initial geometry. At W!=0 uncorrected slopes do
depend on unknown frame/connection data, as the candidate explicitly says.
Even existence of some pointwise connection correction does not establish
torsion-free Levi-Civita compatibility or higher metric/PDE integrability.
Passing the first-jet test does not establish actual realization. The later
NT2 question remains separate. No distinctive UDT empirical conclusion follows.

## Independent artifact recomputation and actual probes

`saved_artifact_check.stdout` authenticates the original saved 24x40 full
Bianchi matrix, 16x40 explicit C/B matrix, exact RREF/pivots, and 40x24 kernel
against the independent generic tensor construction. Every matrix entry
agrees. The original kernel has rank 24 and identity free-coordinate block,
and satisfies M K=0. The original bad-jet residual agrees componentwise.
The original baseline checker was rerun: PASS17, stdout AND stderr byte-identical
to frozen author_final streams. This replay remains regression evidence.

The four registered author mutations were actually replayed. omit_bianchi and
wrong_cycle fail weyl_differential_rank_sixteen; omit_connection fails
all_slot_connection_correction; drop_divergence fails
explicit_six_divergences_ten_evolution_equivalent. All exit 1 with preserved
streams. Independent finite-frame tests reject omitted final slot and wrong
connection-action sign against direct Lorentz-product differentiation.

Two additional actual corruptions defeat the ORIGINAL author checker:

1. Globally double action(q,A) while retaining its use for both raw and
   correction. The checker returns PASS with all 17 guards. Scalar and zero
   curvature remain annihilated and raw-minus-identical-action stays zero,
   so those controls cannot determine the correct coefficient. A separately
   differentiated finite boost produces nonzero discrepancies +/-2 in 16
   components for this corruption. The defective guard is
   all_slot_connection_correction as an independent formula certificate;
   candidate/history already explicitly exclude that interpretation. Smallest
   strengthening: compare action against direct finite frame differentiation.

2. Replace every `kernel.append(v)` with `kernel.append([F(0)]*40)`.
   The checker returns PASS with all 17 guards and a returned kernel of rank
   ZERO. Counting 24 vectors and checking membership cannot establish a basis.
   Defective guard: twentyfour_full_kernel_vectors as a basis certificate.
   Smallest strengthening: require rank 24 or the expected identity block at
   the computed free columns, in addition to membership. Original saved basis
   is independently rank 24; the proof's rank-nullity argument survives.

`run_author_probe.py` preserves the exact original-source pin, replacement
rule and mutated-source hash in each raw capture. Original source was never
edited. The failed checks belong to the implementation's sensitivity, not a
refutation of the original numerical outputs or the analytic theorem.

## Resources, preserved limitations and repair boundary

Every reviewer computational child used one library thread, 512 MiB address
space and 60-second CPU/wall limits through the unchanged capture wrapper.
Observed Python 3.10.12 and SymPy 1.13.1. Exact runs took approximately
0.16--3.86 seconds each. The finite-frame mutation runs briefly overlapped at
launch; each individually retained its one-thread/resource bounds. No GPU,
grid, production solve or external scientific browse was used by reviewer.

The parent startup_363 audit receipt was read: successful full audit, not a
reviewer rerun. All 10 candidate-manifest entries, 13 source-manifest entries
and 12 sealed source-first payloads authenticated. The author initial CPU
failure/LOST unflushed intermediate outputs remain as documented; reviewer
does not reconstruct or credit those outputs. The reviewer source-first
exact-valued-float representation correction and excluded tautological check
also remain. Early harmless missing-path reads and premature exact-row query
are disclosed in sealed source-first notes, not silently erased.

No full admitted-source suite replay/reproof, actual Einstein-development
construction, convergence study, different model, human specialist, formal
proof assistant, physical interface test, source promotion or shared Git
mutation was performed. Source documents are version-pinned rather than
duplicated; hashes establish correspondence, not trusted external chronology.

The shared no-shortcuts, scope and verification protocols drove full-slot
scrutiny, exact quantifiers and actual false-pass probes; they supplied no
scientific premise. Parent has chosen one grouped guard repair with unchanged
scientific formula/scope. Preserve this report and all original failures;
focused re-review must rerun BOTH actual corruption rules on the repaired
checker and verify that accepted evidence and candidate text stay unchanged.
