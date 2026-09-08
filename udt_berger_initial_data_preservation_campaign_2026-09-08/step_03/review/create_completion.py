import datetime,hashlib,json,pathlib,shlex
p=pathlib.Path(__file__).resolve().parent
root=pathlib.Path.cwd()
H=lambda f:hashlib.sha256(pathlib.Path(f).read_bytes()).hexdigest()
integrity=json.loads((p/'final_integrity.stdout').read_text())
assert integrity['status']=='PASS'
auth=json.loads((p/'candidate_authentication.stdout').read_text())
record=dict(verdict='VERIFIED-WITH-CAVEATS',reviewed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    candidate_sha256=auth['candidate_hashes']['CANDIDATE_INITIAL.md'],
    candidate_code_sha256=auth['candidate_hashes']['check_bi3.py'],
    report='REVIEW_REPORT.md',report_sha256=H(p/'REVIEW_REPORT.md'),
    source_first_seal_sha256=H(p/'SOURCE_FIRST_SEAL.json'),
    actual_local_analytic_realizability='Verified as a noncharacteristic analytic CK theorem application to the exact nonlinear constraints.',
    full_first_normal_drift='Y(o)=epsilon*e2/Delta; full Pdot has symmetric23/32 entries epsilon/Delta. K(o)=h gamma and DK(o)=0.',
    quantifiers='Every fixed a,c>0,a!=c,h!=0 and epsilon real; same Lambda=R/2+3h^2; possibly parameter-dependent open patch.',
    scientific_repair_required=False,scientific_repair_cycles_used=0,unresolved_load_bearing_objections=[],
    evidence=dict(source_first_exact_checks=28,source_first_function_mutation_rejections=5,
        post_exposure_independent_checks=44,fixtures_independently_recomputed=12,
        author_regression_checks=55,author_stdout_byte_identical=True,
        frozen_author_mutation_rejections_reproduced=5,additional_full_Bdot_harness_false_passes=1,
        additional_false_pass_independently_detected=True,final_integrity='PASS'),
    caveats=[
        'Local real-analytic construction only; no global compact-S3 extension, gluing, uniform estimates or smooth nonanalytic constraint theorem.',
        'CK and local smooth Einstein-Cauchy results are imported mathematical methods with checked application hypotheses, not physical premises or finite-check consequences.',
        'Actual-time departure uses a marked local Gaussian comparison and the admitted local Cauchy method; no orbit closure, topology or stability theorem.',
        'Original author code is correct. Deleting diagonal inverse-metric variation still passes all55 scoped author checks; the independent full-Bdot anchor detects the incorrect complete derivative.',
        'BI1 remains provisional reviewed input, including its two author-harness false passes and independent full-tensor verification.',
        'Parent synchronization/full358 audit authenticated and reused, not independently replayed or current remote freshness established.',
        'Exact backend/different-model/human/formal axes remain unknown or untested; sources/SymPy and standard mathematical methods are shared.',
        'Initial review authentication Git threaded-lstat failure and bounded launcher repair are preserved. No scientific candidate repair was needed.'
    ],not_promoted=True,shared_git_mutation_commands=False,write_scope='step_03/review only')
with (p/'REVIEW_RESULT.json').open('x') as f:json.dump(record,f,indent=2);f.write('\n')
runner='udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py'
env=['env','OPENBLAS_NUM_THREADS=1','OMP_NUM_THREADS=1','MKL_NUM_THREADS=1','PYTHONDONTWRITEBYTECODE=1']
lines=['# BI3 review execution record','',
       'All paths below are review-owned evidence. Parent and accepted sources were read only.',
       'Each launcher uses the read existing run_capture.py, 512MiB address space,',
       '60-second CPU/wall limits and one numerical-library thread. Python3.10.12,',
       'SymPy1.13.1. No GPU/grid/evolution process. No duplicate full358 audit or sync.',
       '', 'Source-first seal: 2026-09-08T18:43:30.597780+00:00. Candidate exposure followed',
       'that seal after CANDIDATE_FREEZE.md became available. Tool transcript records',
       'initial inspection/reads, direct primary method retrieval and freeze polling.',
       'No mathematical conclusions were sent before the author freeze became available.',
       '', 'The first authentication failure is preserved; retry changes only read-only',
       'Git invocation to disable preload threading and optional locks. The frozen',
       'candidate had no scientific repair. Deliberate mutant assertion failures are',
       'successful adversarial probes, distinct from the failed authentication launcher.',
       '', 'Exact commands (raw streams and JSON share each capture prefix):','']
prefixes=['authentication','authentication_retry','source_first_run','source_first_seal_run',
          'preserve_sources_run','candidate_authentication','candidate_comparison',
          'mutation_probe_run','author_regression','final_integrity']
for name in prefixes:
    r=json.loads((p/(name+'.json')).read_text())
    command=env+['python3','-B',runner,str(p/name),str(root)]+r['command']
    lines.extend(['## '+name,'', '```bash',shlex.join(command),'```','',
        f"Observed: exit {r['returncode']}; timeout {r['timeout']}; {r['duration_seconds']:.9f}s; child RSS {r['maxrss_kib']}KiB.",''])
lines.extend(['The completion generator and final seal likewise run under the same launcher;',
              'their exact argument arrays/timestamps are in completion_run.json and',
              'final_seal_run.json. Final seal captures the stable payloads and snapshots;',
              'its own capture stream/receipt are excluded to avoid self-reference.',
              '', 'REVIEW_REPORT.md gives argument audit, omissions and evidence-use limits.',
              'REVIEW_RESULT.json is the machine-readable disposition. FINAL_REVIEW_SEAL.json',
              'records exact final evidence identities; checksums assert correspondence only.',''])
with (p/'EXECUTION_RECORD.md').open('x') as f:f.write('\n'.join(lines))
print(json.dumps(dict(status='PASS',verdict=record['verdict'],report_sha256=record['report_sha256'],
    result_sha256=H(p/'REVIEW_RESULT.json'),execution_record_sha256=H(p/'EXECUTION_RECORD.md')),indent=2))
