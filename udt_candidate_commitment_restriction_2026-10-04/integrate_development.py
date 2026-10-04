"""One-time CPR1 scoped integration. Sources and exact scientific grades unchanged."""
from pathlib import Path
import json,csv,hashlib,sys
sys.path.insert(0,str(Path.cwd()))
import verify_udt_development as guard
B=Path('udt_candidate_commitment_restriction_2026-10-04');W=Path('development_reconstruction_2026-09-29')
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
p=Path('UDT_DEVELOPMENT.md');t=p.read_text();assert '<a id="r8cpr"></a>' not in t
old='**Current development — CGE1 restricted conditional source/clock geometry reviewed,'
assert t.count(old)==1;t=t.replace(old,'**Current development — CPR1 existing-commitment restriction audit reviewed,',1)
a=t.index('**Current learning.**');z=t.index('<!-- DEVELOPMENT_ORIENTATION_END -->',a)
t=t[:a]+'''**Current learning.** CPR1 tests the conditional CGE1 geometry against the
existing asymptotic slowing and tested-regime recovery commitments. For its
fixed circular source and one fixed finite-energy outgoing receiver, received
slowing stays bounded in the static region, even at its chart horizon. The
smooth outward extension can produce unbounded slowing with positive Lambda,
an escaping receiver and regular connecting signals. Zero or negative Lambda
cannot give that same unbounded-outward mechanism.

This is a conditional restriction on a concrete realization. Emission approaches
a finite limiting time while receiver proper time tends to infinity; areal r
is not automatically physical observer separation or finite X_max. No current
argument attaches this reception-horizon limit to UDT's additional positional
effect. Identical geometry and physically matched GR queries still give the
same records. A proper orbital-rate comparison supplies a conditional recovery
bound once its matching and tolerance are specified, with no empirical value
invented. Angular cancellation supplies no Lambda selection here. DDR inside
R10 remains conditional; locality alone does not fix its physical response.

Two actual fresh contexts checked sources, algebra, original curvature and
actual clock incidences independently. Original-equation and bounded finite
checks pass. A too-loose root stopping condition was caught by the original
incidence residual; its tightened repair, unchanged acceptance tolerances and
reduced sampling are preserved. This is a reviewed conditional consequence,
not native field-law selection or empirical confirmation. Actual final review
bindings and normal/maintenance/full406 receipts own closure.

After orientation read R8CPR, R9/R10 as needed, and R18. The next gate is the
operational attachment: does the additional positional asymptote correspond
to this fixed-history limit, or require another physical comparison? Derive
the attachment from existing commitments or leave it open; no new premise is
declared necessary. Full astronomical source/map/data gates remain distinct.
Stop for lay discussion; no automatic fit, large solve, conditional-class
adoption or parked/protected program restart.
'''+t[z:]
marker='#### Finite mutual ticking and its causal limits — FPC1';assert t.count(marker)==1
t=t.replace(marker,(B/'CENTRAL_INSERT.md').read_text()+'\n\n'+marker,1)
needle='retains both the positive application and these adverse limits.';assert t.count(needle)==1
t=t.replace(needle,needle+''' CPR1 below
tests those limits and the same metric's regular continuation against existing
commitments. Its conditional asymptote/recovery restrictions do not retroactively
admit CGE1 as a native metric or change its original finite queries.''',1)
needle='retain the full hypothesis and source boundaries.';assert t.count(needle)==1
t=t.replace(needle,needle+''' CPR1 in R8CPR keeps this
spaceform restriction explicit: CGE1 with m>0 has nonconstant Weyl curvature,
so not every metric-natural local response is forced to be pure trace there.
Its unadopted gradient-Weyl diagnostic exhibits that distinction without
identifying the physical response or satisfying all R10 class gates.''',1)
needle="or turn GR's comparison-filter role into a physical field-law input.";assert t.count(needle)==1
t=t.replace(needle,needle+''' CPR1 applies existing
asymptotic/recovery requirements to the explicit candidate only conditionally
on the specified physical query and matching. Neither its positive-Lambda
realization nor its recovery inequality closes native class admission.''',1)
a=t.index('The next substantive target is physical discrimination:');z=t.index("NGD1's numerical return",a)
t=t[:a]+'''CPR1 now tests existing commitments against this candidate. R8CPR proves
a static-region received-ratio bound for the fixed regular orbiting source and
finite-energy outgoing receiver. Its same-metric regular extension supports an
unbounded received ratio for an escaping positive-Lambda history with regular
limiting incidence; the zero/negative alternatives cannot realize that same
unbounded-outward experiment. It also gives the exact conditional proper-
orbital-rate recovery bound. These are useful restrictions once the proposed
physical realization is specified, not automatic consequences selecting a
native UDT parameter from all current commitments.

The boundary is now concrete: this finite-emission-endpoint reception horizon
has not been identified with UDT's additional positional separation asymptote.
Areal r is not automatically a spatial distance beyond the static patch, and
X_max remains open. Angular trace cancellation does not select Lambda or make
this clock divergence a proved angular loud regime. R10-class DDR is automatic;
R9FST's stronger spaceform invariance does not apply to the m>0 exterior.

The next substantive question is operational attachment: derive from existing
commitments whether the additional positional target is this actual clock limit
or another comparison, specifying measured separation/clock records and the
physically matched GR reference. Merely naming a chart horizon or fitting an
extra curve cannot establish the connection. The same geometry and matched
queries predict the same records. A failed attachment on this example would
not prove that all clarified postulates are insufficient or require a new one.
Native response admission, astronomical source environment/full angular map and
actual observation reduction remain distinct gates. The [fixed CPR1 return](udt_candidate_commitment_restriction_2026-10-04/DECISION_BRIEF.md)
records the restriction and unresolved identification. Stop for lay discussion;
no automatic fit, larger solve or parked/protected/source campaign restart.

'''+t[z:]
marker='The preserved first candidates expose the repair history.';assert t.count(marker)==1
t=t.replace(marker,'''CPR1 adds two actual fresh source-first/exposed/final contexts, separate
original-curvature and actual-incidence derivations, and independent saved-
quantity checks. Its [work record](udt_candidate_commitment_restriction_2026-10-04/WORK_RECORD.md)
discloses preliminary formula exposure, the parent stopping-threshold defect,
unchanged acceptance criteria and reduced numerical coverage. The reviewers'
early-branch failure and later arithmetic-summary correction are preserved.
The [descendant review](udt_candidate_commitment_restriction_2026-10-04/DESCENDANT_REVIEW.md)
covers positive conditional uses and narrowed negative claims, including the
nonspaceform DDR distinction and open asymptote attachment. Final file-hash
review and required regression receipts are separate from scientific proof;
none supplies a new physical premise or empirical confirmation.

'''+marker,1)
p.write_text(t);Path('CURRENT_RESEARCH_PROGRAM.md').write_text(guard.program_text(t))
common='''CDR1 remains the central-development architecture. UDT_DEVELOPMENT.md is the
sole maintained scientific argument; CURRENT_SCIENTIFIC_PREMISES.tsv and reviewed
sources own exact grades. CURRENT_RESEARCH_PROGRAM.md is its generated bounded
orientation. After orientation read R8CPR and R18, with R9/R10 when load-bearing.

After CGE1 ata8ddc1af, Charles authorized testing existing UDT commitments against
the candidate. CPR1 evidence is in udt_candidate_commitment_restriction_2026-10-04/;
WORK_ORDER owns scope/stops. Two actual fresh source-first/exposed/final contexts
review the argument and independent numerical controls. Failed checks, repairs,
clarifications and exposure history are retained. Actual final attestations,
normal/maintenance/full406 receipts and committed/remote byte checks own closure.
Verify actual HEAD, remote, dirt and processes yourself.

Next: Stop for lay discussion of CPR1's conditional restrictions and the still-open
physical attachment in R18. No native response class, additional positional effect,
X_max value or empirical bound has been established. Native/source/map/data gates
remain distinct. No new premise, registry grade, field law or scale is adopted.
No GPU/long production or parked/protected campaign restarted. Standing pauses,
preservation, no-timeout/manual-stop and resource rules persist.

'''
for name,title,tail in [('LIVE.md','## CURRENT STATE — CPR1 commitment restriction return, 2026-10-04','### Honest claim'),('HANDOFF.md','## Current handoff — CPR1 commitment restriction return, 2026-10-04','Protected payloads require explicit dispatch; preserve without inspecting/hashing:')]:
 p=Path(name);s=p.read_text();a=s.index('## CURRENT STATE') if name=='LIVE.md' else s.index('## Current handoff');z=s.index(tail);s=s[:a]+title+'\n\n'+common+s[z:]
 if name=='LIVE.md':
  a=s.index('Use central R8CGE/R10/R18');z=s.index('\n<!-- STARTUP_CURRENT_END -->',a)
  s=s[:a]+'''Use central R8CPR/R18 and CPR1's decision brief for the conditional restrictions
and unresolved physical attachment. R9/R10 retain response/class boundaries.
Actual astronomical source/map/data and native selection remain open. Verify
final review/check/banking evidence. Existing pauses/protected boundaries persist.
TPS1 raw fields/large streams remain local-only; compact remote records cannot
replay them.
'''+s[z:]
 p.write_text(s)
