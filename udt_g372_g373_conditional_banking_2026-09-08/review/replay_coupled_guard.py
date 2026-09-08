"""Replay only the inspected current CD guard and its actual mutant paths.

AST selection avoids executing old scientific packages or unrelated guards.
This is shared-code regression and catch-proof, not mathematical independence.
"""
import ast
import csv
import hashlib
import json
import pathlib
import shutil
import subprocess
import tempfile
import types

REVIEW = pathlib.Path(__file__).resolve().parent
ROOT = REVIEW.parents[1]
BANK = REVIEW.parent
verifier_path = ROOT / 'verify_current_scientific_premises.py'
checker_path = BANK / 'check_banking.py'
assert hashlib.sha256(verifier_path.read_bytes()).hexdigest() == 'cb14a18ff6843b3f9224eaffb99f7cbfe0121b0d13ac3f1d7b554401fb41a929'
assert hashlib.sha256(checker_path.read_bytes()).hexdigest() == '2236e30b62b083f5f894658b30a3d634a73c4d958ae9b9a79d831e94e6a13375'

needed_constants = {'CONDITIONAL_BANKING_STATUS', 'COUPLED_BANKING_SNAPSHOT',
                    'COUPLED_BANKING_IDS', 'COUPLED_BANKING_SOURCE', 'COUPLED_BANKING_CAMPAIGN'}
needed_functions = {'read_tsv', 'require', 'validate_coupled_banking'}
nodes = []
for node in ast.parse(verifier_path.read_text()).body:
    if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id in needed_constants for t in node.targets):
        nodes.append(node)
    if isinstance(node, ast.FunctionDef) and node.name in needed_functions:
        nodes.append(node)
assert len(nodes) == len(needed_constants) + len(needed_functions)
namespace = dict(Path=pathlib.Path, ROOT=ROOT, csv=csv, hashlib=hashlib, subprocess=subprocess)
exec(compile(ast.Module(body=nodes, type_ignores=[]), str(verifier_path), 'exec'), namespace)
v = types.SimpleNamespace(**namespace)
v.validate_coupled_banking(ROOT)

# Reuse precisely the inspected author mutant expressions and rejection loop.
# Every temporary write stays in the reviewer-owned directory.
tempfile.tempdir = str(REVIEW)
selected = []
for node in ast.parse(checker_path.read_text()).body:
    if isinstance(node, ast.FunctionDef) and node.name == 'check':
        selected.append(node)
    elif isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id in {'mutants', 'caught'} for t in node.targets):
        selected.append(node)
    elif isinstance(node, ast.For) and isinstance(node.target, ast.Tuple) and [elt.id for elt in node.target.elts] == ['name', 'reg', 'rec', 'expected']:
        selected.append(node)
assert len(selected) == 4
replay = dict(v=v, checks={}, registry=(ROOT / 'CURRENT_SCIENTIFIC_PREMISES.tsv').read_text(),
              record=(ROOT / v.COUPLED_BANKING_SOURCE).read_text(), tempfile=tempfile, Path=pathlib.Path)
exec(compile(ast.Module(body=selected, type_ignores=[]), str(checker_path), 'exec'), replay)
assert len(replay['caught']) == 11

# Additional reviewer-chosen mutations target actual source-authentication paths.
# They operate on disposable copies, never the original scientific package.
source_catches = {}
for name, relative, expected in [
    ('frozen_manifest_altered', 'EVIDENCE_SHA256SUMS', 'coupled original manifest changed'),
    ('false_pass_probe_altered', 'step_02/review/author_product_assertion_probe.py', 'coupled frozen evidence changed'),
    ('original_completion_altered', 'COMPLETION_RECORD.md', 'coupled original completion receipt changed'),
]:
    with tempfile.TemporaryDirectory(prefix='cd-review-source-') as temp:
        fixture = pathlib.Path(temp)
        (fixture / 'CURRENT_SCIENTIFIC_PREMISES.tsv').write_text(replay['registry'])
        record = fixture / v.COUPLED_BANKING_SOURCE
        record.parent.mkdir(parents=True)
        record.write_text(replay['record'])
        campaign = fixture / v.COUPLED_BANKING_CAMPAIGN
        shutil.copytree(ROOT / v.COUPLED_BANKING_CAMPAIGN, campaign)
        target = campaign / relative
        target.write_bytes(target.read_bytes() + b'\nREVIEW_INTENTIONAL_MUTANT\n')
        try:
            v.validate_coupled_banking(fixture)
        except SystemExit as error:
            assert expected in str(error), str(error)
            source_catches[name] = str(error)
        else:
            raise AssertionError('false-pass source mutant ' + name)

print(json.dumps({
    'kind': 'SHARED_GUARD_REGRESSION_WITH_ACTUAL_REJECTION_PATHS_NOT_SCIENTIFIC_PROOF',
    'positive_new_guard': 'PASS',
    'author_mutants_caught': replay['caught'],
    'reviewer_source_mutants_caught': source_catches,
    'old_guard_or_scientific_replay': False,
    'scratch_scope': str(REVIEW),
}, indent=2, sort_keys=True))
