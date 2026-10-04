"""One-time CGE1 bounded central integration; no source or grade promotion."""
from pathlib import Path
import json,csv,hashlib,sys
sys.path.insert(0,str(Path.cwd()))
import verify_udt_development as guard
B=Path('udt_conditional_source_geometry_2026-10-04');W=Path('development_reconstruction_2026-09-29')
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
p=Path('UDT_DEVELOPMENT.md');t=p.read_text();assert '<a id="r8cge"></a>' not in t
old='**Current development — ACP1 first astronomical comparison constructed and audited,'
assert t.count(old)==1;t=t.replace(old,'**Current development — CGE1 restricted conditional source/clock geometry reviewed,',1)
a=t.index('**Current learning.**');z=t.index('<!-- DEVELOPMENT_ORIENTATION_END -->',a)
t=t[:a]+'''**Current learning.** CGE1 constructs one restricted candidate for ACP1's
astronomical interface: a static spherical exterior in the already conditional
Ric=Lambda g class, with actual circular test clocks, a free radial receiver
and connecting null signals. The metric determines their motion, received
frequency and finite in-plane sky direction together. No independent Z(D)
profile is appended. This is standard Kottler geometry reconstructed within
an explicit conditional branch, not a native UDT field-law derivation or fit.

The construction uses regular finite-radius source clocks. It does not supply
a matter interior, self-gravitating disk, actual CGCG environment, full2D image
map or source-data reduction. Its parameters and receiver preparation remain
supplied. One radial spectral ratio can be held fixed while changing Lambda
and the receiver preparation; the full angular/time records are not proved
degenerate. Identical geometry and physically matched GR queries give identical
observations. The native physical selection and additional positional effect
therefore remain open, rather than being claimed from numerical agreement.

Original4D metric/geodesic checks and actual-arrival comparisons pass for the
frozen finite examples. Two fresh same-model contexts independently reconstructed
the argument and checked saved quantities by different numerical methods. An
extra division in the initial checking code failed the drift test; its exact
repair, original failure and unchanged candidate/tolerances are preserved.
These are bounded mathematical/numerical checks, not empirical confirmation.
Actual final attestations and normal/maintenance/full406 receipts own closure.

After orientation read R8CGE, R10 and R18. The next scientific gate is physical
discrimination of the conditional family using existing UDT commitments and an
operationally matched additional-effect comparison. No theorem of whole-postulate
insufficiency or need for a new postulate follows. Full astronomical source/map/
data requirements remain distinct. Stop for lay discussion; no automatic fit,
large solve, conditional-class adoption or parked/protected program restart.
'''+t[z:]
marker='#### Finite mutual ticking and its causal limits — FPC1';assert t.count(marker)==1
t=t.replace(marker,(B/'CENTRAL_INSERT.md').read_text()+'\n\n'+marker,1)
needle='A subsequent test\nneeds a candidate metric with consistent source histories and the actual data\nreduction, rather than another independent response profile.'
assert t.count(needle)==1
t=t.replace(needle,needle+''' CGE1 below now
fills a restricted conditional exterior/test-clock instance of that requirement.
The actual astronomical environment, full image map and data reduction remain
open; this partial construction does not retroactively make ACP1 a data fit.''',1)
needle='not a field equation derived unconditionally from positional dilation.'
assert t.count(needle)==1
t=t.replace(needle,needle+''' CGE1 in R8CGE
constructs its static spherical exterior and actual source/receiver query as a
conditional application. That explicit solution does not close class membership
or turn GR's comparison-filter role into a physical field-law input.''',1)
a=t.index('The next scientific target is a candidate metric from UDT commitments, or an');z=t.index("NGD1's numerical return",a)
t=t[:a]+'''CGE1 now supplies a restricted mathematical instance of that metric/source
construction in the already conditional R10 branch. R8CGE derives the exterior,
actual circular test-clock motion and a free receiver's same-metric null/sky
records. Direct original-equation checks, finite arrival derivatives and
independent methods agree. No empirical data entered its frozen examples.

This is a conditional construction gain, not a native-selection gain. Its exact
single-radial-shift family shows how different allowed receiver preparations can
mask changes in Lambda; it does not prove degeneracy of the full observations.
The central environment is a supplied exterior, not a universal cosmic center,
and its regular orbiting clock is not the published source's fitted systemic
reference by declaration. ACP1's full source/map/data requirements persist.

The next substantive target is physical discrimination: determine whether an
existing UDT commitment admits or restricts this conditional family, or directs
construction elsewhere, and specify a physically matched comparison before
claiming an additional positional effect. Identical geometry and matched GR
queries cannot themselves produce a difference. More tuning within the family
would not establish native admission. A narrowed conditional result is useful,
but no new physical premise or field law is adopted to call it UDT's prediction.
Native evolution/response selection, source environment and observation reduction
remain distinct open gates, not a theorem that all clarified UDT postulates are
insufficient. The [fixed CGE1 return](udt_conditional_source_geometry_2026-10-04/DECISION_BRIEF.md)
records the concrete result and limits. Stop for lay discussion; no automatic
fit, larger solve or restart of parked/protected/optional source campaigns.

'''+t[z:]
marker='The preserved first candidates expose the repair history.';assert t.count(marker)==1
t=t.replace(marker,'''CGE1 has two actual fresh source-first/exposed/final contexts. Their separate
original-coordinate derivations, one affine/proper-time ODE shooting comparison,
Gauss–Legendre saved-incidence reconstruction, and distinct drift checks support
the restricted candidate. The original failed checker and exact denominator
repair remain visible, with no scientific candidate/tolerance change. The
[work record](udt_conditional_source_geometry_2026-10-04/WORK_RECORD.md) and
[scoped descendant review](udt_conditional_source_geometry_2026-10-04/DESCENDANT_REVIEW.md)
state exposure, inherited conditional premises, positive/adverse uses and work
not repeated. Final byte review is distinct from the mathematical checks;
normal/maintenance/full406 and exact banking remain actual gates. No empirical,
human/different-model, full-corpus, native source or global stability claim.

'''+marker,1)
p.write_text(t);Path('CURRENT_RESEARCH_PROGRAM.md').write_text(guard.program_text(t))
common='''CDR1 remains the central-development architecture. UDT_DEVELOPMENT.md is the
sole maintained scientific argument; CURRENT_SCIENTIFIC_PREMISES.tsv and reviewed
sources own exact grades. CURRENT_RESEARCH_PROGRAM.md is its generated bounded
orientation. After orientation read R8CGE, R10 and R18; exact older sources only
when load-bearing.

After ACP1 atcdc94b5d, Charles authorized the next scientific step. CGE1 evidence
is in udt_conditional_source_geometry_2026-10-04/; WORK_ORDER owns scope and stops.
It constructs a restricted conditional exterior/test-clock/null comparison.
Two actual fresh source-first/exposed/final contexts review the mathematics and
source/native boundary, with independent ODE and saved-incidence checks. Initial
checker failure, exact repair and exposure history are retained. Actual final
attestations, normal/maintenance/full406 receipts and committed/remote byte checks
own closure. Verify current HEAD, remote, dirt and processes yourself.

Next: Stop for lay discussion of CGE1. The restricted conditional candidate
fills part of ACP1's construction gate; it is not a native UDT metric selection,
full astronomical model, fit or empirical confirmation. R18 owns physical
selection/additional-effect and distinct source/map/data requirements. No new
physical premise, registry grade, field law or scale is adopted. No GPU/long
production or parked/protected campaign restarted. Standing pause, preservation,
no-timeout/manual-stop and resource rules persist.

'''
for name,title,tail in [('LIVE.md','## CURRENT STATE — CGE1 conditional geometry return, 2026-10-04','### Honest claim'),('HANDOFF.md','## Current handoff — CGE1 conditional geometry return, 2026-10-04','Protected payloads require explicit dispatch; preserve without inspecting/hashing:')]:
 p=Path(name);s=p.read_text();a=s.index('## CURRENT STATE') if name=='LIVE.md' else s.index('## Current handoff');z=s.index(tail);s=s[:a]+title+'\n\n'+common+s[z:]
 if name=='LIVE.md':
  a=s.index('Use central R8ACP/R18');z=s.index('\n<!-- STARTUP_CURRENT_END -->',a)
  s=s[:a]+'''Use central R8CGE/R10/R18 and CGE1's decision brief for the conditional
construction and next physical-discrimination gate. Actual astronomical
source/map/data and native selection remain open. Verify final review/check/
banking evidence. Existing pauses/protected boundaries persist. TPS1 raw fields/
large streams remain local-only; compact remote records cannot replay them.
'''+s[z:]
 p.write_text(s)
