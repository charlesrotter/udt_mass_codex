"""One-time source-preserving integration of CPA1; no scientific grade changes."""
from pathlib import Path
import csv, hashlib, json, sys
sys.path.insert(0,str(Path.cwd()))
import verify_udt_development as guard

B=Path('udt_completion_progress_audit_2026-10-04')
W=Path('development_reconstruction_2026-09-29')
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
p=Path('UDT_DEVELOPMENT.md');t=p.read_text()
assert '<a id="r16cpa"></a>' not in t
t=t.replace('**Current development — PDA1 prepared-distance attachment reviewed,',
            '**Current development — CPA1 completion-branch progress audit reviewed,',1)
start=t.index('**Current learning.**');end=t.index('<!-- DEVELOPMENT_ORIENTATION_END -->')
t=t[:start]+'''**Current learning.** CPA1 audits FCL1/CCW1/PDA1 and their supplied completion
class RG. It finds real conditional gains: a free-clock bound in nonuniform
geometry, invariant clock/curvature relations and a conditional initial-distance
asymptote with a bounded preparation counterexample. No load-bearing false or
circular step was found at those stated scopes. Those gains remain available.

The source chain introduces RG as an UNADOPTED trial; the later proofs do not
derive its native admission. Its regular conformal endpoint supplies much of
the asymptotic form. PDA's common collar, endpoint-map regularity and nonzero
distance slope remain explicit conditions; bounded motion alone does not fix
the distance exponent. Initial surface distance is not automatically a
cosmological distance or X_max. A one-way endpoint does not ensure an echo.

The metric/null/proper-clock proofs still hold without UDT-specific interpretive
labels. This is a dependency check, not removal of positional spacetime or proof
of empirical equivalence to GR. Shared mathematics is legitimate. These results
alone do not select native geometry, identify an additional positional effect,
fix scale or prove convergence on UDT field equations. The complete postulates
are not proved insufficient, and no new premise is declared necessary.

The recommendation is to retain the tools and redirect physical development
toward a named UDT-to-geometry implication or concrete independent use. The
bounded source-led admission lookup proposed by PDA is now complete; repeating
it is not a new target. Generic RG-only extensions should not be presented as
native-selection progress. No new selector or successor derivation was found.

After orientation read R16CPA/R16PDA/R16CCW/R16FCL and R18. Two fresh source-first,
exposed and final contexts checked the audit and independently recomputed its
load-bearing algebra by hand. No new scientific program was needed. LIVE/HANDOFF
own closure and the discussion stop; no physical adoption or new campaign begins
automatically. Conditional modeling remains a separate explicit option.
'''+t[end:]
marker='<a id="r17"></a>';assert t.count(marker)==1
t=t.replace(marker,(B/'CENTRAL_INSERT.md').read_text()+'\n\n'+marker,1)
old='''[PDA1's decision brief](udt_prepared_distance_attachment_2026-10-04/DECISION_BRIEF.md)
owns the current lay return. The proposed next discussion is about whether an
existing UDT commitment actually admits this geometry, with a bounded source-led
audit as a possible later work order. That audit is unexecuted and is not an
automatic successor. Retaining the conditional result remains an option;
CCW/FCL/CPW/FCW fixed decisions keep their historical scopes. Stop for discussion;
no physical adoption or new campaign starts automatically.'''
new='''CPA1 now completes that bounded progress/admission-source audit in R16CPA.
The mathematical gains above survive, including the negative controls. The
source chain reaches FCW's explicit unadopted RG trial and CPW's robustness
dispatch; no later step in the inspected chain derives native admission.
Consequences under that input do not themselves justify it. H3's contribution
to the distance exponent is made explicit without miscalling PDA circular.
The proof-input check preserves the metric equations and is not a physical
operation removing positional geometry or an empirical GR-equivalence claim.

[CPA1's decision brief](udt_completion_progress_audit_2026-10-04/DECISION_BRIEF.md)
owns the current lay return. Its recommendation is to keep the conditional tools
and redirect the next physical task to a named current-premise implication or
a concrete independent use. More RG-only examples or the same admission-source
lookup would not by themselves close the physical join. No new native selector
or specific successor derivation was found. The decision does not demand a
unique cosmos, a new premise, a full light theory or all field equations before
targeted work. A deliberately conditional modeling question remains an option.
Prior fixed decisions keep their historical scope. Stop for discussion; no
physical adoption, new campaign pause or successor starts automatically.'''
assert t.count(old)==1;t=t.replace(old,new)
marker='The preserved first candidates expose the repair history.'
addition='''CPA1 uses two new fresh source-first/exposed/final contexts to audit the
progress assessment. Both read the prior source proofs/verdicts before the new
audit, so this is not verdict-blind rediscovery of old results. Parent froze its
audit before reading either new reviewer argument. Independent hand checks cover
the force/estimate, curvature contraction, proper-clock gap, distance incidence
and adverse expansions. Both accepted the bounded assessment without a blocking
scientific defect. Their nonblocking source-precision note distinguishes FCW's
smooth trial/C2 control from CPW/FCL's later C3 scope; the original audit stays
fixed and the reviewed return records the clarification. No new scientific
program was needed or run; prior pass counts are attributed, not evidence of
physical progress. Shared model and source exposure remain; different-model,
independent-code, human, formal, empirical and literature-priority review are
not claimed. [Work record](udt_completion_progress_audit_2026-10-04/WORK_RECORD.md)
and [descendant review](udt_completion_progress_audit_2026-10-04/DESCENDANT_REVIEW.md)
retain actual source ancestry, exposure and read/metadata errors. Final accepted-map
attestations and normal/maintenance/full406 receipts own closure and banking.

'''
assert t.count(marker)==1;t=t.replace(marker,addition+marker,1)
p.write_text(t);Path('CURRENT_RESEARCH_PROGRAM.md').write_text(guard.program_text(t))

