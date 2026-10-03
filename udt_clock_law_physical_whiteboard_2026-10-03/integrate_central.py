"""CPW1 bounded central integration; actual final review/binding remains separate."""
from pathlib import Path
import json,csv,hashlib,sys
sys.path.insert(0,str(Path.cwd()))
import verify_udt_development as verify
B=Path('udt_clock_law_physical_whiteboard_2026-10-03');W=Path('development_reconstruction_2026-09-29')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
p=Path('UDT_DEVELOPMENT.md');s=p.read_text();assert '<a id="r8cpw">' not in s
s=s.replace('FCW1, IEC1 and ESR1, 2026-10-03','FCW1, IEC1, ESR1 and CPW1, 2026-10-03',1)
old='''This result states the trial's mathematical cost, not its physical authority.
Stop for lay discussion; no extension, adoption or successor starts automatically.'''
new='''This result states the trial's mathematical cost, not its physical authority.
CPW1's three-perspective whiteboard recommends parking FC as a physical-selection
extension while retaining its diagnostic and the native scalar kernel. A full
directional echo evaluator is already established and does not select geometry.
The parent proposes one separate optional test of RG completion under specified
moving free clocks and nonuniform geometry. Exact conformal bookkeeping is
checked; the free-clock limit remains unproved and RG UNADOPTED. The proposed
first test fixes one receiver and regular interior emissions, not a population
or distance curve. Stop for lay discussion; no successor or adoption starts.'''
assert old in s;s=s.replace(old,new,1)
s=s.replace('<a id="r8pcc"></a>',(B/'CENTRAL_CLOCK_INSERT.md').read_text()+'\n<a id="r8pcc"></a>',1)
s=s.replace('<a id="r17"></a>',(B/'CENTRAL_COMPLETION_INSERT.md').read_text()+'\n<a id="r17"></a>',1)
old='''The current recommendation is to retain FC as a conditional diagnostic and
discuss its cost before any physical adoption. It constrains total curvature;
applying it only to an additional positional part would first need justified
attribution. A variable-curvature extension would be a new mathematical scope,
not an automatic next step or a proof of physical relevance. The
[ESR1 decision brief](udt_echo_scalar_rigidity_2026-10-03/DECISION_BRIEF.md)
records this return and alternatives. The original [IEC1 proposal](udt_invariant_echo_curvature_2026-10-03/DECISION_BRIEF.md)
remains the fixed authorization precursor. No successor or physical adoption starts.'''
new='''CPW1 now completes the physical-meaning whiteboard requested after ESR1.
Its three independent contributors recommend parking an FC physical-selection
extension: equal first-ratio preparations need not be equated by universal law.
The inspected sources do not establish FC, while R6--R8's richer conditional
comparison law is already available. This is neither a retraction of the scalar
kernel nor a proof that complete UDT needs a new premise. ESR1 and all earlier
positive/adverse controls retain their scopes; physical attribution stays open.

The parent recommends ONE distinct optional next derivation, not contributor
consensus: R16CPW's conformal free-clock robustness test of existing UNADOPTED RG.
For one specified geodesic receiver and regular interior emission family, derive
or refute the endpoint control needed for the clock asymptote without assuming
bounded rescaled receiver velocity. This is a narrower clock-limit question;
fixed-emission distance curves, uniform populations, physical admission, scale
and X_max remain separate. Exact bookkeeping is established here, not the
proposed geodesic theorem. No source/action/Einstein equation is supplied.

The [CPW1 decision brief](udt_clock_law_physical_whiteboard_2026-10-03/DECISION_BRIEF.md)
and [precise successor scope](udt_clock_law_physical_whiteboard_2026-10-03/SUCCESSOR_SCOPE.md)
give the conditional cost, no-change alternative, checks/review budget and stop.
Parking both trials remains available. The original ESR/IEC decision records
stay fixed evidence. Return for discussion; no successor or physical adoption
starts from this reviewed whiteboard.'''
assert old in s;s=s.replace(old,new,1)
s=s.replace('includes53 later returns/clarifications','includes54 later returns/clarifications',1)
review='''CPW1 uses three fresh source-first contributors and two additional fresh
source-first/exposed/final reviewer contexts. All contributors recommend keeping
FC diagnostic; the optional RG robustness recommendation is separately attributed
to the parent. Reviewers independently hand-check the general conformal identity,
relay composition and actual-clock controls and inspect saved exact outputs.
Shared model/library/source exposure remains explicit. One parent structural
matrix-equality failure and exact-comparison repair are preserved; no equation
or scientific premise changes. The proposed successor was narrowed after review
advice and remains unexecuted. [Work record](udt_clock_law_physical_whiteboard_2026-10-03/WORK_RECORD.md)
and [descendant review](udt_clock_law_physical_whiteboard_2026-10-03/DESCENDANT_REVIEW.md)
record exposure, scope and omissions, including a contributor's disclosed
overbroad registry-read error. Actual final accepted-map attestations and
normal/maintenance/full406 receipts own closure; review does not adopt FC/RG.

'''
s=s.replace('The preserved first candidates expose the repair history.',review+'The preserved first candidates expose the repair history.',1)
p.write_text(s);Path('CURRENT_RESEARCH_PROGRAM.md').write_text(verify.program_text(s))
for filename,start,end,title in [('LIVE.md','## CURRENT STATE','### Honest claim','CURRENT STATE'),('HANDOFF.md','## Current handoff','Protected payloads require explicit dispatch;','Current handoff')]:
 p=Path(filename);s=p.read_text();a=s.index(start);z=s.index(end,a)
 current=f'''## {title} — CPW1 physical clock-law whiteboard return, 2026-10-03

CDR1 remains the central-development architecture; exact grades stay in
CURRENT_SCIENTIFIC_PREMISES.tsv. LIVE.md owns status. Verify grok HEAD, remote,
dirt and actual host state. Charles authorized the bounded three-perspective
whiteboard, short checks, two fresh adversarial reviews, same-premise repair,
central integration and lay return. Fixed evidence is under
`udt_clock_law_physical_whiteboard_2026-10-03/`; UDT_DEVELOPMENT.md
R8CPW/R16CPW/R18 owns the maintained argument. CURRENT_RESEARCH_PROGRAM.md is
its generated startup excerpt. No physical premise, equation, scale, registry
grade or CANON adoption is made. FC/RG remain UNADOPTED.

Three source-first contributions, two fresh exposed reviews and scoped exact
controls are saved. Actual final attestations and normal/maintenance/full406
receipts own acceptance/pass status. The initial symbolic comparison failure
and same-equation repair remain preserved. No GPU, empirical/hardware campaign
or generic completion/free-clock theorem is part of CPW1. No-timeout direction
persists with finite/resource/manual stops. Preserve protected/unrelated work.

Next: Stop for lay discussion of the CPW1 decision brief. The parent proposes
one optional completion/free-clock robustness test; its exact narrowed scope
is SUCCESSOR_SCOPE.md in that package. It requires a new bounded decision and
does not start automatically. This does not adopt RG or a physical clock
population. A clock anomaly is not the project objective. Verify processes;
review bindings remain in development_reconstruction_2026-09-29. TPS1 raw
fields/large streams remain local-only; compact remote records cannot replay
raw-dependent checks. CPW1 is banked only after actual commit/push and byte checks.

'''
 s=s[:a]+current+s[z:]
 if filename=='LIVE.md':
  a=s.index('### Next gate');z=s.index('<!-- STARTUP_CURRENT_END -->',a)
  s=s[:a]+'''### Next gate

Stop for lay discussion of CPW1 using central R8CPW/R16CPW/R18 and its decision
brief/SUCCESSOR_SCOPE. Physical admission, native geometry/response and positional
attribution remain open. No automatic successor, premise adoption, GPU/data
campaign or hardware experiment. Existing pauses/protected boundaries remain.

'''+s[z:]
 p.write_text(s)
