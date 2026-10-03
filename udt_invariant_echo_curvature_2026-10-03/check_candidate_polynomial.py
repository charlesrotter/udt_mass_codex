"""Exact word replay and original geometric controls, no science module imports."""
from pathlib import Path
from fractions import Fraction
from math import factorial
import sympy as S,json,time,platform
B=Path(__file__).resolve().parent;start=time.monotonic()
x,y,L,e=S.symbols('x y L e',real=True);cand=json.loads((B/'UNIVERSAL_FORMAL_RESULT.json').read_text())
# Free associative polynomials in two letters with commuting coefficients.
def prod(a,b,limit=7):
 out={}
 for w,v in a.items():
  for z,q in b.items():
   if len(w+z)<=limit:out[w+z]=out.get(w+z,0)+v*q
 return {w:S.expand(v) for w,v in out.items() if S.expand(v)!=0}
def summ(a,b,c=1):
 out=a.copy()
 for w,v in b.items():out[w]=out.get(w,0)+c*v
 return {w:S.expand(v) for w,v in out.items() if S.expand(v)!=0}
def comm(a,b):return summ(prod(a,b),prod(b,a),-1)
def exponential(letter,c):return {letter*i:c**i/S.factorial(i) for i in range(8)}
P={'':S.Integer(1)}
for letter,c in [('u',-x),('n',1),('u',2*y),('n',1),('u',-x)]:P=prod(P,exponential(letter,c))
H=summ(P,{'':1},-1);power={'':1};log={}
for degree in range(1,8):
 power=prod(power,H);log=summ(log,power,S.Rational((-1)**(degree+1),degree))
rebuild={}
for degree,m in cand['Z'].items():
 for key,val in m.items():
  if int(degree)==1:word=key
  else:word='un'+('u' if key[0]=='A' else 'n')+key[1:]
  term={word[0]:1}
  for letter in word[1:]:term=comm(term,{letter:1})
  coeff=2*S.sympify(val,locals={'x':x,'y':y})
  rebuild=summ(rebuild,term,coeff)
assert not summ(rebuild,log,-1)
checks={'free_associative_degree7_identity':True};cases=[]
print('PASS free associative degree7 identity',flush=True)
# Series roots and implicit derivatives from ORIGINAL metric incidence polynomial.
def tmul(a,b):
 return [S.expand(sum(a[j]*b[i-j] for j in range(i+1))) for i in range(4)]
def tinv(a):
 assert a[0]!=0
 b=[1/a[0],S.Integer(0),S.Integer(0),S.Integer(0)]
 for i in range(1,4):b[i]=-sum(a[j]*b[i-j] for j in range(1,i+1))/a[0]
 assert tmul(a,b)==[1,0,0,0]
 return b
def tlog(a):
 assert a[0]==1
 h=[0,*a[1:]];h2=tmul(h,h);h3=tmul(h2,h)
 return [h[i]-h2[i]/2+h3[i]/3 for i in range(4)]
def evalpoly(P,xx,yy):
 powers=[]
 for vals,maxdeg in [(xx,P.degree(x)),(yy,P.degree(y))]:
  pp=[[S.Integer(1),S.Integer(0),S.Integer(0),S.Integer(0)]]
  for j in range(max(0,int(maxdeg))):pp.append(tmul(pp[-1],vals))
  powers.append(pp)
 out=[S.Integer(0)]*4
 for (i,j,k),c in P.terms():
  if k>=4:continue
  prod=tmul(powers[0][i],powers[1][j])
  for z in range(4-k):out[z+k]+=c*prod[z]
 return [S.expand(v) for v in out]
def clocks(F):
 P=S.Poly(F,x,y,e);Px=S.Poly(S.diff(F,x),x,y,e);Py=S.Poly(S.diff(F,y),x,y,e)
 origin=[S.Integer(0)]*4;yy=[S.Integer(1),0,0,0];xx=[S.Integer(2),0,0,0]
 fy0=evalpoly(Py,origin,yy)[0]
 for j in range(1,4):yy[j]=-evalpoly(P,origin,yy)[j]/fy0
 fx0=evalpoly(Px,xx,yy)[0]
 for j in range(1,4):xx[j]=-evalpoly(P,xx,yy)[j]/fx0
 assert evalpoly(P,origin,yy)==[0]*4 and evalpoly(P,xx,yy)==[0]*4
 ps=[-v for v in tmul(evalpoly(Px,origin,yy),tinv(evalpoly(Py,origin,yy)))]
 qs=[-v for v in tmul(evalpoly(Py,xx,yy),tinv(evalpoly(Px,xx,yy)))]
 pp=tmul(ps,ps);den=[2-pp[0],*[-v for v in pp[1:]]]
 lq,lp,ld=tlog(qs),tlog(ps),tlog(den)
 D=[S.factor(lq[i]-lp[i]+ld[i]) for i in range(4)]
 expr=lambda vals:sum(v*e**i for i,v in enumerate(vals))
 return {'D4':D[2],'D6':D[3],'p':expr(ps),'q':expr(qs),'first':expr(yy),'return':expr(xx),'D2':D[1]}
