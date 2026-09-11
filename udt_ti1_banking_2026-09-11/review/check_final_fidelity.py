#!/usr/bin/env python3
"""Final pin/prose/audit correspondence after the sealed substantive review."""
import ast
import datetime
import hashlib
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
PKG=ROOT/'udt_ti1_banking_2026-09-11'
REVIEW=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import ti1_banking_guard as ti1
import verify_current_scientific_premises as guard

sealed=json.loads((REVIEW/'REVIEW_RECEIPT.json').read_text())
for name,want in sealed['sha256'].items():
    if name=='ti1_banking_guard.py':
        continue
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==want,('sealed input changed',name)

def without_pin_assignment(source):
    tree=ast.parse(source)
    found=[]
    updates=[]
    retained=[]
    for node in tree.body:
        if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='TI1_PINS' for t in node.targets):
            found.append(ast.literal_eval(node.value))
        elif (isinstance(node,ast.Expr) and isinstance(node.value,ast.Call)
              and isinstance(node.value.func,ast.Attribute)
              and isinstance(node.value.func.value,ast.Name)
              and node.value.func.value.id=='TI1_PINS'
              and node.value.func.attr=='update'):
            assert len(node.value.args)==1 and not node.value.keywords
            updates.append(ast.literal_eval(node.value.args[0]))
        else:
            retained.append(node)
    assert len(found)==1
    assert len(updates)<=1
    for addition in updates:
        assert isinstance(addition,dict) and not set(addition)&set(found[0])
        found[0].update(addition)
    tree.body=retained
    return found[0],ast.dump(tree,include_attributes=False)

old_pins,old_ast=without_pin_assignment((REVIEW/'INITIAL_TI1_GUARD.py').read_text())
new_pins,new_ast=without_pin_assignment((ROOT/'ti1_banking_guard.py').read_text())
assert old_ast==new_ast,'non-pin guard behavior changed after tested version'
new_review_names={str((REVIEW/name).relative_to(ROOT)) for name in ('REVIEW.md','REVIEW_RECEIPT.json')}
assert set(new_pins)==set(old_pins)|new_review_names
assert all(new_pins[k]==v for k,v in old_pins.items())
for name in new_review_names:
    assert new_pins[name]==hashlib.sha256((ROOT/name).read_bytes()).hexdigest()

audit=PKG/'checks/full396_post_repair'
receipt=json.loads(Path(str(audit)+'.json').read_text())
out=Path(str(audit)+'.stdout').read_text()
assert receipt['returncode']==0 and receipt['timeout'] is False
assert not Path(str(audit)+'.stderr').read_bytes()
assert 'PASS: 396-row premise registry' in out and 'PASS: G413/TI1' in out
inputs=json.loads((PKG/'POST_REPAIR_AUDIT_INPUTS.json').read_text())['sha256']
allowed_prose={'LIVE.md','HANDOFF.md','INDEX.md','MEMORY.md','CURRENT_SCIENTIFIC_PREMISES.md','CURRENT_RESEARCH_PROGRAM.md'}
changed=[name for name,want in inputs.items() if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=want]
assert set(changed)<=allowed_prose,('nonprose audit input changed',changed)
ti1.validate_ti1_banking(ROOT)
guard.validate_startup_surface(ROOT)

names=('LIVE.md','HANDOFF.md','CURRENT_RESEARCH_PROGRAM.md','CURRENT_SCIENTIFIC_PREMISES.md',
       'AGENTS.md','INDEX.md','MEMORY.md','UDT_RESEARCH_ROADMAP.md')
docs={name:{'sha256':hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),
            'lines':len((ROOT/name).read_text().splitlines()),
            'words':len((ROOT/name).read_text().split())} for name in names}
print(json.dumps({'status':'PASS','observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'sealed_review_pins_authenticated':len(sealed['sha256'])-1,
 'guard_changes_since_review':'ONLY_TWO_IMMUTABLE_REVIEW_PINS; AST_OTHERWISE_IDENTICAL',
 'final_audit_receipt':receipt,'audited_nonprose_inputs_unchanged':True,
 'later_prose_changes':changed,'documents':docs,
 'guard_and_startup_calls':'ACTUAL_PASS; correspondence/regression, not new science proof',
 'publication':'NOT_CHECKED; parent owns actual staging/commit/push outcomes'},indent=2))
