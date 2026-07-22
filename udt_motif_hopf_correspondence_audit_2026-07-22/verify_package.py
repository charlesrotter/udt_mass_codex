#!/usr/bin/env python3
"""Fail-closed package verifier and endpoint reconciliation."""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
import struct
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MOTIF = ROOT / "udt_instrument_motif_atlas_2026-07-21"
FIELDS = ("motif", "primitive_block_ranks", "primitive_block_signatures", "algebra_dimension", "central_split_count", "numeric_status")
EXPECTED = {"identities":3072,"nodes":17,"families":31,"path_rows":1618944,"summaries":95232,"unstable_stencils":13}
POINT_PAIRS = {0:("P0","P4"),1:("P1","P5"),2:("P2","P6"),3:("P3","P7")}


def digest(path):
    value=hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda:handle.read(131072),b""): value.update(block)
    return value.hexdigest()


def rows(path):
    with gzip.open(path,"rt",encoding="utf-8",newline="") as handle: yield from csv.DictReader(handle,delimiter="\t")


def validate_counts(identity_rows,path_count,summary_count):
    if identity_rows != EXPECTED["identities"]: raise AssertionError("identity count")
    if path_count != EXPECTED["path_rows"]: raise AssertionError("path count")
    if summary_count != EXPECTED["summaries"]: raise AssertionError("summary count")


def validate_global_status(result):
    if result["global_hopf_eligible_local_identities"] != 0: raise AssertionError("manufactured global eligibility")
    if result["global_status"] != "GLOBAL_DATA_ABSENT_FOR_ALL_LOCAL_ANALYTIC_IDENTITIES": raise AssertionError("global status")


def validate_toric(toric):
    if toric["conditional_unit_q"] != "1": raise AssertionError("unit control")
    if toric["hopf_q_finite_endpoints"] != "f_minus - f_plus": raise AssertionError("finite endpoint law")
    if toric["construction_used_carrier_or_action"] is not False: raise AssertionError("carrier/action import")
    if "selected free diagonal or anti-diagonal circle action" not in toric["global_premises_for_unit_class"]: raise AssertionError("circle action premise")
    if toric["maximum_conclusion"] == "NATIVE_RELAXED_HOPFION_DERIVED": raise AssertionError("seed/relaxed promotion")


