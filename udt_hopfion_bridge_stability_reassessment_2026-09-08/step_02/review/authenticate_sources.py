import csv,hashlib,json,pathlib,subprocess,sys
root=pathlib.Path.cwd()
review=pathlib.Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
seal=json.loads((review/'SOURCE_FIRST_SEAL.json').read_text())
assert sha((review/'SOURCE_FIRST_MANIFEST.tsv').read_bytes())==seal['source_first_manifest_sha256']
frozen=[]
for row in csv.DictReader((review/'SOURCE_FIRST_MANIFEST.tsv').open(),delimiter='\t'):
    assert sha((review/row['path']).read_bytes())==row['sha256'],row['path']
    frozen.append(row['path'])
scientific=[]
for p in sorted((review/'source_snapshots').rglob('*')):
    if not p.is_file():continue
    name=str(p.relative_to(review/'source_snapshots'))
    if not (name.startswith('udt_g3') and ('/AUDIT_REPORT.md' in name or '/EXACT_DERIVATION.md' in name)) and not name.startswith('startup_surface_g3'):
        continue
    baseline=subprocess.run(['git','-c','core.packedGitWindowSize=1m','-c','core.packedGitLimit=16m','show','7e6d144a9f45fc2cee6d041448e6b6ee9e324cc3:'+name],capture_output=True,check=True)
    assert baseline.stdout==p.read_bytes()==(root/name).read_bytes(),name
    scientific.append(dict(path=name,sha256=sha(baseline.stdout)))
print(json.dumps({'frozen_files_unchanged':len(frozen),'scientific_sources_match_baseline_and_current':scientific,'head_now':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'python':sys.version,'classification':'byte correspondence only, not scientific proof or chronology'},indent=2))
