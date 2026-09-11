"""Pin reviewed response backlog documents and exact-scope dispositions."""
import datetime
import hashlib
import json
from pathlib import Path

out = Path(__file__).resolve().parent
repo = out.parent.parent
sha = lambda p: hashlib.sha256((repo/p).read_bytes()).hexdigest()
nd = 'udt_native_response_discrimination_2026-09-09'
qc = 'udt_quiet_correspondence_campaign_2026-09-10'
gl = 'udt_gr_limit_campaign_2026-09-10'
rf = 'udt_response_foundations_campaign_2026-09-10'
rows = [
dict(id='ND1', base=nd+'/step_01', result='REVIEWED_RESULT.md', review='review/DIRECT_REVIEW.md',
     repairs=[], supplemental=[nd+'/step_02/review/CLOSEOUT_FIDELITY.md'],
     required_source_ids=['G260','G311','G312'], required_candidate_ids=[],
     source_roles={'G260':'complete four-metric angular residual and previously classified cancellation family',
        'G311':'all-pair DDR is trace-free balance of specified symmetric response',
        'G312':'specified optional Ricci-square Q plus current filter-only authority',
        'G310':'precursor credit; G311 supplies full local pair theorem',
        'G301':'response-class contrast, not assumption that Q belongs to it'},
     statement='On a connected open I in (0,infinity), f in C2(I), f>0, g=-f dt2+f^-1 dr2+r2 dOmega2, Q=TF_g(Ric g^-1 Ric)=(R/2)S. Q=0 iff f belongs to E:1+a r2+b/r or Z:1+b/r+d/r2, with no C2 interior branch switching. The declared C_ang=0 filter reduces Q-zero metrics exactly to E. Radial Ricci pair balance is blind; angular Ricci pair balance detects d!=0, but every Q contraction vanishes on Z.',
     assumptions=['complete one-function four-dimensional static spherical chart','positive radius and lapse','connected interval; C2 regularity','specified unadopted Q and explicit geometric filter'],
     exclusions=['not a general two-function/nonspherical/time-live metric classification','filter is not an adopted universal law and does not select S versus Q on E','no source/charge/content interpretation of d','no dynamics, stability, physical response selection or selected a/b/scale'],
     review_context='/root/native_response_step1_review',
     review_axes='Source-first argument; independent Fraction metric Taylor-jet to full Ricci implementation before direct candidate exposure; author scientific code/output not read in original direct review. Different model UNKNOWN/UNTESTED.',
     history=['Zero scientific/check repairs to ND1. Finite1955 assertions support algebra, not interval exhaustion. Angular-derivative corruption is one narrow control. Harmless unavailable-jq summary command disclosed. G260 author support used shared scientific utility.'],
     replays=['ND1']),
dict(id='ND2', base=nd+'/step_02', result='REVIEWED_RESULT.md', review='review/DIRECT_REVIEW.md',
     repairs=[], supplemental=[nd+'/step_02/review/CHECK_PLAN.md',nd+'/step_02/review/CLOSEOUT_FIDELITY.md'],
     required_source_ids=['G260','G311','G312'], required_candidate_ids=['ND1'],
     source_roles={'ND1':'required exact connected-interval Q solution classification','G260':'angular operator and E-family kernel','G311':'specified response DDR shape','G312':'optional Q/current authority'},
     statement='At positive f0=1+b0/r on fixed nontrivial compact K=[r-,r+] with 0<r-<r+<infinity, exact two-sided C1-in-C2 Q-solution velocities equal span{r2,r^-1} UNION span{r^-1,r^-2}; S velocities and exact/linear angular-filter intersections equal the first plane. For alpha*delta!=0, alpha*r2+delta/r2 is nonintegrable despite DQ=0; mixed Q leading coefficient is 6*alpha*delta/r4 diag(1,1,-1,-1). More generally, any actual C1-in-local-C2 Q-solution metric curve around Ricci-flat g0 necessarily has TF(N2)=0 for N=d(g^-1 Ric)/d epsilon; this is necessity only.',
     assumptions=['ND1 whole scope/history','C1 parameter curve in C2 profile topology, two-sided','fixed compact comparison window and positive background minimum','actual metric curve for general necessity'],
     exclusions=['velocity union is not linear span','general TF(N2)=0 is not metric realizability or integrability sufficiency','parameter is not physical time; no superposition principle/stability theorem','no general principal-symbol/response-law selection'],
     review_context='/root/native_response_step2_review',
     review_axes='Source-first reconstruction; independent full-coordinate SymPy Ricci/S/Q implementation written/launched before direct new candidate exposure; author Laurent-method disclosure prompted stronger implementation difference. Different model UNKNOWN/UNTESTED.',
     history=['Zero ND2 repairs.559 exact assertions; two narrow false-inference controls. Lorentz nonzero square-zero N retained. ND1 entire review inherited. Campaign Git threaded-lstat and atomic duplicate-patch-target failures were administrative, preserved, with no candidate change.'],
     replays=['ND2']),
dict(id='QC1', base=qc+'/step_01', result='REVIEWED_RESULT.md', review='review/FINAL_REVIEW.md',
     repairs=['CHECK_REPAIR.md'], supplemental=[qc+'/CLOSEOUT_CHECK_REPAIR.md',qc+'/step_02/review/CLOSEOUT_REVIEW.md'],
     required_source_ids=['G260','G312'], required_candidate_ids=[],
     source_roles={'G260':'full static spherical metric/angular identity/zero family','G312':'current filter-only authority',
         'G261':'qualified WORKING/POSIT_NOT_CANON physical interpretation, not needed for conditional supplied-metric bound',
         'LC1':'geometric lapse/acceleration definition credit, independently derived here; observations/instrument assumptions NOT inputs',
         'quiet_correspondence_direction':'direction/work-order provenance, not required mathematical theorem'},
     statement='For all C2 q on fixed K=[l,u],0<l<=1<=u,l<u, reference p=1+A*x2+B/x fixed by two supplied anchor data, continuous residual c=x2*qpp/2-q+1 with sup|c|<=epsilon and two bounded anchor errors, exact signed Green formula y=delta0*U+delta1*V+(2/3) integral_1^x (x2/s3-1/x)c(s)ds gives explicit b0,b1,b2 and D0,D1,D2 bounds through second derivative. Constant residual attains each residual-only component bound. With common p,q>=m>0, obtain log-relative ideal static clock bound [b0(x)+b0(z)]/(2m), stated lapse-gradient/proper-support-acceleration bounds retaining reference derivative control, and full aligned orthonormal sectional/tidal difference bounds with r0^-2 normalization.',
     assumptions=['fixed positive-radius window containing anchor','two supplied anchor data and bounded errors','continuous SUP residual, not samples','common positive lapse margin for nonlinear readouts','supplied areal-radius/time/frame matching, fixed r0/calibrated c_E','reference derivative bound for acceleration/gradient'],
     exclusions=['no physical residual source, tolerance or selected epsilon','no absolute-clock-ratio bound uniform over reference ratios','not equal-proper-distance matching','no uniform horizon/infinite-window/nonspherical/dynamic theorem','LC1 observations/empirical uncertainties not promoted'],
     review_context='/root/quiet_step1_review',
     review_axes='Source-first Green and separate factorized integration argument; independent symbolic full-metric geometry and stdlib direct-profile Fraction/Decimal checks; corrected author replay is shared code. Different model UNKNOWN/UNTESTED.',
     history=['Candidate unchanged. Original494 author checks included floating division and one vacuous anchor assertion; repair sympified inputs and removed vacuous assertion, corrected493. Seven of84 reviewer symbolic sanity rows are tautologies EXCLUDED.2340 Decimal60-digit probes with1e-56 rounding allowance are not exact/interval certification. QC2 closeout status51-vs46 enumeration repair is packaging only; original failure retained.'],
     replays=['QC1_symbolic','QC1_readout']),
dict(id='QC2', base=qc+'/step_02', result='REVIEWED_RESULT.md', review='review/FINAL_REVIEW.md',
     repairs=[], supplemental=[qc+'/CLOSEOUT_CHECK_REPAIR.md',qc+'/step_02/review/CLOSEOUT_REVIEW.md'],
     required_source_ids=['G260','G312'], required_candidate_ids=['QC1'],
     source_roles={'QC1':'whole bound/readout/full-curvature framework and review/repair caveats','G260':'complete metric residual','G312':'current authority'},
     statement='Two exact positive static metric sequences refute precisely stated epsilon-only uniform relative-clock moduli. GROW: p=1,q=1+n^-2*(U-1),K=[1,n],fixed anchor data and common lapse floor1, residual=n^-2 but endpoint clock quotient tends sqrt(4/3), while all sectional differences vanish uniformly. GAP: K=[1/2,1],p=1-(1/2-epsilon)/x,q=p+epsilon*(U-1),0<epsilon<=1/4, bounded reference data VARY between pairs, exact matching within each pair, positive minima2epsilon and C2/sectional differences vanish but endpoint relative clock quotient is exactly sqrt(29/24).',
     assumptions=['QC1 whole conditional definitions/history','supplied geometries, no field equation imposed on q','GROW varies domain extent','GAP varies bounded reference data and has no common positive lapse floor'],
     exclusions=['not a contradiction for one fixed positive reference on fixed K','positive margin is sufficient, not proved uniquely necessary','not physical horizon event, generic departure, dynamics, stability or UDT failure','q=p preserving and QC1 fixed-control examples survive'],
     review_context='/root/quiet_step2_review',
     review_axes='Source-first same GROW and distinct GAP witness; separately written Fraction code overlaps author method; direct symbolic implementation differs. Whole QC1 exposed as dependency; different model UNKNOWN/UNTESTED.',
     history=['No QC2 repair.24 of496 author opposite-sectional checks are dependent regression ONLY. Full four-metric derivation inherited QC1, not independently repeated in QC2. Symbolic36 identities/limits plus3 narrow catches; rational65 identities/829 probes/5 catches. Review supplementary distinct GAP family is not a new banked theorem.'],
     replays=['QC2']),
dict(id='GL1', base=gl+'/step_01', result='REVIEWED_RESULT.md', review='review/DIRECT_REVIEW.md',
     repairs=['CHECK_REPAIR.md'], supplemental=[gl+'/PACKAGING_FIDELITY_REVIEW.md'],
     required_source_ids=['G301','G311','G312'], required_candidate_ids=[],
     source_roles={'G301':'linear full-unoriented Lorentz curvature-to-symmetric-tensor basis sublemma only','G311':'DDR means TF(F)=0 for specified symmetric response','G312':'current authority and known degeneracy control','ND1/ND2':'credited degeneracy context, not required for Taylor bound'},
     statement='For one fixed finite-order Frechet-differentiable full O(1,3)-equivariant symmetric response germ on a neighborhood of zero in the declared ambient curvature-derivative product, T=TF(F) has T(0)=0, curvature-linear block a*S and zero odd-derivative blocks. Supplied ||Jj||<=Mj*epsilon^(j+2) gives uniform ||T-a*S||<=D*epsilon4+M*epsilon2*omega(M*epsilon2),omega->0. Exact DDR yields ||S||/epsilon2->0 only if fixed a!=0; approximate balance needs normalized rho->0. Optional C1,alpha derivative control gives the displayed H/(1+alpha) rate. Exact weighted homogeneity is a separately conditional consistency control.',
     assumptions=['ambient extension including unrealizable formal slots','fixed finite order/map/units/norms and full unoriented equivariance','Frechet differentiability at flat origin','supplied weighted hierarchy and small-domain bound','separate fixed a!=0 for Ricci conclusion'],
     exclusions=['no physical class membership/nonzero coefficient/scale supplied','no actual-curvature normalization without lower bound','no power rate from bare differentiability','no arbitrary-map/unbounded-boost uniformity','no metric family existence/convergence/physical GR result'],
     review_context='/root/gr_limit_step1_review',
     review_axes='Source-first proof; distinct Fraction/Kulkarni implementation with overlapping method; corrected author replay same-code only. Different model UNKNOWN/UNTESTED.',
     history=['Initial author SyntaxError before assertions, preserved in fabb3cae; one missing outer-loop/bracket repair, candidate unchanged. Reviewer34 includes1 bookkeeping:33 substantive witness checks;13 narrow catches. Constructed-curvature author6168 identities are not a full basis census.'],
     replays=['GL1']),
dict(id='GL2', base=gl+'/step_02', result='REVIEWED_RESULT.md', review='review/DIRECT_REVIEW.md',
     repairs=[], supplemental=[gl+'/PACKAGING_FIDELITY_REVIEW.md'],
     required_source_ids=['G301','G311','G312'], required_candidate_ids=['GL1'],
     required_control_candidate_ids=['ND1'],
     source_roles={'GL1':'required whole fixed-germ theorem','ND1':'required for credited included actual a=0 metric diagnostic, not positive Einstein necessity implication','G311':'specified DDR shape','G312':'current authority','Bianchi/constant scaling':'standard methods with C3/nondegeneracy hypotheses checked'},
     statement='Under all GL1 hypotheses and fixed a!=0, actual smooth balanced Lorentz metrics on common connected marked4-domain with h_epsilon=epsilon2*g_epsilon converging in C^max(m+2,3)_loc to nondegenerate Lorentz h0 necessarily have Ric(h0)=Lambda*h0 for one constant unselected Lambda. Constant-rescaling ON-frame jets carry epsilon^(j+2), supplying GL1 hierarchy; C2 continuity passes S=0 and C3 Bianchi makes scalar constant. Optional compact-local normalized approximate balance and C1,1 response rate retain exact GL1 qualifications. ND1 a=0 actual-metric and oscillatory non-DDR metric diagnostics show the stated gates cannot be silently dropped.',
     assumptions=['GL1 entire ambient/fixed-map/type/regularity scope','fixed a!=0','spatially constant normalization','common marking and nondegenerate C^max(m+2,3)_loc limit','controlled local frames','exact DDR or explicitly normalized residual o(epsilon2)'],
     exclusions=['NECESSITY only, not balanced nonflat family existence/converse/compactness/convergence theorem','no rate of metric convergence from response rate','no selected Lambda/sign/Weyl/data/physical GR recovery','oscillatory diagnostic not DDR-balanced','ND1 Q unadopted and a=0'],
     review_context='/root/gr_limit_step2_review',
     review_axes='Source-first scaling/limit argument; independent Fraction Taylor-jet warp metric versus author symbolic spherical metric, overlapping Levi-Civita method; source/candidate exposure documented; author replay shared code. Different model UNKNOWN/UNTESTED.',
     history=['No GL2 repair.58 reviewer assertions include structural zeros,3 redundant TF conversions and1 bookkeeping.17 catches include a zero-a tautology with NO evidential credit;16 narrow substantive catches. Fixed-epsilon checks do not prove arbitrary big-O failure; diverging analytic ratios do.'],
     replays=['GL2']),
dict(id='RF1', base=rf, result='DECISION_BRIEF.md', review='review/DIRECT_REVIEW.md',
     repairs=['review/CHECK_REPAIR.md'], supplemental=[rf+'/review/PACKAGING_FIDELITY.md',rf+'/SOURCE_NOTES.md',rf+'/review/REVIEW_RESULT.json'],
     required_source_ids=['G301','G311','G312'], required_candidate_ids=[],
     source_roles={'G301':'linear Lorentz contraction sublemma after explicit normal quadratic-curvature bijection','G311':'specified DDR shape','G312':'current authority','G296':'order-boundary context, not sufficient response architecture','GL1':'explicit comparative/source-credit predecessor; estimate rederived intrinsically, no ambient-extension premise imported','GL2':'potential application with remaining full hypotheses, not required for RF1','Jentsch arXiv1509.08269v2':'original checked primary corroboration; not newly web-verified or relied on instead of direct finite-order argument; Euclidean Theorem3(a) not imported'},
     preferred_predecessor_order=['GL1'],
     statement='For finite N>=2, homogeneous symmetric normal coefficients hs satisfying hs(x)(x,v)=0 form a linear space of genuine local Lorentz normal metric jets, all realized by g=eta+sum hs on sufficiently small neighborhoods. The h2 curvature map is an equivariant bijection with inverse h2_ij=-(1/3)R_i a j b*x^a*x^b. A fixed finite-order fully unoriented natural symmetric response on a full neighborhood of flat realizable normal jets, Frechet differentiable at flat, admits intrinsic T=a*S+remainder with zero odd blocks and bound D*epsilon4+M*epsilon2*omega(M*epsilon2) under ||hs||<=Ms*epsilon^s. Finite normal-coefficient and actual covariant-curvature weighted bounds are equivalent up to constants via Jacobi/coordinate polynomials retaining curvature products, including h4=eta*(2*K0^2/45-K2/20). Optional rates/DDR/nonzero-a/normalized residual conclusions have stated qualifications; no response extension to unrealizable arrays is needed.',
     assumptions=['fixed N/order/type/response/units','full open response neighborhood of flat realizable jets','full unoriented diffeomorphism naturality','Frechet differentiability at flat, separately assumed','supplied finite weighted regime','separate a!=0 for Ricci consequence'],
     exclusions=['normal metric realization is kinematic, not field-law solution','no full response neighborhood/regularity/nonzero-a from locality alone','not arbitrary curvature-array realization or infinite Taylor convergence','no balanced-family existence/convergence/physical GR limit or scale selection','sufficient gates not claimed necessary for all GR limits'],
     review_context='/root/response_foundations_review',
     review_axes='Source-first standard Jacobi/normal-jet argument, independent actual product-metric Fraction connection implementation before candidate exposure. Original parent saw reviewer code before author diagnostics; author checks therefore not blind, although rank/basis/warped-integral calculations differ. Different model UNKNOWN/UNTESTED.',
     history=['Initial reviewer Python3.10 parse failure before assertions preserved. One check repair: tuple subscription, degree5 quartic-radial retention, remove literal-sign probe. Candidate unchanged. Focused catch proves adding x0^4 to g00 falsely passed old truncation but repaired check rejects x0^5 defect.69 author categories include exact80x100 rank80/nullity20 and20-element curvature basis; finite probes do not prove all orders.25 reviewer categories include structural zeros/parity zeros and repeated product family;5 narrow probes. Original full365 raw byte stream/runtime incompletely captured, separate from preserved scientific outputs.'],
     replays=['RF1_author','RF1_independent','RF1_repair'])]