p=W/'DEVELOPMENT_GRAPH.json';g=json.loads(p.read_text());assert not any(n['id']=='R8CPR' for n in g['nodes'])
sources=[str(B/x) for x in ['WORK_ORDER.md','INITIAL_CANDIDATE.md','CLARIFICATIONS.md','PREMISE_LEDGER.tsv','CONSTRUCTION_RESULT.json','check_restriction.py','CANDIDATE_FREEZE.json','CHECK_REPAIR.md','REPAIRED_CHECK_FREEZE.json','METHOD_REFERENCES.md']]
g['nodes'].extend([
 dict(id='C_CPR_REALIZATION',kind='conditional_protocol',statement='CGE1 conditional family, fixed regular circular source and finite-E outward receiver. For divergent-clock realization additionally Lambda>0, escaping history and strict regular limiting incidence in outgoing-EF continuation; mathematical domain not native completion.',sources=sources,registry_ids=[]),
 dict(id='C_CPR_RECOVERY',kind='conditional_protocol',statement='Compare same geometric m,a and supplied epsilon on squared proper angular rate, not arbitrary coordinate rate or empirical whole-GR bound. No stability or disk assumption.',sources=sources[:4],registry_ids=[]),
 dict(id='O_CPR_ATTACHMENT',kind='open_join',statement='Physical identification of fixed-history reception-horizon asymptote with UDT additional positional separation/X_max remains open, as do native class and observed tolerance. No insufficiency theorem or new-premise necessity.',sources=sources[:4],registry_ids=[]),
 dict(id='R8CPR',kind='argument',anchor='r8cpr',title='Existing-commitment audit: conditional static bound, outward asymptote and proper-orbital recovery',sources=sources,registry_ids=[],required_conditions=['C_CPR_REALIZATION','C_CPR_RECOVERY'])])
