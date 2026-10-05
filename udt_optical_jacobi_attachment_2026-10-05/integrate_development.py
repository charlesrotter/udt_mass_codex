"""One-time OJM1 central integration; no original scientific source regrading."""
from pathlib import Path
import json,csv,hashlib,sys
sys.path.insert(0,str(Path.cwd()))
import verify_udt_development as guard
B=Path('udt_optical_jacobi_attachment_2026-10-05');W=Path('development_reconstruction_2026-09-29')
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
p=Path('UDT_DEVELOPMENT.md');t=p.read_text();assert '<a id="r13ojm"></a>' not in t
def replace(old,new):
    global t
    assert t.count(old)==1,old
    t=t.replace(old,new,1)
replace('**Current development — OAA1 conditional affine-distance attachment reviewed,\n2026-10-04.**','**Current development — OJM1 conditional angular/Jacobi attachment reviewed,\n2026-10-05.**')
a=t.index('**Current learning.**');z=t.index('<!-- DEVELOPMENT_ORIENTATION_END -->',a)
t=t[:a]+'''**Current learning.** OJM1 derives the full two-dimensional map between
observed angle and source rest-screen size for the existing conditional metric.
It generally stretches the two directions differently. On the actual b_*=0
late history, the angular-area distance has the same finite1/H endpoint and
leading received-clock pole as OAA1's affine distance. Finite rays retain their
nonzero varying b; no separate optical or redshift curve is inserted.

Other ray histories have different optical endpoints and can pass through
caustics. Before the first caustic angular-area distance is no greater than
affine distance; that inequality cannot be extended through every crossing.
The full map is retained, with an inverse only off caustics. A geometric source
rest-screen is not yet a finite material disk or independently known ruler.
No universal maximum distance, native metric selection or X_max follows.

Two actual fresh contexts reconstruct the argument and independently replay
saved quantities. Parent exact/finite controls pass; independent original-metric
Jacobi and neighboring-ray checks support the map. One reviewer's initial
strong-ray finite-angle approximation failed, and its smaller-angle repair
at unchanged tolerance is preserved. Map/error wording is clarified without
changing equations. Actual final bindings and normal/maintenance/full406 receipts
own closure. Review, regression and numerical agreement are not physical adoption.

After orientation read R13OJM and R18, with R8ACP/CPR/OAA and R16 as needed.
The conditional optical map is explicit; native metric/comparison admission,
independent source/scale calibration and empirical use remain open. Physically
matched GR gives the same records. The proposed next bounded question is whether
specified timing/angular records determine H or retain degeneracies, without
silently adding a known source size. This does not itself select UDT dynamics.
Stop for lay discussion; no automatic successor, fit, physical adoption, large
solve or parked/protected program restart.
'''+t[z:]
replace('and finite-patch identification are separate conditional readout requirements. OAA1 in R8OAA\nnow gives a finite receiver-normalized affine endpoint in the conditional CGE1\nfamily. Its affine parameter is not a Jacobi/area distance by declaration;\nthe actual two-dimensional map remains the next proposed geometric interface.',
'''and finite-patch identification are separate conditional readout requirements.
OAA1 in R8OAA gives a finite receiver-normalized affine endpoint in the
conditional CGE1 family. OJM1 below now derives its actual two-dimensional
Jacobi map; affine and angular-area distances remain distinct except where
the scoped calculation proves agreement or a shared leading limit.''')
replace('<a id="r14"></a>',(B/'CENTRAL_INSERT.md').read_text()+'\n\n<a id="r14"></a>')
replace('The geometric attachment is now explicit, but its native positional meaning,\nindependent measurement and source-screen/angular interface remain open. A',
'''The geometric attachment is now explicit. OJM1 in R13OJM supplies the
conditional infinitesimal source-screen/angular map; native positional meaning,
independent measurement and actual astronomical source admission remain open. A''')
replace('still requires ACP1\'s source/map reduction. Stable supplied cadence gives its',
'''requires ACP1's source/map reduction. OJM1 in R13OJM now supplies the
conditional infinitesimal Jacobi block; actual finite-source reduction and data
remain separate. Stable supplied cadence gives its''')
replace('therefore carries a source-compatible scalar-map approximation; its D posterior',
'''therefore carries a source-compatible scalar-map approximation; OJM1's
conditional metric map in R13OJM explicitly retains the two directional factors.
Its new map does not retrospectively validate a published source approximation.
The D posterior''')
replace('counterexample rules out that last stronger interpretation.',
'''counterexample rules out that last stronger interpretation. OJM1 in R13OJM
extends the specified late endpoint and pole to angular-area distance, while
retaining generic shear/caustic and source-calibration limits. This does not
fix1/H in light-years or identify H with an observed Hubble parameter.''')
a=t.index('The next proposed bounded scientific step is the actual two-dimensional');z=t.index("NGD1's numerical return",a)
t=t[:a]+'''OJM1 now completes that conditional two-dimensional optical calculation.
The map between sky differential and source rest-screen displacement is derived
from neighboring geodesics, including signed factors and caustics. On the
actual b_*=0 tail, its angular-area distance preserves the finite endpoint and
leading clock pole. Generic optical endpoints retain ray dependence; no scalar
distance describes all directional lengths or supplies an inverse at a caustic.
This is a positive geometric consequence, not a fitted optical/redshift profile.

The next proposed bounded question is whether specified timing and angular
records determine this conditional H or leave a preparation/parameter degeneracy.
Declare available records before inversion; do not silently supply a known ruler,
source model, Hubble parameter or observational likelihood. Physical calibration
and native metric/comparison selection remain separate. Identical geometry and
physically matched GR queries still give identical records. The [fixed OJM1
return and proposed scope](udt_optical_jacobi_attachment_2026-10-05/DECISION_BRIEF.md)
states limits, resource/review bounds and next decision. Stop for lay discussion;
no automatic successor, fit, larger solve or protected-work restart.

'''+t[z:]
marker='The preserved first candidates expose the repair history.'
replace(marker,'''OJM1's two fresh source-first/exposed/final contexts reconstruct the full
optical map and independently replay actual saved incidences and map entries,
including original four-dimensional metric/Jacobi integration. Its [work record](udt_optical_jacobi_attachment_2026-10-05/WORK_RECORD.md)
preserves the strong-ray finite-angle failure/repair and shared-model/library
exposure. The [descendant review](udt_optical_jacobi_attachment_2026-10-05/DESCENDANT_REVIEW.md)
updates optical, clock, scale and adverse uses together. Exact proofs, finite
checks, same-formula regression and reviewed byte bindings remain distinct;
neither a finite source model nor native/empirical admission is inferred.

'''+marker)
p.write_text(t);Path('CURRENT_RESEARCH_PROGRAM.md').write_text(guard.program_text(t))
common='''CDR1 remains the central-development architecture. UDT_DEVELOPMENT.md is the
sole maintained scientific argument; CURRENT_SCIENTIFIC_PREMISES.tsv and reviewed
sources own exact grades. CURRENT_RESEARCH_PROGRAM.md is its generated bounded
orientation. After orientation read R13OJM/R18, with R8ACP/CPR/OAA and R16 as needed.

After OAA1 at278a8f12, Charles authorized the bounded angular/Jacobi-map test.
OJM1 evidence is in udt_optical_jacobi_attachment_2026-10-05/; WORK_ORDER owns
scope/stops. Two fresh source-first/exposed/final contexts reconstruct the
argument and recompute saved quantities. Initial candidates, the reviewer's
finite-angle failure/repair and wording clarifications are preserved. Actual
final attestations, normal/maintenance/full406 receipts and committed/remote
byte checks own closure. Verify actual HEAD, remote and dirt yourself.

Next: Stop for lay discussion of OJM1. R18 and DECISION_BRIEF distinguish
the conditional optical result from native/empirical admission and propose
a bounded record/scale-identifiability question for subsequent authorization.
No new physical premise, response law, registry grade or X_max is adopted.
No GPU/long production or parked/protected program restarted. Standing pauses,
preservation, no-timeout/manual-stop and resource rules persist.

'''
for name,title,tail in [('LIVE.md','## CURRENT STATE — OJM1 optical attachment return, 2026-10-05','### Honest claim'),('HANDOFF.md','## Current handoff — OJM1 optical attachment return, 2026-10-05','Protected payloads require explicit dispatch; preserve without inspecting/hashing:')]:
    p=Path(name);s=p.read_text();a=s.index('## CURRENT STATE') if name=='LIVE.md' else s.index('## Current handoff');z=s.index(tail)
    s=s[:a]+title+'\n\n'+common+s[z:]
    if name=='LIVE.md':
        a=s.index('Use central R8OAA/R18');z=s.index('\n<!-- STARTUP_CURRENT_END -->',a)
        s=s[:a]+'''Use central R13OJM/R18 and OJM1's decision brief for the conditional optical
map/pole and proposed record/scale-identifiability step. Native response/metric,
actual source/ruler and empirical application remain open. Verify final review,
required checks and banking evidence. Pauses/protected boundaries persist;
TPS1 raw fields/large streams remain local-only, not remotely replayable.
'''+s[z:]
    p.write_text(s)
