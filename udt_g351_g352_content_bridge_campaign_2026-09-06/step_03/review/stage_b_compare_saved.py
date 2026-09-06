"""Read-only independent comparator; outputs JSON to stdout, never edits archives."""
import argparse, contextlib, io, itertools, json, pathlib, runpy, sympy as s
p=argparse.ArgumentParser()
p.add_argument('--repo',type=pathlib.Path,required=True)
p.add_argument('--author-tensors',type=pathlib.Path,required=True)
a=p.parse_args(); repo=a.repo.resolve()
here=pathlib.Path(__file__).resolve().parent
out=io.StringIO()
with contextlib.redirect_stdout(out): ns=runpy.run_path(str(here/'stage_a_independent.py'))
saved=json.loads((repo/'udt_g351_g352_content_bridge_campaign_2026-09-06/step_03/AUTHOR_RESULT.json').read_text())
captured=json.loads(a.author_tensors.read_text())
u,v,x,y=ns['coords']; coords=ns['coords']; H=ns['H']
decode={'u':u,'v':v,'x':x,'y':y,'H':s.Function('H'),'a':ns['aa'],'b':ns['bb'],'t':ns['bb']}
parse=lambda text:s.sympify(text,locals=decode)
compared={}
for author_name,own_name,rank in [('Gamma','Gamma',3),('R','R',4),('W','W',4),('starW','star',4),('B','B',4)]:
    actual=ns[own_name]; expected=captured[author_name]
    allkeys=list(itertools.product(range(4),repeat=rank))
    assert set(expected)<=set(''.join(map(str,k)) for k in allkeys)
    for k in allkeys:
        assert s.simplify(actual[k]-parse(expected.get(''.join(map(str,k)),'0')))==0,(author_name,k)
    compared[author_name]={'positions':len(allkeys),'nonzero':sum(z!=0 for z in actual.values())}
for i,j in itertools.product(range(4),repeat=2):
    assert s.simplify(ns['Ric'][i,j]-parse(captured['Ricci'][i][j]))==0
assert s.simplify(ns['B'][0,0,0,0]-parse(saved['generic_B_uuuu']))==0
assert s.simplify(ns['Ric'][0,0]-parse(saved['Ricci_uu']))==0
# Use AUTHOR cubic coefficient 1, not Stage A's coefficient 1/3. The computed
# generic curvature and B tensors supply its root coefficient at every point.
Hc=x**3-3*x*y**2
Hxx=s.diff(Hc,x,2); Hxy=s.diff(Hc,x,y)
Sc=ns['B'][0,0,0,0].subs({ns['aa']:Hxx,ns['bb']:Hxy})
point={x:parse(saved['cubic_point']['x']),y:parse(saved['cubic_point']['y'])}
rho_point=s.real_root(Sc.subs(point),4)
alpha=s.Matrix([s.diff(Sc,z)/(4*Sc) for z in coords])
gc=ns['g'].subs(H,Hc); qc=s.factor((alpha.T*gc.inv()*alpha)[0])
assert s.simplify(rho_point-parse(saved['cubic_point']['root_magnitude']))==0
assert all(s.simplify(alpha[i].subs(point)-parse(saved['cubic_point']['alpha'][i]))==0 for i in range(4))
assert s.simplify(qc.subs(point)-parse(saved['cubic_point']['q']))==0
assert s.simplify(rho_point*alpha[2].subs(point)-parse(saved['cubic_point']['dBeta_ux']))==0
assert s.simplify(rho_point*alpha[3].subs(point)-parse(saved['cubic_point']['dBeta_uy']))==0
assert s.simplify(Sc-36*(x*x+y*y))==0
assert s.simplify(qc-1/(4*(x*x+y*y)))==0
wv=saved['variable_quadratic']; rv=parse(wv['root']); theta=parse(wv['primitive'])
Sv=ns['B'][0,0,0,0].subs({ns['aa']:s.diff(ns['Hv'],x,2),ns['bb']:s.diff(ns['Hv'],x,y)})
assert s.simplify(rv**4-Sv)==0
assert s.simplify(s.diff(theta,u)+rv)==0
assert s.simplify(s.diff(rv,u)-parse(wv['root_derivative']))==0
assert wv['domain']=='u>-1 in supplied length units'
# Distinct direct differentiation of the author's gauge map; no manually
# asserted Jacobian is imported into this computation.
m=s.Function('m')(u); n=s.Function('n')(u)
p1=s.Function('p1')(u); p2=s.Function('p2')(u); zeta=s.Function('zeta')(u)
l1=s.Function('l1')(u); l2=s.Function('l2')(u); c=s.Function('c')(u)
z=s.Matrix([x,y]); pp=s.Matrix([p1,p2]); dp=pp.diff(u)
M=s.Matrix([[m,n],[n,-m]]); ll=s.Matrix([l1,l2])
mapping=s.Matrix([u,v+dp.dot(z)+pp.dot(dp)/2+zeta,x+p1,y+p2])
J=mapping.jacobian(coords)
odes={s.diff(p1,u,2):(M*pp+ll/2)[0],s.diff(p2,u,2):(M*pp+ll/2)[1],
      s.diff(zeta,u):ll.dot(pp)/4+c/2}
oldH=((z+pp).T*M*(z+pp))[0]+ll.dot(z+pp)+c
target=ns['g'].subs(H,(z.T*M*z)[0])
pulled=(J.T*ns['g'].subs(H,oldH)*J).subs(odes)
assert all(s.simplify(z)==0 for z in pulled-target)
rho_u=s.Function('r')(u); bvec=s.Matrix([-rho_u,0,0,0])
assert J.T*bvec==bvec
assert s.simplify(J.det()-1)==0
assert captured['candidate_stdout']==saved
print(json.dumps(dict(status='PASS',independence='Frozen source-first reviewer implementation; no author module imported',
 full_array_comparisons=compared,ricci_positions=16,saved_scalar_fields='All displayed metric/root/alpha/q/dBeta/variable-profile values match',
 cubic={'coefficient':'1','S':str(s.factor(Sc)),'point':[str(point[x]),str(point[y])],
        'root':str(s.simplify(rho_point)),'alpha':[str(s.simplify(z.subs(point))) for z in alpha],
        'q':str(qc.subs(point))},gauge='All 16 differentiated-map metric entries, all 4 beta entries, det=1',
 stage_a_baseline=json.loads(out.getvalue())['checks']),indent=2))