for x in ['R8CGE','R6']:g['edges'].append(dict(**{'from':x,'to':'R8CPR','kind':'proof'}))
for x in ['C_CPR_REALIZATION','C_CPR_RECOVERY']:g['edges'].append(dict(**{'from':x,'to':'R8CPR','kind':'hypothesis'}))
targets=['D1','R2','R6','R7','R8','R8ACP','R8CGE','R8PRT','R9','R9FST','R10','R13','R14','R15','R16','R17','R18','R8CPR','C_CPR_REALIZATION','C_CPR_RECOVERY','O_CPR_ATTACHMENT']
for x in ['D1','R2','R7','R8','R8ACP','R8PRT','R9','R9FST','R10','R13','R14','R15','R16','R17']:g['edges'].append({'from':x,'to':'R8CPR','kind':'context'})
g['edges'].append({'from':'O_CPR_ATTACHMENT','to':'R8CPR','kind':'open_boundary'});g['edges'].append({'from':'R8CPR','to':'R18','kind':'context'})
for x in sources:g['sources_sha256'][x]=h(x)
for x in ['WORK_RECORD.md','DESCENDANT_REVIEW.md','review_math/SOURCE_FIRST.md','review_math/EXPOSED_REVIEW.md','review_math/CHECK_REVIEW.md','review_math/CHECK_REVIEW_CORRECTION.md','review_fidelity/SOURCE_FIRST.md','review_fidelity/EXPOSED_REVIEW.md','review_fidelity/CHECK_REVIEW.md']:
 x=str(B/x);g['review_support'].append(dict(path=x,sha256=h(x),role='review_evidence',targets=targets))
p.write_text(json.dumps(g,indent=2)+'\n')
row=['CPR1_RETURN',str(B/'INITIAL_CANDIDATE.md'),'VERIFIED-WITH-CAVEATS_CONDITIONAL_RESTRICTIONS; native attachment/selection and empirical bound OPEN',';'.join(targets),'SOURCE_FIRST_EXPOSED_FINAL_REVIEW; original-EF/exact curvature and actual-incidence checks; source-preserving check repair, no premise or grade promotion',h(B/'INITIAL_CANDIDATE.md')]
with (W/'RECENT_DISPOSITIONS.tsv').open('a',newline='') as f:csv.writer(f,delimiter='\t',lineterminator='\n').writerow(row)
print(json.dumps({'nodes':len(g['nodes']),'edges':len(g['edges']),'source_pins':len(g['sources_sha256']),'orientation_words':len(guard.orientation(t).split())}))