g=json.loads((W/'DEVELOPMENT_GRAPH.json').read_text());assert len(g['nodes'])==118
sources=[str(B/f) for f in ['INITIAL_SYNTHESIS.md','REVIEWED_RESULT.md','fidelity/SOURCE_FIRST.md','geometry/SOURCE_FIRST.md','operational/SOURCE_FIRST.md','SUCCESSOR_SCOPE.md']]
for f in sources:g['sources_sha256'][f]=sha(f)
lookup={n['id']:n for n in g['nodes']}
for key in ['R6','R7','R8','R16','R18','R8ESR','R16FCW','O_PSW_ATTRIBUTION','O_FCW_ADMISSION']:
 lookup[key]['sources'].append(str(B/'REVIEWED_RESULT.md'))
lookup['O_FCW_ADMISSION']['statement']+=' CPW1 recommends parking FC physical-selection extension; the parent proposes an unexecuted pointwise geodesic-clock robustness test under still-UNADOPTED RG. Exact conformal bookkeeping does not prove receiver limits or physical admission.'
lookup['O_PSW_ATTRIBUTION']['statement']+=' CPW1 keeps scalar normalization and full directional evaluation distinct from physical selection; its supplied controls are not native countermodels, and no new premise is proved necessary.'
g['nodes'].extend([
 dict(id='C_CPW_CONFORMAL',kind='conditional_protocol',statement='Supplied smooth positive conformal metric g=Omega^-2 gbar, regular affine null branches with consistent per-ray normalization and ordinary proper clocks. Exact frequency bookkeeping; a finite positive Omega_o Z limit additionally assumes finite positive A=Omega_e omegabar_e and B=omegabar_o limits. Those limits for actual geodesic preparations are OPEN, not inferred from RG or normalization.',sources=sources,registry_ids=[]),
 dict(id='O_CPW_FREECLOCK_LIMIT',kind='open_join',statement='UNEXECUTED proposed RG robustness target: one finite-data future timelike geodesic receiver approaching a regular future spacelike C3 conformal boundary, regular conformal-null family from compact interior emitter events with consistent omega_e=1; determine rescaled receiver/frequency limits without assuming them. No uniform population, fixed-emission distance law, physical RG admission or X_max identification.',sources=[str(B/'SUCCESSOR_SCOPE.md'),str(B/'REVIEWED_RESULT.md')],registry_ids=[]),
 dict(id='R8CPW',kind='argument',anchor='r8cpw',title='Physical scope of scalar echo sufficiency and retained full comparison data',sources=sources,registry_ids=[],required_conditions=['P_NULL','M_GEOMETRY']),
 dict(id='R16CPW',kind='argument',anchor='r16cpw',title='Conformal clock bookkeeping separated from proposed free-clock endpoint theorem',sources=sources,registry_ids=[],required_conditions=['P_NULL','C_CPW_CONFORMAL'])])