for row in rows:
    base=row.pop('base')
    paths={'candidate':base+'/CANDIDATE.md','reviewed_result':base+'/'+row.pop('result'),
        'whole_direct_review':base+'/'+row.pop('review')}
    row['artifacts']={role:{'path':path,'sha256':sha(path)} for role,path in paths.items()}
    extras=[base+'/'+p for p in row.pop('repairs')]+row.pop('supplemental')
    package=base.split('/')[0]
    extras += [package+'/EXECUTION_RECORD.md',package+'/CAMPAIGN_LOG.md',package+'/WORK_ORDER.md']
    row['whole_repair_closeout_and_history_artifacts']=[{'path':p,'sha256':sha(p)} for p in extras]
    row['original_scientific_status']='REVIEWED_CONDITIONAL_UNPROMOTED'
    row['current_registry_ownership_found']=False
    row['banking_recommendation']='ELIGIBLE_EXACT_CONDITIONAL_SCOPE_PENDING_PARENT_GLOBAL_INTEGRATION_GATES'
    row['proposed_grade']=['BANKED_DERIVED_CONDITIONAL','VERIFIED-WITH-CAVEATS','OWNER_AUTHORIZED','NOT_PHYSICAL_ADOPTION','NOT_CANON']
    row['unresolved_scientific_objections']=[]
    row['remaining_integration_gates']=['parent actual prebank/full integration premise audit','all historical source-pin differences authenticated without unrelated-source waiver','fresh integration fidelity review','source/unrelated-work preservation and authorized registry guard checks']
    row['original_model']='UNKNOWN'
    row['banking_reviewer_model']='UNATTESTED'
    row['historical_g325_failure']='PRESERVED_HISTORY_NOT_CURRENT_BLANKET_BLOCKER'
