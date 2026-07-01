import sys; sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
import numpy as np, scipy.linalg as sla, w4b_evolib as ev
npz = np.load('/tmp/w4b_bg.npz'); lin = np.load('/tmp/w4b_lingap.npz')
for tag, meas in (('M2', 0.22734663), ('M4', 0.21279013)):
    geo = ev.Geo(npz, tag, Nu=24, Nx=1024)
    kc = float(lin[f'{tag}_kc']); kray = int(lin[f'{tag}_kray'])
    dx = geo.dx[kray]; r2 = geo.r[kray]**2; fth2 = geo.fth2[kray]; N = geo.Nx
    r2m = 0.5*(r2[1:]+r2[:-1]); A = np.zeros((N,N)); ii = np.arange(N-1)
    A[ii,ii] += r2m/dx; A[ii+1,ii+1] += r2m/dx; A[ii,ii+1] -= r2m/dx; A[ii+1,ii] -= r2m/dx
    wxs = np.full(N,dx); wxs[0]=wxs[-1]=dx/2
    B = np.diag(3*geo.c/16*fth2*wxs); M = np.diag(r2*wxs)
    keep = np.arange(N)[1:]
    A,B,M = (Z[np.ix_(keep,keep)] for Z in (A,B,M))
    w2 = sla.eigh(A - B/(0.95*kc), M, eigvals_only=True, subset_by_index=[0,0])[0]
    pred = np.sqrt(max(-w2,0))
    print('%s at 0.95kc: predicted rate %.4f measured %.4f rel-dev %.2f%%' % (tag, pred, meas, 100*abs(meas-pred)/pred))
