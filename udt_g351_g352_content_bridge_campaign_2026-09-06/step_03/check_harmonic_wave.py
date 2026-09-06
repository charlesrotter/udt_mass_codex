"""Full local harmonic-wave checks; no physical count or adopted recipe.

Stdout only. Coordinates/numeric examples are in a supplied length unit.
Analytic integrability/naturality quantifiers require separate argument review.
"""
import sys
sys.dont_write_bytecode=True
import argparse,itertools,json,platform
import sympy as S
ap=argparse.ArgumentParser()
ap.add_argument('--mutation',choices=['drop_Hu_connection','drop_dual','force_closed',
                                    'inverse_metric_weight','gauge_linear_force'])
mutation=ap.parse_args().mutation
if not __debug__: raise RuntimeError('Assertions must remain enabled')
u,v,x,y=S.symbols('u v x y',real=True);coords=[u,v,x,y];idx=range(4)
H=S.Function('H')(u,x,y)
def metric(profile):
    return S.Matrix([[profile,-1,0,0],[-1,0,0,0],[0,0,1,0],[0,0,0,1]])
g=metric(H);gi=g.inv();groups=[]
def eq(name,a,b=0):
    if isinstance(a,S.MatrixBase):
        assert (a-b).applyfunc(S.simplify)==S.zeros(*a.shape),name
    else: assert S.simplify(a-b)==0,name
    groups.append(name)
G={}
for a,b,c in itertools.product(idx,repeat=3):
    z=S.simplify(sum(gi[a,d]*(S.diff(g[d,c],coords[b])+S.diff(g[d,b],coords[c])-S.diff(g[b,c],coords[d]))/2 for d in idx))
    if z!=0:G[a,b,c]=z
if mutation=='drop_Hu_connection':G[1,0,0]=S.Integer(0)
eq('variable_profile_connection',G.get((1,0,0),0),-S.diff(H,u)/2)
assert all(G.get((0,a,b),0)==0 for a,b in itertools.product(idx,repeat=2))
groups.append('full_du_parallel')
Rup={}
for a,b,c,d in itertools.product(idx,repeat=4):
    z=S.simplify(S.diff(G.get((a,d,b),0),coords[c])-S.diff(G.get((a,c,b),0),coords[d])+
        sum(G.get((a,c,e),0)*G.get((e,d,b),0)-G.get((a,d,e),0)*G.get((e,c,b),0) for e in idx))
    if z!=0:Rup[a,b,c,d]=z
Ric=S.Matrix(4,4,lambda b,d:sum(Rup.get((a,b,a,d),0) for a in idx))
expected=S.zeros(4);expected[0,0]=-(S.diff(H,x,2)+S.diff(H,y,2))/2
eq('full_Ricci_harmonic_criterion',Ric,expected)
R={}
for a,b,c,d in itertools.product(idx,repeat=4):
    z=S.simplify(sum(g[a,e]*Rup.get((e,b,c,d),0) for e in idx))
    if z!=0:R[a,b,c,d]=z
# Full curvature equals the Hessian block and its exact symmetries.
expected_R={}
for i,j in itertools.product([2,3],repeat=2):
    z=-S.diff(H,coords[i],coords[j])/2
    for key,sgn in [((0,i,0,j),1),((i,0,0,j),-1),((0,i,j,0),-1),((i,0,j,0),1)]:
        expected_R[key]=sgn*z
assert set(R)==set(expected_R)
assert all(S.simplify(R[k]-expected_R[k])==0 for k in R)
groups.append('all_lower_Riemann_components')
a,t=S.symbols('a t',real=True)
subs={S.diff(H,x,2):a,S.diff(H,x,y):t,S.diff(H,y,2):-a}
W={k:z.subs(subs) for k,z in R.items()}
raised_epsilon={}
for i,j,e,f in itertools.product(idx,repeat=4):
    z=S.simplify(sum(S.LeviCivita(i,j,m,n)*gi[m,e]*gi[n,f] for m,n in itertools.product(idx,repeat=2)))
    if z!=0:raised_epsilon[i,j,e,f]=z
D={}
for i,j,c,d in itertools.product(idx,repeat=4):
    z=S.simplify(sum(raised_epsilon.get((i,j,e,f),0)*W.get((e,f,c,d),0)/2 for e,f in itertools.product(idx,repeat=2)))
    if z!=0:D[i,j,c,d]=z
pairs=[(i,j,gi[i,j]) for i,j in itertools.product(idx,repeat=2) if gi[i,j]!=0]
B={}
for i,j,c,d in itertools.product(idx,repeat=4):
    z=S.simplify(sum(ef*mn*(W.get((i,e,c,m),0)*W.get((j,f,d,n),0)+
        (0 if mutation=='drop_dual' else D.get((i,e,c,m),0)*D.get((j,f,d,n),0)))
        for e,f,ef in pairs for m,n,mn in pairs))
    if z!=0:B[i,j,c,d]=z
