#!/usr/bin/env python3
"""Independent fail-closed verifier for the complete-coframe seal audit."""
from __future__ import annotations
import copy,csv,hashlib,json,subprocess
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[1];HERE=Path(__file__).resolve().parent
BASE="5b1b57297bcceb5f8806b1ee238ac2ed2ccfcee3"
EXPECTED_CENSUS={"CONTEXT_CANDIDATE":1708,"LOAD_BEARING_CANDIDATE":84,"EXCLUDED_DUPLICATE_RAW_RECORD":84,"PROVENANCE_OR_COUNTEREXAMPLE_ONLY":1802,"EXCLUDED_GENERATED_ORGANIZATION":226}
def need(c,m):
 if not bool(c):raise AssertionError(m)
def rows(name):
 with (HERE/name).open(encoding="utf-8",newline="") as h:return list(csv.DictReader(h,delimiter="\t"))
def one(items,key,value):
 found=[r for r in items if r[key]==value];need(len(found)==1,f"one:{key}:{value}");return found[0]
def validate_census(items):
 need(len(items)==3904 and len({r["path"] for r in items})==3904,"census-count");counts={}
 for r in items:
  counts[r["initial_disposition"]]=counts.get(r["initial_disposition"],0)+1
  need(len(r["blob"])==40 and len(r["sha256"])==64 and r["matched_tokens"],"census-fields")
  need(not r["path"].startswith("complete_coframe_seal_involution_2026-07-20/"),"census-feedback")
 need(counts==EXPECTED_CENSUS,"census-dispositions");return {"rows":len(items),"dispositions":counts}
def validate_sources(items,census):
 expected={r["path"] for r in census if r["initial_disposition"]=="LOAD_BEARING_CANDIDATE"}
 need(len(items)==84 and len({r["path"] for r in items})==84 and {r["path"] for r in items}==expected,"source-coverage");by={r["path"]:r for r in census}
 for r in items:
  data=subprocess.check_output(["git","show",f"{BASE}:{r['path']}"],cwd=ROOT)
  need(hashlib.sha256(data).hexdigest()==by[r["path"]]["sha256"],f"source-sha:{r['path']}")
  need(subprocess.check_output(["git","rev-parse",f"{BASE}:{r['path']}"],cwd=ROOT,text=True).strip()==by[r["path"]]["blob"],f"source-blob:{r['path']}")
 need(one(items,"path","UDT_NATIVE_ACTION_COLD_PACKET.md")["audit_ruling"]=="FOUNDATION_INPUT","source-foundation")
 need(one(items,"path","transverse_reciprocal_realization_selector_2026-07-19/AUDIT_REPORT.md")["audit_ruling"]=="TRANSVERSE_SCOPE","source-transverse")
 need(one(items,"path","finite_cell_seal_boundary_phase_join_2026-07-20/NEXT_SCIENTIFIC_DECISION.md")["audit_ruling"]=="QUESTION_ONLY","source-question")
 need(one(items,"path","UDT_S2_CARRIER_STATUS_CLARIFICATION_2026-07-15.md")["audit_ruling"]=="CARRIER_EXCLUSION","source-carrier")
 return {"rows":len(items),"base_hashes_replayed":len(items)}
def validate_table(items,key,expected,field,label):
 need(len(items)==len(expected) and len({r[key] for r in items})==len(expected),f"{label}-count")
 for ident,value in expected.items():need(one(items,key,ident)[field]==value,f"{label}:{ident}")
 return {"rows":len(items),"rulings_checked":len(expected)}
def validate_scope(items):
 need(len(items)==17 and len({r["layer"] for r in items})==17,"scope-count")
 need(one(items,"layer","reciprocal character")["status"]=="COVERED_EXACTLY","scope-block")
 need(one(items,"layer","time-on sector")["status"]=="PARTIAL","scope-time")
 need(one(items,"layer","nonlinear solution space")["status"]=="NOT_RUN","scope-solve")
 need(one(items,"layer","external adversarial model review")["status"]=="NOT_PERFORMED","scope-review")
 return {"rows":len(items)}
