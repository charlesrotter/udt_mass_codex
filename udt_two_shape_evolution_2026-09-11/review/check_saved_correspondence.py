#!/usr/bin/env python3
"""Post-exposure saved-output correspondence and exact coefficient audit."""
import hashlib,json,pathlib,platform
import sympy as S
repo=pathlib.Path(__file__).resolve().parents[2]
root=pathlib.Path(__file__).resolve().parents[1]
review=pathlib.Path(__file__).resolve().parent
seal=json.loads((review/'STAGE_A_SEAL.json').read_text())
for p,digest in seal['sha256'].items():
 assert hashlib.sha256((repo/p).read_bytes()).hexdigest()==digest,('Stage_A_pin',p)
rows=(repo/'CURRENT_SCIENTIFIC_PREMISES.tsv').read_text().splitlines()
for q,line in seal['selected_registry_rows'].items(): assert next(x for x in rows if x.startswith(q+'\t'))==line,q
pre=json.loads((root/'PRECOMPUTATION_FREEZE.json').read_text())
for p,digest in pre['sha256'].items(): assert hashlib.sha256((repo/p).read_bytes()).hexdigest()==digest,('author_precomputation',p)
old=[]
for line in (repo/'udt_ti1_banking_2026-09-11/SOURCE_EVIDENCE_SHA256SUMS').read_text().splitlines():
 digest,p=line.split(maxsplit=1);p=p.removeprefix('*')
 assert p.startswith('udt_two_shape_nonlinear_interaction_2026-09-11/'),p
 assert hashlib.sha256((repo/p).read_bytes()).hexdigest()==digest,('TI1',p)
 old.append(p)
author=json.loads((root/'checks/initial_rate.stdout').read_text())
own=json.loads((review/'adm_rate_repaired.stdout').read_text())
p,r,px,rx,pxx,rxx=S.symbols('p r p_X r_X p_XX r_XX',real=True)
s=S.symbols('s',real=True,nonzero=True)
env={str(x):x for x in (p,r,px,rx,pxx,rxx,s)};env['Matrix']=S.Matrix
parse=lambda v:S.sympify(v,locals=env)
mapping={'E':'E','B':'B','E_T':'Edot','B_T':'Bdot','P':'P','P_T_general_profile_jet':'Pdot_general',
 'P_T_harmonic':'Pdot_harmonic','L_harmonic':'L','L0':'L0','S':'S','Ric3_T':'Ric3_dot'}
for a,b in mapping.items():
 delta=parse(author[a])-parse(own[b]);values=list(delta) if isinstance(delta,S.MatrixBase) else [delta]
 assert all(S.factor(v)==0 for v in values),('independent_saved_quantity_correspondence',a)
eps=S.symbols('epsilon',real=True)
scale={p:eps*p,r:eps*r,px:eps*px,rx:eps*rx,pxx:eps*pxx,rxx:eps*rxx}
coeff=lambda expr,n:S.diff(expr.subs(scale,simultaneous=True),eps,n).subs(eps,0)/S.factorial(n)
E=parse(own['E']);ET=parse(own['Edot']);B=parse(own['B']);BT=parse(own['Bdot'])
dot=lambda A,B:sum(A[i,j]*B[i,j] for i in range(3) for j in range(3))
bg_second=S.factor(16*dot(coeff(E,0),coeff(BT,2)))
linear_parts=S.factor(16*(dot(coeff(ET,1),coeff(B,1))+dot(coeff(E,1),coeff(BT,1))))
total=S.factor(coeff(parse(own['Pdot_general']),2))
W=p*rx-r*px
assert S.factor(bg_second-80*s*s*W)==0
assert S.factor(total-bg_second-linear_parts)==0
assert S.factor(bg_second.subs(s,-S.Rational(2,3))-S.Rational(320,9)*W)==0
print(json.dumps({'status':'PASS','python':platform.python_version(),'sympy':S.__version__,
 'seal_pins':len(seal['sha256']),'author_precomputation_pins':len(pre['sha256']),
 'original_TI1_preserved_files':len(old),'registry_rows':list(seal['selected_registry_rows']),
 'independent_saved_expression_groups':list(mapping),'leading_P_rate_background_E_times_second_B_rate':str(bg_second),
 'leading_P_rate_first_order_products_general_profile':str(linear_parts),
 'leading_P_rate_total_general_profile':str(total),
 'meaning':'Exact coefficient decomposition; first-order-only product omission demonstrated, no general linearization-failure theorem',
 'author_scientific_execution':'saved outputs inspected; not same-code replay'},indent=2))
