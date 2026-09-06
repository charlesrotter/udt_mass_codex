"""Compare candidate constraints to the source-first generic tensor image.

Written after candidate proof exposure, before candidate code exposure.
Executes only the independently written source-first implementation.
"""
import contextlib
import io
import json
import pathlib

scope={'__name__':'source_first_comparison'}
with contextlib.redirect_stdout(io.StringIO()):
    exec(pathlib.Path('/tmp/tri_step03_review.pUqgBY2V/independent_tensor.py').read_text(),scope)
s=scope['s'];image=scope['image'];r=scope['r'];basis=scope['basis'];labels=scope['labels']
def unit(name):
    row=s.zeros(1,24);row[labels.index(name)]=1;return row
def E(a,b):return unit(f'E{min(a,b)}{max(a,b)}')
def T(i,tag,a,b):return unit(f'T{i}_{tag}_{min(a,b)}{max(a,b)}')
def H(i,a,b):return (T(i,'plus',a,b)+T(i,'minus',a,b))/2
def O(i,a,b):return (T(i,'plus',a,b)-T(i,'minus',a,b))/2
cycles=((1,2,3),(2,3,1),(3,1,2))
rows=[]
for i,j,k in cycles:
    for tag in ('plus','minus'):rows.append(T(i,tag,j,j)+T(i,tag,k,k))
for i,j,k in cycles:
    rows.extend((H(i,j,j)-E(j,j)+E(k,k),H(i,j,k)-2*E(j,k)))
rows.append(sum((O(i,j,k) for i,j,k in cycles),s.zeros(1,24)))
candidate=s.Matrix.vstack(*rows)
checks={
 'candidate_constraint_rank_13':candidate.rank()==13,
 'all_candidate_constraints_annihilate_independent_image':candidate*image==s.zeros(13,11),
 'exact_image_equals_candidate_constraint_kernel':s.Matrix.hstack(image,*candidate.nullspace()).rank()==11,
}

# Extract mixed B directly from the generic independent curvature tensor using
# B_li=(1/2)epsilon_jkl Q_i0jk, choosing the complementary ascending pair.
def eps(a,b,c):
    if len({a,b,c})<3:return 0
    return 1 if (a,b,c) in cycles else -1
mixed=[[s.zeros(1,11) for _ in range(3)] for _ in range(3)]
for l in range(1,4):
    for i in range(1,4):
        mixed[l-1][i-1]=sum((s.Rational(1,2)*eps(j,k,l)*r(i,0,j,k)*basis for j in range(1,4) for k in range(1,4)),s.zeros(1,11))
for i,j,k in cycles:
    assert O(i,j,j)*image/2==mixed[j-1][k-1]
odd=[O(i,j,k)*image for i,j,k in cycles]
diagonal=((odd[1]-odd[2])/3,(odd[2]-odd[0])/3,(odd[0]-odd[1])/3)
assert all(diagonal[i]==mixed[i][i] for i in range(3))
checks['candidate_mixed_inverse_all_5_components']=True

invalid_even=s.zeros(24,1)
invalid_even[labels.index('T1_plus_22')]=1
invalid_even[labels.index('T1_plus_33')]=-1
invalid_even[labels.index('T1_minus_22')]=1
invalid_even[labels.index('T1_minus_33')]=-1
invalid_odd=s.zeros(24,1)
invalid_odd[labels.index('T1_plus_23')]=1
invalid_odd[labels.index('T1_minus_23')]=-1
checks['even_counterexample_traces_pass_even_fails']=candidate[:6,:]*invalid_even==s.zeros(6,1) and candidate[6:12,:]*invalid_even!=s.zeros(6,1)
checks['odd_counterexample_first12_pass_last_fails']=candidate[:12,:]*invalid_odd==s.zeros(12,1) and candidate[12:,:]*invalid_odd==s.ones(1,1)

# Actual formula/constraint changes: each has a nonzero exact discrepancy.
wrong_factor=candidate.copy()
wrong_factor[7,:]=H(1,2,3)-E(2,3)
missing_cyclic=candidate[:12,:]
wrong_inverse=(odd[1]+odd[2])/3
controls={
 'factor_2_to_1_changes_constraint_image':wrong_factor*image!=s.zeros(13,11),
 'omit_cyclic_sum_admits_bad_record':missing_cyclic*invalid_odd==s.zeros(12,1) and missing_cyclic.rank()==12,
 'wrong_mixed_diagonal_sign_fails_tensor_reconstruction':wrong_inverse!=mixed[0][0],
}
assert all(checks.values()) and all(controls.values())
print(json.dumps(dict(candidate_hash='1d9ec37b3c7cbec4c308ea2177a824077052a2b5541cb34e23e005730a21d903',
 implementation='independent bivector constraint route; no candidate code read/import',
 checks=checks,actual_changed_formula_controls=controls,
 ranks={'candidate_constraints':candidate.rank(),'constraint_omitting_cyclic_sum':missing_cyclic.rank()},
 all_pass=True),indent=2))
