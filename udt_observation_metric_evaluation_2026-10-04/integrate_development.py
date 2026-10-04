"""One-time OEV1 integration; source-preserving documentation, not selection."""
from pathlib import Path
import csv, hashlib, json, sys
sys.path.insert(0,str(Path.cwd()))
import verify_udt_development as guard
B=Path('udt_observation_metric_evaluation_2026-10-04')
W=Path('development_reconstruction_2026-09-29')
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
p=Path('UDT_DEVELOPMENT.md');t=p.read_text()
assert '<a id="r8oev"></a>' not in t
old='**Current development — PRT1 positional translation and step4/5 handoff reviewed,'
assert t.count(old)==1
t=t.replace(old,'**Current development — OEV1 observation constraints and finite evaluator reviewed,',1)
a=t.index('**Current learning.**');z=t.index('<!-- DEVELOPMENT_ORIENTATION_END -->',a)
t=t[:a]+'''**Current learning.** Charles authorized steps 4/5 after PRT1. OEV1 assessed
three observational channels using eight primary papers/releases and executed
a bounded supplied-metric evaluator. Native geometry selection remains OPEN.

Megamaser distances are the strongest immediate independent-distance lead in
this limited comparison. Their distances avoid a redshift-distance cosmology
but retain disk dynamics, source gravity, calibration and posterior dependence.
All six published source rows were converted into frame-labeled spectral-ratio
proxies with separate marginal distance/error intervals. No H0, peculiar-flow,
native curve, joint likelihood or positional attribution was fit. D_A is not
PSW's initial proper separation. Published outcomes were exposed; this is an
exploratory constraint table, not held-out confirmation.

Direct spectroscopic drift and supernova temporal widths ask different questions.
The map preserves observer/source/calibration and population assumptions. A source
precision repair explicitly keeps a tight supernova estimate within the authors'
second-method consistency-check scope, while retaining first-method evidence.
Native dynamics need not be complete to design observations or test a declared
metric/query/readout package; that package is not supplied by these summaries.

The evaluator solves original affine-null/transport equations on the existing
flat, quadratic and cubic controls, with ordinary comoving clocks and fixed
histories. Fourteen queries at three tolerances give 42 retained center records
and 246 ray solves. Tight 14 pass the frozen limits; coarse rows remain refinement
diagnostics. A separate high-precision implementation checks all 6393 saved
samples and 246 endpoint roles, with targeted corrupted-record rejection.
Independent source-table arithmetic also passes. These are finite conditional
checks, not native admission, a continuum enclosure or an asymptotic proof.

Actual-workload smoke includes interruption after a checkpoint, exact restart
agreement and mismatched-config rejection. The CPU workload took seconds and
used no GPU or multi-hour run. Stage 4B returns the handoff's permitted narrowed
observable constraints; stage 5A is complete at the supplied-control scope.
Stage 5B still needs an admitted metric equation/constraint class, chart/gauge,
domain and sufficient initial/boundary data. An evaluator does not provide those.

After orientation read R8OEV and R18. The next scientific gate is one explicit
astronomical metric/query/readout package predicting the same distance/spectrum,
with source/motion conventions and joint uncertainties. More samples of these
controls would not close that physical connection. No new premise, scale or
field law is adopted, and no whole-postulate insufficiency is proved. Stop for
lay discussion; no broader solver or parked campaign restarts automatically.
Two fresh same-model contexts provide actual scoped reviews and distinct
numerical checks; source/outcome exposure and omitted raw pipelines remain
disclosed. Final attestations and normal/maintenance/full 406 receipts own closure.
'''+t[z:]
marker='#### Finite mutual ticking and its causal limits — FPC1'
assert t.count(marker)==1
t=t.replace(marker,(B/'CENTRAL_INSERT.md').read_text()+'\n\n'+marker,1)
old='No stage4/5 campaign is executed here. [Initial candidate]'
new='PRT1 ended with that handoff; OEV1 below executes its bounded next stages. [Initial candidate]'
assert t.count(old)==1;t=t.replace(old,new,1)
a=t.index("[PRT1's decision brief]");z=t.index("\n\nNGD1's numerical return",a)
t=t[:a]+'''The [fixed PRT1 return](udt_positional_requirement_translation_2026-10-04/DECISION_BRIEF.md)
retains that conditional chain. Charles then authorized steps 4/5, now developed
in R8OEV. OEV1's three-channel/eight-source assessment selects megamaser distance
and systemic spectral summaries as the immediate limited data lead. Six source
rows yield explicit marginal constraints with the disk/readout/frame assumptions
retained. No redshift-derived distance, D_A-to-PSW-L identification, H0/flow fit,
joint likelihood or native positional attribution enters that conversion.

The bounded evaluator solves the original affine/transport query on existing
controls and passes actual smoke/restart and independent saved-artifact checks.
Its 14 queries at 3 tolerances are 42 retained records; tight 14 meet frozen limits.
It supplies no metric evolution, native admission or physical scale. Observed
numerical refinement and finite sample agreement are not continuum/global proofs.

[OEV1's decision brief](udt_observation_metric_evaluation_2026-10-04/DECISION_BRIEF.md)
owns the current lay return. Stage 4A is complete; 4B returns the permitted narrowed
observable constraints rather than a nonexistent native-candidate likelihood.
Stage 5A is complete for the declared controls; 5B's native-evolution gate remains
open. The source map and published errors do not decide a physical geometry.
No whole-postulate insufficiency or new-postulate necessity is inferred.

The next scientific gate is one concrete astronomical metric/query/readout
package predicting the same angular distance and spectral ratio, with actual
source/observer histories, ray/area geometry, source/disk/frame conventions or
justified recalibration, motion nuisance treatment and a joint uncertainty model.
This can be developed and tested while native dynamics remains open, provided
its conditional status is explicit. Existing marginal constraints are usable;
unproved source/physical joins limit the inference rather than erase the data.

A native time-live search additionally needs an admitted equation/constraint
class, metric degrees of freedom and gauge, domain and sufficient initial/
boundary data. R6/R7 are query equations on supplied geometry. Re-running the
same control shapes or launching a larger GPU job would not supply the missing
physical relation. Existing conditional field branches, source/GW/GOCE pauses
and protected work remain at their original scope. Stop for lay discussion;
no new adoption, raw-data replay, large solver or automatic campaign restart.
'''+t[z:]
marker='The preserved first candidates expose the repair history.'
addition='''OEV1 uses one observation researcher and two fresh source-first/exposed/final
reviewer contexts. Published outcomes and old proof/verdict exposure are explicit.
Parent numerical equations/code/matrix and diagnostic rules were frozen before
execution; its initial result prose was assembled after the scoped findings.
The mathematical reviewer independently derived the original metric equations
and froze a distinct 60-digit quadrature/affine/transport checker before outcome
handoff. It checked 6393 samples and 246 endpoint roles, repeated extreme anchors
at 90 digits and rejected three corrupted records. The fidelity reviewer visually
checked the primary table and separately replayed 60 numeric fields with Decimal 60.
Its S1 method-ownership objection was repaired with original map/ledger preserved
and actual re-review. No numerical code/config repair was needed. Tight/coarse
acceptance, source covariance limits, failed retrievals and omitted pipeline
replays remain explicit in the [work record](udt_observation_metric_evaluation_2026-10-04/WORK_RECORD.md)
and [descendant review](udt_observation_metric_evaluation_2026-10-04/DESCENDANT_REVIEW.md).
Same-model fresh contexts and distinct numerical implementations are claimed;
human, different-model, formal interval and independent empirical confirmation
are not. Actual final accepted-map attestations and captured normal/maintenance/
full 406 checks own closure; none selects native physics.

'''
assert t.count(marker)==1;t=t.replace(marker,addition+marker,1)
p.write_text(t);Path('CURRENT_RESEARCH_PROGRAM.md').write_text(guard.program_text(t))