manifest_results=[]
for row in rows:
    base=str(Path(row['artifacts']['candidate']['path']).parent)
    manifests=[base+'/SOURCE_SHA256SUMS',base+'/CANDIDATE_SHA256SUMS',base+'/review/REVIEW_SHA256SUMS']
    for m in manifests:
        if not (repo/m).is_file():continue
        entries=[]
        for line in (repo/m).read_text().splitlines():
            if not line.strip():continue
            expected,p=line.split(maxsplit=1);p=p.removeprefix('*')
            actual=sha(p) if (repo/p).is_file() else None
            entries.append({'path':p,'expected':expected,'actual':actual,'match':actual==expected,
                'difference_disposition':'PARENT_AUTHENTICATED_HISTORICAL_REGISTRY_COMPARISON_REQUIRED' if p=='CURRENT_SCIENTIFIC_PREMISES.tsv' and actual!=expected else None})
        manifest_results.append({'manifest':m,'sha256':sha(m),'entries':entries})
payload={'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'reviewer_context':'/root/bank_response_results','exact_runtime_model_version':'UNATTESTED',
    'baseline_head':'f5faabb43a582fec9a71c1d4a3b065efffae25bd','review_type':'SOURCE_DEPENDENCY_AND_BANKING_FIDELITY_NOT_BLIND_REPROOF',
    'current_authority':{'path':'udt_gr_filter_reconciliation_2026-09-09/AUTHORITY_RECORD.md','sha256':sha('udt_gr_filter_reconciliation_2026-09-09/AUTHORITY_RECORD.md')},
    'candidate_count':len(rows),'candidates':rows}
for name,data in [('RESPONSE_CANDIDATES.json',payload),('ORIGINAL_MANIFEST_AUDIT.json',manifest_results)]:
    with (out/name).open('x') as f:json.dump(data,f,indent=2);f.write('\n')
print(json.dumps({'candidates':len(rows),'manifests':len(manifest_results),
    'pin_mismatches':[e for m in manifest_results for e in m['entries'] if not e['match']]}))
