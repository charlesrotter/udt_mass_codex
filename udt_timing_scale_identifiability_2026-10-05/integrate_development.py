"""One-time TSI1 central integration, retaining all inherited scientific grades."""
from pathlib import Path
import json,csv,hashlib,sys
sys.path.insert(0,str(Path.cwd()))
import verify_udt_development as guard
B=Path('udt_timing_scale_identifiability_2026-10-05');W=Path('development_reconstruction_2026-09-29')
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
p=Path('UDT_DEVELOPMENT.md');t=p.read_text();assert '<a id="r16tsi"></a>' not in t
def replace(old,new):
    global t
    assert t.count(old)==1,old
    t=t.replace(old,new,1)
replace('**Current development — OJM1 conditional angular/Jacobi attachment reviewed,','**Current development — TSI1 conditional timing/scale identification reviewed,')
a=t.index('**Current learning.**');z=t.index('<!-- DEVELOPMENT_ORIENTATION_END -->',a)
t=t[:a]+'''**Current learning.** TSI1 supplies a conditional way to determine the scale
without a known source size. For the existing metric and regular source/receiver
histories, the late logarithmic redshift rate on the receiver's calibrated clock
tends to c_E H. Thus that ideal timing record gives1/H=c_E/rate. The principal
angular-position track gives the same late rate in its specified parallel frame.
These follow from actual varying incidences; no redshift curve is inserted.

Untimed redshift/angle records retain an exact scale freedom. Calibrated time
breaks it, without selecting the metric or determining every other parameter.
c_E supplies the time-to-length conversion. G_obs would need a separately
justified physical mass/density connection to add independent information;
a quantity with mass units is not automatically physical source mass.

The ideal-record limit matters. Fixed-spacing ticks in the finite remaining
emitter interval cannot sample infinitely late derivatives. Source variability,
angular reference and finite resolving power require explicit treatment before
empirical use. Finite practical accuracy remains open. Physically matched GR
still gives the same records; no extra UDT prediction or X_max follows.

Parent exact/finite controls and two actual fresh separate contexts support the
conditional result and independently recompute saved quantities. Exposure and
shared-model/library limits are recorded. Actual final bindings and required
normal/maintenance/full406 receipts own closure, not the numerical agreement.

After orientation read R16TSI and R18, with R8CPR/OAA and R13OJM as dependencies.
The next proposed bounded question is finite-record identifiability with declared
source/motion uncertainty and a justified error bound or explicit degeneracy.
Native geometry/comparison admission remains a separate gate. Stop for lay
discussion; no automatic successor, fit, physical adoption, large solve or
parked/protected program restart.
'''+t[z:]
replace('<a id="r16fcw"></a>',(B/'CENTRAL_INSERT.md').read_text()+'\n\n<a id="r16fcw"></a>')
replace('fix1/H in light-years or identify H with an observed Hubble parameter.',
'''fix1/H in light-years from those formulas alone or identify H with an
observed Hubble parameter. TSI1 below now gives a conditional clock-calibration
route without a known ruler; an actual usable timing record remains unsupplied.''')
replace('provided. The conditional optical calculation is now explicit; native metric/\ncomparison selection, independent physical source/scale calibration and data\nremain open.',
'''provided. The conditional optical calculation is now explicit. R16TSI
supplies an ideal timing route to scale without a known source ruler; finite
source reduction, actual usable data and native metric/comparison selection
remain open.''')
replace('independent measurement and actual astronomical source admission remain open. A',
'''independent measurement and actual astronomical source admission remain open.
R16TSI supplies a conditional timing-to-scale interface, distinct from such
an actual measurement or a new native metric selection. A''')
a=t.index('The next proposed bounded question is whether specified timing and angular');z=t.index("NGD1's numerical return",a)
t=t[:a]+'''TSI1 in R16TSI now distinguishes calibrated timing from untimed records.
The ideal late logarithmic redshift rate determines c_E H for this family;
the principal angular track supplies a narrower independent route. No known
source size is required. Untimed redshift/angle records retain an explicit
homothety. This is a positive conditional inverse result, not native selection.

The next proposed bounded question is finite-record identifiability: can a
finite calibrated interval constrain H with declared source motion/frequency
uncertainty and justified error control? Fixed-spacing ticks do not sample the
infinite asymptote, and arbitrary source variability can confound a finite
record. Specify the available records and nuisance freedoms before inference.
The [fixed TSI1 return and proposed scope](udt_timing_scale_identifiability_2026-10-05/DECISION_BRIEF.md)
states resource/review bounds. Native metric/comparison admission remains a
separate gate; matched GR gives the same records. Stop for lay discussion;
no automatic successor, fit, larger solve or protected-work restart.

'''+t[z:]
marker='The preserved first candidates expose the repair history.'
replace(marker,'''TSI1's two fresh source-first/exposed/final contexts independently derive
the timed/untimed distinction, check operational cadence and mass boundaries,
and replay saved rates and scale transformations with separate implementations.
Its [work record](udt_timing_scale_identifiability_2026-10-05/WORK_RECORD.md) and
[descendant review](udt_timing_scale_identifiability_2026-10-05/DESCENDANT_REVIEW.md)
record formula exposure, conditional source protocols and the positive update
to scale calibration alongside the surviving constants-only/untimed limits.
Neither asymptotic identifiability nor numerical agreement establishes finite
astronomical access, native selection or an additional matched-GR effect.

'''+marker)
p.write_text(t);Path('CURRENT_RESEARCH_PROGRAM.md').write_text(guard.program_text(t))
common='''CDR1 remains the central-development architecture. UDT_DEVELOPMENT.md is the
sole maintained scientific argument; CURRENT_SCIENTIFIC_PREMISES.tsv and reviewed
sources own exact grades. CURRENT_RESEARCH_PROGRAM.md is its generated bounded
orientation. After orientation read R16TSI/R18, with R8CPR/OAA and R13OJM as needed.

After OJM1 atded574c1, Charles authorized the next timing/scale tests and
reaffirmed c_E/G_obs anchors. TSI1 evidence is in
udt_timing_scale_identifiability_2026-10-05/; WORK_ORDER owns scope/stops.
Two fresh source-first/exposed/final contexts reconstruct the argument and
recompute saved quantities; formula exposure and limits are recorded. Actual
final attestations, normal/maintenance/full406 receipts and committed/remote
byte checks own closure. Verify actual HEAD, remote and dirt yourself.

Next: Stop for lay discussion of TSI1. R18 and DECISION_BRIEF distinguish
ideal conditional scale recovery from finite-record availability and native
selection, and propose a bounded finite-record test for later authorization.
No new physical premise, response law, registry grade or X_max is adopted.
No GPU/long production or parked/protected program restarted. Standing pauses,
preservation, no-timeout/manual-stop and resource rules persist.

'''
for name,title,tail in [('LIVE.md','## CURRENT STATE — TSI1 timing/scale return, 2026-10-05','### Honest claim'),('HANDOFF.md','## Current handoff — TSI1 timing/scale return, 2026-10-05','Protected payloads require explicit dispatch; preserve without inspecting/hashing:')]:
    p=Path(name);s=p.read_text();a=s.index('## CURRENT STATE') if name=='LIVE.md' else s.index('## Current handoff');z=s.index(tail)
    s=s[:a]+title+'\n\n'+common+s[z:]
    if name=='LIVE.md':
        a=s.index('Use central R13OJM/R18');z=s.index('\n<!-- STARTUP_CURRENT_END -->',a)
        s=s[:a]+'''Use central R16TSI/R18 and TSI1's decision brief for conditional timed scale
recovery and the finite-record gate. Native response/metric, physical source
access and empirical application remain open. Verify final review, required
checks and banking evidence. Pauses/protected boundaries persist;
TPS1 raw fields/large streams remain local-only, not remotely replayable.
'''+s[z:]
    p.write_text(s)
