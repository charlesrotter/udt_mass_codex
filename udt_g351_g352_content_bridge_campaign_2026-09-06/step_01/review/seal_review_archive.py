"""Generate final read-only checks, exact archive membership, and SHA-256 manifest."""
from pathlib import Path
import argparse,datetime,hashlib,json,subprocess
ap=argparse.ArgumentParser();ap.add_argument("--repo",type=Path,required=True)
args=ap.parse_args();repo=args.repo.resolve();out=Path(__file__).resolve().parent
commands=[("stage_a_final_auth",["sha256sum","--check","STAGE_A_SHA256SUMS"],out),
 ("final_source_diff",["git","diff","--exit-code","c19b5fb147d6afbfd91ec248b0693dfc834ce220","--","founding.md","startup_surface_g310_universal_reciprocity_refresh_2026-08-31/ADOPTION_RECORD.md","udt_g261_universal_metric_coupling_parent_operator_ownership_2026-08-25/AUDIT_REPORT.md"],repo),
 ("final_repository_metadata",["git","status","--short","--branch"],repo)]
records=[]
for name,command,cwd in commands:
    r=subprocess.run(command,cwd=cwd,capture_output=True,timeout=60)
    for suffix,data in [("stdout",r.stdout),("stderr",r.stderr)]:
        target=out/(name+"."+suffix);assert not target.exists();target.write_bytes(data)
    records.append({"command":command,"cwd":str(cwd),"exit":r.returncode,
      "stdout_sha256":hashlib.sha256(r.stdout).hexdigest(),"stderr_sha256":hashlib.sha256(r.stderr).hexdigest()})
    assert r.returncode==0
target=out/"FINAL_METADATA.json";assert not target.exists()
target.write_text(json.dumps({"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"commands":records},indent=2)+"\n")
listing=out/"ARCHIVE_FILES.txt";manifest=out/"REVIEW_SHA256SUMS"
assert not listing.exists() and not manifest.exists()
names=sorted([str(p.relative_to(out)) for p in out.rglob("*") if p.is_file()]+[listing.name,manifest.name])
listing.write_text("\n".join(names)+"\n")
manifest.write_text("".join(hashlib.sha256((out/name).read_bytes()).hexdigest()+"  "+name+"\n" for name in names if name!=manifest.name))
assert sorted(str(p.relative_to(out)) for p in out.rglob("*") if p.is_file())==names
print(json.dumps({"archive_files":len(names),"manifest_payloads":len(names)-1,
"stage_a_report_sha256":hashlib.sha256((out/"STAGE_A_SOURCE_FIRST_REVIEW.md").read_bytes()).hexdigest(),
"stage_b_report_sha256":hashlib.sha256((out/"STAGE_B_ADVERSARIAL_REVIEW.md").read_bytes()).hexdigest(),
"review_verdict_sha256":hashlib.sha256((out/"REVIEW_VERDICT.json").read_bytes()).hexdigest(),
"archive_manifest_sha256":hashlib.sha256(manifest.read_bytes()).hexdigest()},indent=2))
