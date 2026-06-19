#!/usr/bin/env python3
"""CLAIM 6: winding number of deg-1 hedgehog = 1 (numeric, independent)."""
import numpy as np

# n = (sinTh sinth cosph, sinTh sinth sinph, cosTh) with Th = theta (deg-1)
# Winding W = (1/4pi) INT eps_abc n_a (d_th n_b)(d_ph n_c) - (d_ph n_b)(d_th n_c)...
# pullback area form: W = (1/4pi) INT n.(d_th n x d_ph n) dth dph
def n_of(Th, th, ph):
    return np.array([np.sin(Th)*np.sin(th)*np.cos(ph),
                     np.sin(Th)*np.sin(th)*np.sin(ph),
                     np.cos(Th)])

# Use Th=theta as stated in claim (hedgehog at fixed r where Th sweeps... actually
# claim says "Th=theta"): map spatial (th,ph) -> target with Th=theta.
N=400
th=np.linspace(1e-6,np.pi-1e-6,N)
ph=np.linspace(0,2*np.pi,N)
TH,PH=np.meshgrid(th,ph,indexing='ij')
dth=th[1]-th[0]; dph=ph[1]-ph[0]
# n with Th=theta
nx=np.sin(TH)*np.sin(TH)*np.cos(PH)  # WAIT: claim n uses sinTh sinth: with Th=theta both equal
# Re-read claim: n=(sinTh sinth cosph,...). With Th=theta, sinTh=sinth=sin(theta).
# That is n = (sin^2 th cos ph, sin^2 th sin ph, cos th) -- check winding of THAT.
nx=np.sin(TH)**2*np.cos(PH)
ny=np.sin(TH)**2*np.sin(PH)
nz=np.cos(TH)
# normalize? this n is NOT unit (|n|^2=sin^4 th+cos^2 th). The winding density uses the
# unit map. Standard deg-1 hedgehog target unit vector: nhat=(sinTh' ...). Compute both.
def winding(nx,ny,nz,normalize):
    n=np.stack([nx,ny,nz],0)
    if normalize:
        n=n/np.linalg.norm(n,axis=0)
    dnt=np.gradient(n,th,axis=1)
    dnp=np.gradient(n,ph,axis=2)
    cross=np.cross(dnt,dnp,axis=0)
    dens=np.sum(n*cross,axis=0)
    return np.sum(dens)*dth*dph/(4*np.pi)

print("CLAIM 6: winding")
print(" literal n (sin^2th cosph...), unnormalized:", winding(nx,ny,nz,False))
print(" literal n normalized:", winding(nx,ny,nz,True))
# The canonical deg-1: identity map nhat=(sinth cosph, sinth sinph, costh)
ux=np.sin(TH)*np.cos(PH); uy=np.sin(TH)*np.sin(PH); uz=np.cos(TH)
print(" identity map nhat=(sinth cosph,...):", winding(ux,uy,uz,False))
