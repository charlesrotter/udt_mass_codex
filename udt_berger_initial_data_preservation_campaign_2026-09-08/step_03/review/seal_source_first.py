import datetime, hashlib, json, pathlib
p=pathlib.Path(__file__).resolve().parent
names=['REVIEW_SCOPE.md','SOURCE_FIRST_ARGUMENT.md','source_first_check.py',
       'source_first_run.stdout','source_first_run.stderr','source_first_run.json',
       'authenticate_initial_failed.py','authenticate.py','authentication.stdout',
       'authentication.stderr','authentication.json','authentication_retry.stdout',
       'authentication_retry.stderr','authentication_retry.json','seal_source_first.py']
hashes={name:hashlib.sha256((p/name).read_bytes()).hexdigest() for name in names}
auth=json.loads((p/'authentication_retry.stdout').read_text())
record=dict(sealed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    exposure='No BI3 author proof/code/results, BI2, whiteboard or campaign log read.',
    hashes=hashes,source_hashes=auth['sources'],
    result='28 exact algebra checks; 5 actual function-level mutation rejections. CK realizability justified in the argument, not certified by finite jets.',
    preserved_failure='Initial authentication reached final git status but Git threaded lstat failed within 512MiB. Original code/streams retained; retry disables preload threading and optional locks. All source/audit/snapshot checks then passed.',
    independence='Fresh user-designated context; independently constructed BI3 argument/code. Shared accepted and reviewed BI1 sources/SymPy. Exact model unknown; different-model/human/formal axes untested.')
with (p/'SOURCE_FIRST_SEAL.json').open('x') as f: json.dump(record,f,indent=2); f.write('\n')
digest=hashlib.sha256((p/'SOURCE_FIRST_SEAL.json').read_bytes()).hexdigest()
print(json.dumps({'status':'SOURCE_FIRST_SEALED','seal_sha256':digest,'sealed_utc':record['sealed_utc']},indent=2))
