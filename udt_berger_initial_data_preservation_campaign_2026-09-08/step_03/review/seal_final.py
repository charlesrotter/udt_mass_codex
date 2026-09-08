import datetime,hashlib,json,pathlib
p=pathlib.Path(__file__).resolve().parent
H=lambda f:hashlib.sha256(pathlib.Path(f).read_bytes()).hexdigest()
source=json.loads((p/'SOURCE_FIRST_SEAL.json').read_text())
for name,digest in source['hashes'].items():assert H(p/name)==digest,name
for name,digest in source['source_hashes'].items():assert H(name)==digest,name
author=json.loads((p/'candidate_authentication.stdout').read_text())
for name,digest in author['candidate_hashes'].items():assert H(p.parent/name)==digest,name
result=json.loads((p/'REVIEW_RESULT.json').read_text())
assert H(p/'REVIEW_REPORT.md')==result['report_sha256']
assert result['verdict']=='VERIFIED-WITH-CAVEATS' and result['scientific_repair_required'] is False
hashes={str(f.relative_to(p)):H(f) for f in sorted(p.rglob('*')) if f.is_file()
        and f.name!='FINAL_REVIEW_SEAL.json' and not f.name.startswith('final_seal_run.')}
record=dict(sealed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    verdict=result['verdict'],report_sha256=result['report_sha256'],
    source_first_seal_sha256=H(p/'SOURCE_FIRST_SEAL.json'),hashes=hashes,
    exclusions='This seal and final_seal_run streams/receipt exclude themselves to avoid self-reference. Later runtime messages are not presealed payloads.',
    scope='Review-only evidence identity, not promotion, independent chronology or proof of truth.')
with (p/'FINAL_REVIEW_SEAL.json').open('x') as f:json.dump(record,f,indent=2);f.write('\n')
print(json.dumps(dict(status='FINAL_REVIEW_SEALED',verdict=record['verdict'],
    seal_sha256=H(p/'FINAL_REVIEW_SEAL.json'),report_sha256=record['report_sha256'],
    sealed_file_count=len(hashes)),indent=2))
