import hashlib
import pathlib

root = pathlib.Path(__file__).resolve().parent
manifest = root / 'STAGE_A_SHA256SUMS'
assert not manifest.exists(), 'refuse Stage A reseal'
files = sorted(p for p in root.iterdir() if p.is_file())
with manifest.open('x') as stream:
    for p in files:
        stream.write(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n')
for p in (root/'STAGE_A_SOURCE_FIRST_RECONSTRUCTION.md', manifest):
    print(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p))
print('payload_count='+str(len(files)))