p=W/'DEVELOPMENT_GRAPH.json';g=json.loads(p.read_text())
sources=[str(B/x) for x in ['WORK_ORDER.md','INITIAL_CANDIDATE.md','CLARIFICATIONS.md','PREMISE_LEDGER.tsv','CONSTRUCTION_RESULT.json','check_optical_map.py','CANDIDATE_FREEZE.json','NUMERICAL_FREEZE.md','METHOD_REFERENCES.md']]
g['nodes'].extend([
dict(id='C_OJM_RAY',kind='conditional_protocol',statement='Inherited conditional positive-H CPR1/OAA1 regular outgoing ray and fixed clock histories. Actual b varies between emissions. Principal b_star0 tail is distinct from general limiting rays and caustics.',sources=sources,registry_ids=[]),
dict(id='C_OJM_SCREEN',kind='conditional_protocol',statement='Infinitesimal source proper rest-screen and quotient-parallel endpoint bases; J maps sky to size, inverse only off caustics. D_A is angular-area, not a universal scalar length map or finite material ruler.',sources=sources,registry_ids=[]),
dict(id='O_OJM_ADMISSION',kind='open_join',statement='Native metric/comparison selection, independently known astronomical source/ruler and physical H calibration remain open. No extra physically matched-GR prediction, universal X_max or empirical admission.',sources=sources[:4],registry_ids=[]),
dict(id='R13OJM',kind='argument',anchor='r13ojm',title='Conditional full optical map, caustics and actual angular-area clock pole',sources=sources,registry_ids=[],required_conditions=['C_OJM_RAY','C_OJM_SCREEN'])])
for x in ['R13','R8CPR','R8OAA']:g['edges'].append({'from':x,'to':'R13OJM','kind':'proof'})
for x in ['C_OJM_RAY','C_OJM_SCREEN']:g['edges'].append({'from':x,'to':'R13OJM','kind':'hypothesis'})
targets=['D1','R2','R6','R7','R8','R8CGE','R8CPR','R8OAA','R8ACP','R9','R10','R13','R14','R15','R16','R17','R18','R13OJM','C_OJM_RAY','C_OJM_SCREEN','O_OJM_ADMISSION']
for x in targets[:17]:
    if x not in ['R13','R8CPR','R8OAA','R18']:g['edges'].append({'from':x,'to':'R13OJM','kind':'context'})
