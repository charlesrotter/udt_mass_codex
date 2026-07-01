import sympy as sp
t, r, th = sp.symbols('t r theta', real=True)
ps = sp.Symbol('psi', real=True)
A = sp.symbols('A')
w = sp.symbols('w', positive=True)
X=[t,r,th,ps]
H = sp.Function('H')(r)
P2 = (3*sp.cos(th)**2 - 1)/2
h = A*H*sp.cos(w*t)
# single P2 warp on flat round background (m=0 confirmed)
g = sp.diag(-1, 1, r**2*(1+h*P2), r**2*sp.sin(th)**2*(1-h*P2))
ginv=g.inv()
n=4
Ga=[[[sp.S(0)]*n for _ in range(n)] for _ in range(n)]
for a in range(n):
  for b in range(n):
    for cc in range(n):
      s=sp.S(0)
      for d in range(n):
        if ginv[a,d]==0: continue
        s+=ginv[a,d]*(sp.diff(g[d,cc],X[b])+sp.diff(g[d,b],X[cc])-sp.diff(g[b,cc],X[d]))
      Ga[a][b][cc]=s/2
Ric=sp.zeros(n,n)
for b in range(n):
  for d in range(n):
    s=sp.S(0)
    for a in range(n):
      s+=sp.diff(Ga[a][b][d],X[a])-sp.diff(Ga[a][b][a],X[d])
      for e in range(n):
        s+=Ga[a][a][e]*Ga[e][b][d]-Ga[a][d][e]*Ga[e][b][a]
    Ric[b,d]=sp.expand(s)
def O1(e): return sp.simplify(sp.series(sp.expand(e),A,0,2).removeO().coeff(A,1))
Rtt=O1(Ric[0,0]); Rtr=O1(Ric[0,1])
Rthth_up=O1(ginv[2,2]*Ric[2,2]); Rpsps_up=O1(ginv[3,3]*Ric[3,3])
tl=sp.simplify(Rthth_up-Rpsps_up)  # traceless angular
trace=sp.simplify(Rthth_up+Rpsps_up)
print("R_tt^(1) =",Rtt)
print("R_tr^(1) =",Rtr)
print("traceless (R^th_th - R^ps_ps) =", sp.simplify(tl/sp.cos(w*t)) if tl.has(sp.cos(w*t)) else tl)
print("trace     (R^th_th + R^ps_ps) =", sp.simplify(trace/sp.cos(w*t)) if trace.has(sp.cos(w*t)) else trace)
