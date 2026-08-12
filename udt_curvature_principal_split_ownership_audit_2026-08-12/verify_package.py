#!/usr/bin/env python3
"""Validate the banked curvature-principal split package."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

import numpy as np


HERE=Path(__file__).resolve().parent; ROOT=HERE.parent


def rows(name):return list(csv.DictReader((HERE/name).open(),delimiter='\t'))
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(atlas,derivation,independent,founding,manifest,status):
    assert len(manifest)==len({x['path'] for x in manifest})==12
    for x in manifest:
        p=ROOT/x['path'];assert p.is_file() and sha(p)==x['sha256']
    assert founding['status']=='PASS' and all(founding['checks'].values())
    assert founding['classification_when_w_nonzero']=='D' and founding['classification_when_w_zero']=='O'
    assert founding['split_result']=={'w_nonzero':'UNIQUE_WEYL_DERIVED_SPLIT','w_zero_a_nonzero':'RICCI_DERIVED_WHEN_WEYL_DEGENERATE','w_zero_a_zero':'NO_TESTED_POINTWISE_CURVATURE_OWNER'}
    assert len(atlas)==1806
    g63=[x for x in atlas if x['scope']=='G63'];g85=[x for x in atlas if x['scope']=='G85']
    assert len(g63)==42 and len({x['identity'] for x in g63})==14
    assert all(Counter(x['point'] for x in g63)[p]==14 for p in ('p','q','r'))
    assert len(g85)==1764 and len({x['identity'].split(':')[0] for x in g85})==196
    assert len({x['identity'].split(':')[1] for x in g85})==3 and Counter(x['point'] for x in g85)==Counter({'C0':588,'CMINUS':588,'CPLUS':588})
    expected_petrov={'D':591,'I':1215}; expected_owner={'CURVATURE_ALIGNED_BUT_NOT_UNIQUE':3,'RICCI_DERIVED_WITH_WEYL_ALIGNMENT':21,'SPLIT_MISALIGNED_WITH_CURVATURE_PRINCIPALS':1194,'WEYL_AND_RICCI_AGREE_ON_SPLIT':588}
    expected_unique_owner={'CURVATURE_ALIGNED_BUT_NOT_UNIQUE':3,'RICCI_DERIVED_WITH_WEYL_ALIGNMENT':21,'SPLIT_MISALIGNED_WITH_CURVATURE_PRINCIPALS':1194,'WEYL_AND_RICCI_AGREE_ON_SPLIT':3}
    assert dict(Counter(x['petrov'] for x in atlas))==expected_petrov
    assert dict(Counter(x['owner_class'] for x in atlas))==expected_owner
    unresolved=[x for x in status if x['object']=='G85_A05_ZERO_SHIFT_KRUSKAL_LOCAL']
    assert len(unresolved)==1 and unresolved[0]['status']=='CONDITIONAL' and unresolved[0]['result']=='INSUFFICIENT_OWNED_JET'
    assert all(x['metric_negative_eigenvalues']=='1' and x['frame_classification_same']=='TRUE' for x in atlas)
    assert derivation['all_split_preserving_frame_classifications_covariant'] is True
    assert 'all_frame_classifications_covariant' not in derivation
    assert derivation['primary_landing']=='CURVATURE_OWNS_REGISTERED_SPLIT_ONLY_ON_A_PROPER_SUBSET_OF_TESTED_STRATA'
    assert derivation['status']=='PRODUCTION_COMPLETE'
    assert derivation['counts']['g85_unique_metric_jets']==1179 and derivation['counts']['total_unique_metric_jets']==1221
    assert derivation['petrov_counts']==expected_petrov and derivation['owner_counts']==expected_owner
    assert derivation['unique_metric_jet_owner_counts']==expected_unique_owner
    assert derivation['no_physical_history_selected'] is True and derivation['no_query_or_realization_selected'] is True
    assert independent['status']=='PASS' and independent['checks']==independent['pass_count']==1806 and independent['unique_metric_jets']==1221
    assert independent['petrov_counts']==expected_petrov and independent['owner_counts']==expected_owner
    assert independent['unique_metric_jet_owner_counts']==expected_unique_owner
    assert independent['max_weyl_relative_error']<=2e-5 and independent['max_ricci_relative_error']<=2e-5
    for name in ('PRODUCTION_CURVATURE_TENSORS.npz','INDEPENDENT_CURVATURE_TENSORS.npz'):
        z=np.load(HERE/name);assert z['keys'].shape==(1806,) and z['weyl'].shape==(1806,4,4,4,4) and z['ricci'].shape==(1806,4,4)
    assert len(rows('INDEPENDENT_COMPARISON.tsv'))==1806 and all(x['pass']=='TRUE' for x in rows('INDEPENDENT_COMPARISON.tsv'))
    return {'status':'PASS','atlas_rows':1806,'g63_rows':42,'g85_rows':1764,'source_rows':12,'petrov_counts':expected_petrov,'owner_counts':expected_owner,'independent_checks':1806,'unresolved_scope_rows':1}


def main():
    result=validate(rows('CURVATURE_SPLIT_ATLAS.tsv'),json.loads((HERE/'DERIVATION_RESULT.json').read_text()),json.loads((HERE/'INDEPENDENT_VERIFICATION.json').read_text()),json.loads((HERE/'FOUNDING_SYMBOLIC_RESULT.json').read_text()),rows('SOURCE_MANIFEST.tsv'),rows('STATUS_LEDGER.tsv'))
    (HERE/'PACKAGE_VERIFICATION.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':main()
