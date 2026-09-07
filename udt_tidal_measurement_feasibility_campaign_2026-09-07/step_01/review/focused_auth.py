"""Authenticate the one mathematical-qualifier repair without git mutation.

No new numerical science: compare exact original/repaired byte hashes,
unchanged source/check evidence and preserved initial review/counterexample.
The linear implication is adjudicated analytically in FOCUSED_REVIEW.md.
"""
import difflib
import hashlib
import json
import pathlib

root=pathlib.Path(__file__).resolve().parents[1]
checks={}
def check(name, claim):
    assert claim, name
    checks[name]=True
def digest(data): return hashlib.sha256(data).hexdigest()
new=(root/'CANDIDATE_ARGUMENT.md').read_bytes()
check('repaired_candidate_hash',digest(new)=='680378622607ea82dad018620fd2408ae989854e3b8539e56e1ef07cf4b94163')
check('one_repair_phrase',new.count(b'a fixed linear operator H')==1)
old=new.replace(b'a fixed linear operator H',b'an operator H',1)
check('inverse_exact_edit_recovers_frozen_original',digest(old)=='589eff684d768831a1390b525e2257ba78f0048b6966c8ae2579097585d1ec44')
expected={
 'check_interface.py':'25321733e08c54d9c2eea7de1b2d8472a61f3682e142166d45765b58e74b768e',
 'SOURCE_LEDGER.tsv':'5f7f67d531f9cf7b66b96783020a80fc04971c34af09c96deec4aedd0f757ad6',
 'SOURCE_ACCESS_AND_EXPOSURE.md':'5f14ff6ffe0153e9b0023693d496bda31eb1f76d354a8abcaabff89c25a8a762',
 'author_check.stdout':'a3986549adb6f2ad3f659386c27135d46c4240063ea30d4d8908a41d7fb98915',
 'author_check.json':'c13778e4ebb589310b24ec83d94cdba353b30143f1a914e368a530a84ae3e8c0',
 'review/DIRECT_ADVERSARIAL_REVIEW.md':'5f80614246b472a3375ea16f9fc84e03863a7356772891da5eff75cf68c580ae',
 'review/STAGE_A_PRIMARY_ADDENDUM.md':'a1761f6e9b48394816166c07cd2559ecb86dae8f8bc90631b69cfa713a0095b5',
}
for path,value in expected.items():
    check('unchanged:'+path,digest((root/path).read_bytes())==value)
check('initial_counterexample_retained','H_one_zero_does_not_imply_constant_blindness' in (root/'review/direct_exact.stdout').read_text())
print(json.dumps({'kind':'EXACT_REPAIR_AUTHENTICATION_NOT_NEW_SCIENTIFIC_PROOF',
 'checks':checks,'count':len(checks),
 'diff':''.join(difflib.unified_diff(old.decode().splitlines(True),new.decode().splitlines(True),fromfile='frozen_initial',tofile='repaired_candidate')),
 'analytic_implication':'Linearity and H(1)=0 imply H(z+kappa*1)=H(z)+kappa*H(1)=H(z).',
 'note':'The grammatical article changes from an to a along with adding fixed linear.'},indent=2,sort_keys=True))
