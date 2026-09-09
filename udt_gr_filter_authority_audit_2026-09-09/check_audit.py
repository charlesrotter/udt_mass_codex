"""Small correspondence and already-proved identity anchors, NOT source certification."""
import csv
import hashlib
import io
import json
from fractions import Fraction as Q
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = '4a699eec12b656a9487fa41f5ebad5993ef7adc5'
GIT = ['git', '-c', 'core.preloadIndex=false', '-c', 'index.threads=1']
ALLOWED = {'LIVE.md', 'HANDOFF.md', 'CURRENT_RESEARCH_PROGRAM.md',
           'CURRENT_SCIENTIFIC_PREMISES.md', 'MEMORY.md', 'INDEX.md'}
FROZEN = {
    'INITIAL_AUDIT.md': 'eb5fcd6b279e463f9a0e96cbf3cc32f1a15f08f27cf9d4f8e01415c0216d03b9',
    'AUTHORITY_MAP.tsv': 'bd24957354f8c4d0c4dd5ce54a00df7fc8af792ccdf67c79b1e162ee40d7569e',
    'DEPENDENCY_IMPACT.tsv': '13c7e57784f2470db762d3ae01f6bde0e9f6b012cb001a54f0a2e4133188559e',
}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def git(*args):
    return subprocess.check_output(GIT + list(args), cwd=ROOT)

checks = []
def check(name, truth):
    if not truth:
        raise AssertionError(name)
    checks.append(name)

source_rows = list(csv.DictReader((HERE / 'SOURCE_LIST.tsv').open(), delimiter='\t'))
pins = []
for row in source_rows:
    path = row['path']
    current = (ROOT / path).read_bytes()
    check('unchanged_source:' + row['id'], current == git('show', BASE + ':' + path))
    pins.append([row['id'], path, sha(current), str(len(current)), row['read_scope']])
out = io.StringIO()
writer = csv.writer(out, delimiter='\t', lineterminator='\n')
writer.writerow(['id', 'path', 'sha256', 'bytes', 'read_scope'])
writer.writerows(pins)
pin_data = out.getvalue().encode()
pin_path = HERE / 'SOURCE_PINS.tsv'
if '--freeze-pins' in sys.argv:
    with pin_path.open('xb') as stream:
        stream.write(pin_data)
else:
    check('source_pin_correspondence', pin_path.read_bytes() == pin_data)

for name, digest in FROZEN.items():
    check('initial_freeze:' + name, sha((HERE / name).read_bytes()) == digest)
registry = list(csv.DictReader((ROOT / 'CURRENT_SCIENTIFIC_PREMISES.tsv').open(), delimiter='\t'))
check('365_unique_registry_rows', len(registry) == len({r['premise_id'] for r in registry}) == 365)
for name in ['AUTHORITY_MAP.tsv', 'DEPENDENCY_IMPACT.tsv']:
    rows = list(csv.DictReader((HERE / name).open(), delimiter='\t'))
    check('well_formed_unique_map:' + name,
          len(rows) == len({r['id'] for r in rows}) and
          all(None not in r and all(v for v in r.values()) for r in rows))

# Trace identity on a finite spanning basis of symmetric covariant tensors.
# The source's analytic argument, not these examples, owns the general statement.
signature = [-1, 1, 1, 1]
metric = [[Q(signature[i] if i == j else 0) for j in range(4)] for i in range(4)]
def trace(tensor):
    return sum(signature[i] * tensor[i][i] for i in range(4))
def tf(tensor):
    tr = trace(tensor)
    return [[tensor[i][j] - tr * metric[i][j] / 4 for j in range(4)] for i in range(4)]
basis_count = 0
for i in range(4):
    for j in range(i, 4):
        ric = [[Q(int((a, b) in {(i, j), (j, i)})) for b in range(4)] for a in range(4)]
        scalar = trace(ric)
        for a, b in [(Q(2, 3), Q(-7, 5)), (Q(-3), Q(1, 2)), (Q(0), Q(5))]:
            response = [[a * ric[m][n] + b * scalar * metric[m][n] for n in range(4)] for m in range(4)]
            check(f'trace_identity:{i}:{j}:{a}', tf(response) == [[a*x for x in row] for row in tf(ric)])
        basis_count += 1
check('nonzero_scalar_response_is_not_zero_response', tf(metric) == [[Q(0)]*4 for _ in range(4)] and metric[0][0] != 0)
# Contracted Bianchi coefficients in four dimensions, only after choosing Ricci S.
check('bianchi_coefficient', Q(1, 2) - Q(1, 4) == Q(1, 4))

# Recompute G260's retained static family from analytic derivatives, at finite points.
angular_count = 0
for a, b, r in [(Q(0), Q(-1), Q(2)), (Q(2), Q(3), Q(1)),
                (Q(-1, 8), Q(1, 2), Q(1)), (Q(3, 7), Q(-2, 5), Q(3))]:
    f = 1 + a*r*r + b/r
    fp = 2*a*r - b/r**2
    fpp = 2*a + 2*b/r**3
    e0 = r*fp+f-1
    e1 = r*fp+r*r*fpp/2
    check('positive_domain:' + str(angular_count), f > 0 and r > 0)
    check('angular_family:' + str(angular_count), e0 == e1 == 3*a*r*r)
    angular_count += 1
check('cancellation_not_ricci_flat_separator', 3*Q(2)*Q(1)**2 != 0)

changed = set(git('diff', '--name-only', BASE, '--').decode().splitlines())
foreign = {p for p in changed if p not in ALLOWED and not p.startswith(HERE.name + '/')}
check('only_authorized_root_and_audit_changes', not foreign)
check('grok_branch', git('branch', '--show-current').strip() == b'grok')
status = git('status', '--short', '--untracked-files=normal').decode().splitlines()
untracked = sorted(line for line in status if line.startswith('?? ') and
                   not line.startswith('?? ' + HERE.name + '/'))
check('unrelated_untracked_name_set', len(untracked) == 46 and
      sha('\n'.join(untracked).encode()) == 'd65d71d63a56b95aabfd61f33317b1f1f2b2a62a85ded8258c525b99a5e156ea')
print(json.dumps(dict(status='PASS_BOUNDED_AUDIT_CORRESPONDENCE_AND_IDENTITY_ANCHORS',
                     baseline=BASE, python=sys.version, source_pins=len(pins),
                     check_count=len(checks), checks=checks, symmetric_basis_tensors=basis_count,
                     spherical_examples=angular_count, authorized_root_changes=sorted(changed & ALLOWED),
                     unrelated_untracked_entries=len(untracked), protected_payload_bytes='NOT_INSPECTED',
                     full365='FAILED_SEPARATE_STARTUP_ATTEMPT_G325_NOT_REPLAYED_HERE',
                     scope='Not theorem certification, physical selection, complete dependencies, or guard migration'),
                 indent=2, sort_keys=True))
