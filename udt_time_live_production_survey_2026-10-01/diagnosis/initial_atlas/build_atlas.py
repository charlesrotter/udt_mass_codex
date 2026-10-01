"""Descriptive, outcome-exposed atlas of existing qualified/diagnostic readouts."""
import csv
import hashlib
import json
import math
from pathlib import Path
import re

D = Path(__file__).resolve().parent
B = D.parent
ROOT = B.parent
OUT = D / 'atlas'

def read(p):
    return json.loads(Path(p).read_text())

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def require(ok, message):
    if not ok:
        raise ValueError(message)

def build_rows():
    paths = [B/'production_analysis/postprocess/MATH_CANDIDATE.json',
             D/'clock_completion/CLOCK_CANDIDATE.json',
             D/'review_math/REPAIR_MATH.json',
             D/'refined_clock_completion/REFINED_CLOCK_CANDIDATE.json',
             B/'production_runtime/case_grid.json', D/'REPAIR_CASES.json',
             D/'ATLAS_PLAN.md', Path(__file__), B/'CLOCK_DISPATCH.json',
             B/'launch_evidence/case_grid.json']
    original, clocks, repaired, newclocks, grid, mapping = map(read, paths[:6])
    require(original['checked_cases'] == 234 and len(original['datasets']) == 78,
            'ORIGINAL_COVERAGE')
    require(repaired['selected_cases'] == 26 and len(repaired['datasets']) == 13,
            'REPAIR_COVERAGE')
    require(clocks['cases'] == 234 and clocks['independent_cases'] == 30,
            'ORIGINAL_CLOCK_COVERAGE')
    require(len(newclocks['datasets']) == 13 and len(newclocks['refined_output_sha256']) == 26,
            'REFINED_CLOCK_COVERAGE')
    bindings = {str(p.relative_to(ROOT)): sha(p) for p in paths}
    require(grid == read(B/'launch_evidence/case_grid.json'), 'FIXED_GRID_CHANGED')
    threshold = read(B/'CLOCK_DISPATCH.json')['matched_logZ_threshold']
    require(threshold == 2e-7, 'UNCHANGED_CLOCK_THRESHOLD')
    records = {}
    for p, h in clocks['source_sha256'].items():
        require(sha(ROOT/p) == h, 'ORIGINAL_CLOCK_CHANGED')
        bindings[p] = h
        records[Path(p).parent.name] = read(ROOT/p)
    for name, h in newclocks['refined_output_sha256'].items():
        p = D/'refined_clock_completion'/name/'clock.json'
        require(sha(p) == h, 'REFINED_CLOCK_CHANGED')
        bindings[str(p.relative_to(ROOT))] = h
        records[name] = read(p)
    require(len(records) == 260, 'ALL_CLOCK_HISTORIES')
    for name, h in newclocks['original_anchor_sha256'].items():
        require(sha(B/'production_analysis'/name/'clock.json') == h, 'ANCHOR_CHANGED')
    old = {x['dataset']: x for x in original['datasets']}
    new = {x['dataset']: x for x in repaired['datasets']}
    require(set(new) == {x['dataset'] for x in mapping['datasets']}, 'REPAIR_DATASET_JOIN')
    require(sum(x['status'] == 'PASS' for x in old.values()) == 65, 'ORIGINAL_65_13_CHANGED')
    require(all(old[k]['status'] != 'PASS' for k in new), 'REPAIR_REPLACES_QUALIFIED_DATASET')
    rows = []
    for edition, names in [('original', list(old)), ('refined', list(new))]:
        for name in names:
            match = re.fullmatch(r'(axial|oblique)_a([0-5])(?:_p([0-3])_r([0-2]))?', name)
            require(match is not None, 'DATASET_ID')
            family, ai, pi, ri = match.groups()
            require((family == 'axial') == (pi is None and ri is None), 'RECIPE_ID')
            amplitude = grid['amplitudes'][int(ai)]
            suffixes = ['_n24', '_n24_half', '_n32'] if edition == 'original' else ['_n24_half', '_n24_quarter', '_n32_half']
            cases = [name + s for s in suffixes]
            require(all(len(records[c]['readouts']) == 4 for c in cases), 'RAY_COUNT')
            field = old[name]['status'] if edition == 'original' else new[name]['repaired_status']
            for index, direction in enumerate(['x', 'y', 'z', 'diagonal']):
                rays = [records[c]['readouts'][index] for c in cases]
                for ray in rays[1:]:
                    for key in ['te', 'to', 'emitter_position', 'initial_coordinate_direction']:
                        require(ray[key] == rays[0][key], 'UNMATCHED_QUERY')
                vals = [r['logZ'] for r in rays]
                require(all(math.isfinite(x) for x in vals), 'NONFINITE_READOUT')
                for r in rays:
                    require(r['Z'] > 0 and math.isclose(math.log(r['Z']), r['logZ'], abs_tol=2e-15), 'Z_CONVENTION')
                delta = max(abs(vals[0]-v) for v in vals[1:])
                signs = ['redshift' if v > 0 else 'blueshift' if v < 0 else 'zero' for v in vals]
                rows.append(dict(edition=edition, dataset=name, family=family,
                    amplitude_multiplier=amplitude, phase_offset=None if pi is None else grid['fourth_oblique_phase_offsets'][int(pi)],
                    polarization_degrees=None if ri is None else grid['polarization_angles_degrees'][int(ri)],
                    direction=direction, original_field_status=old[name]['status'],
                    field_status_this_edition=field, baseline_case=cases[0], temporal_case=cases[1], spatial_case=cases[2],
                    baseline_logZ=vals[0], temporal_logZ=vals[1], spatial_logZ=vals[2],
                    max_logZ_difference=delta, clock_comparison='PASS' if delta < threshold else 'FAIL',
                    spatial_Z=rays[2]['Z'], spatial_sign=signs[2], all_three_signs_agree=len(set(signs)) == 1))
    require(len(rows) == 364, 'ATLAS_ROW_COVERAGE')
    # Independently reconstruct every aggregate maximum from the plotted triples.
    for edition, reports in [('original', clocks['matched']), ('refined', [x for d in newclocks['datasets'] for x in d['matched']])]:
        for report in reports:
            a, c = report['reference'], report['other']
            delta = max(abs(x['logZ']-y['logZ']) for x,y in zip(records[a]['readouts'], records[c]['readouts'], strict=True))
            require(delta == report['max_logZ_difference'], 'CLOCK_AGGREGATE_MISMATCH')
            require(report['diagnostic'] == ('PASS' if delta < threshold else 'FAIL'), 'CLOCK_STATUS_MISMATCH')
    stats = {}
    for edition in ['original', 'refined']:
        selected = [x for x in rows if x['edition'] == edition]
        stats[edition] = dict(datasets=len(selected)//4,
            qualified_datasets=len({r['dataset'] for r in selected if r['field_status_this_edition'] == 'PASS'}),
            maximum_matched_logZ_difference=max(r['max_logZ_difference'] for r in selected),
            directions={k: dict(min_logZ=min(r['spatial_logZ'] for r in selected if r['direction']==k),
                max_logZ=max(r['spatial_logZ'] for r in selected if r['direction']==k),
                signs={s:sum(r['spatial_sign']==s for r in selected if r['direction']==k) for s in ['redshift','blueshift','zero']})
                for k in ['x','y','z','diagonal']})
    stats['independent_original_subset'] = dict(cases=len(clocks['independent_comparisons']),
        maximum_logZ_difference=max(x['max_logZ_difference'] for x in clocks['independent_comparisons']),
        maximum_endpoint_difference=max(x['max_endpoint_difference'] for x in clocks['independent_comparisons']))
    return rows, bindings, stats

