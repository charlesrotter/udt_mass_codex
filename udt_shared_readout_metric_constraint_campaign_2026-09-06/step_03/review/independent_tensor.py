"""Source-first exact algebraic route; no campaign scientific imports."""
import hashlib
import itertools
import json
import platform
import subprocess
import sys
import sympy as s

PIN='70034a6faa9264bf054eb473d5eb7a0889f3d2de'
sources=['AGENTS.md','CURRENT_SCIENTIFIC_PREMISES.tsv','founding.md',
 'udt_g261_universal_metric_coupling_parent_operator_ownership_2026-08-25/AUDIT_REPORT.md',
 'udt_g312_quiet_gr_response_constitution_discriminator_2026-09-01/AUDIT_REPORT.md',
 'startup_surface_g312_two_premise_adoption_refresh_2026-09-01/ADOPTION_RECORD.md',
 'udt_g313_tracefree_ricci_solution_space_bootstrap_map_2026-09-01/AUDIT_REPORT.md',
 'udt_g313_tracefree_ricci_solution_space_bootstrap_map_2026-09-01/EXACT_DERIVATION.md',
 'udt_g348_generic_lorentzian_null_screen_area_theorem_2026-09-04/AUDIT_REPORT.md',
 'udt_g348_generic_lorentzian_null_screen_area_theorem_2026-09-04/EXACT_DERIVATION.md']
source_hashes={p:hashlib.sha256(subprocess.check_output(['git','show',PIN+':'+p])).hexdigest() for p in sources}
eta=(-1,1,1,1)
pairs=list(itertools.combinations(range(4),2))
coeff=list(itertools.combinations_with_replacement(range(6),2))
zero=s.zeros(1,21)
def r(a,b,c,d):
    if a==b or c==d:return zero.copy()
    sign=(1 if a<b else -1)*(1 if c<d else -1)
    i=pairs.index(tuple(sorted((a,b))))
    j=pairs.index(tuple(sorted((c,d))))
    row=zero.copy()
    row[coeff.index(tuple(sorted((i,j))))]=sign
    return row
def ric(b,d):
    return sum((eta[a]*r(a,b,d,a) for a in range(4)),zero.copy())

rows=[r(0,1,2,3)+r(1,2,0,3)+r(2,0,1,3)]
for b,d in itertools.combinations_with_replacement(range(4),2):
    if (b,d)!=(0,0):rows.append(ric(b,d)+(eta[b] if b==d else 0)*ric(0,0))
constraints=s.Matrix.vstack(*rows)
basis=s.Matrix.hstack(*constraints.nullspace())
measure=[]
labels=[]
for a,b in itertools.combinations_with_replacement(range(1,4),2):
    measure.append(r(a,0,0,b));labels.append(f'E{a}{b}')
for i in range(1,4):
    screen=[a for a in range(1,4) if a!=i]
    for sign,tag in [(1,'plus'),(-1,'minus')]:
        for a,b in itertools.combinations_with_replacement(screen,2):
            measure.append(r(a,0,0,b)+r(a,i,i,b)+sign*(r(a,0,i,b)+r(a,i,0,b)))
            labels.append(f'T{i}_{tag}_{a}{b}')
observation=s.Matrix.vstack(*measure)
image=observation*basis
annihilators=s.Matrix.vstack(*(v.T for v in image.T.nullspace()))

checks={}
checks['constraint_rank']=constraints.rank()==10
checks['Einstein_dimension']=basis.shape==(21,11)
checks['observation_rank']=image.rank()==11
checks['null_only_rank']=image[6:,:].rank()==10
checks['timelike_only_rank']=image[:6,:].rank()==6
checks['annihilator_dimension_rank']=annihilators.shape==(13,24) and annihilators.rank()==13
checks['annihilator_exact']=annihilators*image==s.zeros(13,11)
for a,b,c,d in itertools.product(range(4),repeat=4):
    value=(r(a,b,c,d)+r(b,c,a,d)+r(c,a,b,d))*basis
    assert value==s.zeros(1,11)
checks['all_256_Bianchi_components']=True
for i in range(1,4):
    for tag in ('plus','minus'):
        tr=sum((image[labels.index(f'T{i}_{tag}_{a}{a}'),:] for a in range(1,4) if a!=i),s.zeros(1,11))
        assert tr==s.zeros(1,11)
checks['all_six_null_traces']=True

# K=1 constant sectional curvature in exactly the declared R convention.
constant=s.zeros(21,1)
for n,(i,j) in enumerate(coeff):
    a,b=pairs[i];c,d=pairs[j]
    delta=lambda x,y:eta[x] if x==y else 0
    constant[n]=delta(b,c)*delta(a,d)-delta(a,c)*delta(b,d)
constrecord=observation*constant
checks['constant_curvature_E_and_null']=constrecord[:6,0]==s.Matrix([-1,0,0,-1,0,-1]) and constrecord[6:,:]==s.zeros(18,1)
checks['constant_curvature_Einstein']=constraints*constant==s.zeros(10,1)

# An exact admissible sample and an individually trace-free, cross-query bad record.
sample=image*s.Matrix(range(1,12))
bad=sample.copy()
bad[labels.index('T1_plus_23')]+=1
bad[labels.index('T1_minus_23')]+=1
checks['valid_record_passes']=annihilators*sample==s.zeros(13,1)
checks['tracefree_symmetric_changed_record_rejected']=annihilators*bad!=s.zeros(13,1)

# Changed-model control: erase every mixed bivector block before observation.
erase=s.eye(21)
for n,(i,j) in enumerate(coeff):
    if (0 in pairs[i]) != (0 in pairs[j]):erase[n,n]=0
mixed_erased_rank=(observation*erase*basis).rank()
checks['erasing_mixed_curvature_breaks_full_reconstruction']=mixed_erased_rank==6
assert all(checks.values()),checks
print(json.dumps(dict(python=sys.version,sympy=s.__version__,platform=platform.platform(),
 source_pin=PIN,source_hashes=source_hashes,
 convention='R_abcd=g(R(ea,eb)ec,ed); Ric_bd=sum_a eta_aa R_abda',
 dimensions={'constraints':constraints.shape,'basis':basis.shape,'image':image.shape,'annihilator':annihilators.shape},
 ranks={'constraints':constraints.rank(),'full':image.rank(),'null_only':image[6:,:].rank(),'timelike_only':image[:6,:].rank(),'mixed_erased':mixed_erased_rank},
 labels=labels,checks=checks,
 annihilator=[[str(x) for x in row] for row in annihilators.tolist()],
 all_pass=True),indent=2))
