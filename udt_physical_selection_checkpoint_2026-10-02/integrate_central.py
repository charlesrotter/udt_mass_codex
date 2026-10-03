from pathlib import Path
import json,csv,hashlib
import verify_udt_development as verify
B=Path('udt_physical_selection_checkpoint_2026-10-02');W=Path('development_reconstruction_2026-09-29');h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
p=Path('UDT_DEVELOPMENT.md');s=p.read_text();assert '<a id="r8psc">' not in s
s=s.replace('ERC1 and RCD1, 2026-10-01','ERC1, RCD1 and PSC1, 2026-10-02',1)
orientation="""PSC1 examines two UNADOPTED physical connections. A common weak scalar-curvature
response scale does not select a nonlinear equation: a cubic-curvature completion
shares that scale but changes the prepared clock curve. Requiring an identical
linear pole over an admitted interval of background curvatures selects quadratic
f only within the stipulated metric-f(R) class. That extra invariance does not
follow from a universal law, and the backgrounds generally occupy different
integration-constant sectors. Local horizon thermodynamics instead requires
specified entropy/heat/temperature/production; it does not select the entropy
function. The return retains the geometric diagnostic and recommends no adoption
or automatic extension of the R² survey. Native implication remains open.
"""
s=s.replace('<!-- DEVELOPMENT_ORIENTATION_END -->',orientation+'<!-- DEVELOPMENT_ORIENTATION_END -->',1)
clock="""<a id="r8psc"></a>

#### Distinguishing a nonlinear completion — PSC1

R17PSC's UNADOPTED metric-f(R) comparison control f=R+alphaR²+betaR³ has the
same near-flat first-order tensor response for every beta, while its nonlinear
clock prediction differs. This is a mathematical control, not a third proposed
physical connection or an admitted UDT geometry. Retain R8RCD's homogeneous,
comoving, independent-initial-L and differential-tick protocol. Set
a0=1,H0=R0=Lambda=0,P0=Rdot0!=0,alpha!=0. With F=df/dR,

    Hdot=R/6-2H², Rdot=P,
    Pdot=-3HP+[FR-2f+4Lambda-3F_RR P²]/(3F_R),
    C=3FH²-(FR-f)/2+3H F_R P-Lambda, Cdot=-4HC.

Here F_R=2alpha+6betaR is nonzero near the initial event, so the smooth local
ODE and initially zero constraint yield actual homogeneous tensor solutions.
The trace alone would not suffice. For example a=sqrt(1+2ht),h!=0, on a positive
patch has R=0 and satisfies the scalar trace for the quadratic Lambda0 case,
yet its original00 residual is3H²!=0. Original equations remain necessary.

For the constrained flat-event data, Pdot0=-3beta P0²/alpha and
Pddot0=-P0/(6alpha)+27beta²P0³/alpha². The arrival correction starts at fourth
order, giving through fifth order

    log p=b3 L³+b4 L⁴+b5 L⁵+O(L⁶),
    b3=P0/36, b4=-beta P0²/(48alpha),
    b5=-P0/(4320alpha)+3beta²P0³/(80alpha²),
    beta/alpha=-b4/(27b3²),
    b5=-b3/(120alpha)+(12/5)b4²/b3.

Thus a nonzero quartic term under this specified preparation rejects R8RCD's
quadratic equation, even when the leading clock effect and weak scalar pole
agree. At beta=0 the old result is recovered unchanged. This is a conditional
coefficient test, not unique full-theory identification, noisy-data estimation
or proof from finitely many coefficients that a complete history satisfies the
equation. Generic astronomical redshift records do not automatically supply this
preparation or its independent distances. Beta has dimension length^4; no
physical coefficient, source amplitude or observational pass is selected.

Sources: [fixed candidate](udt_physical_selection_checkpoint_2026-10-02/INITIAL_CANDIDATE.md)
and [reviewed conditional return](udt_physical_selection_checkpoint_2026-10-02/REVIEWED_RESULT.md).

"""
s=s.replace('## 6. Response restrictions and an optional conditional dynamics branch',clock+'## 6. Response restrictions and an optional conditional dynamics branch',1)
response="""<a id="r17psc"></a>

**Physical-selection checkpoint — PSC1.** Two proposals are considered, neither
adopted. S asks whether independently reconstructed scalar curvature has a common
response scale relating space and time behavior. H asks whether local causal
horizons obey an independently justified energy/entropy balance. They are
physical commitments under consideration, not consequences of positional clock
kinematics. Current founding/DDR/locality/filter meanings remain intact.

For S, restrict explicitly to metric-f(R), F=df/dR and
E_f=F Ric-fg/2+(g Box-Hess)F. This is a supplied comparison class, not selected
by UDT. Conservation and DDR give E_f+Lambda g=0. Linearize its trace
3Box F+FR-2f+4Lambda=0 at an actual constant-curvature background R0, holding
Lambda fixed during that perturbation. Where F_R(R0)!=0,

    [Box_0-M²(R0)]delta R=0,
    M²(R0)=[F(R0)-R0 F_R(R0)]/[3F_R(R0)].

For f=R+alphaR²+betaR³, alpha>0, M²(0)=1/(6alpha) for every beta. All beta
terms in the original tensor begin at second perturbative order near flat.
Temporal dispersion omega²/c_E²=k²+M² and a supplied decaying static radial
mode exp(-Mr)/r therefore share a length ell=1/M and homogeneous period
2pi ell/c_E, without selecting beta. ERC1 already contained the quadratic
space/time pieces; their repetition is not a new selector. Boundaries, mode
amplitudes, source-free sector and independent geometric measurements remain
supplied. Positive M² alone is not global stability or empirical GR recovery.

A STRONGER UNADOPTED version demands M²=mu²>0 throughout an admitted open
connected curvature interval I. With F_R!=0, R+3mu²!=0,0 in I and F(0)=1,

    (R+3mu²)F_R=F,
    d[F/(R+3mu²)]/dR=0,
    f=R+R²/(6mu²)+constant on I.

This is a conditional selection inside the stipulated class, up to normalization
and a pure-trace constant; it is not unrestricted equation/action uniqueness or
physical response normalization. Neither an interval condition nor the class
restriction follows from the same governing law for every observer. A universal
nonlinear equation may have background-dependent response; the cubic control has
M²(R0)=(1-3betaR0²)/(6alpha+18betaR0) and slope at0=-beta/(2alpha²).

Background admission is essential. Each constant-curvature solution has
Lambda(R0)=[2f(R0)-R0F(R0)]/4. The comparison interval generally varies this
integration datum between solutions. At ONE fixed Lambda, an open interval of
vacuum roots instead requires R F_R-F=0, hence M²=0 wherever defined. Thus the
positive-pole selection theorem does not provide freely available environments
in one universe. A source-supported comparison would need a justified source
law and separate analysis, absent here. Finite measurements cannot prove exact
interval invariance; scalar trace agreement cannot replace original tensors.

For H, the established local horizon construction adds quantum temperature,
physical conserved heat/stress, entropy density, stationarity and production.
These are not supplied by ordinary proper clocks or causal geometry. To check
its local coefficient, write S=s0 integral F(R)dA, s0>0,F>0. On an affine null
generator with endpoint0, past lambda<0 and endpoint shear0, entropy stationarity
sets q=F'+Ftheta=0. Raychaudhuri theta'=-theta²/2-R_kk gives

    q'=F''-F R_kk-(3/2)(F')²/F.

Primes here are affine derivatives. Without production the extra gradient term
prevents recovery of the target metric-f(R) null equation for generic varying F.
The specified local production density -s0 lambda(3/2)(F')²/F is nonnegative
with this orientation and cancels that term. All-null balance plus the stipulated
conserved source then has E_f as a conserved completion when F=df/dR, up to the
integration constant. This is leading local balance, not exact finite-horizon or
global thermodynamics. Other shear/entropy completions are not classified.

Constant F yields Einstein shape; choosing F=1+2alphaR yields R²; choosing a
quadratic F yields the cubic control. The entropy function has already supplied
the equation choice. Inferring it from that equation and feeding it back is not
independent physical selection. No UDT entropy observable, heat/source law or
practical independent measurement is established. The [primary-method provenance](udt_physical_selection_checkpoint_2026-10-02/REFERENCES.md)
credits Jacobson1995 and the Eling-Guedens-Jacobson2006 correction; none is a
UDT premise. The [reviewed return](udt_physical_selection_checkpoint_2026-10-02/REVIEWED_RESULT.md)
retains these hypothesis costs and distinguishing-test limits.

"""
s=s.replace('**Finite clock variation.**',response+'**Finite clock variation.**',1)
trajectory="""PSC1 makes the physical choice more explicit in R17PSC/R8PSC. S's weak response
is testable in principle but permits nonlinear completions; its stronger interval
invariance is selective only after substantial class/background commitments.
H relocates selection into a supplied entropy law and currently lacks an independent
UDT entropy/source interface. The recommendation is to retain S as a geometric
diagnostic and stop treating H as an independent R² selector; neither is adopted.
The no-change option keeps the founding interpretation and conditional comparisons.
A possible successor is a bounded feasibility study of independent curvature
readout and mode/preparation/error requirements, before any observational fit or
GPU campaign. It is not automatically authorized by this return. The [PSC1 decision
packet](udt_physical_selection_checkpoint_2026-10-02/DECISION_BRIEF.md) names
the premises, provenance, alternatives, counterevidence and exact discussion
decision. No necessary-new-postulate or complete-underdetermination claim follows.

"""
s=s.replace("NGD1's numerical return in R12N",trajectory+"NGD1's numerical return in R12N",1)
s=s.replace('includes47 later returns/clarifications','includes48 later returns/clarifications',1)
review="""PSC1 uses two fresh separate source-first contexts followed by exposed candidate
and final correspondence reviews; the prior RCD1 capacity limit did not prevent
this allocation. Shared model/Python/SymPy and parent publication/reviewer-preview
exposure remain disclosed. Parent42 exact identities check original homogeneous
tensor components, constraints, pole/classification and local entropy coefficients.
The independent stdlib saved-jet checker initially failed on a transcribed mixed
coefficient; the direct expansion repairs77760 to46656 without changing the
candidate or saved data. Original failure and repaired script/output are preserved.
After coefficient inference those parent residuals rearrange the same equations
and add no independent law evidence; reviewers reconstruct the original metric.
Reviewer reports own their additional checks and independent implementations;
counts are not independent result counts. No empirical or new evolution/GPU
test ran. [Descendant review](udt_physical_selection_checkpoint_2026-10-02/DESCENDANT_REVIEW.md)
and [execution](udt_physical_selection_checkpoint_2026-10-02/WORK_RECORD.md)
retain positive/negative scopes, actual review stages and untested axes. Actual
attestations and captured closure checks own final correspondence/pass status.

"""
s=s.replace('The preserved first candidates expose the repair history.',review+'The preserved first candidates expose the repair history.',1)
p.write_text(s);Path('CURRENT_RESEARCH_PROGRAM.md').write_text(verify.program_text(s))
for filename,start,end,title in [('LIVE.md','## CURRENT STATE','### Honest claim','CURRENT STATE'),('HANDOFF.md','## Current handoff','Protected payloads require explicit dispatch;','Current handoff')]:
 p=Path(filename);s=p.read_text();a=s.index(start);z=s.index(end,a)
 text=f"""## {title} — PSC1 physical-selection checkpoint after RCD1, 2026-10-02

CDR1 remains the central-development architecture; exact grades stay in
CURRENT_SCIENTIFIC_PREMISES.tsv. LIVE.md owns status. Verify grok HEAD, remote,
dirt and host state. Charles authorized at most two physical proposals, an
analytic pass, relevant checks, two reviews and one bounded repair/re-review,
central integration and a lay decision return. Fixed WORK_ORDER, INITIAL_CANDIDATE,
REVIEWED_RESULT, DECISION_BRIEF and WORK_RECORD are under
`udt_physical_selection_checkpoint_2026-10-02/`. UDT_DEVELOPMENT.md R8PSC/R17PSC/R18
owns the maintained argument. Both proposals and the R² equation remain UNADOPTED.
No source/action/entropy/scale, registry-grade or CANON adoption is made.

Short exact CPU checks and two actual fresh source-first/exposed reviews support
the scoped return. Parent's saved-jet transcription failure and its smallest
checker repair are preserved. Actual final reports/attestations and captured
normal,57-maintenance and full406 receipts own review/pass status. No new
evolution,GPU,observational fit or paused source/carrier campaign ran. Prior
evidence retains its original scope. No-timeout direction persists with finite,
resource and manual stops; preserve all protected payloads.

Next: Stop for lay discussion of the selection result and physical premise costs.
The proposed curvature-readout feasibility stage is not started automatically.
No new premise or horizon thermodynamics is adopted. Later sessions must verify
actual host state. Binding versions remain in development_reconstruction_2026-09-29.
Prior TPS1 raw fields/large streams remain local-only; remote compact records
cannot replay raw-dependent checks. ERC1 small arrays remain banked.

"""
 s=s[:a]+text+s[z:]
 if filename=='LIVE.md':
  a=s.index('### Next gate');z=s.index('<!-- STARTUP_CURRENT_END -->',a)
  s=s[:a]+"""### Next gate

Stop for lay discussion at PSC1's reviewed conditional proposal return. Use
central R8PSC/R17PSC/R18 and PSC1's decision brief. Strong constant-pole selection
requires an unadopted class/background premise; horizon balance does not choose
its entropy function. No automatic R² survey extension or successor. Existing
pauses and protected-work boundaries remain. Verify actual processes before
claiming host state; this checkpoint has no ongoing scientific solve.

"""+s[z:]
 p.write_text(s)
