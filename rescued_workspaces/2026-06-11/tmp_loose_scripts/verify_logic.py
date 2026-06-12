import sympy as sp
r = sp.symbols('r', positive=True)
A = sp.Function('A')(r); B = sp.Function('B')(r)
# G^t_t - G^r_r = -(AB)'/(rAB^2).  Set = 0 (vacuum or T^t_t=T^r_r):
# => (AB)' = 0 => AB = const. Asymptotic flatness A->1,B->1 => const=1 => B=1/A.
# Demonstrate that WITHOUT T^t_t=T^r_r, B=1/A is not forced:
# pick arbitrary A,B with AB != const, identity is nonzero -> needs a matter with T^t_t != T^r_r.
print("(AB)'=0 <=> AB=const; asympt flat => AB=1 => B=1/A. Requires LHS=0 i.e. T^t_t=T^r_r.")
# Check: a perfect fluid p_r = -rho gives T^t_t=T^r_r? T^t_t=-rho, T^r_r=p_r. Equal iff p_r=-rho.
print("perfect fluid: T^t_t=-rho, T^r_r=p_r; equal iff p_r=-rho (vacuum-like EoS). CONFIRMED non-general.")