def invariants(g,R,U,n):
 dot=lambda v,w:(v.T*g*w)[0]
 assert dot(U,U)==-1 and dot(n,n)==1 and dot(U,n)==0
 A=R(n,U,U);BB=R(n,U,n);T=dot(A,n);aa=dot(A,A);ab=dot(A,BB);bb=dot(BB,BB)
 pairs=[(A,U),(A,n),(BB,U),(BB,n)]
 K={(i,j):dot(R(*pairs[i],pairs[j][0]),pairs[j][1]) for i in range(4) for j in range(4)}
 assert all(S.simplify(K[1,j]-K[2,j])==0 for j in range(4))
 D4=2*aa+ab-2*T**2
 D6=(120*K[0,0]+108*K[0,1]-120*K[0,3]+90*K[1,1]-27*K[1,3]+60*T**3+120*T*aa-236*T*ab-60*T*bb)/180
 V=A-T*n;W=BB-T*U
 return dict(T=T,V2=dot(V,V),W2=dot(W,W),VW=dot(V,W),D4=S.factor(D4),D6=S.factor(D6))
def record(name,F,g,R,U,n):
 print('START '+name,flush=True)
 got=clocks(F);inv=invariants(g,R,U,n)
 assert got['D2']==0 and got['D4']==inv['D4'] and got['D6']==inv['D6'],(name,got,inv)
 assert S.simplify(got['p'].coeff(e,1)+inv['T']/2)==0
 assert S.simplify(got['q'].coeff(e,1)+3*inv['T']/2)==0
 if inv['V2']==0:assert S.simplify(inv['D6']-inv['T']*inv['W2']/3)==0
 print('PASS '+name,flush=True)
 cases.append({'name':name,'invariants':{k:str(v) for k,v in inv.items()},'original_clocks':{k:str(v) for k,v in got.items()},'exact_match':True})
