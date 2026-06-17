"""
PART: mpmath high-precision spot-check of one eigenvalue by SHOOTING.
Independent of the FD eigensolvers. Solve the Schrodinger form
  -psi'' + V psi = E psi,  V = -2 phi' f^2 / r  (tortoise coord x),
on a box [0, x_wall] with psi(0)=0 (regular/Dirichlet) and find E=omega^2
such that psi(x_wall)=0 (the box ground state).  mp.dps=40.

Uses a clean Gaussian phi0=-0.8 well, R_wall=6.  Compares to FD value.
"""
import mpmath as mp
mp.mp.dps = 40

phi0 = mp.mpf('-0.8'); width = mp.mpf('1.0')
def phi(r): return phi0*mp.e**(-(r/width)**2)
def phip(r): return phi0*mp.e**(-(r/width)**2)*(-2*r/width**2)
def f(r): return mp.e**(-2*phi(r))

R_wall = mp.mpf('6.0')
# build tortoise map x(r) by integrating dr/f, and store sample of V(x)
Nr = 2000
rs = [R_wall*mp.mpf(i)/Nr for i in range(Nr+1)]
# x(r): cumulative trapezoid of 1/f
xs = [mp.mpf(0)]
for i in range(1,Nr+1):
    dr = rs[i]-rs[i-1]
    xs.append(xs[-1] + dr*(1/f(rs[i])+1/f(rs[i-1]))/2)
x_wall = xs[-1]
# V as function of x via r(x) lookup (linear interp on rs/xs)
def Vofx(xq):
    # find bracket
    if xq<=xs[0]: r=rs[0]
    elif xq>=xs[-1]: r=rs[-1]
    else:
        lo,hi=0,Nr
        while hi-lo>1:
            mid=(lo+hi)//2
            if xs[mid]<xq: lo=mid
            else: hi=mid
        t=(xq-xs[lo])/(xs[hi]-xs[lo]); r=rs[lo]+t*(rs[hi]-rs[lo])
    if r<mp.mpf('1e-9'): r=mp.mpf('1e-9')
    return -2*phip(r)*f(r)**2/r

# RK4 shoot: psi(0)=0, psi'(0)=1, integrate to x_wall, return psi(x_wall)
def shoot(E, M=4000):
    h=x_wall/M
    x=mp.mpf(0); psi=mp.mpf(0); dpsi=mp.mpf(1)
    def acc(xx,pp): return (Vofx(xx)-E)*pp
    for i in range(M):
        k1p=dpsi;            k1d=acc(x,psi)
        k2p=dpsi+h/2*k1d;    k2d=acc(x+h/2,psi+h/2*k1p)
        k3p=dpsi+h/2*k2d;    k3d=acc(x+h/2,psi+h/2*k2p)
        k4p=dpsi+h*k3d;      k4d=acc(x+h,psi+h*k3p)
        psi+=h/6*(k1p+2*k2p+2*k3p+k4p)
        dpsi+=h/6*(k1d+2*k2d+2*k3d+k4d)
        x+=h
    return psi

# ground state E between 0.1 and 0.5 (FD gave ~0.286)
E = mp.findroot(lambda e: shoot(e), mp.mpf('0.286'))
print("mpmath dps=40, RK4 M=4000, shooting")
print("x_wall =", mp.nstr(x_wall, 10))
print("ground state omega^2 (E) =", mp.nstr(E, 15))
print("omega0 =", mp.nstr(mp.sqrt(E),15))
