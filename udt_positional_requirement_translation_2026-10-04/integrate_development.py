"""One-time PRT1 source-preserving central integration; not a science selector."""
from pathlib import Path
import csv,hashlib,json,sys
sys.path.insert(0,str(Path.cwd()))
import verify_udt_development as guard
B=Path('udt_positional_requirement_translation_2026-10-04')
W=Path('development_reconstruction_2026-09-29')
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
p=Path('UDT_DEVELOPMENT.md');t=p.read_text()
assert '<a id="r8prt"></a>' not in t
old='**Current development — GRL1 bounded GR connection review completed,'
assert t.count(old)==1;t=t.replace(old,'**Current development — PRT1 positional translation and step4/5 handoff reviewed,',1)
a=t.index('**Current learning.**');z=t.index('<!-- DEVELOPMENT_ORIENTATION_END -->',a)
t=t[:a]+'''**Current learning.** Charles authorized an existing comparison, faithful
translation of the positional requirement and derivation of its restrictions,
then a handoff to observations and numerics. PRT1 returns a reviewed conditional
formulation; the native positional assignment remains OPEN.

The chosen experiment uses properly separated, parallel-prepared free clocks
and two independent first signals. Its ordinary query data need no universal
population law. Free preparation removes initial velocity mismatch and proper
acceleration but does not remove ordinary curvature or isolate a positional
component. Net positivity and a selected reference contrast therefore remain
explicit alternative conditional assignments, not derived physical laws.

Strict finite slowing can imply only a weak local tidal sign; its quadratic
coefficient may vanish. Same sign across laboratories is weaker than PCC's
identical coefficient. A supplied existing control satisfies the weaker
all-frame signs in a stated region without being an Einstein metric. Another
existing control has zero initial curvature, cubic clock onset and a divergent
first-reception ratio at a finite limiting preparation distance, while future
local curvature stays regular. The new future-domain calculation is conditional;
its scale, limit and power are not native X_max or an adopted cosmology.

These checks prevent selecting a quadratic onset, constant-curvature form or
asymptotic exponent from qualitative slowing alone. They preserve the founding
requirement and old positive/negative results without proving that the full
postulates are insufficient or a new premise is necessary. No response, physical
reference, field equation, population or scale is selected.

The concrete next handoff is step4A: a bounded observation-to-comparison table
for at most three channels, with actual readouts, independent distance, source/
observer histories, uncertainty and prior exposure. Then freeze one candidate
analysis before inspecting new confirmation outcomes. Supplied-metric clock/
ray/transport evaluation in step5A can proceed independently under its own
work order. Broader step5B needs declared equations/conditional constraints,
domains and actual-workload smoke/load/restart gates; it is not a complete
native-space survey. No stage4/5 campaign runs in this return.

After orientation read R8PRT and R18, with PSW/FPC/PCC/ACI/GRL as load-bearing.
Two fresh reviewer contexts hand-checked the arguments and actual controls,
then reviewed precision and handoff. Initial candidates and wording corrections
remain preserved. Shared model/source exposure is disclosed; no scientific
program, human, different-model, formal or empirical review is claimed. Actual
final attestations and normal/maintenance/full406 receipts own closure. The
recommended next task is the bounded step4A interface audit, not an automatic
startup dispatch or physical adoption.
'''+t[z:]
marker='#### Finite mutual ticking and its causal limits — FPC1'
assert t.count(marker)==1;t=t.replace(marker,(B/'CENTRAL_INSERT.md').read_text()+'\n\n'+marker,1)
old="select nature's metric. R18 owns the return for discussion."
new="""select nature's metric. Charles's subsequent PRT1 task below tests a precise
translation and supplies the next-stage handoff; R18 owns the current return."""
assert t.count(old)==1;t=t.replace(old,new,1)
a=t.index("[GRL1's decision brief]");z=t.index("\n\nNGD1's numerical return",a)
t=t[:a]+'''The [fixed GRL1 return](udt_gr_physical_connection_review_2026-10-04/DECISION_BRIEF.md)
retains that distinction. Charles then authorized PRT1's steps1–3 and a clear
handoff to4/5. R8PRT now specifies the existing prepared free-clock experiment,
separates its net and matched-contrast readings from the required additional
effect, and derives conditional weak tidal inequalities. Its non-Einstein
positive-sign control preserves the distinction from PCC's equal-coefficient
trial. The old cubic control's newly checked future domain allows zero initial
quadratic term and a distant first-reception asymptote with bounded future local
curvature. These supplied controls do not select a native UDT geometry.

[PRT1's decision brief](udt_positional_requirement_translation_2026-10-04/DECISION_BRIEF.md)
owns the current lay return. The native positional assignment remains open;
steps1–3 return a precise conditional chain rather than a closed physical law.
No whole-postulate insufficiency or new-postulate necessity is inferred. Existing
mathematical tools and their adverse examples keep their source grades/domains.

The recommended next bounded task is step4A's observation-to-comparison map,
specified in the [step4/5 handoff](udt_positional_requirement_translation_2026-10-04/STEPS_4_5_HANDOFF.md)
with [controlling precision](udt_positional_requirement_translation_2026-10-04/PRECISION.md).
For at most three channels identify actual observed ratios, independent distance,
source/observer histories, readout/flux assumptions, errors/covariance, selection
and prior exposure. Then propose one frozen candidate analysis. This design work
can begin before native dynamics is closed; a missing protocol bridge limits its
inference, not all observational planning. Native positional attribution still
cannot be inferred merely from a positive measured net shift.

Step5A may independently evaluate clock/null/transport queries on a supplied
geometry with original residual and incidence checks. Step5B needs a declared
equation/constraint class and domains/data; observation constraints alone do not
provide native evolution. The actual workload needs smoke/load/restart/stop
checks before long production. No generic fitted response, preferred power-law
onset/asymptote, complete native census or automatic old-GPU-campaign restart is
authorized by this handoff. This task ends with the reviewed handoff; actual
stage4/5 execution proceeds under its bounded work order.
'''+t[z:]
marker='The preserved first candidates expose the repair history.'
addition='''PRT1 uses two fresh source-first/exposed/final contexts, with old owner/proof/
verdict exposure disclosed. Parent froze its new candidate before reading either
new reviewer's substantive findings. Both reviewers independently hand-derived
the original metric curvature, Lorentz-frame contractions, reverse preparation,
actual arrival derivative, conformal integral/tail and first/echo branch limits.
No scientific program ran. The local sign inference mainly reuses PSW/FPC/PCC;
the future cubic control analysis is newly scoped work on the old supplied
example, not native admission. Precision clarifies Ric(D) as a tensor, the
unquotiented future domain and independent availability of supplied-metric
evaluation. The concrete handoff was written after source-first review; its
contrast-tail caution is credited. Both reviewers caught wording that appeared
to freeze confirmation outcomes; the corrected text freezes analysis choices
before inspecting outcomes. Its first edition and actual correction are retained,
and the next task is explicitly recommended under a bounded work order.
[Work record](udt_positional_requirement_translation_2026-10-04/WORK_RECORD.md) and
[descendant review](udt_positional_requirement_translation_2026-10-04/DESCENDANT_REVIEW.md)
record positive/negative scope and omissions. No human, different-model, formal,
independent-code, empirical or full-corpus scientific review is claimed. Actual
final accepted-map attestations and required captured checks own closure; neither
review nor commit supplies the open physical assignment or adopts physics.

'''
assert t.count(marker)==1;t=t.replace(marker,addition+marker,1)
p.write_text(t);Path('CURRENT_RESEARCH_PROGRAM.md').write_text(guard.program_text(t))