G=S.diag(-1,1,1,1);zero=S.zeros(4,1)
def basis(j):return S.eye(4)[:,j]
def product_case(name,indices,k,U,n):
 # Original constant-curvature quadric in m+1 dimensions, flat complement.
 m=len(indices);J=S.diag(*[G[i,i] for i in indices],S.Rational(1,k));o=S.zeros(m+1,1);o[-1]=1
 def ext(v):return S.Matrix([v[i] for i in indices]+[0])
 def gen(v):v=ext(v);return k*(v*(o.T*J)-o*(v.T*J))
 Pu=gen(U);Pn=gen(n)
 assert Pu.T*J+J*Pu==S.zeros(m+1) and Pn.T*J+J*Pn==S.zeros(m+1)
 av=[Pu**j*o*x**j/S.factorial(j) for j in range(9)]
 bv=[sum((Pn**i*Pu**(j-i)*o*y**(j-i)/(S.factorial(i)*S.factorial(j-i)) for i in range(j+1)),S.zeros(m+1,1)) for j in range(9)]
 flat=[i for i in range(4) if i not in indices]
 flatnorm=sum(G[i,i]*(n[i]+(y-x)*U[i])**2 for i in flat)
 coeff={j:S.expand(k*sum((av[a].T*J*bv[j-a])[0] for a in range(j+1))-(k**(j//2)*flatnorm**(j//2)/S.factorial(j) if j%2==0 else 0)) for j in range(9)}
 assert coeff[0]==0 and all(coeff[j]==0 for j in [1,3,5,7])
 F=sum(coeff[2*j+2]*e**j for j in range(4))
 def R(a,b,c):
  va=S.Matrix([a[i] if i in indices else 0 for i in range(4)]);vb=S.Matrix([b[i] if i in indices else 0 for i in range(4)]);vc=S.Matrix([c[i] if i in indices else 0 for i in range(4)])
  return k*((vb.T*G*vc)[0]*va-(va.T*G*vc)[0]*vb)
 record(name,F,G,R,U,n)
# Families2-4: signed space form, Lorentz2 product, spatial2 product.
gam=S.Rational(13,12);u=S.Rational(5,12);aa=S.Rational(5,13);bb=S.Rational(12,13)
for k in [1,-1]:
 U=gam*basis(0)+u*basis(2);m=u*basis(0)+gam*basis(2)
 product_case('spaceform_'+str(k),[0,1,2,3],k,U,aa*m+bb*basis(1))
 for tilt in [S.Integer(0),aa,-aa]:
  lateral=S.Integer(1) if tilt==0 else bb
  product_case('lorentz2_'+str(k)+'_'+str(tilt),[0,1],k,U,tilt*m+lateral*basis(1))
 U=gam*basis(0)+u*basis(1);m=u*basis(0)+gam*basis(1)
 product_case('spatial2_'+str(k),[1,2],k,U,aa*m+bb*basis(2))
record('flat',1-(y-x)**2,G,lambda a,b,c:zero,basis(0),basis(1))
# Family5: constant-profile plane wave, g=2du dv+sum lambda_i x_i²du²+dx²+dy².
# Original geodesics u=b, xi=L ni cosh(sqrt(lambda_i)b),
# v=-b/2 -sum xi xi'/2. Original null action multiplied by Delta u gives F.
Gp=S.Matrix([[0,1,0,0],[1,0,0,0],[0,0,1,0],[0,0,0,1]])
lam=[S.Integer(1),S.Integer(-2)];Up=S.Matrix([1,S.Rational(-1,2),0,0])
def Rp(a,b,c):
 cov=S.zeros(4,1)
 for i in range(2):
  j=i+2;v=lam[i]*(a[j]*b[0]-a[0]*b[j])
  cov[0]+=v*c[j];cov[j]-=v*c[0]
 return Gp.inv()*cov
for ns in [(S.Integer(1),S.Integer(0)),(S.Rational(3,5),S.Rational(4,5))]:
 d=y-x;F=-L**2*d**2
 for h,nj in zip(lam,ns):
  xb=L*nj*sum(h**j*(L*y)**(2*j)/S.factorial(2*j) for j in range(4))
  xp=L*nj*sum(h**(j+1)*(L*y)**(2*j+1)/S.factorial(2*j+1) for j in range(4))
  coth=1+h*(L*d)**2/3-h**2*(L*d)**4/45+2*h**3*(L*d)**6/945
  F+=coth*xb**2-L*d*xb*xp
 expanded=S.Poly(S.expand(F),L)
 FF=sum(expanded.coeff_monomial(L**(2*j+2))*e**j for j in range(4))
 record('plane_wave_'+str(ns),FF,Gp,Rp,Up,S.Matrix([0,0,*ns]))
# Original plane-wave Christoffel-derived R components/parallelness validation.
z0,z1,z2,z3=S.symbols('u v X Y');coords=[z0,z1,z2,z3]
g=S.Matrix([[z2**2-2*z3**2,1,0,0],[1,0,0,0],[0,0,1,0],[0,0,0,1]]);gi=g.inv()
Gamma={(a,b,c):S.simplify(sum(gi[a,d]*(S.diff(g[d,c],coords[b])+S.diff(g[d,b],coords[c])-S.diff(g[b,c],coords[d]))/2 for d in range(4))) for a in range(4) for b in range(4) for c in range(4)}
# R[a,b,c,d] lowers output: g(R(e_a,e_b)e_c,e_d).
R4={}
for a in range(4):
 for b in range(4):
  for c in range(4):
   rout=S.Matrix([S.simplify(S.diff(Gamma[r,b,c],coords[a])-S.diff(Gamma[r,a,c],coords[b])+sum(Gamma[r,a,j]*Gamma[j,b,c]-Gamma[r,b,j]*Gamma[j,a,c] for j in range(4))) for r in range(4)])
   for d in range(4):R4[a,b,c,d]=S.simplify((rout.T*g*basis(d))[0])
for a in range(4):
 for b in range(4):
  for c in range(4):
   for d in range(4):
    assert S.simplify(R4[a,b,c,d]-(Rp(basis(a),basis(b),basis(c)).T*Gp*basis(d))[0])==0
    for m in range(4):
     cov=S.diff(R4[a,b,c,d],coords[m])-sum(Gamma[j,m,a]*R4[j,b,c,d]+Gamma[j,m,b]*R4[a,j,c,d]+Gamma[j,m,c]*R4[a,b,j,d]+Gamma[j,m,d]*R4[a,b,c,j] for j in range(4))
     assert S.simplify(cov)==0
checks.update({'truncated_ring_root_and_inverse_identities':True,'original_plane_wave_R_and_nablaR':True,'all_original_metric_clock_coefficients':True,'PSW_leading_coefficients':True,'V0_corollary':True})
out={'status':'PASS','python':platform.python_version(),'sympy':S.__version__,'duration_seconds':time.monotonic()-start,'families':5,'exact_cases':len(cases),'optional_numeric_cases':0,'checks':checks,'cases':cases,'limit':'Exact symbolic identities and supplied original metric controls; no fitted invariant, generic finite-distance certificate or physical law.'}
(B/'PARENT_POLYNOMIAL_CHECK_RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='cases'}))
