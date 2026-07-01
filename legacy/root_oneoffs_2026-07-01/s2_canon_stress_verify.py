import sympy as sp
r,th,ps = sp.symbols('r theta psi', positive=True)
xi,kap,m = sp.symbols('xi kappa m', positive=True)
A=sp.Function('A')(r); B=sp.Function('B')(r)
sth=sp.sin(th)
# round diagonal metric (areal), A=B=0 case checked numerically; keep general A,B here
g=sp.diag(-sp.exp(2*A),sp.exp(2*B),r**2,r**2*sth**2)
# CANON unit S^2 hedgehog n = x/r  (degree-1, f(theta)=theta)
n=sp.Matrix([sth*sp.cos(m*ps), sth*sp.sin(m*ps), sp.cos(th)])
print("|n|^2-1 =", sp.simplify(n.dot(n)-1))
dn=[sp.zeros(3,1) for _ in range(4)]
for a in range(3):
    dn[1][a]=sp.diff(n[a],r); dn[2][a]=sp.diff(n[a],th); dn[3][a]=sp.diff(n[a],ps)
Gf=sp.zeros(4,4)
for mu in range(4):
    for nu in range(4):
        Gf[mu,nu]=sp.simplify(dn[mu].dot(dn[nu]))
gI=sp.symbols('gItt gIrr gIth gIps'); gd=sp.diag(*gI)
def cross(u,v): return sp.Matrix([u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]])
S=[[cross(dn[a],dn[b]) for b in range(4)] for a in range(4)]
L2=-(xi/2)*sum(gd[i,i]*Gf[i,i] for i in range(4))
L4=-(kap/4)*sum(gd[i,i]*gd[j,j]*S[i][j].dot(S[i][j]) for i in range(4) for j in range(4))
L=L2+L4
glow=[-sp.exp(2*A),sp.exp(2*B),r**2,r**2*sth**2]
subs={gI[0]:-sp.exp(-2*A),gI[1]:sp.exp(-2*B),gI[2]:1/r**2,gI[3]:1/(r**2*sth**2)}
names=['t','r','th','ps']; Tmix={}
for i in range(4):
    Tii=-2*sp.diff(L,gI[i])+glow[i]*L
    Tmix[names[i]]=sp.simplify((sp.diag(*[subs[gI[k]] for k in range(4)])[i,i])*Tii.subs(subs))
print("rho=-T^t_t =", sp.simplify(-Tmix['t']))
print("p_r =", sp.simplify(Tmix['r']))
print("p_th=", sp.simplify(Tmix['th']))
print("p_ps=", sp.simplify(Tmix['ps']))
print("T^t_t==T^r_r?", sp.simplify(Tmix['t']-Tmix['r'])==0)
# the M10/M11 banked: T^th_th = (kap m^2 - m^2 r^2 xi + r^2 xi)/(2 r^4)
banked = (kap*m**2 - m**2*r**2*xi + r**2*xi)/(2*r**4)
print("p_th - banked =", sp.simplify(Tmix['th']-banked))
