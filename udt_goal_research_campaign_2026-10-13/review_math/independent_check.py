"""Independent original-metric and first-integral checks; no producer imports."""
import functools, hashlib, json, platform
from pathlib import Path
import sympy as s
import mpmath as mp

out={'python':platform.python_version(),'sympy':s.__version__,'mpmath':mp.__version__,
     'kind':'exact geometry and arbitrary-precision quadrature diagnostic, not interval proof'}
t,r,th,ph=s.symbols('t r theta phi',real=True)
f=s.Function('f')(r)
coords=[t,r,th,ph]
g=s.diag(-f,1/f,r*r,r*r*s.sin(th)**2)
gi=g.inv()
@functools.lru_cache(None)
def conn(a,b,c):
    return s.simplify(sum(gi[a,d]*(s.diff(g[d,c],coords[b])+s.diff(g[d,b],coords[c])-s.diff(g[b,c],coords[d]))/2 for d in range(4)))
@functools.lru_cache(None)
def curvature(a,z,x,y):
    return s.simplify(s.diff(conn(a,y,z),coords[x])-s.diff(conn(a,x,z),coords[y])+sum(conn(a,x,b)*conn(b,y,z)-conn(a,y,b)*conn(b,x,z) for b in range(4)))
scale=[1/s.sqrt(f),s.sqrt(f),1/r,1/(r*s.sin(th))]
def orth_A(x,y,z,w):
    return s.simplify(g[w,w]*curvature(w,z,x,y)*scale[x]*scale[y]*scale[z]*scale[w])
indices=[(1,0,0,1),(2,0,0,2),(3,0,0,3),(1,2,2,1),(1,3,3,1),(2,3,3,2)]
vals=[orth_A(*q) for q in indices]
expected=[s.diff(f,r,2)/2,s.diff(f,r)/(2*r),s.diff(f,r)/(2*r),-s.diff(f,r)/(2*r),-s.diff(f,r)/(2*r),(1-f)/r**2]
assert all(s.simplify(a-b)==0 for a,b in zip(vals,expected))
out['original_metric_curvature']={str(q):str(v) for q,v in zip(indices,vals)}

# Assemble the independently computed six slots as an algebraic tensor.
def tensor_from_six(six):
    A={}
    for (a,b,c,d),v in zip(indices,six):
        for x,y,z,w,sign in [(a,b,c,d,1),(b,a,c,d,-1),(a,b,d,c,-1),(b,a,d,c,1),
                             (c,d,a,b,1),(d,c,a,b,-1),(c,d,b,a,-1),(d,c,b,a,1)]:
            A[x,y,z,w]=sign*v
    return A
def contract(A,x,y,z,w):
    return s.simplify(sum(v*x[a]*y[b]*z[c]*w[d] for (a,b,c,d),v in A.items()))
e=[s.eye(4)[:,i] for i in range(4)]
quartic=[s.simplify(v.subs(f,1-r**4).doit()) for v in vals]
A=tensor_from_six(quartic)
rad=[contract(A,e[i],e[0]+e[1],e[0]+e[1],e[i]) for i in [2,3]]
tan=[contract(A,e[i],e[0]+e[2],e[0]+e[2],e[i]) for i in [1,3]]
assert rad==[0,0] and tan==[-4*r*r,-r*r]
K=tensor_from_six([-4,-1,-1,1,1,4])
boost=s.Rational(5,4)*e[0]+s.Rational(3,4)*e[3]
bad=-contract(K,e[2],boost,boost,e[2])
assert bad==-s.Rational(11,16)
out['adverse_controls']={'quartic_radial_screen':list(map(str,rad)),
                         'quartic_tangential_screen':list(map(str,tan)),
                         'positive_unboosted_weyl_control_boosted_C':str(bad)}