p=W/'DEVELOPMENT_GRAPH.json';g=json.loads(p.read_text());lookup={n['id']:n for n in g['nodes']};assert len(g['nodes'])==95
sources=[str(B/n) for n in ['INITIAL_CANDIDATE.md','REVIEWED_RESULT.md','REFERENCES.md','DISCOVERY_SCOPE.md']]
for f in sources:g['sources_sha256'][f]=h(f)
for name in ['R8','R9','R16','R17','R18','O_PSW_ATTRIBUTION']:lookup[name]['sources'].append(str(B/'REVIEWED_RESULT.md'))
lookup['O_PSW_ATTRIBUTION']['statement']+=' PSC1 gives two unadopted physical proposals, restricted constant-pole selection and nonlinear completion/clock controls; no native applicability or entropy/source identification follows.'
conditions=[('C_PSC_FR','conditional_class','UNADOPTED metric-f(R) comparison E_f=F Ric-fg/2+(g Box-Hess)F, F=df/dR, DDR completion with constant Lambda. Class not derived; no action/source adoption.'),('C_PSC_INTERVAL','conditional_protocol','Strong S subclaim only: actual constant-curvature backgrounds on connected open interval containing0; fixed Lambda in each perturbation, varying sectors across family; F_R!=0,R+3mu²!=0,positive constant pole mu²,F0=1. Not owner universality or actual environments in one fixed sector.'),('C_PSC_CLOCK','conditional_protocol','Clock subclaim only: f=R+alphaR²+betaR³ control, alpha!=0, regular homogeneous comoving RCD1 protocol, independent L, a0=1,H0=R0=Lambda=0,P0!=0; local f_RR!=0. Original constraint and full tensor retained.'),('C_PSC_HORIZON','conditional_protocol','Proposal H only: s0>0,F>0 entropy density, quantum temperature and conserved physical heat/source identification assumed; all-null local balance, entropy stationarity, endpoint shear0,past affine lambda<0 and stated production. Leading local order only; no UDT entropy or source adopted.')]
for id,kind,statement in conditions:g['nodes'].append({'id':id,'kind':kind,'statement':statement,'sources':[sources[0]],'registry_ids':[]})
for id,anchor,title,req in [('R8PSC','r8psc','Nonlinear completion and prepared-clock discriminator',['M_GEOMETRY','P_NULL','C_PSC_FR','C_PSC_CLOCK']),('R17PSC','r17psc','Conditional physical-selection proposals and premise costs',['M_GEOMETRY','P_DDR','C_PSC_FR','C_PSC_INTERVAL','C_PSC_HORIZON'])]:
 g['nodes'].append({'id':id,'kind':'argument','anchor':anchor,'title':title,'sources':sources,'registry_ids':[],'required_conditions':req})
 for c in req:g['edges'].append({'from':c,'to':id,'kind':'hypothesis'})
