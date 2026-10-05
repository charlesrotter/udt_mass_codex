"""One-time FRI1 central integration with unchanged inherited grades."""
from pathlib import Path
import json,csv,hashlib,sys
sys.path.insert(0,str(Path.cwd()))
import verify_udt_development as guard
B=Path('udt_finite_record_scale_test_2026-10-05');W=Path('development_reconstruction_2026-09-29')
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
p=Path('UDT_DEVELOPMENT.md');t=p.read_text();assert '<a id="r16fri"></a>' not in t
def replace(old,new):
    global t
    assert t.count(old)==1,old
    t=t.replace(old,new,1)
replace('**Current development — TSI1 conditional timing/scale identification reviewed,','**Current development — FRI1 finite-record scale bounds and ambiguity reviewed,')
a=t.index('**Current learning.**');z=t.index('<!-- DEVELOPMENT_ORIENTATION_END -->',a)
t=t[:a]+'''**Current learning.** FRI1 moves the conditional scale question to finite
records. Exact bounds on the actual clock history give a finite H enclosure
with explicit source drift, measurement and timestamp uncertainty. Frozen
longer-record controls yield total interval widths about1.902% of the input H,
including a receiver-energy change. These are deterministic conditional bounds,
not observational error bars or an adopted geometry.

The shorter record has a proved factor2 ambiguity: two different scales can
match the same finite timing AND angular means within the declared errors,
even with stable sources. They are compared at the same calibrated times.
This is not equality of noiseless curves or a no-go for every finite record.

The supplied shape/tail domain is scale invariant and does not give a known
source ruler. Its physical admission, finite readout errors, source drift and
angular reference remain explicit conditions. c_E converts clock data to length;
G_obs has no newly derived independent mass/density interface. Matched GR gives
the same records; native geometry/comparison selection and X_max remain open.

Parent exact-rational/finite controls and two actual fresh contexts support
the argument and independently replay saved incidences and uncertainty bounds.
Formula exposure, reused parent evaluator and shared-model/library limits are
recorded. Final semantic/hash bindings and required checks own closure.

After orientation read R16FRI/R18, with R16TSI and R8CPR as dependencies.
The proposed next bounded step is to audit independent physical support for
the shape/tail, source-drift and finite-readout conditions before claiming an
empirical scale. Stop for lay discussion; no automatic successor, data fit,
new physical premise, large solve or parked/protected program restart.
'''+t[z:]
replace('<a id="r16fcw"></a>',(B/'CENTRAL_INSERT.md').read_text()+'\n\n<a id="r16fcw"></a>')
replace('R16TSI supplies a conditional timing-to-scale interface, distinct from such\nan actual measurement or a new native metric selection. A',
'''R16TSI supplies a conditional timing-to-scale interface and R16FRI adds a
finite uncertainty test; neither is an actual astronomical measurement or new
native metric selection. A''')
replace('supplies an ideal timing route to scale without a known source ruler; finite\nsource reduction, actual usable data and native metric/comparison selection',
'''supplies an ideal timing route to scale without a known source ruler, and
R16FRI adds finite conditional error bounds. Finite source reduction, actual
usable data and native metric/comparison selection''')
replace('route without a known ruler; an actual usable timing record remains unsupplied.',
'''route without a known ruler; FRI1 adds finite conditional uncertainty control.
An actual astronomical timing record and physical error admission remain unsupplied.''')
replace('Finite practical inversion, empirical source admission and native geometry\nselection remain separate gates. The [return brief](udt_timing_scale_identifiability_2026-10-05/DECISION_BRIEF.md)\nstates the next bounded proposal without launching it.',
'''FRI1 below now supplies finite conditional inversion and a finite-error
ambiguity witness. Empirical source/error admission and native geometry selection
remain separate gates. The [fixed TSI1 return](udt_timing_scale_identifiability_2026-10-05/DECISION_BRIEF.md)
preserves the earlier proposed scope without becoming current authorization.''')
a=t.index('TSI1 in R16TSI now distinguishes calibrated timing from untimed records.');z=t.index("NGD1's numerical return",a)
t=t[:a]+'''TSI1 in R16TSI distinguishes calibrated timing from untimed records.
FRI1 now supplies a finite uncertainty enclosure in a stated scale-invariant
shape/tail class. Its longer synthetic record narrows H to about a1.902%-wide
range, while a short finite timing-and-angle record provably admits two scales
differing by2. These are compatible conditional conclusions, not a universal
identifiability or non-identifiability theorem.

The remaining practical gate is independent physical admission of the shape/
tail, source-frequency bound and finite-window readout errors. They were supplied
conditions, not established from these records or from a native matter/light law.
The [fixed FRI1 return and proposed scope](udt_finite_record_scale_test_2026-10-05/DECISION_BRIEF.md)
proposes a bounded interface audit before empirical inference. Native metric/
comparison selection remains separate; matched GR gives the same records.
Stop for lay discussion; no automatic successor, fit, larger solve or protected
work restart.

'''+t[z:]
marker='The preserved first candidates expose the repair history.'
replace(marker,'''FRI1's two actual fresh contexts derive and challenge finite-window uncertainty
bounds and independently replay the actual records, including receiver-time
scheduling and finite error certificates. Its [work record](udt_finite_record_scale_test_2026-10-05/WORK_RECORD.md)
discloses source-first leads, parent evaluator reuse and shared-model/library
limits. The [descendant review](udt_finite_record_scale_test_2026-10-05/DESCENDANT_REVIEW.md)
updates both the positive finite calibration and the adverse short-record
ambiguity without extending either to native selection or real instruments.

'''+marker)
p.write_text(t);Path('CURRENT_RESEARCH_PROGRAM.md').write_text(guard.program_text(t))
common='''CDR1 remains the central-development architecture. UDT_DEVELOPMENT.md is the
sole maintained scientific argument; CURRENT_SCIENTIFIC_PREMISES.tsv and reviewed
sources own exact grades. CURRENT_RESEARCH_PROGRAM.md is its generated bounded
orientation. After orientation read R16FRI/R18, with R16TSI/R8CPR as needed.

After TSI1 at37c08648, Charles explicitly authorized finite timing/angular
records with uncertainty, seeking scale recovery or demonstrable ambiguity.
FRI1 evidence is in udt_finite_record_scale_test_2026-10-05/; WORK_ORDER owns
scope/stops. Two fresh source-first/exposed/final contexts reconstruct the
argument and recompute saved quantities. Exposure and evaluator reuse are
recorded. Actual final attestations, normal/maintenance/full406 receipts and
committed/remote byte checks own closure. Verify HEAD, remote and dirt yourself.

Next: Stop for lay discussion of FRI1. R18 and DECISION_BRIEF distinguish
finite conditional bounds/ambiguity from independent physical source/error
admission and native selection. A bounded interface audit is proposed for
subsequent authorization. No new physical premise, response law, registry grade
or X_max is adopted. No GPU/long production or parked/protected program restart.
Standing pauses, preservation, no-timeout/manual-stop and resource rules persist.

'''
for name,title,tail in [('LIVE.md','## CURRENT STATE — FRI1 finite-record return, 2026-10-05','### Honest claim'),('HANDOFF.md','## Current handoff — FRI1 finite-record return, 2026-10-05','Protected payloads require explicit dispatch; preserve without inspecting/hashing:')]:
    p=Path(name);s=p.read_text();a=s.index('## CURRENT STATE') if name=='LIVE.md' else s.index('## Current handoff');z=s.index(tail)
    s=s[:a]+title+'\n\n'+common+s[z:]
    if name=='LIVE.md':
        a=s.index('Use central R16TSI/R18');z=s.index('\n<!-- STARTUP_CURRENT_END -->',a)
        s=s[:a]+'''Use central R16FRI/R18 and FRI1's decision brief for finite conditional scale
bounds/ambiguity and the physical-interface gate. Native response/metric and
empirical admission remain open. Verify final review, required checks and
banking evidence. Pauses/protected boundaries persist;
TPS1 raw fields/large streams remain local-only, not remotely replayable.
'''+s[z:]
    p.write_text(s)
