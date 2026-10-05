"""OAA1 central integration, preserving original source/grade authority."""
from pathlib import Path
import json,csv,hashlib,sys
sys.path.insert(0,str(Path.cwd()))
import verify_udt_development as guard
B=Path('udt_operational_asymptote_attachment_2026-10-04');W=Path('development_reconstruction_2026-09-29')
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
p=Path('UDT_DEVELOPMENT.md');t=p.read_text();assert '<a id="r8oaa"></a>' not in t
old='**Current development — CPR1 existing-commitment restriction audit reviewed,'
assert t.count(old)==1;t=t.replace(old,'**Current development — OAA1 conditional affine-distance attachment reviewed,',1)
a=t.index('**Current learning.**');z=t.index('<!-- DEVELOPMENT_ORIENTATION_END -->',a)
t=t[:a]+'''**Current learning.** OAA1 connects the existing conditional clock asymptote
to a specified geometric distance. Along the actual source/receiver histories,
the receiver-normalized affine distance tends to1/H while received redshift
diverges. On the already supplied preparation a simple pole in the distance
deficit follows from the metric and rays. No separate redshift curve is fitted.
The emitter normalization of the same ray instead grows without bound.

This supplies a concrete geometric attachment, while its native physical meaning
remains open. The finite endpoint is not a universal maximum: another allowed
preparation approaches it from above, with an exact rational sign proof. The
from-below result holds on its stated eventual tail, not every earlier epoch.
Late receiver events cannot return a signal to the original interior source;
the affine limit is therefore distinct from that source's completed radar
experiment. Neither observer-dependent readouts nor this scoped counterexample
refute the owner's same-law universality or intended asymptotic target.

Two actual fresh contexts reconstructed the argument and checked saved quantities
with independent implementations. Parent finite checks, the exact ceiling
counterexample and the conditional circular-source radar bound pass. A reviewer
caught an overbroad finite-time sentence; its narrower tail scope and initial
text are preserved. A source-first early-branch failure and reviewer resource
repair remain visible. Actual final bindings and normal/maintenance/full406
receipts own closure. No native metric/distance selection or empirical test
has been established, and physically matched GR records remain identical.

After orientation read R8OAA and R18, with R8/SGE1, R13 and R16 as needed.
The remaining attachment is physical selection and independent observational
meaning. A proposed next bounded step is the same candidate's actual angular/
Jacobi map, to test how this affine endpoint relates to geometric source-size
and angle records. It does not assume affine equals angular distance or select
UDT dynamics. Stop for lay discussion; no automatic successor, fit, physical
adoption, large solve or parked/protected campaign restart.
'''+t[z:]
marker='#### Finite mutual ticking and its causal limits — FPC1';assert t.count(marker)==1
t=t.replace(marker,(B/'CENTRAL_INSERT.md').read_text()+'\n\n'+marker,1)
needle='follows from the remaining open join.';assert t.count(needle)==1
t=t.replace(needle,needle+''' OAA1 below now supplies a
declared affine-distance attachment to this limit, while preserving the open
native physical identification and distinguishing the actual radar domain.''',1)
needle='observer-normalized null-path length, not automatically radar/spatial distance.';assert t.count(needle)==1
t=t.replace(needle,needle+''' OAA1 in R8OAA
uses a different quantity: one endpoint frequency times the full affine interval.
It is not this auxiliary-field integral or an adopted universal distance.''',1)
needle='and finite-patch identification are separate conditional readout requirements.';assert t.count(needle)==1
t=t.replace(needle,needle+''' OAA1 in R8OAA
now gives a finite receiver-normalized affine endpoint in the conditional CGE1
family. Its affine parameter is not a Jacobi/area distance by declaration;
the actual two-dimensional map remains the next proposed geometric interface.''',1)
needle='nor establishes that additional physics must be adopted.'
# Leave unrelated negative-result language untouched; new scale pointer goes in R16.
needle='Neither a finite diameter, a coordinate boundary nor a norm bound supplies it.';assert t.count(needle)==1
t=t.replace(needle,needle+''' OAA1 in R8OAA
adds a declared affine endpoint1/H on the conditional CPR1 histories and its
proper-orbital tolerance bound. It does not select H, identify a global X_max
or make that endpoint a universal affine ceiling; an explicit conditional
counterexample rules out that last stronger interpretation.''',1)
a=t.index('The next substantive question is operational attachment:');z=t.index("NGD1's numerical return",a)
t=t[:a]+'''OAA1 now supplies the missing mathematical attachment to one declared
geometric distance: the receiver-normalized affine interval D_o tends to1/H.
The actual b_*=0 source/receiver preparation has a late simple pole in1/H-D_o,
derived from the same metric rather than an independently supplied redshift
profile. Emitter-normalized affine distance diverges on that same ray. This
advances the conditional construction, without selecting a UDT physical
distance, metric law or independently measured astronomical separation.

The result also restricts its own interpretation. An independently discovered
regular preparation approaches1/H from above, with an exact rational sign
certificate; therefore it is not a universal affine maximum over this conditional
family. Source return is unavailable from the late receiver events beyond the
outer horizon. Conditional earlier circular-source echoes obey a divergent
radar lower bound as that horizon is approached. These distinctions prevent a
finite affine endpoint from silently becoming radar distance or X_max. None
proves whole-postulate insufficiency or a required new premise.

The next proposed bounded scientific step is the actual two-dimensional
source-screen/Jacobi map for the same metric and declared branch. Determine how
the affine endpoint and clock pole appear in geometric source-size/angle records,
retaining caustics, screen identification and existing reciprocity. Do not assume
affine equals D_A, add a flux/matter law, fit data or reopen paused source programs.
Physical selection of this comparison and native response admission remain
separate gates; identical geometry and physically matched GR queries still
produce identical records. The [fixed OAA1 return and proposed scope](udt_operational_asymptote_attachment_2026-10-04/DECISION_BRIEF.md)
state the reviewed result, resource/review bounds and next decision. Stop for
lay discussion; no automatic successor, larger solve or protected-work restart.

'''+t[z:]
marker='The preserved first candidates expose the repair history.';assert t.count(marker)==1
t=t.replace(marker,'''OAA1's two fresh source-first/exposed/final contexts independently reconstruct
the affine limit and causal/radar distinction, replay actual saved incidences,
and check the exact ceiling counterexample. Its [work record](udt_operational_asymptote_attachment_2026-10-04/WORK_RECORD.md)
states shared-model/library exposure, the preserved early-branch failure,
reviewer resource-enforcement repair and narrowed eventual-tail wording. The
[descendant review](udt_operational_asymptote_attachment_2026-10-04/DESCENDANT_REVIEW.md)
updates distance, scale, optical and adverse uses together. Exact rational proof,
finite arithmetic, independent review and version checks remain distinct; no
native, empirical, full-corpus or universal-distance claim is inferred.

'''+marker,1)
p.write_text(t);Path('CURRENT_RESEARCH_PROGRAM.md').write_text(guard.program_text(t))
common='''CDR1 remains the central-development architecture. UDT_DEVELOPMENT.md is the
sole maintained scientific argument; CURRENT_SCIENTIFIC_PREMISES.tsv and reviewed
sources own exact grades. CURRENT_RESEARCH_PROGRAM.md is its generated bounded
orientation. After orientation read R8OAA/R18, with R8/SGE1,R13/R16 as needed.

After CPR1 at11cca783, Charles authorized the operational-separation attachment
test. OAA1 evidence is in udt_operational_asymptote_attachment_2026-10-04/;
WORK_ORDER owns scope/stops. Two actual fresh source-first/exposed/final contexts
review the argument and saved quantities, with exact and finite checks. Initial
candidate, early-branch failure, reviewer resource repair and scope clarification
are preserved. Actual final attestations, normal/maintenance/full406 receipts and
committed/remote byte checks own closure. Verify actual HEAD, remote and dirt.

Next: Stop for lay discussion of OAA1. R18 and DECISION_BRIEF distinguish the
reviewed conditional affine attachment from native/empirical admission and
propose the bounded angular/Jacobi-map step for subsequent authorization.
No new physical distance postulate, response law, registry grade or X_max is
adopted. No GPU/long production or parked/protected program restarted. Standing
pauses, preservation, no-timeout/manual-stop and resource rules persist.

'''
for name,title,tail in [('LIVE.md','## CURRENT STATE — OAA1 affine attachment return, 2026-10-04','### Honest claim'),('HANDOFF.md','## Current handoff — OAA1 affine attachment return, 2026-10-04','Protected payloads require explicit dispatch; preserve without inspecting/hashing:')]:
 p=Path(name);s=p.read_text();a=s.index('## CURRENT STATE') if name=='LIVE.md' else s.index('## Current handoff');z=s.index(tail);s=s[:a]+title+'\n\n'+common+s[z:]
 if name=='LIVE.md':
  a=s.index('Use central R8CPR/R18');z=s.index('\n<!-- STARTUP_CURRENT_END -->',a)
  s=s[:a]+'''Use central R8OAA/R18 and OAA1's decision brief for the conditional affine
attachment, its counterexample and proposed optical-interface step. Native
response/distance selection and actual source/map/data remain open. Verify final
review/check/banking evidence. Existing pauses/protected boundaries persist;
TPS1 raw fields/large streams remain local-only, not remotely replayable.
'''+s[z:]
 p.write_text(s)