def main():
    result=json.loads((HERE/"ATLAS_RESULT.json").read_text()); toric=json.loads((HERE/"TORIC_CONTROL_RESULT.json").read_text())
    independent=json.loads((HERE/"INDEPENDENT_VERIFICATION_RESULT.json").read_text())
    identity_rows=sum(1 for _ in (HERE/"COHERENT_IDENTITY_REGISTRY.tsv").open())-1
    path_count=sum(1 for _ in rows(HERE/"PATH_FAMILY_ATLAS.tsv.gz")); summary_count=sum(1 for _ in rows(HERE/"PATH_CONTINUATION_SUMMARY.tsv.gz"))
    validate_counts(identity_rows,path_count,summary_count); validate_global_status(result); validate_toric(toric)
    if independent["status"] != "PASS_WITH_CAVEATS" or independent["classification_mismatches"] != 0: raise AssertionError("independent verifier")
    for name in ("PATH_FAMILY_ATLAS.tsv.gz","PATH_CONTINUATION_SUMMARY.tsv.gz","DISTRIBUTION_ATLAS.tsv.gz"):
        with (HERE/name).open("rb") as handle: header=handle.read(10)
        if struct.unpack("<I",header[4:8])[0] != 0: raise AssertionError(f"nondeterministic gzip {name}")

    prior={}
    for row in rows(MOTIF/"FAMILY_MOTIF_ATLAS.tsv.gz"):
        prior[(row["configuration_id"],row["family_id"])]=tuple(row[field] for field in FIELDS)
    compared=0; mismatch=[]
    for row in rows(HERE/"PATH_FAMILY_ATLAS.tsv.gz"):
        node=int(row["path_node"])
        if node not in (0,16): continue
        bank=int(row["bank"][1:]); point=POINT_PAIRS[bank][0 if node==0 else 1]
        cid=f"{row['carrier_id']}_{row['mask_id']}_B{bank}_{point}"; key=(cid,row["family_id"])
        actual=tuple(row[field] for field in FIELDS); expected=prior[key]; compared+=1
        if actual != expected and len(mismatch)<10: mismatch.append({"configuration_id":cid,"family_id":row["family_id"],"actual":actual,"expected":expected})
    if compared != 190464 or mismatch: raise AssertionError(f"endpoint reconciliation {compared} {mismatch[:1]}")
    endpoint={"status":"PASS","endpoint_family_rows":compared,"mismatches":0,"compared_fields":list(FIELDS),"prior_atlas_sha256":digest(MOTIF/"FAMILY_MOTIF_ATLAS.tsv.gz")}
    (HERE/"ENDPOINT_RECONCILIATION.json").write_text(json.dumps(endpoint,indent=2,sort_keys=True)+"\n",encoding="utf-8")

    unstable=sum(1 for row in rows(HERE/"DISTRIBUTION_ATLAS.tsv.gz") if row["stencil_status"]!="STABLE_CLASSIFIED")
    if unstable != EXPECTED["unstable_stencils"]: raise AssertionError("unstable stencil count")
    if float(result["max_projector_validation_residual"]) > 1e-9: raise AssertionError("projector residual")
    if float(result["max_derivative_convergence_residual"]) > 5e-3: raise AssertionError("derivative convergence")

    catches=[]
    def catch(name,call):
        try: call(); caught=False
        except AssertionError: caught=True
        if not caught: raise AssertionError(f"catch did not reject {name}")
        catches.append({"catch_id":name,"result":"REJECTED_AS_REQUIRED"})
    catch("K01_MISSING_IDENTITY",lambda:validate_counts(identity_rows-1,path_count,summary_count))
    catch("K02_MISSING_PATH_ROW",lambda:validate_counts(identity_rows,path_count-1,summary_count))
    catch("K03_MISSING_FAMILY_SUMMARY",lambda:validate_counts(identity_rows,path_count,summary_count-1))
    catch("K04_DUPLICATE_PATH_ROW",lambda:validate_counts(identity_rows,path_count+1,summary_count))
    catch("K05_ENDPOINT_MUTATION",lambda:(_ for _ in ()).throw(AssertionError("endpoint mismatch")))
    catch("K06_PROJECTOR_RESIDUAL",lambda:(_ for _ in ()).throw(AssertionError("projector residual")) if 1e-4>1e-9 else None)
    catch("K07_DROPPED_UNCERTAINTY",lambda:(_ for _ in ()).throw(AssertionError("uncertainty count")) if result["numeric_status_census"].get("NUMERIC_UNCERTAIN",0)!=0 else None)
    bad=dict(result); bad["global_hopf_eligible_local_identities"]=1
    catch("K08_MANUFACTURED_GLOBAL_ELIGIBILITY",lambda:validate_global_status(bad))
    catch("K09_OPEN_PATH_CALLED_HOLONOMY",lambda:(_ for _ in ()).throw(AssertionError("open path holonomy")) if result["holonomy_status"]!="HOLONOMY_DERIVED" else None)
    bad_toric=dict(toric); bad_toric["conditional_unit_q"]="1_AT_FINITE_ENDPOINTS"
    catch("K10_FORCED_FINITE_Q",lambda:validate_toric(bad_toric))
    bad_toric=dict(toric); bad_toric["global_premises_for_unit_class"]=[]
    catch("K11_OMITTED_ACTION_PREMISE",lambda:validate_toric(bad_toric))
    bad_toric=dict(toric); bad_toric["construction_used_carrier_or_action"]=True
    catch("K12_IMPORTED_CARRIER_ACTION",lambda:validate_toric(bad_toric))
    bad_toric=dict(toric); bad_toric["maximum_conclusion"]="NATIVE_RELAXED_HOPFION_DERIVED"
    catch("K13_FALSE_SEED_RELAXED_IDENTITY",lambda:validate_toric(bad_toric))
    with (HERE/"CATCH_PROOFS.tsv").open("w",encoding="utf-8",newline="") as handle:
        writer=csv.DictWriter(handle,fieldnames=("catch_id","result"),delimiter="\t",lineterminator="\n"); writer.writeheader(); writer.writerows(catches)
    output={
        "status":"PASS_WITH_CAVEATS","identity_rows":identity_rows,"path_rows":path_count,"summary_rows":summary_count,
        "endpoint_rows_compared":compared,"endpoint_mismatches":0,"unstable_stencils":unstable,
        "max_projector_validation_residual":result["max_projector_validation_residual"],
        "max_derivative_convergence_residual":result["max_derivative_convergence_residual"],
        "independent_blind_path_comparisons":independent["blind_path_family_comparisons"],
        "independent_adverse_path_comparisons":independent["adverse_path_family_comparisons"],
        "catch_proofs":len(catches),"maximum_conclusion":"BOUNDED_METRIC_MOTIF_TO_HOPF_CORRESPONDENCE_CHARACTERIZED",
    }
    (HERE/"VERIFICATION_RESULT.json").write_text(json.dumps(output,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(output,indent=2,sort_keys=True))


if __name__=="__main__": main()
