"""Reuse frozen tensor functions; preserve source-code/result exposure honestly."""
from pathlib import Path
import sympy as s,json,sys,hashlib,platform
p=Path(__file__).resolve().parent
source=p/'check_candidate.py';text=source.read_text()
# Import only unchanged utility definitions, not parent top-level experiment.
part=text[text.index('def conn_ric'):text.index("u,v,x,y=s.symbols")]
ns={'s':s};exec(compile(part,str(source), 'exec'),ns)
t=s.symbols('t',positive=True);xi,y,z=s.symbols('xi y z',real=True);c=(t,xi,y,z)
g=s.diag(-s.exp(2*t),s.exp(2*t),t,t);K=s.Matrix([0,0,1,0]);C,R=ns['conn_ric'](g,c);F=ns['exterior'](g*K,c)
scalar=s.simplify(s.trace(g.inv()*R));Fup=g.inv()*F*g.inv()
rows=[]
def equal(name,a,b):
 v=a-b;v=list(v) if isinstance(v,s.MatrixBase) else [v];res=[s.simplify(x) for x in v];rows.append({'name':name,'pass':all(x==0 for x in res),'residuals':list(map(str,res))})
equal('full_Ricci',R,s.diag(1/t+1/(2*t*t),1/t,0,0));equal('scalar',scalar,-s.exp(-2*t)/(2*t*t));equal('Killing',ns['lie'](g,K,c),s.zeros(4));equal('Ric_K',R*K,s.zeros(4,1));equal('closed',s.Matrix(ns['closed'](F,c)),s.zeros(4,1));equal('original_divergence',ns['densdiv'](g,F,c,s.exp(2*t)*t),s.zeros(4,1));equal('invariant',sum(F[a,b]*Fup[a,b] for a in range(4) for b in range(4)),-2*s.exp(-2*t)/t)
# Nonzero values at a declared exact point suffice to refute an all-zero tensor claim.
rows.append({'name':'non_Einstein_at_t1','pass':s.simplify((R-scalar*g/4)[2,2].subs(t,1))!=0,'value':str(s.simplify((R-scalar*g/4)[2,2].subs(t,1)))})
r={'kind':'post-freeze exact supplied non-Einstein control; same-code utility reuse, not independent verification','python':platform.python_version(),'sympy':s.__version__,'utility_source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'Ricci':str(R),'scalar':str(scalar),'checks':rows,'passed':sum(x['pass'] for x in rows),'count':len(rows),'all_pass':all(x['pass'] for x in rows)}
Path(sys.argv[1]).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'passed':r['passed'],'count':r['count'],'all_pass':r['all_pass']}));sys.exit(0 if r['all_pass'] else 1)
