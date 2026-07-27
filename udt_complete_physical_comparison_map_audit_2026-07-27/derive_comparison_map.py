#!/usr/bin/env python3
"""Exact comparison-map candidate census and bounded assembly audit."""
from __future__ import annotations
import csv,hashlib,json
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
def write(name,rows):
    with (HERE/name).open('w',newline='',encoding='utf-8') as h:
        w=csv.DictWriter(h,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
def sources():
    specs=[
      ('S01','udt_founding_reciprocity_object_audit_2026-07-27/AUDIT_REPORT.md',11,20,'718878082fd4dc545df29ac626389f957514a6463cbc61ad9a5eff58dd786bb4','covariant local relational comparison law','founding covariance does not require global rigidity'),
      ('S02','udt_founding_reciprocity_object_audit_2026-07-27/AUDIT_REPORT.md',38,62,'718878082fd4dc545df29ac626389f957514a6463cbc61ad9a5eff58dd786bb4','complete endpoint-only versus path-labelled','complete physical semantics remain open'),
      ('S03','udt_metric_native_signed_depth_availability_audit_2026-07-26/EXACT_DERIVATION.md',30,47,'ee62cc854262baddbd1f9187752233caa3a854d5df10f51acd7e04bb1e4a2fae','Endpoint theorem','endpoint-additive real cocycles are potential differences'),
      ('S04','udt_metric_native_signed_depth_availability_audit_2026-07-26/EXACT_DERIVATION.md',50,79,'ee62cc854262baddbd1f9187752233caa3a854d5df10f51acd7e04bb1e4a2fae','trace pairing','Levi-Civita connection has zero reciprocal self-adjoint projection'),
      ('S05','udt_metric_native_signed_depth_availability_audit_2026-07-26/EXACT_DERIVATION.md',81,108,'ee62cc854262baddbd1f9187752233caa3a854d5df10f51acd7e04bb1e4a2fae','reference change','raw coframe depth depends on selected reference transition'),
      ('S06','udt_metric_native_signed_depth_availability_audit_2026-07-26/EXACT_DERIVATION.md',110,147,'ee62cc854262baddbd1f9187752233caa3a854d5df10f51acd7e04bb1e4a2fae','Relative coframe logarithm','reciprocal subgroup logarithm is additive but generic noncommuting projection is not'),
      ('S07','udt_metric_native_signed_depth_availability_audit_2026-07-26/EXACT_DERIVATION.md',149,187,'ee62cc854262baddbd1f9187752233caa3a854d5df10f51acd7e04bb1e4a2fae','Bilocal magnitude','symmetric distance is not signed depth; one-form paths need period control'),
      ('S08','udt_observer_pair_path_groupoid_assembly_audit_2026-07-26/EXACT_DERIVATION.md',3,21,'7e9573e5428bb2d35145adee2ee2113a67409419f0099bed8c368d8a79490dd6','correct local object','ordered observer/ruler pair defines the local reciprocal endomorphism'),
      ('S09','udt_observer_pair_path_groupoid_assembly_audit_2026-07-26/EXACT_DERIVATION.md',23,64,'7e9573e5428bb2d35145adee2ee2113a67409419f0099bed8c368d8a79490dd6','Path transport','transport and vertical pair changes compose on typed arrows'),
      ('S10','udt_observer_pair_path_groupoid_assembly_audit_2026-07-26/EXACT_DERIVATION.md',66,91,'7e9573e5428bb2d35145adee2ee2113a67409419f0099bed8c368d8a79490dd6','Adding reciprocal depth','full path comparison composes given an additive depth cocycle'),
      ('S11','udt_observer_pair_path_groupoid_assembly_audit_2026-07-26/EXACT_DERIVATION.md',93,138,'7e9573e5428bb2d35145adee2ee2113a67409419f0099bed8c368d8a79490dd6','Path depth and periods','endpoint and path cocycle normal forms and faithful loop periods'),
      ('S12','udt_observer_pair_clock_operator_audit_2026-07-24/EXACT_DERIVATION.md',164,205,'7e03ef2631908a1e26c636bb9beb7410bdc534c9fde1e15d37eb9de5efadf29d','physical orthonormal coframe','coordinate reciprocal scaling and physical-frame transport are different types'),
      ('S13','udt_observer_pair_clock_operator_audit_2026-07-24/EXACT_DERIVATION.md',208,226,'7e03ef2631908a1e26c636bb9beb7410bdc534c9fde1e15d37eb9de5efadf29d','stationary lapse ratio','stationary lapse gives the conditional endpoint clock ratio'),
      ('S14','udt_relational_pair_depth_realization_audit_2026-07-24/AUDIT_REPORT.md',44,53,'de149d583e63dfd3977a477b4147e24c5bb388421a54cb8e66ff758436a35e5f','angular sector is unavoidable','noncollinear composition requires angular data'),
      ('S15','udt_relational_pair_depth_realization_audit_2026-07-24/AUDIT_REPORT.md',82,115,'de149d583e63dfd3977a477b4147e24c5bb388421a54cb8e66ff758436a35e5f','Cut-locus result','scalar cut-locus depth and full frame transport have different multiplicity'),
      ('S16','udt_complete_nonultrastatic_reciprocal_branch_audit_2026-07-27/EXACT_DERIVATION.md',53,86,'36e22610ec03dc4421e005f0a327be288cde000fb5fa63f4d8ea9cec3711875d','Stationary clock depth','intrinsic Killing line supplies normalized metric-native endpoint depth'),
      ('S17','udt_complete_nonultrastatic_reciprocal_branch_audit_2026-07-27/EXACT_DERIVATION.md',88,126,'36e22610ec03dc4421e005f0a327be288cde000fb5fa63f4d8ea9cec3711875d','angular twist produces the ruler line','twist conditionally supplies an intrinsic unoriented ruler'),
      ('S18','udt_complete_nonultrastatic_reciprocal_branch_audit_2026-07-27/EXACT_DERIVATION.md',128,201,'36e22610ec03dc4421e005f0a327be288cde000fb5fa63f4d8ea9cec3711875d','complete metric-native time-line control','one complete control has unique intrinsic Killing line but no founded ruler'),
      ('S19','udt_intrinsic_reciprocal_holonomy_audit_2026-07-27/AUDIT_REPORT.md',22,30,'7296d4fc3e9a44510f05c0a61a5dce498f894e0d9bf6b9bb6f8e947ef1983398','36 fail ordinary','actual full transport is path dependent while scalar clock ratio is endpoint exact'),
      ('S20','udt_global_local_relational_closure_audit_2026-07-25/AUDIT_REPORT.md',30,40,'61c0f3301d3b9f1105611efc23d81a8c58cb96f855745757dafaba29c8aba0cd','reducible direct sum','clock and transverse cocycles currently assemble reducibly; local solder remains obstructed'),
    ]
    out=[]
    for sid,p,a,b,sha,marker,claim in specs:
        raw=(ROOT/p).read_bytes();actual=hashlib.sha256(raw).hexdigest();lines=raw.decode().splitlines();cited='\n'.join(lines[a-1:b]);assert actual==sha,(p,actual);assert marker in cited,(sid,marker)
        out.append({'source_id':sid,'path':p,'line_start':a,'line_end':b,'sha256':actual,'claim':claim,'marker':marker})
    return out
def candidate_outcomes():
    return [
      {'candidate_id':'M01','classification':'CONDITIONAL_ENDPOINT_SCALAR_MAP','exact_positive':'potential difference is exact additive signed cocycle','failed_or_open':'global founded section physical identification and descent;scalar only','extra_inputs':'global exact phi section','selected_physics':'NO'},
      {'candidate_id':'M02','classification':'DERIVED_BOUNDED_COMPLETE_STATIONARY_SCALAR_MAP','exact_positive':'intrinsic Killing-line norm ratio supplies phi(q)-phi(p);constant normalization cancels','failed_or_open':'stationary intrinsic line is branch-specific;scalar only;arbitrary observers not covered','extra_inputs':'complete stationary branch with intrinsic timelike Killing line','selected_physics':'NO'},
      {'candidate_id':'M03','classification':'METRIC_NATIVE_MAGNITUDE_NOT_SIGNED_COCYCLE','exact_positive':'metric supplies a separation magnitude on a typed complete branch','failed_or_open':'reversal-even;generic nonadditivity;dimensionless profile and scale absent','extra_inputs':'causal_or_spatial_distance_type;F;scale','selected_physics':'NO'},
      {'candidate_id':'M04','classification':'CONDITIONAL_OBSERVER_CHART_MAGNITUDE','exact_positive':'centerless observer-indexed distance family exists given F','failed_or_open':'signed lift overlap law angular composition and scale','extra_inputs':'base observer;F;chart transitions;orientation','selected_physics':'NO'},
      {'candidate_id':'M05','classification':'CONDITIONAL_ORIENTED_PATH_ACCUMULATION','exact_positive':'signed line integral composes on retained oriented paths','failed_or_open':'not a universal geodesic-distance law;stationary reduction unproved','extra_inputs':'oriented path and signed line element or one-form','selected_physics':'NO'},
      {'candidate_id':'M06','classification':'CONDITIONAL_EXACT_SECTION_PATH_COCYCLE','exact_positive':'integral dphi equals endpoint phi difference with zero periods','failed_or_open':'global founded section and physical identification','extra_inputs':'global exact phi section','selected_physics':'NO'},
      {'candidate_id':'M07','classification':'GENERIC_CONDITIONAL__BOUNDED_STATIONARY_ALPHA_K_DERIVED','exact_positive':'any alpha gives path cocycle;alpha_K=-d log sqrt(-g(K,K)) is metric-native and exact in intrinsic stationary control','failed_or_open':'no universal nonstationary alpha;generic alpha unselected','extra_inputs':'global one-form;or intrinsic stationary Killing line for alpha_K','selected_physics':'NO'},
      {'candidate_id':'M08','classification':'COVARIANT_FRAME_MOTION_READOUT_NOT_UNIVERSAL_POSITIONAL_DEPTH','exact_positive':'signed rapidity is available with observer orientation and path','failed_or_open':'static spatial control gives zero orthonormal rapidity while founded delta phi is nonzero;generic boosts nonadditive as scalars','extra_inputs':'observer velocities;path;orientation','selected_physics':'NO'},
      {'candidate_id':'M09','classification':'STATIC_COORDINATE_REALIZATION_NOT_COVARIANT_OBSERVABLE','exact_positive':'coordinate covector transport equals D(delta phi) in static diagonal control','failed_or_open':'reference and chart dependent;physical orthonormal transport is identity','extra_inputs':'chart and selected reference coframe','selected_physics':'NO'},
      {'candidate_id':'M10','classification':'DERIVED_TYPED_CONSTRUCTOR_GIVEN_DEPTH_PAIR_AND_PATH','exact_positive':'joint path-groupoid arrow composes and reverses exactly for every supplied additive depth','failed_or_open':'does not derive depth or select path semantics;full embedding may retain lambda or pair reset','extra_inputs':'depth cocycle;ordered pair frames;path;connection','selected_physics':'NO'},
      {'candidate_id':'M11','classification':'CONDITIONAL_ENDPOINT_OPERATOR_GIVEN_COMMON_SECTION','exact_positive':'S(phi_p)^-1 S(phi_q) composes exactly','failed_or_open':'global section event identification and full angular trivialization','extra_inputs':'common global reciprocal section','selected_physics':'NO'},
      {'candidate_id':'M12','classification':'FULL_TRANSPORT_CLASS_DATA_NOT_SIGNED_ADDITIVE_DEPTH','exact_positive':'conjugacy invariants are frame invariant','failed_or_open':'D(delta) and D(-delta) are conjugate after pair swap;trace is even;generic class projections do not add','extra_inputs':'path transport and chosen class function','selected_physics':'NO'},
    ]
def property_rows():
    # PASS means exact after the candidate's declared inputs are supplied, not physical selection.
    P='PASS';C='CONDITIONAL_INPUT';F='FAIL'
    matrix={
      'M01':[P,P,P,P,P,P,C,P,F,P,P,C],
      'M02':[P,P,P,P,P,P,P,P,F,P,P,C],
      'M03':[F,C,F,F,P,F,P,C,F,P,P,C],
      'M04':[F,C,F,F,P,F,P,C,F,P,P,F],
      'M05':[C,P,P,C,C,F,P,C,F,P,P,C],
      'M06':[P,P,P,P,P,P,P,P,F,P,P,P],
      'M07':[C,P,P,P,P,C,P,C,F,P,P,C],
      'M08':[C,P,C,F,P,F,P,P,F,P,C,C],
      'M09':[C,P,C,C,F,P,P,P,F,P,C,F],
      'M10':[C,P,P,P,P,C,P,P,P,P,P,P],
      'M11':[P,P,P,P,C,P,C,P,F,P,P,P],
      'M12':[F,C,F,F,F,F,P,C,F,P,C,F],
    }
    rows=[]
    for m,vals in matrix.items():
        for i,v in enumerate(vals,1):rows.append({'candidate_id':m,'axiom_id':f'A{i:02d}','result':v})
    return rows
def assemblies():
    return [
      {'assembly_id':'J01','components':'M02','scope':'complete static S3 control with unique Killing line','result':'BOUNDED_METRIC_NATIVE_ENDPOINT_SCALAR_DEPTH_DERIVED','missing':'full intrinsic ruler and universal observer law'},
      {'assembly_id':'J02','components':'M07(alpha_K)','scope':'same intrinsic stationary control','result':'BOUNDED_EXACT_METRIC_NATIVE_ONE_FORM_COCYCLE_DERIVED','missing':'nonstationary replacement and physical branch selection'},
      {'assembly_id':'J03','components':'M02+M10','scope':'intrinsic stationary branch plus supplied ordered pair and retained path','result':'EXACT_REDUCIBLE_COMPARISON_DATA_FAMILY_CONDITIONAL','missing':'physical path semantics and irreducible metric solder or proof none is needed'},
      {'assembly_id':'J04','components':'M02+M10+twist_ruler','scope':'twisted complete S3 coframe given stationary line','result':'EXACT_CONDITIONAL_CLOCK_RULER_PATH_FAMILY','missing':'intrinsic uniqueness of stationary line;lambda;on_shell selection'},
      {'assembly_id':'J05','components':'unique_K_control+twist_ruler_control','scope':'two separate witnesses','result':'FORBIDDEN_CROSS_WITNESS_SPLICE','missing':'one configuration satisfying both gates'},
      {'assembly_id':'J06','components':'all','scope':'universal physical UDT observer comparison','result':'OPEN_NO_SINGLE_ALL_GATE_SELECTED_MAP','missing':'selected complete branch;arbitrary-observer extension;physical endpoint/path semantics;global solder'},
    ]
def exact_checks():
    # Endpoint and stationary cocycles.
    pp,pq,pr,c,a=sp.symbols('phi_p phi_q phi_r c a', real=True, nonzero=True)
    d=lambda x,y:y-x
    assert sp.simplify(d(pp,pq)+d(pq,pr)-d(pp,pr))==0 and d(pp,pp)==0 and d(pq,pp)==-d(pp,pq)
    Q=lambda x:c*sp.exp(-x)
    assert sp.simplify(sp.log(Q(pp)/Q(pq))-(pq-pp))==0
    assert sp.simplify(sp.log((a*Q(pp))/(a*Q(pq)))-sp.log(Q(pp)/Q(pq)))==0
    # Metric-skew Levi-Civita generator is trace-orthogonal to self-adjoint reciprocal X.
    z=sp.symbols('z',real=True);eta=sp.diag(-1,1);Omega=sp.Matrix([[0,z],[z,0]]);X=sp.diag(-1,1)
    adj=lambda M:eta.inv()*M.T*eta
    assert adj(Omega)==-Omega and adj(X)==X and sp.trace(X*Omega)==0
    # Symmetric and reversal-odd implies trivial.
    rho=sp.symbols('rho',real=True);assert sp.solve([sp.Eq(rho,-rho)],[rho])=={rho:0}
    # Pair swap conjugates +delta and -delta, so a pure conjugacy class loses the sign.
    q=sp.symbols('q',positive=True);D=sp.diag(1/q,q);F=sp.Matrix([[0,1],[1,0]])
    assert sp.simplify(F*D*F-D.inv())==sp.zeros(2)
    # Exact typed path composition on four sample screen weights.
    U1=sp.eye(4);U1[0,0]=U1[1,1]=sp.Rational(5,4);U1[0,1]=U1[1,0]=sp.Rational(3,4)
    U2=sp.eye(4);U2[2,2]=U2[3,3]=sp.Rational(3,5);U2[2,3]=sp.Rational(-4,5);U2[3,2]=sp.Rational(4,5)
    typed=[]
    for lam in (-1,0,1,2):
        Dn=lambda n:sp.diag(sp.Rational(1,n),sp.Rational(n),sp.Rational(n)**lam,sp.Rational(n)**lam)
        D3_at_1=sp.simplify(U1*Dn(3)*U1.inv());T1=U1*Dn(2);T2=U2*D3_at_1
        assert sp.simplify(T2*T1-U2*U1*Dn(6))==sp.zeros(4);typed.append(lam)
    # Coordinate and orthonormal stationary control are deliberately distinct.
    static={'coordinate_covector_depth':'delta_phi','orthonormal_spatial_rapidity':'0','founded_stationary_depth':'delta_phi'}
    complete=json.loads((ROOT/'udt_intrinsic_reciprocal_holonomy_audit_2026-07-27/DERIVATION_RESULT.json').read_text())
    assert complete['loop_transports']==36 and complete['loops_with_nonzero_ordinary_closure_residual']==36
    return {'endpoint_cocycle':'PASS','stationary_Killing_norm_cocycle':'PASS','Killing_normalization_cancels':'PASS','Levi_Civita_reciprocal_projection':'ZERO_EXACT','symmetric_signed_nontrivial':'IMPOSSIBLE','conjugacy_preserves_depth_sign':'NO','typed_path_lambda_samples':typed,'static_transport_type_control':static,'cut_locus_full_loop_nonclosures':36}
def main():
    src=sources();out=candidate_outcomes();props=property_rows();joins=assemblies();checks=exact_checks()
    write('SOURCE_PROPOSITIONS.tsv',src);write('CANDIDATE_OUTCOMES.tsv',out);write('PROPERTY_MATRIX.tsv',props);write('ASSEMBLY_OUTCOMES.tsv',joins)
    result={'schema':'udt-complete-physical-comparison-map-1.0','status':'COMPUTED','sources':len(src),'candidates':len(out),'axioms':12,'property_cells':len(props),'assemblies':len(joins),'complete_map_derived_unconditionally':False,'bounded_stationary_scalar_map_derived':True,'bounded_stationary_metric_native_one_form_derived':True,'conditional_reducible_comparison_family_available_exact':True,'single_all_gate_intrinsic_pair_witness':False,'endpoint_physical_semantics_selected':False,'path_physical_semantics_selected':False,'lambda_selected':False,'smallest_open_join':'ONE_COMPLETE_BRANCH_INTRINSIC_CLOCK_RULER_COFRAME_AND_PHYSICAL_ARROW_CATEGORY','checks':checks,'grade':'VERIFIED_WITH_CAVEATS'}
    (HERE/'DERIVATION_RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