for a,b,k in [('P_NULL','R8CPW','hypothesis'),('M_GEOMETRY','R8CPW','hypothesis'),('R6','R8CPW','proof'),('R7','R8CPW','proof'),('R8','R8CPW','proof'),('R8ESR','R8CPW','context'),('D1','R8CPW','context'),('O_PSW_ATTRIBUTION','R8CPW','open_boundary'),('P_NULL','R16CPW','hypothesis'),('C_CPW_CONFORMAL','R16CPW','hypothesis'),('R6','R16CPW','proof'),('R16FCW','R16CPW','context'),('C_FCW_RG','O_CPW_FREECLOCK_LIMIT','context'),('O_CPW_FREECLOCK_LIMIT','R16CPW','open_boundary'),('O_FCW_ADMISSION','R16CPW','open_boundary'),('R8CPW','R18','context'),('R16CPW','R18','context')]:
 g['edges'].append({'from':a,'to':b,'kind':k})
targets=['D1','R6','R7','R8','R9','R16','R18','R8ESR','R16FCW','R8CPW','R16CPW','O_CPW_FREECLOCK_LIMIT','O_PSW_ATTRIBUTION','O_FCW_ADMISSION']
for rel in ['review_math/EXPOSED_REVIEW.md','review_fidelity/EXPOSED_REVIEW.md','review_fidelity/PROPOSAL_PRECISION_REVIEW.md','DESCENDANT_REVIEW.md']:
 f=str(B/rel);g['review_support'].append(dict(path=f,sha256=sha(f),role='review_evidence',targets=targets))
(W/'DEVELOPMENT_GRAPH.json').write_text(json.dumps(g,indent=2)+'\n')
p=W/'RECENT_DISPOSITIONS.tsv';rows=list(csv.DictReader(p.open(),delimiter='\t'));assert len(rows)==53
row=dict(id='CPW1_RETURN',source=str(B/'REVIEWED_RESULT.md'),current_scope='VERIFIED-WITH-CAVEATS_SOURCE_RELATIVE_WHITEBOARD; park physical FC extension, retain native kernel/full comparison diagnostics; exact conditional conformal bookkeeping; RG/geodesic robustness only proposed, no native selection',central_location='D1;R6;R7;R8;R9;R16;R18;R8ESR;R16FCW;R8CPW;R16CPW',rederivation_depth='OWNER_SOURCE_FACTORISATION_AUDIT_AND_RECOVERED_RELAY_IDENTITY; two supplied actual-clock controls; direct conformal affine/frequency algebra and exact control;3fresh contributors and2fresh adversarial reviewers; successor not executed',source_sha256=sha(B/'REVIEWED_RESULT.md'))
with p.open('a',newline='') as f:csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n').writerow(row)
print(json.dumps(dict(nodes=len(g['nodes']),edges=len(g['edges']),sources=len(g['sources_sha256']),review_support=len(g['review_support']),later_returns=54)))
