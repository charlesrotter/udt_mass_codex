"""Finite exact closure/holonomy controls; not the universal fibration proof."""
import json
import math
import sys
from fractions import Fraction
import sympy as sp

mode=sys.argv[1] if len(sys.argv)>1 else 'baseline'
assert mode in {'baseline','integer_only','all_rational_regular','wrong_period','swap_axes'}

def closed_slope(r):
    if mode=='integer_only':
        return bool(r.is_integer)
    return r.is_rational is True

def periods(r):
    q=r.denominator
    return (r.numerator if mode=='wrong_period' else q, Fraction(1),1/r)

def axis_orders(r):
    p,q=r.numerator,r.denominator
    return (p,q) if mode=='swap_axes' else (q,p)

def regular(r):
    return True if mode=='all_rational_regular' else axis_orders(r)==(1,1)

checks={}
def check(name,ok): checks[name]=bool(ok)
fixtures=[Fraction(1),Fraction(3,2),Fraction(2,3),Fraction(7,5),Fraction(5,7)]
data=[]
for r in fixtures:
    p,q=r.numerator,r.denominator
    period,ax0,ax1=periods(r)
    check(f'closure_{r}',closed_slope(sp.Rational(p,q)))
    check(f'interior_period_{r}',period==q and (r*period).denominator==1)
    check(f'axis_periods_{r}',ax0==1 and r*ax1==1)
    # Actual modular rotations after n primitive core turns, separate from helper.
    direct0=next(n for n in range(1,q+1) if (p*n)%q==0)
    direct1=next(n for n in range(1,p+1) if (q*n)%p==0)
    check(f'axis_holonomy_orders_{r}',axis_orders(r)==(direct0,direct1))
    check(f'regular_{r}',regular(r)==(p==q==1))
    data.append(dict(slope=str(r),period_units_2pi=str(period),axis_orders=axis_orders(r)))
check('sqrt2_exactly_not_rational',not closed_slope(sp.sqrt(2)))
check('irrational_positive_near_Hopf',not closed_slope(1+sp.sqrt(2)/1000))
check('representative_rescaling_leaves_slope',sp.cancel((3*sp.Symbol('r'))/3)==sp.Symbol('r'))
# Deliberate coverage limitation: all rational sample points pass rationality
# for r(s)=1+s, although an exact irrational interior point fails it.
sample=[sp.Rational(j,10) for j in range(1,10)]
sample_pass=all(closed_slope(1+s) for s in sample)
irr=sp.sqrt(2)/2
check('rational_sampling_false_pass_retained',sample_pass and not closed_slope(1+irr))
print(json.dumps(dict(kind='finite exact controls NOT proof',mode=mode,checks=checks,
    passed=sum(checks.values()),failed=[n for n,v in checks.items() if not v],
    fixtures=data,rational_sampling_false_pass=sample_pass,
    versions=dict(python=sys.version.split()[0],sympy=sp.__version__)),indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