def validate_derivation(d):
 need(d["result"]=="PASS" and len(d["checks"])==19,"derive-checks")
 need(d["constant_real_classification"]["general_inverting_involution"]=="F_b=[[0,b],[1/b,0]], b nonzero","derive-family")
 need(d["constant_real_classification"]["diagonal_eta"]=="no positive-conformal solution","derive-eta")
 need(d["constant_real_classification"]["dual_K"]=="entire F_b family preserves K","derive-K")
 need(d["field_transport"]["Lorentz_isometry"] is False,"derive-transport")
 need(d["angular_extensions"]["conjugacy_traces"]==[2,-2,0] and d["angular_extensions"]["selector"]=="not supplied","derive-angular")
 need(d["primary_outcome"]=="MULTIPLE_COMPLETIONS","derive-outcome")
 need(d["maximum_conclusion"]=="RECIPROCAL_CHARACTER_INVERSION_HAS_NO_REAL_CONSTANT_POSITIVE_CSN_ISOMETRY_IN_THE_CHOSEN_DIAGONAL_CLOCK_RADIAL_READOUT; IT_HAS_A_CONTINUUM_OF_CONDITIONAL_O11_REFLECTIONS_IF_THE_DUAL_PAIRING_IS_CHOSEN_AS_NULL_BASIS_METRIC; ANGULAR_AND_TIME_ON_EXTENSIONS_ARE_NONUNIQUE; PRIMARY_BRANCH_MULTIPLE_COMPLETIONS","derive-max")
 return {"checks":len(d["checks"]),"outcome":d["primary_outcome"]}
def source_syntax():
 cold=(ROOT/"UDT_NATIVE_ACTION_COLD_PACKET.md").read_text();canon=(ROOT/"CANON.md").read_text();csn=(ROOT/"UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md").read_text();trans=(ROOT/"transverse_reciprocal_realization_selector_2026-07-19/AUDIT_REPORT.md").read_text();parent=(ROOT/"finite_cell_seal_boundary_phase_join_2026-07-20/AUDIT_REPORT.md").read_text()
 need("one faithful dual-pairing formalization" in cold and "P^T K P=K" in cold,"syntax-K-role")
 need("the transverse spatial block or full time-live geometry" in cold,"syntax-open-full")
 need("so its value vanishes there while its normal derivative is free" in cold,"syntax-free-jet")
 need("the local lorentzian readout" in cold.lower() and "retain their separately ledgered non-derived statuses" in cold,"syntax-readout")
 need("angular/transverse block, all off-diagonal/shift terms" in canon,"syntax-canon-open")
 need("whether the seal kills / pins /" in canon and "permits ω is the OPEN" in canon,"syntax-time")
 need("\\Omega(x)>0" in csn and "finite-cell boundary functional" in csn,"syntax-CSN")
 need("Its transverse two-plane is the identity" in trans and "cannot naturally produce the nonzero shear" in trans,"syntax-transverse")
 need("J^T eta J = -eta" in parent and "PARTIAL_SEAL_DATA_ONLY" in parent,"syntax-parent")
 return {"cold_packet":"PASS","canon":"PASS","CSN":"PASS","transverse":"PASS","parent":"PASS"}