p=W/'DEVELOPMENT_GRAPH.json';g=json.loads(p.read_text())
sources=[str(B/x) for x in ['WORK_ORDER.md','INITIAL_CANDIDATE.md','CONSTRUCTION_RESULT.json','check_timing_scale.py','CANDIDATE_FREEZE.json','NUMERICAL_FREEZE.md','CLARIFICATIONS.md']]
g['nodes'].extend([
dict(id='C_TSI_HISTORY',kind='conditional_protocol',statement='Inherited CPR1/OJM1 positive-H strict regular outgoing ray branch, finite fixed-E escaping receiver and circular source. Smooth actual incidence b(x), ordinary proper clocks; principal b_star0 only for angular logarithmic slope.',sources=sources,registry_ids=[]),
dict(id='C_TSI_RECORD',kind='conditional_protocol',statement='T ideal smooth calibrated clock arrival map or constant-normalization frequency ratio; A principal point-position track in fixed parallel radial frame. Infinite asymptotic access not supplied by finite fixed-spacing ticks. U untimed data retain homothety.',sources=sources,registry_ids=[]),
dict(id='O_TSI_ADMISSION',kind='open_join',statement='Finite-record/source/noise admission and native metric/comparison selection remain open. No m-to-physical-mass interface, new matched-GR effect, X_max or observed Hubble parameter adopted.',sources=sources[:2],registry_ids=[]),
dict(id='R16TSI',kind='argument',anchor='r16tsi',title='Conditional timing and principal angular scale recovery with untimed homothety',sources=sources,registry_ids=[],required_conditions=['C_TSI_HISTORY','C_TSI_RECORD'])])
for x in ['R8CPR','R8OAA','R13OJM','R16']:g['edges'].append({'from':x,'to':'R16TSI','kind':'proof'})
for x in ['C_TSI_HISTORY','C_TSI_RECORD']:g['edges'].append({'from':x,'to':'R16TSI','kind':'hypothesis'})
targets=['D1','R2','R6','R7','R8','R8CGE','R8CPR','R8OAA','R8ACP','R9','R10','R13','R13OJM','R14','R15','R16','R17','R18','R16TSI','C_TSI_HISTORY','C_TSI_RECORD','O_TSI_ADMISSION']
for x in targets[:18]:
    if x not in ['R8CPR','R8OAA','R13OJM','R16','R18']:g['edges'].append({'from':x,'to':'R16TSI','kind':'context'})
