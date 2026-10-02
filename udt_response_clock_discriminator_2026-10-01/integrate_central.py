from pathlib import Path
import json,csv,hashlib
import verify_udt_development as verify
B=Path('udt_response_clock_discriminator_2026-10-01');W=Path('development_reconstruction_2026-09-29')
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
p=Path('UDT_DEVELOPMENT.md');s=p.read_text()
s=s.replace('PCC1 and ERC1, 2026-10-01','PCC1, ERC1 and RCD1, 2026-10-01',1)
orientation="""RCD1 derives an exact conditional clock-curve test for ERC1's derivative equation
in its declared homogeneous/comoving sector. The flat-event cubic and fifth-order
terms determine its coefficient independently of the free initial amplitude;
the earlier exact cubic-only geometry fails this equation. Constant-H records
cannot identify that coefficient. Echo doubling is protocol information, not
independent law selection. The audited native implication remains unestablished.
Full response identity is only a sufficient route: different tensors can impose
the same geometry equation, and native clock predictions need not first select
a local response. Two reused separate contexts reviewed the result; fresh-context
allocation was unavailable. The candidate remains UNADOPTED. Stop for discussion.
"""
s=s.replace('<!-- DEVELOPMENT_ORIENTATION_END -->',orientation+'<!-- DEVELOPMENT_ORIENTATION_END -->',1)
clock="""<a id="r8rcd"></a>

#### Testing the evolving equation with clock records — RCD1

Retain R17ERC's UNADOPTED E_B equation and its explicitly imposed spatially flat
homogeneous/isotropic metric, a(0)=1, a>0, supplied comoving proper clocks and
regular first arrivals. Initial proper separation L is independently calibrated.
For first emission0, L=integral_0^t du/a(u) and p(L)=a(t(L)). The derivative of
arrival with respect to emission at fixed receiver defines the tick ratio;
differentiation over receiver locations gives dt/dL=p here. They are different
operations with equal values in this protocol, not arbitrary finite pulse ratios.
With primes=d/dL and dot=(1/p)d/dL,

    t(L)=integral_0^L p(s)ds, H=p'/p², R=6p''/p³,
    Rdot=6[p'''/p⁴-3p'p''/p⁵],
    U=3p'^2/p⁴,
    V=36p'p'''/p⁶-18p''²/p⁶-72p'^2p''/p⁷.

The original00 equation is C=U+alpha V-Lambda=0. For positive C4 p on a
connected interval and constant alpha,Lambda, C identically zero is equivalent
to all original homogeneous tensor equations. For their common spatial residual
D, the off-shell identity is Cdot=-3H(C+D). On H!=0 it gives D=0. On interiors
where H=0, a is constant and C=0 forces Lambda=0, hence D=0. All other zeros
are limits of H!=0 points, so continuity finishes the proof. Pointwise C=0 at a
turn is insufficient; no division by H,p',R,Rdot or F=1+2alpha R is licensed.

An equivalent shape equation is K+alpha J=0, with

    K=(p p''-2p'^2)/p⁴=Hdot,
    J=6[p²p''''-8pp'p'''-p(p'')²+14p'^2p'']/p⁷
     =2R Hdot+Rddot-H Rdot.

Indeed C+D=-2(K+alpha J) and dot(U+alpha V)=6H(K+alpha J).
For alpha!=0,p>0 this has nonzero fourth-derivative coefficient6alpha/p⁵,
so it is a regular local fourth-order ODE. The remaining three initial
derivatives after p0=1 encode state data; Lambda is recovered or constrains
them if fixed separately. This is not a general PDE or global stability result.

If V1!=V2, alpha=(U2-U1)/(V1-V2), Lambda=U1+alpha V1; these same constants
must pass the entire curve. Equivalently alpha=-K/J where J!=0, with K=0
required where J=0. Two-point fitting is not confirmation. Near-zero J or
nearly constant V is ill-conditioned; no noise model is tested. Compatible
constant V forces constant H, V=0 and p=1/(1-H0 L), Lambda=3H0² on its positive
branch, so those records cannot determine alpha. The alpha=0 sector has the
same form. Parameter ignorance and F=0 equation degeneracy are distinct issues.

For the nonzero-amplitude flat-event data in R8ERC,

    log p=b3 L³+b5 L⁵+O(L⁶),
    b3=P0/36, b5=-P0/(4320alpha), alpha=-b3/(120b5).

The initial amplitude cancels. By contrast, PCC1's exact supplied a=1+beta t³,
beta!=0, has b5=0 and fails every finite constant-alpha candidate: Lambda=0
is forced initially and the original00 residual starts27beta²t⁴ (the shape
residual starts6beta t). Its kinematic role and initially flat curvature survive;
this is a rejection for one equation, not a UDT countermodel or PCC1 refutation.

For every positive a in this comoving sector q(L)=p(2L)/p(L) where both arrivals
exist. Echo coefficients7b3 and31b5 are kinematic; the relation b5=-b3/(120alpha)
is candidate-specific. Independently measured echoes can check the protocol or
extend the sampled interval, but echoes computed from p add no independent law
evidence. Generic comoving clocks are not PSW's parallel preparation. Imposing
this symmetry before recovering one a(t) is not general4D metric reconstruction,
a native event/path assignment or identification of p with presentation phi.

Sources: [initial derivation](udt_response_clock_discriminator_2026-10-01/INITIAL_DERIVATION.md),
[controlling scope repair](udt_response_clock_discriminator_2026-10-01/REPAIR.md)
and [reviewed result](udt_response_clock_discriminator_2026-10-01/REVIEWED_RESULT.md).

"""
s=s.replace('## 6. Response restrictions and an optional conditional dynamics branch',clock+'## 6. Response restrictions and an optional conditional dynamics branch',1)
scope="""<a id="r17rcd"></a>

**Physical implication and response equivalence — RCD1.** The inspected
owner/kernel/DDR/locality/filter/conservation/scaling chain has not justified
ERC1's derivative equation or R8RCD's clock law as native UDT. Pair normalization
evaluates supplied data; DDR balances a specified response; local metric
sufficiency does not select derivative order; GR FILTER ONLY does not import
an action. These bounded findings do not prove complete-premise insufficiency.

Identifying E_physical=E_B is one sufficient route, not a necessary full-tensor
identity or universal prerequisite for predicting clocks. For smooth nowhere-zero
f and smooth q, TF(f E_B+qg)=f TF(E_B), so DDR has the same zero set. Variable
f,q need not preserve off-shell conservation; constant f!=0,q preserve even
that identity. This is an equivalence control, not a new physical candidate.
Clock records can test the normalized equation and its relative alpha within
this class; they cannot identify unique response normalization, pure trace,
action or mechanism. A different justified native geometric argument may predict
clocks without first choosing E. The [controlling repair](udt_response_clock_discriminator_2026-10-01/REPAIR.md)
removes that unnecessary hurdle while preserving the conditional equations.

"""
s=s.replace('**Finite clock variation.**',scope+'**Finite clock variation.**',1)
scale="""RCD1's conditional coefficient recovery in R8RCD requires an informative smooth
clock curve and an independent length/time calibration. c_E converts units;
c_E and G_obs alone still do not choose alpha. Lambda is an integration datum
and initial derivatives describe state. This does not establish a physical
source scale or the absolute normalization of a response tensor.

"""
idx=s.index('<a id="r17"></a>');s=s[:idx]+scale+s[idx:]
trajectory="""RCD1 now supplies the concrete clock relationship in R8RCD and audits its native
implication in R17RCD. State freedom does not make every curve pass the equation:
the cubic-only history is excluded, while a specific fifth-order correction
permits the flat-event candidate. The physical implication is still unestablished
in the inspected chain. The next proposal should name a justified UDT argument
or independently justified observation that can require, distinguish or reject
this relationship. More compatible curves or a coefficient fitted to the same
generated history do not do that. Response identification is one possible route,
not a universal prerequisite. The [RCD1 decision brief](udt_response_clock_discriminator_2026-10-01/DECISION_BRIEF.md)
returns the conditional discriminator for discussion, with no adoption or
automatic successor. No new premise is proved necessary.

"""
s=s.replace("NGD1's numerical return in R12N",trajectory+"NGD1's numerical return in R12N",1)
s=s.replace('includes46 later returns/clarifications','includes47 later returns/clarifications',1)
review="""RCD1 uses two actual reused separate contexts after fresh-thread allocation
failed; fresh-context review is UNAVAILABLE/NOT PASSED. Prior exposure, shared
model/SymPy and source-first/exposed phases are recorded. The parent reconstructed
52 original-metric identities and rational saved-series coefficients. Reviewers
independently checked24 and34 identities, then used series reversion and Lagrange
inversion respectively to reconstruct saved ERC1 coefficients. The parent had
seen their source-first formulas, and flagged the response-identity issue before
their actual assessments; neither third blind discovery nor blind objection
origination is claimed. Both accepted the controlling scope repair. These are
exact conditional checks, not observations, general completeness or noisy-data
inference. No new evolution/GPU survey ran. The [descendant review](udt_response_clock_discriminator_2026-10-01/DESCENDANT_REVIEW.md)
tracks positive and negative scope; [execution](udt_response_clock_discriminator_2026-10-01/WORK_RECORD.md)
and actual final reports/attestations own bindings, omissions and closure status.

"""
s=s.replace('The preserved first candidates expose the repair history.',review+'The preserved first candidates expose the repair history.',1)
p.write_text(s);Path('CURRENT_RESEARCH_PROGRAM.md').write_text(verify.program_text(s))
for filename,start,end,header in [('LIVE.md','## CURRENT STATE','### Honest claim','CURRENT STATE'),('HANDOFF.md','## Current handoff','Protected payloads require explicit dispatch;','Current handoff')]:
 p=Path(filename);s=p.read_text();a=s.index(start);z=s.index(end,a)
 text=f"""## {header} — RCD1 conditional clock discriminator after ERC1, 2026-10-01

LIVE.md owns status; verify grok HEAD, remote, dirt and actual host state.
Charles authorized the physical-connection audit and bounded exact clock test,
checks, reviews, same-premise repair and central integration. Fixed evidence is
under `udt_response_clock_discriminator_2026-10-01/`: WORK_ORDER.md, WORK_RECORD.md,
REVIEWED_RESULT.md and DECISION_BRIEF.md. UDT_DEVELOPMENT.md R8RCD/R17RCD/R18
owns the maintained argument. The derivative equation remains UNADOPTED; native
physical implication is unestablished. No source, action, scale, registry grade
or CANON changes are adopted. Prior results retain their original scope.

Short symbolic and saved-series checks are complete. Two actual reused separate
contexts performed independent argument/code reviews and reviewed one scope
repair. Fresh-context allocation failed and is UNAVAILABLE/NOT PASSED; exposure
and limits are recorded. Actual final attestations and captured normal,
57-maintenance and full406 receipts own integration/pass status. No new evolution,
GPU or long production ran. No-timeout direction persists with finite/resource/
manual stops. Preserve all protected work and prior TPS1 local-only raw caveats.

Next: stop for lay discussion of the conditional discriminator and open native
implication. No response adoption, new physical premise or successor starts
automatically. Later sessions must verify actual host state; no scientific
worker is intended to remain at return. Version/review bindings remain under
`development_reconstruction_2026-09-29/`.

"""
 s=s[:a]+text+s[z:]
 if filename=='LIVE.md':
  a=s.index('### Next gate');z=s.index('<!-- STARTUP_CURRENT_END -->',a)
  s=s[:a]+"""### Next gate

RCD1 returns for discussion. Use central R8RCD/R17RCD/R18 and its decision brief.
The exact conditional clock test does not establish native UDT applicability.
Full response identity is one sufficient route, not a universal prerequisite.
No successor or scientific adoption begins automatically; existing pauses and
protected-work boundaries remain. ERC1 arrays are banked; TPS1 raw fields and
large streams remain local-only and cannot be replayed from compact remote
records alone. Verify actual processes before claiming host state.

"""+s[z:]
 p.write_text(s)
