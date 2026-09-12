"""Construct documentary indices only; no scientific inference or source mutation."""
from pathlib import Path
import csv
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parent.parent
PKG = Path(__file__).resolve().parent
BASE = 'ab6033469c37f63a0f3aa6527804b7e3cd2f5be6'
PROTECTED = (
    'udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/',
    'udt_native_onshell_timelive_reset_owner_audit_2026-08-10/',
    'udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/',
    'udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12/',
    'archive/', '8_25/',
)

def dump_tsv(name, fields, rows):
    with (PKG / name).open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter='\t', lineterminator='\n')
        w.writeheader()
        w.writerows(rows)

def read_tsv(path):
    with path.open() as f:
        return list(csv.DictReader(f, delimiter='\t'))

# These editorial group summaries never replace exact registry grades or proofs.
FAMILY_TEXT = '''F01|Foundation, calibration, carrier and action|Founded reciprocal structure; observed anchors; conditional full-metric and carrier lanes|Strong local CSN challenged/inactive; S2 posit; EH conditional; native source/action/mass open|1;2;10
F02|Angular spectra, couplings and profile controls|Corrected bounded angular spectral/coupling atlases and regular-center profile roles|Mode/control evidence does not select native radial dynamics, shape or carrier|10
F03|Early complete-pair, observer and empirical interfaces|Observer/carry/overlap/full-differential and conditional observational evaluator development|Current regrades apply; protected original payloads excluded; fitted profiles/imported transfer are not native|2;7;11
F04|Valued relation networks, reconstruction and scale|Metric faithfulness with full marked area/density data; projective/ruler and carry distinctions|A valued complete state needs no second selector; full physical assignment is a different job|3;10;12
F05|Completed pair normalization and scaffold controls|Later G178 certification, G179 general pullback, G180 tape and G182 carry; control subtraction|WORKING normalization; G166 exact review-open grade distinct; supplied regular domain|2;3
F06|Clock/direction records, tomography and realization|Completed-record rank, null incidence/carry, curvature jets and Cartan realization; empirical reconstruction|Normalized scalar loss is not full-record loss; local realization hypotheses and empirical provenance retained|3;7;11
F07|Metric value, scale, quiet and projective attachment|G255 accepted recovery census; full frame carry; nonzero-weight anchor and proper-clock scale attachment|Old no-law findings scoped; no unique scale/history from c_E or projective state alone|3;4;10
F08|Observational attachment and SNe provenance|Native core intact; valid conditional evaluation and empirical calibration/holdout separated|Resolution-sensitive scale and optical-area/history boundary; no audited native SNe prediction|11
F09|History, causal and query-domain architecture|Compatibility, causal access, co-presence and complete query/germ type distinctions|Identity constraints are not values; W6 working; physical population/native full assembly open|1;3;12
F10|Response class and strengthened postulates|DDR full trace-free shape closure and entire-G301 conditional Einstein implication|Current G312 GR filter only; native membership route remains unclosed|1;4
F11|Conditional data, development and mode/response structure|Full constraints, non-CMC families, local/MGHD and explicit quotients; restricted mode/response classifications|Complete data differ from point jets; fixed datum uniqueness not data selection or stability|5;6;10
F12|Supplied-spacetime null, screen and finite-area geometry|Finite relations, full Jacobi phase flow, arbitrary-metric reciprocity and finite sheet-area theorem|Regular/chart/rank and preimage domains; geometry does not supply flux or detector weighting|7
F13|Measure, continuous readout and chosen recipes|Character classification; provisional conservation and chosen continuous readout; phase/product conditions|Weights and physical identity retain their specific ownership; later G383 acceptance overlay|1;8
F14|Shared records, phase and product persistence|Shared-measure and tide consistency; actual local phase/recipe/product preservation and departure|Finite algebra not generic PDE realization; original-data matching and restricted recurrence matter|8
F15|Optional source and joint development|Current/tensor/reconstruction interfaces and independently seeded actual joint analytic development|Optional unadopted paused law; no smooth/global stability, content or coupling selection|9
F16|Fixed-base conformal compatibility|Neighborhood-loop compatibility and bounded conformal solution classification|Fixed supplied base/domain; not all-metric degrees of freedom or absolute scale selection|10
F17|Ricci line, fibre persistence and neighboring tides|Full-data symmetry/development, nonpreservation counterexample and restricted realizable null jets|Preserving examples and exact domains survive; no generic instability or topology change|10
F18|Nonlinear realizability, localization and exact evolution|NR tangent iff; repaired 3D localization; early core; neighboring rates; NE exact positive-time family|Actual constructions with distinct reach; no universal stability/completeness/physical identity|5;6
F19|Native-response comparison and controlled limits|ND nonlinear discrimination; QC controlled bounds/counterexamples; GL conditional limit; RF realizable jets|No native selection or nonzero leading coefficient from locality alone; RF removed ambient extension requirement|4;13
F20|Expanded clock and kernel information|Endpoint-potential criterion, directional curvature readout, twist separator and exact general rotation|Full record and observer/marking conditions; no native assembly or instrument acquisition|6;7
F21|Measurement, design, benchmark and procedure|TM/RD conditional math, CO1 geometry, CO2 design, LC2 benchmark and FW2 failed sensitivity|Distinct evidence types; apparatus/support eligibility and exposure preserved|11
F22|Two-shape interaction and initial evolution|TI1/G413 and TI2/G414 full accepted conditional constructions and record recovery|Local/analytic/equation/marking limits; TI3 separate reviewed unpromoted extension|5;6;13'''

