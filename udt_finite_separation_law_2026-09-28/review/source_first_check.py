"""Independent exact-rational source-first checks; no FSL1 author code imported."""
import hashlib,json,pathlib,platform,subprocess,sys
from fractions import Fraction as F
ROOT=pathlib.Path('/home/udt-admin/udt_mass_codex')
R=ROOT/'udt_finite_separation_law_2026-09-28/review'
checks=[]
def check(name,condition):
    if not condition: raise AssertionError(name)
    checks.append(name)
def mm(a,b): return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def mv(a,v): return [sum(x*y for x,y in zip(row,v)) for row in a]
def trans(a): return list(map(list,zip(*a)))
def I(): return [[F(int(i==j)) for j in range(4)] for i in range(4)]
def boost(axis,t):
    b=I(); c=(1+t*t)/(1-t*t);s=2*t/(1-t*t)
    b[0][0]=b[axis][axis]=c;b[0][axis]=b[axis][0]=s
    return b
eta=I();eta[0][0]=-1
rot=I();rot[1][1]=rot[2][2]=0;rot[1][2]=-1;rot[2][1]=1
b1=boost(1,F(1,2));b2=boost(2,F(1,3));br=mm(b1,rot)
for j,b in enumerate([b1,b2,br,mm(b2,b1)]):check(f'Lorentz_{j}',mm(mm(trans(b),eta),b)==eta)
ray_y=[F(1),F(0),F(1),F(0)]
ray=ray_y
f1=mv(b1,ray);n1=[v/f1[0] for v in f1]
f2=mv(b2,n1);full=mv(mm(b2,b1),ray)
check('same_ray_composition',full[0]==f1[0]*f2[0])
check('wrong_untransported_direction_rejected',full[0]!=f1[0]*mv(b2,ray)[0])
check('same_column',mv(b1,[1,0,0,0])==mv(br,[1,0,0,0]))
rayx=[F(1),F(1),F(0),F(0)]
check('same_column_distinct_clock_factor',mv(b1,rayx)[0]!=mv(br,rayx)[0])
for j,b in enumerate([b1,b2,br,mm(b2,b1)]):
  for d,ray in enumerate([[1,1,0,0],[1,0,1,0],[1,0,0,1],[1,-1,0,0]]):
    y=mv(b,ray);c=mv(b,[1,0,0,0]);chi=[v/c[0] for v in c[1:]];m=[v/y[0] for v in y[1:]]
    check(f'received_direction_formula_{j}_{d}',1/y[0]==c[0]*(1-sum(a*z for a,z in zip(chi,m))))
check('planar_forward_factor',mv(b1,rayx)[0]==3)
check('planar_opposite_factor',mv(b1,[1,-1,0,0])[0]==F(1,3))
boundary=[]
for w in [F(1),F(10),F(100)]:
  gamma=1+w*w/2;a=w*w/2
  check(f'boundary_unit_clock_{w}',-gamma*gamma+a*a+w*w==-1)
  check(f'boundary_no_redshift_{w}',gamma-a==1)
  boundary.append({'w':str(w),'gamma':str(gamma),'rho_squared':str(1-1/(gamma*gamma)),'interval_ratio':'1'})
launch=json.loads((ROOT/'udt_finite_separation_law_2026-09-28/LAUNCH.json').read_text())
source_hashes={}
for rel,expected in launch['sources'].items():
  actual=hashlib.sha256((ROOT/rel).read_bytes()).hexdigest();check('launch_hash_'+rel,actual==expected);source_hashes[rel]=actual
extra=['CROSS_MODEL_VERIFY.md','.claude/skills/verifier-before-record/SKILL.md','.claude/skills/no-shortcuts/SKILL.md','.claude/skills/completeness-map/SKILL.md','udt_g274_projective_pair_position_network_descent_2026-08-26/SOURCE_MANIFEST.tsv','udt_g269_null_transport_mutual_clock_screen_interlock_2026-08-26/EXACT_DERIVATION.md','udt_g272_complete_relation_rapidity_distance_ownership_2026-08-26/EXACT_DERIVATION.md','udt_g273_projective_pair_distance_foundational_ownership_2026-08-26/EXACT_DERIVATION.md','udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py','udt_finite_separation_law_2026-09-28/WORK_ORDER.md','udt_finite_separation_law_2026-09-28/LAUNCH.json']
for rel in extra:source_hashes[rel]=hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()
for line in (ROOT/'udt_g274_projective_pair_position_network_descent_2026-08-26/SOURCE_MANIFEST.tsv').read_text().splitlines()[1:]:
  rel,digest,_=line.split('\t')
  if rel in extra:check('G274_manifest_'+rel,source_hashes[rel]==digest)
out={'python':sys.version,'platform':platform.platform(),'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'branch':subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip(),'checks':checks,'count':len(checks),'composition':{'correct':str(full[0]),'wrong_direction':str(f1[0]*mv(b2,ray_y)[0])},'column_separator':{'first':str(mv(b1,rayx)[0]),'second':str(mv(br,rayx)[0])},'boundary_sequence':boundary,'source_hashes':source_hashes}
with (R/'source_first_result_corrected.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
print(json.dumps(out,indent=2))
