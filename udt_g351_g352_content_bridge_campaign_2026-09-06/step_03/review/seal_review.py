"""One-time evidence membership/hash seal; never overwrites an existing seal."""
import argparse, hashlib, json, pathlib
p=argparse.ArgumentParser();p.add_argument('--directory',type=pathlib.Path,required=True)
a=p.parse_args(); d=a.directory.resolve()
listing=d/'ARCHIVE_FILES.txt'; manifest=d/'REVIEW_SHA256SUMS'
if listing.exists() or manifest.exists():raise SystemExit('Refusing to overwrite an existing seal')
paths=sorted(z.relative_to(d).as_posix() for z in d.rglob('*') if z.is_file())
if any(z.is_symlink() for z in d.rglob('*')):raise SystemExit('Symlinks are excluded from this seal')
paths=sorted(paths+['ARCHIVE_FILES.txt','REVIEW_SHA256SUMS'])
with listing.open('x') as f:f.write('\n'.join(paths)+'\n')
payloads=[z for z in paths if z!='REVIEW_SHA256SUMS']
with manifest.open('x') as f:
    for name in payloads:f.write(hashlib.sha256((d/name).read_bytes()).hexdigest()+'  '+name+'\n')
print(json.dumps({'files':len(paths),'payloads':len(payloads),
 'report_sha256':hashlib.sha256((d/'STAGE_B_ADVERSARIAL_REVIEW.md').read_bytes()).hexdigest(),
 'manifest_sha256':hashlib.sha256(manifest.read_bytes()).hexdigest()},indent=2))
