"""One-time explicit central integration; no source acceptance or grade updates."""
from pathlib import Path
import csv, hashlib, json, sys
sys.path.insert(0,str(Path.cwd()))
import verify_udt_development as guard

B=Path('udt_prepared_distance_attachment_2026-10-04')
W=Path('development_reconstruction_2026-09-29')
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
master=Path('UDT_DEVELOPMENT.md')
t=master.read_text()
assert '<a id="r16pda"></a>' not in t
t=t.replace('**Current development — CCW1 completion-connection whiteboard reviewed,',
            '**Current development — PDA1 prepared-distance attachment reviewed,',1)
begin=t.index('**Current learning.**')
end=t.index('<!-- DEVELOPMENT_ORIENTATION_END -->')
t=t[:begin]+'''**Current learning.** FCL1 derives the free-clock limit in supplied UNADOPTED
regular conformal completion RG; CCW1 links it to invariant source-clock gaps
and limiting curvature. PDA1 (R16PDA) now derives a distance attachment: for one
fixed emitted ray through a specified bounded free-clock population, a regular
endpoint map and nonzero distance slope yield Z proportional asymptotically to
1/(L_*-L). L is actual initial surface distance, not a renamed geometry variable.

The uniform common collar, label-derivative limit and attachment slope are
explicit conditions, checked in exact examples. A smooth bounded noncrossing
preparation can instead give Z proportional to1/sqrt(L_*-L). Thus bounded
initial motion alone does not fix the distance exponent. Both examples retain
divergent received slowing; neither selects a physical observer population.
CCW's Z=1 population instead has unbounded initial boosts and fails this gate.
An immediate echo in the supplied controls ceases before the one-way limit.

The result is local to that ray/preparation, not a universal distance-only law.
Generic endpoint regularity, prescribed remote/global rays, physical RG
admission, native event/path assignment, additional-effect attribution, scale
and X_max remain open. No whole-postulate insufficiency or need for a new premise
is proved. CPW1's scalar echo sufficiency FC stays parked as a physical selector.
FCL/CCW's earlier invariant and adverse results retain their stated scopes.

After orientation read R16PDA/R16CCW/R16FCL and R18. Two fresh source-first,
exposed and final reviewer contexts and45 exact parent controls support this
conditional return. LIVE/HANDOFF own closure and the discussion stop. The next
discussion should address native geometry admission; no successor or physical
adoption starts automatically. Keeping the conditional result remains an option.
'''+t[end:]
old='''this second bounded test if the RG route is continued; it is unexecuted and
does not adopt a physical population or geometry. Local emitter construction'''
new='''this second bounded test if the RG route is continued; PDA1 below now answers
its fixed-ray prepared-distance scope without adopting a population or geometry. Local emitter construction'''
assert t.count(old)==1;t=t.replace(old,new)
t=t.replace('retain the exact arguments, limits and unexecuted next test.',
            'retain the exact arguments, limits and then-unexecuted next proposal; PDA1 records its scoped return.',1)
