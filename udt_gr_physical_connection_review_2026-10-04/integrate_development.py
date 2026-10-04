"""One-time GRL1 integration; no original source or grade is rewritten."""
from pathlib import Path
import csv,hashlib,json,sys
sys.path.insert(0,str(Path.cwd()))
import verify_udt_development as guard
B=Path('udt_gr_physical_connection_review_2026-10-04')
W=Path('development_reconstruction_2026-09-29')
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
p=Path('UDT_DEVELOPMENT.md');t=p.read_text()
assert '<a id="r8grl"></a>' not in t
old='**Current development — ACI1 finite-curvature implication attempt reviewed,'
assert t.count(old)==1
t=t.replace(old,'**Current development — GRL1 bounded GR connection review completed,',1)
a=t.index('**Current learning.**');z=t.index('<!-- DEVELOPMENT_ORIENTATION_END -->',a)
t=t[:a]+'''**Current learning.** GRL1 examined ten primary papers in three separate
research contexts, followed by two fresh adversarial reviewers. Two conditional
geometric tests survive. The requested native physical connection remains OPEN.

Exact agreement of light cones and sufficiently rich free-fall paths fixes the
metric up to a constant scale; matched received-clock ratios then agree. One
common free congruence is insufficient. This is a guard against appending a
clock effect to otherwise identical complete geometric data, not a requirement
of exact global GR agreement or a bound on permitted physical deviations.

A local joint-drift identity separates curvature from changing line of sight
and the source congruence's shear/vorticity. A supplied flat free-clock control
has positive raw redshift drift but zero corrected curvature diagnostic. The
result is a limiting measurement relation with explicit smoothness, geodesic,
null-branch and sphere-average conditions, not a finite observational estimator.

Operational GR foundations largely recover structure already in the metric
interface. Curvature reconstruction does not identify DDR's response; received
tick rates still require actual arrival maps, and geometric areas do not supply
physical luminosity or energy-flux laws. An external quadrupole inconsistency
was quarantined; the retained scalar drift relation was independently rederived.

No inspected commitment fixes this drift diagnostic, its physical source family
or the missing positional assignment. Temporal drift and the far-separation
asymptote are different questions. ACI1's conditional finite curvature bound
and prior completion tools survive. No response, sign, field equation, scale,
population or X_max realization is selected. This finite review does not prove
whole-postulate insufficiency or necessity for a new premise.

After orientation read R8GRL and R18, with R8ACI/R16CPA as needed. The initial
candidate and one bounded precision repair are preserved; actual separate-context
reviews checked the arguments and exact controls by hand. Shared model/source
exposure remains, with no human, different-model, formal or empirical review.
No scientific CPU or GPU run was needed. Final attestations and required checks
own closure. Stop for discussion of a justified physical comparison requirement
or independent observational restriction; no successor or adoption starts
automatically. The founding positional interpretation remains the premise.
'''+t[z:]
marker='#### Finite mutual ticking and its causal limits — FPC1'
assert t.count(marker)==1
t=t.replace(marker,(B/'CENTRAL_INSERT.md').read_text()+'\n\n'+marker,1)
old='''normalization failures and their bounded repair are preserved. Stop for the
direction discussion in R18; no model adoption or successor follows automatically.'''
new='''normalization failures and their bounded repair are preserved. The later
authorized GRL1 review in R8GRL tests related literature connections without
supplying this physical assignment. R18 owns the current discussion return.'''
assert t.count(old)==1;t=t.replace(old,new,1)
a=t.index("[ACI1's decision brief]");z=t.index("\n\nNGD1's numerical return",a)
t=t[:a]+'''The [fixed ACI1 return](udt_asymptotic_curvature_implication_2026-10-04/DECISION_BRIEF.md)
retains that finite necessary test without native admission. Charles then
authorized GRL1's bounded GR literature review, now developed in R8GRL. Its
rich-operational-agreement theorem and corrected local drift diagnostic add
useful conditional tests. Neither supplies the extra positional requirement's
physical comparison assignment. Exact complete agreement with a reference
metric is stronger than GR FILTER ONLY; temporal drift is not the asymptotic
separation requirement. The supplied flat control blocks a raw-drift curvature
sign inference while preserving the corrected geometric identity.

[GRL1's decision brief](udt_gr_physical_connection_review_2026-10-04/DECISION_BRIEF.md)
owns the current lay return. A next proposal needs a justified physical
requirement for an actual comparison, or independently defined observations
that constrain the geometry under disclosed assumptions. This review selects
neither route. Another inverse-measurement identity alone cannot supply the
physical restriction. No whole-postulate insufficiency, new-premise necessity,
native field equation or X_max realization is proved. Stop for discussion;
no further literature/model/data campaign or physical adoption begins
automatically. Prior fixed decisions and mathematical tools retain their scope.
'''+t[z:]
marker='The preserved first candidates expose the repair history.'
addition='''GRL1 uses three separate research contexts and two additional fresh
source-first/exposed/final reviewers. Ten substantive primary papers were
inspected; one mistaken paper identifier reached unrelated title metadata only
and was discarded. Exact versions, inspected sections and access omissions are
recorded in each source ledger. Old source/verdict exposure is disclosed.
The parent froze its synthesis after all three research reports and before
reading either new reviewer's substantive source-first findings; earlier hand
exploration was not blind preregistration. No independence from the research
reports is claimed. Both reviewers reconstructed the conditional arguments and
original-incidence controls by hand. One bounded repair resolves excessive
all-direction necessity wording and emission-versus-Fermi labels, and records
the scaled-incidence C1 justification and independent Riccati argument with
attribution. Initial candidate and all earlier seals remain fixed. The
external quadrupole channel is unused. No scientific program, GPU campaign,
human, different-model, empirical, formal or full-corpus review occurred.
[Work record](udt_gr_physical_connection_review_2026-10-04/WORK_RECORD.md) and
[descendant review](udt_gr_physical_connection_review_2026-10-04/DESCENDANT_REVIEW.md)
retain the scope, omissions and both positive/negative interpretation checks.
Actual final attestations and normal/maintenance/full406 receipts own closure;
review and banking do not adopt the open physical join.

'''
assert t.count(marker)==1;t=t.replace(marker,addition+marker,1)
p.write_text(t);Path('CURRENT_RESEARCH_PROGRAM.md').write_text(guard.program_text(t))

