import csv, datetime, hashlib, json, pathlib, subprocess

root = pathlib.Path.cwd()
campaign = pathlib.Path('udt_berger_initial_data_preservation_campaign_2026-09-08')
H = lambda p: hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
expected_head = '8593f11cd96a575be3513d1ec56e92ac4f5811ff'
git = lambda *args: subprocess.check_output(['git', *args], text=True).strip()
head = git('rev-parse','HEAD')
remote = git('rev-parse','refs/remotes/origin/grok')
branch = git('branch','--show-current')
assert head == remote == expected_head and branch == 'grok'
fetch = pathlib.Path(git('rev-parse','--git-path','FETCH_HEAD'))
fetch_hashes = [line.split('\t')[0] for line in fetch.read_text().splitlines()]
assert expected_head in fetch_hashes
receipt = json.loads((campaign/'STARTUP_AUDIT.json').read_text())
assert receipt['command'] == ['python3','-B','verify_current_scientific_premises.py']
assert receipt['cwd'] == str(root)
assert receipt['returncode'] == 0 and receipt['timeout'] is False
for ext in ['stdout','stderr']:
    assert receipt[ext] == (campaign/('STARTUP_AUDIT.'+ext)).read_text()
assert 'PASS: 358-row premise registry' in receipt['stdout']
manifest = {}
for line in (campaign/'SOURCE_SHA256SUMS').read_text().splitlines():
    digest, name = line.split(maxsplit=1)
    manifest[name] = digest
names = ['AGENTS.md','CLAUDE.md','CURRENT_SCIENTIFIC_PREMISES.tsv',
         'verify_current_scientific_premises.py',
         'udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py',
         'udt_g315_conditional_cauchy_characteristic_data_interface_2026-09-01/EXACT_DERIVATION.md',
         'udt_g330_berger_hopf_eigenline_local_persistence_2026-09-02/EXACT_DERIVATION.md',
         'udt_g337_double_silent_third_normal_ownership_2026-09-03/EXACT_DERIVATION.md']
for name in names: assert H(name) == manifest[name], name
bi1 = campaign/'step_01'
assert H(bi1/'CANDIDATE_INITIAL.md') == 'ce6b36dce14c07049ee9be193ca07989c5ea2f2507d8587c7b978317d0980fbc'
assert H(bi1/'review/REVIEW_REPORT.md') == 'f68aeba4a80fa7b095122d7ea07bc45e3d0213bddbee1d23d64f96e2cd538c80'
with open('CURRENT_SCIENTIFIC_PREMISES.tsv') as f:
    rows = list(csv.DictReader(f, delimiter='\t'))
assert len(rows) == 358
names += [str(bi1/x) for x in ['CANDIDATE_INITIAL.md','REVIEWED_RESULT.md',
          'review/REVIEW_REPORT.md','review/SOURCE_FIRST_ARGUMENT.md']]
names += [str(campaign/x) for x in ['STARTUP_AUDIT.json','STARTUP_AUDIT.stdout',
          'STARTUP_AUDIT.stderr','STARTUP_AUDIT.command.txt','SOURCE_SHA256SUMS',
          'step_03/QUESTION.md','step_03/METHOD_SOURCE.md','step_03/REVIEW_DISPATCH.md']]
print(json.dumps(dict(status='PASS', observed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    head=head, local_remote_ref=remote, branch=branch,
    fetch_hashes=fetch_hashes, fetch_mtime_utc=datetime.datetime.fromtimestamp(fetch.stat().st_mtime,datetime.timezone.utc).isoformat(),
    sync_scope='Parent snapshot correspondence, not new network freshness; parent BI1 review receipt reused without reading campaign log.',
    parent_audit=receipt, registry_count=358,
    sources={n:H(n) for n in names},
    grades={r['premise_id']:r['epistemic_label'] for r in rows if r['premise_id'] in ['G315','G330','G337']},
    git_status=git('status','--short','--branch')), indent=2))