draft = read_tsv(PKG / 'REGISTRY_COVERAGE_DRAFT.tsv')
registry = read_tsv(ROOT / 'CURRENT_SCIENTIFIC_PREMISES.tsv')
assert len(draft) == len(registry) == 397

parent = {}
for p in sorted(set(re.findall(r'\]\(([^)]+)\)', (ROOT / 'UDT_CONSOLIDATED_RESEARCH_ACCOUNT.md').read_text()))):
    if p.startswith('udt_accepted_work_consolidation_2026-09-12/') or p == 'UDT_RESEARCH_ROADMAP.md':
        continue
    if p == 'UDT_METRIC_KERNEL_DEVELOPMENT.md':
        parent[p] = 'fixed-snapshot scope/pointer only; manuscript arguments not reopened'
    elif p == 'founding.md':
        parent[p] = 'W5/W6 and observed-anchor sections212--267; historical other sections not read as current status'
    elif p.endswith('BANKING_RECORD.md'):
        parent[p] = 'controlling accepted scientific claims, dependency and limit sections; original full proofs/suites not reopened for every row'
    elif p.endswith('DECISION_BRIEF.md'):
        parent[p] = 'full decision brief; later acceptance overlay used; underlying full implementation not reopened'
    elif p.endswith('REVIEWED_RESULT.md'):
        parent[p] = 'full reviewed result/scope statement; original full proof/review depth separately attributed below'
    else:
        parent[p] = 'controlling scientific report or authority/ledger inspected; source argument summary, not new proof/suite replay'

parent.update({
    'AGENTS.md': 'full current method authority reread for CWA1; not scientific evidence',
    'CLAUDE.md': 'How we work, DRIVER TRIGGERS and repository discipline only; method authority',
    'CROSS_MODEL_VERIFY.md': 'triggered scoped synthesis/review protocol; method authority',
    'CURRENT_SCIENTIFIC_PREMISES.md': 'full compact current scope; exact source grades remain controlling',
    'CURRENT_SCIENTIFIC_PREMISES.tsv': '397 rows processed without wide-row dump; selected load-bearing rows inspected; actual new full verifier PASS',
    'udt_accepted_work_consolidation_2026-09-12/STARTUP_INPUTS.json': 'CWA1 launch source record; excluded from immutable original-source pins below',
})
parent.pop('udt_accepted_work_consolidation_2026-09-12/STARTUP_INPUTS.json')
for name in ['completeness-map', 'verifier-before-record', 'no-shortcuts']:
    parent[f'.claude/skills/{name}/SKILL.md'] = 'full triggered method protocol; no scientific premise supplied'

# Additional direct reads documented in construction notes, resolved from exact registry pointers.
for ident in ['G163','G253','G255','G299','G314','G315','G316','G317','G318','G319','G320']:
    p = next(r['controlling_source'] for r in registry if r['premise_id'] == ident)
    parent[p] = 'controlling scientific audit report inspected; original derivation/suite not reopened; aggregate-read execution tails may be omitted'

reviewer = {}
for filename in ['SOURCE_READ_DEPTH.tsv', 'SUPPLEMENTAL_READ_DEPTH.tsv']:
    for row in read_tsv(PKG / 'review' / filename):
        reviewer.setdefault(row['path'], []).append(row['read_depth'])

