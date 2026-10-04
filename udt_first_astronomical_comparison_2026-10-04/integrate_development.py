"""One-time ACP1 source-preserving central integration."""
from pathlib import Path
import csv,json,hashlib,sys
sys.path.insert(0,str(Path.cwd()))
import verify_udt_development as guard
B=Path('udt_first_astronomical_comparison_2026-10-04');W=Path('development_reconstruction_2026-09-29')
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
p=Path('UDT_DEVELOPMENT.md');t=p.read_text();assert '<a id="r8acp"></a>' not in t
old='**Current development — OEV1 observation constraints and finite evaluator reviewed,'
assert t.count(old)==1;t=t.replace(old,'**Current development — ACP1 first astronomical comparison constructed and audited,',1)
a=t.index('**Current learning.**');z=t.index('<!-- DEVELOPMENT_ORIENTATION_END -->',a)
t=t[:a]+'''**Current learning.** Charles authorized construction and audit of the first
astronomical comparison. ACP1 now specifies how one geometry must predict the
CGCG 074-064 maser spots' observed directions, spectral shifts and monitored
changes together. It is a concrete conditional forward comparison, not a
selected astronomical metric, fitted distance curve or empirical confirmation.

R6/R7 provide the actual clock/null readout, and R13 provides the full angular
map. A scalar distance determines area but does not determine shear or the
complete spot map. Importing the published scalar distance requires its source-
compatible map approximation or a justified refit. The correct receiver-time
optical slope also contains the optical-velocity convention: a constant common
redshift factor cancels from that derivative, while remaining in the spectral
offset and received timing. No extra slowdown factor may be appended by habit.

The source likelihood retains its conventional disk/transition/calibration,
measurement flags, error floors and finite-window estimator. The full spot
table and estimator were not retrieved/replayed, and no likelihood fit ran.
The CGCG summary yields conditional endpoint/area restrictions; printed marginal
statistical intervals and separately reported model-choice systematics stay
separate. A fitted systemic redshift is not itself an actual regular reference
clock. Its transformed Phi/chi summaries need that additional realization
before becoming an R6 clock leg or any native event/path-depth assignment.

Two fresh same-model contexts independently reconstructed source and geometry
interfaces, checked distinct exact/high-precision examples, and re-reviewed
four source-preserving precision repairs. Their actual final attestations and
normal/maintenance/full406 receipts own closure. Initial code failures and
exposure history are retained; no human/different-model or formal interval
certification is claimed. OEV1's observation map and finite evaluator survive
at their original scope, with summary portability now made more explicit.

After orientation read R8ACP and R18. The next scientific gate is an actual
candidate metric with consistent source histories and the required observation
reduction. Native geometry/evolution and reference-clock realization remain
open. No whole-postulate insufficiency, new physical law, X_max scale or native
matter/light model follows. Stop for lay discussion; no fit, larger numerical
campaign or parked/protected program restarts automatically.
'''+t[z:]
marker='#### Finite mutual ticking and its causal limits — FPC1';assert t.count(marker)==1
t=t.replace(marker,(B/'CENTRAL_INSERT.md').read_text()+'\n\n'+marker,1)
needle='None of these channels automatically supplies the prepared query of R8PRT.'
assert t.count(needle)==1
t=t.replace(needle,needle+''' ACP1 below
makes the source-summary portability conditions explicit: a general geometry
requires its full angular map or a justified scalar reduction, and a fitted
systemic factor needs a regular reference-clock realization before becoming
an actual R6 clock leg. OEV1's preserved arithmetic is unchanged.''',1)
needle='This is metric angular-area reciprocity; it does not yet identify\nbrightness, luminosity distance, photons or detector flux.'
assert t.count(needle)==1
t=t.replace(needle,needle+''' ACP1's astronomical
application in R8ACP retains the complete observer-to-source Jacobi map;
its determinant alone does not supply a scalar disk-length map. Source/observer
and finite-patch identification are separate conditional readout requirements.''',1)
a=t.index("[OEV1's decision brief]");z=t.index("NGD1's numerical return",a)
t=t[:a]+'''OEV1 completed its observation map, permitted narrowed marginal constraints
and finite supplied-control evaluator. It did not select an astronomical metric
or native evolution equation. Charles then authorized ACP1 to construct and
audit the first actual astronomical comparison.

[ACP1's lay return](udt_first_astronomical_comparison_2026-10-04/DECISION_BRIEF.md)
owns the current discussion. R8ACP specifies one same-metric forward comparison
for CGCG 074-064: actual spot directions, spectral ratios and their finite-window
changes. It derives the optical-drift accounting and full angular-map requirement,
retains the source-owned likelihood and reports concrete summary restrictions.
The selected target is justified by explicit source documentation, not by a
successful UDT fit. No fitted or native astronomical geometry is supplied.

The audit narrows the source bridge: statistical margins do not replace model
systematics; a scalar D needs the matching source/map approximation; a fitted
systemic z0 needs a regular reference-clock realization before an actual R6
clock-leg interpretation. No clock is invented at the SMBH center. A full
spot-level test needs the complete table, source histories and actual
monitoring/channel reduction. Access failures and a source count inconsistency
are retained without manufacturing data or asserting the published fit is wrong.

The next scientific target is a candidate metric from UDT commitments, or an
explicitly authorized conditional class, with source histories consistent with
that geometry. It must predict the whole stated comparison before being tested;
a separate Z(D) profile cannot close the metric connection. The statistical
comparison additionally needs the actual data/reduction and declared source
uncertainties. These are now specific inputs to a concrete construction.
Native metric evolution still separately needs admitted equations/constraints,
gauge/domain and sufficient data. An observational forward comparison does not
provide a field law, and its open inputs do not prove that UDT needs a new
postulate. Existing conditional field/source branches, pauses and protected
work remain unchanged. Stop for lay discussion; no automatic fit or large solve.

'''+t[z:]
marker='The preserved first candidates expose the repair history.';assert t.count(marker)==1
t=t.replace(marker,'''ACP1 uses two actual fresh source-first/exposed/final contexts. They checked
FSL1/G348 and the actual MCP source passages, then independently executed
Fraction/Decimal70 and Decimal80 checks without importing parent code. The
18-case mathematical check and 45-case source/arithmetic check retain their
exact scopes, failures and comparisons. Parent symbolic and nine high-precision
inverse-arrival checks supplement the argument. Initial parent output-write
and reviewer syntax failures are preserved with freezes and repaired execution.
Four precision repairs fix the sky-map sign, reference-clock ownership, finite
monitoring estimator and separate systematics. Both actual exposed reports
re-reviewed the repair. Final integrated-byte attestations are distinct from
those scientific checks; normal/maintenance/full406 and banking remain actual
operational gates. The [work record](udt_first_astronomical_comparison_2026-10-04/WORK_RECORD.md)
and [descendant review](udt_first_astronomical_comparison_2026-10-04/DESCENDANT_REVIEW.md)
retain exposure, source limits and positive/adverse uses. No full dataset fit,
old-corpus reproof, human/different-model review, native adoption or empirical
confirmation is claimed.

'''+marker,1)
p.write_text(t);Path('CURRENT_RESEARCH_PROGRAM.md').write_text(guard.program_text(t))
common='''CDR1 remains the central-development architecture. UDT_DEVELOPMENT.md is the
sole maintained scientific argument; CURRENT_SCIENTIFIC_PREMISES.tsv and reviewed
sources own exact grades. CURRENT_RESEARCH_PROGRAM.md is its generated bounded
orientation. After orientation read R8ACP and R18; older exact sources only when
load-bearing.

After OEV1 at7fc10f93, Charles authorized construction and audit of the first
astronomical comparison. ACP1 evidence is in
udt_first_astronomical_comparison_2026-10-04/; WORK_ORDER owns scope and stops.
Two actual fresh source-first/exposed/final contexts audited the CGCG comparison
and source/geometry joins, independently checked finite quantities and
re-reviewed four precision repairs. Initial candidates, failures, sources and
exposure are preserved. Actual final attestations, normal/maintenance/full406
receipts and committed/remote byte checks own closure. Verify HEAD, remote,
dirt and processes yourself; this prose is not the current commit hash.

Next: Stop for lay discussion of ACP1. A conditional astronomical forward
comparison is constructed; no candidate metric or likelihood fit is supplied.
R18 names the remaining native candidate, source-reference and observation-data
requirements. The complete spot table/estimator was not retrieved/replayed.
No new physical premise, registry promotion, scale or field law was adopted.
No GPU/long production ran, and no larger solve or parked campaign restarts
automatically. Standing pauses/no-timeout/manual/resource/protected-work rules
remain in force.

'''
for name,title,tail in [('LIVE.md','## CURRENT STATE — ACP1 astronomical comparison return, 2026-10-04','### Honest claim'),('HANDOFF.md','## Current handoff — ACP1 astronomical comparison return, 2026-10-04','Protected payloads require explicit dispatch; preserve without inspecting/hashing:')]:
 p=Path(name);q=p.read_text();a=q.index('## CURRENT STATE') if name=='LIVE.md' else q.index('## Current handoff');z=q.index(tail);q=q[:a]+title+'\n\n'+common+q[z:]
 if name=='LIVE.md':
  a=q.index('Use central R8OEV/R18');z=q.index('\n<!-- STARTUP_CURRENT_END -->',a)
  q=q[:a]+'''Use central R8ACP/R18 and ACP1's decision brief for discussion of the
constructed comparison, corrected readout and remaining candidate/data inputs.
No astronomical metric, fit or native evolution law is selected by the audit.
Verify actual final review/check/banking records. Existing pauses/protected
boundaries persist. TPS1 raw fields/large streams remain local-only; compact
remote records cannot replay raw-dependent checks.
'''+q[z:]
 p.write_text(q)
