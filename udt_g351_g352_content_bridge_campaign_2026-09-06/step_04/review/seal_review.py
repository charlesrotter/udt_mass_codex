import hashlib
import pathlib

root=pathlib.Path(__file__).resolve().parent
membership=root/'ARCHIVE_FILES.txt'
manifest=root/'REVIEW_SHA256SUMS'
assert not membership.exists() and not manifest.exists(), 'refuse archive reseal'
names=sorted([p.name for p in root.iterdir() if p.is_file()]+[membership.name,manifest.name])
with membership.open('x') as stream:
    stream.write('\n'.join(names)+'\n')
with manifest.open('x') as stream:
    for name in names:
        if name!=manifest.name:
            stream.write(hashlib.sha256((root/name).read_bytes()).hexdigest()+'  '+name+'\n')
for p in (root/'STAGE_B_ADVERSARIAL_REVIEW.md',root/'REVIEW_VERDICT.json',manifest):
    print(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p))
print('archive_file_count='+str(len(names)))
print('manifest_payload_count='+str(len(names)-1))
