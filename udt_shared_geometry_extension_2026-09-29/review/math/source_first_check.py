"""Reviewer-owned exact controls; no author SGE1 code/candidate exposure."""
import json
import platform
import sympy as s

checks = []
def check(name, expression):
    value = s.simplify(expression)
    if value != 0:
        raise AssertionError((name, value))
    checks.append(name)

# Independent index contraction in a rest frame. nabla_a U_b has the first
# index as derivative. All spatial motion channels remain symbolic.
H = s.symbols('H', real=True)
a = s.Matrix(s.symbols('a1:4', real=True))
n = s.Matrix(s.symbols('n1:4', real=True))
s11,s22,s12,s13,s23,w12,w13,w23 = s.symbols(
    's11 s22 s12 s13 s23 w12 w13 w23', real=True)
sig = s.Matrix([[s11,s12,s13],[s12,s22,s23],[s13,s23,-s11-s22]])
w = s.Matrix([[0,w12,w13],[-w12,0,w23],[-w13,-w23,0]])
D = s.zeros(4)
for i in range(3):
    D[0,i+1] = a[i]
    for j in range(3):
        D[i+1,j+1] = H*s.KroneckerDelta(i,j)+sig[i,j]+w[i,j]
l = s.Matrix([1,*n])
B = (l.T*D*l)[0]
check('directional_contraction', B - (H*n.dot(n)+a.dot(n)+(n.T*sig*n)[0]))
check('vorticity_cancels', (n.T*w*n)[0])
even = s.expand((B+B.xreplace(dict(zip(n,-n))))/2)
odd = s.expand((B-B.xreplace(dict(zip(n,-n))))/2)
check('even_rate', even-H*n.dot(n)-(n.T*sig*n)[0])
check('odd_rate', odd-a.dot(n))

# All-direction isotropy: necessary coefficients already forced by finite
# directional probes, after tracefree shear is imposed.
C=s.symbols('C',real=True)
dirs=[s.eye(3)[:,i]*e for i in range(3) for e in (1,-1)]
dirs += [(s.eye(3)[:,i]+s.eye(3)[:,j])/s.sqrt(2)
         for i,j in [(0,1),(0,2),(1,2)]]
eqs=[B.subs(dict(zip(n,v)))-C for v in dirs]
sol=s.solve(eqs,[*a,s11,s22,s12,s13,s23,C],dict=True)
assert sol == [{a[0]:0,a[1]:0,a[2]:0,s11:0,s22:0,s12:0,s13:0,s23:0,C:H}]
checks.append('isotropic_rate_forces_zero_acceleration_and_shear')

# Null quadratic rigidity at an orthonormal point.
entries=s.symbols('h00 h01 h02 h03 h11 h12 h13 h22 h23 h33')
h00,h01,h02,h03,h11,h12,h13,h22,h23,h33=entries
M=s.Matrix([[h00,h01,h02,h03],[h01,h11,h12,h13],
            [h02,h12,h22,h23],[h03,h13,h23,h33]])
eqs=[(s.Matrix([1,*v]).T*M*s.Matrix([1,*v]))[0] for v in dirs]
nullsol=s.solve(eqs,entries[1:],dict=True)
assert nullsol == [{h01:0,h02:0,h03:0,h11:-h00,h12:0,
                    h13:0,h22:-h00,h23:0,h33:-h00}]
checks.append('all_null_quadratic_zero_forces_metric_multiple')

# Direct incidence in a positive Rindler lapse strip. a0>0, d>0 is a
# supplied diagnostic, not UDT admission. Coordinate one-way travel is L.
a0,d,tau=s.symbols('a0 d tau',positive=True)
N=1+a0*d
L=s.log(N)/a0
out=N*(tau+L)
ret=s.Symbol('b',real=True)/N+L
p=s.diff(out,tau)
q=s.diff(ret,s.Symbol('b',real=True))
echo=ret.subs(s.Symbol('b',real=True),out)
check('direct_static_incidence_out_slope',p-N)
check('direct_static_incidence_return_slope',q-1/N)
check('direct_static_incidence_echo_slope',s.diff(echo,tau)-1)
check('direct_static_incidence_positive_delay',echo-tau-2*L)

# Actual future relay algebra from arbitrary positive slopes.
p,q=s.symbols('p q',positive=True)
Tprime=(1+p*q)/2
Rprime=(p*q-1)/2
check('radar_slope',Rprime/Tprime-(p*q-1)/(p*q+1))
check('two_way_symmetric_log',s.exp(s.log(p*q))-p*q)
assert (s.Rational(3)*s.Rational(1,2)-1)/(s.Rational(3)*s.Rational(1,2)+1)>0
assert s.Rational(1,2)<1
checks.append('positive_radar_drift_does_not_force_both_redshift')

# Source FSL1 saturation countercontrol, independently checked here.
r=s.symbols('r',positive=True)
gam=1+r*r/2
sp=s.Matrix([r*r/2,r,0])
check('saturation_family_timelike',gam**2-sp.dot(sp)-1)
check('saturation_family_unit_redshift',gam-sp[0]-1)
check('saturation_family_norm_limit',s.limit(sp.dot(sp)/gam**2,r,s.oo)-1)

print(json.dumps({'status':'PASS','count':len(checks),'checks':checks,
                  'python':platform.python_version(),'sympy':s.__version__,
                  'evidence':'exact symbolic controls, not physical selection or formal proof'},indent=2))