common='''CDR1 remains the central-development architecture. UDT_DEVELOPMENT.md is the
sole maintained scientific argument; CURRENT_SCIENTIFIC_PREMISES.tsv and reviewed
sources own exact grades. The generated CURRENT_RESEARCH_PROGRAM.md is the bounded
startup orientation. Read R8GRL and R18 after orientation; R8ACI/R16CPA as needed.

After ACI1 at865a1163, Charles authorized the bounded GR literature connection
review. GRL1 evidence is in udt_gr_physical_connection_review_2026-10-04/;
WORK_ORDER owns scope. Three research and two fresh source-first/exposed/final
reviewer contexts, ten substantive papers, two analytic tests and one precision
repair are recorded. Initial candidates, seals and actual exposure stay fixed.
Final attestations and normal/maintenance/full406 receipts own closure;
commit/push and byte checks own banking. Verify actual HEAD, remote, dirt and
processes rather than assuming this text identifies the tip.

Next: Stop for lay discussion of GRL1's return and the physical assignment.
No native selector or specific successor was found. The retained conditional
tests do not choose a physical observer family, response or field equation.
No physical adoption, registry promotion, further model/literature/data campaign
or GPU/hardware work begins automatically. No scientific CPU or GPU program
ran in this review. Standing pauses, no-timeout/resource/manual-stop rules and
protection of unrelated work persist.

'''
for name,title,tail in [('LIVE.md','## CURRENT STATE — GRL1 bounded GR review return, 2026-10-04','### Honest claim'),('HANDOFF.md','## Current handoff — GRL1 bounded GR review return, 2026-10-04','Protected payloads require explicit dispatch; preserve without inspecting/hashing:')]:
    p=Path(name);q=p.read_text();a=q.index('## CURRENT STATE') if name=='LIVE.md' else q.index('## Current handoff');z=q.index(tail)
    q=q[:a]+title+'\n\n'+common+q[z:]
    if name=='LIVE.md':
        a=q.index('Stop for lay discussion using central');z=q.index('\n<!-- STARTUP_CURRENT_END -->',a)
        q=q[:a]+'''Stop for lay discussion using central R8GRL/R18 and GRL1's decision brief.
The native physical assignment remains open; conditional rigidity and drift
tests are retained with ACI1 and the prior completion tools. No automatic
successor or physical adoption. Verify final bindings/checks and synchronization.
Existing pauses/protected boundaries persist. TPS1 raw fields/large streams
remain local-only; compact remote records cannot replay raw-dependent checks.
'''+q[z:]
    p.write_text(q)

