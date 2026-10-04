"""One-time ACI1 integration; preserve all original sources and grades."""
from pathlib import Path
import csv,hashlib,json,sys
sys.path.insert(0,str(Path.cwd()))
import verify_udt_development as guard

B=Path('udt_asymptotic_curvature_implication_2026-10-04')
W=Path('development_reconstruction_2026-09-29')
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
p=Path('UDT_DEVELOPMENT.md');t=p.read_text()
assert '<a id="r8aci"></a>' not in t
t=t.replace('**Current development — CPA1 completion-branch progress audit reviewed,',
            '**Current development — ACI1 finite-curvature implication attempt reviewed,',1)
a=t.index('**Current learning.**');z=t.index('<!-- DEVELOPMENT_ORIENTATION_END -->',a)
t=t[:a]+'''**Current learning.** Charles directed retention of the completion results as
tools and a search for an implication from an existing UDT commitment to a
geometric restriction. ACI1 tests the working asymptotic slowing requirement
without RG. The native physical assignment remains unclosed; a conditional
finite curvature exclusion is obtained.

For specified actual clock comparisons admitting a regular fixed-endpoint
path sweep, bounded initial relative motion and accumulated acceleration,
unbounded received slowing requires an unbounded transported-curvature integral.
The finite4D proof adds curvature control beyond the old endpoint-rapidity bound
and small-loop expansion. The integral depends on the comparison/sweep and
transported clock; it is not scalar curvature or a supplied bound for nature.
Large integral alone predicts no redshift. The domain conditions matter.

A supplied sharp control has free parallel-prepared clocks, divergent slowing,
zero scalar curvature and regular local curvature, with reception proper time
growing without bound. It excludes the earlier specific RG endpoint through
CCW's necessary scalar limit. It is not a native-admitted UDT history or X_max.
Flat initial-motion, acceleration and winding controls retain the theorem's
kinematic and sweep limits.

The unresolved physical step is attaching the additional positional requirement
to the declared comparison family. Net redshift is not automatically positional
attribution. No metric, response, sign, scale, population or new premise is
selected, and no whole-postulate insufficiency is proved. CPA1's assessment
survives: the completion results remain valid conditional tools, not native
geometry selection. Repeating its source lookup or extending generic examples
would not itself close this assignment.

After orientation read R8ACI, R16CPA and R18. Two fresh reviewer contexts
reconstructed and checked the finite argument and controls. Parent exposure to
an early reviewer outline preceded its file freeze; independent pre-review
parent discovery is not claimed. One parent control program passed51 symbolic
assertions after two preserved exact-normalization failures; some assertions
are consistency checks. Final attestations and required checks own closure.
Stop for discussion of the physical assignment; no adoption or successor begins
automatically. The founding positional interpretation remains the premise.
'''+t[z:]
marker='#### Finite mutual ticking and its causal limits — FPC1'
assert t.count(marker)==1
t=t.replace(marker,(B/'CENTRAL_INSERT.md').read_text()+'\n\n'+marker,1)
old='''and recommendation limits. Stop for Charles's direction discussion; review
does not adopt RG, regrade a source or launch a successor.'''
new='''and recommendation limits. Charles subsequently directed retention of the
tools and investigation of an existing-commitment geometric implication. ACI1
in R8ACI attempts the asymptotic-curvature route and preserves an unclosed
physical assignment alongside its finite conditional gain. Review adopts no RG
premise or source regrade; R18 owns the current discussion return.'''
assert t.count(old)==1;t=t.replace(old,new,1)
a=t.index("[CPA1's decision brief]");z=t.index('\n\nNGD1\'s numerical return',a)
t=t[:a]+'''Charles accepted CPA1's direction to retain tools and seek an existing-premise
geometric implication. ACI1 in R8ACI now returns a finite curvature restriction
for a declared realization of the working asymptotic target. Its unclosed
physical comparison assignment leads the result; this is not a native geometry
selector. The proof controls relative transport through a curvature integral,
with initial-motion/acceleration allowances and a fixed-endpoint sweep domain.
Its regular scalar-zero sharp control shows why neither a local singularity
nor the specific RG endpoint follows from divergent received slowing alone.

[ACI1's decision brief](udt_asymptotic_curvature_implication_2026-10-04/DECISION_BRIEF.md)
owns the current lay return. The additional positional requirement has not been
assigned by an inspected source implication to this net-clock family. Retain
the finite necessary test and all prior completion tools, while distinguishing
their mathematical uses from physical selection. This attempt does not justify
automatically proving more generic bounds or launching another template family.
It supplies no selected successor, new-premise necessity, field equation or
X_max realization. Stop for discussion of the physical assignment. Prior fixed
decisions keep their scope; no physical adoption or campaign begins automatically.
'''+t[z:]
marker='The preserved first candidates expose the repair history.'
addition='''ACI1 uses two actual fresh source-first/exposed/final contexts. Their finite
transport derivations and hand control checks precede new-candidate exposure,
with old proof/verdict exposure disclosed. The intended parent-before-review
freeze order was breached by math's unsolicited pre-seal route outline; parent
read it before its file freeze and claims no independent pre-review discovery.
The supplement credits fidelity's cosh control idea. Both exposed reviews found
no required scientific repair but insisted that the native physical assignment
remain the headline open issue. One parent exact control program had two
preserved normal-form failures before51 symbolic assertions passed; metrics,
equations and expected values stayed fixed. Some assertions are consistency,
not independent confirmation. Actual incidence, curvature and integration were
recomputed by hand. No reviewer scientific CPU, different-model, human, formal,
independent-code or empirical review is claimed. [Work record](udt_asymptotic_curvature_implication_2026-10-04/WORK_RECORD.md)
and [descendant review](udt_asymptotic_curvature_implication_2026-10-04/DESCENDANT_REVIEW.md)
preserve exposure, read/path failures, exact repairs and both favorable/adverse
scope. Final accepted-map attestations, normal/maintenance/full406 receipts and
actual banking own closure; neither review nor commit adopts physics.

'''
assert t.count(marker)==1;t=t.replace(marker,addition+marker,1)
p.write_text(t);Path('CURRENT_RESEARCH_PROGRAM.md').write_text(guard.program_text(t))