p=W/'DEVELOPMENT_GRAPH.json';g=json.loads(p.read_text());assert not any(n['id']=='R8CGE' for n in g['nodes'])
sources=[str(B/x) for x in ['WORK_ORDER.md','INITIAL_CANDIDATE.md','PREMISE_LEDGER.tsv','CONSTRUCTION_RESULT.json','check_construction.py','CANDIDATE_FREEZE.json','CHECK_REPAIR.md','REPAIRED_CHECK_FREEZE.json','PRECISION_NOTE.md','METHOD_REFERENCES.md']]
g['nodes'].extend([
 dict(id='C_CGE_BRANCH',kind='conditional_protocol',statement='R10 full conditional Ric=Lambda g class, restricted static spherical R2 exterior f>0,r>0. m,Lambda supplied; no native response-class admission, source interior or cosmic center.',sources=sources,registry_ids=[]),
 dict(id='C_CGE_QUERY',kind='conditional_protocol',statement='Regular circular test geodesic and outward radial free receiver with supplied initial data; direct outward equatorial regular affine-null incidence. Stable spectral cadence conditional; full source/map/data reduction not supplied.',sources=sources,registry_ids=[]),
 dict(id='O_CGE_SELECTION',kind='open_join',statement='Native class selection/additional positional effect, real source environment, systemic reference realization, full angular map and observation reduction remain distinct open gates. No whole-postulate insufficiency follows.',sources=sources[:3],registry_ids=[]),
 dict(id='R8CGE',kind='argument',anchor='r8cge',title='Restricted conditional mass-parameter exterior, orbiting clocks and actual null comparison',sources=sources,registry_ids=[],required_conditions=['C_CGE_BRANCH','C_CGE_QUERY'])])
