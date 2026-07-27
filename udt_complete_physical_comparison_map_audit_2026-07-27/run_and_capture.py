#!/usr/bin/env python3
from __future__ import annotations
import os,subprocess,sys
from pathlib import Path
if len(sys.argv)!=4:raise SystemExit('usage: run_and_capture.py SCRIPT STDOUT STDERR')
root=Path(__file__).resolve().parent.parent;env=dict(os.environ);env.update({'CUDA_VISIBLE_DEVICES':'','PYTHONDONTWRITEBYTECODE':'1'});r=subprocess.run([sys.executable,sys.argv[1]],cwd=root,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE);Path(sys.argv[2]).write_bytes(r.stdout);Path(sys.argv[3]).write_bytes(r.stderr);sys.stdout.buffer.write(r.stdout);sys.stderr.buffer.write(r.stderr);raise SystemExit(r.returncode)
