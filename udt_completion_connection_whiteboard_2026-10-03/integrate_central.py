"""CCW1 bounded integration; reviews and closure receipts are separate gates."""
from pathlib import Path
import csv,json,hashlib,sys
sys.path.insert(0,str(Path.cwd()))
import verify_udt_development as verify
B=Path('udt_completion_connection_whiteboard_2026-10-03')
W=Path('development_reconstruction_2026-09-29')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
p=Path('UDT_DEVELOPMENT.md');s=p.read_text();assert '<a id="r16ccw">' not in s
s=s.replace('**Current development — FCL1 conditional free-clock result reviewed,\n2026-10-03.**',
            '**Current development — CCW1 completion-connection whiteboard reviewed,\n2026-10-04.**',1)
a=s.index('**Current learning.**');z=s.index('<!-- DEVELOPMENT_ORIENTATION_END -->',a)
s=s[:a]+'''**Current learning.** FCL1 (R16FCL) derives the free-receiver limit in
supplied UNADOPTED regular conformal completion RG. CCW1 (R16CCW) links it to
invariant clock readings and curvature: if epsilon is the remaining source
proper-time interval to the limiting emission, epsilon Z tends to N_*>0 and
the receiver's limiting scalar curvature is12/N_*^2. Neither epsilon nor Omega
is spatial distance. This is a conditional relation, not a native geometry law.

With an explicit local C3 extension, a chosen nearby emitter and regular
signal family can be constructed. Prescribed distant sources/global rays remain
separate. A different-free-receiver population with unbounded initial boosts
can have Z=1 even as its reception events approach the boundary. The individual
FCL theorem survives; fixed-emission distance comparisons need preparation and
incidence control. The beta2 same-future-tail obstruction is strengthened by
its invariant zero-curvature limit; interior nonuniqueness remains.

No inspected argument supplies physical RG admission, native event/path
assignment, additional-effect attribution, scale or X_max. No whole-postulate
insufficiency or need for a new premise is proved. CPW1's scalar echo sufficiency
FC remains parked as a physical selector; its conditional diagnostics survive.
The next proposed test derives a fixed-emission distance attachment for a
specified bounded free-clock preparation in supplied RG. It is unexecuted and
would not select the native geometry. Retaining the conditional result without
adopting RG remains an option.

After orientation read R16CCW/R16FCL and R18. LIVE/HANDOFF own closure and the
lay decision. Three source-first contributors, a fourth fresh adversarial
reviewer, a reused fidelity reviewer and exact controls support the scoped
return; no successor or physical adoption starts automatically.
'''+s[z:]
needle='The latter fails RG in this displayed completion and smooth finite positive\nnonzero conformal gauges, not under a proved classification of all extensions.'
assert needle in s;s=s.replace(needle,needle+' R16CCW later\nuses scalar curvature to exclude an RG endpoint for that same physical future\ntail in any representation, without classifying other ends or extensions.',1)
needle='The regular ray family is supplied, not proved\nto exist from RG alone.'
assert needle in s;s=s.replace(needle,'The regular ray family is supplied in FCL1. R16CCW constructs a chosen local\nemitter family under its explicit extension condition; prescribed remote\naccess is not established by RG alone.',1)
s=s.replace('<a id="r17"></a>',(B/'CENTRAL_INSERT.md').read_text()+'\n\n<a id="r17"></a>',1)
a=s.index('The answered question is no longer left as an unexecuted obstruction.');z=s.index("NGD1's numerical return",a)
s=s[:a]+'''The answered FCL question is no longer left as an unexecuted obstruction.
CCW1 now connects its asymptote to source proper time and limiting scalar
curvature, and constructs a regular family for a chosen nearby emitter under
an explicit local extension condition. It retains the distinct question of
access from a prescribed distant source. The beta2 obstruction is stronger for
its same physical future tail; the frozen original FCW source is not rewritten.
A different-free-receiver population with unbounded initial boosts keeps Z=1,
so the pointwise theorem cannot become a distance curve by changing quantifiers.

Physical RG admission and native event/path assignment remain open. The
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
Stop for lay discussion; no successor or physical adoption starts automatically.

'''+s[z:]
s=s.replace('[55 later returns]','[56 later returns]',1)
s=s.replace('registered rows have an editorial disposition;55 relevant later returns','registered rows have an editorial disposition;56 relevant later returns',1)
s=s.replace('includes55 later returns/clarifications','includes56 later returns/clarifications',1)
review='''CCW1 used three fresh source-first whiteboard contributors and a fourth
fresh source-first/exposed adversarial reviewer. A reused physical contributor
provided the second exposed/final integration review; that context is not
independent authorship of its own clock-gap argument. The fourth reviewer
independently recovered the invariant clock-gap/curvature relation before
seeing the synthesis. Exposed reviews checked curvature signs, actual clocks,
finite regularity, local/global and population quantifiers, and physical
attribution. Parent direct-Christoffel exact controls passed four families/seven
cases. No scientific repair was required; the initial candidate stays fixed.
A failed metadata seal attempt used the wrong contributor hash-key shape before
writing any freeze; the corrected seal records it. No different-model, human,
formal or empirical verification is claimed. [Work record](udt_completion_connection_whiteboard_2026-10-03/WORK_RECORD.md)
and [descendant review](udt_completion_connection_whiteboard_2026-10-03/DESCENDANT_REVIEW.md)
retain exposure, checks and omissions. Actual final attestations and closure
receipts own integration/banking status.

'''
s=s.replace('The preserved first candidates expose the repair history.',review+'The preserved first candidates expose the repair history.',1)
p.write_text(s);Path('CURRENT_RESEARCH_PROGRAM.md').write_text(verify.program_text(s))
common='''CDR1 remains the central-development architecture. UDT_DEVELOPMENT.md is the
sole maintained scientific argument; CURRENT_SCIENTIFIC_PREMISES.tsv and reviewed
sources own exact grades. The generated CURRENT_RESEARCH_PROGRAM.md is the bounded
startup orientation. Read R16CCW/R16FCL/R18 after orientation for the current argument.

Charles authorized the CCW1 whiteboard after the completed FCL1 derivation and
startup cleanup. FCL1 was checked, committed and synchronized at28efe475;
CCW1 evidence is in udt_completion_connection_whiteboard_2026-10-03/.
Its WORK_ORDER owns scope. Three source-first contributions, the original
synthesis, exact controls and fresh/reused exposed reviews are preserved.
Final attestations and actual normal/maintenance/full406 receipts own closure;
commit/push and byte checks own banking. Verify actual HEAD, remote, dirt and
processes rather than assuming this text identifies the tip.

Next: Stop for lay discussion of the CCW1 decision brief and unexecuted
prepared-distance proposal. The whiteboard authorizes no successor or RG/FC
adoption, native field/source/action law, registry promotion, GPU/data/hardware
campaign. One short CPU exact-control script was run; no long solver. The
no-timeout direction persists with finite scope/resource/manual stops.
Preserve protected and unrelated work.

'''
for filename,title,end in [('LIVE.md','CURRENT STATE','### Honest claim'),('HANDOFF.md','Current handoff','Protected payloads require explicit dispatch;')]:
 p=Path(filename);t=p.read_text();a=t.index('## '+title);z=t.index(end,a)
 t=t[:a]+f'## {title} — CCW1 completion-connection whiteboard return, 2026-10-04\n\n'+common+t[z:]
 if filename=='LIVE.md':
  a=t.index('### Next gate');z=t.index('<!-- STARTUP_CURRENT_END -->',a)
  t=t[:a]+'''### Next gate

Stop for lay discussion using central R16CCW/R16FCL/R18 and the CCW1 decision
brief. The proposed prepared-distance test is unexecuted; no successor starts
automatically. Native admission and physical attribution remain open. Verify
actual evidence, final bindings and synchronization. Existing pauses/protected
boundaries persist. TPS1 raw fields/large streams remain local-only; compact
remote records cannot replay raw-dependent checks.

'''+t[z:]
 p.write_text(t)