assert set(B)=={(0,0,0,0)},'full_B_support'
groups.append('full_B_support')
eq('full_B_coefficient',B[0,0,0,0],a**2+t**2)

N=S.diff(H,x,2)**2+S.diff(H,x,y)**2
lap=S.diff(N,x,2)+S.diff(N,y,2)
harmonic_jets={S.diff(H,x,2,y,2):-S.diff(H,x,4),
               S.diff(H,x,y,3):-S.diff(H,x,3,y),
               S.diff(H,x,y,2):-S.diff(H,x,3)}
eq('harmonic_Hessian_norm_Bochner_identity',lap.subs(harmonic_jets),
   4*(S.diff(H,x,3)**2+S.diff(H,x,2,y)**2))

# Smooth nonzero cubic witness on a patch away from x=y=0.
Hc=x**3-3*x*y**2; r2=x*x+y*y
bc=S.sqrt(6)*r2**S.Rational(1,4)
betac=S.Matrix([-bc,0,0,0]); gc=metric(Hc);gic=gc.inv()
alpha=S.Matrix([0,0,x/(2*r2),y/(2*r2)])
nabla=S.Matrix(4,4,lambda i,j:S.diff(betac[j],coords[i])) # Gamma^u_ab=0 proved above.
eq('cubic_full_recurrence',nabla,alpha*betac.T)
dBeta=S.Matrix(4,4,lambda i,j:S.diff(betac[j],coords[i])-S.diff(betac[i],coords[j]))
if mutation=='force_closed':dBeta=S.zeros(4)
eq('cubic_nonclosure_guard',dBeta[0,2],bc*x/(2*r2))
qscalar=(alpha.T*gic*alpha)[0]
eq('cubic_positive_conversion',qscalar,1/(4*r2))
eq('root_current_conserved',S.diff(bc,v))
eq('converted_current_conserved',S.diff(qscalar*bc,v))
h=S.symbols('h',positive=True)
scaled_q=qscalar if mutation=='inverse_metric_weight' else (alpha.T*(h**2*gc).inv()*alpha)[0]
eq('conversion_homothety_weight',scaled_q,h**-2*qscalar)

# Nonconstant but phase-compatible quadratic witness, u>-1.
bw=S.sqrt(2)*(1+u);Hw=(1+u)**2*(x*x-y*y)
eq('variable_quadratic_root',bw**4,(S.diff(Hw,x,2)**2+S.diff(Hw,x,y)**2))
eq('variable_quadratic_primitive',S.diff(-S.sqrt(2)*(u+u*u/2),u),-bw)
eq('variable_quadratic_not_parallel',S.diff(bw,u),S.sqrt(2))

# Remove general linear/constant terms without changing du or transverse Hessian.
m,n,l1,l2,c,s1,s2,z1,z2=S.symbols('m n l1 l2 c s1 s2 z1 z2',real=True)
M=S.Matrix([[m,n],[n,-m]]);s=S.Matrix([s1,s2]);z=S.Matrix([z1,z2]);ell=S.Matrix([l1,l2]);X=S.Matrix([x,y])
ss=M*s+(S.zeros(2,1) if mutation=='gauge_linear_force' else ell/2)
hp=(ell.dot(s))/4+c/2
J=S.Matrix([[1,0,0,0],[ss.dot(X)+(z.dot(z)+s.dot(ss))/2+hp,1,z1,z2],
            [z1,0,1,0],[z2,0,0,1]])
oldH=((X+s).T*M*(X+s))[0]+ell.dot(X+s)+c
eq('full_linear_term_gauge_removal',J.T*metric(oldH)*J,metric((X.T*M*X)[0]))
eq('gauge_du_preserved',J.T*S.Matrix([1,0,0,0]),S.Matrix([1,0,0,0]))
Dh=S.diag(1,h**2,h,h)
eq('variable_centered_wave_homothety',Dh.T*metric(((h*X).T*M*(h*X))[0])*Dh,h**2*metric((X.T*M*X)[0]))
point={x:S.Integer(1),y:S.Integer(2)}
print(json.dumps({'kind':'exact algebra and finite controls; not physical content identification',
 'python':platform.python_version(),'sympy':S.__version__,'mutation':mutation,
 'passed_groups':groups,'group_count':len(groups),'metric_shape':[4,4],
 'generic_B_uuuu':str(B[0,0,0,0]),'Ricci_uu':str(Ric[0,0]),
 'cubic_point':{'x':'1','y':'2','root_magnitude':str(bc.subs(point)),
 'alpha':[str(z.subs(point)) for z in alpha], 'q':str(qscalar.subs(point)),
 'dBeta_ux':str(dBeta[0,2].subs(point)),'dBeta_uy':str(dBeta[0,3].subs(point))},
 'variable_quadratic':{'domain':'u>-1 in supplied length units','root':str(bw),
 'primitive':str(-S.sqrt(2)*(u+u*u/2)),'root_derivative':str(S.diff(bw,u))}},indent=2))
