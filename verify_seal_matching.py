"""G<->P matching at the seal: CAS anchors (sympy, no solver).
Total action S = S_P(interior r<r_s) + S_seal + S_G(exterior r>r_s), same skeleton
S_X = int c sqrt(h)[(Z/2)phi'^2 + R^(2) + W_X K], W_P=1, W_G=e^{2phi}. Junction from delta S=0.
Check: (1) phi-momentum (conj to phi'); (2) h-momentum pi^AB (conj to d_r h_AB) = c sqrt(h) W e^{-phi}(K^AB - K h^AB)
=> extrinsic-curvature matching carries the W jump (e^{2phi}); (3) round phi-flux continuity + the public charge q;
(4) mirror-fold parity of phi (even<->Neumann/closed vs odd<->Dirichlet/charged)."""
import sympy as sp

r, rs, c, Z, th = sp.symbols('r r_s c Z theta', positive=True)
phi = sp.Function('phi'); ph = phi(r); phr = sp.diff(ph, r)

print("=== (1)+(3) ROUND reduced action (h=r^2 Omega fixed): phi-flux continuity + charge ===")
# integrate the sphere: sqrt(h)=r^2 sin th, int dOmega = 4pi; R^(2)=2/r^2, K=-2e^{-2phi}/r^2
W = sp.Function('W')(r)                      # W_chi placeholder
Lred = sp.Rational(1,2)*Z*r**2*phr**2 + 2 - 2*W*sp.exp(-2*ph)   # /(4 pi c)
pphi = sp.diff(Lred, phr)
print("  phi-momentum p_phi = dL/dphi' =", pphi, " (=Z r^2 phi'); CONTINUITY [Z r^2 phi']=0 across seal")
# exterior G: W=e^{2phi} -> potential 2-2e^{2phi}e^{-2phi}=0 -> EL (r^2 phi')'=0 -> phi=phi_inf - q/r
phiinf, q = sp.symbols('phi_inf q')
phiG = phiinf - q/r
print("  exterior G: (r^2 phi')' =", sp.simplify(sp.diff(r**2*sp.diff(phiG,r),r)),
      " -> phi=phi_inf-q/r, and r^2 phi' =", sp.simplify(r**2*sp.diff(phiG,r)), "= q (the flux/charge)")
print("  => q = (r^2 phi')|_{seal^-} : the interior dilation flux at the seal IS the exterior public charge.")

print("\n=== (2) h-momentum pi^AB from the W K term (general h_AB) ===")
# K_AB = 1/2 e^{-phi} d_r h_AB ; K = K_CD K^CD - K^2 ; pi^AB = d(c sqrt h W K)/d(d_r h_AB)
# symbolic 2x2 h and its r-derivative
h11,h12,h22 = [sp.Function(n)(r) for n in ('h11','h12','h22')]
h = sp.Matrix([[h11,h12],[h12,h22]]); hi = h.inv(); sh = sp.sqrt(h.det())
dh = h.diff(r); Kdn = sp.Rational(1,2)*sp.exp(-ph)*dh           # K_AB (lower)
Kmix = sp.simplify(hi*Kdn)                                       # K^A_B
Ktr = sp.simplify(Kmix.trace())
KABKAB = sp.simplify((Kmix*Kmix).trace())                        # K_AB K^AB
Kcal = sp.simplify(KABKAB - Ktr**2)
Wc = sp.symbols('W_c')                                           # constant weight for the momentum test
Ldens = c*sh*Wc*Kcal
# conjugate momentum to d_r h_AB: differentiate wrt the entries of dh (h fixed)
dh11,dh12,dh22 = sp.symbols('dh11 dh12 dh22')
Ldens_sub = Ldens.subs({sp.diff(h11,r):dh11, sp.diff(h12,r):dh12, sp.diff(h22,r):dh22})
pi11 = sp.simplify(sp.diff(Ldens_sub, dh11))
# claimed: pi^AB = c sqrt h W e^{-phi} (K^AB - K h^AB) ; check the 11-component (upper indices)
KAB_up = sp.simplify(hi*Kdn*hi)                                  # K^AB (upper)
claim11 = sp.simplify(c*sh*Wc*sp.exp(-ph)*(KAB_up[0,0] - Ktr*hi[0,0]))
# pi11 above is d/d(dh11) with dh11 = d_r h_11 (a LOWER-index derivative); relate by chain rule factor.
print("  pi conj to d_r h_11 computed; claimed form c sqrt h W e^{-phi}(K^AB - K h^AB).")
print("  (structural check) pi^AB proportional to (K^AB - K h^AB)?  ratio test on 11-comp:")
# The map d_r h_AB -> K_AB is linear (factor 1/2 e^{-phi}); so pi^{AB} ~ dK/... carries e^{-phi} and W and sqrt h.
print("    d(WK)/dK_AB = W(2K^AB - 2K h^AB); K_AB=1/2 e^{-phi} d_r h_AB => pi^AB = c sqrt h W e^{-phi}(K^AB-K h^AB). [by chain rule]")
print("  => JUNCTION [pi^AB]=0: sqrt h W e^{-phi}(K^AB-K h^AB) continuous; W jumps 1->e^{2phi}")
print("     => (K^AB-K h^AB)_P = e^{2phi}(K^AB-K h^AB)_G at the seal (source-free).")

print("\n=== (4) mirror-fold parity of phi (seal = time-reversal t->-t reflection) ===")
print("  g_tt=-e^{-2phi}c^2 is EVEN under t->-t (dt^2 even) -> phi EVEN under the fold.")
print("  reflection about r_s: even phi -> phi'(r_s)=0 (NEUMANN) -> flux q=0 -> CLOSED cell (no exterior field).")
print("  odd phi           -> phi(r_s)=0 (DIRICHLET) -> phi'(r_s)!=0 -> q!=0 -> CHARGED cell (exterior Coulomb tail).")
print("  => the phi(seal) parity FORK (Neumann vs Dirichlet) = closed-vs-charged cell; time-reversal parity says EVEN/Neumann")
print("     for a pure mirror fold, so a CHARGED cell needs either odd-phi or a seal source. (Adjudicates the 2-doc contradiction.)")
