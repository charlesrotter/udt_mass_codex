"""IEC1 scoped central integration; no review acceptance is manufactured."""
from pathlib import Path
import json,csv,hashlib,sys
sys.path.insert(0,str(Path.cwd()))
import verify_udt_development as verify
B=Path('udt_invariant_echo_curvature_2026-10-03');W=Path('development_reconstruction_2026-09-29')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
p=Path('UDT_DEVELOPMENT.md');s=p.read_text();assert '<a id="r8iec">' not in s
s=s.replace('CBR1 and FCW1, 2026-10-03','CBR1, FCW1 and IEC1, 2026-10-03',1)
s=s.replace('the general invariant being measured remains open. A separately proposed regular','the invariant question is answered within a declared class by IEC1 below. A separately proposed regular',1)
s=s.replace('invariant echo derivation first; no successor starts automatically.','''completed invariant echo derivation below; no successor starts automatically.
IEC1 derives the finite-echo curvature diagnostic through sixth order for supplied
locally symmetric Lorentz4 geometries. General directions can differ from the
simple echo relation at fourth order; FCW1's sixth-order case extends to tidal
eigen-directions. Opposite preparation directions isolate one transverse
curvature contribution. The local geometric proof, exact algebra and independent
controls use ordinary proper clocks and actual future returns. Neither this
symmetry class nor scalar sufficiency FC is adopted as physical UDT law. The
result interprets the diagnostic; native geometry, positional attribution and
all-frame selection remain open. Stop for discussion of a bounded selectivity
test; no classification or new research campaign starts automatically.''',1)
old='''formula and classification are OPEN. The obstruction alone does not predict the
order of echo failure. Deriving that invariant on a declared locally symmetric
sector is the recommended discussion target, without adopting FC.'''
new='''formula is now derived through L^6 for the declared locally symmetric class in
IEC1 below, with a generally nonzero quartic term and the displayed sixth-order
coefficient whenever V=0. Classification and physical FC admission remain OPEN.
The plane obstruction alone still does not predict the order of echo failure.'''
assert old in s;s=s.replace(old,new,1)
s=s.replace('<a id="r8pcc"></a>',(B/'CENTRAL_INSERT.md').read_text()+'\n<a id="r8pcc"></a>',1)
old='''recommended next discussion is an invariant sixth-order echo derivation on a
declared locally symmetric sector, with source-preserving counterexamples and
review. That geometric investigation need not adopt FC. Completion/protocol
robustness is a second option; a physical reason for RG is still absent. The'''
new='''first recommended derivation is now completed by IEC1 in R8IEC: the general
locally symmetric echo includes a quartic transverse-curvature term and an
explicit sixth-order contraction. The earlier coefficient survives for tidal
eigen-directions. Opposite preparations separate geometric information without
adopting FC. Completion/protocol robustness remains a second option; a physical
reason for RG is still absent. The'''
assert old in s;s=s.replace(old,new,1)
needle='adoption, field-law selection or new campaign starts automatically.'
assert needle in s;s=s.replace(needle,needle+'''

IEC1's next recommended discussion is a bounded selectivity test within the same
supplied ∇R=0 class: can one smooth scalar q=Q(p) across all regular PSW frames/
directions coexist with non-space-form curvature? Arbitrary Q and the specific
ECS relation must be distinguished, including degeneracies. This would test the
cost/selectivity of the still-UNADOPTED FC proposal, not derive its physical
authority from universality. The [IEC1 decision brief](udt_invariant_echo_curvature_2026-10-03/DECISION_BRIEF.md)
states the proposed algebra/control/review budget, alternatives and return point.
No such all-frame theorem is claimed or successor authorized by this return.''',1)
s=s.replace('includes51 later returns/clarifications','includes52 later returns/clarifications',1)
review='''IEC1 uses two fresh separate source-first/exposed/final reviewer contexts. Each
independently constructed a tilted spherical control before candidate exposure;
their measured sheets and principal parameters coincide, so these are not two
complementary class surveys. The parent derives the general formula by local
symmetric-space algebra and replays its associative word identity. The reviewed
signature-independent Jacobi/transvection proof, actual later-return derivatives,
independent full-interval/control comparisons and hand quartic audit support the
result at its stated scope. Shared model/libraries/methods remain explicit;
no physical or empirical acceptance is implied. Initial candidates and proof
completion are preserved. [IEC1 work record](udt_invariant_echo_curvature_2026-10-03/WORK_RECORD.md)
and [descendant review](udt_invariant_echo_curvature_2026-10-03/DESCENDANT_REVIEW.md)
retain discovery, execution, omissions and positive/negative changes. Actual
final attestations and required-check receipts own closure status.

'''
s=s.replace('The preserved first candidates expose the repair history.',review+'The preserved first candidates expose the repair history.',1)
p.write_text(s);Path('CURRENT_RESEARCH_PROGRAM.md').write_text(verify.program_text(s))
for filename,start,end,title in [('LIVE.md','## CURRENT STATE','### Honest claim','CURRENT STATE'),('HANDOFF.md','## Current handoff','Protected payloads require explicit dispatch;','Current handoff')]:
 p=Path(filename);s=p.read_text();a=s.index(start);z=s.index(end,a)
 current=f'''## {title} — IEC1 invariant echo-curvature return, 2026-10-03

CDR1 remains the central-development architecture; exact grades stay in
CURRENT_SCIENTIFIC_PREMISES.tsv. LIVE.md owns status. Verify grok HEAD, remote,
dirt and actual host state. Charles authorized pursuit of FCW1's first lead,
including bounded derivation, checks, fresh separate review, same-premise repair,
central integration and lay return. Fixed evidence is under
`udt_invariant_echo_curvature_2026-10-03/`; UDT_DEVELOPMENT.md R8IEC/R18 owns
the maintained argument; CURRENT_RESEARCH_PROGRAM.md is its generated startup
excerpt. No physical premise, equation, scale, registry grade
or CANON adoption is made. FC/RG remain UNADOPTED.

The conditional derivation and two fresh source-first/exposed reviews are saved.
Actual control receipts, final attestations and normal/maintenance/full406
receipts own completion/pass status. No GPU, empirical fit, hardware experiment
or paused source/carrier campaign is part of IEC1. No-timeout direction persists
with finite/resource/manual stops. Preserve protected payloads and unrelated work.

Next: Stop for lay discussion of IEC1. Its decision brief proposes a bounded
all-frame scalar-rule selectivity test; this is not an automatic successor or
physical FC adoption. Completion/protocol robustness is still a separate option.
A clock anomaly is not the project objective. Later sessions verify actual
processes. Bindings remain in development_reconstruction_2026-09-29.
TPS1 raw fields/large streams remain local-only; remote compact records cannot
replay raw-dependent checks. IEC1 evidence is banked only when actual commit/push
and exact-byte checks have completed.

'''
 s=s[:a]+current+s[z:]
 if filename=='LIVE.md':
  a=s.index('### Next gate');z=s.index('<!-- STARTUP_CURRENT_END -->',a)
  s=s[:a]+'''### Next gate

Stop for lay discussion of IEC1 using central R8IEC/R18 and its decision brief.
Native geometry/response and positional attribution remain open. No automatic
successor, physical premise adoption, GPU/data campaign or hardware experiment.
Existing pauses/protected boundaries remain; verify actual processes before
claiming host state.

'''+s[z:]
 p.write_text(s)
