import sympy as sp
# Velocity bound claim: v_r = 2GF/(G^2+F^2) e^{-phi}, |2GF|<=G^2+F^2
G,F = sp.symbols('G F', real=True)
# |2GF| <= G^2+F^2  <=>  (G^2+F^2) - 2|GF| = (|G|-|F|)^2 >=0. TRUE always.
print("AM-GM: (|G|-|F|)^2 >= 0 => |2GF| <= G^2+F^2 : identically true")
# So v_r e^{phi} = 2GF/(G^2+F^2) in [-1,1]. The bound is just AM-GM, NOT a dynamical relativistic statement.
# Standing-mode net flux: for real stationary G,F, the spatial Dirac current j^r = 2GF e^{-phi}/r^2 is
# generally NONZERO pointwise (real), but the TIME-AVERAGED net flux through any shell...
# Actually for a real bispinor the radial probability current 2 Re(G* F) does not vanish per se;
# it's the *conserved* current with div(j)=0 in stationary state => integral flux through a closed shell
# is the same at all r only if no source. Standing wave => net transport zero across a node structure.
print("v_r e^phi in [-1,1] is AM-GM identity, not a measured relativistic velocity")
