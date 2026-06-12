#!/usr/bin/env python3
"""Independent adversarial recomputation of D1/D2 for the weld discriminator.
Own grid, own integrator, own comb regularization, Limber-style single
integral AND an independent double integral. Phase-anchoring attack included.
"""
import numpy as np

MU = 0.2472981283
R  = 9.164114
C5 = np.cos(np.pi/5)
DL = 297.0
OFF= 243.0

def phi0(r):  x=MU*r; return 1.5*x - C5*x**2 + (2/3)*x**3
def phi0p(r): x=MU*r; return MU*(1.5 - 2*C5*x + 2*x**2)
PHC = phi0(R)

def cumtrap(y, x):
    out = np.zeros_like(y)
    out[1:] = np.cumsum(0.5*(y[1:]+y[:-1])*np.diff(x))
    return out

def fields(r, envpow=1.0, envelope='dphi'):
    ph, php = phi0(r), phi0p(r)
    f = np.exp(-2*ph)
    dphi = phi0(r)/PHC
    if envelope == 'dphi':      S = dphi**envpow
    elif envelope == 'linear':  S = (r/R)**envpow
    elif envelope == 'sin':     S = np.sin(0.5*np.pi*r/R)**envpow
    H1E = np.exp(2*ph)*cumtrap(2*dphi, r)
    H1N = 2*dphi/(f*php)
    WE = (np.exp(2*ph)/r**2)*H1E*np.exp(-3*ph)
    WN = (np.exp(2*ph)/r**2)*H1N*np.exp(-3*ph)
    return WE, WN, S/np.max(S)

# ---------------- D1: own quantile stats -------------------------------
def quant(r, V):
    w = V*V
    c = cumtrap(w, r); c /= c[-1]
    return tuple(np.interp([.16,.5,.84], c, r))

r_f = np.linspace(1e-3, R, 48000)
WE, WN, S = fields(r_f)
VE, VN = WE*np.sqrt(S), WN*np.sqrt(S)
qE, qN = quant(r_f, VE), quant(r_f, VN)
print("D1 (independent): r50_E=%.4f width_E=%.4f | r50_N=%.4f width_N=%.4f"
      % (qE[1], qE[2]-qE[0], qN[1], qN[2]-qN[0]))
print("   delta r50 = %.4f Gpc  (script: 0.0292)" % (qE[1]-qN[1]))

# interior-mass / suppression numbers (attack E)
i_pk = np.argmax(VE**2)
for rr in (1.0, 2.0, 5.0, 8.0, 8.8):
    i = np.searchsorted(r_f, rr)
    print("   V_E^2(%.1f)/V_E^2(peak)=%.3e   V_N^2/peak=%.3e   H1E/H1N=%.3f"
          % (rr, VE[i]**2/VE[i_pk]**2, VN[i]**2/VN[i_pk]**2,
         (WE[i]/WN[i])))
c2E = cumtrap(VE**2, r_f); c2N = cumtrap(VN**2, r_f)
for rr in (5.0, 8.0):
    i = np.searchsorted(r_f, rr)
    print("   fraction of V^2 mass below r=%.0f:  E %.2e  N %.2e"
          % (rr, c2E[i]/c2E[-1], c2N[i]/c2N[-1]))

# ---------------- D2 Limber-style single integral ----------------------
# Q(ell) = int V^2 sin^2(chi) dr / int V^2 dr ; oscillatory part integrated
# only on [5,R] (dense grid, slow oscillation); below r=5 sin^2 -> 1/2 (mass
# fraction there bounds the error and is printed above).
r_b = np.linspace(5.0, R, 60000)          # boundary grid, own resolution

def limber_Q(ells, off=OFF, V2pair=None, envelope='dphi', envpow=1.0,
             combfun=None):
    WEb, WNb, Sb = fields(r_b, envpow=envpow, envelope=envelope)
    V2E, V2N = WEb**2*Sb, WNb**2*Sb
    nE = np.trapezoid(V2E, r_b); nN = np.trapezoid(V2N, r_b)
    QE = np.empty(len(ells)); QN = np.empty(len(ells))
    for i, l in enumerate(ells):
        chi = np.pi*(l*R/r_b - off)/DL
        M = np.sin(chi)**2 if combfun is None else combfun(chi)
        QE[i] = np.trapezoid(V2E*M, r_b)/nE
        QN[i] = np.trapezoid(V2N*M, r_b)/nN
    return QE, QN

def peaks(ells, Q, lo=330, hi=1950):
    st = ells[1]-ells[0]; out=[]
    for i in range(1, len(ells)-1):
        if lo<=ells[i]<=hi and Q[i]>Q[i-1] and Q[i]>=Q[i+1]:
            d = 0.5*(Q[i-1]-Q[i+1])/(Q[i-1]-2*Q[i]+Q[i+1])
            out.append(ells[i]+d*st)
    return np.array(out)

def shifts(pA, pB, tol=80):
    return np.array([pB[np.argmin(np.abs(pB-p))]-p for p in pA
                     if len(pB) and np.min(np.abs(pB-p))<=tol])

ells = np.arange(100.0, 2001.0, 1.0)
QE, QN = limber_Q(ells)
pE, pN = peaks(ells, QE), peaks(ells, QN)
sh = shifts(pE, pN)
print("\nD2 LIMBER (independent, own grid+integrator, ell step 1):")
print("   E peaks:", np.round(pE,1))
print("   N peaks:", np.round(pN,1))
print("   shifts N-E:", np.round(sh,2), " mean = %.3f" % np.mean(sh))

