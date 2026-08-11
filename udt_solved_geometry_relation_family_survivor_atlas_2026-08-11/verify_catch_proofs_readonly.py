#!/usr/bin/env python3
"""Read-only replay of all 23 catch-proof predicates; writes no evidence."""

from __future__ import annotations

import ast
import csv
import hashlib
import json
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
PROTECTED = "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/"
STOPPED = "udt_native_onshell_timelive_reset_owner_audit_2026-08-10/"


def rows(name): return list(csv.DictReader((HERE/name).open(), delimiter="\t"))
def universe(v):
    ids=[r['sample_id'] for r in v]
    return len(ids)==14 and len(set(ids))==14 and sum(r['geometry']=='R17_GLOBAL' for r in v)==9 and sum(r['geometry']=='TIMELIVE_LOCAL' for r in v)==5


s=rows('NUMERICAL_SAMPLE_UNIVERSE.tsv'); a=rows('SOLVED_GEOMETRY_ATLAS.tsv'); g=rows('GEODESIC_DIAGNOSTICS.tsv'); p=rows('PATH_DIAGNOSTICS.tsv')
i=json.loads((HERE/'INDEPENDENT_VERIFICATION.json').read_text()); d=json.loads((HERE/'DERIVATION_RESULT.json').read_text()); m=rows('SOURCE_MANIFEST.tsv')
pt=(HERE/'solve_survivor_atlas.py').read_text(); it=(HERE/'verify_survivor_atlas_independent.py').read_text()
checks=[]
def C(x): checks.append(bool(x))
C(universe(s)); C(not universe(s[:-1])); C(not universe(s+[s[0]])); C((len(a),len(g),len(p))==(14,28,28))
C({r['sample_id'] for r in s}=={r['sample_id'] for r in a} and all(sum(x['sample_id']==r['sample_id'] for x in g+p)==4 for r in s))
C({r['parameter_2'] for r in s if r['geometry']=='R17_GLOBAL'}=={'epsilon=-0.12','epsilon=0','epsilon=+0.12'} and {r['parameter_1'] for r in s if r['geometry']=='TIMELIVE_LOCAL'}=={'epsilon=-0.15','epsilon=-0.075','epsilon=0','epsilon=+0.075','epsilon=+0.15'})
C(max(float(r['endpoint_atlas_defect']) for r in a)<=5e-10); C(max(float(r['r17_phi_identity_defect']) for r in a if r['r17_phi_identity_defect']!='NA')<=5e-10)
C(max(float(r['norm_drift']) for r in g)<=5e-8 and max(float(r['transport_metric_defect']) for r in g)<=5e-8)
C(all(r['classification'] in {'REGULAR_PROPAGATOR','NEAR_CONJUGATE_OR_NUMERICALLY_UNRESOLVED','NUMERIC_UNRESOLVED'} for r in g) and min(float(r['dexp_min_singular']) for r in g)>1e-5)
C(max(float(r['lc_metric_defect']) for r in p)<=5e-8); C(all(float(r['lc_holonomy_norm'])>1e-5 and r['classification']=='NONIDENTITY' for r in p))
C(i['status']=='PASS' and i['checks']==i['pass_count']==56)
mods={n.module for n in ast.walk(ast.parse(it)) if isinstance(n,(ast.Import,ast.ImportFrom)) and getattr(n,'module',None)}; C('solve_survivor_atlas' not in mods)
C(all(hashlib.sha256((HERE/n).read_bytes()).hexdigest()==h for n,h in i['production_hashes'].items()))
C(all(not r['path'].startswith(PROTECTED) and not r['path'].startswith(STOPPED) for r in m)); C(PROTECTED not in pt+it and STOPPED not in pt+it)
C(all(x not in pt for x in ('c_E','X_max','rho_tot','bootstrap_density','matter_action')))
C(all(np.linalg.norm(np.array([float(x) for x in r['endpoint_x'].split(';')])-np.array([.12,-.18,.23,-.14]))>1e-3 for r in g if r['sample_id'].startswith('TL_')))
rng=np.random.default_rng(20260811); L=[np.eye(4)+.03*(x-x.T) for x in [rng.normal(size=(4,4)) for _ in range(3)]]; apq=np.diag([1.1,.9,1.02,.98]); aqr=np.diag([.95,1.04,.99,1.03]); apr=aqr@apq
C(np.linalg.norm((L[2]@aqr@np.linalg.inv(L[1]))@(L[1]@apq@np.linalg.inv(L[0]))-L[2]@apr@np.linalg.inv(L[0]))<1e-12)
least=min(p,key=lambda r:float(r['lc_holonomy_norm'])); P=np.array([float(x) for x in least['holonomy_matrix'].split(';')]).reshape(4,4); M=np.eye(4)+.02*rng.normal(size=(4,4)); Q=M@P@np.linalg.inv(M)
C(np.linalg.norm(P-np.eye(4))>1e-5 and np.linalg.norm(Q-np.eye(4))>1e-5); C(d['scope']=='bounded_metric_geometry_not_physical_stability')
prose=' '.join((HERE/n).read_text() for n in ('PREREGISTRATION.md','PONDER_MAP.md','SOLVER_COMPLETENESS_MAP.md','NUMERICAL_CONTRACT.md')); C(not any(x in prose.lower() for x in ('physically stable','dynamically stable','the selected physical relation','unique physical branch')))
stored=rows('CATCH_PROOF_RESULTS.tsv'); summary=json.loads((HERE/'CATCH_PROOF_RESULT.json').read_text())
assert len(checks)==23 and all(checks); assert len(stored)==23 and all(r['status']=='PASS' for r in stored); assert summary['status']=='PASS' and summary['tests']==summary['passed']==23
print(json.dumps({'status':'PASS','predicates_reexecuted_readonly':23,'stored_rows_verified':23}, indent=2, sort_keys=True))
