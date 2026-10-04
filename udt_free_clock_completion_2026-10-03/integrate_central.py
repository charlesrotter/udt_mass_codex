"""Bounded FCL1 integration; actual final review/banking is a separate gate."""
from pathlib import Path
import json,csv,hashlib,sys
sys.path.insert(0,str(Path.cwd()))
import verify_udt_development as verify
B=Path('udt_free_clock_completion_2026-10-03')
W=Path('development_reconstruction_2026-09-29')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
p=Path('UDT_DEVELOPMENT.md');s=p.read_text();assert '<a id="r16fcl">' not in s
s=s.replace('**Current development — CPW1 reviewed; free-clock completion test authorized,',
            '**Current development — FCL1 conditional free-clock result reviewed,',1)
a=s.index('**Authorized question.**');z=s.index('<!-- DEVELOPMENT_ORIENTATION_END -->',a)
s=s[:a]+'''**Current result.** FCL1 (R16FCL) derives the missing receiver limit within
UNADOPTED regular conformal completion RG. One finite-data freely falling receiver
approaching the specified spacelike boundary has rescaled tangent tending to its
conformal normal. Its physical proper time diverges. For the supplied regular
interior-emitter null family, physical received frequency tends to zero and
Omega_o Z tends to a finite positive constant. Motion and nonuniform geometry
are allowed; no bounded rescaled velocity or Einstein equation is assumed.

This is a varying-emission single-receiver limit, not a monotonic full-history
or fixed-emission distance curve, population theorem or X_max derivation. RG and
the regular signal family remain supplied; physical admission, native event/path
assignment, positional attribution and scale remain OPEN. The accelerated-clock
control lies outside the free-receiver theorem. Earlier adverse and positive
results keep their source scopes.

After orientation read R16FCL, R16FCW/R16CPW for its conditional origin and R6
for the clock observable. LIVE/HANDOFF own actual closure status and the lay
return. The bounded derivation includes two fresh independent argument reviews
and exact controls; no further investigation or physical adoption starts here.
'''+s[z:]
needle='No theorem about\nthose free-clock limits is proved here.'
assert needle in s;s=s.replace(needle,'No theorem about\nthose free-clock limits was proved by CPW1; R16FCL below now answers its exact\nconditional successor scope.',1)
needle='Protocol/congruence robustness\nis a possible second derivation target before any physical RG admission.'
assert needle in s;s=s.replace(needle,'Protocol/congruence robustness\nwas the next conditional target; R16FCL below now answers the specified\nsingle-free-receiver question while physical RG admission remains open.',1)
s=s.replace('<a id="r17"></a>',(B/'CENTRAL_INSERT.md').read_text()+'\n\n<a id="r17"></a>',1)
needle='Completion/protocol robustness remains a second option; a physical\nreason for RG is still absent.'
assert needle in s;s=s.replace(needle,'FCL1 now answers the specified completion/free-clock robustness question\nconditionally in R16FCL; a physical reason for RG is still absent.',1)
a=s.index('The parent recommends ONE distinct optional next derivation, not contributor');z=s.index("NGD1's numerical return",a)
s=s[:a]+'''FCL1 now completes that separately proposed free-clock derivation after Charles
authorized it and the startup cleanup. The geodesic equation supplies the missing
receiver bound in arbitrary nonuniform RG geometry near the specified endpoint;
the regular interior-emitter null family then gives the positive finite Omega Z
limit and divergent redshift. A moving free control passes, while an accelerated
control demonstrates the importance of the receiver hypothesis. Two fresh
independent arguments support the result; no physical premise is adopted.

The answered question is no longer left as an unexecuted obstruction. Physical
RG admission and regular comparison-family existence remain supplied. Native
geometry/event-path assignment, positional attribution, scale, X_max, uniform
populations and fixed-emission distance curves remain separate open questions.
The founding asymptote alone still does not imply RG; interior nonuniqueness
and the earlier conditional echo results retain their scope. The next scientific
issue is the physical connection supplying the completion, not another repetition
of the now-proved receiver-limit calculation.

The [FCL1 decision brief](udt_free_clock_completion_2026-10-03/DECISION_BRIEF.md)
records that gain and its limits. The original CPW1 scope/decision and ESR/IEC
records remain fixed historical evidence. Stop for lay discussion; this result
does not itself authorize another derivation, premise adoption or campaign.

'''+s[z:]
s=s.replace('[45 later returns]','[55 later returns]',1)
s=s.replace('registered rows have an editorial disposition;45 relevant later returns','registered rows have an editorial disposition;55 relevant later returns',1)
s=s.replace('includes54 later returns/clarifications','includes55 later returns/clarifications',1)
s=s.replace('advice and remains unexecuted. [Work record]','advice and was unexecuted in CPW1; FCL1 now supplies its scoped result. [Work record]',1)
review='''FCL1 uses two new fresh source-first/exposed/final reviewer contexts. Both
independently reconstructed an energy estimate before seeing the parent momentum
proof; exposed review checked its sharper bound, physical proper-time remainder,
normal-chart and null-family regularity, normalization and gauge. Both recomputed
the two actual clock controls and one rational nonuniform force case by hand;
the other five cases retain their parent exact-control status. No mathematical
repair was required, and the frozen candidate remains unchanged. Finite C3
regularity was checked explicitly rather than silently treated as C-infinity.
Shared model/premises remain limits; no human/different-model/empirical verification.
[Work record](udt_free_clock_completion_2026-10-03/WORK_RECORD.md) and
[descendant review](udt_free_clock_completion_2026-10-03/DESCENDANT_REVIEW.md)
state actual checks and omissions. SFC1 first shortened startup while preserving
the then-current scientific body; its metadata/guard repairs and original failed
audit remain fixed. FCL1 updates only its new scientific scope and current return.
Actual final attestations and normal/maintenance/full406 receipts own closure.

'''
s=s.replace('The preserved first candidates expose the repair history.',review+'The preserved first candidates expose the repair history.',1)
p.write_text(s);Path('CURRENT_RESEARCH_PROGRAM.md').write_text(verify.program_text(s))
common='''CDR1 remains the central-development architecture. UDT_DEVELOPMENT.md is the
sole maintained scientific argument; CURRENT_SCIENTIFIC_PREMISES.tsv and reviewed
sources own exact grades. The generated CURRENT_RESEARCH_PROGRAM.md is the bounded
startup orientation. Read R16FCL/R18 after orientation for the current argument.

Charles authorized startup cleanup followed by CPW1's bounded free-clock derivation.
The cleanup was reviewed, checked, committed and synchronized at4d9f202f, including
its preserved metadata/guard repairs. FCL1 evidence is in
udt_free_clock_completion_2026-10-03/; WORK_ORDER owns its completed scope.
The original candidate, exact controls, two fresh independent source-first and
exposed reviews are saved. Final attestations and actual normal/maintenance/full406
receipts own integration/pass status. Commit/push and byte checks own banking;
verify actual HEAD, remote, dirt and processes rather than assuming this is the tip.

Next: Stop for lay discussion of FCL1's conditional result and decision brief.
Its authorized construction/review cycle is the current return, not permission
for a further successor. No RG/FC adoption, native field/source/action law,
registry promotion, GPU/data/hardware campaign or automatic extension. One short
CPU exact-control script was run; no long solver. No-timeout direction persists
with finite scope/resource/manual stops. Preserve protected/unrelated work.

'''
for filename,title,end in [('LIVE.md','CURRENT STATE','### Honest claim'),('HANDOFF.md','Current handoff','Protected payloads require explicit dispatch;')]:
 p=Path(filename);t=p.read_text();a=t.index('## '+title);z=t.index(end,a)
 t=t[:a]+f'## {title} — FCL1 conditional free-clock return, 2026-10-03\n\n'+common+t[z:]
 if filename=='LIVE.md':
  a=t.index('### Next gate');z=t.index('<!-- STARTUP_CURRENT_END -->',a)
  t=t[:a]+'''### Next gate

Stop for lay discussion using central R16FCL/R18 and the FCL1 decision brief.
Native physical admission and remaining scope are open; no successor starts
automatically. Verify actual evidence, final bindings and synchronization.
Existing pauses and protected boundaries persist. TPS1 raw fields/large streams
remain local-only; compact remote records cannot replay raw-dependent checks.

'''+t[z:]
 p.write_text(t)
