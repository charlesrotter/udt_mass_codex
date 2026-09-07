"""Exposed comparison with independently reconstructed source-first tensors."""
import contextlib
import io
import itertools
import json
import pathlib
import runpy
import sympy as s

here=pathlib.Path(__file__).resolve().parent
with contextlib.redirect_stdout(io.StringIO()):
    data=runpy.run_path(str(here/'source_first_metric.py'))
    alg=runpy.run_path(str(here/'source_first_algebra.py'))
author=json.loads((here.parent/'author_corrected.stdout').read_text())
u,v,x,y,e,c=[data[q] for q in ('u','v','x','y','e','c')]
ids=range(4); slots=list(itertools.product(ids,repeat=4)); clean=lambda q:s.simplify(s.factor(q))
g=data['gc']; gi=data['gic']; Q={k:clean(z.subs(c,s.Rational(2,3))) for k,z in data['Q'].items()}
star=data['dual'](Q,gi)
B={(a,b,d,f):clean(sum(gi[h,k]*gi[m,n]*(Q[a,h,d,m]*Q[b,k,f,n]+star[a,h,d,m]*star[b,k,f,n]) for h,k,m,n in slots)) for a,b,d,f in slots}
checks={}
def check(name,condition):
    checks[name]=bool(condition)
    assert condition,name
locals={'u':u,'v':v,'x':x,'y':y,'epsilon':e}
saved={tuple(map(int,key.strip('()').split(','))):s.sympify(value,locals=locals) for key,value in author['B_exact_nonzero'].items()}
check('full256_saved_B',all(clean(B[k]-saved.get(k,0))==0 for k in slots))
check('ambient_root_obstruction',B[0,0,0,1]==2*e*e and B[0,0,1,1]==0)
check('all_obstruction_permutations',all(B[k]==2*e*e for k in set(itertools.permutations((0,0,0,1)))) and all(B[k]==0 for k in set(itertools.permutations((0,0,1,1)))))
check('nonzero_minor_all_points',clean(B[0,0,0,0]*B[0,0,1,1]-B[0,0,0,1]**2)==-4*e**4)
check('full_saved_gamma',data['gamma']==s.sympify(author['gamma'],locals=locals))
check('full_saved_S',clean(data['S']-s.sympify(author['S'],locals=locals))==0)
omega=(e*y,0,0,0)
check('all16_coordinate_recurrence',all(clean(data['Gamma'][a][d,1].subs(c,s.Rational(2,3))-s.KroneckerDelta(d,1)*omega[a])==0 for a,d in itertools.product(ids,repeat=2)))
check('active_recurrence_curvature',s.diff(omega[0],y)==e)
# An active nonzero curvature contraction verifies this is not a parallel line.
line_curv={(a,b,d):clean(Q[a,b,1,d]) for a,b,d in itertools.product(ids,repeat=3)}
check('coordinate_line_curvature_nonzero',any(z!=0 for z in line_curv.values()))
# General metric coefficient check directly from Levi-Civita again.
kappa=s.symbols('kappa',real=True); zg=(u,v,x,y)
gg=data['g'].copy();gg[0,0]+= (kappa+2)*e*v*y;gigin=gg.inv()
GG=[s.Matrix(4,4,lambda d,b:clean(sum(gigin[d,h]*(s.diff(gg[h,b],zg[a])+s.diff(gg[h,a],zg[b])-s.diff(gg[a,b],zg[h])) for h in ids)/2)) for a in ids]
RR={(a,b):(GG[b].diff(zg[a])-GG[a].diff(zg[b])+GG[a]*GG[b]-GG[b]*GG[a]).applyfunc(clean) for a,b in itertools.product(ids,repeat=2)}
ric=s.Matrix(4,4,lambda b,d:clean(sum(RR[a,b][a,d] for a in ids)))
target=s.zeros(4);target[0,0]=e**2*x**2*(-6*c-kappa+2);target[0,3]=target[3,0]=-(kappa+2)*e/2
check('general_c_kappa_Ricci', (ric-target).applyfunc(clean)==s.zeros(4))
check('omitted_completion_control_active',ric.subs({c:0,kappa:-2})[0,0]==4*e**2*x**2)
# Author saturation formula translated into the sealed reviewer's variables.
A,D,EE,F,FF,MM,NN,PP,QQ,RRR=alg['variables']
translation={'a':A,'b':EE,'cE':F,'d':D,'f':FF,'m':MM,'nM':PP,'p':QQ,'q':NN,'t':RRR}
check('saved_energy',s.expand(s.sympify(author['algebraic_B0000'],locals=translation)-alg['energy'])==0)
check('saved_flux',s.expand(s.sympify(author['algebraic_B0003'],locals=translation)-alg['flux'])==0)
check('saved_sum_of_squares',s.expand(s.sympify(author['sum_of_squares'],locals=translation)-alg['saturation'])==0)
# Changing the FIRST-dual term genuinely changes the general energy formula.
no_dual=sum(alg['eta'][h]*alg['eta'][k]*alg['Q'][0,h,0,k]**2 for h,k in itertools.product(ids,repeat=2))
check('dropped_dual_control_active',s.expand(no_dual-alg['energy'])!=0)
print(json.dumps(dict(status='PASS',checks=checks,full_tensor_slots=256,full64_algebraic_annihilation=alg['kernel'] is not None,general_Ricci=str(ric),root_minor=str(-4*e**4),line_curvature={str(k):str(z) for k,z in line_curv.items() if z!=0},independent_code='sealed reviewer source_first_metric.py and source_first_algebra.py; no author scientific imports'),indent=2))
