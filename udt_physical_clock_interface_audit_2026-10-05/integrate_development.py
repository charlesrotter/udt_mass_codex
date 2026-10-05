"""One-time PIA1 integration; unchanged inherited premises and source grades."""
from pathlib import Path
import json,csv,hashlib,sys
sys.path.insert(0,str(Path.cwd()))
import verify_udt_development as guard
B=Path('udt_physical_clock_interface_audit_2026-10-05');W=Path('development_reconstruction_2026-09-29')
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
p=Path('UDT_DEVELOPMENT.md');t=p.read_text();assert '<a id="r16pia"></a>' not in t
def replace(old,new):
    global t
    assert t.count(old)==1,old
    t=t.replace(old,new,1)
replace('**Current development — FRI1 finite-record scale bounds and ambiguity reviewed,','**Current development — PIA1 physical clock/source interface audited,')
a=t.index('**Current learning.**');z=t.index('<!-- DEVELOPMENT_ORIENTATION_END -->',a)
t=t[:a]+'''**Current learning.** PIA1 independently audits whether real clock/source
protocols justify FRI1's observing regime and error bounds. Its supplied tail
requires a TOTAL paired-clock ratio Z>54180, alongside particular source/
receiver preparation. No complete physical admission is supplied by the three
reviewed protocol classes: engineered atomic links, pulsar timing, or resolved
megamaser monitoring. This is a scoped missing interface, not a no-go for UDT
or every possible finite experiment.

FRI1's finite H enclosure and short-record factor2 ambiguity survive under
their original conditions. The longer synthetic interval's1.902% total width
is not an experimental precision forecast. Precise clocks alone do not admit
the geometry. Published source/model/frame reductions and statistical errors
cannot silently replace actual clock ratios or all-time deterministic bounds.

PIA1 derives a finite mean-frequency/mean-log conversion bound, retains source
and receiver calibration separately, and explains how a justified JOINT error
model could supply conditional coverage. No such physical model is adopted.
c_E converts calibrated time; G_obs supplies no new mass interface. Matched GR
still gives the same records; native geometry/comparison selection and X_max
remain open.

Two actual fresh source-first/exposed/final contexts check the algebra and
saved arithmetic; the fidelity reviewer also checks the five primary sources.
Shared model and exposure limits, initial candidate and review clarifications
are retained. Exact final bindings and required checks own closure.

After orientation read R16PIA/R18, with R16FRI/R16TSI and R8ACP as dependencies.
The proposed next bounded step is to test a specified moderate-ratio protocol
for applicability and scale sensitivity or explicit ambiguity in the same
conditional metric. The tail certificate does not transfer. Stop for lay
discussion; no automatic successor, data fit, new physical premise, large solve
or parked/protected program restart.
'''+t[z:]
replace('<a id="r16fcw"></a>',(B/'CENTRAL_INSERT.md').read_text()+'\n\n<a id="r16fcw"></a>')
replace('proposes checking those physical interfaces before claiming empirical scale.',
'''preserves the earlier proposal. R16PIA below now audits those physical
interfaces and finds a concrete missing admission, without changing this
conditional enclosure or the adverse finite-record witness.''')
a=t.index('The remaining practical gate is independent physical admission of the shape/');z=t.index("NGD1's numerical return",a)
t=t[:a]+'''PIA1 in R16PIA now audits that practical gate. The conditional class requires
total Z>54180; no complete independent shape/tail/source/frame/error admission
is supplied by the three reviewed physical protocols. FRI1's positive enclosure
and negative short-record witness survive, but the synthetic1.902% width is
not an instrument forecast. An independently valid actual-Z bound could reject
this class; reduced astronomical proxies do not establish that test directly.

The [PIA1 return and proposed scope](udt_physical_clock_interface_audit_2026-10-05/DECISION_BRIEF.md)
recommends examining a specified moderate-ratio protocol in the same conditional
metric, deriving applicable readouts and sensitivity or an explicit ambiguity.
The extreme-tail error certificate cannot be transplanted. Native metric/
comparison selection is separate; matched GR still gives the same records.
Stop for lay discussion; no automatic successor, fit, larger solve, new
source law or protected/parked restart.

'''+t[z:]
marker='The preserved first candidates expose the repair history.'
replace(marker,'''PIA1 adds two actual fresh contexts with independent arithmetic/argument
checks and an independent primary-source methods audit. Its
[work record](udt_physical_clock_interface_audit_2026-10-05/WORK_RECORD.md)
distinguishes same-model review from physical instrument validation. The
[source-preserving repair](udt_physical_clock_interface_audit_2026-10-05/REVIEW_REPAIR.md)
clarifies conditional coverage, base-history schedules, total-Z admission and
actual instrument weighting. No FRI1 equation or registry grade changes.

'''+marker)
p.write_text(t);Path('CURRENT_RESEARCH_PROGRAM.md').write_text(guard.program_text(t))
common='''CDR1 remains the central-development architecture. UDT_DEVELOPMENT.md is the
sole maintained scientific argument; CURRENT_SCIENTIFIC_PREMISES.tsv and reviewed
sources own exact grades. CURRENT_RESEARCH_PROGRAM.md is its generated bounded
orientation. After orientation read R16PIA/R18, with R16FRI/R16TSI/R8ACP as needed.

After FRI1 at0c5386a6, Charles authorized an independent physical clock/source
audit of the observation regime and uncertainty bounds. PIA1 evidence is in
udt_physical_clock_interface_audit_2026-10-05/; WORK_ORDER owns scope/stops.
Two fresh source-first/exposed/final contexts audit arguments and saved arithmetic;
primary-source verification and exposure are recorded. Actual final attestations,
normal/maintenance/full406 receipts and committed/remote byte checks own closure.
Verify actual HEAD, remote and dirt yourself.

Next: Stop for lay discussion of PIA1's scoped missing physical interface.
R18 and DECISION_BRIEF propose a subsequent bounded moderate-regime applicability/
ambiguity test. No automatic successor, physical premise, source law, registry
grade, empirical fit or X_max adoption. No GPU/long production or parked/
protected program restart. Standing preservation, no-timeout/manual-stop and
resource rules persist.

'''
for name,title,tail in [('LIVE.md','## CURRENT STATE — PIA1 physical-interface return, 2026-10-05','### Honest claim'),('HANDOFF.md','## Current handoff — PIA1 physical-interface return, 2026-10-05','Protected payloads require explicit dispatch; preserve without inspecting/hashing:')]:
    p=Path(name);s=p.read_text();a=s.index('## CURRENT STATE') if name=='LIVE.md' else s.index('## Current handoff');z=s.index(tail)
    s=s[:a]+title+'\n\n'+common+s[z:]
    if name=='LIVE.md':
        a=s.index('Use central R16FRI/R18');z=s.index('\n<!-- STARTUP_CURRENT_END -->',a)
        s=s[:a]+'''Use central R16PIA/R18 and PIA1's decision brief for the physical-interface
audit and proposed bounded successor. FRI1 remains a conditional tool; physical
admission and native selection remain open. Verify actual final review, required
checks and banking evidence. Pauses/protected boundaries persist;
TPS1 raw fields/large streams remain local-only, not remotely replayable.
'''+s[z:]
    p.write_text(s)