common='''CDR1 remains the central-development architecture. UDT_DEVELOPMENT.md is the
sole maintained scientific argument; CURRENT_SCIENTIFIC_PREMISES.tsv and reviewed
sources own exact grades. The generated CURRENT_RESEARCH_PROGRAM.md is the bounded
startup orientation. Read R8OEV and R18 after orientation; exact older sources
only when load-bearing.

After PRT1 at 51551332, Charles authorized steps 4/5. OEV1 evidence is in
udt_observation_metric_evaluation_2026-10-04/; WORK_ORDER owns scope and stops.
One observation researcher and two fresh source-first/exposed/final contexts
reviewed the three-channel map, narrowed published-data conversion and finite
supplied-metric evaluator. Frozen inputs/code, original source wording and actual
precision repair/re-review are preserved. Final attestations and normal/
maintenance/full 406 receipts own closure; commit/push and byte checks own banking.
Verify actual HEAD, remote, dirt and processes rather than treating this text
as the tip.

Next: Stop for lay discussion of the OEV1 return. Stage 4A and the narrowed 4B
constraint table are complete; 5A is complete at its supplied-control scope.
No native-candidate likelihood or 5B native metric evolution was performed.
R18 states the concrete astronomical comparison and metric-equation/data gates.
The finite CPU workload passed smoke/restart and independent numerical checks;
no GPU or multi-hour run was needed. No new premise, registry promotion,
physical scale or automatic campaign restart follows. Standing pauses,
no-timeout/resource/manual-stop rules and protection of unrelated work persist.

'''
for name,title,tail in [('LIVE.md','## CURRENT STATE — OEV1 observation/evaluator return, 2026-10-04','### Honest claim'),('HANDOFF.md','## Current handoff — OEV1 observation/evaluator return, 2026-10-04','Protected payloads require explicit dispatch; preserve without inspecting/hashing:')]:
 p=Path(name);q=p.read_text();a=q.index('## CURRENT STATE') if name=='LIVE.md' else q.index('## Current handoff');z=q.index(tail)
 q=q[:a]+title+'\n\n'+common+q[z:]
 if name=='LIVE.md':
  a=q.index('Use central R8PRT/R18');z=q.index('\n<!-- STARTUP_CURRENT_END -->',a)
  q=q[:a]+'''Use central R8OEV/R18 and OEV1's decision brief for lay discussion of the
usable observation constraints, evaluator and remaining physical connection.
An astronomical metric/query/readout package and native evolution equation/data
class remain distinct gates. No larger control sweep or parked campaign starts
automatically. Verify final bindings/checks and synchronization before integration.
Existing pauses/protected boundaries persist. TPS1 raw fields/large streams
remain local-only; compact remote records cannot replay raw-dependent checks.
'''+q[z:]
 p.write_text(q)

