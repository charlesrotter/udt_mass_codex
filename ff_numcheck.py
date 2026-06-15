#!/usr/bin/env python3
"""
ff_numcheck.py — FAST numeric finite-difference cross-check of the time-row
Einstein components G_tr, G_ttheta. No symbolic inversion. Independent of
fermion_forcing2.py. Confirms: static arm -> 0; stationary nonzero arm -> nonzero;
time-dependent arm -> changes value (velocity contribution).
"""
import numpy as np

c = 1.0
# coordinates: x = [t, r, theta, phi]
def metric(x, phi_f, A_f, B_f):
    t, r, th, ph = x
    p = phi_f(t, r, th); em = np.exp(-2*p); ep = np.exp(2*p)
    A = A_f(t, r, th); B = B_f(t, r, th)
    g = np.array([
        [-em*c**2, A,   B,    0.0],
        [ A,       ep,  0.0,  0.0],
        [ B,       0.0, r**2, 0.0],
        [ 0.0,     0.0, 0.0,  r**2*np.sin(th)**2],
    ])
    return g

def einstein(x0, phi_f, A_f, B_f, h=1e-4):
    n = 4
    def g_at(x): return metric(x, phi_f, A_f, B_f)
    # first derivatives dg[k] = d g / d x^k  (central)
    dg = np.zeros((n,n,n))
    for k in range(n):
        xp = list(x0); xm = list(x0); xp[k]+=h; xm[k]-=h
        dg[k] = (g_at(xp)-g_at(xm))/(2*h)
    # second derivatives ddg[k,l] = d^2 g / dx^k dx^l
    ddg = np.zeros((n,n,n,n))
    for k in range(n):
        for l in range(n):
            xpp=list(x0);xpm=list(x0);xmp=list(x0);xmm=list(x0)
            xpp[k]+=h;xpp[l]+=h; xpm[k]+=h;xpm[l]-=h
            xmp[k]-=h;xmp[l]+=h; xmm[k]-=h;xmm[l]-=h
            ddg[k,l]=(g_at(xpp)-g_at(xpm)-g_at(xmp)+g_at(xmm))/(4*h*h)
    g = g_at(x0); gi = np.linalg.inv(g)
    # Christoffel Gamma^a_{bc} = 1/2 g^{ad}(d_b g_{dc}+d_c g_{db}-d_d g_{bc})
    Gam=np.zeros((n,n,n))
    for a in range(n):
        for b in range(n):
            for cc in range(n):
                s=0.0
                for dd in range(n):
                    s+=gi[a,dd]*(dg[b][dd,cc]+dg[cc][dd,b]-dg[dd][b,cc])
                Gam[a,b,cc]=0.5*s
    # dGamma^a_{bc}/dx^e via derivative of the formula (use ddg, dg, and dgi)
    # dgi/dx^e = -gi . dg[e] . gi
    dgi=np.zeros((n,n,n))
    for e in range(n):
        dgi[e]=-gi@dg[e]@gi
    dGam=np.zeros((n,n,n,n))  # dGam[e,a,b,c]
    for e in range(n):
        for a in range(n):
            for b in range(n):
                for cc in range(n):
                    s=0.0
                    for dd in range(n):
                        s+=dgi[e][a,dd]*(dg[b][dd,cc]+dg[cc][dd,b]-dg[dd][b,cc])
                        s+=gi[a,dd]*(ddg[b,e][dd,cc]+ddg[cc,e][dd,b]-ddg[dd,e][b,cc])
                    dGam[e,a,b,cc]=0.5*s
    # Ricci_{bd}=dGam^a_{bd}/dx^a - dGam^a_{ba}/dx^d + Gam^a_{ae}Gam^e_{bd} - Gam^a_{de}Gam^e_{ba}
    Ric=np.zeros((n,n))
    for b in range(n):
        for d in range(n):
            s=0.0
            for a in range(n):
                s+=dGam[a,a,b,d]-dGam[d,a,b,a]
                for e in range(n):
                    s+=Gam[a,a,e]*Gam[e,b,d]-Gam[a,d,e]*Gam[e,b,a]
            Ric[b,d]=s
    R=np.einsum('ab,ab->',gi,Ric)
    G=Ric-0.5*g*R
    return G

# concrete phi(r,theta), static
phi_f=lambda t,r,th: 0.3*np.cos(th)*r
x0=[0.4,1.4,0.6,0.25]

zero=lambda t,r,th:0.0
print("--- (2) STATIC arm=0 ---")
G=einstein(x0,phi_f,zero,zero)
print("G_tr=%.3e  G_ttheta=%.3e"%(G[0,1],G[0,2]))

print("--- (1) STATIONARY nonzero arm ---")
As=lambda t,r,th:0.2*r*np.sin(th); Bs=lambda t,r,th:0.15*r**2*np.cos(th)
G=einstein(x0,phi_f,As,Bs)
print("G_tr=%.4e  G_ttheta=%.4e"%(G[0,1],G[0,2]))

print("--- (3) TIME-DEPENDENT arm ---")
At=lambda t,r,th:0.2*np.sin(t)*r*np.sin(th); Bt=lambda t,r,th:0.15*np.cos(t)*r**2*np.cos(th)
G=einstein(x0,phi_f,At,Bt)
print("G_tr=%.4e  G_ttheta=%.4e"%(G[0,1],G[0,2]))
print("DONE_NUM")
