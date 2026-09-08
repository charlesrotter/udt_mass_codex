import hashlib,json,pathlib,subprocess
p=pathlib.Path(__file__).resolve().parent
H=lambda f:hashlib.sha256(pathlib.Path(f).read_bytes()).hexdigest()
sealed=json.loads((p/'SOURCE_FIRST_SEAL.json').read_text())
for name,digest in sealed['hashes'].items():assert H(p/name)==digest,name
for name,digest in sealed['source_hashes'].items():
    assert H(name)==digest,name
    assert H(p/'source_snapshots'/name)==digest,name
auth=json.loads((p/'candidate_authentication.stdout').read_text())
for name,digest in auth['candidate_hashes'].items():
    assert H(p.parent/name)==digest,name
    assert H(p/'candidate_snapshots'/name)==digest,name
assert (p/'author_regression.stdout').read_bytes()==(p/'candidate_snapshots/author_check_01.stdout').read_bytes()
assert json.loads((p/'source_first_run.stdout').read_text())['number_of_checks']==28
assert json.loads((p/'candidate_comparison.stdout').read_text())['check_count']==44
mut=json.loads((p/'mutation_probe_run.stdout').read_text())
assert mut['replayed_author_rejections']==5 and mut['additional_full_Bdot_false_passes']==1
for result in mut['results']:
    assert hashlib.sha256(result['mutant_source'].encode()).hexdigest()==result['mutant_sha256']
    if result['name']=='delete_inverse_metric_derivative':
        assert result['failure'] is None and result['independent_anchor']=='REJECTED'
    else:assert result['failure']['type']=='AssertionError'
receipts={}
for name in ['authentication','authentication_retry','source_first_run','source_first_seal_run',
             'preserve_sources_run','candidate_authentication','candidate_comparison',
             'mutation_probe_run','author_regression']:
    record=json.loads((p/(name+'.json')).read_text())
    assert record['address_space_bytes']==512*1024**2 and record['cpu_seconds']==60
    assert record['timeout'] is False
    assert record['returncode']==(1 if name=='authentication' else 0),name
    receipts[name]=record
git=lambda *args:subprocess.check_output(['git','--no-optional-locks','-c','core.preloadIndex=false',*args],text=True).strip()
assert git('rev-parse','HEAD')=='8593f11cd96a575be3513d1ec56e92ac4f5811ff'
assert git('branch','--show-current')=='grok'
print(json.dumps(dict(status='PASS',source_first_payloads_unchanged=True,declared_sources_unchanged=True,
    frozen_candidate_unchanged=True,snapshots_match=True,author_regression_byte_identical=True,
    report_sha256=H(p/'REVIEW_REPORT.md'),receipts=receipts,
    final_git_status=git('status','--short','--branch'),
    scope='Correspondence and bounded evidence validation only. No source audit execution, synchronization or promotion.'),indent=2))
