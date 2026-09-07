"""Execute the actual zero-residual assertion on computed defective operators."""
import json
import screen
x=screen.method_checks(); caught={}
for name in ['wrong_sign_relative','missing_H_term_relative','physical_scale_wrong_relative']:
    try:assert x[name]<1e-10
    except AssertionError:caught[name]='EXPECTED_ASSERTION_FAILURE'
    else:raise AssertionError('False pass: '+name)
assert x['correct_null_relative']<1e-10
assert x['physical_scale_correct_relative']<1e-10
print(json.dumps(dict(scope='same-author synthetic catch-proof, not independent review',
 computed_relative_errors=x,defective_zero_assertions=caught,all_defects_rejected=True),indent=2))
