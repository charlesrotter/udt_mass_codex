import mpmath as mp
mp.mp.dps = 50

def L(k): return mp.log((1+k)/(1-k))
def G1(k): return (2*k + (k*k-1)*L(k))/k**3
def H(k):  return L(k)/(2*k) - 1

# independent numeric integral of the BARE integrand sin^3/(1+k cos)
def Inat(k):
    return mp.quad(lambda t: mp.sin(t)**3/(1+k*mp.cos(t)), [0, mp.pi])

# the dpf-side ORIGINAL quadrature: P/(F kappa^2/8) reduces to exactly Inat
# density = f_theta^2/(4f), f=F(1+k cos), avg = INT dens sin th dth /2
def Pquad_over(k):  # P / (F) with kappa=k, returns the angular factor
    integ = lambda t: (mp.sin(t))**2/(1+k*mp.cos(t))  # (F k sin)^2/(4F(1+kcos)) /(Fk^2) *4 = sin^2/(1+kcos)
    # P = INT [ (F k sin)^2/(4 f) ] sin th dth /2 = (F k^2/8) INT sin^3/(1+kcos) dth
    return mp.quad(lambda t: mp.sin(t)**3/(1+k*mp.cos(t)), [0, mp.pi])

for k in [mp.mpf('0.1'),mp.mpf('0.3'),mp.mpf('0.5'),mp.mpf('0.683095'),mp.mpf('0.9')]:
    print(f"k={float(k):.6f}  Inat={mp.nstr(Inat(k),20)}  G1={mp.nstr(G1(k),20)}  |I-G1|={mp.nstr(abs(Inat(k)-G1(k)),5)}  H={mp.nstr(H(k),12)}")
# series of G1 and H to compare what 'matches'
import sympy as sp
ks=sp.symbols('k')
Lg=sp.log((1+ks)/(1-ks))
print("\nseries G1:", sp.series((2*ks+(ks**2-1)*Lg)/ks**3, ks,0,7))
print("series H :", sp.series(Lg/(2*ks)-1, ks,0,7))
