"""Packaging-only correspondence and declared-scope checks; no science recomputation."""
import hashlib
import json
import pathlib
import subprocess

R=pathlib.Path(__file__).resolve().parents[3]
P=pathlib.Path(__file__).resolve().parent
campaign=P.parents[1]
manifest=P/"REVIEW_MANIFEST.tsv"
entries=[]
for line in manifest.read_text().splitlines()[1:]:
    sha,path=line.split("\t")
    actual=hashlib.sha256((R/path).read_bytes()).hexdigest()
    assert actual==sha,path
    entries.append(path)
def git(*args):
    p=subprocess.run(["git",*args],cwd=R,capture_output=True,text=True,timeout=10)
    return {"command":["git",*args],"returncode":p.returncode,"stdout":p.stdout,"stderr":p.stderr}
head=git("rev-parse","HEAD")
assert head["returncode"]==0 and head["stdout"].strip()=="291bbd73584318f87697345cd86c48f17064e5de"
changes=git("diff","--name-only","HEAD")
assert changes["returncode"]==0
allowed={"LIVE.md","HANDOFF.md","CURRENT_RESEARCH_PROGRAM.md"}
assert set(changes["stdout"].splitlines()).issubset(allowed)
scope_preservation=git("diff","--exit-code","HEAD","--","udt_complementary_wave_observable_campaign_2026-09-07","udt_gw170817_fixed_window_test_campaign_2026-09-07","CANON.md","CURRENT_SCIENTIFIC_PREMISES.md","CURRENT_SCIENTIFIC_PREMISES.tsv","UDT_METRIC_KERNEL_DEVELOPMENT.md","UDT_METRIC_KERNEL_COVERAGE.tsv")
assert scope_preservation["returncode"]==0 and not scope_preservation["stdout"]
names=["DECISION_BRIEF.md","README.md"]
pins={str(campaign/name):hashlib.sha256((campaign/name).read_bytes()).hexdigest() for name in names}
for name in sorted(allowed):
    pins[name]=hashlib.sha256((R/name).read_bytes()).hexdigest()
# Preserve the already pinned EOF whitespace rather than change historical hashes.
whitespace=[]
for path in entries:
    result=git("diff","--check","--no-index","/dev/null",path)
    if result["returncode"]:
        assert result["returncode"]==2,(path,result)
        assert "new blank line at EOF." in result["stdout"],(path,result)
        assert len(result["stdout"].splitlines())==1,(path,result)
        whitespace.append(result)
    else:
        assert result["stdout"]==""
print(json.dumps({"passed":True,"scope":"packaging-only, no scientific tests repeated","head":head["stdout"].strip(),"review_manifest_entries_verified":len(entries),"integration_pins":pins,"tracked_changes":changes["stdout"].splitlines(),"source_preservation":scope_preservation,"preserved_pinned_whitespace_exceptions":whitespace,"unrelated_untracked_payloads":"not opened or hashed; parent name-preservation record is separate","remote_freshness":"not independently checked by reviewer"},sort_keys=True,indent=2))
