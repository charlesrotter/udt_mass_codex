#!/usr/bin/env python3
"""Mutation catches for the curvature-principal split package."""

from __future__ import annotations

import copy,csv,json
from pathlib import Path

from verify_package import validate

HERE=Path(__file__).resolve().parent
def rows(name):return list(csv.DictReader((HERE/name).open(),delimiter='\t'))
def expect(name,mutate,state):
    s=copy.deepcopy(state);mutate(s)
    try:validate(s['atlas'],s['d'],s['i'],s['f'],s['m'],s['s'])
    except Exception:return {'catch':name,'status':'CAUGHT'}
    raise RuntimeError('mutation escaped: '+name)


def main():
    state={'atlas':rows('CURVATURE_SPLIT_ATLAS.tsv'),'d':json.loads((HERE/'DERIVATION_RESULT.json').read_text()),'i':json.loads((HERE/'INDEPENDENT_VERIFICATION.json').read_text()),'f':json.loads((HERE/'FOUNDING_SYMBOLIC_RESULT.json').read_text()),'m':rows('SOURCE_MANIFEST.tsv'),'s':rows('STATUS_LEDGER.tsv')}
    validate(state['atlas'],state['d'],state['i'],state['f'],state['m'],state['s'])
    tests=[
      ('missing_G63_row',lambda s:s['atlas'].pop(0)),
      ('missing_G85_profile_identity',lambda s:s['atlas'].__setitem__(slice(None),[x for x in s['atlas'] if 'G75_AM_S01_E05:' not in x['identity']])),
      ('collapse_D_to_II',lambda s:next(x for x in s['atlas'] if x['petrov']=='D').update(petrov='II')),
      ('invent_type_O_aether_landing',lambda s:s['f'].update(classification_when_w_zero='AETHER_REQUIRED')),
      ('promote_history_selection',lambda s:s['d'].update(no_physical_history_selected=False)),
      ('promote_query_selection',lambda s:s['d'].update(no_query_or_realization_selected=False)),
      ('corrupt_source_hash',lambda s:s['m'][0].update(sha256='0'*64)),
      ('false_frame_covariance',lambda s:s['atlas'][0].update(frame_classification_same='FALSE')),
      ('independent_check_removed',lambda s:s['i'].update(pass_count=1805)),
      ('loosen_tensor_error',lambda s:s['i'].update(max_weyl_relative_error=3e-5)),
      ('wrong_package_landing',lambda s:s['d'].update(primary_landing='CURVATURE_OWNS_REGISTERED_SPLIT_ON_ALL_TESTED_NONDEGENERATE_STRATA')),
      ('owner_count_promotion',lambda s:s['d']['owner_counts'].update(WEYL_AND_RICCI_AGREE_ON_SPLIT=589)),
      ('founding_D_without_O_branch',lambda s:s['f'].update(classification_when_w_zero='D')),
      ('remove_unresolved_zero_shift_scope',lambda s:s['s'].__setitem__(slice(None),[x for x in s['s'] if x['object']!='G85_A05_ZERO_SHIFT_KRUSKAL_LOCAL'])),
    ]
    out=[expect(name,mut,state) for name,mut in tests]
    result={'status':'PASS','catch_count':len(out),'caught':sum(x['status']=='CAUGHT' for x in out)}
    (HERE/'CATCH_PROOF_RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    with (HERE/'CATCH_PROOFS.tsv').open('w',newline='') as f:
      w=csv.DictWriter(f,fieldnames=('catch','status'),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(out)
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':main()
