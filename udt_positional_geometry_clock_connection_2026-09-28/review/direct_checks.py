"""Separate implementation: exact conformal-Minkowski incidence, no geodesic ODE.

FREE diagnostic metric/control curves; not physical UDT inputs. c_E=1 units.
Independent source-first reasoning preceded author exposure; this program was
written after direct exposure, using a different analytical construction.
"""
import json
import math
import platform
import sympy as sp
import scipy
from scipy.optimize import brentq
from scipy.integrate import quad

exact=[]
def zero(name,expr):
    z=sp.simplify(expr)
    if z!=0: raise RuntimeError((name,z))
    exact.append({'name':name,'residual':str(z)})

# Independently exhibit the affine metric as a pullback of Minkowski space.
tau,x,a0,b,c=sp.symbols('tau x a0 b c',real=True,nonzero=True)
T=(tau+a0/b)*sp.cosh(b*x/c)
X=c*(tau+a0/b)*sp.sinh(b*x/c)
J=sp.Matrix([T,X]).jacobian([tau,x])
pullback=J.T*sp.diag(-c*c,1)*J
for i in range(2):
    for j in range(2):
        zero(f'affine_Minkowski_pullback_{i}{j}',pullback[i,j]-sp.diag(-c*c,(a0+b*tau)**2)[i,j])

# Time coordinate transformation T=f(t), f'>0: Ntilde=N/f',
# ptilde=f'p, beta unchanged. Added slowness integral is log(f'_B/f'_A).
NA,NB,jA,jB=sp.symbols('NA NB jA jB',positive=True)
zero('time_reparam_lapse_integral_cancellation',
     sp.log((NB/jB)/(NA/jA))+sp.log(jB/jA)-sp.log(NB/NA))

# Nonlinear independent ray coordinates f(t), h(x) are monotone globally.
# g=Omega(t,x)^2[-f'(t)^2 dt^2+h'(x)^2 dx^2].
records=[]; rejections={'omit_lapse':[], 'omit_integral':[], 'reverse_motion':[]}
controls=[
    ('coordinate_only',.2,.1,0.,0.,0.,(0.,0.),(0.,0.)),
    ('conformal_accelerating',.2,.1,.09,.02,-.03,(.03,.01),(-.04,.006)),
    ('conformal_accelerating_second',.08,.04,-.07,.04,.025,(-.02,-.008),(.03,-.005)),
]
for name,alpha,beta,gamma,zeta,kappa,left,right in controls:
    def f(t):return t+alpha*t**3
    def fp(t):return 1+3*alpha*t*t
    def fpp(t):return 6*alpha*t
    def h(x):return x+beta*x**3
    def hp(x):return 1+3*beta*x*x
    def omega(t,x):return math.exp(gamma*t*x+zeta*t*t+kappa*x*x)
    def observer(t,side):
        v,a=left if side==0 else right
        return side+v*t+a*t*t,v+2*a*t
    def proper(t,side):
        xx,v=observer(t,side)
        q=fp(t)**2-hp(xx)**2*v*v
        if q<=0:raise RuntimeError('non-timelike supplied control')
        return omega(t,xx)*math.sqrt(q)
    for eps in (-1,1):
        sideA,sideB=(0,1) if eps==1 else (1,0)
        te=.3
        def arrival(te):
            xa,_=observer(te,sideA)
            def incidence(tr):
                xb,_=observer(tr,sideB)
                return f(tr)-f(te)-eps*(h(xb)-h(xa))
            return brentq(incidence,te,te+4,xtol=5e-15,rtol=1e-14)
        tr=arrival(te)
        xa,va=observer(te,sideA);xb,vb=observer(tr,sideB)
        ba=hp(xa)*va/fp(te);bb=hp(xb)*vb/fp(tr)
        if max(abs(ba),abs(bb))>=1:raise RuntimeError('endpoint timelike failure')
        coordinate_slope=(fp(te)-eps*hp(xa)*va)/(fp(tr)-eps*hp(xb)*vb)
        direct=proper(tr,sideB)*coordinate_slope/proper(te,sideA)
        def integrand(xx):
            target=f(te)+eps*(h(xx)-h(xa))
            tt=brentq(lambda u:f(u)-target,te-1e-10,tr+1e-10,xtol=5e-15,rtol=1e-14)
            return -hp(xx)*fpp(tt)/fp(tt)**2
        integral=quad(integrand,min(xa,xb),max(xa,xb),epsabs=2e-13,epsrel=2e-13)[0]
        lapse=math.log(omega(tr,xb)*fp(tr)/(omega(te,xa)*fp(te)))
        motion=eps*(math.atanh(bb)-math.atanh(ba))
        formula=math.exp(lapse+motion+integral)
        # In the T=f(t) coordinate ptilde=h'(x), so partial_T ptilde=0.
        transformed=omega(tr,xb)/omega(te,xa)*math.exp(motion)
        pulses=[]
        for step in (.01,.003,.001):
            early,late=arrival(te-step),arrival(te+step)
            emitted=quad(lambda t:proper(t,sideA),te-step,te+step,epsabs=2e-13,epsrel=2e-13)[0]
            received=quad(lambda t:proper(t,sideB),early,late,epsabs=2e-13,epsrel=2e-13)[0]
            pulses.append({'half_interval':step,'ratio':received/emitted,'error':abs(received/emitted-direct)})
        errors={'formula':abs(formula-direct),'time_reparam':abs(transformed-direct),
                'integral_identity':abs(integral+math.log(fp(tr)/fp(te)))}
        if max(errors.values())>1e-11:raise RuntimeError((name,eps,errors))
        if pulses[-1]['error']>2e-7:raise RuntimeError(('pulse',name,eps,pulses))
        if pulses[0]['error']>1e-10 and pulses[-1]['error']>=.02*pulses[0]['error']:
            raise RuntimeError(('pulse convergence',name,eps,pulses))
        for kind,bad in [('omit_lapse',math.exp(motion+integral)),
                         ('omit_integral',math.exp(lapse+motion)),
                         ('reverse_motion',math.exp(lapse-motion+integral))]:
            err=abs(bad-direct)
            if err>1e-5:rejections[kind].append({'case':name,'direction':eps,'error':err})
        records.append({'case':name,'direction':eps,'arrival':tr,'direct_incidence_ratio':direct,
                        'candidate_formula_ratio':formula,'transformed_coordinate_ratio':transformed,
                        'endpoint_beta':[ba,bb],'errors':errors,'pulse_intervals':pulses})
if not all(rejections.values()):raise RuntimeError(('vacuous mutants',rejections))
print(json.dumps({'classification':'exact symbolic identities and independent floating-point controls, not certification',
 'versions':{'python':platform.python_version(),'sympy':sp.__version__,'scipy':scipy.__version__},
 'method':'exact conformal-Minkowski null incidence with brentq; independent integral quad; finite pulse clocks',
 'tolerances':{'identity':1e-11,'pulse':2e-7,'mutant_rejection':1e-5},
 'exact':exact,'records':records,'wrong_formula_rejections':rejections,
 'max_formula_error':max(r['errors']['formula'] for r in records),
 'max_final_pulse_error':max(r['pulse_intervals'][-1]['error'] for r in records),
 'all_pass':True},indent=2))
