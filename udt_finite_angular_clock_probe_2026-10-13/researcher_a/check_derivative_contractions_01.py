"""Exhaust all g/U pairings of one differentiated Weyl tensor.

This verifies the combinatorial exhaustion in VACUUM_QUARTIC_CANDIDATE, not
the field identities or the natural-jet theorem. Slots 0..3 are Weyl slots;
remaining slots are ordered covariant derivatives, the last innermost.
"""
import collections
import hashlib
import json
from pathlib import Path


def patterns(slots):
    if not slots:
        yield (),()
        return
    first,*rest=slots
    for singles,pairs in patterns(rest):
        yield (first,)+singles,pairs
    for j,partner in enumerate(rest):
        leftover=rest[:j]+rest[j+1:]
        for singles,pairs in patterns(leftover):
            yield singles,((first,partner),)+pairs


def classify(singles,pairs,total):
    if {0,1}.issubset(singles) or {2,3}.issubset(singles):
        return 'antisymmetric_pair_has_two_U'
    if any(i<4 and j<4 for i,j in pairs):
        return 'Weyl_trace'
    inner=total-1
    if total>4 and any((i==inner and j<4) or (j==inner and i<4) for i,j in pairs):
        return 'innermost_derivative_is_Weyl_divergence'
    return 'unclassified'


def main():
    result={'meaning':'combinatorial exhaustion only; identities owned by analytic proof',
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'orders':{}}
    for degree in range(3):
        total=4+degree
        records=[];counts=collections.Counter()
        for singles,pairs in patterns(list(range(total))):
            label=classify(singles,pairs,total)
            counts[label]+=1
            records.append({'U_slots':singles,'metric_pairs':pairs,'reason':label})
        assert counts['unclassified']==0,records
        result['orders'][str(degree)]={'counts':dict(counts),'total':len(records),'patterns':records}
    target=Path(__file__).with_name('derivative_contractions_01_result.json')
    with target.open('x') as f:
        json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps({k:{j:v for j,v in val.items() if j!='patterns'} for k,val in result['orders'].items()},indent=2))


if __name__=='__main__':main()
