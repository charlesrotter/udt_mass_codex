"""Numeric comparison: reduced energy of NORMALIZED candidate-A (genuinely unit)
vs corpus E2_r, at a sample (F,F',phi,r). Pure numpy, fast."""
import numpy as np

def grad2_unit(F,Fp,phd,r,th,ph):
    # candidate A
    nA = np.array([np.sin(F)*np.sin(th)*np.cos(ph),
                   np.sin(F)*np.sin(th)*np.sin(ph),
                   np.cos(F)])
    nrm = np.linalg.norm(nA)
    nhat = nA/nrm
    # numeric derivatives of nhat wrt r,th,ph
    h=1e-6
    def nh(F_,th_,ph_):
        v=np.array([np.sin(F_)*np.sin(th_)*np.cos(ph_),
                    np.sin(F_)*np.sin(th_)*np.sin(ph_),
                    np.cos(F_)]); return v/np.linalg.norm(v)
    # r enters only via F(r): dnhat/dr = dnhat/dF * Fp
    dF = (nh(F+h,th,ph)-nh(F-h,th,ph))/(2*h) * Fp
    dt = (nh(F,th+h,ph)-nh(F,th-h,ph))/(2*h)
    dp = (nh(F,th,ph+h)-nh(F,th,ph-h))/(2*h)
    g = np.exp(-2*phd)*dF.dot(dF) + (1/r**2)*dt.dot(dt) + (1/(r**2*np.sin(th)**2))*dp.dot(dp)
    return g

F,Fp,phd,r=1.0,0.5,0.0,1.0
# sphere integral of (1/2) g * e^{phd} r^2 sin th
Nth=400; Nph=8
ths=np.linspace(1e-4,np.pi-1e-4,Nth)
phs=np.linspace(0,2*np.pi,Nph,endpoint=False)
tot=0.0
for th in ths:
    for ph in phs:
        g=grad2_unit(F,Fp,phd,r,th,ph)
        tot += 0.5*g*np.exp(phd)*r**2*np.sin(th)
dth=ths[1]-ths[0]; dph=2*np.pi/Nph
E_norm = tot*dth*dph
E2c = (2*np.pi/3)*(r**2*np.sin(F)**2*Fp**2 + 2*r**2*Fp**2 + 4*np.sin(F)**2)
print(f"normalized-A reduced (1/2 grad^2): {E_norm:.6f}")
print(f"corpus E2_r:                        {E2c:.6f}")
print(f"ratio norm/corpus: {E_norm/E2c:.4f}")
