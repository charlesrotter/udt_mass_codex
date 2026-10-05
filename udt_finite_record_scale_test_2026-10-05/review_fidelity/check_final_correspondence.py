"""Exact-byte correspondence after actual scoped final semantic review."""
from pathlib import Path
import datetime,hashlib,json,sys,subprocess
PKG=Path('udt_finite_record_scale_test_2026-10-05');OUT=PKG/'review_fidelity'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
freeze=PKG/'INTEGRATION_FREEZE.json'
assert len(sys.argv)==2 and sha(freeze)==sys.argv[1], 'FREEZE_CHANGED'
d=json.loads(freeze.read_text());accepted=d['accepted_sha256']
forbidden=['udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/','udt_native_onshell_timelive_reset_owner_audit_2026-08-10/','udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/','udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12/']
assert not any(k.startswith(tuple(forbidden)) for k in accepted),'PROTECTED_PATH_IN_MAP'
bad=[k for k,v in accepted.items() if not Path(k).is_file() or sha(k)!=v]
assert not bad,bad
assert sha(freeze)==sys.argv[1], 'FREEZE_CHANGED_DURING_READ'
graph=json.loads(Path('development_reconstruction_2026-09-29/DEVELOPMENT_GRAPH.json').read_text())
nodes={n['id']:n for n in graph['nodes']}
assert set(nodes['R16FRI']['required_conditions'])=={'C_FRI_SHAPE','C_FRI_RECORD'}
assert nodes['O_FRI_ADMISSION']['kind']=='open_join'
assert any(e['from']=='O_FRI_ADMISSION' and e['to']=='R16FRI' and e['kind']=='open_boundary' for e in graph['edges'])
assert subprocess.check_output(['git','rev-parse','--abbrev-ref','HEAD'],text=True).strip()=='grok'
report=dict(status='PASS',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),integration_freeze_sha256=sys.argv[1],accepted_file_count=len(accepted),bad_paths=bad,protected_paths_in_map=0,branch='grok',actual_head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),changed_inherited=d['changed_inherited'],scope='Exact correspondence of authorized map, declared conditional/open graph structure; substantive semantics reviewed separately in FINAL_REVIEW.md. No protected payload read, numerical rerun or premise-grade change.',total_independent_incidence_cases=56,script_sha256=sha(__file__))
(OUT/'FINAL_CORRESPONDENCE.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
