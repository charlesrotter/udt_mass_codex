from pathlib import Path
import json,hashlib,csv,io
import verify_udt_development as verify
B=Path('udt_positional_curvature_connection_2026-10-01');W=Path('development_reconstruction_2026-09-29')
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
(W.parent/'CURRENT_RESEARCH_PROGRAM.md').write_text(verify.program_text(Path('UDT_DEVELOPMENT.md').read_text()))
# Operational adapters: retain every paused/protected/archive paragraph verbatim.
p=Path('LIVE.md');s=p.read_text();a=s.index('## CURRENT STATE');z=s.index('### Honest claim',a)
s=s[:a]+'''## CURRENT STATE — PCC1 reviewed isotropic-addition trial after ECS1 and CDR1, 2026-10-01

Work on `grok`; independently verify HEAD, synchronization and dirt.
Charles's “test authorized” accepted the explicit bounded isotropic additional
clock-curvature test, two fresh reviews and one bounded repair/re-review cycle.
Fixed scope and execution are in `udt_positional_curvature_connection_2026-10-01/`:
WORK_ORDER.md, WORK_RECORD.md, REVIEWED_RESULT.md and DECISION_BRIEF.md.
UDT_DEVELOPMENT.md R8/R18 owns the maintained argument. The trial physical
hypothesis remains UNADOPTED; no response, reference, native geometry, scalar
scale/sign, exact registry grade or CANON change is adopted.

PCC1 used short serial exact checks and two source-first/candidate/supplement
reviews. Parent and math initial trig-normalization failures and unchanged-science
repairs are preserved, as is the fixed-file diagnostic replay resolving a review
objection. The initial scientific candidate is unchanged. No GPU or production
evolution ran. Prior packages remain fixed at their original scopes. Charles's
no-timeout direction persists with finite/resource/manual stops.

'''+s[z:]
a=s.index('### Next gate');z=s.index('<!-- STARTUP_CURRENT_END -->',a)
s=s[:a]+'''### Next gate

The authorized conditional test is complete. Stop for lay discussion using the
PCC1 decision brief, actual final attestations and captured checks. The tested
comparison still needs physical reference/matching and positional attribution;
no distinct UDT prediction, native admission or finite-distance law is established.
A successor needs its own discriminating question and bounded work order. The
trial is not adopted by testing or saving it. Existing pauses/protected work remain.
No scientific worker was left running at this return; a later session must verify
actual host state before process claims. Prior TPS1 raw fields/checkpoints and
large streams remain local-only and ignored; a remote clone cannot replay those
raw-dependent checks from compact banked records alone.

'''+s[z:];p.write_text(s)
p=Path('HANDOFF.md');s=p.read_text();a=s.index('## Current handoff');z=s.index('Protected payloads require explicit dispatch;',a)
s=s[:a]+'''## Current handoff — PCC1 reviewed conditional addition after ECS1 and CDR1, 2026-10-01

LIVE.md wins. Charles's “test authorized” accepted the proposed isotropic
additional clock-curvature test with two fresh reviews and a bounded repair cycle.
Fixed WORK_ORDER.md, WORK_RECORD.md, REVIEWED_RESULT.md and DECISION_BRIEF.md are
in `udt_positional_curvature_connection_2026-10-01/`. UDT_DEVELOPMENT.md R8/R18
owns the maintained science. Exact406 grades in CURRENT_SCIENTIFIC_PREMISES.tsv,
CANON and physical adoption remain unchanged; the tested hypothesis is UNADOPTED.

PCC1's pointwise implication, regional controls and nonuniform comparison retain
the supplied reference/matching and leading-clock limits. No native response,
source, scale/sign, finite-distance law or empirical filter pass is selected.
Both contexts independently reconstructed and checked before exposed candidate
and supplement reviews. Initial trig-normalization failures, code repairs and
diagnostic replay are preserved. No scientific-candidate repair was required.
Prior packages keep their scopes; no new GPU or production campaign ran.

Next: stop for discussion at this conditional trial return. No physical adoption,
new premise or successor computation begins automatically. Two actual final
attestations bind the integrated edition; captured normal,57-maintenance and
full406 checks own pass status. Later sessions must verify host state; no scientific
worker was left running at this return. Prior TPS1 raw fields and checkpoints
remain local-only. LIVE retains all pauses and archive caveats. No-timeout direction
persists with finite/resource/manual stops. Current version/review bindings are
in development_reconstruction_2026-09-29/.

'''+s[z:];p.write_text(s)
# Explicit conditional argument graph.
p=W/'DEVELOPMENT_GRAPH.json';g=json.loads(p.read_text());lookup={n['id']:n for n in g['nodes']}
sources=[str(B/n) for n in ['INITIAL_DERIVATION.md','SUPPLEMENT.md','REVIEWED_RESULT.md','math/SOURCE_FIRST_ARGUMENT.md','fidelity/SOURCE_FIRST.md','PRIMARY_REFERENCE.md']]
for path in sources:g['sources_sha256'][path]=h(path)
for name in ['R8','R18','O_PSW_ATTRIBUTION']:
 lookup[name]['sources'].append(str(B/'REVIEWED_RESULT.md'))
