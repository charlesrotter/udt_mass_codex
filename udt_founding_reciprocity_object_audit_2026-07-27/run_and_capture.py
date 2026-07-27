#!/usr/bin/env python3
from __future__ import annotations
import os,subprocess,sys
from pathlib import Path
if len(sys.argv)!=4:raise SystemExit('usage: run_and_capture.py SCRIPT STDOUT STDERR')
root=Path(__file__).resolve().parent.parent;script=Path(sys.argv[1]);out=Path(sys.argv[2]);err=Path(sys.argv[3]);env=dict(os.environ);env.update({'CUDA_VISIBLE_DEVICES':'','PYTHONDONTWRITEBYTECODE':'1'})
r=subprocess.run([sys.executable,str(script)],cwd=root,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
out.write_bytes(r.stdout);err.write_bytes(r.stderr);sys.stdout.buffer.write(r.stdout);sys.stderr.buffer.write(r.stderr);raise SystemExit(r.returncode)