g=json.loads((W/'DEVELOPMENT_GRAPH.json').read_text());assert len(g['nodes'])==114
sources=[str(B/f) for f in ['INITIAL_CANDIDATE.md','DERIVATION_COMPLETION.md','UNIVERSAL_FORMAL_RESULT.json','DIRECTION_COROLLARY.md','REVIEWED_RESULT.md']]
for f in sources:g['sources_sha256'][f]=sha(f)
lookup={n['id']:n for n in g['nodes']}
for key in ['R8','R18','R8ECS','R8ECSM','R8FCW','O_PSW_ATTRIBUTION','O_FCW_ADMISSION']:
 lookup[key]['sources'].append(str(B/'REVIEWED_RESULT.md'))
lookup['O_FCW_ADMISSION']['statement']='Physical justification/adoption of FC or RG, all-frame rigidity, generic completion/protocol robustness and native geometry/scale remain OPEN. IEC1 now supplies the invariant echo expansion through L6 within supplied locally symmetric Lorentz4 metrics; generic variable-curvature extension is open. No successor starts automatically.'
lookup['O_PSW_ATTRIBUTION']['statement']+=' IEC1 curvature contractions interpret net prepared echoes within a supplied locally symmetric class; they do not assign a positional component or DDR response.'
g['nodes'].append(dict(id='C_IEC_LOCAL_SYMMETRY',kind='conditional_protocol',statement='Supplied smooth time-oriented Lorentz4 metric with covariantly constant Riemann tensor, PSW parallel-prepared ordinary unit free clocks, fixed event/frame, positive small proper separation and actual regular first/future-return null branches in a common normal tube. Local symmetry and scalar sufficiency FC are not derived physical premises.',sources=sources,registry_ids=[]))
g['nodes'].append(dict(id='R8IEC',kind='argument',anchor='r8iec',title='Invariant prepared-echo expansion through sixth order in locally symmetric geometry',sources=sources,registry_ids=[],required_conditions=['C_IEC_LOCAL_SYMMETRY']))
for a,b,k in [('C_IEC_LOCAL_SYMMETRY','R8IEC','hypothesis'),('R6','R8IEC','proof'),('R8ECS','R8IEC','context'),('R8FCW','R8IEC','context'),('R8ECSM','R8IEC','context'),('R8IEC','R18','context'),('O_FCW_ADMISSION','R8IEC','open_boundary'),('O_PSW_ATTRIBUTION','R8IEC','open_boundary')]:
 assert a in {n['id'] for n in g['nodes']},a
 g['edges'].append({'from':a,'to':b,'kind':k})