p=W/'DEVELOPMENT_GRAPH.json';g=json.loads(p.read_text())
sources=[str(B/x) for x in ['WORK_ORDER.md','INITIAL_CANDIDATE.md','REVIEW_REPAIR.md','CLARIFICATIONS.md','SOURCES.md','CONSTRUCTION_RESULT.json','check_interfaces.py','CANDIDATE_FREEZE.json','NUMERICAL_FREEZE.md']]
g['nodes'].extend([
dict(id='O_PIA_ADMISSION',kind='open_join',statement='Independent physical extreme-tail/preparation/source/frame/readout admission remains missing for the three reviewed protocols. Statistical precision is not deterministic hull coverage. No empirical exclusion or all-experiment no-go.',sources=sources[:5],registry_ids=[]),
dict(id='R16PIA',kind='argument',anchor='r16pia',title='Physical clock/source regime and uncertainty audit',sources=sources,registry_ids=[],required_conditions=['C_FRI_SHAPE','C_FRI_RECORD'])])
g['edges'].append({'from':'R16FRI','to':'R16PIA','kind':'proof'})
for x in ['C_FRI_SHAPE','C_FRI_RECORD']:g['edges'].append({'from':x,'to':'R16PIA','kind':'hypothesis'})
targets=['D1','R6','R7','R8','R8CPR','R8ACP','R8OAA','R13','R13OJM','R16','R16TSI','R16FRI','R17','R18','R16PIA','O_FRI_ADMISSION','O_PIA_ADMISSION']
for x in targets[:14]:
    if x not in ['R16FRI','R18']:g['edges'].append({'from':x,'to':'R16PIA','kind':'context'})
g['edges'].extend([{'from':'O_PIA_ADMISSION','to':'R16PIA','kind':'open_boundary'},{'from':'R16PIA','to':'R18','kind':'context'}])
for x in sources:g['sources_sha256'][x]=h(x)
for x in ['WORK_RECORD.md','DESCENDANT_REVIEW.md','review_math/SOURCE_FIRST_REVIEW.md','review_math/EXPOSED_REVIEW.md','review_math/REPAIR_REVIEW.md','review_fidelity/SOURCE_FIRST.md','review_fidelity/EXPOSED_REVIEW.md']:
    x=str(B/x);g['review_support'].append({'path':x,'sha256':h(x),'role':'review_evidence','targets':targets})
p.write_text(json.dumps(g,indent=2)+'\n')
row=['PIA1_RETURN',str(B/'INITIAL_CANDIDATE.md'),'VERIFIED-WITH-CAVEATS_CONDITIONAL_PHYSICAL_INTERFACE_AUDIT; source/error/domain admission and native selection OPEN',';'.join(targets),'SOURCE_FIRST_EXPOSED_FINAL_REVIEW; conditional regime/readout bounds and five primary-source method checks; no empirical exclusion/instrument validation',h(B/'INITIAL_CANDIDATE.md')]
with (W/'RECENT_DISPOSITIONS.tsv').open('a',newline='') as f:csv.writer(f,delimiter='\t',lineterminator='\n').writerow(row)
print(json.dumps({'nodes':len(g['nodes']),'edges':len(g['edges']),'source_pins':len(g['sources_sha256']),'orientation_words':len(guard.orientation(t).split())}))