p=W/'DEVELOPMENT_GRAPH.json';g=json.loads(p.read_text())
assert all(n['id']!='R8GRL' for n in g['nodes'])
sources=[str(B/s) for s in ['INITIAL_SYNTHESIS.md','REPAIR.md','REVIEWED_RESULT.md','WORK_ORDER.md']]
g['nodes'].append(dict(id='C_GRL_RIGIDITY',kind='conditional_protocol',statement='T1 only: identified connected smooth Lorentz4 metrics, matching time/sign convention and null cones, with all unparameterized timelike geodesics matching; two nonparallel common timelike tangents per point already suffice after cone matching. Identical endpoint curves/events and regular null correspondence for equal ratios. Not a physical GR-matching postulate.',sources=sources,registry_ids=[]))
g['nodes'].append(dict(id='C_GRL_DRIFT',kind='conditional_protocol',statement='T2 only: smooth unit geodesic source/observer congruence, parallel Fermi frame, common normal tube and regular short null branch; fixed source during reception derivative; local Fermi separation limit and exact uniform sphere average. No finite-distance estimator; redshift-coordinate division only where n.Bn is nonzero.',sources=sources,registry_ids=[]))
g['nodes'].append(dict(id='O_GRL_ASSIGNMENT',kind='open_join',statement='No inspected physical commitment supplies exact reference matching, a required corrected drift value/sign or its physical source congruence. Conditional geometric tests do not select native geometry, DDR response or positional attribution. No whole-postulate insufficiency or necessity for a new premise is proved.',sources=sources,registry_ids=[]))
g['nodes'].append(dict(id='R8GRL',kind='argument',anchor='r8grl',title='Conditional operational rigidity and local corrected drift; physical assignment remains open',sources=sources,registry_ids=[],required_conditions=['C_GRL_RIGIDITY','C_GRL_DRIFT']))
for frm in ['C_GRL_RIGIDITY','C_GRL_DRIFT']:g['edges'].append({'from':frm,'to':'R8GRL','kind':'hypothesis'})
for frm in ['R6','R7']:g['edges'].append({'from':frm,'to':'R8GRL','kind':'proof'})
for frm in ['D1','R8','R8ACI','R9','R13','R14','R16CPA']:g['edges'].append({'from':frm,'to':'R8GRL','kind':'context'})
g['edges'].append({'from':'O_GRL_ASSIGNMENT','to':'R8GRL','kind':'open_boundary'})
g['edges'].append({'from':'R8GRL','to':'R18','kind':'context'})
for source in sources:g['sources_sha256'][source]=sha(source)
targets=['D1','R6','R7','R8','R8ACI','R9','R13','R14','R16CPA','R8GRL','R18','C_GRL_RIGIDITY','C_GRL_DRIFT','O_GRL_ASSIGNMENT']
support=['DESCENDANT_REVIEW.md']
for lane in ['foundations','clocks','observables']:support.extend(['research_'+lane+'/REPORT.md','research_'+lane+'/SOURCES.json'])
for lane in ['math','fidelity']:support.extend(['review_'+lane+'/EXPOSED_REVIEW.md','review_'+lane+'/REPAIR_REVIEW.md'])
for source in support:
    source=str(B/source);g['review_support'].append(dict(path=source,sha256=sha(source),role='review_evidence',targets=targets))
p.write_text(json.dumps(g,indent=2)+'\n')
row=['GRL1_RETURN',str(B/'REVIEWED_RESULT.md'),'VERIFIED-WITH-CAVEATS_CONDITIONAL_GEOMETRIC_TESTS; native physical assignment OPEN; no adopted premise or registry regrade',';'.join(targets[:11]),'THREE_RESEARCH_AND_TWO_FRESH_REVIEW_CONTEXTS; ten primary papers; two hand-derived conditional tests; one precision repair; no scientific program or native selector',sha(B/'REVIEWED_RESULT.md')]
with (W/'RECENT_DISPOSITIONS.tsv').open('a',newline='') as f:csv.writer(f,delimiter='\t',lineterminator='\n').writerow(row)
print(json.dumps(dict(nodes=len(g['nodes']),edges=len(g['edges']),source_pins=len(g['sources_sha256']),review_support=len(g['review_support']),orientation_words=len(guard.orientation(t).split()))))