p=W/'DEVELOPMENT_GRAPH.json';g=json.loads(p.read_text())
sources=[str(B/x) for x in ['WORK_ORDER.md','INITIAL_CANDIDATE.md','CLARIFICATIONS.md','PREMISE_LEDGER.tsv','CONSTRUCTION_RESULT.json','check_attachment.py','CANDIDATE_FREEZE.json','AFFINE_CEILING_COUNTEREXAMPLE.md','CEILING_EXACT_RESULT.json','check_ceiling_exact.py','CEILING_CHECK_FREEZE.json','RADAR_BOUND.md','METHOD_REFERENCES.md']]
g['nodes'].extend([
dict(id='C_OAA_AFFINE',kind='conditional_protocol',statement='Chosen actual CPR1 ray and endpoint proper clocks; D_i=omega_i times affine interval. Coordinate/affine-gauge invariant but observer-dependent geometric readout, not adopted distance or radar/area equality.',sources=sources,registry_ids=[]),
dict(id='C_OAA_BRANCH',kind='conditional_protocol',statement='Inherited conditional positive-H CPR1 escaping regular branch. General finite receiver-affine limit; eventual below-limit pole only for stated b_star0 preparation. Radar lower bound conditional on echo existence; static radial control a different query.',sources=sources,registry_ids=[]),
dict(id='O_OAA_PHYSICAL',kind='open_join',statement='Native physical separation/response admission, independently observed distance and full source-screen/Jacobi map remain open. Finite affine endpoint not universal ceiling/X_max or extra matched-GR prediction.',sources=sources[:4],registry_ids=[]),
dict(id='R8OAA',kind='argument',anchor='r8oaa',title='Conditional receiver-affine distance pole and causal/radar attachment limits',sources=sources,registry_ids=[],required_conditions=['C_OAA_AFFINE','C_OAA_BRANCH'])])
for x in ['R6','R8CPR']:g['edges'].append({'from':x,'to':'R8OAA','kind':'proof'})
for x in ['C_OAA_AFFINE','C_OAA_BRANCH']:g['edges'].append({'from':x,'to':'R8OAA','kind':'hypothesis'})
targets=['D1','R2','R6','R7','R8','R8CGE','R8CPR','R8ACP','R8PRT','R9','R10','R13','R14','R15','R16','R17','R18','R8OAA','C_OAA_AFFINE','C_OAA_BRANCH','O_OAA_PHYSICAL']
for x in targets[:17]:
 if x not in ['R6','R8CPR','R18']:g['edges'].append({'from':x,'to':'R8OAA','kind':'context'})