def independent_algebra():
 a,b,c,d=sp.symbols("a b c d",real=True);A=sp.diag(-1,1);F=sp.Matrix([[a,b],[c,d]])
 anti=F*A+A*F;need(anti==sp.Matrix([[-2*a,0],[0,2*d]]),"independent-anticommute")
 need(sp.solve(list(anti),(a,d),dict=True)==[{a:0,d:0}],"independent-offdiagonal")
 q=sp.symbols("q",nonzero=True,real=True);G=sp.Matrix([[0,q],[1/q,0]]);need(G*G==sp.eye(2),"independent-involution")
 phi=sp.symbols("phi",real=True);D=sp.diag(sp.exp(-phi),sp.exp(phi));need(sp.simplify(G*D*G-D.subs(phi,-phi))==sp.zeros(2),"independent-inversion")
 eta=sp.diag(-1,1);K=sp.Matrix([[0,1],[1,0]]);pull=sp.simplify(G.T*eta*G)
 need(pull==sp.diag(q**-2,-q**2),"independent-eta-pull")
 need(pull[0,0]>0 and eta[0,0]<0,"independent-positive-factor-obstruction")
 need(sp.simplify(G.T*K*G)==K,"independent-K")
 H=sp.Matrix([[1,1],[1,-1]])/sp.sqrt(2);need(sp.simplify(H.T*K*H)==sp.diag(1,-1),"independent-H")
 B=sp.simplify(H.T*D*H);need(sp.simplify(B.T*sp.diag(1,-1)*B)==sp.diag(1,-1),"independent-boost")
 theta=sp.symbols("theta",real=True);R=sp.Matrix([[sp.cos(theta),-sp.sin(theta)],[sp.sin(theta),sp.cos(theta)]]);Q=sp.simplify(R*sp.diag(1,-1)*R.T)
 need(sp.simplify(Q*Q)==sp.eye(2) and sp.trace(Q)==0,"independent-angular")
 need({sp.trace(sp.eye(2)),sp.trace(-sp.eye(2)),sp.trace(Q)}=={2,-2,0},"independent-classes")
 return {"constant_family":"PASS","positive_eta_obstruction":"PASS","K_isometry":"PASS","basis_boost":"PASS","angular_classes":[2,-2,0]}
def expect(label,fn):
 try:fn()
 except (AssertionError,KeyError,subprocess.CalledProcessError):return "PASS"
 raise AssertionError(f"catch-did-not-fail:{label}")
