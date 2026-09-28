"""Packaging/fidelity correspondence only; no scientific calculations replayed."""
from pathlib import Path
import hashlib,json,datetime,subprocess,time
packet=Path('udt_positional_geometry_clock_connection_2026-09-28')
hashf=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
freeze=json.loads((packet/'FINAL_REVIEW_FREEZE.json').read_text())
checks={k:hashf(k)==v for k,v in freeze['files'].items()}
initial=(packet/'INITIAL_CANDIDATE.md').read_text();candidate=(packet/'CANDIDATE.md').read_text()
body_equal=initial[initial.index('Baseline,'):]==candidate[candidate.index('Baseline,'):]
direct=json.loads((packet/'DIRECT_REVIEW_FREEZE.json').read_text())
initial_pinned=hashf(packet/'INITIAL_CANDIDATE.md')==direct['files'][str(packet/'CANDIDATE.md')]
pins=json.loads((packet/'SOURCE_PINS.json').read_text());src={**pins['sources'],**pins['supplemental_sources']}
source_checks={}
for path,sha in src.items():
    baseline=subprocess.run(['git','show',pins['baseline_head']+':'+path],capture_output=True,check=True).stdout
    source_checks[path]={'pinned':hashf(path)==sha,'baseline_bytes':Path(path).read_bytes()==baseline}

# The original parent baseline is git-status presentation, including quotes on
# "Mass creates gravity.txt". Compare actual pathnames, not display strings.
untracked=subprocess.run(['git','ls-files','--others','--exclude-standard','-z'],capture_output=True,check=True).stdout.decode().rstrip('\0').split('\0')
outside=[p for p in untracked if not p.startswith(str(packet)+'/')]
baseline_display=json.loads((packet/'BASELINE_UNTRACKED_PATHS.json').read_text())
baseline_names=[json.loads(p) if p.startswith('"') else p for p in baseline_display]
tracked=subprocess.run(['git','diff','--name-only'],capture_output=True,text=True,check=True).stdout.splitlines()
expected=sorted(['CURRENT_RESEARCH_PROGRAM.md','HANDOFF.md','INDEX.md','LIVE.md','MEMORY.md','UDT_RESEARCH_ROADMAP.md'])
closing=json.loads((packet/'closing_premise_audit/execution.json').read_text())
closing_stdout=(packet/'closing_premise_audit/stdout.txt').read_text()
commands=[]
for command in [['python3','-c','import verify_current_scientific_premises as v; v.validate_startup_surface(v.ROOT); print("Current startup surface validator: PASS")'],['git','diff','--check']]:
    tick=time.monotonic();run=subprocess.run(command,capture_output=True,text=True,timeout=120)
    commands.append({'command':command,'returncode':run.returncode,'stdout':run.stdout,'stderr':run.stderr,'elapsed_seconds':time.monotonic()-tick})
record={'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'final_freeze_matches':checks,'candidate_body_identical':body_equal,'initial_candidate_matches_direct_freeze':initial_pinned,'source_checks':source_checks,'outside_packet_untracked_names_match':outside==baseline_names,'outside_packet_untracked_count':len(outside),'display_normalizations':[(p,q) for p,q in zip(baseline_display,baseline_names) if p!=q],'tracked_paths_match_whitelist':sorted(tracked)==expected,'closing_full_audit_attributed_record':{'returncode':closing['returncode'],'elapsed_seconds':closing['elapsed_seconds'],'seven_input_hashes_match':closing['input_sha256_at_start']==closing['input_sha256_at_finish'],'seven_inputs_count':len(closing['input_sha256_at_start']),'stdout_contains_406_pass':'PASS: 406-row premise registry' in closing_stdout,'stderr_empty':not (packet/'closing_premise_audit/stderr.txt').read_bytes(),'stdout_sha256':hashf(packet/'closing_premise_audit/stdout.txt')},'reviewer_focused_commands':commands}
record['all_pass']=all(checks.values()) and body_equal and initial_pinned and outside==baseline_names and sorted(tracked)==expected and all(all(v.values()) for v in source_checks.values()) and not any(c['returncode'] for c in commands)
print(json.dumps(record,indent=2))
if not record['all_pass']:raise RuntimeError('Final correspondence failure; see stdout record.')