p=W/'DEVELOPMENT_GRAPH.json';g=json.loads(p.read_text())
sources=[str(B/x) for x in ['WORK_ORDER.md','INITIAL_CANDIDATE.md','CONSTRUCTION_RESULT.json','check_finite_records.py','CANDIDATE_FREEZE.json','NUMERICAL_FREEZE.md','CLARIFICATIONS.md']]
g['nodes'].extend([
dict(id='C_FRI_SHAPE',kind='conditional_protocol',statement='Inherited principal CPR/TSI branch in supplied scale-invariant mu,A,E,y domain, whole finite-window support hull admitted. H free; tail membership not inferred from records. No all-image uniqueness.',sources=sources,registry_ids=[]),
dict(id='C_FRI_RECORD',kind='conditional_protocol',statement='Finite equal-width translated log-frequency and arithmetic-angle means, deterministic readout and timestamp bounds, receiver-time source drift bound, fixed parallel angular frame. Conditional interfaces, not derived instrument/source laws.',sources=sources,registry_ids=[]),
dict(id='O_FRI_ADMISSION',kind='open_join',statement='Independent physical shape/tail/source/error admission and native metric/comparison selection remain open. No empirical accuracy, physical mass, X_max, Hubble identification or extra matched-GR effect.',sources=sources[:2],registry_ids=[]),
dict(id='R16FRI',kind='argument',anchor='r16fri',title='Finite scale enclosure and factor-two same-time uncertainty witness',sources=sources,registry_ids=[],required_conditions=['C_FRI_SHAPE','C_FRI_RECORD'])])
for x in ['R8CPR','R16TSI','R16']:g['edges'].append({'from':x,'to':'R16FRI','kind':'proof'})
for x in ['C_FRI_SHAPE','C_FRI_RECORD']:g['edges'].append({'from':x,'to':'R16FRI','kind':'hypothesis'})
targets=['D1','R2','R6','R7','R8','R8CGE','R8CPR','R8OAA','R8ACP','R9','R10','R13','R13OJM','R14','R15','R16','R16TSI','R17','R18','R16FRI','C_FRI_SHAPE','C_FRI_RECORD','O_FRI_ADMISSION']
for x in targets[:19]:
    if x not in ['R8CPR','R16TSI','R16','R18']:g['edges'].append({'from':x,'to':'R16FRI','kind':'context'})
