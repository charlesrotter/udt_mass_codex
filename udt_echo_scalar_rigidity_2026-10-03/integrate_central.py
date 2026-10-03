"""ESR1 central synthesis; final actual review/binding is separate."""
from pathlib import Path
import json,csv,hashlib,sys
sys.path.insert(0,str(Path.cwd()))
import verify_udt_development as verify
B=Path('udt_echo_scalar_rigidity_2026-10-03');W=Path('development_reconstruction_2026-09-29')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
p=Path('UDT_DEVELOPMENT.md');s=p.read_text();assert '<a id="r8esr">' not in s
s=s.replace('FCW1 and IEC1, 2026-10-03','FCW1, IEC1 and ESR1, 2026-10-03',1)
old='''result interprets the diagnostic; native geometry, positional attribution and
all-frame selection remain open. Stop for discussion of a bounded selectivity
test; no classification or new research campaign starts automatically.'''
new='''result interprets the diagnostic; native geometry and positional attribution
remain open. ESR1 below answers its conditional all-frame scalar selectivity test.
ESR1 proves that one smooth scalar echo rule across every prepared observer and
direction forces constant sectional curvature within the supplied locally symmetric
class. Positive, negative and flat curvature remain possible, without a selected
scale. Nonflat records fix the rational rule only on their attained interval;
flat records fix only its value at1. The proof uses quartic clock information,
curvature algebra and actual future returns, with independent exact checks.
FC remains UNADOPTED: universal governing law does not establish scalar sufficiency.
This result states the trial's mathematical cost, not its physical authority.
Stop for lay discussion; no extension, adoption or successor starts automatically.'''
assert old in s;s=s.replace(old,new,1)
old='''General all-observer inverse/rigidity and native-sector
questions remain open; the restricted-sheet nonuniqueness survives.'''
new='''General all-observer inverse and native-sector questions remain open;
ESR1 below answers the specific conditional all-frame FC rigidity question in
locally symmetric geometry. The restricted-sheet nonuniqueness survives.'''
assert old in s;s=s.replace(old,new,1)
old='''coefficient whenever V=0. Classification and physical FC admission remain OPEN.
The plane obstruction alone still does not predict the order of echo failure.'''
new='''coefficient whenever V=0. ESR1 below classifies locally symmetric all-frame
FC cases; physical FC admission remains OPEN. The plane obstruction alone
still does not predict the order of echo failure.'''
assert old in s;s=s.replace(old,new,1)
old='''assignment, physical FC admission and all-frame rigidity remain open. FCW1's
completion/RG lead is unchanged and was not pursued.'''
new='''assignment and physical FC admission remain open. ESR1 below answers this
class's specific all-frame FC rigidity question. FCW1's completion/RG lead
is unchanged and was not pursued.'''
assert old in s;s=s.replace(old,new,1)
s=s.replace('<a id="r8pcc"></a>',(B/'CENTRAL_INSERT.md').read_text()+'\n<a id="r8pcc"></a>',1)
old='''IEC1's next recommended discussion is a bounded selectivity test within the same
supplied ∇R=0 class: can one smooth scalar q=Q(p) across all regular PSW frames/
directions coexist with non-space-form curvature? Arbitrary Q and the specific
ECS relation must be distinguished, including degeneracies. This would test the
cost/selectivity of the still-UNADOPTED FC proposal, not derive its physical
authority from universality. The [IEC1 decision brief](udt_invariant_echo_curvature_2026-10-03/DECISION_BRIEF.md)
states the proposed algebra/control/review budget, alternatives and return point.
No such all-frame theorem is claimed or successor authorized by this return.'''
new='''IEC1's proposed all-frame scalar selectivity question is now answered by ESR1
in R8ESR. Within the supplied ∇R=0 class, arbitrary smooth Q forces constant
sectional curvature; the exact rational rule then follows on attained records.
Flat and zero-leading cases are explicitly covered. The theorem leaves sign,
scale and global geometry free and supplies no physical authority for FC.
It strengthens the conditional classification without refuting the weaker
restricted-sheet mimics or turning universal law into scalar sufficiency.

The current recommendation is to retain FC as a conditional diagnostic and
discuss its cost before any physical adoption. It constrains total curvature;
applying it only to an additional positional part would first need justified
attribution. A variable-curvature extension would be a new mathematical scope,
not an automatic next step or a proof of physical relevance. The
[ESR1 decision brief](udt_echo_scalar_rigidity_2026-10-03/DECISION_BRIEF.md)
records this return and alternatives. The original [IEC1 proposal](udt_invariant_echo_curvature_2026-10-03/DECISION_BRIEF.md)
remains the fixed authorization precursor. No successor or physical adoption starts.'''
assert old in s;s=s.replace(old,new,1)
s=s.replace('includes52 later returns/clarifications','includes53 later returns/clarifications',1)
review='''ESR1 uses two fresh source-first/exposed/final reviewer contexts. Independent
proofs converge; the parent/math boost-plane argument is complemented by the
fidelity review's Ricci null-cone step. Both independently authored full algebraic
curvature rank checks with different rational frame sets; shared model/SymPy
and related bivector methods are explicit limits. Parent exact Q matching and
original signed-incidence roots independently check branch/formula handling.
The first structural-equality failure, exact canonicalization repair and reviewer
count/method-label corrections are preserved; no scientific candidate or tolerance
changed. [ESR1 work record](udt_echo_scalar_rigidity_2026-10-03/WORK_RECORD.md)
and [descendant review](udt_echo_scalar_rigidity_2026-10-03/DESCENDANT_REVIEW.md)
record exposure, actual checks and omissions. Final identical-map attestations
and captured normal/maintenance/full406 receipts own completion status.

'''
s=s.replace('The preserved first candidates expose the repair history.',review+'The preserved first candidates expose the repair history.',1)
p.write_text(s);Path('CURRENT_RESEARCH_PROGRAM.md').write_text(verify.program_text(s))
for filename,start,end,title in [('LIVE.md','## CURRENT STATE','### Honest claim','CURRENT STATE'),('HANDOFF.md','## Current handoff','Protected payloads require explicit dispatch;','Current handoff')]:
 p=Path(filename);s=p.read_text();a=s.index(start);z=s.index(end,a)
 current=f'''## {title} — ESR1 scalar echo-selectivity return, 2026-10-03

CDR1 remains the central-development architecture; exact grades stay in
CURRENT_SCIENTIFIC_PREMISES.tsv. LIVE.md owns status. Verify grok HEAD, remote,
dirt and actual host state. Charles authorized IEC1's proposed bounded scalar
selectivity study, including construction, short checks, two fresh reviews,
same-premise repair, central integration and lay return. Fixed evidence is under
`udt_echo_scalar_rigidity_2026-10-03/`; UDT_DEVELOPMENT.md R8ESR/R18 owns
the maintained argument. CURRENT_RESEARCH_PROGRAM.md is its generated startup
excerpt. No physical premise, equation, scale, registry grade or CANON adoption
is made. FC/RG remain UNADOPTED.

The conditional proof, exact controls and two fresh source-first/exposed reviews
are saved. Actual final attestations and normal/maintenance/full406 receipts own
acceptance/pass status. The initial symbolic comparison failure and same-equation
repair remain preserved. No GPU, empirical fit, hardware experiment or paused
source/carrier campaign is part of ESR1. No-timeout direction persists with
finite/resource/manual stops. Preserve protected payloads and unrelated work.

Next: Stop for lay discussion of ESR1 and the physical cost of the scalar trial.
Its decision brief recommends retaining FC as a conditional diagnostic. A
variable-curvature extension or the separate completion lead needs its own
bounded decision; neither starts automatically. A clock anomaly is not the
project objective. Verify actual processes; review bindings remain in
development_reconstruction_2026-09-29. TPS1 raw fields/large streams remain
local-only, so remote compact records cannot replay raw-dependent checks.
ESR1 is banked only when actual commit/push and exact-byte checks have completed.

'''
 s=s[:a]+current+s[z:]
 if filename=='LIVE.md':
  a=s.index('### Next gate');z=s.index('<!-- STARTUP_CURRENT_END -->',a)
  s=s[:a]+'''### Next gate

Stop for lay discussion of ESR1 using central R8ESR/R18 and its decision brief.
Physical FC authority, native geometry/response and positional attribution remain
open. No automatic successor, premise adoption, GPU/data campaign or hardware
experiment. Existing pauses/protected boundaries remain; verify actual processes.

'''+s[z:]
 p.write_text(s)
