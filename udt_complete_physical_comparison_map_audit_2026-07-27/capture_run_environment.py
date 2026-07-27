#!/usr/bin/env python3
from __future__ import annotations
import json,platform
import numpy,sympy
from pathlib import Path
HERE=Path(__file__).resolve().parent
out={'cpu_only':True,'CUDA_VISIBLE_DEVICES':'','python':platform.python_version(),'platform':platform.platform(),'numpy':numpy.__version__,'sympy':sympy.__version__,'dtype':'exact_symbolic_and_rational','production_command':'PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES= python3 udt_complete_physical_comparison_map_audit_2026-07-27/derive_comparison_map.py','independent_command':'PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES= python3 udt_complete_physical_comparison_map_audit_2026-07-27/verify_comparison_map_independent.py','fresh_review_agent':'comparison_map_adversary'}
(HERE/'RUN_ENVIRONMENT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