lookup['O_PSW_ATTRIBUTION']['statement']+=' PCC1 tests an UNADOPTED all-frame leading additional-curvature assignment with supplied reference/matching; conditional compatibility and scoped Einstein-reference consequence do not close native positional attribution or select a finite law.'
conds=[
 ('P_PCC_MATCH','conditional_protocol','Two supplied smooth time-oriented Lorentz4 metrics, matched events and time-oriented tangent isometry; PSW1 equal proper L, parallel-prepared free clocks, same units and regular direct null branches, fixed worldlines across nearby emissions. Reference and matching are not selected.'),
 ('C_PCC_ALLFRAME','conditional_class','UNADOPTED trial: the leading L^2 additional log-clock coefficient is one scalar for every future unit timelike U and every orthogonal unit n, with simultaneous matched frames. Applies to curvature DIFFERENCE, not total isotropy; does not identify DDR response.'),
 ('P_PCC_REGION','conditional_protocol','Smooth supplied event/frame matching across a region with the all-frame curvature-difference condition imposed there; use physical connection for derivatives. General Bianchi condition is necessary only, with full integrability still required.'),
 ('C_PCC_EINSTEIN_REFERENCE','conditional_class','Additional supplied reference assumption Ric[g0]=Lambda0 g0 with constant Lambda0 on the connected regular domain; explicitly conditional under GR FILTER ONLY, not adopted UDT dynamics.')]
for id,kind,statement in conds:g['nodes'].append({'id':id,'kind':kind,'statement':statement,'sources':[sources[0]],'registry_ids':[]})
args=[('R8PCC','r8pcc','All-frame additional leading clock-curvature equivalence',['P_PCC_MATCH','C_PCC_ALLFRAME','P_NULL','M_GEOMETRY']),('R8PCCR','r8pccr','Regional necessary compatibility and variable-reference witness',['P_PCC_MATCH','C_PCC_ALLFRAME','P_PCC_REGION','M_GEOMETRY']),('R8PCCE','r8pcce','Einstein-reference constancy and nonuniform compatibility witness',['P_PCC_MATCH','C_PCC_ALLFRAME','P_PCC_REGION','C_PCC_EINSTEIN_REFERENCE','M_GEOMETRY'])]
for id,anchor,title,conditions in args:
 g['nodes'].append({'id':id,'kind':'argument','anchor':anchor,'title':title,'sources':sources,'registry_ids':[],'required_conditions':conditions})
 for c in conditions:g['edges'].append({'from':c,'to':id,'kind':'hypothesis'})
for a,b,kind in [('R8','R8PCC','proof'),('R8PCC','R8PCCR','proof'),('R8PCCR','R8PCCE','proof'),('R5','R8PCC','context'),('R9','R8PCCE','context'),('R10','R8PCCE','context'),('R8PCC','R18','context'),('R8PCCR','R18','context'),('R8PCCE','R18','context')]:g['edges'].append({'from':a,'to':b,'kind':kind})
targets=['R5','R6','R8','R9','R10','R16','R17','R18','R8PCC','R8PCCR','R8PCCE']
for rel in ['math/CANDIDATE_REVIEW.md','math/SUPPLEMENT_REVIEW.md','fidelity/CANDIDATE_REVIEW.md','fidelity/SUPPLEMENT_REVIEW.md','IMPLEMENTATION_REPAIR.json','DIAGNOSTIC_REPLAY_REPAIR.json','DESCENDANT_REVIEW.md']:
 path=str(B/rel);g['review_support'].append({'path':path,'sha256':h(path),'role':'review_evidence','targets':targets})
p.write_text(json.dumps(g,indent=2)+'\n')
p=W/'RECENT_DISPOSITIONS.tsv';rows=list(csv.DictReader(p.open(),delimiter='\t'));assert len(rows)==43
row={'id':'PCC1_RETURN','source':str(B/'REVIEWED_RESULT.md'),'current_scope':'VERIFIED-WITH-CAVEATS_UNADOPTED_TRIAL; all-frame leading matched clock contrast fixes curvature difference, not total isotropy; regional necessary identity and variable-reference witness; Einstein-reference constancy and nonuniform Kottler comparison; no native admission/finite law','central_location':'R5;R8;R9;R10;R16;R17;R18;R8PCC;R8PCCR;R8PCCE','rederivation_depth':'SOURCE_FIRST_ALGEBRAIC_AND_ORIGINAL_CONNECTION;291 parent,1014 math,294 fidelity finite controls;792 Fraction and262/270 exposed saved checks; preserved trig failures, normalization repairs and replay fix; no scientific candidate repair or adoption','source_sha256':h(B/'REVIEWED_RESULT.md')}
with p.open('a',newline='') as f:csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n').writerow(row)
prior=W/'REVIEW_RECORD.json';(B/'PRIOR_REVIEW_RECORD.json').write_bytes(prior.read_bytes())
print(json.dumps({'graph_source_pins':len(g['sources_sha256']),'graph_nodes':len(g['nodes']),'later_returns':44,'prior_review_record_preserved_sha256':h(B/'PRIOR_REVIEW_RECORD.json')},indent=2))