g=json.loads((W/'DEVELOPMENT_GRAPH.json').read_text());assert len(g['nodes'])==116
sources=[str(B/f) for f in ['INITIAL_CANDIDATE.md','REVIEWED_RESULT.md','review_math/SOURCE_FIRST.md','review_fidelity/SOURCE_FIRST.md']]
for f in sources:g['sources_sha256'][f]=sha(f)
lookup={n['id']:n for n in g['nodes']}
for key in ['R8','R18','R8ECS','R8ECSM','R8FCW','R8IEC','O_PSW_ATTRIBUTION','O_FCW_ADMISSION']:
 lookup[key]['sources'].append(str(B/'REVIEWED_RESULT.md'))
lookup['O_FCW_ADMISSION']['statement']='Physical justification/adoption of FC or RG, generic variable-curvature rigidity, completion/protocol robustness and native geometry/scale remain OPEN. IEC1 supplies the local symmetric echo expansion; ESR1 proves arbitrary-smooth-Q all-preparation rigidity exactly within that class, conditional on the explicitly UNADOPTED FC trial. No successor starts automatically.'
lookup['O_PSW_ATTRIBUTION']['statement']+=' ESR1 classifies total curvature only under hypothetical all-preparation scalar sufficiency within parallel-curvature metrics; no positional-component attribution follows.'
g['nodes'].append(dict(id='C_ESR_FC',kind='conditional_protocol',statement='UNADOPTED FC trial: one smooth Q near1 for every PSW event/future-unit-U/unit-n including both physical directions and every sufficiently small positive L on regular actual first/later-return branches in a connected supplied locally symmetric Lorentz4 region. Preparation-dependent radius allowed; no physical scalar-sufficiency premise is adopted.',sources=sources,registry_ids=[]))
g['nodes'].append(dict(id='R8ESR',kind='argument',anchor='r8esr',title='All-preparation scalar echo rule selects constant sectional curvature within the locally symmetric class',sources=sources,registry_ids=[],required_conditions=['C_IEC_LOCAL_SYMMETRY','C_ESR_FC']))
for a,b,k in [('C_IEC_LOCAL_SYMMETRY','R8ESR','hypothesis'),('C_ESR_FC','R8ESR','hypothesis'),('R8IEC','R8ESR','proof'),('R8ECS','R8ESR','proof'),('R8ECSM','R8ESR','context'),('R8FCW','R8ESR','context'),('R8ESR','R18','context'),('O_FCW_ADMISSION','R8ESR','open_boundary'),('O_PSW_ATTRIBUTION','R8ESR','open_boundary')]:
 g['edges'].append({'from':a,'to':b,'kind':k})
