"""Scoped FCW1 central integration; actual final review/binding is separate."""
from pathlib import Path
import json,csv,hashlib,sys
sys.path.insert(0,str(Path.cwd()))
import verify_udt_development as verify
B=Path('udt_finite_comparison_whiteboard_2026-10-03');W=Path('development_reconstruction_2026-09-29')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
p=Path('UDT_DEVELOPMENT.md');s=p.read_text();assert '<a id="r8fcw">' not in s
s=s.replace('PSC1, CMF1 and CBR1, 2026-10-03','PSC1, CMF1, CBR1 and FCW1, 2026-10-03',1)
s=s.replace('<!-- DEVELOPMENT_ORIENTATION_END -->','''FCW1's reviewed whiteboard adds two conditional leads. A common transverse boost
exposes ECS1's aligned product mimic through a sixth-order finite echo difference;
the general invariant being measured remains open. A separately proposed regular
conformal completion forces a simple clock pole in a supplied homogeneous/comoving
sector, but leaves interior history and scale free. Scalar echo sufficiency FC
and completion regularity RG are explicit UNADOPTED trials, not consequences of
universal law or the founding asymptote. ICN1 already owns the third proposal's
exterior timing ambiguity. No native geometry/equation is selected. Discuss the
invariant echo derivation first; no successor starts automatically.
<!-- DEVELOPMENT_ORIENTATION_END -->''',1)
s=s.replace('X_max. The all-observer and sector-restricted inverse questions remain untested.','''X_max. FCW1 below now distinguishes this explicit product under a common
transverse boost. General all-observer inverse/rigidity and native-sector
questions remain open; the restricted-sheet nonuniqueness survives.''',1)
clock='''<a id="r8fcw"></a>

#### A transverse prepared-clock test of the aligned mimic — FCW1

ECS1's supplied dS2 × flat2 product reproduces its aligned clock sheet exactly.
A common transverse boost of both clocks distinguishes that particular mimic.
This answers one finite-comparison question left open above. It does not select
UDT's geometry or prove a general all-observer inverse theorem. Full local
curvature already distinguishes this product; the extra information was missed
by restricted scalar/aligned comparisons, not by every local-curvature method.

Supply g=-dt²+cosh²(kt)dx²+dy²+dz², k>0. At t=0 take U=γe0+u e2,n=e1,
γ²-u²=1; u is proper transverse velocity, v=u/γ coordinate speed. The clocks
A(s)=(γs,0,us,0), B(b)=(γb,L,ub,0) are unit geodesics. Since a'(0)=0,
the initial x-segment is a unit spacelike geodesic and transports U unchanged:
this is PSW preparation. Product null geodesics balance the dS2 proper duration
against the flat displacement. The embedding inner product gives actual local
incidence

    F(s,b,L)=cos(kL)cosh(kγs)cosh(kγb)
             -sinh(kγs)sinh(kγb)-cosh(ku(b-s))=0.

Reflection exchanges the clocks. On the regular future branch b=f(s),
p=f'(0) and q=f'(f(0)), with nearby emissions on the same fixed worldlines.
The latter is the actual later return-leg ratio, not an inverse. Put w=u²,
ℓ=kL. Original-incidence series and independent endpoint differentiation give

    log p=(w+1)ℓ²/2 +(w+1)(w+2)ℓ⁴/24
          -(w+1)(6w²-7w-16)ℓ⁶/720 +O(ℓ⁸),
    log q=3(w+1)ℓ²/2 +(w+1)(9w+10)ℓ⁴/8
          +(w+1)(194w²+527w+336)ℓ⁶/240 +O(ℓ⁸),
    D=log q-log[p/(2-p²)]=-w(w+1)²ℓ⁶/3+O(ℓ⁸).

The initial quartic conjecture failed and remains preserved. Analytic control
comes from s=Lx,b=Ly: divide F by k²L² and extend to L=0, obtaining
((y-x)²-1)/2 with derivative_y=1 at y=x+1. The analytic implicit function
theorem justifies the even expansion and derivatives at each fixed finite boost.
No uniform high-boost range or explicit finite-L error bound is claimed. At
γ=5/4,u=3/4 the dimensionless sixth-order coefficient is -1875/4096.

Trial FC, UNADOPTED, asks for one smooth single-valued q=Q(p) across all declared
events, frames, directions and small separations in a specified physical sector.
Unboosted p=sec(kL) fixes Q=p/(2-p²) on a right-neighborhood of1; boosted p
lies in that interval but q differs. Thus no alternate Q rescues FC on this
product while preserving its unboosted records. ULC1's same governing law does
not imply this scalar sufficiency: environmental information may enter a
universal law. Applying FC only to an additional positional contribution needs
an attribution not supplied here. No native-kernel or UDT refutation follows.

The product has ∇Riemann=0. With m=u e0+γe2, its curvature nevertheless gives

    R(n,U)U=-k²γ² n,
    R(n,U)n=-k²γ² U+k²γu m.

The second expression leaves the initial plane and obstructs a totally geodesic
extension; the first tidal vector alone does not establish that obstruction.
Define T(n,n)=-k²γ², W=perp R(n,U)n. In this one family the coefficient of
L^6 is T(n,n)|W|²/3; the coefficient of ℓ^6 is dimensionless. A general invariant
formula and classification are OPEN. The obstruction alone does not predict the
order of echo failure. Deriving that invariant on a declared locally symmetric
sector is the recommended discussion target, without adopting FC.

Parent original-incidence roots at60/100 digits and independent rational/general
series checks support the result; finite sampling is not a remainder certificate.
Space-form positive controls, PSW's leading1:3, Kasner's older cubic failure and
ECS1's restricted-sheet ambiguity survive. ICN1 already owns the third whiteboard
proposal's exterior conformal timing ambiguity; its attribution repair keeps that
prior and does not create a new native selector. Sources: [fixed candidate proof](udt_finite_comparison_whiteboard_2026-10-03/INITIAL_SYNTHESIS.md),
[reviewed result and dimensional clarification](udt_finite_comparison_whiteboard_2026-10-03/REVIEWED_RESULT.md),
and [positive/negative descendant review](udt_finite_comparison_whiteboard_2026-10-03/DESCENDANT_REVIEW.md).

'''
s=s.replace('<a id="r8pcc"></a>',clock+'<a id="r8pcc"></a>',1)
completion='''<a id="r16fcw"></a>

#### A proposed regular completion and a restricted clock asymptote — FCW1

Trial RG is UNADOPTED: the relevant geometry admits a regular spacelike conformal
completion gbar=Ω²g, with smooth nondegenerate gbar and nonzero timelike dΩ at
Ω=0. Founding asymptotic dilation and the working X_max meaning do not supply
this additional regularity/transversality. Examine the supplied homogeneous
sector g=-dt²+a(t)²d⃗x²=Ω(η)^-2(-dη²+d⃗x²), dη=dt/a, Ω=1/a,
a(0)=1,η(0)=0. This is RCD1's comoving-clock protocol, not generic PSW preparation;
no response equation or preferred universal observer is imposed.

A direct ray emitted atη=0 reaches the clock at calibrated initial separation
L whenη=L. Affine k=Ω²(1,1,0,0), unit U=Ω∂η and ω=-g(U,k)=Ω give
p(L)=1/Ω(L), dt/dL=p. These are the existing RCD1 conditional kinematics.
Assume Ω is C² to a finite L*, positive before it, Ω(L*)=0,Ω'(L*)=-h<0.
Writing δ=L*-L, Taylor and direct4D curvature give

    Ω=hδ+O(δ²), p=1/(hδ)[1+O(δ)],
    t=-(1/h)log(δ/δ_ref)+O(1),
    H=-Ω'→h, Hdot=-ΩΩ''→0, R=12Ω'²-6ΩΩ''→12h².

Proper time is infinite at this asymptotic endpoint; no actual reception occurs
there. In this sector the orthonormal Ricci components approach positive
constant-curvature form, without selecting the interior geometry. L* is this
emission epoch/protocol's first-arrival range in initial-distance/conformal
labels, not identified with X_max. The echo separately needs2L<L*. Neither
limit is a wall, seam, cutoff or selected physical scale. h and L* remain free
control/state parameters; c_E=1 is a unit convention, not a scale derivation.

Mere divergent slowing does not force a simple pole. For x=1-hη and Ωβ=x^β,
β=1 and2 both give finite range1/h and infinite future comoving proper time,
with p=x^-β, H=βh x^(β-1), R=6β(β+1)h²x^(2β-2). The first has
a=exp(ht); the second has a=(1+ht)², zero endpoint gradient and H,R→0.
The latter fails RG in this displayed completion and smooth finite positive
nonzero conformal gauges, not under a proved classification of all extensions.
Conversely, a positive compact interior deformation Ω=x(1+εb), b supported
away from both endpoints, preserves every initial/end germ, range and residue
while changing interior curvature. These are kinematic controls, not admitted
native solutions. RG selects neither a unique history, equation nor extra UDT
effect. Its physical justification remains open.

If |Ω''|≤M is independently justified on a final interval, Taylor bounds
|1/p-hδ|≤Mδ²/2. No such data/bound is supplied. Fitting h,L*,M to the same
finite observations would not confirm an asymptote. Protocol/congruence robustness
is a possible second derivation target before any physical RG admission. This
clock pole is not PSC1's weak-response pole. [FCW1 reviewed scope](udt_finite_comparison_whiteboard_2026-10-03/REVIEWED_RESULT.md)
retains the proofs, controls and new-hypothesis cost.

'''
s=s.replace('<a id="r17"></a>',completion+'<a id="r17"></a>',1)
needle="returns this choice without starting a successor, GPU campaign or empirical fit. The [PSC1 decision"
s=s.replace(needle,"returns this choice without starting a successor, GPU campaign or empirical fit. The [PSC1 decision",1)
# Insert current return after historical CBR/PSC decision paragraph, preserving prior chronology.
needle='decision. No necessary-new-postulate or complete-underdetermination claim follows.'
assert needle in s
s=s.replace(needle,needle+'''

FCW1 now supplies the requested finite-comparison whiteboard return in R8FCW and
R16FCW. One specific aligned mimic fails a transverse prepared echo at sixth
order; a proposed regular conformal completion fixes a restricted pole exponent
but leaves interior histories free. These are explicit conditional gains beyond
repeating a nonselection argument. FC and RG are new UNADOPTED physical trials,
not hidden consequences of universality or the founding interpretation. The
recommended next discussion is an invariant sixth-order echo derivation on a
declared locally symmetric sector, with source-preserving counterexamples and
review. That geometric investigation need not adopt FC. Completion/protocol
robustness is a second option; a physical reason for RG is still absent. The
[FCW1 decision brief](udt_finite_comparison_whiteboard_2026-10-03/DECISION_BRIEF.md)
returns these targets, alternatives and hypothesis costs. No successor, physical
adoption, field-law selection or new campaign starts automatically.''',1)
s=s.replace('includes50 later returns/clarifications','includes51 later returns/clarifications',1)
review='''FCW1 used two fresh proposer contexts and one explicitly reused operational
context after a third-fresh allocation failed; all proposals preceded peer
exposure. Two fresh final reviewer allocations then succeeded. Both independently
reconstructed the target arguments before exposure, followed by actual candidate
and final integration review. Original failed quartic conjectures, a reviewer
same-premise sixth-order extraction repair, ICN1 attribution repair and dimensional
wording clarification remain preserved. The parent21 gates include40 actual-null
incidence cases and a direct4D curvature check. Shared model/libraries and common
embedding identity limit independence; no different-formalism, human, empirical
or physical-admission review is claimed. [FCW1 work record](udt_finite_comparison_whiteboard_2026-10-03/WORK_RECORD.md)
and [descendant review](udt_finite_comparison_whiteboard_2026-10-03/DESCENDANT_REVIEW.md)
retain omissions, quantifiers and positive/negative scope. Actual final attestations
and captured required-check receipts own closure status, not this chronology.

'''
s=s.replace('The preserved first candidates expose the repair history.',review+'The preserved first candidates expose the repair history.',1)
p.write_text(s);Path('CURRENT_RESEARCH_PROGRAM.md').write_text(verify.program_text(s))
for filename,start,end,title in [('LIVE.md','## CURRENT STATE','### Honest claim','CURRENT STATE'),('HANDOFF.md','## Current handoff','Protected payloads require explicit dispatch;','Current handoff')]:
 p=Path(filename);s=p.read_text();a=s.index(start);z=s.index(end,a)
 current=f'''## {title} — FCW1 finite-comparison whiteboard return, 2026-10-03

CDR1 remains the central-development architecture; exact grades stay in
CURRENT_SCIENTIFIC_PREMISES.tsv. LIVE.md owns status. Verify grok HEAD, remote,
dirt and actual host state. Charles authorized the proposed three-perspective
whiteboard, cross-examination, short checks, independent review, integration and
lay return. Fixed evidence is under `udt_finite_comparison_whiteboard_2026-10-03/`;
UDT_DEVELOPMENT.md R8FCW/R16FCW/R18 owns the maintained argument. No physical
premise, equation, scale, registry grade or CANON adoption is made.

Proposal/cross-examination and bounded CPU checks completed. Two proposers were
fresh, one explicitly reused after allocation failure; two actual fresh final
reviewers then performed source-first/exposed reviews. Final attestations and
normal/maintenance/full406 receipts own acceptance/pass status. No GPU, empirical
fit, hardware experiment or paused source/carrier campaign ran. No-timeout
direction persists with finite/resource/manual stops. Preserve protected payloads
and existing unrelated untracked work.

Next: Stop for lay discussion of FCW1. Its decision brief recommends discussing
an invariant finite-echo derivation, with completion/protocol robustness as a
second option. Neither starts automatically; the proposed FC/RG conditions remain
UNADOPTED. A clock anomaly is not the project objective. Later sessions verify
actual processes. Bindings remain in development_reconstruction_2026-09-29.
TPS1 raw fields/large streams remain local-only; remote compact records cannot
replay raw-dependent checks. FCW1 evidence is banked only when actual commit/push
and exact-byte checks have completed.

'''
 s=s[:a]+current+s[z:]
 if filename=='LIVE.md':
  a=s.index('### Next gate');z=s.index('<!-- STARTUP_CURRENT_END -->',a)
  s=s[:a]+'''### Next gate

Stop for lay discussion of the FCW1 conditional whiteboard return. Use central
R8FCW/R16FCW/R18 and its decision brief. Native geometry/response and positional
attribution remain open. No automatic successor, physical premise adoption,
GPU/data campaign or hardware experiment. Existing pauses/protected boundaries
remain; verify actual processes before claiming host state.

'''+s[z:]
 p.write_text(s)