g=json.loads((W/'DEVELOPMENT_GRAPH.json').read_text());assert len(g['nodes'])==124
sources=[str(B/f) for f in ['INITIAL_SYNTHESIS.md','REVIEWED_RESULT.md','WORK_ORDER.md']]
for f in sources:g['sources_sha256'][f]=sha(f)
lookup={n['id']:n for n in g['nodes']}
for key in ['R6','R16','R16FCW','R16FCL','R18','O_CPW_FREECLOCK_LIMIT','O_FCW_ADMISSION']:
 lookup[key]['sources'].append(str(B/'REVIEWED_RESULT.md'))
lookup['O_CPW_FREECLOCK_LIMIT']['statement']='FCL1 answers its pointwise free-receiver limit; CCW1 adds invariant source-clock-gap/curvature relations and an explicit-extension local chosen-emitter existence lemma. Prescribed remote/global access, uniform prepared populations and fixed-emission distance attachment remain open. The unbounded-boost free population control prevents a silent quantifier exchange. This open join is not a proof input.'
lookup['O_FCW_ADMISSION']['statement']='Physical RG admission, native geometry and additional-effect attribution remain OPEN. CCW1 supplies necessary curvature/clock diagnostics and scoped local signal existence, not a selector. CPW1 parks physical FC; prior conditional diagnostics survive. A prepared-distance successor is proposed but unexecuted; no scale/X_max selection.'
g['nodes'].extend([
 dict(id='C_CCW_RG',kind='conditional_protocol',statement='UNADOPTED supplied C3 Lorentz4 regular spacelike conformal endpoint g=x^-2 b, nonzero timelike dx; for the clock/local-receiver conclusions, one finite-data free receiver approaching that endpoint. No rescaled-velocity bound, native selection or field equation. Curvature identity itself only needs the stated completion.',sources=sources,registry_ids=[]),
 dict(id='C_CCW_QUERY',kind='conditional_protocol',statement='Scope split: clock limits additionally use an actual regular interior-emitter null family with consistent normalization; local family existence instead uses a C3 Lorentz extension/convex normal neighborhood and existentially chosen timelike emitter, without assuming that branch. A prescribed remote source, uniform population, distance map and physical attribution are not supplied by this condition. Diagnostic metrics/preparations are freely supplied controls.',sources=sources,registry_ids=[]),
 dict(id='R16CCW',kind='argument',anchor='r16ccw',title='Conditional invariant clock-curvature relation, local signal existence and population limitation',sources=sources,registry_ids=[],required_conditions=['P_NULL','C_CCW_RG','C_CCW_QUERY'])])
