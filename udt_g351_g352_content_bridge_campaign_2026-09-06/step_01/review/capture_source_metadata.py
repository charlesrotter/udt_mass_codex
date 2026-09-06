"""Read-only repository authentication, with evidence only in this scratch directory."""
from pathlib import Path
import datetime, hashlib, json, subprocess, sys

repo=Path(sys.argv[1]).resolve()
out=Path(__file__).resolve().parent
snapshot="c19b5fb147d6afbfd91ec248b0693dfc834ce220"
sources=["AGENTS.md","LIVE.md","HANDOFF.md","CURRENT_RESEARCH_PROGRAM.md",
"CURRENT_SCIENTIFIC_PREMISES.md","CURRENT_SCIENTIFIC_PREMISES.tsv","CLAUDE.md","INDEX.md","MEMORY.md",
"startup_surface_g312_two_premise_adoption_refresh_2026-09-01/ADOPTION_RECORD.md",
"udt_g313_curvature_phase_current_candidate_2026-09-06/CANDIDATE_ARGUMENT.md",
"udt_g313_curvature_phase_current_candidate_2026-09-06/REVIEW_RECORD.md",
"udt_g313_curvature_phase_current_candidate_2026-09-06/review_2026-09-06/STAGE_B_ADVERSARIAL_REVIEW.md"]
for package in ["udt_g312_quiet_gr_response_constitution_discriminator_2026-09-01",
"udt_g313_tracefree_ricci_solution_space_bootstrap_map_2026-09-01",
"udt_g350_frequency_area_carried_content_ownership_2026-09-05",
"udt_g351_source_free_labelwise_carried_measure_conservation_2026-09-05",
"udt_g352_clock_rate_carried_measure_readout_2026-09-05"]:
    sources += [package+"/AUDIT_REPORT.md",package+"/EXACT_DERIVATION.md"]
sources += [".claude/skills/"+s+"/SKILL.md" for s in
            ["no-shortcuts","completeness-map","solution-space-not-imposition","verifier-before-record"]]
commands=[]
def run(args):
    r=subprocess.run(args,cwd=repo,capture_output=True,timeout=60)
    commands.append({"command":args,"cwd":str(repo),"exit":r.returncode,
                     "stdout":r.stdout.decode(),"stderr":r.stderr.decode()})
    assert r.returncode==0,args
    return r.stdout
branch=run(["git","branch","--show-current"]).decode().strip()
head=run(["git","rev-parse","HEAD"]).decode().strip()
run(["git","status","--short","--branch"])
run(["git","log","-8","--oneline"])
rows=[]
for path in sources:
    frozen=run(["git","show",snapshot+":"+path])
    current=(repo/path).read_bytes()
    assert current==frozen,path
    rows.append({"path":path,"sha256":hashlib.sha256(current).hexdigest(),
                 "equals_source_snapshot":True})
# Preserve exact command/exit/stderr but do not duplicate source content in logs.
for command in commands:
    if command["command"][:2]==["git","show"]:
        raw=command.pop("stdout").encode()
        command["stdout_sha256"]=hashlib.sha256(raw).hexdigest()
        command["stdout_note"]="exact source bytes retained in named read-only repository path"
record={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"branch":branch,"head":head,
"snapshot":snapshot,"remote_freshness":"UNVERIFIED_IN_REVIEWER_CONTEXT", "sources":rows,"commands":commands}
(out/"STAGE_A_SOURCE_METADATA.json").write_text(json.dumps(record,indent=2)+"\n")
print(json.dumps({"branch":branch,"head":head,"matched_source_files":len(rows),
                  "metadata_sha256":hashlib.sha256((out/"STAGE_A_SOURCE_METADATA.json").read_bytes()).hexdigest()},indent=2))
