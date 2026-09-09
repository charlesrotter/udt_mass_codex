"""Generate correspondence manifests without opening any author candidate/code."""
import hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[2]
review=Path(__file__).resolve().parent
sources=['AGENTS.md','LIVE.md','HANDOFF.md','CURRENT_RESEARCH_PROGRAM.md',
 'CURRENT_SCIENTIFIC_PREMISES.md','CURRENT_SCIENTIFIC_PREMISES.tsv','CLAUDE.md',
 'INDEX.md','MEMORY.md','CROSS_MODEL_VERIFY.md',
 '.claude/skills/no-shortcuts/SKILL.md','.claude/skills/completeness-map/SKILL.md',
 '.claude/skills/verifier-before-record/SKILL.md','.claude/skills/solver-first/SKILL.md',
 '.claude/skills/solution-space-not-imposition/SKILL.md',
 'startup_surface_g310_universal_reciprocity_refresh_2026-08-31/ADOPTION_RECORD.md',
 'startup_surface_g312_two_premise_adoption_refresh_2026-09-01/ADOPTION_RECORD.md',
 'udt_nonlinear_ripple_geometry_2026-09-09/WORK_ORDER.md',
 'udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py']
for package in ['udt_g303_two_class_nonlinear_cauchy_data_classification_2026-08-30',
 'udt_g315_conditional_cauchy_characteristic_data_interface_2026-09-01',
 'udt_g327_g324_axial_first_fourier_tensor_modes_2026-09-02']:
    sources += [package+'/'+f for f in ['AUDIT_REPORT.md','EXACT_DERIVATION.md']]
sources += ['udt_spatial_curvature_evolution_2026-09-09/'+f for f in
 ['CANDIDATE.md','PROVENANCE_CORRECTION.md','review/DIRECT_REVIEW.md','review/PROVENANCE_FOLLOWUP.md']]
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
with (review/'SOURCE_FIRST_SOURCE_PINS.tsv').open('x') as out:
    out.write('path\tsha256\n')
    for name in sources:
        out.write(name+'\t'+digest(root/name)+'\n')
files=sorted(p for p in review.iterdir() if p.is_file())
with (review/'SOURCE_FIRST_SHA256SUMS').open('x') as out:
    for path in files:
        out.write(digest(path)+'  '+str(path.relative_to(root))+'\n')
print('SOURCE_FIRST.md '+digest(review/'SOURCE_FIRST.md'))
print('SOURCE_FIRST_SHA256SUMS '+digest(review/'SOURCE_FIRST_SHA256SUMS'))
print('entries '+str(len(files)))
