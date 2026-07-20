#!/usr/bin/env python3
import hashlib
from pathlib import Path
H=Path(__file__).resolve().parent;X={"SHA256SUMS.txt","REPOSITORY_GATES.json"};M=H/"SHA256SUMS.txt";E=[x.split("  ",1) for x in M.read_text().splitlines() if x];N=[n for _,n in E];A=sorted(p.name for p in H.iterdir() if p.is_file() and p.name not in X)
if N!=A or len(N)!=len(set(N)):raise AssertionError("coverage")
for d,n in E:
 if hashlib.sha256((H/n).read_bytes()).hexdigest()!=d:raise AssertionError(n)
print(f"PASS entries={len(E)} manifest_sha256={hashlib.sha256(M.read_bytes()).hexdigest()}")
