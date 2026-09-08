import hashlib,json,pathlib
p=pathlib.Path(__file__).resolve().parent
seal=json.loads((p/'SOURCE_FIRST_SEAL.json').read_text())
saved={}
for name,digest in seal['source_hashes'].items():
    data=pathlib.Path(name).read_bytes()
    assert hashlib.sha256(data).hexdigest()==digest,name
    target=p/'source_snapshots'/name
    target.parent.mkdir(parents=True,exist_ok=True)
    with target.open('xb') as f: f.write(data)
    saved[name]=digest
print(json.dumps({'status':'PASS','preserved_source_count':len(saved),'hashes':saved},indent=2))
