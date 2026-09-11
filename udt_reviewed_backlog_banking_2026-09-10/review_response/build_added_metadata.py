"""Pin added finite metrology mathematics and design-control dispositions."""
import datetime
import hashlib
import json
from pathlib import Path
out=Path(__file__).resolve().parent
repo=out.parent.parent
sha=lambda p:hashlib.sha256((repo/p).read_bytes()).hexdigest()
tm='udt_tidal_measurement_feasibility_campaign_2026-09-07'
co='udt_complementary_wave_observable_campaign_2026-09-07'
rows=[
dict(id='TM1',candidate=tm+'/step_01/CANDIDATE_ARGUMENT.md',result=tm+'/step_01/review/VERDICT.json',
    reviews=[tm+'/step_01/review/DIRECT_ADVERSARIAL_REVIEW.md',tm+'/step_01/review/FOCUSED_REVIEW.md'],
    repairs=[tm+'/step_01/REPAIR_RECORD.md',tm+'/step_01/CANDIDATE_FREEZE.md',tm+'/step_01/SOURCE_ACCESS_AND_EXPOSURE.md'],
    required_source_ids=['G313','G358','G312'],required_candidate_ids=[],
    source_roles={'G313':'connected scalar constancy within conditional Einstein equation class','G358':'explicit Q slot convention and ideal E trace','G312':'CURRENT filter-only qualifier, not old stronger adoption','G261/W4':'WORKING physical-metric interpretation, not device derivation','ESA E1/E2/E3':'historical engineering/source-audit credit; supplied ideal map is independently derived conditional kinematics, no current release certification'},
    statement='For the specified ideal local rotating held-pair instrument map with positive signed-axis baselines L and calibrated half-acceleration differences Ad, S=2Ad L^-1=T+Omega2+dotOmega, T=sym(S)-Omega2, dotOmega=skew(S), tr(T)=tr(S)+2|omega|2. Additive D and angular-rate error deltaomega give trace error tr(D)+4omega.dot(deltaomega)+2|deltaomega|2. In the conditional connected Einstein class, kappa=tr(T)=-c_E2*Lambda. The scalar channel kappa+b aliases an unknown constant bias; fixed linear H with H1=0 erases all constant signal. These are conditional interface/identifiability statements.',
    assumptions=['supplied ideal infinitesimal/comoving/slow-relative-motion metrology map','specified Q/Jacobi sign and calibrated units','full matrices, correct signed baseline/pair order and half-difference factor2','Einstein equation with full reviewed premises for kappa constancy','fixed LINEAR processing H'],
    exclusions=['GOCE released-channel eligibility OPEN','no finite-body/baseline/nongravitational/relativistic/calibration error bound supplied','no modern processing audit or flight data','no physical device derivation/adoption or empirical result','historical engineering sign conflicts are retained, not used to pick favorable convention'],
    review_context='/root/tidal_tm1_review',
    review_axes='Actual fresh source-first symbolic rotating-frame argument followed by independent Fraction direct-force reconstruction; original author replay shared-code regression. Later focused review same exposed context. Model UNKNOWN; different-model/human/formal axes UNTESTED.',
    history=['Initial candidate589eff... incorrectly asserted H1=0 for unrestricted H; nonlinear H(x)=x(x-1) is preserved counterexample. Sole exact phrase repair to fixed linear H yields final680378...; focused review closed it. Direct11 checks include1 author-output packaging check; focused11 are authentication, not proof. Source retrieval incidentally exposed qualitative historical performance prose; no pristine observational blindness. Old ESA sign/yy transcription and unavailable full2018 algorithm remain in source history.'],
    replays=['TM1','TM1_repair']),
dict(id='TM2',candidate=tm+'/step_02/CANDIDATE_ARGUMENT.md',result=tm+'/step_02/review/VERDICT.json',
    reviews=[tm+'/step_02/review/DIRECT_ADVERSARIAL_REVIEW.md'],
    repairs=[tm+'/step_02/CANDIDATE_FREEZE.md',tm+'/step_02/review/AUTHOR_MUTATIONS.json'],
    required_source_ids=['G313','G358','G312'],required_candidate_ids=['TM1'],
    source_roles={'TM1':'reviewed conditional trace/interface interpretation and retained eligibility/source limits','G313/G358':'conditional constant trace with explicit convention','G312':'current filter-only equation qualification','finite linear algebra':'methods directly proved, not an adopted nuisance law'},
    statement='For fixed finite linear y=P(kappa*1+N*beta+delta)+epsilon with PRE-P nuisance N, p=P1,Q=PN,M=[p Q], scalar kappa is noiseless-identifiable iff p not in col(Q), conditional on consistency. A complete left annihilator C has ker C=col M and genuine departure-response rank rank(CP)=rank(P)-rank(M); a specified departure is distinguishable iff CPdelta!=0. Entire heldout B prediction from consistent A is unique iff ker(MA) subset ker(MB), equivalently MB=K MA. Fixed residual [-K I] obeys triangle/error-covariance bounds with training errors and correlations retained; signal exceeding twice the justified null bound is sufficient for guaranteed rejection. Chosen four-time affine-drift examples demonstrate calibration/test distinction and exact blind designs.',
    assumptions=['fixed P/N with nuisance BEFORE P','finite registered query design, no nonlinear/adaptive unknown gain unless valid reduction supplied','noiseless consistency for uniqueness statements','fixed A/B partition/K, independently justified recorded error or covariance for error claims','TM1 full conditional physical interpretation only'],
    exclusions=['rank(C) alone is not signal-sensitive rank','absolute scalar identification not required for a useful contrast','full B failure does not exclude all predictable B functionals','row disjointness is not raw/provenance/statistical independence','chosen affine drift not physical GOCE law; finite samples not continuous-time completeness','no modern product eligibility, power, measured Lambda or UDT-specific empirical rejection'],
    review_context='/root/tidal_tm2_review',
    review_axes='Fresh source-first Fraction linear algebra versus author SymPy; direct reconstruction from saved P/N; four actual author one-edit mutations plus four reviewer mutations were historical finite catch evidence. Same-code replay regression. Model UNKNOWN; other axes UNTESTED.',
    history=['No mathematical repair. Source-first19 groups include25 finite P/nuisance combinations. Direct21 includes6 packaging/authentication checks; author32 guards. Four historical author mutations genuinely failed but were not recreated in this banking fidelity review. TM1 exposure/repair inherited. Current direct script old349 source manifest intentionally not bypassed; source-first and author unchanged replays used, old registry separately authenticated.'],
    replays=['TM2_source','TM2_author']),
dict(id='CO1',candidate=co+'/step_01/CANDIDATE.md',result=co+'/step_01/review/REVIEW_RESULT.json',
    reviews=[co+'/step_01/review/INITIAL_REVIEW.md',co+'/step_01/review/FINAL_REVIEW.md'],
    repairs=[co+'/step_01/INITIAL_CANDIDATE.md',co+'/step_01/INITIAL_geometry_checks.py',co+'/step_01/review/focused_rereview.py'],
    required_source_ids=['G313','G312'],required_candidate_ids=[],
    source_roles={'G313':'conditional Einstein-arena zero-Lambda pp-wave predecessor','G312':'CURRENT filter-only authority; old law-adoption wording qualified','G261/W4/G276':'working metric interpretation/calibration context, not laser/instrument derivation','LC1/LC2/ORS1':'complementarity/motivation/source credit, not empirical or mathematical premises of pp-wave/null theorem','LAL/GWOSC/GCN/LVC documents':'supplied measurement/nominal-query route provenance; current releases not re-certified'},
    statement='For arbitrary smooth A(u),B(u), metric -2du dv+dx2+dy2+[A(u)(x2-y2)+2B(u)xy]du2 is exactly locally Ricci-flat with R_uiuj=[[-A,-B],[-B,A]]. In the separately supplied weak local tensor-plane-wave detector regime, E=-h_tt/(2c_E2), and frozen calibrated differential arm response D:h gives its band-limited tidal projection. For fixed real/complex N-by2 F of rank r, N-r null contrasts annihilate two arbitrary waveform values; Z has null COLUMNS. Holdout row predictability is exactly training row-space membership. For centered complex covariance and residual coefficient ROW b, variance=b C b^dagger; nonzero bias separate. Normalized null leakage <=||DeltaF||2||h||2+|q^dagger e|.',
    assumptions=['exact smooth local pp-wave geometry is conditional Einstein-branch mathematics','weak h, nearly flat planar detector patch and supplied propagation direction','supplied calibrated arm/laser/clock/delay/noise response; frozen D or explicit time-response corrections','fixed F and valid covariance/centering or deterministic bounds','full source/selection exposure declared'],
    exclusions=['not a general UDT two-polarization theorem or source waveform selection','weak approximation not exact nonlinear TT metric','no DC/full curvature/metric or joined laboratory/source reconstruction','null sees only complement of col F; arbitrary per-channel error can erase test','small frequency/rotation parameters not metrological error bounds','no product certification, observed null, physical adoption or distinct UDT signature'],
    review_context='/root/co1_geometry_review',
    review_axes='Fresh source-first Fraction linearized curvature/rational-arm and exact pp-wave metric-jet implementation; candidate outline/parent Z-typo disclosure arrived after seal. Reviewer discovered complex covariance error. Focused rerun same exposed context; model UNKNOWN, different-model/human/formal UNTESTED.',
    history=['One grouped repair: Z row/column dimension error and complex covariance orientation; valid positive-definite example gives correct3 versus erroneous1. Final centered-error/mean-bias wording completed same repair; original candidate/code/output all preserved. Added rank1 rowspace clarification is within reviewed final statement. Actual wrong producer covariance expression reinserted IN MEMORY and rejected; sourcefirst independent code plus finite checks not exhaustive. Published event/weak-Virgo and GW-triggered followup exposure retained.'],
    replays=['CO1','CO1_ppwave','CO1_repair']),
dict(id='CO2',candidate=co+'/step_02/CANDIDATE.md',result=co+'/step_02/design_run.stdout',
    reviews=[co+'/step_02/review/FINAL_REVIEW.md',co+'/step_02/review/PACKAGING_REVIEW.md'],
    repairs=[co+'/step_02/design_inputs.json',co+'/step_02/review/REVIEW_RESULT.json',co+'/step_02/review/SOURCE_FIRST_SEAL.md'],
    required_source_ids=['G312'],required_candidate_ids=['CO1'],
    source_roles={'CO1':'entire supplied weak tensor-wave/response/null/covariance class and repairs','G312':'current authority qualifies inherited Einstein language, no direct physical inference from filter','design_inputs.json':'fixed official arm decimals, nominal query/time, conventional supplied geometry','design_run.stdout nominal rotation':'SHARED supplied astrometry; independent replay does not independently certify it','saved LAL header':'byte-authenticated historical public-source snapshot; copied durably here','noise ratios/stress offsets':'chosen design controls, not observations or uncertainty bounds'},
    statement='Accepted fixed-query numerical DESIGN CONTROL for the pinned H1/L1/V1 arm decimals, nominal optical direction/GPS time and supplied saved rotation under CO1 response. Full-precision matrix has rank2, singular values about1.185937/0.211048, unweighted condition5.61929, one null q~(0.329437,0.636443,0.697433), and Virgo prediction dV=-0.472356*dH-0.912551*dL. H/L training condition7.66035; three holdouts are rescalings of one relation. Declared comparator noise ratios and27 finite sky/time stresses have only the saved finite design scope.',
    assumptions=['pinned published source decimals and nominal supplied sky/time/association','supplied ICRS-like-to-GCRS identification and saved ERFA/IERS nominal rotation','real long-wavelength frozen CO1 response','float64/scalar floating calculations and stated tolerances','hypothetical noise ratios and finite stress offsets explicitly chosen'],
    exclusions=['BANKED_CONDITIONAL_DESIGN_CONTROL, not general derived theorem or empirical strain result','shared rotation not independent astrometry/IERS verification','source decimals not exact metrology; no source retuning/arm renormalization','27 stresses not supremum uncertainty bounds','rank/condition not power/sensitivity/significance','no transfer/release/calibration covariance eligibility or current route endorsement','original next-work-order remains historical, no analysis authorized'],
    review_context='/root/co2_design_review',
    review_axes='Fresh source-first independent stdlib scalar projections/Gram eigenvalues/minors/no SVD or producer imports; shared supplied nominal rotation. Original no producer replay, no independent astrometry. Later fidelity same context. Model UNKNOWN; other axes UNTESTED.',
    history=['No CO2 science repair. Original preservation threaded-lstat failure retained and repaired with transient invocation-only Git preload control. Source fetch404 failures retained. Banking replay executes unchanged independent code successfully; every scientific JSON field EXACTLY matches saved output. Only sys.version build string differs June22→August31 Python3.10.12/GCC11.4.0; strict byte mismatch preserved and explicit comparison adjudicated. No full-stdout identity claim.'],
    replays=['CO2'])]
