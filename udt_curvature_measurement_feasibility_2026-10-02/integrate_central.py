"""Apply CMF1 once; final review/banking are separate operations."""
from pathlib import Path
import csv,json,hashlib
import verify_udt_development as verify
B=Path('udt_curvature_measurement_feasibility_2026-10-02');W=Path('development_reconstruction_2026-09-29')
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
p=Path('UDT_DEVELOPMENT.md');s=p.read_text();assert '<a id="r8cmf">' not in s
s=s.replace('RCD1 and PSC1, 2026-10-02','RCD1, PSC1 and CMF1, 2026-10-02',1)
s=s.replace('<!-- DEVELOPMENT_ORIENTATION_END -->','''CMF1 supplies an ideal measurement interface: seven prepared timelike clock-frame
contractions recover scalar curvature without a response equation. Independently
calibrated geodesic space/time sampling can then estimate Box R, with explicit
noise/truncation requirements. The quadratic candidate's exact scalar trace gives
a necessary test without an adjustable background family; it does not verify
the full tensor equation or establish source-free applicability. Practical
precision, informative physical preparation and positional attribution remain
OPEN. This is a conditional test protocol, not a measured UDT result or adoption.
<!-- DEVELOPMENT_ORIENTATION_END -->''',1)
clock='''<a id="r8cmf"></a>

#### Measuring the curvature independently — CMF1

PSW1's exact parallel-prepared free-clock protocol gives c(U)=Ric(U,U) through
the limiting outgoing triad mean. In a supplied orthonormal tetrad (u,e_i),
choose 0<v<1 and U_i±=gamma(u±v e_i), gamma²=1/(1-v²). Tensor contraction gives

    c_i+ + c_i−=2gamma²[c0+v² Ric_ii],
    R=sum_i(c_i+ + c_i−)/(2gamma²v²)−(1+3/v²)c0.

Thus seven frame types suffice for scalar R independently of a response equation.
At the illustrative v²=1/3, R=sum_six c_i±−10c0. Every frame needs its own
spatial triad, proper-distance/parallel preparation and differential received-tick
measurement at the same event. This is21 directional limiting coefficients,
not21 finite readings, an optimal design or full tensor tomography. Three spatial
off-diagonal Ricci components remain undetermined. Boosts, distances and event
matching must be independently calibrated. No preferred observer is selected.
The ultrastatic product -dt²+h_K, with3D sectional curvature K, has zero electric
tides and unit stationary tick ratios while R=6K; one frame's complete tidal form
therefore does not determine R. This is an off-equation geometric control.

If each log ratio has combined readout/preparation error at most epsilon_y and
geometric remainder bounded by B L³, each c estimate has error at most
6(epsilon_y/L²+B L). With common bounds, the scalar error is at most
(6/v²−2)6(epsilon_y/L²+B L)+E_frame. Frame/ruler errors not already included
need the separate E_frame bound. B is query dependent and independently supplied;
smoothness gives existence locally, not its measured value. Small boosts amplify
errors; high boosts change preparation and remainder costs. No optimum is proved.
Flat residual radial velocity w gives log p=atanh(w), so an uncontrolled Doppler
term can imitate or overwhelm the L² curvature coefficient. Fixed noise cannot
be cured by L→0. Freely falling test-clock preparation/backreaction is idealized;
no existing instrument or physical source/excitation is certified.

Scalar R at one event supplies no derivatives. Independently establish geodesic
placements exp_o(±h e_a), a=0..3, with e0 timelike, and reconstruct R at those
eight endpoints and the central event. Along a geodesic its second derivative
is the Hessian contraction. Consequently

    D_h R=[−R(+he0)−R(−he0)+sum_i(R(+he_i)+R(−he_i))−4R(o)]/h²

converges to Box_g R. The proper steps, tetrad and geodesic placements are extra
metric/ruler/transport information; scalar reconstruction alone does not supply
them. Results may be collected later; no instantaneous/advanced signaling is
assumed. Arbitrarily accelerated paths require removal of acceleration times
scalar gradient. For per-event scalar error epsilon_R and directional fourth-
derivative bounds B_a, the deterministic error is at most

    12epsilon_R/h²+(h²/12)sum_a B_a+E_place.

The shared central reading has weight−4; this bound assumes no independent noise.
For a joint ideal limit, epsilon_R=o(h²), bounded B_a and E_place→0 suffice.
At fixed nondegenerate boosts, sufficient PSW scaling is L=o(h²),
epsilon_y=o(L²h²), E_frame=o(h²), using dimensionless distances in fixed units.
R in C4 (for example g in C6) supports the stencil. These are requirements, not
demonstrated experimental resources. Finite smooth samples without derivative
bounds cannot certify a limiting jet. The measured scalar is total curvature;
its native positional attribution J1 remains OPEN.

Sources: [fixed initial construction](udt_curvature_measurement_feasibility_2026-10-02/INITIAL_CANDIDATE.md),
[controlling precision record](udt_curvature_measurement_feasibility_2026-10-02/REPAIR.md)
and [conditional return](udt_curvature_measurement_feasibility_2026-10-02/REVIEWED_RESULT.md).

'''
s=s.replace('## 6. Response restrictions and an optional conditional dynamics branch',clock+'## 6. Response restrictions and an optional conditional dynamics branch',1)
response='''<a id="r17cmf"></a>

**Independent necessary response test — CMF1.** For the same UNADOPTED
quadratic source-free comparison E_f+Lambda g=0, f=R+alphaR², constants
alpha!=0,Lambda, its exact trace is

    6alpha Box_g R−R+4Lambda=0.

This inherited equation holds beyond a homogeneous or linearized sector.
CMF1 adds the independent measurement interface in R8CMF, not a new response.
Let Q=Box_g R. Two events with Delta R!=0 and Delta Q!=0 determine
alpha=Delta R/(6Delta Q), Lambda=(R1−6alpha Q1)/4. Further independent events
must obey the same affine relation Q=M²(R−4Lambda), M²=1/(6alpha).
Two-point fitting supplies no confirmation. Positive alpha requires a positive
slope; Delta R!=0 with Delta Q=0 rejects all finite alpha. Equal sampled R with
unequal Q rejects alpha!=0; equal R and Q at two events leaves a parameter line.
Only constancy of R on an open region forces Q=0, Lambda=R/4 and leaves alpha
undetermined. Near-zero differences make parameter recovery ill-conditioned.
With per-event bounds epsilon_R,epsilon_Q and |Delta R|>2epsilon_R,

    |M_hat²−M²|<=(2epsilon_Q+2|M²|epsilon_R)/(|Delta R|−2epsilon_R).

The exact trace test avoids a tunable background family or monochromatic mode;
informative variation, independent measurements/derivative bounds and the
stipulated source-free sector are still required. No physical source-free
certificate or way to excite such a state is supplied. Unknown forcing can
imitate any different scalar-response coefficient, so geometry data alone do
not separate an unrestricted source from the law. No source model is adopted.

Scalar agreement is necessary, not sufficient: R8PSC's a=sqrt(1+2ht),h!=0,
Lambda=0 has R=0 and passes the trace while original E00=3H²!=0. Seven-frame
scalar readout does not supply all remaining tensor components. A failure tests
this candidate plus the stated preparation/sector, not the UDT founding premise.
Inferring geometry/distances using the tested equation would make the test circular.

PSC1's general-f(R) weak pole still needs independently matched constant-curvature
Einstein background, linear remainder and source/mode controls. Delta R is
first-order gauge invariant for constant background R; a varying background
needs relational matching. Flat dispersion and radial exponential profiles are
restricted to flat/controlled-flat settings, not arbitrary curved backgrounds.
One temporal frequency without spatial-wave-number information cannot identify
the pole. Neither the exact trace test nor finite observations establish PSC1's
strong positive-pole invariance over an open background interval. Its fixed-Lambda
obstruction and nonlinear weak-pole nonselection remain unchanged.

R8PSC's quartic/quintic clock test retains the stronger spatially flat homogeneous,
comoving, independently measured L and H0=R0=Lambda=0,P0!=0 preparation. Generic
PSW or astronomical records do not provide it. Isolating b4 or b5 amplifies
log-clock error respectively as L^-4 or L^-5, with independent lower-order,
distance and Taylor-remainder control also needed. Echo kinematics and generated
affine fixtures are not independent law evidence. No empirical/native selection,
new physical premise, response normalization or practical instrument result follows.

'''
s=s.replace('**Finite clock variation.**',response+'**Finite clock variation.**',1)
old='''A possible successor is a bounded feasibility study of independent curvature
readout and mode/preparation/error requirements, before any observational fit or
GPU campaign. It is not automatically authorized by this return.'''
new='''CMF1 now supplies that bounded feasibility result in R8CMF/R17CMF: ideal scalar
readout and a necessary exact trace test survive, with practical preparation,
precision and source applicability still open. A possible next step is a small
CPU reconstruction from independently generated clock/ruler records, with fixed
noise/truncation tests and separate full-tensor controls. That would test numerical
recoverability, not physical feasibility or native selection; it has not run.
Alternatively return to the native positional-attribution question. No GPU,
observational fit or new physical premise is automatically authorized.'''
assert old in s;s=s.replace(old,new,1)
s=s.replace('includes48 later returns/clarifications','includes49 later returns/clarifications',1)
review='''CMF1 uses two fresh separate source-first contexts and exposed candidate/final
reviews. Source-first exposure includes the parent's reconstruction question and
later exact-trace formula; independent derivation is not blind origination.
Parent32 exact identities plus rank/weight/nonzero controls, independently authored
symbolic and stdlib rational checks, and saved metric-jet reconstruction support
the scoped mathematical interface. The initial parent parse failure is retained.
One precision pass states joint limits, separates two synthetic controls and
clarifies finite-sample degeneracy without changing equations or tolerances.
All contexts share the inherited model/Python; no different-model, human, formal
or instrument validation is claimed. [Descendant review](udt_curvature_measurement_feasibility_2026-10-02/DESCENDANT_REVIEW.md)
and [execution](udt_curvature_measurement_feasibility_2026-10-02/WORK_RECORD.md)
retain positive/negative scopes, exposure and omissions. Actual final attestations
and captured normal/maintenance/full406 checks own correspondence and pass status.

'''
s=s.replace('The preserved first candidates expose the repair history.',review+'The preserved first candidates expose the repair history.',1)
p.write_text(s);Path('CURRENT_RESEARCH_PROGRAM.md').write_text(verify.program_text(s))
for filename,start,end,title in [('LIVE.md','## CURRENT STATE','### Honest claim','CURRENT STATE'),('HANDOFF.md','## Current handoff','Protected payloads require explicit dispatch;','Current handoff')]:
 p=Path(filename);s=p.read_text();a=s.index(start);z=s.index(end,a)
 text=f'''## {title} — CMF1 curvature measurement feasibility after PSC1, 2026-10-02

CDR1 remains the central-development architecture; exact grades stay in
CURRENT_SCIENTIFIC_PREMISES.tsv. LIVE.md owns status. Verify grok HEAD, remote,
dirt and actual host state. Charles authorized the bounded feasibility study,
analytic checks, two fresh reviews and one source-preserving precision pass,
central integration and lay return. Fixed evidence is under
`udt_curvature_measurement_feasibility_2026-10-02/`. UDT_DEVELOPMENT.md
R8CMF/R17CMF/R18 owns the maintained argument. No equation, source, scale,
entropy, registry grade or CANON adoption is made.

Short exact CPU checks and actual source-first/exposed reviews support this
conditional return. The initial parse failure and scoped clarification are
preserved. Actual final reports/attestations and normal/maintenance/full406
receipts own acceptance/pass status. No GPU, evolution, observational fit,
hardware experiment or paused source/carrier campaign ran. No-timeout direction
persists with finite/resource/manual stops. Preserve all protected payloads.

Next: Stop for lay discussion of CMF1. No successor has started automatically;
the proposed small CPU measurement-reconstruction benchmark needs its own scope.
Physical/native applicability remains open. Later sessions must verify processes.
Bindings remain in development_reconstruction_2026-09-29. TPS1 raw fields/large
streams remain local-only; remote compact records cannot replay raw-dependent
checks. ERC1 small arrays remain banked.

'''
 s=s[:a]+text+s[z:]
 if filename=='LIVE.md':
  a=s.index('### Next gate');z=s.index('<!-- STARTUP_CURRENT_END -->',a)
  s=s[:a]+'''### Next gate

Stop for lay discussion at CMF1's conditional feasibility return. Use central
R8CMF/R17CMF/R18 and the CMF1 decision brief. No physical experiment, source-free
certificate, full tensor validation or native law follows from the ideal protocol.
No automatic GPU/data campaign or successor. Existing pauses/protected boundaries
remain; verify actual processes before claiming host state.

'''+s[z:]
 p.write_text(s)