p=W/'DEVELOPMENT_GRAPH.json';g=json.loads(p.read_text());lookup={n['id']:n for n in g['nodes']};assert len(g['nodes'])==90
sources=[str(B/n) for n in ['INITIAL_DERIVATION.md','REPAIR.md','REVIEWED_RESULT.md','math/SOURCE_FIRST.md','fidelity/SOURCE_FIRST.md','CHECK_PLAN.md']]
for f in sources:g['sources_sha256'][f]=h(f)
for name in ['R8','R9','R16','R17','R18','O_PSW_ATTRIBUTION']:lookup[name]['sources'].append(str(B/'REVIEWED_RESULT.md'))
lookup['O_PSW_ATTRIBUTION']['statement']+=' RCD1 supplies a conditional clock-curve discriminator, with native physical implication unestablished; exact full response identity is sufficient, not necessary or a universal gate.'
conds=[('C_RCD_EQUATION','conditional_class','UNADOPTED E_B=G+alpha Q with constant alpha and DDR gives E_B+Lambda g=0, constant Lambda. A sufficient response route only; no physical response normalization/action/source adoption.'),('C_RCD_CLOCK','conditional_protocol','Smooth spatially flat homogeneous/isotropic metric, a0=1,a>0, supplied comoving proper clocks, independently calibrated initial proper L, regular first arrivals at emission0. Positive C4 p on connected interval for equation equivalence; no general4D tomography or native query assignment.'),('C_RCD_FLAT_EVENT','conditional_protocol','Coefficient subclaim only: alpha nonzero,a0=1,H0=R0=Lambda=0,P0 nonzero; exact Taylor coefficients and independent unit calibration. Echo doubling kinematic; no noise inference or empirical pass.')]
for id,kind,statement in conds:g['nodes'].append({'id':id,'kind':kind,'statement':statement,'sources':[sources[0],sources[1]],'registry_ids':[]})
for id,anchor,title,required in [('R8RCD','r8rcd','Conditional clock reconstruction and equation discriminator',['P_NULL','M_GEOMETRY','C_RCD_EQUATION','C_RCD_CLOCK','C_RCD_FLAT_EVENT']),('R17RCD','r17rcd','Native implication audit and response-equivalence scope',['P_DDR','M_GEOMETRY','C_RCD_EQUATION'])]:
 g['nodes'].append({'id':id,'kind':'argument','anchor':anchor,'title':title,'sources':sources,'registry_ids':[],'required_conditions':required})
 for c in required:g['edges'].append({'from':c,'to':id,'kind':'hypothesis'})
