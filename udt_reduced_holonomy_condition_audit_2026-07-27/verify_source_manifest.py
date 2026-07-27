#!/usr/bin/env python3
from __future__ import annotations
import csv,hashlib,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
def main():
    rows=list(csv.DictReader((HERE/'SOURCE_MANIFEST.tsv').open(newline='',encoding='utf-8'),delimiter='\t'));assert len(rows)==14
    for row in rows:
        path=ROOT/row['path'];assert hashlib.sha256(path.read_bytes()).hexdigest()==row['sha256'];assert subprocess.check_output(['git','rev-parse',f"HEAD:{row['path']}"],cwd=ROOT,text=True).strip()==row['git_blob']
    print('PASS source manifest 14/14');return 0
if __name__=='__main__':raise SystemExit(main())
