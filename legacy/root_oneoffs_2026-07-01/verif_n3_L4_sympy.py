"""
INDEPENDENT VERIFIER — L4 angular structure.
L4 = -(kappa/4)(d_m n x d_n n)^2. t-t reduction inertia density:
  (kappa/2) g^{ij}[ (v_a.v_b)(d_i n.d_j n) - (v_a.d_i n)(v_b.d_j n) ]
We compute the ANGULAR part (i,j over theta,phi) of the L4 cross-tensor
analytically and check it is also diagonal axial 2+1 (the doc claims L4 ratio
~1.17, i.e. nearly isotropic, soliton-localized in both channels).
DATA-BLIND. sympy.
"""
import sympy as sp

th, ph, Th, Thp = sp.symbols('theta phi Theta Theta_p', real=True)  # Thp=dTheta/dr
sT,cT = sp.sin(Th), sp.cos(Th)
n1 = sT*sp.sin(th)*sp.cos(ph); n2 = sT*sp.sin(th)*sp.sin(ph); n3 = cT
n = sp.Matrix([n1,n2,n3])
e=[sp.Matrix([1,0,0]),sp.Matrix([0,1,0]),sp.Matrix([0,0,1])]
v=[ea.cross(n) for ea in e]

# spatial derivatives in the hedgehog. coords (r,theta,phi); metric e^{2phi}dr^2+r^2dOmega.
# n depends on r through Theta(r). d_r n = Thp * dn/dTheta.
dn_dTh = sp.Matrix([sp.cos(Th)*sp.sin(th)*sp.cos(ph), sp.cos(Th)*sp.sin(th)*sp.sin(ph), -sp.sin(Th)])
n_r  = Thp*dn_dTh
n_th = sp.Matrix([sp.diff(c,th) for c in n])
n_ph = sp.Matrix([sp.diff(c,ph) for c in n])

# inverse metric components (we keep r,phi symbolic via 1/r^2, 1/(r^2 sin^2)).
r = sp.symbols('r', positive=True)
gphi = sp.symbols('phi', real=True)  # metric potential
ginv = {'r': sp.exp(-2*gphi), 'th': 1/r**2, 'ph': 1/(r**2*sp.sin(th)**2)}
dn = {'r': n_r, 'th': n_th, 'ph': n_ph}

def dot(a,b): return (a.T*b)[0]

def L4_density(a,b):
    s = 0
    for i in ['r','th','ph']:
        s += ginv[i]*( dot(v[a],v[b])*dot(dn[i],dn[i]) - dot(v[a],dn[i])*dot(dn[i],v[b]) )
    # cross terms i!=j: g is diagonal so only i=j survive in g^{ij}d_i.d_j?
    # Actually L4 t-t reduction has g^{ij} with full sum; metric diagonal => i=j only.
    return sp.simplify(s)

dW = sp.sin(th)
def ang(expr):
    inner = sp.integrate(sp.expand(expr*dW),(ph,0,2*sp.pi))
    return sp.simplify(sp.integrate(inner,(th,0,sp.pi)))

print("=== L4 inertia ANGULAR-integrated cross tensor M4_ab(Theta,Theta',r,phi) ===")
M4 = sp.zeros(3,3)
for a in range(3):
    for b in range(3):
        M4[a,b] = ang(L4_density(a,b))
M4 = sp.simplify(M4)
print("M4[00] =", M4[0,0])
print("M4[11] =", M4[1,1])
print("M4[22] =", M4[2,2])
print("off-diagonals:")
for a in range(3):
    for b in range(3):
        if a!=b and M4[a,b]!=0:
            print(f"  M4[{a}{b}] =", M4[a,b])
print("All other off-diagonals zero:",
      all(M4[a,b]==0 for a in range(3) for b in range(3) if a!=b))
print("\nM4[00]-M4[11] =", sp.simplify(M4[0,0]-M4[1,1]), "(0 => perp degenerate)")
print("M4[00]-M4[22] =", sp.simplify(M4[0,0]-M4[2,2]), "(=>axial 2+1 in L4 too)")