g=json.loads((W/'DEVELOPMENT_GRAPH.json').read_text());assert len(g['nodes'])==109
sources=[str(B/f) for f in ['INITIAL_SYNTHESIS.md','REVIEWED_RESULT.md','consistency/INITIAL_PROPOSAL.md','relational/INITIAL_PROPOSAL.md','operational/ATTRIBUTION_REPAIR.md']]
for f in sources:g['sources_sha256'][f]=sha(f)
lookup={n['id']:n for n in g['nodes']}
for key in ['R8','R16','R18','R8ECS','R8ECSM','O_PSW_ATTRIBUTION']:
 if key in lookup:lookup[key]['sources'].append(str(B/'REVIEWED_RESULT.md'))
lookup['O_PSW_ATTRIBUTION']['statement']+=' FCW1 net echo discrimination does not attribute an additional positional component; FC/RG remain unadopted physical trials.'
for ident,kind,statement in [
 ('C_FCW_ECHO','conditional_protocol','Supplied dS2 x flat2 metric, PSW parallel free-clock preparation with common transverse boost, local regular actual first/return branches, fixed finite boost and small L. FC scalar sufficiency is the UNADOPTED trial being tested, not an inherited law.'),
 ('C_FCW_RG','conditional_protocol','UNADOPTED regular completion, checked only in supplied flat homogeneous conformal sector with ordinary comoving clocks: positive Omega, initial normalization, C2 simple endpoint zero with negative nonzero derivative. No selected native history/scale/X_max.'),
 ('O_FCW_ADMISSION','open_join','Physical justification/adoption of FC or RG, general invariant echo formula/rigidity, generic completion/protocol robustness and native geometry/scale remain OPEN. No next target starts automatically.')]:
 g['nodes'].append(dict(id=ident,kind=kind,statement=statement,sources=sources,registry_ids=[]))