p=W/'DEVELOPMENT_GRAPH.json';g=json.loads(p.read_text());assert all(n['id']!='R8OEV' for n in g['nodes'])
sources=[str(B/s) for s in ['WORK_ORDER.md','INITIAL_RESULT.md','observation/CHANNEL_MAP.md','observation/SOURCE_LEDGER.json','observation/DIAGNOSTIC_PLAN.md','observation/MCP_TABLE1_INPUT.tsv','observation/MCP_CONSTRAINTS.tsv','observation/reduce_table.py','numerics/FREEZE.json','numerics/config.json','numerics/evaluate.py','numerics/summarize.py','numerics/RESULT.json']]
g['nodes'].append(dict(id='C_OEV_READOUT',kind='conditional_protocol',statement='For observation branch: exposed eight-source/three-channel assessment and six MCP XIII Table1 marginal disk-distance/CMB optical-velocity summaries; conventional source dynamics/gravity/frame reductions retained. Exact v/c and log1p conversions only, no joint likelihood or covariance-zero, positional attribution, D_A=PSW L, H0/flow fit or native candidate.',sources=sources[:8],registry_ids=[]))
g['nodes'].append(dict(id='C_OEV_CONTROLS',kind='conditional_protocol',statement='For numerical branch only: supplied unquotiented 4D metrics a=1,1+t^2,1+t^3 with cubic t>-1; radial invariant slice, comoving proper clocks, preparation0, fixed histories, actual finite future first/selected reverse/echo queries. Separate nondimensional control scales, original affine/transport equations, frozen finite matrix/tolerances; tight 14 at 3-setting total42 rows. No native metric admission, general-clock/caustic/continuum or physical scale claim.',sources=sources,registry_ids=[]))
g['nodes'].append(dict(id='O_OEV_NATIVE',kind='open_join',statement='Native astronomical metric/query/readout assignment, source/motion calibration and joint uncertainty model remain open for candidate confrontation; observation design/marginal constraints do not require native dynamics to be closed. Native metric evolution additionally needs admitted equation/constraint class, gauge/domain and sufficient data. No whole-postulate insufficiency or new-premise necessity follows.',sources=sources[:4],registry_ids=[]))
g['nodes'].append(dict(id='R8OEV',kind='argument',anchor='r8oev',title='Source-conditional observational constraints and checked finite supplied-metric evaluator; native astronomical comparison/evolution open',sources=sources,registry_ids=[],required_conditions=['C_OEV_READOUT','C_OEV_CONTROLS']))
for frm in ['C_OEV_READOUT','C_OEV_CONTROLS']:
 g['edges'].append({'from':frm,'to':'R8OEV','kind':'hypothesis'})