for a,b,k in [('P_NULL','R16CCW','hypothesis'),('C_CCW_RG','R16CCW','hypothesis'),('C_CCW_QUERY','R16CCW','hypothesis'),('R6','R16CCW','proof'),('R16CPW','R16CCW','proof'),('R16FCL','R16CCW','proof'),('R16FCW','R16CCW','context'),('R9FST','R16CCW','context'),('O_FCW_ADMISSION','R16CCW','open_boundary'),('R16CCW','R18','context')]:
 g['edges'].append({'from':a,'to':b,'kind':k})
targets=['D1','R6','R8','R16','R16FCW','R16CPW','R16FCL','R16CCW','R18','O_CPW_FREECLOCK_LIMIT','O_FCW_ADMISSION','C_CCW_RG','C_CCW_QUERY']
for rel in ['contributor_geometry/REPORT.md','contributor_physical/REPORT.md','contributor_adversarial/REPORT.md','review_math/EXPOSED_REVIEW.md','review_fidelity/EXPOSED_REVIEW.md','DESCENDANT_REVIEW.md']:
 f=str(B/rel);g['review_support'].append(dict(path=f,sha256=sha(f),role='review_evidence',targets=targets))
(W/'DEVELOPMENT_GRAPH.json').write_text(json.dumps(g,indent=2)+'\n')
p=W/'RECENT_DISPOSITIONS.tsv';rows=list(csv.DictReader(p.open(),delimiter='\t'));assert len(rows)==55
row=dict(id='CCW1_RETURN',source=str(B/'REVIEWED_RESULT.md'),current_scope='VERIFIED-WITH-CAVEATS_CONDITIONAL_DIAGNOSTICS; RG UNADOPTED; invariant clock-gap/curvature relation, explicit-extension local chosen-emitter existence, same-tail beta2 obstruction and unbounded-population counterexample; proposed distance test unexecuted',central_location='D1;R6;R8;R16;R16FCW;R16CPW;R16FCL;R16CCW;R18',rederivation_depth='ANALYTIC_CONNECTIONS_AND_EXACT4FAMILY7CASE_CONTROLS; three source-first contributors, fourth fresh independent source-first/exposed review and reused fidelity review; no native geometry/physical adoption/scale/distance law',source_sha256=sha(B/'REVIEWED_RESULT.md'))
with p.open('a',newline='') as f:csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n').writerow(row)
print(json.dumps(dict(nodes=len(g['nodes']),edges=len(g['edges']),sources=len(g['sources_sha256']),review_support=len(g['review_support']),later_returns=56,orientation_words=len(verify.orientation(s).split()))))