g=json.loads((W/'DEVELOPMENT_GRAPH.json').read_text());assert len(g['nodes'])==122
sources=[str(B/f) for f in ['INITIAL_CANDIDATE.md','REVIEWED_RESULT.md','WORK_ORDER.md']]
for f in sources:g['sources_sha256'][f]=sha(f)
lookup={n['id']:n for n in g['nodes']}
for key in ['R6','R16','R16CPW','R18','O_CPW_FREECLOCK_LIMIT','O_FCW_ADMISSION','C_CPW_CONFORMAL']:
 lookup[key]['sources'].append(str(B/'REVIEWED_RESULT.md'))
lookup['C_CPW_CONFORMAL']['statement']='Supplied conformal metric and regular affine-null/proper-clock interface. CPW1 exact bookkeeping gives finite positive Omega_o Z if its endpoint factors have finite positive limits. CPW1 did not establish actual free-clock limits; FCL1 separately derives them under explicit C_FCL_RG_CLOCK hypotheses. Normalization alone remains insufficient.'
lookup['O_CPW_FREECLOCK_LIMIT']['statement']='FCL1 ANSWERS the specified pointwise geodesic receiver/frequency limit under C_FCL_RG_CLOCK. Residual open boundary: physical RG/branch admission, arbitrary accelerated clocks, uniform populations, fixed-emission distance curves, echo availability and X_max identification. This node is not a proof input; do not leave the answered conditional question mislabeled unexecuted.'
lookup['O_FCW_ADMISSION']['statement']='Physical justification/adoption of FC or RG and native geometry/scale remain OPEN. ESR1 retains its conditional locally symmetric FC classification; CPW1 parks physical FC extension. FCL1 proves the specified pointwise completion/free-clock limit under supplied C3 RG and regular interior-emitter null family, without physical admission or global/population/distance selection.'
g['nodes'].extend([
 dict(id='C_FCL_RG_CLOCK',kind='conditional_protocol',statement='UNADOPTED supplied C3 gbar/Omega regular spacelike future completion g=Omega^-2 gbar with nonzero timelike dOmega; one finite-data future unit physical geodesic approaching specified boundary point, with compact collar bounds derived locally; regular interior emitter compact away from Omega0, limiting emission event, supplied smooth unique conformal-null family and nonzero regular endpoint affine data, consistent omega_e1. No assumed rescaled-velocity bound, Einstein equation, uniform population or distance identification.',sources=sources,registry_ids=[]),
 dict(id='R16FCL',kind='argument',anchor='r16fcl',title='Conditional free-geodesic normal limit and actual-clock asymptote in nonuniform completion',sources=sources,registry_ids=[],required_conditions=['P_NULL','C_FCL_RG_CLOCK'])])