g['edges'].extend([{'from':'O_OJM_ADMISSION','to':'R13OJM','kind':'open_boundary'},{'from':'R13OJM','to':'R18','kind':'context'}])
for x in sources:g['sources_sha256'][x]=h(x)
for x in ['WORK_RECORD.md','DESCENDANT_REVIEW.md','review_math/SOURCE_FIRST.md','review_math/EXPOSED_REVIEW.md','review_math/RETURN_SCOPE_REVIEW.md','review_fidelity/SOURCE_FIRST.md','review_fidelity/INDEPENDENT_CHECK_REPORT.md','review_fidelity/EXPOSED_REVIEW.md']:
    x=str(B/x);g['review_support'].append({'path':x,'sha256':h(x),'role':'review_evidence','targets':targets})
p.write_text(json.dumps(g,indent=2)+'\n')
row=['OJM1_RETURN',str(B/'INITIAL_CANDIDATE.md'),'VERIFIED-WITH-CAVEATS_CONDITIONAL_OPTICAL_MAP_AND_POLE; native metric/source/scale and observation OPEN',';'.join(targets),'SOURCE_FIRST_EXPOSED_FINAL_REVIEW; exact Jacobi/ray-variation proof, actual incidences, independent original-metric/saved-value checks; finite-angle failure/repair preserved',h(B/'INITIAL_CANDIDATE.md')]
with (W/'RECENT_DISPOSITIONS.tsv').open('a',newline='') as f:csv.writer(f,delimiter='\t',lineterminator='\n').writerow(row)
print(json.dumps({'nodes':len(g['nodes']),'edges':len(g['edges']),'source_pins':len(g['sources_sha256']),'orientation_words':len(guard.orientation(t).split())}))