common='''CDR1 remains the central-development architecture. UDT_DEVELOPMENT.md is the
sole maintained scientific argument; CURRENT_SCIENTIFIC_PREMISES.tsv and reviewed
sources own exact grades. The generated CURRENT_RESEARCH_PROGRAM.md is the bounded
startup orientation. Read R8ACI, R16CPA and R18 after orientation.

After CPA1 at dfe6ba37, Charles directed retention of the tools and investigation
of an existing-commitment geometric implication. ACI1 evidence is in
udt_asymptotic_curvature_implication_2026-10-04/; WORK_ORDER owns scope. The initial
candidate, two failed normalizers, successful exact control, early reviewer
outline exposure and two actual source-first/exposed/final contexts are preserved.
Final attestations and actual normal/maintenance/full406 receipts own closure;
commit/push and byte checks own banking. Verify actual HEAD, remote, dirt and
processes rather than assuming this text identifies the tip.

Next: Stop for lay discussion of ACI1's narrowed return and physical assignment.
No new native selector or specific successor was found. The completed CPA1
admission-source lookup stays complete; ACI1's finite conditional restriction
does not select a physical observer family or close positional attribution.
No RG/FC adoption, registry promotion, new campaign pause, field/source/action
law or GPU/data/hardware campaign begins automatically. One short exact control
program ran in three preserved attempts, no long solver. Standing no-timeout,
resource/manual stops and protection of unrelated work persist.

'''
for name,title,tail in [('LIVE.md','## CURRENT STATE — ACI1 narrowed implication return, 2026-10-04','### Honest claim'),('HANDOFF.md','## Current handoff — ACI1 narrowed implication return, 2026-10-04','Protected payloads require explicit dispatch; preserve without inspecting/hashing:')]:
    p=Path(name);q=p.read_text();a=q.index('## CURRENT STATE') if name=='LIVE.md' else q.index('## Current handoff');z=q.index(tail)
    q=q[:a]+title+'\n\n'+common+q[z:]
    if name=='LIVE.md':
        a=q.index('Stop for lay discussion using central');z=q.index('\n<!-- STARTUP_CURRENT_END -->',a)
        q=q[:a]+'''Stop for lay discussion using central R8ACI/R16CPA/R18 and ACI1's decision
brief. The native physical assignment remains unclosed; the finite conditional
curvature test and supplied controls are retained. No automatic successor or
physical adoption. Verify actual final bindings/checks and synchronization.
Existing pauses/protected boundaries persist. TPS1 raw fields/large streams
remain local-only; compact remote records cannot replay raw-dependent checks.
'''+q[z:]
    p.write_text(q)

