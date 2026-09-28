"""Packaging correspondence only; no scientific calculation or git mutation."""
import datetime, hashlib, json, pathlib, re, subprocess
root=pathlib.Path.cwd();p=root/'udt_common_geometry_whiteboard_2026-09-28';out=p/'review'
sha=lambda b:hashlib.sha256(b).hexdigest()
manifest=json.loads((p/'CONSTRUCTION_MANIFEST.json').read_text())
construction=[]
for name,record in manifest['files'].items():
    data=(p/name).read_bytes()
    if sha(data)!=record['sha256'] or len(data)!=record['bytes']:construction.append(name)
original_review=[];review_entries=0
for line in (out/'REVIEW_MANIFEST.sha256').read_text().splitlines():
    digest,name=line.split('  ',1);review_entries+=1
    if sha((root/name).read_bytes())!=digest:original_review.append(name)
seal=json.loads((out/'SOURCE_FIRST_SEAL.json').read_text())
seal_bad=[name for name,digest in seal['files'].items() if sha((out/name).read_bytes())!=digest]
launch=json.loads((p/'LAUNCH.json').read_text())
authority={name:{'sha256':sha((root/name).read_bytes()),'unchanged':sha((root/name).read_bytes())==launch['source_sha256'][name]} for name in ['AGENTS.md','CLAUDE.md','CANON.md','founding.md','CURRENT_SCIENTIFIC_PREMISES.md','CURRENT_SCIENTIFIC_PREMISES.tsv','verify_current_scientific_premises.py']}

# Apply only the saved zero-context text hunks in memory to git-show base bytes.
# This independently reproduces the parent's scratch result without writing a tree.
snapshot=json.loads((p/'STATUS_AT_CONSTRUCTION.json').read_text())
patch=(p/'STATUS_AT_CONSTRUCTION.patch').read_text()
if sha(patch.encode())!=snapshot['patch_sha256']:raise RuntimeError('patch hash')
reconstructed={};reconstruction={}
for section in patch.split('diff --git ')[1:]:
    lines=section.splitlines(keepends=True)
    name=lines[0].split()[0][2:]
    if name not in snapshot['files_sha256']:raise RuntimeError(('unexpected patch path',name))
    old=subprocess.check_output(['git','show',snapshot['base']+':'+name]).decode().splitlines(keepends=True)
    cursor=0;result=[];i=1
    while i<len(lines):
        if not lines[i].startswith('@@ '):i+=1;continue
        match=re.match(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@',lines[i])
        start=int(match[1]);count=int(match[2] or 1);newcount=int(match[4] or 1)
        pos=start if count==0 else start-1
        removed=[];added=[];i+=1
        while i<len(lines) and not lines[i].startswith('@@ '):
            line=lines[i]
            if line.startswith('-'):removed.append(line[1:])
            elif line.startswith('+'):added.append(line[1:])
            else:raise RuntimeError(('unexpected nonzero context',line))
            i+=1
        if len(removed)!=count or len(added)!=newcount or old[pos:pos+count]!=removed:raise RuntimeError(('hunk mismatch',name,pos))
        result.extend(old[cursor:pos]);result.extend(added);cursor=pos+count
    result.extend(old[cursor:]);data=''.join(result).encode();reconstructed[name]=data
    reconstruction[name]={'sha256':sha(data),'matches_snapshot':sha(data)==snapshot['files_sha256'][name]}
if set(reconstructed)!=set(snapshot['files_sha256']):raise RuntimeError('snapshot coverage')

source_bad=[];source_count=0;recovered_source_versions=[]
for pins in ['SOURCE_FIRST_PINS.sha256','ADDITIONAL_SOURCE_PINS.sha256']:
    for line in (out/pins).read_text().splitlines():
        digest,name=line.split('  ',1);source_count+=1
        if name in reconstructed:
            data=reconstructed[name];recovered_source_versions.append(name)
        elif name=='udt_common_geometry_whiteboard_2026-09-28/WORK_ORDER.md':
            data=(p/'AUTHORIZED_WORK_ORDER.md').read_bytes();recovered_source_versions.append(name)
        else:data=(root/name).read_bytes()
        if sha(data)!=digest:source_bad.append(name)
initial=set(launch['preexisting_untracked_paths'])
untracked=set(subprocess.check_output(['git','ls-files','--others','--exclude-standard'],text=True).splitlines())
staged=set(subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines())
missing=sorted(initial-untracked);staged_old=sorted(initial&staged)
targets=['LIVE.md','HANDOFF.md','CURRENT_RESEARCH_PROGRAM.md','UDT_RESEARCH_ROADMAP.md','INDEX.md','MEMORY.md']
targets+=['udt_common_geometry_whiteboard_2026-09-28/'+s for s in ['DECISION_BRIEF.md','REVIEWED_RESULT.md','CLOSEOUT.md','WORK_ORDER.md','REVIEW_RUNTIME.json','STATUS_AT_CONSTRUCTION.json','STATUS_AT_CONSTRUCTION.patch']]
pins={name:sha((root/name).read_bytes()) for name in targets}
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'branch':subprocess.check_output(['git','branch','--show-current'],text=True).strip(),'construction_entries':len(manifest['files']),'construction_mismatches':construction,'original_review_entries':review_entries,'original_review_mismatches':original_review,'source_first_seal_mismatches':seal_bad,'authority':authority,'active_snapshot_reconstruction':reconstruction,'pinned_source_entries':source_count,'pinned_source_mismatches':source_bad,'reconstructed_source_versions':sorted(set(recovered_source_versions)),'preexisting_name_count':len(initial),'missing_preexisting_untracked_names':missing,'staged_preexisting_names':staged_old,'reviewed_document_sha256':pins,'scope':'Correspondence and filename preservation only; no protected payload opened and no science/audit rerun'}
print(json.dumps(record,indent=2))
if construction or original_review or seal_bad or source_bad or missing or staged_old or not all(r['unchanged'] for r in authority.values()) or not all(r['matches_snapshot'] for r in reconstruction.values()):raise RuntimeError('final correspondence failed')
