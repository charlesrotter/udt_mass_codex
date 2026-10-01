"""Bounded final correspondence/coverage check; no new field or ray solve."""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
D = ROOT / 'udt_time_live_production_survey_2026-10-01/diagnosis'
R = D / 'review_math'
FREEZE_HASH = '97cffde48522b68e4b4544d1d7b33a0d198296b73ce22708206d99fde8f751ad'


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def read(path):
    return json.loads(path.read_text())


def main():
    freeze = D / 'FINAL_INTEGRATION_FREEZE.json'
    assert sha(freeze) == FREEZE_HASH, 'COMMON_FREEZE_CHANGED'
    f = read(freeze)
    old = read(D / 'PREVIOUS_REVIEW_RECORD.json')['accepted_sha256']
    accepted = f['accepted_sha256']
    protected = ['udt_native_onshell_timelive_reset_owner_audit_2026-08-10/',
                 'udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/',
                 'udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12/',
                 'udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/']
    assert not any(p.startswith(q) for p in accepted for q in protected)
    assert len(accepted) == 12102 and len(old) == 7707
    assert set(old) <= set(accepted)
    changed = sorted(p for p in old if old[p] != accepted[p])
    assert changed == sorted(f['explicit_changed_previous']) and len(changed) == 7
    total = 0
    for p, expected in accepted.items():
        path = ROOT / p
        assert path.resolve().is_relative_to(ROOT) and path.is_file(), p
        assert sha(path) == expected, ('BOUND_FILE_CHANGED', p)
        total += path.stat().st_size
    candidates = f['banking_candidates']
    assert len(candidates) == len(set(candidates)) == f['banking_candidate_count'] == 4414
    assert set(candidates) <= set(accepted)
    assert not any(Path(p).suffix in ['.npz', '.npy', '.pt', '.lock'] for p in candidates)
    assert sum((ROOT / p).stat().st_size for p in candidates) == f['banking_candidate_bytes']
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    assert head == f['head'] == '464dfa03744fe6e74a615d1e15a9ba0e844d0e26'
    assert subprocess.check_output(['git', 'branch', '--show-current'], cwd=ROOT, text=True).strip() == 'grok'
    for p in ['CURRENT_SCIENTIFIC_PREMISES.tsv', 'CANON.md']:
        assert (ROOT / p).read_bytes() == subprocess.check_output(['git', 'show', 'HEAD:' + p], cwd=ROOT), p
    graph_path = 'development_reconstruction_2026-09-29/DEVELOPMENT_GRAPH.json'
    g = read(ROOT / graph_path)
    previous = json.loads(subprocess.check_output(['git', 'show', 'HEAD:' + graph_path], cwd=ROOT))
    assert g['edges'] == previous['edges'], 'TYPED_EDGES_CHANGED'
    old_nodes = {n['id']: n for n in previous['nodes']}
    new_nodes = {n['id']: n for n in g['nodes']}
    assert set(old_nodes) == set(new_nodes)
    assert all(new_nodes[k] == v for k, v in old_nodes.items() if k not in ['R12T', 'R18'])
    for k in ['R12T', 'R18']:
        assert new_nodes[k]['required_conditions'] == old_nodes[k]['required_conditions']
        assert set(old_nodes[k]['sources']) <= set(new_nodes[k]['sources'])
    assert all(g['sources_sha256'][p] == h for p, h in previous['sources_sha256'].items())
    for p, h in g['sources_sha256'].items():
        if p not in previous['sources_sha256'] or p in accepted:
            assert accepted[p] == h
    for support in g['review_support']:
        if support not in previous['review_support'] or support['path'] in accepted:
            assert accepted[support['path']] == support['sha256']
    assert all(x in g['review_support'] for x in previous['review_support'])
    central = (ROOT / 'UDT_DEVELOPMENT.md').read_text()
    program = (ROOT / 'CURRENT_RESEARCH_PROGRAM.md').read_text()
    excerpt = central.split('<!-- DEVELOPMENT_ORIENTATION_BEGIN -->')[1].split('<!-- DEVELOPMENT_ORIENTATION_END -->')[0]
    generated = program.split('<!-- GENERATED_DEVELOPMENT_BEGIN -->')[1].split('<!-- GENERATED_DEVELOPMENT_END -->')[0]
    assert excerpt == generated, 'ORIENTATION_DRIFT'
    tps = D.parent
    original = read(tps / 'production_analysis/postprocess/MATH_CANDIDATE.json')
    repair = read(R / 'REPAIR_MATH.json')
    orig_pass = {x['dataset'] for x in original['datasets'] if x['status'] == 'PASS'}
    orig_flags = {x['dataset'] for x in original['datasets'] if x['status'] != 'PASS'}
    repaired = {x['dataset'] for x in repair['datasets'] if x['repaired_status'] == 'PASS'}
    assert (len(orig_pass), len(orig_flags), len(repaired)) == (65, 13, 13)
    assert repaired == orig_flags and len(orig_pass | repaired) == 78
    assert original['selected_cases'] == 234 and not original['missing_cases']
    assert all(s == 'PASS' for x in original['datasets'] for s in x['original_equations'].values())
    assert repair['selected_cases'] == 26 and repair['original_equations_pass']
    for x in repair['datasets']:
        assert x['original_status'] == 'DIAGNOSTIC_NOT_QUALIFIED'
        assert max(x['final_time_refinement'].values()) <= 2e-7
        for s in x['spatial']:
            assert s['ratio'] >= 10 or s['all_points_both_meshes_max'] < 1e-8
            assert (s['ratio'] >= 10) == (x['dataset'] != 'axial_a5')
    o = read(R / 'ORIGINAL_CLOCK_RESULT_REVIEW.json')
    c = read(R / 'REFINED_CLOCK_RESULT_REVIEW.json')
    a = read(R / 'ATLAS_RESULT_REVIEW.json')
    assert (o['cases'], o['rays'], o['matched_pairs'], o['independent_cases']) == (234, 936, 156, 30)
    assert (c['history_count'], c['new_histories'], c['anchor_histories'], c['pair_comparisons']) == (39, 26, 13, 26)
    assert (a['actual_rows'], a['actual_clock_histories']) == (364, 260)
    assert o['candidate_sha256'] == sha(D / 'clock_completion/CLOCK_CANDIDATE.json')
    assert c['candidate_sha256'] == sha(D / 'refined_clock_completion/REFINED_CLOCK_CANDIDATE.json')
    assert c['field_math_sha256'] == sha(R / 'REPAIR_MATH.json')
    assert a['atlas_sha256'] == sha(D / 'atlas/ATLAS.json')
    assert a['CSV_sha256'] == sha(D / 'atlas/clock_atlas.csv')
    assert read(R / 'ATLAS_VISUAL_REVIEW.json')['status'] == 'ACTUAL_ATLAS_VISUAL_REVIEW_PASS'
    result = dict(status='FINAL_INTEGRATION_CORRESPONDENCE_PASS',
                  reviewer_context='/root/survey_completion_math', head=head,
                  freeze_sha256=FREEZE_HASH, accepted_files_checked=len(accepted),
                  accepted_bytes_checked=total, preserved_previous=7700,
                  changed_previous=changed, banking_candidates=len(candidates),
                  protected_paths_touched=0, unchanged_typed_edges=len(g['edges']),
                  old_source_pins_preserved=len(previous['sources_sha256']),
                  new_review_support=len(g['review_support']) - len(previous['review_support']),
                  original_dataset_pass=65, original_dataset_flags=13,
                  repaired_dataset_pass=13, qualified_tested_dataset_union=78,
                  checks='All common bound bytes, old-map preservation, unchanged conditions/edges, new graph and review support pins plus existing direct-map pins, generated orientation, original/refined disjoint qualification union, actual prior result-report joins.',
                  limits='Correspondence and finite scalar integration check, alongside substantive source reading and earlier independent saved-field work; not all-history re-evolution, historical reproof, scientific adoption or final parent repository gates.')
    with (R / 'FINAL_INTEGRATION_CHECK.json').open('x') as out:
        json.dump(result, out, indent=2)
        out.write('\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