marker='<a id="r17"></a>'
assert t.count(marker)==1;t=t.replace(marker,(B/'CENTRAL_INSERT.md').read_text()+'\n'+marker,1)
old='''Physical RG admission and native event/path assignment remain open. The
invariant clock/curvature test is necessary for this candidate completion and
does not select it or establish an additional UDT contribution. Uniform
preparations, fixed-emission incidence, actual distance attachment, global rays,
scale and X_max still require their own arguments. No new physical premise is
adopted and no complete-postulate insufficiency theorem is obtained.

The parent recommends the bounded prepared-distance test described in
[CCW1's successor proposal](udt_completion_connection_whiteboard_2026-10-03/NEXT_TEST_PROPOSAL.md)
if the RG route is continued. It would evaluate a specified experiment in the
supplied geometry, not derive its native admission. This is an unexecuted
recommendation, not a contributor consensus to adopt RG. The no-change option
retains the conditional mathematics. [CCW1's decision brief](udt_completion_connection_whiteboard_2026-10-03/DECISION_BRIEF.md)
owns the lay return; the FCL/CPW/FCW fixed decisions remain historical evidence.
Stop for lay discussion; no successor or physical adoption starts automatically.'''
new='''PDA1 now completes the authorized prepared-distance test in R16PDA. Uniform
free-clock control, a supplied regular invertible endpoint map and nonzero
distance transversality derive an actual simple pole for one fixed emitted
ray through that prepared population. The operational initial surface distance
is computed on the receiving labels. Exact controls verify a positive moving
family and a bounded, noncrossing family whose distance slope vanishes and whose
asymptote is a square-root pole. Bounded motion alone therefore does not supply
the positive theorem's transversality. This does not refute a specified radial
parallel preparation, ordinary local clocks or the founding asymptotic aim.

Physical RG admission and native event/path assignment remain open. Generic
H2/common-collar admission, global prescribed sources/populations and a universal
distance-only law are not established. The invariant clock/curvature and local
distance results evaluate the supplied geometry; they do not select it, isolate
the additional UDT contribution, set a scale or identify X_max. No new physical
premise or complete-postulate insufficiency theorem is adopted.

[PDA1's decision brief](udt_prepared_distance_attachment_2026-10-04/DECISION_BRIEF.md)
owns the current lay return. The proposed next discussion is about whether an
existing UDT commitment actually admits this geometry, with a bounded source-led
audit as a possible later work order. That audit is unexecuted and is not an
automatic successor. Retaining the conditional result remains an option;
CCW/FCL/CPW/FCW fixed decisions keep their historical scopes. Stop for discussion;
no physical adoption or new campaign starts automatically.'''
assert t.count(old)==1;t=t.replace(old,new)
marker='The preserved first candidates expose the repair history.'
review='''PDA1 uses two new fresh source-first/exposed/final reviewer contexts. Their
source-first wavefront/path derivations preceded exposure to the parent fixed-ray
candidate; the parent froze its own candidate before reading their arguments.
Exposed reviews checked the distinct quantifiers, explicit H1/H2/H3 conditions,
uniform estimate, actual incidence, gauge residue, bounded noncrossing degeneracy
and echo domain. Both independently recomputed load-bearing geodesic/implicit-jet
quantities by hand. Parent exact controls passed45 checks in five families; no
scientific repair or reviewer scientific program was needed. Shared inherited
model/premises and SymPy remain limits; no different-model/human/formal/empirical
verification. Reviewer alternative generic regularity and wavefront arguments
remain review leads, not extra integrated theorems. [Work record](udt_prepared_distance_attachment_2026-10-04/WORK_RECORD.md)
and [descendant review](udt_prepared_distance_attachment_2026-10-04/DESCENDANT_REVIEW.md)
preserve exposure, the metadata lookup failure, checks and omissions. Actual
final accepted-map attestations and normal/maintenance/full406 receipts own
integration/banking closure; neither review nor commit adopts RG.

'''
assert t.count(marker)==1;t=t.replace(marker,review+marker,1)
master.write_text(t)
Path('CURRENT_RESEARCH_PROGRAM.md').write_text(guard.program_text(t))

common='''CDR1 remains the central-development architecture. UDT_DEVELOPMENT.md is the
sole maintained scientific argument; CURRENT_SCIENTIFIC_PREMISES.tsv and reviewed
sources own exact grades. The generated CURRENT_RESEARCH_PROGRAM.md is the bounded
startup orientation. Read R16PDA/R16CCW/R16FCL/R18 after orientation.

Charles authorized the prepared-distance test after the completed CCW1 return
at976f860d. PDA1 evidence is in udt_prepared_distance_attachment_2026-10-04/;
its WORK_ORDER owns scope. The unchanged initial candidate, frozen exact
controls and two fresh source-first/exposed/final reviews are preserved.
Final attestations and actual normal/maintenance/full406 receipts own closure;
commit/push and byte checks own banking. Verify actual HEAD, remote, dirt and
processes rather than assuming this text identifies the tip.

Next: Stop for lay discussion of the PDA1 decision brief. A possible source-led
native-admission audit is an unexecuted discussion recommendation, not an
authorized successor. No RG/FC adoption, native field/source/action law, registry
promotion, GPU/data/hardware campaign starts automatically. One short CPU exact
control program ran; no long solver. The no-timeout direction persists with
finite scope/resource/manual stops. Preserve protected and unrelated work.

'''
for name,title,tail in [('LIVE.md','## CURRENT STATE — PDA1 prepared-distance return, 2026-10-04','### Honest claim'),('HANDOFF.md','## Current handoff — PDA1 prepared-distance return, 2026-10-04','Protected payloads require explicit dispatch; preserve without inspecting/hashing:')]:
    p=Path(name);q=p.read_text();b=q.index('## CURRENT STATE') if name=='LIVE.md' else q.index('## Current handoff')
    e=q.index(tail);q=q[:b]+title+'\n\n'+common+q[e:]
    if name=='LIVE.md':
        b=q.index('Stop for lay discussion using central');e=q.index('\n<!-- STARTUP_CURRENT_END -->',b)
        q=q[:b]+'''Stop for lay discussion using central R16PDA/R16CCW/R16FCL/R18 and the PDA1
decision brief. The conditional prepared-distance test is complete; native
admission and physical attribution remain open. No successor starts automatically.
Verify actual evidence, final bindings and synchronization. Existing pauses and
protected boundaries persist. TPS1 raw fields/large streams remain local-only;
compact remote records cannot replay raw-dependent checks.
'''+q[e:]
    p.write_text(q)