targets=['R7','R8','R9','R16','R18','R8ECS','R8ECSM','R8FCW','R8IEC','R8ESR','O_PSW_ATTRIBUTION','O_FCW_ADMISSION']
for rel in ['review_math/EXPOSED_REVIEW.md','review_math/PARENT_REPAIR_REVIEW.md','review_fidelity/EXPOSED_REVIEW.md','review_fidelity/REPAIR_REVIEW.md','DESCENDANT_REVIEW.md']:
 f=str(B/rel);g['review_support'].append(dict(path=f,sha256=sha(f),role='review_evidence',targets=targets))
(W/'DEVELOPMENT_GRAPH.json').write_text(json.dumps(g,indent=2)+'\n')
p=W/'RECENT_DISPOSITIONS.tsv';rows=list(csv.DictReader(p.open(),delimiter='\t'));assert len(rows)==52
row=dict(id='ESR1_RETURN',source=str(B/'REVIEWED_RESULT.md'),current_scope='VERIFIED-WITH-CAVEATS_CONDITIONAL_RIGIDITY; within supplied locally symmetric Lorentz4, all-PSW smooth scalar Q iff constant sectional curvature; flat and one-sided-Q freedom retained; FC remains UNADOPTED',central_location='R7;R8;R9;R16;R18;R8ECS;R8ECSM;R8FCW;R8IEC;R8ESR',rederivation_depth='IEC_QUARTIC_TO_Q_JETS_OPPOSITE_DIRECTIONS_AND_FULL_TENSOR_POLARIZATION; independent Ricci-null-cone route and exact curvature ranks; signed original future incidences; no native admission or variable-curvature theorem',source_sha256=sha(B/'REVIEWED_RESULT.md'))
with p.open('a',newline='') as f:csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n').writerow(row)
print(json.dumps(dict(nodes=len(g['nodes']),edges=len(g['edges']),sources=len(g['sources_sha256']),review_support=len(g['review_support']),later_returns=53)))