g=json.loads((W/'DEVELOPMENT_GRAPH.json').read_text());lookup={n['id']:n for n in g['nodes']}
assert len(g['nodes'])==101
sources=[str(B/f) for f in ['INITIAL_CANDIDATE.md','REPAIR.md','REVIEWED_RESULT.md','DISCOVERY_SCOPE.md','REFERENCES.md']]
for f in sources:g['sources_sha256'][f]=h(f)
for key in ['R8','R9','R16','R17','R18','O_PSW_ATTRIBUTION']:lookup[key]['sources'].append(str(B/'REVIEWED_RESULT.md'))
lookup['O_PSW_ATTRIBUTION']['statement']+=' CMF1 reconstructs total scalar curvature under supplied clock preparation; no positional attribution or physical source-free sector is established.'
conditions=[('C_CMF_PREP','conditional_protocol','PSW1 smooth Lorentz4 parallel-prepared free test clocks, ordinary proper time, regular future-null derivatives and same-event calibrated tetrads; independent initial distances/boosts; seven frame types at 0<v<1.'),('C_CMF_ERRORS','conditional_protocol','Derivative/finite-error subclaims only: independently calibrated exponential geodesic placements and proper steps, bounded R C4 directional derivatives, bounded clock/frame/placement errors with stated joint limits. No instrument capability derived.'),('C_CMF_TRACE','conditional_class','Exact trace subclaim only: UNADOPTED source-free metric f=R+alphaR² equation with constant finite alpha!=0,Lambda; informative independently measured R,Box R. Trace necessary not sufficient, no physical source certificate.')]
for key,kind,statement in conditions:g['nodes'].append({'id':key,'kind':kind,'statement':statement,'sources':sources[:3],'registry_ids':[]})
for key,anchor,title,req in [('R8CMF','r8cmf','Independent scalar-curvature clock and derivative readout',['M_GEOMETRY','P_NULL','C_CMF_PREP','C_CMF_ERRORS']),('R17CMF','r17cmf','Necessary exact trace test and feasibility limits',['M_GEOMETRY','C_CMF_TRACE','C_CMF_ERRORS'])]:
 g['nodes'].append({'id':key,'kind':'argument','anchor':anchor,'title':title,'sources':sources,'registry_ids':[],'required_conditions':req})
 for c in req:g['edges'].append({'from':c,'to':key,'kind':'hypothesis'})