# A reciprocal time-varying metric: direct connection and null Hessian.
q=s.Function('q')(t,r)
h=s.diag(-q,1/q)
hi=h.inv()
hc={}
for a in range(2):
 for b in range(2):
  for c in range(2):
   hc[a,b,c]=s.simplify(sum(hi[a,d]*(s.diff(h[d,c],coords[b])+s.diff(h[d,b],coords[c])-s.diff(h[b,c],coords[d]))/2 for d in range(2)))
hs=[]
for sign in [1,-1]:
 k=[1/s.sqrt(q),sign*s.sqrt(q)]
 hs.append(s.simplify(-sum(hc[1,b,c]*k[b]*k[c] for b in range(2) for c in range(2))))
assert hs==[s.diff(q,t)/q,-s.diff(q,t)/q]
out['NAR_dynamic_adverse_hessian']=list(map(str,hs))

def arrival_run(dps,hstep):
 mp.mp.dps=dps
 r0=mp.mpf(1)/4
 E=mp.sqrt(1-r0**4)
 def radius(v):return (r0**4+v*v)**(mp.mpf(1)/4)
 def rs(x):return mp.quad(lambda y:1/(1-y**4),[0,x])
 def emission(v):return -rs(r0)+mp.quad(lambda w:1/(2*radius(w)**3*(E+w)),[0,v])
 def proper(v):return mp.quad(lambda w:1/(2*radius(w)**3),[0,v])
 def root(em):return mp.findroot(lambda v:emission(v)-em,(mp.mpf('0.006'),mp.mpf('0.01')))
 h=mp.mpf(hstep)
 rows=[]
 for em in [-h,mp.mpf(0),h]:
  v=root(em); rr=radius(v); ts=em+rs(rr); tau=proper(v)
  rows.append({'emission':mp.nstr(em,32),'v':mp.nstr(v,32),'r':mp.nstr(rr,32),
               't':mp.nstr(ts,32),'tau':mp.nstr(tau,32),
               'return_t':mp.nstr(em+2*rs(rr),32),'incidence_residual':mp.nstr(emission(v)-em,8)})
 p=(mp.mpf(rows[2]['tau'])-mp.mpf(rows[0]['tau']))/(2*h)
 qret=(mp.mpf(rows[2]['return_t'])-mp.mpf(rows[0]['return_t']))/(mp.mpf(rows[2]['tau'])-mp.mpf(rows[0]['tau']))
 v0=root(0)
 pe=E+v0;qe=1/(E-v0)
 assert abs(p-pe)<mp.mpf('1e-8') and abs(qret-qe)<mp.mpf('1e-8')
 assert pe>1 and qe>1 and radius(v0)<1
 return {'dps':dps,'h':hstep,'rows':rows,'p_finite_difference':mp.nstr(p,32),
         'q_finite_difference':mp.nstr(qret,32),'p_endpoint':mp.nstr(pe,32),
         'q_endpoint':mp.nstr(qe,32),'p_error':mp.nstr(p-pe,8),'q_error':mp.nstr(qret-qe,8),
         'held_clock_p_same_radius':mp.nstr(mp.sqrt(1-radius(v0)**4),32)}
runs=[arrival_run(40,'0.00001'),arrival_run(60,'0.000002')]
out['independent_quadrature_arrival_runs']=runs
saved_path='udt_goal_research_campaign_2026-10-13/researcher_b/checks/arrival_01.stdout'
saved=json.loads(Path(saved_path).read_text())
last=saved['runs'][-1]
for name,key in [('p_endpoint','p_fd'),('q_endpoint','q_fd')]:
 assert abs(mp.mpf(runs[-1][name])-mp.mpf(str(last[key])))<mp.mpf('1e-10')
out['saved_arrival_sha256']=hashlib.sha256(Path(saved_path).read_bytes()).hexdigest()
out['saved_fd_differences']={a:mp.nstr(mp.mpf(runs[-1][a])-mp.mpf(str(last[b])),12) for a,b in [('p_endpoint','p_fd'),('q_endpoint','q_fd')]}
out['passed']=True
print(json.dumps(out,indent=2))