for ident,anchor,title,req in [('R8FCW','r8fcw','Transverse finite echo discriminates the explicit aligned product mimic',['C_FCW_ECHO']),('R16FCW','r16fcw','Conditional regular completion fixes a restricted clock asymptote',['C_FCW_RG'])]:
 g['nodes'].append(dict(id=ident,kind='argument',anchor=anchor,title=title,sources=sources,registry_ids=[],required_conditions=req))
 for c in req:g['edges'].append({'from':c,'to':ident,'kind':'hypothesis'})
for a,b,k in [('R6','R8FCW','proof'),('R7','R8FCW','context'),('R8ECS','R8FCW','proof'),('R8ECSM','R8FCW','context'),('R8RCD','R16FCW','proof'),('R16','R16FCW','context'),('R8FCW','R18','context'),('R16FCW','R18','context'),('O_FCW_ADMISSION','R8FCW','open_boundary'),('O_FCW_ADMISSION','R16FCW','open_boundary'),('O_PSW_ATTRIBUTION','R8FCW','open_boundary')]:
 assert a in {n['id'] for n in g['nodes']},a
 g['edges'].append({'from':a,'to':b,'kind':k})
for rel in ['review_math/EXPOSED_REVIEW.md','review_fidelity/EXPOSED_REVIEW.md','DESCENDANT_REVIEW.md']:
 f=str(B/rel);g['review_support'].append(dict(path=f,sha256=sha(f),role='review_evidence',targets=['R7','R8','R16','R18','R8ECS','R8ECSM','R8RCD','R8FCW','R16FCW','O_PSW_ATTRIBUTION','O_FCW_ADMISSION']))
