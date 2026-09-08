import datetime,hashlib,json,pathlib,re
p=pathlib.Path(__file__).resolve().parent
step=p.parent
H=lambda b:hashlib.sha256(b).hexdigest()
seal=json.loads((p/'SOURCE_FIRST_SEAL.json').read_text())
for name,digest in seal['hashes'].items(): assert H((p/name).read_bytes())==digest,name
for name,digest in seal['source_hashes'].items(): assert H(pathlib.Path(name).read_bytes())==digest,name
freeze=(step/'CANDIDATE_FREEZE.md').read_text()
pairs=re.findall(r'^\s+([0-9a-f]{64})\s+(\S+)\s*$',freeze,re.M)
assert len(pairs)==4
for digest,name in pairs: assert H((step/name).read_bytes())==digest,name
names=['CANDIDATE_FREEZE.md','CANDIDATE_INITIAL.md','check_bi3.py',
       'author_check_01.stdout','author_check_01.stderr','author_check_01.json',
       'author_mutations_01.stdout','author_mutations_01.stderr','author_mutations_01.json']
snap=p/'candidate_snapshots'; snap.mkdir(exist_ok=True)
hashes={}
for name in names:
    data=(step/name).read_bytes(); hashes[name]=H(data)
    with (snap/name).open('xb') as f:f.write(data)
check=json.loads((step/'author_check_01.stdout').read_text())
assert check['status']=='PASS' and check['source_sha256']==hashes['check_bi3.py']
assert len(check['checks'])==55 and len(check['fixtures'])==12
for prefix in ['author_check_01','author_mutations_01']:
    run=json.loads((step/(prefix+'.json')).read_text())
    assert run['returncode']==0 and run['timeout'] is False
    assert run['address_space_bytes']==512*1024**2 and run['cpu_seconds']==60
mutants=json.loads((step/'author_mutations_01.stdout').read_text())
assert mutants['original_sha256']==hashes['check_bi3.py']
assert mutants['count']==mutants['rejected']==5
for mutant in mutants['results']:
    assert H(mutant['mutant_source'].encode())==mutant['mutant_sha256']
    assert mutant['rejected'] and mutant['failure']['type']=='AssertionError'
print(json.dumps(dict(status='PASS',authenticated_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    exposure='Candidate freeze first opened after source-first seal. Author proof/code/results now read. No BI2 scientific package, campaign log or whiteboard opened.',
    candidate_hashes=hashes,source_first_seal_sha256=H((p/'SOURCE_FIRST_SEAL.json').read_bytes()),
    preserved_candidate_files=len(names),author_check_count=55,author_fixture_count=12,
    saved_mutations=5,parent_no_review_exposure='Attested in CANDIDATE_FREEZE.md; not independently observed.'),indent=2))