g['edges'].extend([{'from':'O_OAA_PHYSICAL','to':'R8OAA','kind':'open_boundary'},{'from':'R8OAA','to':'R18','kind':'context'}])
for x in sources:g['sources_sha256'][x]=h(x)
for x in ['WORK_RECORD.md','DESCENDANT_REVIEW.md','review_math/SOURCE_FIRST.md','review_math/EXPOSED_REVIEW.md','review_fidelity/SOURCE_FIRST.md','review_fidelity/EXPOSED_REVIEW.md','review_fidelity/EXPOSED_ADDENDUM.md','review_fidelity/RADAR_EXTENSION_REVIEW.md']:
 x=str(B/x);g['review_support'].append({'path':x,'sha256':h(x),'role':'review_evidence','targets':targets})
p.write_text(json.dumps(g,indent=2)+'\n')
row=['OAA1_RETURN',str(B/'INITIAL_CANDIDATE.md'),'VERIFIED-WITH-CAVEATS_CONDITIONAL_AFFINE_ATTACHMENT; native distance/metric and observation OPEN; no universal ceiling',';'.join(targets),'SOURCE_FIRST_EXPOSED_FINAL_REVIEW; exact and finite same-geometry checks, independent saved replays, exact ceiling counterexample, scoped tail clarification',h(B/'INITIAL_CANDIDATE.md')]
with (W/'RECENT_DISPOSITIONS.tsv').open('a',newline='') as stream:csv.writer(stream,delimiter='\t',lineterminator='\n').writerow(row)
print(json.dumps({'nodes':len(g['nodes']),'edges':len(g['edges']),'source_pins':len(g['sources_sha256']),'orientation_words':len(guard.orientation(t).split())}))
