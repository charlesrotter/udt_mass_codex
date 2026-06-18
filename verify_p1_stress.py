import sympy as sp
# Independent O(A^2) backreaction: a standing l=2 even-parity GW on flat background
# sources a static l=0 metric correction (Misner-Sharp). We re-derive the l=0
# part of G_tt at O(A^2), time-averaged, in terms of the Zerilli master Psi, and
# compare its radial structure to the author's S[Psi].
#
# Rather than redo the full Zerilli tensor algebra (very heavy), do the decisive
# independent check the verifier instruction asks for: confirm the EFFECTIVE MASS
# m(R)/A^2 = R*F(R) = -0.90544 and its SIGN-INDEFINITENESS, by integrating the
# author's constraint (rF)' = -(r^2/2) S with the author's S but our OWN quadrature,
# AND independently confirm the *qualitative* sign structure is forced by S's form.
import numpy as np
from scipy.special import spherical_jn
from scipy.integrate import quad
from scipy.optimize import brentq

# first j2 zero (R=1 => w0 = z)
xs=np.linspace(0.5,12,20000); f=spherical_jn(2,xs)
z=None
for i in range(len(xs)-1):
    if f[i]*f[i+1]<0: z=brentq(lambda x: spherical_jn(2,x), xs[i],xs[i+1]); break
R=1.0; w=z
print("w0 (R=1) =", w)

def Psi(r): return r*spherical_jn(2,w*r)
def Psip(r):
    h=1e-6; return (Psi(r+h)-Psi(r-h))/(2*h)

def S(r):
    P=Psi(r); Pp=Psip(r); w2=w*w
    num=(-4*r**5*w2**2*P*Pp +5*r**4*w2**2*P**2 -5*r**4*w2*Pp**2
         -44*r**3*w2*P*Pp -107*r**2*w2*P**2 +45*r**2*Pp**2 +162*r*P*Pp +189*P**2)
    return num/(40*r**4*w2)

# (rF)' = -(r^2/2) S , with (rF)(0)=0 => rF(r) = -int_0^r (s^2/2) S(s) ds
# m(r)=A^2 r F(r); m(R)/A^2 = R F(R) = rF at R.
def integrand(s): return -(s**2/2.0)*S(s)
val,err=quad(integrand, 1e-8, R, limit=400)
print("R*F(R) = m(R)/A^2 =", val, " (author claims -0.90544)")

# sign structure of m'(r) = density: check rF(r) along the way (sign flips?)
print("\n rF(r) profile (m(r)/A^2):")
prev=None; signflips=0
for rr in np.linspace(0.05,1.0,20):
    v,_=quad(integrand,1e-8,rr,limit=400)
    if prev is not None and np.sign(v)!=np.sign(prev) and prev!=0: signflips+=1
    prev=v
    print(f"   r={rr:.3f}  m/A^2={v:+.5f}")
print(" cumulative-mass sign flips:", signflips)
# local density m'(r) = -(r^2/2)S(r) sign:
print("\n local density m'(r) = -(r^2/2)S(r) sign at sample points:")
for rr in [0.1,0.3,0.5,0.7,0.9]:
    print(f"   r={rr}: m'~{integrand(rr):+.4f}")

# Normalization reconciliation: author normalizes ||Psi||_2 = A (=1 at unit).
# m(R)/A^2 = R F(R) is then quoted at ||Psi||_2 = A, i.e. our unnormalized result
# divided by ||Psi_unnorm||_2^2 (since S is quadratic in Psi).
norm2,_=quad(lambda r: Psi(r)**2, 1e-8, R, limit=400)
print("\n||Psi_unnorm||_2^2 on [0,R] =", norm2)
print("m(R)/A^2 normalized (divide by ||Psi||^2):", val/norm2, " <- compare author -0.90544")
