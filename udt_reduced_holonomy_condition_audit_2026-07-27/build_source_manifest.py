#!/usr/bin/env python3
from __future__ import annotations
import csv,hashlib,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
def main():
    rows=list(csv.DictReader((HERE/'SOURCE_SCOPE.tsv').open(newline='',encoding='utf-8'),delimiter='\t'));assert len(rows)==14 and len({r['path'] for r in rows})==14
    out=['path\tgit_blob\tsha256\trole']
    for row in rows:
        path=ROOT/row['path'];assert path.is_file();blob=subprocess.check_output(['git','rev-parse',f"HEAD:{row['path']}"],cwd=ROOT,text=True).strip();out.append(f"{row['path']}\t{blob}\t{hashlib.sha256(path.read_bytes()).hexdigest()}\t{row['role']}")
    (HERE/'SOURCE_MANIFEST.tsv').write_text('\n'.join(out)+'\n');print('PASS source manifest 14');return 0
if __name__=='__main__':raise SystemExit(main())
