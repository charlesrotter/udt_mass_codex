import sympy as sp
t,r,th,ps=sp.symbols('t r theta psi',real=True)
xi,kap=sp.symbols('xi kappa',positive=True)
coords=[t,r,th,ps]
a=sp.Function('a')(r,th); b=sp.Function('b')(r,th); c=sp.Function('c')(r,th); d=sp.Function('d')(r,th); Th=sp.Function('Theta')(r,th)
glow=[-sp.exp(2*a),sp.exp(2*b),sp.exp(2*c)*r**2,sp.exp(2*d)*r**2*sp.sin(th)**2]
g=sp.diag(*glow); ginv=g.inv()
sT,cT=sp.sin(Th),sp.cos(Th); sth=sp.sin(th)
nA=[cT,sT*sth*sp.cos(ps),sT*sth*sp.sin(ps),sT*sp.cos(th)]
def dmu(e,mu): return sp.diff(e,coords[mu])
Gmn=sp.zeros(4,4)
for m in range(4):
 for n in range(4):
  Gmn[m,n]=sum(dmu(nA[A],m)*dmu(nA[A],n) for A in range(4))
L2=-(xi/2)*sum(ginv[i,j]*Gmn[i,j] for i in range(4) for j in range(4))
SS2=lambda A,nn,B,q: Gmn[A,B]*Gmn[nn,q]-Gmn[A,q]*Gmn[nn,B]
L4=-(kap/4)*sum(ginv[m,pp]*ginv[n,q]*SS2(m,n,pp,q) for m in range(4) for n in range(4) for pp in range(4) for q in range(4))
L=L2+L4
rootg=sp.exp(a+b+c+d)*r**2*sth
lag=rootg*L
EL=(sp.diff(sp.diff(lag,sp.diff(Th,r)),r)+sp.diff(sp.diff(lag,sp.diff(Th,th)),th)-sp.diff(lag,Th))/rootg
EL=EL.subs(ps,0)            # psi-independent physical scalar
EL=sp.simplify(EL)
subs={}
for f,nm in [(a,'a'),(b,'b'),(c,'c'),(d,'d'),(Th,'Th')]:
    subs[sp.diff(f,r,2)]=sp.Symbol(nm+'_rr'); subs[sp.diff(f,th,2)]=sp.Symbol(nm+'_tt')
    subs[sp.diff(f,r,th)]=sp.Symbol(nm+'_rt'); subs[sp.diff(f,r)]=sp.Symbol(nm+'_r')
    subs[sp.diff(f,th)]=sp.Symbol(nm+'_t'); subs[f]=sp.Symbol(nm)
ELx=EL.subs(subs,simultaneous=True)
syms=[r,th]
for nm in ['a','b','c','d','Th']:
    syms+=[sp.Symbol(nm),sp.Symbol(nm+'_r'),sp.Symbol(nm+'_t'),sp.Symbol(nm+'_rr'),sp.Symbol(nm+'_tt'),sp.Symbol(nm+'_rt')]
syms+=[xi,kap]
f=sp.lambdify(syms,ELx,'numpy')
# fallback: write source with numpy printer
from sympy.printing.numpy import NumPyPrinter
code="import numpy as np\nfrom numpy import exp,sin,cos,tan,sqrt\n\ndef matter_el_resid_CORRECT("+",".join(str(s) for s in syms)+"):\n    return "+NumPyPrinter().doprint(ELx)+"\n"
open('axisym_matter_el_CORRECT.py','w').write(code)
print("OK len",len(str(ELx)))