for frm in ['R6','R7']:g['edges'].append({'from':frm,'to':'R8OEV','kind':'proof'})
for frm in ['D1','R8','R8PRT','R8PCC','R8ACI','R8GRL','R9','R13','R14','R16','R17']:g['edges'].append({'from':frm,'to':'R8OEV','kind':'context'})
g['edges'].append({'from':'O_OEV_NATIVE','to':'R8OEV','kind':'open_boundary'})
g['edges'].append({'from':'R8OEV','to':'R18','kind':'context'})
for source in sources:g['sources_sha256'][source]=sha(source)
targets=['D1','R6','R7','R8','R8PRT','R8PCC','R8ACI','R8GRL','R9','R13','R14','R16','R17','R8OEV','R18','C_OEV_READOUT','C_OEV_CONTROLS','O_OEV_NATIVE']
support=['DESCENDANT_REVIEW.md','WORK_RECORD.md','observation/EXPOSURE.md','source_precision/REPAIR_RECORD.json','review_math/SOURCE_FIRST.md','review_math/CANDIDATE_REVIEW.md','review_math/INDEPENDENT_RESULT.json','review_fidelity/SOURCE_FIRST.md','review_fidelity/EXPOSED_REVIEW.md']
for source in support:
 source=str(B/source);g['review_support'].append(dict(path=source,sha256=sha(source),role='review_evidence',targets=targets))
p.write_text(json.dumps(g,indent=2)+'\n')
row=['OEV1_RETURN',str(B/'INITIAL_RESULT.md'),'VERIFIED-WITH-CAVEATS_OBSERVATION_INTERFACE_AND_FINITE_EVALUATOR; native astronomical comparison/evolution OPEN; no physical adoption or empirical confirmation',';'.join(targets[:15]),'THREE_CHANNEL_EIGHT_SOURCE_MAP; SIX_EXPOSED_MARGINAL_CONVERSIONS; TWO_FRESH_SOURCE_FIRST_EXPOSED_FINAL_REVIEWERS; independent highprecision6393samples/246endpoint roles and Decimal 60; source-precision repair',sha(B/'INITIAL_RESULT.md')]
with (W/'RECENT_DISPOSITIONS.tsv').open('a',newline='') as f:csv.writer(f,delimiter='\t',lineterminator='\n').writerow(row)
print(json.dumps(dict(nodes=len(g['nodes']),edges=len(g['edges']),source_pins=len(g['sources_sha256']),orientation_words=len(guard.orientation(t).split()))))