targets=['R7','R8','R9','R16','R17','R18','R8ECS','R8ECSM','R8FCW','R16FCW','R8IEC','O_PSW_ATTRIBUTION','O_FCW_ADMISSION']
for rel in ['review_math/EXPOSED_REVIEW.md','review_math/COMPLETION_REVIEW.md','review_math/HAND_QUARTIC_AUDIT.md','review_fidelity/EXPOSED_REVIEW.md','review_fidelity/COMPLETION_REVIEW.md','review_fidelity/DIRECTION_REVIEW.md','DESCENDANT_REVIEW.md']:
 f=str(B/rel);g['review_support'].append(dict(path=f,sha256=sha(f),role='review_evidence',targets=targets))
(W/'DEVELOPMENT_GRAPH.json').write_text(json.dumps(g,indent=2)+'\n')
p=W/'RECENT_DISPOSITIONS.tsv';rows=list(csv.DictReader(p.open(),delimiter='\t'));assert len(rows)==51
row=dict(id='IEC1_RETURN',source=str(B/'REVIEWED_RESULT.md'),current_scope='VERIFIED-WITH-CAVEATS_CONDITIONAL_GEOMETRIC_DERIVATION; supplied locally symmetric Lorentz4 echo d4/d6 invariants, V0 sixth-order and opposite-direction corollaries; no FC adoption/native selection',central_location='R7;R8;R9;R16;R17;R18;R8ECS;R8ECSM;R8FCW;R16FCW;R8IEC',rederivation_depth='LOCAL_JACOBI_TRANSVECTION_PROOF_AND_EXACT_WORD_CURVATURE_ALGEBRA; true first/return null derivatives, analytic remainder, original product/plane-wave controls and fresh source-first/exposed review; no general classification',source_sha256=sha(B/'REVIEWED_RESULT.md'))
with p.open('a',newline='') as f:csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n').writerow(row)
print(json.dumps(dict(nodes=len(g['nodes']),edges=len(g['edges']),sources=len(g['sources_sha256']),review_support=len(g['review_support']),later_returns=52)))