for a,b,k in [('P_NULL','R16FCL','hypothesis'),('C_FCL_RG_CLOCK','R16FCL','hypothesis'),('R6','R16FCL','proof'),('R16CPW','R16FCL','proof'),('R16FCW','R16FCL','context'),('O_FCW_ADMISSION','R16FCL','open_boundary'),('R16FCL','R18','context')]:g['edges'].append(dict(from_=a,to=b,kind=k))
# JSON uses the existing graph key name, not the Python reserved keyword.
for e in g['edges']:
 if 'from_' in e:e['from']=e.pop('from_')
targets=['D1','R6','R16','R16FCW','R16CPW','R16FCL','R18','O_CPW_FREECLOCK_LIMIT','O_FCW_ADMISSION','C_FCL_RG_CLOCK']
for rel in ['review_math/EXPOSED_REVIEW.md','review_math/REGULARITY_ADDENDUM.md','review_fidelity/EXPOSED_REVIEW.md','DESCENDANT_REVIEW.md']:
 f=str(B/rel);g['review_support'].append(dict(path=f,sha256=sha(f),role='review_evidence',targets=targets))
(W/'DEVELOPMENT_GRAPH.json').write_text(json.dumps(g,indent=2)+'\n')
p=W/'RECENT_DISPOSITIONS.tsv';rows=list(csv.DictReader(p.open(),delimiter='\t'));assert len(rows)==54
row=dict(id='FCL1_RETURN',source=str(B/'REVIEWED_RESULT.md'),current_scope='VERIFIED-WITH-CAVEATS_CONDITIONAL_FREE_CLOCK_LIMIT; derived normal tangent/infinite proper time/positive finite OmegaZ under supplied C3 RG and regular emitter-null family; RG UNADOPTED',central_location='R6;R16;R16FCW;R16CPW;R16FCL;R18',rederivation_depth='GENERAL_SPATIAL_MOMENTUM_BOUND_AND_CLOCK_LIMIT; two fresh independent energy proofs, exposed exact/regularity/hand-control checks; one parent exact3family8case control; no native geometry/distance/population/scale promotion',source_sha256=sha(B/'REVIEWED_RESULT.md'))
with p.open('a',newline='') as f:csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n').writerow(row)
print(json.dumps(dict(nodes=len(g['nodes']),edges=len(g['edges']),sources=len(g['sources_sha256']),review_support=len(g['review_support']),later_returns=55,orientation_words=len(verify.orientation(s).split()))))