p=W/'DEVELOPMENT_GRAPH.json';g=json.loads(p.read_text());assert not any(n['id']=='R8ACP' for n in g['nodes'])
sources=[str(B/x) for x in ['WORK_ORDER.md','INITIAL_CANDIDATE.md','REPAIR.md','COMPARISON_CONTRACT.json','PREMISE_LEDGER.tsv','CONSTRUCTION_RESULT.json','check_construction.py','CHECK_FREEZE.json','REPAIRED_CHECK_FREEZE.json']]
g['nodes'].extend([
 dict(id='C_ACP_QUERY',kind='conditional_protocol',statement='Actual CGCG maser/receiver histories, one supplied smooth Lorentz geometry, regular null branches, calibrated astrometry, source cadence and actual finite observation reduction. Full angular map precedes scalar source-compatible approximation. No native metric supplied.',sources=sources,registry_ids=[]),
 dict(id='C_ACP_SOURCE',kind='conditional_protocol',statement='MCP XI conventional disk/transition/frame/likelihood and XIII related marginal summary retained as conditional readouts; measured flags, source floors/priors and separate statistical/model-choice systematics. Full table/estimator not retrieved/replayed; no fit or double counting.',sources=sources,registry_ids=[]),
 dict(id='O_ACP_REALIZATION',kind='open_join',statement='Native candidate metric with consistent source histories, regular reference-clock realization for systemic z0, complete data/reduction and statistical treatment remain open. Missing joins neither erase conditional forward map nor prove whole-postulate insufficiency.',sources=sources[:4],registry_ids=[]),
 dict(id='R8ACP',kind='argument',anchor='r8acp',title='First actual astronomical comparison: full angular map and optical-drift accounting; native/source realization open',sources=sources,registry_ids=[],required_conditions=['C_ACP_QUERY','C_ACP_SOURCE'])])