for x in ['R2','R6','R10']:g['edges'].append({'from':x,'to':'R8CGE','kind':'proof'})
for x in ['C_CGE_BRANCH','C_CGE_QUERY']:g['edges'].append({'from':x,'to':'R8CGE','kind':'hypothesis'})
for x in ['D1','R7','R8ACP','R8PRT','R9','R13','R14','R15','R16','R17']:g['edges'].append({'from':x,'to':'R8CGE','kind':'context'})
g['edges'].append({'from':'O_CGE_SELECTION','to':'R8CGE','kind':'open_boundary'});g['edges'].append({'from':'R8CGE','to':'R18','kind':'context'})
for x in sources:g['sources_sha256'][x]=h(x)
targets=['D1','R2','R6','R7','R8ACP','R8PRT','R9','R10','R13','R14','R15','R16','R17','R18','R8CGE','C_CGE_BRANCH','C_CGE_QUERY','O_CGE_SELECTION']
for x in ['WORK_RECORD.md','DESCENDANT_REVIEW.md','review_math/SOURCE_FIRST.md','review_math/CANDIDATE_REVIEW.md','review_fidelity/SOURCE_FIRST.md','review_fidelity/DIRECT_REVIEW.md']:
 x=str(B/x);g['review_support'].append(dict(path=x,sha256=h(x),role='review_evidence',targets=targets))
p.write_text(json.dumps(g,indent=2)+'\n')
row=['CGE1_RETURN',str(B/'INITIAL_CANDIDATE.md'),'VERIFIED-WITH-CAVEATS_CONDITIONAL_EXTERIOR_TEST_CLOCK_QUERY; native selection/full astronomical model OPEN; no fit or adoption',';'.join(targets[:15]),'SOURCE_FIRST_EXPOSED_FINAL_REVIEW; original-equation and40ray checks; independent ODE and quadrature; failed checker preserved and repaired without candidate/tolerance change',h(B/'INITIAL_CANDIDATE.md')]
with (W/'RECENT_DISPOSITIONS.tsv').open('a',newline='') as f:csv.writer(f,delimiter='\t',lineterminator='\n').writerow(row)
print(json.dumps({'nodes':len(g['nodes']),'edges':len(g['edges']),'source_pins':len(g['sources_sha256']),'orientation_words':len(guard.orientation(t).split())}))