# D1: absence from a pin table is not evidence of non-exposure. The original
# sealed assessment explicitly records these scoped startup reads.
startup_depths = {
    'AGENTS.md': 'scoped startup method authority read; parent top-level startup attributed',
    'CLAUDE.md': 'required How we work, DRIVER TRIGGERS and repository-discipline sections read at scoped startup',
    'CURRENT_SCIENTIFIC_PREMISES.md': 'compact current-premise orientation read; no source-proof census',
    'CURRENT_SCIENTIFIC_PREMISES.tsv': 'selected exact load-bearing registry rows and machine metadata; no wide whole-ledger proof review',
}
for name in ['completeness-map', 'verifier-before-record', 'no-shortcuts']:
    startup_depths[f'.claude/skills/{name}/SKILL.md'] = 'triggered protocol read at scoped startup; method, not scientific premise'
for p, depth in startup_depths.items():
    reviewer.setdefault(p, []).append(depth + '; attribution: review/SOURCE_FIRST_ASSESSMENT.md')
direct_seal = json.loads((PKG / 'review' / 'DIRECT_REVIEW_SEAL.json').read_text())
for item in direct_seal['direct_stage_source_additions']:
    require_bytes = (ROOT / item['path']).read_bytes()
    assert hashlib.sha256(require_bytes).hexdigest() == item['sha256']
    reviewer.setdefault(item['path'], []).append('direct stage: ' + item['read_depth'])

ledger = []
pins = {}
for p in sorted(set(parent) | set(reviewer)):
    assert not p.startswith(PROTECTED), p
    current = (ROOT / p).read_bytes()
    old = subprocess.check_output(['git', 'show', f'{BASE}:{p}'], cwd=ROOT)
    assert current == old, f'source changed since baseline: {p}'
    sha = hashlib.sha256(current).hexdigest()
    pins[p] = sha
    ledger.append(dict(path=p, sha256=sha,
        parent_read_depth=parent.get(p, 'not directly reopened by parent; separately attributed reviewer inspection'),
        reviewer_read_depth=' | '.join(reviewer.get(p, [])) or 'not recorded in imported reviewer source-pin/read tables; no inference of non-exposure',
        role='METHOD_OR_SCOPE' if p in ['AGENTS.md','CLAUDE.md','CROSS_MODEL_VERIFY.md','CURRENT_SCIENTIFIC_PREMISES.md','UDT_METRIC_KERNEL_DEVELOPMENT.md'] or '/skills/' in p else 'SCIENTIFIC_SOURCE_OR_ACCEPTANCE'))

dump_tsv('SOURCE_READ_LEDGER.tsv', list(ledger[0]), ledger)
(PKG / 'SOURCE_PINS.json').write_text(json.dumps(dict(baseline=BASE, interpretation='Byte correspondence only; read depth and original scopes control; no protected payloads', files=pins), indent=2, sort_keys=True)+'\n')

out = []
for r in draft:
    p = r['controlling_source_exact']
    num = int(r['premise_id'][1:]) if r['premise_id'].startswith('G') else None
    if p.startswith(PROTECTED):
        disposition = 'REGISTRY_POINTER_ONLY__PROTECTED_OR_ARCHIVE_SOURCE_NOT_OPENED'
    elif p in parent:
        disposition = 'CONTROLLING_SOURCE_SCIENTIFIC_SCOPE_INSPECTED__DEPTH_IN_SOURCE_LEDGER__NOT_REPROVED'
    elif p in reviewer:
        disposition = 'CONTROLLING_SOURCE_SEPARATE_CONTEXT_INSPECTED__DEPTH_IN_SOURCE_LEDGER__NOT_REPROVED'
    elif num is not None and 165 <= num <= 254:
        disposition = 'TRACED_THROUGH_ACCEPTED_G255_RECOVERY_AND_EXACT_CURRENT_POINTER__ORIGINAL_NOT_REOPENED'
    else:
        disposition = 'EXACT_REGISTRY_AND_FAMILY_TRACE__ORIGINAL_ARGUMENT_NOT_REOPENED'
    r['inspection_disposition'] = disposition
    out.append(r)
dump_tsv('REGISTRY_COVERAGE.tsv', list(out[0]), out)

families = []
for line in FAMILY_TEXT.splitlines():
    fid, topic, gain, limit, sections = line.split('|')
    members = [r['premise_id'] for r in out if r['family_id'] == fid]
    families.append(dict(family_id=fid, count=len(members), premise_ids=';'.join(members), topic=topic,
                         retained_gain=gain, scope_limit=limit, account_sections=sections,
                         inspection='Per-row disposition and SOURCE_READ_LEDGER.tsv; no blanket independent proof review'))
dump_tsv('FAMILY_MAP.tsv', list(families[0]), families)
print(json.dumps(dict(registry_rows=len(out), families=len(families), pinned_sources=len(pins), role='documentary construction; no scientific verification')))