(W/'DEVELOPMENT_GRAPH.json').write_text(json.dumps(g,indent=2)+'\n')
p=W/'RECENT_DISPOSITIONS.tsv';rows=list(csv.DictReader(p.open(),delimiter='\t'));assert len(rows)==50
row=dict(id='FCW1_RETURN',source=str(B/'REVIEWED_RESULT.md'),current_scope='VERIFIED-WITH-CAVEATS_CONDITIONAL_FINITE_COMPARISON; transverse product echo fails scalar Q at sixth order; UNADOPTED regular completion fixes restricted simple pole but not history/scale; no native selection',central_location='R7;R8;R16;R18;R8ECS;R8ECSM;R8RCD;R8FCW;R16FCW',rederivation_depth='EXACT_ORIGINAL_NULL_INCIDENCE_AND_METRIC_CURVATURE; analytic local remainder, matched-p rejection and C2 asymptote with beta/bump controls; two fresh source-first/exposed reviews; failures and attribution repair retained',source_sha256=sha(B/'REVIEWED_RESULT.md'))
with p.open('a',newline='') as f:csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n').writerow(row)
print(json.dumps(dict(nodes=len(g['nodes']),edges=len(g['edges']),sources=len(g['sources_sha256']),review_support=len(g['review_support']),later_returns=51)))
