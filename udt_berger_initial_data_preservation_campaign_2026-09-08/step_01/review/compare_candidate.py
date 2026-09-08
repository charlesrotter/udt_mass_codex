"""Post-seal comparison of frozen author results against independent saved tensors."""
import json
from pathlib import Path
import sympy as S

step=Path('udt_berger_initial_data_preservation_campaign_2026-09-08/step_01')
independent=json.loads((step/'review/source_first_run.stdout').read_text())
author=json.loads((step/'author_check_02.stdout').read_text())
p,q=S.symbols('p q',positive=True)
x,y,z,u,v,w=S.symbols('x y z u v w',real=True)
own_symbols=dict(zip(['p','q','x','y','z','u','v','w'],[p,q,x,y,z,u,v,w]))
author_symbols=dict(zip(['p','q','u','w','v','z','r','t'],[p,q,x,y,z,u,v,w]))
def own(expr):
    return S.sympify(expr,locals=own_symbols)
def theirs(expr):
    return S.sympify(expr,locals=author_symbols)
Sd=own(independent['homogeneous_Ricci_dot'])
Ad=own(independent['homogeneous_endomorphism_dot'])
author_S=S.Matrix([[theirs(item) for item in row] for row in author['symbolic_S']])
author_Pd=S.Matrix([[theirs(item) for item in row] for row in author['symbolic_Pdot']])
author_M=S.Matrix([theirs(item) for item in author['symbolic_momentum']])
P=S.diag(0,0,1)
Q=S.eye(3)-P
gap=q*(q-p)
own_Pd=(Q*Ad*P+P*Ad*Q)/gap
own_M=S.Matrix([(q-p)*w,(p-q)*v,0])
K=S.Matrix([[x,u,v],[u,y,w],[v,w,z]])
checks=[]
def check(name,residual):
    residual=S.simplify(residual)
    entries=list(residual) if isinstance(residual,S.MatrixBase) else [residual]
    checks.append({'name':name,'pass':all(e==0 for e in entries),'residual':str(residual)})
check('all nine saved Ricci variations equal independent Koszul derivative',author_S-Sd)
check('all nine saved projector variations equal independent result',author_Pd-own_Pd)
check('all three saved momentum expressions equal independent result',author_M-own_M)

# Recompute every saved fixture from exact supplied entries, not author flags.
fixtures=[]
for i,item in enumerate(author['fixtures']):
    a,c=S.Rational(item['a']),S.Rational(item['c'])
    matrix=S.Matrix([[S.Rational(entry) for entry in row] for row in item['K']])
    sub={p:2/c,q:2*c/a**2,x:matrix[0,0],y:matrix[1,1],z:matrix[2,2],
         u:matrix[0,1],v:matrix[0,2],w:matrix[1,2]}
    H=8/a**2-2*c**2/a**4+S.trace(matrix)**2-S.trace(matrix*matrix)-2*item['Lambda']
    M=own_M.subs(sub)
    PD=own_Pd.subs(sub)
    check(f'fixture {i} exact Hamiltonian',H)
    check(f'fixture {i} independent momentum',M)
    check(f'fixture {i} independent projector derivative',PD)
    fixtures.append({'index':i,'Hamiltonian':str(H),'momentum':str(M),'projector_dot':str(PD)})

# The author's division-free chart is a bijective linear relabeling of all survivors.
C,V,d,b,E=S.symbols('C V d b E',real=True)
inverse={x:C-V+d,y:C-V-d,z:V,u:b,v:0,w:0}
forward=S.Matrix([(x+y)/2+z,z,(x-y)/2,u])
check('quadric chart inverse',forward.subs(inverse)-S.Matrix([C,V,d,b]))
check('quadric exactly original constraint',
      ((S.trace(K)**2-S.trace(K*K))/2).subs(inverse)-(C*C-V*V-d*d-b*b))
check('quadric full sign reversal',
      (C*C-V*V-d*d-b*b).subs({C:-C,V:-V,d:-d,b:-b})-(C*C-V*V-d*d-b*b))

# J is a fixed Lie algebra automorphism; its naturality proof does not assume
# any Einstein evolution or horizontal rotational symmetry of K.
J=S.diag(-1,-1,1)
brackets={(0,1):S.Matrix([0,0,q]),(1,2):S.Matrix([p,0,0]),(2,0):S.Matrix([0,p,0])}
for (i,j),bracket in brackets.items():
    check(f'J bracket automorphism {i}{j}',J*bracket-J[i,i]*J[j,j]*bracket)
check('J invariance full horizontal-shear K',J.T*K.subs({v:0,w:0})*J-K.subs({v:0,w:0}))

# Original arbitrary homogeneous formal Pdot is not artificially symmetric.
check('mixed block index/metric identity',(own_Pd-own_Pd.T)[0,2]-2*v)
check('all allowed homogeneous first image zero',Q*own_Pd.subs({v:0,w:0})*P)
check('all allowed homogeneous full projector zero',own_Pd.subs({v:0,w:0}))

out={'all_pass':all(c['pass'] for c in checks),'checks':checks,
     'fixtures_recomputed':fixtures,'count':len(checks),
     'independence':'author tensors from uncommuted covariant derivatives; reviewer Ricci derivative from sealed differentiated Koszul curvature; common SymPy/brackets and projector identities disclosed',
     'limits':['comparison against author output occurred after source-first seal',
               'symbolic identities support bounded analytic proof, not a smooth constraint census',
               'J is only used to establish first-jet naturality here; no local development conclusion']}
print(json.dumps(out,indent=2,sort_keys=True))
raise SystemExit(0 if out['all_pass'] else 1)