for a,b,k in [('R8RCD','R8PSC','context'),('R17ERC','R8PSC','context'),('R9','R17PSC','proof'),('R17RCD','R17PSC','context'),('O_UNIVERSAL_LAW','R17PSC','interpretation'),('R8PSC','R18','context'),('R17PSC','R18','context')]:g['edges'].append({'from':a,'to':b,'kind':k})
for rel in ['math/CANDIDATE_REVIEW.md','fidelity/CANDIDATE_REVIEW.md','DESCENDANT_REVIEW.md','IMPLEMENTATION_REPAIR.md']:
 f=str(B/rel);g['review_support'].append({'path':f,'sha256':h(f),'role':'repair_scope' if rel=='IMPLEMENTATION_REPAIR.md' else 'review_evidence','targets':['D1','R4','R5','R6','R8','R9','R10','R12','R16','R17','R18','R8RCD','R17RCD','R8PSC','R17PSC','O_PSW_ATTRIBUTION']})
p.write_text(json.dumps(g,indent=2)+'\n')
p=W/'RECENT_DISPOSITIONS.tsv';rows=list(csv.DictReader(p.open(),delimiter='\t'));assert len(rows)==47
row={'id':'PSC1_RETURN','source':str(B/'REVIEWED_RESULT.md'),'current_scope':'VERIFIED-WITH-CAVEATS_UNADOPTED_PHYSICAL_PROPOSALS; weak pole nonselection, restricted interval-pole quadratic selection, nonlinear clock discriminator, horizon entropy premise costs; no native law/source/entropy adoption','central_location':'R8;R9;R16;R17;R18;R8PSC;R17PSC','rederivation_depth':'EXACT_ORIGINAL_TENSOR_AND_JET_CHECKS; analytic interval classification and fixed-Lambda caveat; local entropy balance; two fresh source-first/exposed reviews; preserved checker repair; no new evolution/observations','source_sha256':h(B/'REVIEWED_RESULT.md')}
with p.open('a',newline='')as f:csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n').writerow(row)
print(json.dumps({'source_pins':len(g['sources_sha256']),'nodes':len(g['nodes']),'edges':len(g['edges']),'review_support':len(g['review_support']),'later_returns':48}))
