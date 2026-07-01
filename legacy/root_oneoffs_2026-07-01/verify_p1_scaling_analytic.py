import sympy as sp
# Goal: derive the R-scaling of the geon WITHOUT trusting the author's solver,
# by a clean dimensional/scaling argument on the O(A^2) system.
#
# The system (per doc): linear wave  -Psi'' + 6/r^2 Psi = w^2 Psi, Psi~r^3 core, Psi(R)=0.
# Backreaction (Misner-Sharp constraint): (rF)' = -(r^2/2) S[Psi],  S quadratic in Psi.
# phi = A^2 F.  w shift driven by phi-dressing of the wave operator at O(A^2).
#
# SCALING ARGUMENT (the tautology core):
# Define rescaled radial var x = r/R, x in [0,1]. Linear eigenfn on [0,R]:
#   Psi_R(r) = N_R * r j_2(w0 r),  w0 = z/R (z = j2 first zero).
# Under r=Rx: r j_2(w0 r) = R x j_2(z x). So the SHAPE in x is R-independent;
# only an overall length factor R multiplies it.
z = sp.Symbol('z', positive=True)
R = sp.Symbol('R', positive=True)
x = sp.Symbol('x', positive=True)
A = sp.Symbol('A', positive=True)
# L2 normalization on [0,R]: ||Psi||_2^2 = int_0^R Psi^2 dr = A^2.
# Psi = N_R * r j2(w0 r). int_0^R (r j2(z r/R))^2 dr = R^3 * int_0^1 (x j2(z x))^2 dx = R^3 * I2.
# So N_R^2 * R^3 * I2 = A^2 => N_R = A / (R^{3/2} sqrt(I2)).
# max|Psi| = N_R * max_r |r j2(w0 r)| = N_R * R * max_x|x j2(z x)| = A/(R^{1/2}) * (max.../sqrt I2)
# => max|Psi| ~ A / sqrt(R)   <-- matches doc "max|Psi| ~ A/sqrt(R)"
print("max|Psi| scaling: N_R*R ~ A/sqrt(R)  (since N_R ~ A/R^{3/2}, times R)")
print("  => peak-warp p := max|Psi| ~ A/sqrt(R)")

# Backreaction: (rF)' = -(r^2/2) S, S ~ quadratic in Psi and its derivs => S ~ N_R^2 * (1/R^0 shape, but derivs bring 1/R)
# Psi ~ N_R * R * f(x);  d/dr = (1/R) d/dx.  S has terms ~ Psi'^2, Psi^2/r^2, w^2 Psi^2.
#   Psi ~ N_R R f,   Psi' ~ N_R f',   Psi/r ~ N_R f/x,  w ~ z/R so w Psi ~ N_R f.
#   => every quadratic term in S ~ N_R^2 * (R-independent function of x).  S ~ N_R^2 g(x).
# Constraint: (rF)' = -(r^2/2) S.  With r=Rx, d/dr=(1/R)d/dx:
#   (1/R) d/dx (R x F) = -(R^2 x^2/2) N_R^2 g(x)
#   d/dx(x F) = -(R^2 x^2 /2) N_R^2 g   *... wait carry R:
#   LHS (1/R)*R * d/dx(xF) = d/dx(xF). RHS = -(R x)^2/2 * N_R^2 g = -(R^2 x^2/2) N_R^2 g
#   => d/dx(xF) = -(R^2 x^2/2) N_R^2 g(x)
#   => F ~ R^2 N_R^2 * (shape)  = R^2 * (A^2/R^3) * shape = A^2/R * shape(x).
# So phi = A^2 F ... wait phi=A^2 F already has A^2; here F itself carries A^2? 
# In doc phi=A^2 F means F is the A-stripped profile. Let's strip A: set Psi=A*psi_unit, N_R=1/(R^{3/2}sqrtI2).
# Then F_unit ~ R^2 * N_R^2 = R^2 / R^3 = 1/R.  => max|F| ~ 1/R.   MATCHES (0.96,0.48,0.24,0.12).
print("max|F| scaling (A-stripped):  F ~ R^2 * N_R^2 ~ R^2/R^3 = 1/R   => max|F| ~ 1/R  CONFIRMED")
print("  doc values 0.960,0.480,0.240,0.120 halve per R-doubling => 1/R exactly. consistent.")

# Frequency shift: dw ~ <Psi| dV |Psi> / <Psi|Psi> with dV ~ phi-dressing ~ A^2 F * (operator).
# phi = A^2 F_unit, F_unit ~ 1/R.  dw ~ A^2 * (1/R) * (1/R) from operator length-dims => dw/dA^2 ~ 1/R^2.
print("dw/dA^2 ~ 1/R^2  CONFIRMED (doc: -9.43,-2.36,-0.59,-0.147 -> *R^2 flat)")
# check the doc dw numbers scale as 1/R^2:
for Rv,dw in [(1,-9.43),(2,-2.36),(4,-0.590),(8,-0.147)]:
    print(f"   R={Rv}: dw/dA^2*R^2 = {dw*Rv**2:.3f}")

# The -1.705 ratio: frac/max|phi| = (dw/w0)/(A^2 max|F|).
# dw ~ A^2 /R^2 (with some const), w0 = z/R ~ 1/R, max|phi|=A^2 max|F| ~ A^2/R.
# frac = dw/w0 ~ (A^2/R^2)/(1/R) = A^2/R.
# frac/max|phi| ~ (A^2/R)/(A^2/R) = R-INDEPENDENT.  <-- THE CANCELLATION. tautology confirmed.
print("\nfrac = dw/w0 ~ (A^2/R^2)/(1/R) = A^2/R ;  max|phi| ~ A^2/R")
print("=> frac/max|phi| ~ R-INDEPENDENT by construction. THE -1.705 R-invariance IS the 1/R cancellation. TAUTOLOGY CONFIRMED.")