# midpoint offsets
mids = np.array([OFF+(n+0.5)*DL for n in range(8)]); mids=mids[(mids>330)&(mids<1950)]
offE = np.mean([p - mids[np.argmin(np.abs(mids-p))] for p in pE])
offN = np.mean([p - mids[np.argmin(np.abs(mids-p))] for p in pN])
print("   midpoint offsets: E %.2f  N %.2f" % (offE, offN))

# ---------------- PHASE-ANCHORING ATTACK --------------------------------
print("\nPHASE ATTACK (slide/randomize comb phase OFF):")
rng = np.random.default_rng(7)
res = []
for off in list(np.arange(0, 297, 33)) + list(rng.uniform(0,297,8)):
    QEp, QNp = limber_Q(ells, off=off)
    s = shifts(peaks(ells,QEp), peaks(ells,QNp))
    if len(s): res.append((off, np.mean(s), np.min(s), np.max(s)))
arr = np.array([x[1] for x in res])
for off, m, lo, hi in res:
    print("   off=%6.1f  mean shift %+6.3f  [%+5.2f,%+5.2f]" % (off,m,lo,hi))
print("   over all phases: mean of means %+.3f, range [%.3f, %.3f]"
      % (arr.mean(), arr.min(), arr.max()))

# different comb SHAPE (not sin^2): raised cosine with different harmonic mix
print("\nCOMB-SHAPE attack (M = 0.5+0.3cos(2chi)+0.2cos(4chi) shifted comb):")
f2 = lambda chi: 0.5 - 0.3*np.cos(2*chi) + 0.2*np.cos(4*chi)
QEc, QNc = limber_Q(ells, combfun=f2)
s = shifts(peaks(ells,QEc), peaks(ells,QNc))
print("   shifts:", np.round(s,2), " mean %.3f" % np.mean(s))

# envelope attacks (MY source choices)
print("\nENVELOPE attack:")
for env, ep in (('linear',1.0), ('sin',1.0), ('dphi',2.0), ('dphi',0.5)):
    QEe, QNe = limber_Q(ells, envelope=env, envpow=ep)
    s = shifts(peaks(ells,QEe), peaks(ells,QNe))
    print("   env=%s^%.1f: mean shift %+.3f  n=%d" % (env, ep, np.mean(s), len(s)))

# ---------------- INDEPENDENT DOUBLE INTEGRAL ---------------------------
# own conventions: trapezoid weights, sinc (cell-average) anti-alias, N=300
print("\nDOUBLE-INTEGRAL (independent, N=300, trapezoid, sinc anti-alias):")
N = 300
rg = np.linspace(1e-3, R, N); h = rg[1]-rg[0]
wq = np.full(N, h); wq[0]*=0.5; wq[-1]*=0.5
WEg, WNg, Sg = fields(rg)
VEg, VNg = WEg*np.sqrt(Sg), WNg*np.sqrt(Sg)
R1, R2 = np.meshgrid(rg, rg, indexing='ij'); D2 = (R1-R2)**2
ellsd = np.arange(100.0, 2001.0, 5.0)
def dbl(V, l, comb, kappa=1.0):
    Lc = kappa*R/l
    K = np.exp(-D2/(2*Lc*Lc))
    if comb:
        chi = np.pi*(l*R/rg - OFF)/DL
        kr = 2*np.pi*l*R/(DL*rg**2)
        d = np.sinc(kr*h/(2*np.pi))          # cell-average damping (own choice)
        M = 0.5 + (np.sin(chi)**2 - 0.5)*d
        Vc = V*np.sqrt(np.clip(M,0,None))
    else:
        Vc = V
    return (Vc*wq) @ K @ (Vc*wq)
QdE = np.array([dbl(VEg,l,True)/dbl(VEg,l,False) for l in ellsd])
QdN = np.array([dbl(VNg,l,True)/dbl(VNg,l,False) for l in ellsd])
pdE, pdN = peaks(ellsd,QdE), peaks(ellsd,QdN)
sd = shifts(pdE,pdN)
print("   E peaks:", np.round(pdE,1))
print("   N peaks:", np.round(pdN,1))
print("   shifts:", np.round(sd,2), " mean %.3f" % np.mean(sd))
# spot check two ells vs Limber Q values
for l in (605.0, 1500.0):
    i = np.searchsorted(ellsd, l); j = np.searchsorted(ells, l)
    print("   ell=%4.0f  Q_E dbl=%.4f limber=%.4f | Q_N dbl=%.4f limber=%.4f"
          % (l, QdE[i], QE[j], QdN[i], QN[j]))
# coherence x2 on double integral
QdE2 = np.array([dbl(VEg,l,True,2.0)/dbl(VEg,l,False,2.0) for l in ellsd])
QdN2 = np.array([dbl(VNg,l,True,2.0)/dbl(VNg,l,False,2.0) for l in ellsd])
s2 = shifts(peaks(ellsd,QdE2), peaks(ellsd,QdN2))
print("   Lc x2: mean shift %.3f" % np.mean(s2))

# ---------------- per-weld spread vs differential (attack C) ------------
print("\nATTACK C numbers: differential across MY variants:")
allmeans = [np.mean(sh), np.mean(s), np.mean(sd), np.mean(s2)] + [x[1] for x in res]
allmeans = np.array(allmeans)
print("   all differential means: min %.3f max %.3f" % (allmeans.min(), allmeans.max()))