g['edges'].extend([{'from':'O_FRI_ADMISSION','to':'R16FRI','kind':'open_boundary'},{'from':'R16FRI','to':'R18','kind':'context'}])
for x in sources:g['sources_sha256'][x]=h(x)
for x in ['WORK_RECORD.md','DESCENDANT_REVIEW.md','review_math/SOURCE_FIRST.md','review_math/SHAPE_DOMAIN_REVIEW.md','review_math/EXPOSED_REVIEW.md','review_math/SAVED_REPLAY_REVIEW.md','review_fidelity/SOURCE_FIRST.md','review_fidelity/INDEPENDENT_REVIEW.md','review_fidelity/EXPOSED_REVIEW.md']:
    x=str(B/x);g['review_support'].append({'path':x,'sha256':h(x),'role':'review_evidence','targets':targets})
p.write_text(json.dumps(g,indent=2)+'\n')
row=['FRI1_RETURN',str(B/'INITIAL_CANDIDATE.md'),'VERIFIED-WITH-CAVEATS_CONDITIONAL_FINITE_RECORD_SCALE_BOUNDS_AND_AMBIGUITY; physical source/error and native admission OPEN',';'.join(targets),'SOURCE_FIRST_EXPOSED_FINAL_REVIEW; exact rational continuum bounds, actual same-time histories and independent finite-window/error replays; no empirical precision',h(B/'INITIAL_CANDIDATE.md')]
with (W/'RECENT_DISPOSITIONS.tsv').open('a',newline='') as f:csv.writer(f,delimiter='\t',lineterminator='\n').writerow(row)
print(json.dumps({'nodes':len(g['nodes']),'edges':len(g['edges']),'source_pins':len(g['sources_sha256']),'orientation_words':len(guard.orientation(t).split())}))