def main():
 census=rows("SOURCE_CENSUS.tsv");sources=rows("SOURCE_ADJUDICATION.tsv");blocks=rows("BLOCK_REALIZATION_LEDGER.tsv");extensions=rows("EXTENSION_FAMILY_LEDGER.tsv");witnesses=rows("COMPLETE_EXTENSION_WITNESSES.tsv");req=rows("REQUIREMENT_MATRIX.tsv");outcomes=rows("OUTCOME_BRANCH_LEDGER.tsv");status=rows("STATUS_LEDGER.tsv");scope=rows("COMPLETENESS_SCOPE.tsv");d=json.loads((HERE/"DERIVATION_RESULT.json").read_text())
 block_expected={"B01":"NOT_POSITIVE_CSN_LORENTZIAN_ISOMETRY","B02":"NO_REAL_CONSTANT_PHYSICAL_REFLECTION_IN_THIS_READOUT","B03":"CONTINUUM_CONDITIONAL_O11_REFLECTIONS","B04":"CONDITIONAL_PHYSICAL_BLOCK_WITNESS","B05":"TAUTOLOGICAL_TRANSPORT_NOT_ISOMETRY","B06":"CONDITIONAL_BASIS_REALIZATION_NOT_UNIQUE","B07":"REJECTED_NONREAL"}
 ext_values=["CONDITIONAL_EXTENSION","CONDITIONAL_INEQUIVALENT_COFRAME_EXTENSION","CONTINUUM_CONDITIONAL_EXTENSIONS","CONDITIONAL_STRATIFIED","CONDITIONAL_TRANSVERSE_IDENTITY_WITNESS","CONDITIONAL_ANGULAR_SWAP_WITNESS","PARTIAL_FOUNDED_BASE_ACTION","FOUNDED_SCALAR_ACTION_ONLY","OPEN_EXTENSION","MULTIPLE_GAUGE_EXTENSIONS","OPEN_DISCRETE_EXTENSION","OPEN_GLOBAL_EXTENSIONS"]
 ext_expected={f"X{i:02d}":v for i,v in enumerate(ext_values,1)}
 witness_values=["COMPLETE_ALGEBRAIC_COFRAME_WITNESS_CONDITIONAL","INEQUIVALENT_COMPLETE_ALGEBRAIC_COFRAME_WITNESS_CONDITIONAL","CONTINUUM_COMPLETE_ALGEBRAIC_WITNESSES_CONDITIONAL","COMPLETE_FIELD_MATCHING_WITNESS_NOT_METRIC_ISOMETRY","CONDITIONAL_GLOBAL_GEOMETRIC_WITNESS"]
 witness_expected={f"W{i:02d}":v for i,v in enumerate(witness_values,1)}
 req_expected={"B01_RAW_SWAP":"FAIL_PHYSICAL_METRIC","B03_K_FAMILY":"CONDITIONAL_BLOCK_ONLY","B04_BALANCED_K":"CONDITIONAL_BLOCK_ONLY","B05_FIELD_TRANSPORT":"FAIL_SYMMETRY; PASS_FIELD_MATCHING","W01":"COMPLETE_CONDITIONAL_NOT_NATIVE","W02":"COMPLETE_CONDITIONAL_NOT_NATIVE","W03":"CONTINUUM_CONDITIONAL_NOT_NATIVE","W05_HOPF":"CONDITIONAL_ANGULAR_WITNESS","CURRENT_FOUNDATION":"NO_COMPLETE_NATIVE_INVOLUTION"}
 outcome_expected={"COMPLETE_NATIVE_COFRAME_INVOLUTION":"NOT_REACHED","RECIPROCAL_BLOCK_ONLY":"NOT_REACHED","MULTIPLE_COMPLETIONS":"PRIMARY_OUTCOME","NO_PHYSICAL_INVOLUTION_JOIN":"NOT_REACHED"}
 status_values=["FOUNDING","FAITHFUL_DUAL_PAIRING_FORMALIZATION","DERIVED_CONDITIONAL","CANONIZED_BINDING","DERIVED_EXACT","REFUTED_FOR_CONSTANT_REAL_FAMILY","DERIVED_EXACT","DERIVED_EXACT","DERIVED_EXACT_COCYCLE","PARTIAL_FOUNDED_BASE_ACTION","CONDITIONAL_WITNESS","CONDITIONAL_INEQUIVALENT_WITNESS","DERIVED_EXACT_FAMILY","CONDITIONAL_WITNESS","CANONIZED_SECTOR_AUTHORITY","FOUNDING","NOT_DERIVED","OPEN","OUT_OF_SCOPE_OPEN","OPEN_NOT_ADOPTED","OPEN_NOT_DERIVED","NOT_DERIVED","PRIMARY_OUTCOME","VERIFIED_WITH_CAVEATS"]
 status_expected={f"S{i:02d}":v for i,v in enumerate(status_values,1)}
 groups={"source_census":validate_census(census),"source_adjudication":validate_sources(sources,census),"blocks":validate_table(blocks,"id",block_expected,"ruling","blocks"),"extensions":validate_table(extensions,"id",ext_expected,"ruling","extensions"),"witnesses":validate_table(witnesses,"id",witness_expected,"status","witnesses"),"requirements":validate_table(req,"candidate",req_expected,"result","requirements"),"outcomes":validate_table(outcomes,"branch",outcome_expected,"ruling","outcomes"),"status":validate_table(status,"id",status_expected,"status","status"),"completeness":validate_scope(scope),"derivation":validate_derivation(d),"source_syntax":source_syntax(),"independent_algebra":independent_algebra()}
 catches={}
 catches["missing_census_rejected"]=expect("census",lambda:validate_census(census[:-1]));changed=copy.deepcopy(census);one(changed,"path","CANON.md")["sha256"]="0"*64
 catches["canon_mutation_rejected"]=expect("canon-hash",lambda:validate_sources(sources,changed));catches["missing_source_rejected"]=expect("source",lambda:validate_sources(sources[:-1],census));changed=copy.deepcopy(sources);one(changed,"path","UDT_S2_CARRIER_STATUS_CLARIFICATION_2026-07-15.md")["audit_ruling"]="NATIVE_CARRIER"
 catches["carrier_import_rejected"]=expect("carrier",lambda:validate_sources(changed,census))
 catches["missing_block_rejected"]=expect("block",lambda:validate_table(blocks[:-1],"id",block_expected,"ruling","blocks"))
 for ident,bad,label in [("B01","PHYSICAL_ISOMETRY","raw-swap"),("B02","UNIQUE_REFLECTION","constant-family"),("B03","FOUNDED_METRIC","K-choice"),("B04","NATIVE_BLOCK","balanced-choice"),("B05","LORENTZ_ISOMETRY","transport"),("B06","UNIQUE_PHYSICAL_SLOTS","basis"),("B07","PHYSICAL_COMPLETION","complex")]:
  changed=copy.deepcopy(blocks);one(changed,"id",ident)["ruling"]=bad;catches[f"{label}_overclaim_rejected"]=expect(label,lambda changed=changed:validate_table(changed,"id",block_expected,"ruling","blocks"))
 catches["missing_extension_rejected"]=expect("extension",lambda:validate_table(extensions[:-1],"id",ext_expected,"ruling","extensions"))
 for ident,bad,label in [("X01","SELECTED","angular-I"),("X02","EQUIVALENT","angular-minus"),("X03","UNIQUE_AXIS","angular-axis"),("X05","TRANSVERSE_RECIPROCITY_DERIVED","direct-four"),("X06","NATIVE_HOPF","Hopf"),("X07","COMPLETE_NORMAL","normal"),("X09","EXECUTABLE","time-on"),("X10","SCALE_FIXED","CSN"),("X11","ORIENTATION_SELECTED","chirality"),("X12","S3_SELECTED","global")]:
  changed=copy.deepcopy(extensions);one(changed,"id",ident)["ruling"]=bad;catches[f"{label}_overclaim_rejected"]=expect(label,lambda changed=changed:validate_table(changed,"id",ext_expected,"ruling","extensions"))
 catches["missing_witness_rejected"]=expect("witness",lambda:validate_table(witnesses[:-1],"id",witness_expected,"status","witnesses"));changed=copy.deepcopy(witnesses);one(changed,"id","W02")["status"]="EQUIVALENT_TO_W01";catches["inequivalent_witness_loss_rejected"]=expect("witness-inequivalence",lambda:validate_table(changed,"id",witness_expected,"status","witnesses"))
 changed=copy.deepcopy(witnesses);one(changed,"id","W03")["status"]="UNIQUE_COMPLETE";catches["continuum_collapse_rejected"]=expect("witness-continuum",lambda:validate_table(changed,"id",witness_expected,"status","witnesses"))
 catches["missing_requirement_rejected"]=expect("requirement",lambda:validate_table(req[:-1],"candidate",req_expected,"result","requirements"))
 for ident,bad,label in [("B01_RAW_SWAP","PASS","negative-factor"),("B03_K_FAMILY","NATIVE_BLOCK","K-provenance"),("B05_FIELD_TRANSPORT","PHYSICAL_SYMMETRY","transport-requirement"),("W01","COMPLETE_NATIVE","complete-witness"),("W05_HOPF","NATIVE_GLOBAL","Hopf-requirement"),("CURRENT_FOUNDATION","COMPLETE","foundation")]:
  changed=copy.deepcopy(req);one(changed,"candidate",ident)["result"]=bad;catches[f"{label}_overclaim_rejected"]=expect(label,lambda changed=changed:validate_table(changed,"candidate",req_expected,"result","requirements"))
 catches["missing_outcome_rejected"]=expect("outcome",lambda:validate_table(outcomes[:-1],"branch",outcome_expected,"ruling","outcomes"));changed=copy.deepcopy(outcomes);one(changed,"branch","COMPLETE_NATIVE_COFRAME_INVOLUTION")["ruling"]="PRIMARY_OUTCOME";catches["native_outcome_promotion_rejected"]=expect("native-outcome",lambda:validate_table(changed,"branch",outcome_expected,"ruling","outcomes"))
 changed=copy.deepcopy(outcomes);one(changed,"branch","RECIPROCAL_BLOCK_ONLY")["ruling"]="PRIMARY_OUTCOME";catches["block_founded_promotion_rejected"]=expect("block-outcome",lambda:validate_table(changed,"branch",outcome_expected,"ruling","outcomes"))
 catches["missing_status_rejected"]=expect("status",lambda:validate_table(status[:-1],"id",status_expected,"status","status"))
 for ident,bad,label in [("S02","PHYSICAL_METRIC","K-status"),("S06","DERIVED_ISOMETRY","eta-status"),("S09","PHYSICAL_SYMMETRY","transport-status"),("S13","UNIQUE","angular-status"),("S15","COMPLETE_PARITY","time-status"),("S17","DERIVED","boundary-tangent"),("S18","S3_DERIVED","global-status"),("S19","C2_DERIVED","action"),("S20","NATIVE_CARRIER","carrier-status"),("S21","MASS_DERIVED","mass"),("S22","DERIVED","complete-status"),("S23","UNIQUE_COMPLETION","outcome-status"),("S24","SETTLED","grade")]:
  changed=copy.deepcopy(status);one(changed,"id",ident)["status"]=bad;catches[f"{label}_overclaim_rejected"]=expect(label,lambda changed=changed:validate_table(changed,"id",status_expected,"status","status"))
 catches["missing_scope_rejected"]=expect("scope",lambda:validate_scope(scope[:-1]));changed=copy.deepcopy(d);changed["primary_outcome"]="COMPLETE_NATIVE_COFRAME_INVOLUTION";catches["derivation_outcome_mutation_rejected"]=expect("derive-outcome",lambda:validate_derivation(changed));changed=copy.deepcopy(d);changed["field_transport"]["Lorentz_isometry"]=True;catches["transport_promotion_rejected"]=expect("derive-transport",lambda:validate_derivation(changed));changed=copy.deepcopy(d);changed["maximum_conclusion"]="COMPLETE_UDT_ACTION_BOUNDARY_AND_MASS";catches["maximum_overreach_rejected"]=expect("derive-max",lambda:validate_derivation(changed))
 with (HERE/"CATCH_PROOFS.tsv").open("w",encoding="utf-8",newline="") as h:w=csv.DictWriter(h,fieldnames=["catch","result"],delimiter="\t",lineterminator="\n");w.writeheader();w.writerows({"catch":k,"result":v} for k,v in sorted(catches.items()))
 out={"schema":"udt-complete-coframe-seal-involution-verification-1.0","result":"PASS","groups":groups,"catch_proofs":catches,"counts":{"census":len(census),"sources":len(sources),"blocks":len(blocks),"extensions":len(extensions),"witnesses":len(witnesses),"requirements":len(req),"outcomes":len(outcomes),"status":len(status),"completeness":len(scope),"catch_proofs":len(catches)},"derivation_sha256":hashlib.sha256((HERE/"DERIVATION_RESULT.json").read_bytes()).hexdigest(),"verdict":"MULTIPLE_COMPLETIONS; NO_REAL_CONSTANT_POSITIVE_CSN_ISOMETRY_IN_CONDITIONAL_DIAGONAL_READOUT; CONDITIONAL_K_NULL_REFLECTION_FAMILY; ANGULAR_AND_TIME_ON_LIFTS_UNSELECTED","certification":"VERIFIED-WITH-CAVEATS: independent source/hash, full constant-block, basis, angular-class, and mutation reconstruction; no fresh external-model review","compute":{"cpu_only":True,"gpu_used":False,"sympy":sp.__version__}}
 (HERE/"VERIFICATION_RESULT.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");print(json.dumps({"result":"PASS","groups":len(groups),"catch_proofs":len(catches),"verdict":out["verdict"]},sort_keys=True))
if __name__=="__main__":main()