for row in rows:
    row['artifacts']={k:{'path':row.pop(k),'sha256':None} for k in ['candidate','result']}
    for a in row['artifacts'].values():a['sha256']=sha(a['path'])
    row['whole_reviews']=[{'path':p,'sha256':sha(p)} for p in row.pop('reviews')]
    row['whole_repair_history_and_metadata']=[{'path':p,'sha256':sha(p)} for p in row.pop('repairs')]
    row['current_registry_ownership_found']=False
    row['banking_recommendation']='ELIGIBLE_AT_EXACT_SCOPE_PENDING_PARENT_INTEGRATION'
    kind='BANKED_CONDITIONAL_DESIGN_CONTROL' if row['id']=='CO2' else 'BANKED_DERIVED_CONDITIONAL'
    row['proposed_grade']=[kind,'VERIFIED-WITH-CAVEATS','OWNER_AUTHORIZED','NOT_PHYSICAL_ADOPTION','NOT_CANON']
    row['unresolved_scientific_objections']=[]
    row['exact_runtime_model_version']='UNATTESTED'
    row['current_authority_qualification']='All inherited admitted/lawful Einstein labels are conditional on full reviewed equation/class hypotheses; current G312 is FILTER ONLY, not response-law construction input.'
    row['remaining_integration_gates']=['parent final registry/guard/current premise checks','fresh integration fidelity review','preservation/source guard checks']
payload={'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'reviewer_context':'/root/bank_response_results','review_type':'SAME_CONTEXT_EXTENDED_SOURCE_DEPENDENCY_AND_FIDELITY',
    'candidate_count':4,'candidates':rows,
    'source_history_audit':'added_sources.stdout and added_registry_transition.stdout',
    'replay_audit':'METROLOGY_REPLAY_RESULTS.json plus added_correspondence.stdout; strict CO2 byte mismatch retained',
    'reviewer_launcher_repair':'LAUNCHER_REPAIR.md; administrative pre-execution adapter defect, no original source changed'}
with (out/'ADDED_CANDIDATES.json').open('x') as f:json.dump(payload,f,indent=2);f.write('\n')
print(json.dumps({'candidate_count':4,'mathematics':3,'design_controls':1}))
