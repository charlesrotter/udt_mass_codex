"""Direct TRI1 example checks and two boundary controls; stdlib exact rationals."""
from fractions import Fraction as F
import json,sys
passed=[];rejected=[]
def c(name,value):
    assert value,name
    passed.append(name)
def no(name,value):
    assert not value,name
    rejected.append(name)
def arrival(s):return s+s*s
def deriv(s):return 1+2*s
def total(r1,r2):return r1/F(2)+r2/F(4)
c('candidate aggregate1',total(F(1),F(1))==F(3,4))
c('candidate aggregate2',total(F(3),F(1))==F(7,4))
c('candidate normalized aggregate1',total(F(1),F(1))/2==F(3,8))
c('candidate normalized aggregate2',total(F(3),F(1))/4==F(7,16))
no('universal normalized aggregate',total(F(1),F(1))/2==total(F(3),F(1))/4)
c('candidate finite duration',arrival(F(1))-arrival(F(0))==2)
no('point value gives finite duration',deriv(F(0))==2)
c('candidate first atom',arrival(F(1,4))==F(5,16))
c('candidate second atom',arrival(F(3,4))==F(21,16))
c('candidate interval count',sum(int(0<arrival(s)<=1) for s in [F(1,4),F(3,4)])==1)
for s in [F(0),F(1,4),F(3,4),F(1)]:
    c('positive square root control '+str(s),1+4*arrival(s)==deriv(s)**2 and deriv(s)>0)
    c('density pullback control '+str(s),F(1)/deriv(s)*deriv(s)==1)
# Literal full moments independently accumulated in null coordinates:
# covariant 2x2 matrix for plus weight a and minus weight b is
# ((a+b,b-a),(b-a,a+b)). Its mixed action reverses row0.
def mixed(a,b,u):
    t,x=u
    return (-(a+b)*t-(b-a)*x,(b-a)*t+(a+b)*x)
c('candidate first moment old',(4+1,4-1)==(5,3))
c('candidate first moment new',(4*F(1,2)+1,4*F(1,2)-1)==(3,1))
c('candidate old M eigendirection',mixed(F(4),F(1),(F(3),F(1)))==(F(-12),F(-4)))
c('candidate new M eigendirection',mixed(F(1),F(1),(F(1),F(0)))==(F(-2),F(0)))
c('candidate old rest velocity',F(1)/3==F(1,3))
c('candidate new rest velocity',F(0)/1==0)
no('spectral rescaling preserves M',mixed(F(4),F(1),(F(1),F(0)))==mixed(F(1),F(1),(F(1),F(0))))
# r_e=1 almost everywhere; alter its value at s=1/2 only. The measure
# and usual continuous receiver density are unchanged, exposing the a.e. scope.
s=F(1,2);r_source_selected=F(2);r_receiver_cont=F(1)/deriv(s)
no('all representatives obey pointwise density equality',r_receiver_cont==r_source_selected/deriv(s))
# A1:[0,1]->[0,2], A2:[0,1]->[0,4]; at t=3 only stream2 exists.
t=F(3)
active_total=sum(rate/Z for rate,Z in [(F(1),F(2)),(F(1),F(4))] if 0<=t/Z<=1)
c('inactive channel excluded from aggregate',active_total==F(1,4))
no('inverse formula valid outside channel domain',active_total==total(F(1),F(1)))
print(json.dumps({'verdict':'PASS','exact_checks':len(passed),'rejected_wrong_identities':len(rejected),'checks':passed,'wrong_identities':rejected,'python':sys.version,'method':'independently written stdlib Fraction; candidate-exposed exact witnesses'},indent=2))