common='''CDR1 remains the central-development architecture. UDT_DEVELOPMENT.md is the
sole maintained scientific argument; CURRENT_SCIENTIFIC_PREMISES.tsv and reviewed
sources own exact grades. The generated CURRENT_RESEARCH_PROGRAM.md is the bounded
startup orientation. Read R8PRT and R18 after orientation; older chapters only
when made load-bearing by the task.

After GRL1 at c641bf5a, Charles authorized steps1–3 and a clear handoff to4/5.
PRT1 evidence is in udt_positional_requirement_translation_2026-10-04/;
WORK_ORDER owns this bounded scope. Two fresh source-first/exposed/final contexts
reviewed the conditional translation, two analytic tests and executable handoff.
Original candidate, scientific precision and corrected handoff wording retain
their actual review history. Final attestations and normal/maintenance/full406
receipts own closure; commit/push and byte checks own banking. Verify actual
HEAD, remote, dirt and processes rather than treating this text as the tip.

Next: Stop for lay discussion of the reviewed steps1–3 and the step4/5 handoff.
The recommended step4A task is a bounded observation-to-comparison map, then a proposed
frozen analysis; STEPS_4_5_HANDOFF and PRECISION in PRT1 own the fixed details.
Supplied-metric step5A evaluation can proceed independently under its own bounded
work order. Broader5B needs declared equations/constraints and workload gates.
Current work ends with the reviewed handoff. No stage4/5 analysis or production
run has started; no new physical premise, registry promotion or automatic
campaign restart is supplied by a startup pointer. Standing pauses, no-timeout/
resource/manual-stop rules and protection of unrelated work persist.

'''
for name,title,tail in [('LIVE.md','## CURRENT STATE — PRT1 steps1–3 return and step4/5 handoff, 2026-10-04','### Honest claim'),('HANDOFF.md','## Current handoff — PRT1 steps1–3 return and step4/5 handoff, 2026-10-04','Protected payloads require explicit dispatch; preserve without inspecting/hashing:')]:
    p=Path(name);q=p.read_text();a=q.index('## CURRENT STATE') if name=='LIVE.md' else q.index('## Current handoff');z=q.index(tail)
    q=q[:a]+title+'\n\n'+common+q[z:]
    if name=='LIVE.md':
        a=q.index('Stop for lay discussion using central');z=q.index('\n<!-- STARTUP_CURRENT_END -->',a)
        q=q[:a]+'''Use central R8PRT/R18 and PRT1's reviewed handoff for the next bounded
step4A observation-interface task. The native positional assignment stays open;
the conditional restrictions and prior tools remain usable at their scopes.
Stage5 evaluator capability is distinct from native metric evolution. Verify
final bindings/checks and synchronization before integration or execution.
Existing pauses/protected boundaries persist. TPS1 raw fields/large streams
remain local-only; compact remote records cannot replay raw-dependent checks.
'''+q[z:]
    p.write_text(q)

