#!/usr/bin/env python3
"""Apply frozen cross-route spectral uncertainty policy and preserve the complete maps."""

import csv,json
from collections import Counter
from pathlib import Path

HERE=Path(__file__).resolve().parent
def read(name):
    with (HERE/name).open(newline="",encoding="utf-8") as stream:return list(csv.DictReader(stream,delimiter="\t"))
def write(name,rows):
    with (HERE/name).open("w",newline="",encoding="utf-8") as stream:
        w=csv.DictWriter(stream,fieldnames=list(rows[0]),delimiter="\t",lineterminator="\n");w.writeheader();w.writerows(rows)

production=read("GRAM_INTRINSIC_SUBSPACE_ATLAS.tsv");independent=read("INDEPENDENT_GRAM_INTRINSIC_SUBSPACE_ATLAS.tsv");comparison=read("GRAM_INTRINSIC_SUBSPACE_COMPARISON.tsv")
if len(production)!=len(independent) or len(production)!=len(comparison) or len(production)!=3663:raise RuntimeError("spectral census mismatch")
output=[]
for p,i,c in zip(production,independent,comparison):
    if (p["key"],p["tensor"])!=(i["key"],i["tensor"]) or (p["key"],p["tensor"])!=(c["key"],c["tensor"]):raise RuntimeError("spectral order mismatch")
    row=dict(p)
    resolved=p["status"]==i["status"]=="RESOLVED" and c["pass"]=="TRUE"
    row["independent_status"]=i["status"];row["cross_route_status"]="VERIFIED" if resolved else "SPECTRALLY_UNRESOLVED"
    row["adjudicated_structure"]=p["structure"] if resolved else "SPECTRALLY_UNRESOLVED"
    output.append(row)
write("ADJUDICATED_GRAM_INTRINSIC_SUBSPACE_ATLAS.tsv",output)
result={"schema":"udt-Gram-intrinsic-subspaces-adjudication-v1","status":"PASS_WITH_SPECTRALLY_UNRESOLVED","rows":len(output),"verified_rows":sum(r["cross_route_status"]=="VERIFIED" for r in output),"spectrally_unresolved_rows":sum(r["cross_route_status"]!="VERIFIED" for r in output),"adjudicated_structure_counts":dict(sorted(Counter(r["adjudicated_structure"] for r in output).items())),"per_tensor_structure_counts":{tensor:dict(sorted(Counter(r["adjudicated_structure"] for r in output if r["tensor"]==tensor).items())) for tensor in ("k_riem","k_ric","k_weyl")},"resolved_candidate_2plane_counts":dict(sorted(Counter(r["candidate_2plane_count"] for r in output if r["cross_route_status"]=="VERIFIED").items()))}
(HERE/"GRAM_INTRINSIC_SUBSPACE_ADJUDICATION.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n");print(json.dumps(result,indent=2,sort_keys=True))
