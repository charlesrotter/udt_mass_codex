import argparse
import hashlib
import json
import pathlib

parser=argparse.ArgumentParser()
parser.add_argument('--repo',type=pathlib.Path,required=True)
args=parser.parse_args()
root=pathlib.Path(__file__).resolve().parent
expected={
    'old_root_as_phase':'new_full_phase_is_closed',
    'omit_polar_J':'intrinsic_polar_cut_area',
    'omit_conversion_q':'finite_dimensionless_label_amount',
    'phase_measure_rebuild_gauge':'fixed_measure_phase_spacing_gauge',
    'phase_blind_product':'nonseparable_product_discriminator',
}
baseline=(root/'stage_b_author_baseline.stdout').read_bytes()
author=(args.repo/'udt_g351_g352_content_bridge_campaign_2026-09-06/step_04/AUTHOR_RESULT.json').read_bytes()
assert baseline==author, 'author stdout byte mismatch'
mutants=[]
for name,guard in expected.items():
    record=json.loads((root/f'stage_b_mutant_{name}.json').read_text())
    err=(root/f'stage_b_mutant_{name}.stderr').read_text()
    lines=[line for line in err.splitlines() if line.startswith('AssertionError: ')]
    assert record['returncode']==1 and lines==['AssertionError: '+guard], (name,record,lines)
    mutants.append(dict(mutation=name,observed_first_guard=guard,returncode=record['returncode']))
changed=[]
for line in (root/'stage_a_sources.stdout').read_text().splitlines():
    digest,rel=line.split('  ',1)
    now=hashlib.sha256((args.repo/rel).read_bytes()).hexdigest()
    if now!=digest:
        changed.append(rel)
allowed=['udt_g351_g352_content_bridge_campaign_2026-09-06/CAMPAIGN_LOG.md']
assert set(changed).issubset(allowed), ('load-bearing source changed',changed)
print(json.dumps(dict(baseline_byte_identical=True,author_baseline_groups=json.loads(baseline)['group_count'],
                     mutants=mutants,stage_a_source_count=27,
                     changed_maintained_sources=changed,
                     unchanged_nonmaintenance_source_hashes=True),indent=2,sort_keys=True))
