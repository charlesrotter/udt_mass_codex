import sympy as sp
r=sp.symbols('r',positive=True); th=sp.symbols('theta')
xi,kap=sp.symbols('xi kappa',positive=True)
a=sp.Function('a')(r); b=sp.Function('b')(r); Th=sp.Function('Theta')(r)
# correct EL (round) solved for rhs:
ap,bp,Thp,Thpp,B=sp.symbols('ap bp Thp Thpp B'); ThS=sp.symbols('ThS')
s=sp.sin(ThS)
num=(-2*kap*r**2*s**2*Thp*ap+2*kap*r**2*s**2*Thp*bp-kap*r**2*sp.sin(2*ThS)*Thp**2
     +2*kap*B*s**3*sp.cos(ThS)-r**4*xi*Thp*ap+r**4*xi*Thp*bp-2*r**3*xi*Thp+r**2*xi*B*sp.sin(2*ThS))
den=r**2*(2*kap*s**2+r**2*xi)
rhs_correct=num/den
# committed axisym EL (round, theta-indep, c=d=0) via sympy exec, solve for Thpp
src=open('axisym_matter_el.py').read()
src='\n'.join(l for l in src.split('\n') if not l.strip().startswith('import numpy') and not l.strip().startswith('from numpy'))
ns={'np':sp,'exp':sp.exp,'sin':sp.sin,'cos':sp.cos,'sqrt':sp.sqrt,'tan':sp.tan}
exec(src,ns); EL=ns['matter_el_resid']
Z=sp.Integer(0)
# use symbols; set exp(2b)=B by substituting b such that... easier: keep b symbol, then sub exp(2*b)->B
bb=sp.symbols('bb'); aa=sp.symbols('aa')
e=EL(r,th, aa,bb,Z,Z,ThS, ap,bp,Z,Z,Thp, Z,Z,Z,Z,Z, sp.symbols('app'),sp.symbols('bpp'),Z,Z,Thpp, Z,Z,Z,Z,Z, Z,Z,Z,Z,Z, xi,kap)
e=e.subs(sp.exp(2*bb),B).subs(sp.exp(-2*bb),1/B)
# committed EL has overall exp(-2b) factor etc; solve for Thpp
solc=sp.solve(e,Thpp)
rhs_comm=sp.simplify(solc[0])
print("committed-axisym rhs - correct rhs (round) =")
print(sp.simplify(rhs_comm-rhs_correct))
df=sp.simplify(sp.nsimplify(rhs_comm-rhs_correct, rational=True))
print("\nAfter nsimplify (float->rational):", df)
# numeric spot check
import numpy as np
f1=sp.lambdify((r,B,ThS,Thp,ap,bp), rhs_comm,'numpy')
f2=sp.lambdify((r,B,ThS,Thp,ap,bp), rhs_correct,'numpy')
rng=np.random.default_rng(1)
mx=0
for _ in range(20):
    v=[rng.uniform(0.5,4),rng.uniform(0.3,3),rng.uniform(0.2,3),rng.uniform(-.5,.5),rng.uniform(-.5,.5),rng.uniform(-.5,.5)]
    mx=max(mx,abs(float(f1(*v))-float(f2(*v))))
print("max |committed - correct| over 20 random round pts:", mx)