path=W/'DEVELOPMENT_GRAPH.json';g=json.loads(path.read_text())
sources=[str(B/p) for p in ['INITIAL_CANDIDATE.md','REVIEWED_RESULT.md','WORK_ORDER.md']]
conditions={
 'C_PDA_RG_RAY':'UNADOPTED supplied C3 Lorentz4 RG g=x^-2 b, nonzero timelike dx and normal collar; one fixed interior emission and regular fixed null ray with nonzero limiting conformal affine tangent, whole-ray omega_e1; local actual emitter variations at each reception. No native geometry or global source-access claim.',
 'C_PDA_PREPARATION':'H1 supplied smooth bounded free receivers prepared on an interior spacelike surface, initial metric proper distance from specified origin away from cut locus; common actual compact collar/transit/coefficient/entry bounds. Query choices, not a physical population; compactness alone is insufficient.',
 'C_PDA_ENDPOINT':'H2 supplied C1 interior label flow with uniform first-label-derivative convergence to continuous J, F(a*)=ray endpoint and detJ(a*) nonzero. F existence/continuity follows H1. Not derived generically from FCL or bare C3; explicit exact controls check it.',
 'C_PDA_TRANSVERSE':'H3 for the positive simple-pole theorem: d=D L J^-1 z_prime(0)<0, c=-d>0. Above-endpoint orientation analogous; d0 is independently analyzed. The bounded square-root witness satisfies H1/H2 and fails this condition; no iff criterion.'}
for nid,statement in conditions.items():g['nodes'].append(dict(id=nid,kind='conditional_protocol',statement=statement,sources=sources,registry_ids=[]))
g['nodes'].append(dict(id='R16PDA',kind='argument',anchor='r16pda',title='Conditional fixed-ray prepared-distance pole and bounded noncrossing attachment degeneracy',sources=sources,registry_ids=[],required_conditions=['P_NULL',*conditions]))
for n in g['nodes']:
    if n['id']=='O_CPW_FREECLOCK_LIMIT':
        n['statement']='FCL1 pointwise limit and CCW1 clock-curvature/local-source results survive. PDA1 conditionally closes fixed-ray prepared-distance attachment under explicit uniform collar, endpoint derivative/nonsingularity and distance-transversality conditions. Generic admission of those preparation conditions, prescribed remote/global populations and distance-only universality remain OPEN. Unbounded-boost and bounded-degenerate controls keep distinct scopes. Open join is not a proof input.'
        n['sources'].append(str(B/'REVIEWED_RESULT.md'))
    if n['id']=='O_FCW_ADMISSION':
        n['statement']='Physical RG admission, native geometry and additional-effect attribution remain OPEN. CCW1 invariant/local-source and PDA1 prepared-distance results evaluate supplied conditions, not select the geometry. CPW1 physical FC remains parked. No native scale/X_max or whole-postulate insufficiency theorem.'
        n['sources'].append(str(B/'REVIEWED_RESULT.md'))
for frm in ['P_NULL',*conditions]:g['edges'].append(dict(from_=frm,to='R16PDA',kind='hypothesis'))
for frm,kind in [('R6','proof'),('R16FCL','proof'),('R16CCW','context'),('R16CPW','context'),('R8','context'),('O_FCW_ADMISSION','open_boundary'),('O_CPW_FREECLOCK_LIMIT','open_boundary')]:g['edges'].append(dict(from_=frm,to='R16PDA',kind=kind))
g['edges'].append(dict(from_='R16PDA',to='R18',kind='context'))
for edge in g['edges']:
    if 'from_' in edge:edge['from']=edge.pop('from_')
for p in sources:g['sources_sha256'][p]=sha(p)
targets=['D1','R6','R8','R16','R16FCW','R16CPW','R16FCL','R16CCW','R16PDA','R18','O_CPW_FREECLOCK_LIMIT','O_FCW_ADMISSION',*conditions]
for p in ['review_math/EXPOSED_REVIEW.md','review_fidelity/EXPOSED_REVIEW.md','DESCENDANT_REVIEW.md','PARENT_CHECK_RESULT.md']:
    p=str(B/p);g['review_support'].append(dict(path=p,sha256=sha(p),role='review_evidence',targets=targets))
path.write_text(json.dumps(g,indent=2)+'\n')
row=['PDA1_RETURN',str(B/'REVIEWED_RESULT.md'),'VERIFIED-WITH-CAVEATS_CONDITIONAL_FIXED_RAY_ATTACHMENT; RG UNADOPTED; explicit H1/H2/H3; actual initial-distance pole and bounded noncrossing square-root degeneracy; no native admission',
     ';'.join(targets[:10]),'ANALYTIC_UNIFORM_ESTIMATE_AND_ACTUAL_INCIDENCE; five exact control families45checks; two fresh source-first/exposed/final contexts; no native geometry/attribution/scale or universal distance-only law',sha(B/'REVIEWED_RESULT.md')]
with (W/'RECENT_DISPOSITIONS.tsv').open('a',newline='') as f:csv.writer(f,delimiter='\t',lineterminator='\n').writerow(row)
print(json.dumps(dict(nodes=len(g['nodes']),edges=len(g['edges']),source_pins=len(g['sources_sha256']),review_support=len(g['review_support']),orientation_words=len(t[t.index('<!-- DEVELOPMENT_ORIENTATION_BEGIN -->'):t.index('<!-- DEVELOPMENT_ORIENTATION_END -->')].split()))))