p=W/'DEVELOPMENT_GRAPH.json';g=json.loads(p.read_text())
assert all(n['id']!='R8ACI' for n in g['nodes'])
sources=[str(B/s) for s in ['INITIAL_CANDIDATE.md','CONTROL_SUPPLEMENT.md','REVIEWED_RESULT.md','WORK_ORDER.md']]
g['nodes'].append(dict(id='C_ACI_SWEEP',kind='conditional_protocol',statement='Smooth Lorentz4, actual regular affine-null proper-clock comparison, declared reference path and fixed-endpoint finite piecewise-C2 sweep with compatible seams. Transported curvature rest norm depends on g,u,F; no automatic global sweep, scalar-only or observer-independent norm claim.',sources=sources,registry_ids=[]))
g['nodes'].append(dict(id='C_ACI_CONTROLLED',kind='conditional_protocol',statement='For the asymptotic exclusion only: a declared family realizes net Z tending to infinity with uniformly bounded initial preparation mismatch and accumulated proper acceleration; qualifying sweeps exist. These are query/domain conditions, not a selected physical positional population.',sources=sources,registry_ids=[]))
g['nodes'].append(dict(id='O_ACI_ASSIGNMENT',kind='open_join',statement='The requested native physical assignment remains OPEN: no inspected source implication attaches the additional positional asymptote to the controlled net-clock/sweep family. Finite curvature exclusion is conditional, not native geometry selection, a new-postulate necessity or a whole-theory no-go.',sources=sources,registry_ids=[]))
g['nodes'].append(dict(id='R8ACI',kind='argument',anchor='r8aci',title='Finite curvature bound and sharp regular scalar-zero control; native physical assignment remains unclosed',sources=sources,registry_ids=[],required_conditions=['C_ACI_SWEEP','C_ACI_CONTROLLED']))
for frm in ['C_ACI_SWEEP','C_ACI_CONTROLLED']:
    g['edges'].append({'from':frm,'to':'R8ACI','kind':'hypothesis'})
for frm in ['R6','R7','R16CCW']:
    g['edges'].append({'from':frm,'to':'R8ACI','kind':'proof'})
for frm in ['D1','R8','R16CPA']:
    g['edges'].append({'from':frm,'to':'R8ACI','kind':'context'})
g['edges'].append({'from':'O_ACI_ASSIGNMENT','to':'R8ACI','kind':'open_boundary'})
g['edges'].append({'from':'R8ACI','to':'R18','kind':'context'})
for source in sources:g['sources_sha256'][source]=sha(source)
targets=['D1','R6','R7','R8','R16CCW','R16FCL','R16PDA','R16CPA','R8ACI','R18','O_FCW_ADMISSION','O_ACI_ASSIGNMENT','C_ACI_SWEEP','C_ACI_CONTROLLED']
for source in ['B/math/EXPOSED_REVIEW.md','B/fidelity/EXPOSED_REVIEW.md','DESCENDANT_REVIEW.md','CONTROL_REPAIR.md','CONTROL_REPAIR_FOLLOWUP.md']:
    source=str(B/source);g['review_support'].append(dict(path=source,sha256=sha(source),role='review_evidence',targets=targets))
p.write_text(json.dumps(g,indent=2)+'\n')
row=['ACI1_RETURN',str(B/'REVIEWED_RESULT.md'),'VERIFIED-WITH-CAVEATS_CONDITIONAL_FINITE_CURVATURE_BOUND; native physical assignment UNCLOSED; exact4D comparison bound and supplied scalar-zero sharp control; no RG or physical adoption',
     ';'.join(targets[:10]),'FINITE_TRANSPORT_VARIATION_AND_HYPERBOLOID_BOUND; two fresh source-first/exposed/final contexts; parent early-outline exposure;51 exact assertions include consistency; two normal-form failures preserved; no native selector',sha(B/'REVIEWED_RESULT.md')]
with (W/'RECENT_DISPOSITIONS.tsv').open('a',newline='') as f:csv.writer(f,delimiter='\t',lineterminator='\n').writerow(row)
print(json.dumps(dict(nodes=len(g['nodes']),edges=len(g['edges']),source_pins=len(g['sources_sha256']),review_support=len(g['review_support']),orientation_prose_words=len(t[t.index('<!-- DEVELOPMENT_ORIENTATION_BEGIN -->')+len('<!-- DEVELOPMENT_ORIENTATION_BEGIN -->'):t.index('<!-- DEVELOPMENT_ORIENTATION_END -->')].split()))))