g['edges'].extend([{'from':'O_TSI_ADMISSION','to':'R16TSI','kind':'open_boundary'},{'from':'R16TSI','to':'R18','kind':'context'}])
for x in sources:g['sources_sha256'][x]=h(x)
for x in ['WORK_RECORD.md','DESCENDANT_REVIEW.md','review_math/SOURCE_FIRST.md','review_math/EXPOSED_REVIEW.md','review_fidelity/SOURCE_FIRST.md','review_fidelity/EXPOSED_REVIEW.md']:
    x=str(B/x);g['review_support'].append({'path':x,'sha256':h(x),'role':'review_evidence','targets':targets})
p.write_text(json.dumps(g,indent=2)+'\n')
row=['TSI1_RETURN',str(B/'INITIAL_CANDIDATE.md'),'VERIFIED-WITH-CAVEATS_CONDITIONAL_TIMING_SCALE_RECOVERY; finite data/source and native geometry OPEN',';'.join(targets),'SOURCE_FIRST_EXPOSED_FINAL_REVIEW; smooth-tail proof, exact metric/frame and finite actual-incidence checks, independent saved-rate replays; ideal-record limits',h(B/'INITIAL_CANDIDATE.md')]
with (W/'RECENT_DISPOSITIONS.tsv').open('a',newline='') as f:csv.writer(f,delimiter='\t',lineterminator='\n').writerow(row)
print(json.dumps({'nodes':len(g['nodes']),'edges':len(g['edges']),'source_pins':len(g['sources_sha256']),'orientation_words':len(guard.orientation(t).split())}))
