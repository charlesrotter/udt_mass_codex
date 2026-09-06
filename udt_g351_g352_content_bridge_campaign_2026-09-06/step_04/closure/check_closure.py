"""Pinned Step 4/aggregate documentation/archive correspondence; stdout only."""
import argparse
import hashlib
import json
import pathlib
import subprocess

p=argparse.ArgumentParser()
p.add_argument('--repo',type=pathlib.Path,required=True)
p.add_argument('--sealed',type=pathlib.Path,required=True)
a=p.parse_args()
repo=a.repo.resolve()
sealed=a.sealed.resolve()
pin='2eb8299292b45fb3987bbd48fd95e2e254549e86'
package='udt_g351_g352_content_bridge_campaign_2026-09-06/'
prefix=package+'step_04/review/'
commands=[]
sha=lambda data:hashlib.sha256(data).hexdigest()

def git(*args):
    cmd=['git','-c','core.packedGitWindowSize=1m','-c','core.packedGitLimit=64m',
         '-c','core.preloadindex=false','-c','index.threads=1',*args]
    r=subprocess.run(cmd,cwd=repo,capture_output=True,timeout=30)
    commands.append(dict(command=cmd,returncode=r.returncode,stderr=r.stderr.decode(),
                         stdout_sha256=sha(r.stdout),stdout_bytes=len(r.stdout)))
    assert r.returncode==0,(cmd,r.returncode,r.stderr)
    return r.stdout

docs={
 'DECISION_BRIEF.md':'698038549df858d577e27bb37c008f51f100a9292a3062f1355f7a09740a8361',
 'CAMPAIGN_LOG.md':'76cb06917d67a4502cfee87fbd667212f17ff263039fe5841c79abf7f640b5f1',
 'step_04/REVIEW_RECORD.md':'e89cf5131c7abfc26a2a25aa4c84e4a0919ce50ceae8ba2d3005fdf6d85d7b88',
}
for rel,digest in docs.items():
    pinned=git('show',pin+':'+package+rel)
    assert sha(pinned)==digest and pinned==(repo/package/rel).read_bytes(),rel

names=(sealed/'ARCHIVE_FILES.txt').read_text().splitlines()
assert names==sorted(set(names)) and len(names)==68
for directory in (sealed,repo/prefix):
    actual=sorted(z.relative_to(directory).as_posix() for z in directory.rglob('*') if z.is_file())
    assert actual==names,('membership',str(directory))
pinned_names=[z.decode()[len(prefix):] for z in git('ls-tree','-r','-z','--name-only',pin,'--',prefix).split(b'\0') if z]
assert pinned_names==names
manifest=(sealed/'REVIEW_SHA256SUMS').read_bytes()
assert sha(manifest)=='77317b537a196cb6165ed2c491a73a3f2dd0354a1c6f16f76373b0f47bc32178'
assert len(manifest.decode().splitlines())==67
for line in manifest.decode().splitlines():
    digest,name=line.split('  ',1)
    assert sha((sealed/name).read_bytes())==digest,name
rows=[]
for name in names:
    original=(sealed/name).read_bytes()
    copied=(repo/prefix/name).read_bytes()
    pinned=git('show',pin+':'+prefix+name)
    assert original==copied==pinned,name
    rows.append(dict(name=name,sha256=sha(original),bytes=len(original),
                     sealed_copy_pinned_identical=True))

# Authenticate sources/frozen candidates by their saved manifests, not replay.
manifest_rows=[]
for step in range(1,5):
    for filename in ('SOURCE_SHA256SUMS','FROZEN_CANDIDATE_SHA256SUMS'):
        relative=package+f'step_{step:02d}/'+filename
        payload=(repo/relative).read_bytes()
        assert git('show',pin+':'+relative)==payload,relative
        lines=payload.decode().splitlines()
        for line in lines:
            digest,path=line.split('  ',1)
            assert sha((repo/path).read_bytes())==digest,path
        manifest_rows.append(dict(path=relative,sha256=sha(payload),payloads=len(lines),pass_hashes=True))

status=git('status','--porcelain=v1','--untracked-files=normal').decode()
old_status=(sealed/'final_repository_status_serial.stdout').read_text()
unrelated=lambda text:sorted(line for line in text.splitlines()
                             if line.startswith('?? ') and not line[3:].startswith(package))
assert unrelated(status)==unrelated(old_status) and len(unrelated(status))==46
outside=git('diff','--name-only','c19b5fb147d6afbfd91ec248b0693dfc834ce220',
            '--','.',':(exclude)'+package.rstrip('/'))
assert outside==b'',outside
head=git('rev-parse','HEAD').decode().strip()
print(json.dumps(dict(status='PASS_DOCUMENTATION_ARCHIVE_CORRESPONDENCE',
                     scope='Step 4 and aggregate documentation closure; no new mathematical review',
                     pin=pin,actual_head=head,documentation_sha256=docs,
                     archive_files=68,manifest_payloads=67,
                     exact_membership_and_bytes=True,archive_rows=rows,
                     source_frozen_manifest_checks=manifest_rows,
                     current_status=status,unrelated_status_entries_preserved=46,
                     out_of_scope_tracked_diff=outside.decode(),commands=commands),indent=2))