p=W/'DEVELOPMENT_GRAPH.json';g=json.loads(p.read_text());assert all(n['id']!='R8PRT' for n in g['nodes'])
sources=[str(B/s) for s in ['INITIAL_CANDIDATE.md','PRECISION.md','REVIEWED_RESULT.md','WORK_ORDER.md']]
g['nodes'].append(dict(id='C_PRT_SIGN',kind='conditional_protocol',statement='For the sign implications only: actual PSW proper separation, parallel-prepared free clocks, independent first future signals, smooth common normal tube and fixed histories during arrival derivatives. Net N or physically matched reference-contrast C positivity is explicitly conditional/unadopted; all-direction/all-U quantifiers only when stated. Strict finite positivity gives weak quadratic sign, not a nonzero coefficient.',sources=sources,registry_ids=[]))
g['nodes'].append(dict(id='C_PRT_CONTROLS',kind='conditional_protocol',statement='Supplied controls only: a=1+k t^2, k>0, flat physical comparator and |t|<k^(-1/2) for all-frame strict leading sign; query-dependent small-L thresholds. Cubic a=1+b t^3, b>0, on (-b^(-1/3),infinity) times unquotiented R3, preparation0, direct first signals0<L<L_* and echo2L<L_*. No native admission, physical scale, global completeness or X_max; cubic future does not satisfy first control all-frame sign everywhere.',sources=sources,registry_ids=[]))
g['nodes'].append(dict(id='O_PRT_ASSIGNMENT',kind='open_join',statement='Received ticking and additional mutual slowing are established intended premises, but the inspected implication assigning a universal net N or selected-reference C condition to this prepared query remains unproved. Ordinary query data need no population law. Conditional restrictions/handoff do not prove whole-postulate insufficiency, select native dynamics or require a new postulate.',sources=sources,registry_ids=[]))
g['nodes'].append(dict(id='R8PRT',kind='argument',anchor='r8prt',title='Prepared positional translation, weak sign controls and future cubic asymptote; native assignment open with executable observation/evaluator handoff',sources=sources,registry_ids=[],required_conditions=['C_PRT_SIGN','C_PRT_CONTROLS']))
for frm in ['C_PRT_SIGN','C_PRT_CONTROLS']:g['edges'].append({'from':frm,'to':'R8PRT','kind':'hypothesis'})
for frm in ['R6','R7','R8']:g['edges'].append({'from':frm,'to':'R8PRT','kind':'proof'})
for frm in ['D1','R8PCC','R8ACI','R8GRL','R9','R13','R14','R16']:g['edges'].append({'from':frm,'to':'R8PRT','kind':'context'})
g['edges'].append({'from':'O_PRT_ASSIGNMENT','to':'R8PRT','kind':'open_boundary'});g['edges'].append({'from':'R8PRT','to':'R18','kind':'context'})
for source in sources:g['sources_sha256'][source]=sha(source)
targets=['D1','R6','R7','R8','R8PCC','R8PCCR','R8PCCE','R8ACI','R8GRL','R9','R13','R14','R16','R8PRT','R18','C_PRT_SIGN','C_PRT_CONTROLS','O_PRT_ASSIGNMENT']
support=['DESCENDANT_REVIEW.md','STEPS_4_5_HANDOFF.md','handoff_repair/REPAIR_RECORD.md']
for lane in ['math','fidelity']:support.extend(['review_'+lane+'/SOURCE_FIRST.md','review_'+lane+'/CANDIDATE_REVIEW.md','review_'+lane+'/PRECISION_HANDOFF_REVIEW.md'])
for source in support:
    source=str(B/source);g['review_support'].append(dict(path=source,sha256=sha(source),role='review_evidence',targets=targets))
p.write_text(json.dumps(g,indent=2)+'\n')
row=['PRT1_RETURN',str(B/'REVIEWED_RESULT.md'),'VERIFIED-WITH-CAVEATS_CONDITIONAL_TRANSLATION_AND_CONTROLS; native positional assignment OPEN; steps4/5 handoff not execution or physical adoption',';'.join(targets[:15]),'TWO_FRESH_SOURCE_FIRST_EXPOSED_FINAL_CONTEXTS; hand-rederived weak-sign non-Einstein and cubic-future controls; precision/handoff wording repair; no scientificCPU/GPU or native selector',sha(B/'REVIEWED_RESULT.md')]
with (W/'RECENT_DISPOSITIONS.tsv').open('a',newline='') as f:csv.writer(f,delimiter='\t',lineterminator='\n').writerow(row)
print(json.dumps(dict(nodes=len(g['nodes']),edges=len(g['edges']),source_pins=len(g['sources_sha256']),review_support=len(g['review_support']),orientation_words=len(guard.orientation(t).split()))))