def plot(rows):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    fig, axes = plt.subplots(2, 2, figsize=(11, 8), sharex=True)
    for ax, direction in zip(axes.flat, ['x','y','z','diagonal'], strict=True):
        chosen = [r for r in rows if r['direction'] == direction]
        old = [r for r in chosen if r['edition'] == 'original']
        recipes = sorted({(r['family'], str(r['phase_offset']), str(r['polarization_degrees'])) for r in old})
        for recipe in recipes:
            group = sorted([r for r in old if (r['family'],str(r['phase_offset']),str(r['polarization_degrees'])) == recipe], key=lambda r:r['amplitude_multiplier'])
            ax.plot([r['amplitude_multiplier'] for r in group], [1000*r['spatial_logZ'] for r in group],
                    color='#263745' if recipe[0]=='axial' else '#91a8b5', linewidth=1.7 if recipe[0]=='axial' else .65, alpha=.8)
        for r in chosen:
            qualified = r['field_status_this_edition'] == 'PASS'
            refined = r['edition'] == 'refined'
            color = '#137955' if refined else '#24658b' if qualified else '#b96413'
            ax.scatter(r['amplitude_multiplier'], 1000*r['spatial_logZ'], s=70 if refined else 22,
                       marker='*' if refined else 'o', facecolor=color if qualified else 'none', edgecolor=color, linewidth=.9, zorder=4 if refined else 3)
            if r['clock_comparison'] != 'PASS':
                ax.scatter(r['amplitude_multiplier'],1000*r['spatial_logZ'],s=45,marker='x',color='#b32020',zorder=5)
        ax.set_title(direction+' initial ray direction')
        ax.set_ylabel('1000 × log Z')
        ax.grid(alpha=.2)
        ax.ticklabel_format(axis='y', style='plain', useOffset=False)
        ax.set_xticks([.25,.5,1,1.5,2,3])
        ax.set_xlabel('Supplied initial amplitude multiplier')
    handles = [Line2D([],[],marker='o',linestyle='none',color='#24658b',label='Original, field gates pass'),
               Line2D([],[],marker='o',linestyle='none',color='#b96413',markerfacecolor='none',label='Original, field unqualified'),
               Line2D([],[],marker='*',markersize=9,linestyle='none',color='#137955',label='Refined realization (open if unqualified)'),
               Line2D([],[],color='#263745',label='Axial recipe'),Line2D([],[],color='#91a8b5',label='12 oblique recipes')]
    fig.suptitle('Conditional Ricci-flat comparison: supplied late-window clock shifts',fontsize=14)
    fig.legend(handles=handles,loc='lower center',ncol=3,fontsize=8,bbox_to_anchor=(.5,.045))
    fig.text(.5,.015,'Positive log Z: redshift. Negative: blueshift. Red ×: clock diagnostic failed. Amplitude is not distance; no UDT selection.',ha='center',fontsize=8)
    fig.tight_layout(rect=[0,.11,1,.95])
    for suffix in ['png','pdf']:
        fig.savefig(OUT/('clock_atlas.'+suffix),dpi=180)
    plt.close(fig)
    return matplotlib.__version__

def main():
    rows, bindings, stats = build_rows()
    OUT.mkdir(exist_ok=False)
    with (OUT/'clock_atlas.csv').open('x',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    version=plot(rows)
    result=dict(status='DESCRIPTIVE_ATLAS_PENDING_REVIEW',rows=len(rows),source_sha256=bindings,
        statistics=stats,matplotlib=version,artifacts_sha256={p.name:sha(p) for p in OUT.iterdir() if p.is_file()},
        scope='Original78 and repaired13 realizations shown separately. All signs/field flags retained. Supplied Ric=0 arena, fixed short late-window clocks; no distance curve, population, continuum certification or native UDT selection. Outcomes exposed before descriptive plan.')
    with (OUT/'ATLAS.json').open('x') as stream:
        json.dump(result,stream,indent=2,allow_nan=False);stream.write('\n')
    print(json.dumps(dict(status=result['status'],statistics=stats)),flush=True)

if __name__=='__main__':
    main()