for a,b,k in [('R8','R8CMF','proof'),('R8CMF','R17CMF','context'),('R17PSC','R17CMF','context'),('R8PSC','R17CMF','context'),('R8RCD','R17CMF','context'),('R8CMF','R18','context'),('R17CMF','R18','context')]:g['edges'].append({'from':a,'to':b,'kind':k})
for rel in ['math/CANDIDATE_REVIEW.md','fidelity/CANDIDATE_REVIEW.md','DESCENDANT_REVIEW.md']:
 f=str(B/rel);g['review_support'].append({'path':f,'sha256':h(f),'role':'review_evidence','targets':['R8','R9','R16','R17','R18','R8RCD','R8PSC','R17PSC','R8CMF','R17CMF','O_PSW_ATTRIBUTION']})
(W/'DEVELOPMENT_GRAPH.json').write_text(json.dumps(g,indent=2)+'\n')
p=W/'RECENT_DISPOSITIONS.tsv';rows=list(csv.DictReader(p.open(),delimiter='\t'));assert len(rows)==48
row={'id':'CMF1_RETURN','source':str(B/'REVIEWED_RESULT.md'),'current_scope':'VERIFIED-WITH-CAVEATS_CONDITIONAL_IDEAL_MEASUREMENT; seven-frame scalar curvature and geodesic Box readout/error requirements; necessary exact quadratic trace test; practical/source/native applicability OPEN; equation UNADOPTED','central_location':'R8;R9;R16;R17;R18;R8CMF;R17CMF','rederivation_depth':'EXACT_GEOMETRIC_LINEAR_ALGEBRA_AND_STENCIL; independent saved metric/tensor checks; two fresh source-first/exposed contexts; scoped joint-limit/control-metadata repair; no real experiment, data or evolution','source_sha256':h(B/'REVIEWED_RESULT.md')}
with p.open('a',newline='') as f:csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n').writerow(row)
print(json.dumps({'nodes':len(g['nodes']),'edges':len(g['edges']),'sources':len(g['sources_sha256']),'review_support':len(g['review_support']),'later_returns':49}))
