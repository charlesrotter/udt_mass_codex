"""
CORE ENGINE -- exact transverse l>=1 second variation, fully numerical 3D action,
on the genuinely-UNIT hedgehog background n_hat = normalize(candidate-A).

Perturbation honoring |n|=1 EXACTLY:
   n(eps) = normalize( n0 + eps * delta ),   delta = a(r) f(th,ph) e1 + b(r) g(th,ph) e2
where {e1,e2} orthonormal tangent frame at n_hat. We DO NOT pre-orthogonalize delta
to n0 (normalize handles the constraint), but e1,e2 are tangent so to O(eps) delta is
tangent and to O(eps^2) normalize subtracts the n0-component automatically.

We compute the exact action density on n(eps), integrate over the sphere (theta,phi)
on a grid, and finite-difference in eps to get the quadratic form. We do this for
trial radial profiles to assemble the radial operator H and weight W as matrices in a
radial basis (finite differences in r). Then eigensolve H x = omega^2 W x.

ANGULAR CHANNELS (grand-spin / standard harmonics):
We use real spherical-harmonic angular factors Y_{l m}(th,ph) multiplying the tangent
vectors. Because the hedgehog is invariant under combined rotations, the cleanest is to
use ordinary Y_lm on the e1 (polar) and e2 (azimuthal) tangent directions; channels mix
within fixed total-l blocks but the LOWEST eigenvalue per l is what we need (variational).
For the sign verdict we scan a basis spanning the angular structure of given l and take
the Rayleigh minimum over radial AND the few angular harmonics of that l.

Time-kinetic weight W: from the t-kinetic of L2+L4 with g^{tt} = -e^{2phi}. For a tangent
fluctuation delta_t = (rate) the kinetic energy quadratic = INT [ (1/2) e^{2phi}*xi |ddot n|^2
 + L4 time part ] sqrt(g). We compute W by the SAME finite-difference machinery applied to
the time-kinetic density (n depends on t through the mode amplitude).
"""
import numpy as np

# ---------- unit background ----------
def nhat_and_frame(F, th, ph):
    """Return n0 (unit), e1, e2 orthonormal tangent frame at (F,th,ph)."""
    a = np.sin(F)*np.sin(th)*np.cos(ph)
    b = np.sin(F)*np.sin(th)*np.sin(ph)
    c = np.cos(F)
    v = np.array([a,b,c]); n0 = v/np.linalg.norm(v)
    # tangent e1 from d n0/dF, e2 = n0 x e1
    h=1e-7
    def nn(FF):
        w=np.array([np.sin(FF)*np.sin(th)*np.cos(ph),
                    np.sin(FF)*np.sin(th)*np.sin(ph),
                    np.cos(FF)]); return w/np.linalg.norm(w)
    d=(nn(F+h)-nn(F-h))/(2*h)
    d=d-d.dot(n0)*n0
    ne=np.linalg.norm(d)
    if ne<1e-12:
        # fallback arbitrary tangent
        tmp=np.array([1.0,0,0]); tmp=tmp-tmp.dot(n0)*n0
        if np.linalg.norm(tmp)<1e-6: tmp=np.array([0,1.0,0]); tmp=tmp-tmp.dot(n0)*n0
        e1=tmp/np.linalg.norm(tmp)
    else:
        e1=d/ne
    e2=np.cross(n0,e1)
    return n0,e1,e2

# ---------- exact action density (per unit dr dOmega, *sqrt(g)) ----------
def action_density(field_func, F, Fp, phd, r, th, ph, h=1e-6):
    """field_func(F,th,ph)->unit 3-vector. Returns (L2+L4 energy density)*sqrt(g)
    using exact metric. r-derivative via F only (chain rule with Fp) PLUS explicit:
    here the field depends on r only through F, so dn/dr = dn/dF * Fp. (Mode radial
    dependence handled outside.)"""
    n0=field_func(F,th,ph)
    dF=(field_func(F+h,th,ph)-field_func(F-h,th,ph))/(2*h)
    dnr=dF*Fp
    dnt=(field_func(F,th+h,ph)-field_func(F,th-h,ph))/(2*h)
    dnp=(field_func(F,th,ph+h)-field_func(F,th,ph-h))/(2*h)
    grr=np.exp(-2*phd); gtt=1/r**2; gpp=1/(r**2*np.sin(th)**2)
    grad2=grr*dnr.dot(dnr)+gtt*dnt.dot(dnt)+gpp*dnp.dot(dnp)
    e2=0.5*grad2
    Srt=np.cross(dnr,dnt); Srp=np.cross(dnr,dnp); Stp=np.cross(dnt,dnp)
    L4s=2*(grr*gtt*Srt.dot(Srt)+grr*gpp*Srp.dot(Srp)+gtt*gpp*Stp.dot(Stp))
    e4=0.25*L4s
    sqrtg=np.exp(phd)*r**2*np.sin(th)
    return (e2+e4)*sqrtg
