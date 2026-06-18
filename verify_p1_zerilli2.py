import numpy as np
from scipy.special import spherical_jn

# Verify -Psi'' + 6/r^2 Psi = w^2 Psi for Psi=r*j_2(w r), numerically via finite diff.
w = 1.3
def Psi(r): return r*spherical_jn(2, w*r)
rs = np.linspace(0.3, 5.0, 40)
h = 1e-5
lhs = (-( Psi(rs+h)-2*Psi(rs)+Psi(rs-h))/h**2 + 6/rs**2*Psi(rs))
rhs = w**2*Psi(rs)
print("max|lhs-rhs| (Zerilli ODE, Psi=r j_2):", np.max(np.abs(lhs-rhs)))

# Dirichlet zeros: Psi(R)=0 with R=1 => j_2(w)=0 => w = j_2 zeros.
# j_2 zeros: find first 6.
from scipy.optimize import brentq
def f(x): return spherical_jn(2, x)
zeros=[]
x=0.1
xs=np.linspace(0.5,30,6000)
vals=f(xs)
for i in range(len(xs)-1):
    if vals[i]*vals[i+1]<0:
        zeros.append(brentq(f, xs[i], xs[i+1]))
zeros=np.array(zeros[:6])
print("j_2 zeros (=w_n at R=1, Dirichlet):", np.round(zeros,4))
print("ratios w_n/w_1:", np.round(zeros/zeros[0],4))

# Neumann: Psi'(R)=0. d/dr[r j_2(wr)] at r=1.
def g(x):  # derivative of r*j2(x r) wrt r at r=1, as function of x=w
    rr=1.0; hh=1e-6
    return ( (rr+hh)*spherical_jn(2,x*(rr+hh)) - (rr-hh)*spherical_jn(2,x*(rr-hh)) )/(2*hh)
nz=[]
vals2=np.array([g(x) for x in xs])
for i in range(len(xs)-1):
    if vals2[i]*vals2[i+1]<0:
        nz.append(brentq(g, xs[i], xs[i+1]))
nz=np.array(nz[:6])
print("Neumann w_n:", np.round(nz,4))
print("Neumann ratios:", np.round(nz/nz[0],4))
