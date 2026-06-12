import numpy as np
from scipy.special import sph_harm
from numpy import pi, sqrt

NTH, NPH = 80, 160
xg, wg = np.polynomial.legendre.leggauss(NTH); theta=np.arccos(xg)
phi=np.linspace(0,2*pi,NPH,endpoint=False); dphi=2*pi/NPH
TH,PH=np.meshgrid(theta,phi,indexing='ij'); W=np.outer(wg,np.ones(NPH))*dphi
nx,ny,nz=np.sin(TH)*np.cos(PH),np.sin(TH)*np.sin(PH),np.cos(TH)
NHAT=[nx,ny,nz]

def Y(l,m):
    if l<0 or abs(m)>l: return np.zeros_like(TH,dtype=complex)
    return sph_harm(m,l,PH,TH)
def l_of(k): return k if k>0 else -k-1
def j_of(k): return abs(k)-0.5
def omega(k,mu):
    l=l_of(k); j=j_of(k)
    if abs(mu)>j: z=np.zeros_like(TH,dtype=complex); return (z,z)
    if k<0: a=sqrt((l+mu+0.5)/(2*l+1)); b=sqrt((l-mu+0.5)/(2*l+1))
    else:   a=-sqrt((l-mu+0.5)/(2*l+1)); b=sqrt((l+mu+0.5)/(2*l+1))
    return (a*Y(l,int(mu-0.5)), b*Y(l,int(mu+0.5)))
def mus(k):
    j=j_of(k); return [(-2*j+2*t)/2 for t in range(int(2*j)+1)]
def inner(A,B): return np.sum(np.conj(A[0])*B[0]*W)+np.sum(np.conj(A[1])*B[1]*W)

# Pauli matrices
sx=np.array([[0,1],[1,0]],complex); sy=np.array([[0,-1j],[1j,0]]); sz=np.array([[1,0],[0,-1]],complex)
S=[sx,sy,sz]

def h_tensor(kind):
    if kind=="m0": return np.diag([-1.,-1.,2.])/sqrt(6)
    if kind=="m2": h=np.zeros((3,3)); h[0,0]=1;h[1,1]=-1; return h/sqrt(2)
    if kind=="m1": h=np.zeros((3,3)); h[0,2]=1;h[2,0]=1; return h/sqrt(2)

# ----------------------------------------------------------------------------------
# LINEARIZED-GRAVITY DIRAC SPIN CONNECTION.
# Metric g_munu = eta + h, vierbein e^a_mu = delta + (1/2) h^a_mu (symmetric gauge).
# For a STATIC, purely spatial h_ij(x) = f(r) * H_ij  (H = const sym traceless tensor),
# the spatial spin connection (Lorentz generators) is, to first order:
#   omega_i^{ab} = (1/2)(d_b h_{ai} - d_a h_{bi})   [spatial a,b,i, antisymmetric in a,b]
# The Dirac coupling is  H_sc = (i/4) gamma^i sigma_{ab} omega_i^{ab}  ... working in the
# 3D rotation sector the relevant piece is  H_sc = -(1/2) Sigma . B_grav where
#   B_grav_c = (1/2) eps_{cab} omega_i^{ab} (acting with gamma^i).
# Cleanest standard form: the spatial spin connection contributes
#   H_sc = (i/8) [gamma^i, gamma^j-type] ... -> let me build it directly and concretely.
#
# Concretely (e.g. Obukhov, or standard linearized result): for static h_ij the
# fermion sees an effective term  (1/4) eps^{abc} (d_a h_{bi}) gamma^i gamma_5-ish...
# To avoid importing a possibly-wrong vertex, I build the spin connection from the
# vierbein DIRECTLY by finite differences and contract with the gamma's.  Then I test
# kappa selection.  Profile f(r): I use h_ij = f(r) H_ij with f(r) varying, so d(h) has
# BOTH a radial-derivative piece (~ f'(r) nhat) and the constant-H angular structure.
# ----------------------------------------------------------------------------------