for frm in ['R6','R7','R13']:g['edges'].append({'from':frm,'to':'R8ACP','kind':'proof'})
for frm in ['C_ACP_QUERY','C_ACP_SOURCE']:g['edges'].append({'from':frm,'to':'R8ACP','kind':'hypothesis'})
for frm in ['D1','R8PRT','R8OEV','R8ACI','R8GRL','R9','R14','R16','R17']:g['edges'].append({'from':frm,'to':'R8ACP','kind':'context'})
g['edges'].append({'from':'O_ACP_REALIZATION','to':'R8ACP','kind':'open_boundary'});g['edges'].append({'from':'R8ACP','to':'R18','kind':'context'})
for s in sources:g['sources_sha256'][s]=h(s)
targets=['D1','R6','R7','R13','R8PRT','R8OEV','R8ACI','R8GRL','R9','R14','R16','R17','R8ACP','R18','C_ACP_QUERY','C_ACP_SOURCE','O_ACP_REALIZATION']
for s in ['WORK_RECORD.md','DESCENDANT_REVIEW.md','review_math/SOURCE_FIRST.md','review_math/DIRECT_REVIEW.md','review_fidelity/SOURCE_FIRST.md','review_fidelity/EXPOSED_REVIEW.md']:
 s=str(B/s);g['review_support'].append(dict(path=s,sha256=h(s),role='review_evidence',targets=targets))
p.write_text(json.dumps(g,indent=2)+'\n')
row=['ACP1_RETURN',str(B/'INITIAL_CANDIDATE.md'),'VERIFIED-WITH-CAVEATS_REPAIRED_CONDITIONAL_ASTRONOMICAL_COMPARISON; native metric/source realization OPEN; no fit or adoption',';'.join(targets[:14]),'SOURCE_FIRST_EXPOSED_FINAL_REVIEW; four source-preserving precision repairs; independent18case math and45case source checks; original failures retained',h(B/'INITIAL_CANDIDATE.md')]
with (W/'RECENT_DISPOSITIONS.tsv').open('a',newline='') as f:csv.writer(f,delimiter='\t',lineterminator='\n').writerow(row)
print(json.dumps({'nodes':len(g['nodes']),'edges':len(g['edges']),'source_pins':len(g['sources_sha256']),'orientation_words':len(guard.orientation(t).split())}))