common='''CDR1 remains the central-development architecture. UDT_DEVELOPMENT.md is the
sole maintained scientific argument; CURRENT_SCIENTIFIC_PREMISES.tsv and reviewed
sources own exact grades. The generated CURRENT_RESEARCH_PROGRAM.md is the bounded
startup orientation. Read R16CPA/R16PDA/R16CCW/R16FCL/R18 after orientation.

Charles authorized CPA1's five-question progress audit after PDA1 at c0c6ce8f.
Evidence is in udt_completion_progress_audit_2026-10-04/; WORK_ORDER owns the
bounded three-result/source-chain scope. The original audit, source-precision
addendum and two fresh source-first/exposed/final reviews are preserved.
Final attestations and actual normal/maintenance/full406 receipts own closure;
commit/push and byte checks own banking. Verify actual HEAD, remote, dirt and
processes rather than assuming this text identifies the tip.

Next: Stop for lay discussion of CPA1's decision brief and direction recommendation.
No specific successor derivation or new native selector was found. The previous
bounded admission-source lookup is complete; a further task needs a named new
implication or concrete use. No RG/FC adoption, registry promotion, new campaign
pause, field/source/action law or GPU/data/hardware campaign begins automatically.
No new scientific program ran in this audit. Standing no-timeout/resource/manual
stop rules and protection of unrelated work persist.

'''
for name,title,tail in [('LIVE.md','## CURRENT STATE — CPA1 progress-audit return, 2026-10-04','### Honest claim'),('HANDOFF.md','## Current handoff — CPA1 progress-audit return, 2026-10-04','Protected payloads require explicit dispatch; preserve without inspecting/hashing:')]:
    p=Path(name);q=p.read_text();a=q.index('## CURRENT STATE') if name=='LIVE.md' else q.index('## Current handoff');z=q.index(tail)
    q=q[:a]+title+'\n\n'+common+q[z:]
    if name=='LIVE.md':
        a=q.index('Stop for lay discussion using central');z=q.index('\n<!-- STARTUP_CURRENT_END -->',a)
        q=q[:a]+'''Stop for lay discussion using central R16CPA and the CPA1 decision brief.
The progress audit and bounded admission-source trace are complete at their
stated scope. The direction recommendation is for discussion, not a new adopted
physical premise or automatic successor. Verify actual final bindings/checks and
synchronization. Existing pauses and protected boundaries persist. TPS1 raw
fields/large streams remain local-only; compact remote records cannot replay
raw-dependent checks.
'''+q[z:]
    p.write_text(q)