for a,b,k in [('R17ERC','R8RCD','proof'),('R8','R8RCD','proof'),('R9','R17RCD','proof'),('R17ERC','R17RCD','context'),('O_UNIVERSAL_LAW','R17RCD','interpretation'),('R8RCD','R18','context'),('R17RCD','R18','context')]:g['edges'].append({'from':a,'to':b,'kind':k})
for rel in ['math/CANDIDATE_REVIEW.md','fidelity/CANDIDATE_REVIEW.md','fidelity/REPAIR_REVIEW.md','DESCENDANT_REVIEW.md']:
 f=str(B/rel);g['review_support'].append({'path':f,'sha256':h(f),'role':'review_evidence','targets':['D1','R4','R5','R6','R8','R9','R10','R12','R16','R17','R18','R8ERC','R17ERC','R8RCD','R17RCD','O_PSW_ATTRIBUTION']})
p.write_text(json.dumps(g,indent=2)+'\n')
p=W/'RECENT_DISPOSITIONS.tsv';rows=list(csv.DictReader(p.open(),delimiter='\t'));assert len(rows)==46
row={'id':'RCD1_RETURN','source':str(B/'REVIEWED_RESULT.md'),'current_scope':'VERIFIED-WITH-CAVEATS_UNADOPTED_CLOCK_DISCRIMINATOR; exact homogeneous clock equation and coefficient/state distinction; native implication unestablished; full response identity sufficient not necessary; no physical adoption','central_location':'R8;R9;R16;R17;R18;R8RCD;R17RCD','rederivation_depth':'ORIGINAL_METRIC_EXACT_ALGEBRA; saved rational series via three implementations; two reused separate contexts, fresh allocation unavailable; one scope repair and descendant review; no new evolution or observations','source_sha256':h(B/'REVIEWED_RESULT.md')}
with p.open('a',newline='')as f:csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n').writerow(row)
print(json.dumps({'sources':len(g['sources_sha256']),'nodes':len(g['nodes']),'edges':len(g['edges']),'review_support':len(g['review_support']),'later_returns':47}))
