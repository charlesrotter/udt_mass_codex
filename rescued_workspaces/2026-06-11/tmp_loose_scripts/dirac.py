import numpy as np
from scipy.integrate import solve_ivp

# Metric's own profile (the field-equation solution)
def phi_metric(r):
    return 0.5*np.log(r/(2.0+r))
def phip_metric(r):
    # d/dr [0.5 ln(r/(2+r))] = 0.5*(1/r - 1/(2+r)) = 0.5*( (2+r - r)/(r(2+r)) ) = 0.5*2/(r(2+r))
    return 1.0/(r*(2.0+r))

# Verify phi solves phi'' + 2 phi'/r - 2 phi'^2 = 0
import sympy as sp
rr=sp.symbols('r',positive=True)
ph=sp.Rational(1,2)*sp.log(rr/(2+rr))
expr=sp.diff(ph,rr,2)+2*sp.diff(ph,rr)/rr-2*sp.diff(ph,rr)**2
print("field eq residual:", sp.simplify(expr))