p=W/'DEVELOPMENT_GRAPH.json';g=json.loads(p.read_text())
assert all(n['id']!='R16CPA' for n in g['nodes'])
sources=[str(B/s) for s in ['INITIAL_AUDIT.md','REVIEWED_RESULT.md','WORK_ORDER.md','SOURCE_CHECK_ADDENDUM.md']]
sources.append('udt_finite_comparison_whiteboard_2026-10-03/relational/INITIAL_PROPOSAL.md')
g['nodes'].append(dict(id='C_CPA_SCOPE',kind='conditional_protocol',statement='Source-relative audit of FCL/CCW/PDA and FCW/CPW trial ancestry with directly controlling founding/owner/G312 meanings. Inspect actual proof dependencies and quantifiers; no full-postulate insufficiency, empirical GR equivalence, literature novelty, physical adoption or automatic successor. Direction recommendation is not a selecting equation.',sources=sources,registry_ids=[]))
g['nodes'].append(dict(id='R16CPA',kind='argument',anchor='r16cpa',title='Progress audit: real conditional gains, unchanged native-admission join and scoped direction recommendation',sources=sources,registry_ids=[],required_conditions=['C_CPA_SCOPE']))
for n in g['nodes']:
    if n['id']=='O_FCW_ADMISSION':
        n['statement']='Physical RG admission, native geometry and additional-effect attribution remain OPEN. CPA1 inspected the actual FCW trial/CPW dispatch and three-result proof chain: conditional gains preserved, no native selector found in that bounded chain. The source-led lookup is complete at that scope; no whole-postulate insufficiency or required-new-premise theorem. Recommendation redirects next physical work to a named implication/concrete use, not automatic RG-only expansion. No adoption/scale/X_max selection.'
        n['sources'].append(str(B/'REVIEWED_RESULT.md'))
g['edges'].append({'from':'C_CPA_SCOPE','to':'R16CPA','kind':'hypothesis'})
for frm in ['D1','R6','R8','R9FST','R16FCW','R16CPW','R16FCL','R16CCW','R16PDA']:
    g['edges'].append({'from':frm,'to':'R16CPA','kind':'context'})
g['edges'].append({'from':'O_FCW_ADMISSION','to':'R16CPA','kind':'open_boundary'})
g['edges'].append({'from':'R16CPA','to':'R18','kind':'context'})
for source in sources:g['sources_sha256'][source]=sha(source)
targets=['D1','R6','R8','R9FST','R16FCW','R16CPW','R16FCL','R16CCW','R16PDA','R16CPA','R18','O_FCW_ADMISSION','O_CPW_FREECLOCK_LIMIT','C_CPA_SCOPE']
for source in ['review_math/EXPOSED_REVIEW.md','review_fidelity/EXPOSED_REVIEW.md','DESCENDANT_REVIEW.md','SOURCE_CHECK_SEAL.json']:
    source=str(B/source);g['review_support'].append(dict(path=source,sha256=sha(source),role='review_evidence',targets=targets))
p.write_text(json.dumps(g,indent=2)+'\n')
row=['CPA1_RETURN',str(B/'REVIEWED_RESULT.md'),'VERIFIED-WITH-CAVEATS_SOURCE_RELATIVE_PROGRESS_AUDIT; real conditional mathematical gains; RG UNADOPTED; native selection and additional attribution remain open in inspected chain',
     ';'.join(targets[:11]),'SOURCE_ANCESTRY_AND_PROOF_INPUT_AUDIT; two fresh source-first/exposed/final contexts with hand recomputation; no new scientific program, source regrade, complete-postulate no-go or physical adoption',sha(B/'REVIEWED_RESULT.md')]
with (W/'RECENT_DISPOSITIONS.tsv').open('a',newline='') as f:csv.writer(f,delimiter='\t',lineterminator='\n').writerow(row)
print(json.dumps(dict(nodes=len(g['nodes']),edges=len(g['edges']),source_pins=len(g['sources_sha256']),review_support=len(g['review_support']),orientation_prose_words=len(t[t.index('<!-- DEVELOPMENT_ORIENTATION_BEGIN -->')+len('<!-- DEVELOPMENT_ORIENTATION_BEGIN -->'):t.index('<!-- DEVELOPMENT_ORIENTATION_END -->')].split()))))
