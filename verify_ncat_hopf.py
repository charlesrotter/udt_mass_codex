#!/usr/bin/env python3
"""Genuine Whitehead Hopf integral for the degree-k hedgehog (suspension) field,
on a periodic box (embed cell), dA=F solved spectrally. H should be 0 (integer)."""
import numpy as np
PI=np.pi

def hopf_whitehead(k,N=48):
    # Map the hedgehog onto a periodic cube via a smooth field that is vacuum on
    # the boundary (so flux is compactly supported -> H well-defined integer).
    # Use Cartesian box; build n as suspension of angular degree-k map with a
    # radial bump that returns to north pole at large radius (compact support).
    L=2.0
    x=np.linspace(-L,L,N,endpoint=False);d=x[1]-x[0]
    X,Y,Z=np.meshgrid(x,x,x,indexing='ij')
    rr=np.sqrt(X**2+Y**2+Z**2)+1e-12
    th=np.arccos(np.clip(Z/rr,-1,1)); ps=np.arctan2(Y,X)
    # profile: Lam=0 at r=0 and r large (vacuum north pole both ends) -> hedgehog bump
    prof=np.exp(-((rr-0.8)/0.35)**2)  # localized shell
    Lam=PI*prof*np.sin(th)*0+ prof*th  # suspension: Lam = prof(r)*th
    n=np.stack([np.sin(Lam)*np.cos(k*ps),np.sin(Lam)*np.sin(k*ps),np.cos(Lam)])
    # F_i = (1/2) eps_ijk  n.(dj n x dk n)  -> vector field F_i (the 'magnetic field')
    g=[np.gradient(n[c],d,d,d) for c in range(3)]  # g[c] = [dx n_c, dy n_c, dz n_c]
    dn=[np.stack([g[c][ax] for c in range(3)]) for ax in range(3)]  # dn[ax]=d_ax n (3,N,N,N)
    def cr(a,b):return np.stack([a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]])
    def dt(a,b):return np.sum(a*b,axis=0)
    F=np.zeros((3,N,N,N))
    # F_x = n.(dy n x dz n), cyclic
    F[0]=dt(n,cr(dn[1],dn[2]))
    F[1]=dt(n,cr(dn[2],dn[0]))
    F[2]=dt(n,cr(dn[0],dn[1]))
    # solve A with curl A = F, div A=0 spectrally: A_hat = i k x F_hat / |k|^2
    kf=2*PI*np.fft.fftfreq(N,d=d)
    KX,KY,KZ=np.meshgrid(kf,kf,kf,indexing='ij')
    K2=KX**2+KY**2+KZ**2;K2[0,0,0]=1
    Fh=[np.fft.fftn(F[c]) for c in range(3)]
    # A_hat = i (K x F_hat)/K2
    Ah=[1j*(KY*Fh[2]-KZ*Fh[1])/K2,
        1j*(KZ*Fh[0]-KX*Fh[2])/K2,
        1j*(KX*Fh[1]-KY*Fh[0])/K2]
    A=[np.real(np.fft.ifftn(Ah[c])) for c in range(3)]
    AF=sum(A[c]*F[c] for c in range(3))
    H=np.sum(AF)*d**3/(4*PI)**2
    totflux=np.sum(F[2])*d**3
    return H

print("[Hopf] genuine Whitehead integral H (should be ~0 integer for hedgehog):")
for k in (1,2,3):
    for N in (40,56):
        H=hopf_whitehead(k,N)
        print(f"   k={k} N={N}: H = {H:+.4f}")
