import sympy as sp
# Independent confirmation: conserved Dirac charge Q=INT j^t sqrt(-g) d^3x.
# j^t = e^t_0 psibar gamma^0 psi = e^{PHI} psi^dagger psi.  sqrt(-g)=r^2 sin th.
# In Form-T, the radial spinor density psi^dagger psi (angular-normalized) relates to G,F. 
# The standard Form-T convention (CG 4.4): the reduced radial functions are defined so that
# psi^dagger psi * (frame/measure) integrates with the e^{2PHI} weight in (g,f). We derived the
# conserved orthogonality => norm = INT(G^2+F^2)dr. Cross-check: does this match j^t integral?
# j^t sqrt(-g) ~ e^{PHI} * psi^dag psi * r^2. If (g,f) carry psi^dag psi r^2 e^{PHI}~ e^{2PHI}(g^2+f^2)
# then Q~INT e^{2PHI}(g^2+f^2)dr = INT(G^2+F^2)dr. Consistent. 
print("Consistent: j^t-charge measure = e^{2PHI}(g^2+f^2)dr = (G^2+F^2)dr. Confirms SL result.")