# We work on a thin shell; the ONLY thing that matters for kappa-selection is the ANGULAR
# operator content. The spin-connection vertex for static h has schematic form
#    Omega_i ~ d_j h_{ki}  (one derivative of h).
# With h_{ki}(x)=f(r) H_{ki}, d_j h_{ki} = f'(r) nhat_j H_{ki}  +  f(r) (d_j H_{ki}).
# H is constant => second term 0. So spin connection ~ f'(r) nhat_j H_{ki}: it carries an
# EXTRA nhat_j (orbital unit) times the constant rank-2 H. This is the rank-3 worry.
#
# The Dirac spin-connection Hamiltonian (Foldy-Wouthuysen / standard, static field) reduces
# in the upper/lower Dirac structure. The leading angular operator that can change kappa is
#    O_sc = Sigma^a  (eps_{ajk} d_j h_{ki})  ... contracted appropriately. Build the most
# general first-order single-derivative-of-h operator and test its WORST-CASE kappa reach.
#
# Most general first-order vertex bilinear in (one Sigma or none) x (one factor of d h):
#   candidate angular operators acting on the 2-spinor channel:
#     A) Sigma . ( (grad x h.?) )  -- but let's just enumerate the independent rank tensors.
# The object d_j h_{ki} with h_{ki}=f'(r) nhat_j H_{ki} angular part = nhat_j H_{ki}.
# Contract with available spin (Sigma^a, rank1) and the i,j,k indices. The genuinely NEW
# angular factor vs the vierbein term is the EXTRA nhat. So I test: does (nhat) x (vierbein
# vertex) i.e. an operator with TWO nhat's leak to kappa=-4?

# Build operators and test reach from kappa=-1.
def apply_sigma_dot_v(spinor, v):
    up,dn=spinor
    return (v[2]*up+(v[0]-1j*v[1])*dn, (v[0]+1j*v[1])*up-v[2]*dn)

def hv(h):  # v = h . nhat
    return [sum(h[i,jj]*NHAT[jj] for jj in range(3)) for i in range(3)]

# Operator family for spin connection candidates. The spin connection term in the Dirac eq
# for static h, after reduction, has the structure  Sigma . ( nhat x (h.nhat) )  and
# Sigma_a (curl of h)_a type pieces and ALSO a piece  ~ (nhat . Sigma)(something). 
# I will test the FULL set of single-particle angular operators built from {nhat, h.nhat, Sigma}
# that are first order in h, and check whether ANY produces a NONZERO kappa=-1 -> kappa=-4.

def reach(op_apply, k0, targets, kind):
    h=h_tensor(kind)
    out={}
    for kp in targets:
        Ssum=0.0
        for mu in mus(k0):
            T=op_apply(omega(k0,mu),h)
            for mup in mus(kp):
                Ssum+=abs(inner(omega(kp,mup),T))**2
        out[kp]=Ssum
    return out

# candidate operators (each maps a 2-spinor -> 2-spinor, angular only):
def op_curl(spinor,h):
    # Sigma . (nhat x v),  v=h.nhat  -- a "magnetic" type term from the spin connection
    v=hv(h)
    cross=[ny*v[2]-nz*v[1], nz*v[0]-nx*v[2], nx*v[1]-ny*v[0]]
    return apply_sigma_dot_v(spinor,cross)
def op_ndotSig_times_ndotv(spinor,h):
    # (nhat.Sigma)(nhat.v) type: TWO nhats -> rank could be higher
    v=hv(h)
    ndv=nx*v[0]+ny*v[1]+nz*v[2]
    snO=apply_sigma_dot_v(spinor,NHAT)
    return (ndv*snO[0], ndv*snO[1])
def op_v_only(spinor,h):
    # scalar (nhat.v) multiply  (no spin) -- pure orbital
    v=hv(h); ndv=nx*v[0]+ny*v[1]+nz*v[2]
    return (ndv*spinor[0], ndv*spinor[1])
def op_extra_nhat_sigma_v(spinor,h):
    # (nhat.Sigma) applied then sigma.v : product of two sigma's with two nhats... 
    snO=apply_sigma_dot_v(spinor,NHAT)
    return apply_sigma_dot_v(snO,hv(h))

targets=[-1,1,-2,2,-3,3,-4,4,-5]
print("Spin-connection candidate operators: kappa=-1 reach (m0). Watch kappa=-4.")
for name,op in [("Sig.(n x v)",op_curl),
                ("(n.Sig)(n.v)",op_ndotSig_times_ndotv),
                ("(n.v) scalar",op_v_only),
                ("(n.Sig)(sig.v)",op_extra_nhat_sigma_v)]:
    r=reach(op,-1,targets,"m0")
    rr={kp:round(v,4) for kp,v in r.items() if v>1e-12}
    leak4 = r[-4]>1e-10
    print(f"  {name:18s}: reach={rr}   kappa=-4 S={r[-4]:.3e} {'<<< LEAK' if leak4 else ''}")
