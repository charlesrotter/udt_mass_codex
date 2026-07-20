#!/usr/bin/env python3
"""Independent fail-closed verifier for the finite-cell seal boundary join."""
from __future__ import annotations
import copy,csv,hashlib,json,subprocess
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[1];HERE=Path(__file__).resolve().parent;BASE="55a2c53daade7282526581f20360f57aecfec12d"
EXPECTED_CENSUS={"CONTEXT_CANDIDATE":1693,"LOAD_BEARING_CANDIDATE":72,"EXCLUDED_DUPLICATE_RAW_RECORD":80,"PROVENANCE_OR_COUNTEREXAMPLE_ONLY":1802,"EXCLUDED_GENERATED_ORGANIZATION":226}
def need(c,m):
 if not bool(c):raise AssertionError(m)
def rows(name):
 with (HERE/name).open(encoding="utf-8",newline="") as h:return list(csv.DictReader(h,delimiter="\t"))
def one(items,key,value):
 f=[r for r in items if r[key]==value];need(len(f)==1,f"one:{key}:{value}");return f[0]
def validate_census(items):
 need(len(items)==3873 and len({r["path"] for r in items})==3873,"census-count");counts={}
 for r in items:
  counts[r["initial_disposition"]]=counts.get(r["initial_disposition"],0)+1
  need(len(r["blob"])==40 and len(r["sha256"])==64 and r["matched_tokens"],"census-fields")
  need(not r["path"].startswith("finite_cell_seal_boundary_phase_join_2026-07-20/"),"census-feedback")
 need(counts==EXPECTED_CENSUS,"census-dispositions");return {"rows":len(items),"dispositions":counts}
def validate_sources(items,census):
 expected={r["path"] for r in census if r["initial_disposition"]=="LOAD_BEARING_CANDIDATE"}
 need(len(items)==72 and len({r["path"] for r in items})==72 and {r["path"] for r in items}==expected,"source-coverage");by={r["path"]:r for r in census}
 for r in items:
  data=subprocess.check_output(["git","show",f"{BASE}:{r['path']}"],cwd=ROOT)
  need(hashlib.sha256(data).hexdigest()==by[r["path"]]["sha256"],f"source-sha:{r['path']}")
  need(subprocess.check_output(["git","rev-parse",f"{BASE}:{r['path']}"],cwd=ROOT,text=True).strip()==by[r["path"]]["blob"],f"source-blob:{r['path']}")
 need(one(items,"path","c2_finite_cell_boundary_variation_2026-07-20/NEXT_SCIENTIFIC_DECISION.md")["audit_ruling"]=="QUESTION_ONLY","source-question")
 need(one(items,"path","udt_premise_reset_audit_2026-07-19/OWNER_MEANING_LEDGER.tsv")["audit_ruling"]=="SEMANTIC_CONTROL","source-reset")
 need(one(items,"path","native_action_final_adjudication_2026-07-18/MECHANICAL_AGREEMENT_DISAGREEMENT.tsv")["audit_ruling"]=="FROZEN_BOUNDARY_STATUS","source-frozen")
 need(one(items,"path","UDT_S2_CARRIER_STATUS_CLARIFICATION_2026-07-15.md")["audit_ruling"]=="CARRIER_EXCLUSION","source-carrier")
 return {"rows":len(items),"base_hashes_replayed":len(items)}
def validate_table(items,key,expected,field,label):
 need(len(items)==len(expected) and len({r[key] for r in items})==len(expected),f"{label}-count")
 for i,v in expected.items():need(one(items,key,i)[field]==v,f"{label}:{i}")
 return {"rows":len(items),"rulings_checked":len(expected)}
def validate_scope(items):
 need(len(items)==17 and len({r["layer"] for r in items})==17,"scope-count")
 need(one(items,"layer","static phi seal")["status"]=="COVERED_EXACTLY","scope-phi")
 need(one(items,"layer","induced metric variations")["status"]=="PARTIAL","scope-h")
 need(one(items,"layer","external adversarial model review")["status"]=="NOT_PERFORMED","scope-review")
 return {"rows":len(items)}
