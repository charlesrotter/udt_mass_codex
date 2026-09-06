import hashlib
import pathlib
root=pathlib.Path(__file__).resolve().parent
manifest=root/'CLOSURE_SHA256SUMS'
membership=root/'ARCHIVE_FILES.txt'
assert not manifest.exists() and not membership.exists()
names=sorted([p.name for p in root.iterdir() if p.is_file()]+[manifest.name,membership.name])
with membership.open('x') as stream:
    stream.write('\n'.join(names)+'\n')
with manifest.open('x') as stream:
    for name in names:
        if name!=manifest.name:
            stream.write(hashlib.sha256((root/name).read_bytes()).hexdigest()+'  '+name+'\n')
for path in (root/'CLOSURE_FIDELITY.md',manifest):
    print(hashlib.sha256(path.read_bytes()).hexdigest()+'  '+str(path))
print('files='+str(len(names))+' payloads='+str(len(names)-1))
