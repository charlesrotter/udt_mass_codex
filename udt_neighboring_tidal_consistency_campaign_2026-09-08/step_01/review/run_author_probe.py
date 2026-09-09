"""Execute an actual isolated author-source corruption without editing the author file."""
import hashlib
import json
from pathlib import Path
import sys

path=Path(__file__).resolve().parents[1]/'check_nt1.py'
source=path.read_text()
probe=sys.argv[1]
replacements={
    'scaled_action':('return {idx:sum(A[r][idx[s]]*q[idx[:s]+(r,)+idx[s+1:]]',
                     'return {idx:F(2)*sum(A[r][idx[s]]*q[idx[:s]+(r,)+idx[s+1:]]'),
    'zero_kernel':('    kernel.append(v)','    kernel.append([F(0)]*40)'),
}
old,new=replacements[probe]
assert source.count(old)==1
modified=source.replace(old,new)
print(json.dumps(dict(probe=probe,source=str(path),source_sha256=hashlib.sha256(source.encode()).hexdigest(),
    old=old,new=new,modified_sha256=hashlib.sha256(modified.encode()).hexdigest(),
    classification='actual implementation corruption, author original unchanged')),flush=True)
sys.argv=[str(path)]
exec(compile(modified,str(path),'exec'),{'__file__':str(path),'__name__':'__main__'})