def validate_derivation(d):
 need(d["result"]=="PASS" and len(d["checks"])==20,"derive-checks")
 need(d["tangent_rank"]=={"matrix_rank":3,"seal_constraint_rank":1,"seal_nullity":3,"interpretation":"delta phi=0 removes one reciprocal tangent while common scale, angular shear, and additional full-metric tangents remain"},"derive-rank")
 need(d["mirror_challenge"]["canon_phi_prime"]=="FREE","derive-mirror")
 need(d["reciprocal_swap_challenge"]["Lorentzian_pullback"]=="swap^T eta swap = -eta","derive-swap")
 need(d["primary_outcome"]=="PARTIAL_SEAL_DATA_ONLY","derive-outcome")
 need(d["supporting_nonuniqueness"]=="MULTIPLE_INEQUIVALENT_POLARIZATION_WITNESSES_REMAIN_COMPATIBLE","derive-witness")
 need(d["maximum_conclusion"]=="STATIC_ODD_PHI_SUPPLIES_ONE_DIRICHLET_RATIO_DATUM_WITH_FREE_NORMAL_DERIVATIVE; IT_DOES_NOT SELECT_THE_CONDITIONAL_C2_METRIC_TWO_JET_MOMENTA_CORNER_OR_CHARGE; PRIMARY_BRANCH_PARTIAL_SEAL_DATA_ONLY","derive-max")
 return {"checks":len(d["checks"]),"outcome":d["primary_outcome"]}
def source_syntax():
 cold=(ROOT/"UDT_NATIVE_ACTION_COLD_PACKET.md").read_text();canon=(ROOT/"CANON.md").read_text();csn=(ROOT/"UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md").read_text()
 boot=(ROOT/"UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md").read_text();xmax=(ROOT/"UDT_XMAX_STATUS_CLARIFICATION_2026-07-15.md").read_text();co=(ROOT/"copresence_causal_accessibility_selector_2026-07-19/DERIVATION_REPORT.md").read_text()
 need("so its value vanishes there while its normal derivative is free" in cold,"syntax-cold-free")
 need("that parity statement does not select the action's boundary functional" in cold,"syntax-cold-limit")
 need("Dirichlet φ(r_s)=0" in canon and "with φ' free" in canon,"syntax-canon")
 need("whether the seal kills / pins /" in canon and "permits ω is the OPEN" in canon,"syntax-time-on")
 need("does not select locality, derivative order, an action, a boundary term" in cold,"syntax-reciprocity-limit")
 need("not yet a complete action, boundary law" in csn and "the finite-cell boundary functional" in csn,"syntax-CSN")
 need("No nonlocal insertion" in boot and "Primary global reading" in boot,"syntax-bootstrap")
 need("WORKING POSIT" in xmax and "origin and value are reopened" in xmax,"syntax-Xmax")
 need("Co-presence is not zero-time separation" in co and "does not choose the complete action" in co,"syntax-copresence")
 return {"cold_packet":"PASS","canon":"PASS","CSN":"PASS","bootstrap":"PASS","Xmax":"PASS","copresence":"PASS"}
def independent_algebra():
 s,p,A=sp.symbols("s p A");v=sp.Matrix([s-p,s+p,s+A,s-A]);J=v.jacobian([s,p,A]);need(J.rank()==3,"independent-rank")
 dp=sp.Matrix([0,1,0]);need((J*dp)==sp.Matrix([-1,1,0,0]),"independent-phi")
 ds=sp.Matrix([1,0,0]);dA=sp.Matrix([0,0,1]);seal=sp.Matrix([[-1,1,0,0]])
 need((seal*J*ds)[0]==0 and (seal*J*dA)[0]==0,"independent-survivors")
 n,a=sp.symbols("n a",real=True);h=-sp.exp(-2*a*n);need(h.subs(n,0)==-1 and sp.diff(h,n).subs(n,0)==2*a,"independent-free-jet")
 phi=sp.symbols("phi");D=sp.diag(sp.exp(-phi),sp.exp(phi));S=sp.Matrix([[0,1],[1,0]]);eta=sp.diag(-1,1)
 need(S*D*S==D.subs(phi,-phi),"independent-inversion");need(S.T*eta*S==-eta,"independent-anti-isometry")
 need(not sp.solve(sp.Eq(sp.symbols("q",positive=True)**2,-1),sp.symbols("q",positive=True)),"independent-positive-CSN")
 return {"static_tangent_rank":J.rank(),"free_clock_metric_jet":str(sp.diff(h,n).subs(n,0)),"reciprocal_swap":"PASS","Lorentzian_anti_isometry":"PASS"}
def expect(label,fn):
 try:fn()
 except (AssertionError,KeyError,subprocess.CalledProcessError):return "PASS"
 raise AssertionError(f"catch-did-not-fail:{label}")
def main():
 census=rows("SOURCE_CENSUS.tsv");sources=rows("SOURCE_ADJUDICATION.tsv");clauses=rows("CLAUSE_TO_BOUNDARY_SLOT.tsv");slots=rows("SLOT_COVERAGE.tsv")
 witnesses=rows("POLARIZATION_WITNESSES.tsv");challenges=rows("STRONGEST_JOIN_CHALLENGES.tsv");outcomes=rows("OUTCOME_BRANCH_LEDGER.tsv");status=rows("STATUS_LEDGER.tsv");scope=rows("COMPLETENESS_SCOPE.tsv");d=json.loads((HERE/"DERIVATION_RESULT.json").read_text())
 clause_expected={"J01":"PARTIAL_DOMAIN_ONLY","J02":"PARTIAL_ONE_SCALAR","J03":"BLOCKS_CLAMPED_JOIN","J04":"PARTIAL_SECTOR_MAP","J05":"NO_POLARIZATION","J06":"NULL_DIRECTION_NOT_POLARIZATION","J07":"NO_POLARIZATION","J08":"NO_WALL_DATA","J09":"NO_EXECUTABLE_LOCAL_JOIN","J10":"NO_EXECUTABLE_LOCAL_JOIN","J11":"NO_POLARIZATION","J12":"MISSING_OBJECT_NOT_JOIN","J13":"MISSING_OBJECT_NOT_JOIN","J14":"PHASE_SPACE_NOT_POLARIZATION","J15":"CONFIRMS_PARTIAL_ONLY"}
 slot_values=["SUPPLIED_DOMAIN_ONTOLOGY","OPEN","OPEN","SUPPLIED_ONE_SCALAR_STATIC","NULL_NOT_SECTIONED","OPEN","FREE_NOT_FIXED","OPEN","NOT_SELECTED","NOT_SELECTED","OPEN","OPEN_SECTOR","NOT_SUPPLIED","OPEN","PARTIAL_SEAL_DATA_ONLY"]
 slot_expected={f"K{i:02d}":v for i,v in enumerate(slot_values,1)}
 witness_expected={"W01":"COMPATIBLE_COMPLETE_VARIATION_WITNESS_NOT_SELECTED","W02":"COMPATIBLE_INEQUIVALENT_VARIATION_WITNESS_NOT_SELECTED","W03":"OPEN_COMPLETION_WITNESS_NOT_USED_FOR_MINIMUM_COUNTERPAIR"}
 challenge_values=["PARTIAL_DERIVED_CONDITIONAL","NOT_DERIVED_AND_INCOMPATIBLE_WITH_GENERIC_FREE_PHI_PRIME","REFUTED_AS_SUFFICIENT","REFUTED_AS_SUFFICIENT","REFUTED_AS_SECTION_SELECTOR","REJECTED_AS_INFERENCE","NOT_DERIVED","UNDERDETERMINED","REJECTED_AS_INFERENCE","REFUTED_BY_COMPATIBLE_POLARIZATION_PAIR","ALGEBRAIC_INVERSION_WITNESS_NOT_PHYSICAL_ISOMETRY"]
 challenge_expected={f"Q{i:02d}":v for i,v in enumerate(challenge_values,1)}
 outcome_expected={"UNIQUE_NATIVE_POLARIZATION_JOIN":"NOT_REACHED","PARTIAL_SEAL_DATA_ONLY":"PRIMARY_OUTCOME","MULTIPLE_POLARIZATIONS_REMAIN":"SUPPORTING_NONUNIQUENESS_NOT_PRIMARY","NO_EXECUTABLE_JOIN":"NOT_REACHED"}
 status_values=["CANONIZED_BINDING","CANONIZED_BINDING","DERIVED_FROM_CANON","FALSE_EXCLUDED","DERIVED_CONDITIONAL","NOT_DERIVED","NOT_DERIVED","DERIVED_EXACT_ALGEBRA","REFUTED_FOR_RAW_SWAP","NOT_DERIVED","REFUTED_AS_SECTION_SELECTOR","REJECTED_AS_INFERENCE","NOT_DERIVED","NOT_SUPPLIED","NOT_DERIVED","OPEN","OPEN","DERIVED_LOGICAL_INDEPENDENCE","PARTIAL_SEAL_DATA_ONLY","OPEN_NOT_ACTIVATED","VERIFIED_WITH_CAVEATS"]
 status_expected={f"S{i:02d}":v for i,v in enumerate(status_values,1)}
 groups={"source_census":validate_census(census),"source_adjudication":validate_sources(sources,census),"clauses":validate_table(clauses,"id",clause_expected,"join_ruling","clause"),"slots":validate_table(slots,"id",slot_expected,"status","slot"),"witnesses":validate_table(witnesses,"id",witness_expected,"role","witness"),"challenges":validate_table(challenges,"id",challenge_expected,"ruling","challenge"),"outcomes":validate_table(outcomes,"branch",outcome_expected,"ruling","outcome"),"status":validate_table(status,"id",status_expected,"status","status"),"completeness":validate_scope(scope),"derivation":validate_derivation(d),"source_syntax":source_syntax(),"independent_algebra":independent_algebra()}
 catches={}
 catches["missing_census_rejected"]=expect("census",lambda:validate_census(census[:-1]));changed=copy.deepcopy(census);one(changed,"path","CANON.md")["sha256"]="0"*64
 catches["canon_mutation_rejected"]=expect("canon-hash",lambda:validate_sources(sources,changed));catches["missing_source_rejected"]=expect("source",lambda:validate_sources(sources[:-1],census))
 changed=copy.deepcopy(sources);one(changed,"path","UDT_S2_CARRIER_STATUS_CLARIFICATION_2026-07-15.md")["audit_ruling"]="NATIVE_CARRIER";catches["carrier_import_rejected"]=expect("carrier",lambda:validate_sources(changed,census))
 catches["missing_clause_rejected"]=expect("clause",lambda:validate_table(clauses[:-1],"id",clause_expected,"join_ruling","clause"))
 for ident,bad,label in [("J02","FULL_H_FIXED","phi-full-h"),("J03","K_FIXED","free-jet"),("J04","STATIC_NEUMANN","temporal-mirror"),("J05","COMPLETE_POLARIZATION","reciprocity"),("J06","PHYSICAL_SECTION","CSN"),("J07","OFFSHELL_BOUNDARY","copresence"),("J09","PHYSICAL_WALL","Xmax"),("J11","VARIED_BOUNDARY","bootstrap"),("J12","B_DERIVED","B"),("J13","SIGMA_DERIVED","Sigma"),("J14","SELECTED_WALL","parent")]:
  changed=copy.deepcopy(clauses);one(changed,"id",ident)["join_ruling"]=bad;catches[f"{label}_overclaim_rejected"]=expect(label,lambda changed=changed:validate_table(changed,"id",clause_expected,"join_ruling","clause"))
 catches["missing_slot_rejected"]=expect("slot",lambda:validate_table(slots[:-1],"id",slot_expected,"status","slot"))
 for ident,bad,label in [("K02","DERIVED","Xmax-slot"),("K05","FIXED","scale-slot"),("K07","FIXED","jet-slot"),("K09","SELECTED","E-slot"),("K10","SELECTED","Pi-slot"),("K11","SELECTED","corner-slot"),("K13","DERIVED","bootstrap-slot"),("K14","NORMALIZED","charge-slot"),("K15","COMPLETE_JOIN","join-slot")]:
  changed=copy.deepcopy(slots);one(changed,"id",ident)["status"]=bad;catches[f"{label}_overclaim_rejected"]=expect(label,lambda changed=changed:validate_table(changed,"id",slot_expected,"status","slot"))
 catches["missing_witness_rejected"]=expect("witness",lambda:validate_table(witnesses[:-1],"id",witness_expected,"role","witness"));changed=copy.deepcopy(witnesses);one(changed,"id","W02")["role"]="SAME_AS_W01";catches["witness_inequivalence_loss_rejected"]=expect("witness-change",lambda:validate_table(changed,"id",witness_expected,"role","witness"))
 catches["missing_challenge_rejected"]=expect("challenge",lambda:validate_table(challenges[:-1],"id",challenge_expected,"ruling","challenge"))
 for ident,bad,label in [("Q02","K_ZERO_DERIVED","mirror-K"),("Q05","SECTION_DERIVED","CSN-section"),("Q06","BOUNDARY_DERIVED","copresence-boundary"),("Q08","BOOTSTRAP_CLOSED","bootstrap-join"),("Q09","ZERO_MASS","bare-Q"),("Q10","UNIQUE","counterpair"),("Q11","LORENTZIAN_ISOMETRY","swap")]:
  changed=copy.deepcopy(challenges);one(changed,"id",ident)["ruling"]=bad;catches[f"{label}_overclaim_rejected"]=expect(label,lambda changed=changed:validate_table(changed,"id",challenge_expected,"ruling","challenge"))
 catches["missing_outcome_rejected"]=expect("outcome",lambda:validate_table(outcomes[:-1],"branch",outcome_expected,"ruling","outcome"));changed=copy.deepcopy(outcomes);one(changed,"branch","UNIQUE_NATIVE_POLARIZATION_JOIN")["ruling"]="PRIMARY_OUTCOME";catches["unique_outcome_promotion_rejected"]=expect("unique",lambda:validate_table(changed,"branch",outcome_expected,"ruling","outcome"))
 catches["missing_status_rejected"]=expect("status",lambda:validate_table(status[:-1],"id",status_expected,"status","status"))
 for ident,bad,label in [("S04","DERIVED","phi-prime"),("S07","DERIVED","metric-reflection"),("S09","DERIVED","swap-isometry"),("S12","DERIVED","co-presence"),("S13","DERIVED","Xmax-status"),("S17","DERIVED_MASS","mass"),("S19","COMPLETE_JOIN","primary-grade"),("S20","CLOSED","physics-closure"),("S21","SETTLED","evidence-grade")]:
  changed=copy.deepcopy(status);one(changed,"id",ident)["status"]=bad;catches[f"{label}_overclaim_rejected"]=expect(label,lambda changed=changed:validate_table(changed,"id",status_expected,"status","status"))
 catches["missing_scope_rejected"]=expect("scope",lambda:validate_scope(scope[:-1]));changed=copy.deepcopy(d);changed["primary_outcome"]="UNIQUE_NATIVE_POLARIZATION_JOIN";catches["derivation_outcome_mutation_rejected"]=expect("derive-outcome",lambda:validate_derivation(changed));changed=copy.deepcopy(d);changed["reciprocal_swap_challenge"]["Lorentzian_pullback"]="isometry";catches["swap_obstruction_loss_rejected"]=expect("derive-swap",lambda:validate_derivation(changed));changed=copy.deepcopy(d);changed["maximum_conclusion"]="COMPLETE_UDT_BOUNDARY_AND_MASS";catches["maximum_overreach_rejected"]=expect("derive-max",lambda:validate_derivation(changed))
 with (HERE/"CATCH_PROOFS.tsv").open("w",encoding="utf-8",newline="") as h:w=csv.DictWriter(h,fieldnames=["catch","result"],delimiter="\t",lineterminator="\n");w.writeheader();w.writerows({"catch":k,"result":v} for k,v in sorted(catches.items()))
 out={"schema":"udt-finite-cell-seal-boundary-join-verification-1.0","result":"PASS","groups":groups,"catch_proofs":catches,"counts":{"census":len(census),"sources":len(sources),"clauses":len(clauses),"slots":len(slots),"witnesses":len(witnesses),"challenges":len(challenges),"outcomes":len(outcomes),"status":len(status),"completeness":len(scope),"catch_proofs":len(catches)},"derivation_sha256":hashlib.sha256((HERE/"DERIVATION_RESULT.json").read_bytes()).hexdigest(),"verdict":"PARTIAL_SEAL_DATA_ONLY; STATIC_DELTA_PHI_ZERO_WITH_FREE_NORMAL_DERIVATIVE; COMPLETE_C2_POLARIZATION_NOT_SELECTED; RAW_RECIPROCITY_SWAP_NOT_A_LORENTZIAN_SEAL_ISOMETRY","certification":"VERIFIED-WITH-CAVEATS: independent source/hash, tangent, mirror, swap, and counterpair reconstruction; no fresh external-model review","compute":{"cpu_only":True,"gpu_used":False,"sympy":sp.__version__}}
 (HERE/"VERIFICATION_RESULT.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");print(json.dumps({"result":"PASS","groups":len(groups),"catch_proofs":len(catches),"verdict":out["verdict"]},sort_keys=True))
if __name__=="__main__":main()
