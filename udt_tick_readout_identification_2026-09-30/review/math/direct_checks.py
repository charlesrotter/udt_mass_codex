from pathlib import Path
from fractions import Fraction as F
import hashlib,json
root=Path(__file__).resolve().parents[3]
package=root/'udt_tick_readout_identification_2026-09-30'
local=Path(__file__).resolve().parent
checks=[]
def eq(name,a,b):
    assert a==b,(name,a,b)
    checks.append(name)
freeze=json.loads((package/'CANDIDATE_FREEZE.json').read_text())
for path,h in freeze['sha256'].items():
    eq('candidate frozen bytes '+path,hashlib.sha256((root/path).read_bytes()).hexdigest(),h)
sf=json.loads((local/'SOURCE_FIRST_FREEZE.json').read_text())
for path,h in sf['files'].items():
    eq('source-first frozen bytes '+path,hashlib.sha256((local/path).read_bytes()).hexdigest(),h)
kp=[F(1),F(1),F(0),F(0)]; km=[F(1),F(-1),F(0),F(0)]
def cov(k):return [-k[0],*k[1:]]
def moment(beams):return [[sum(w*cov(k)[a]*cov(k)[b] for w,k in beams) for b in range(4)] for a in range(4)]
M=moment([(4,kp),(1,km)])
half=[x/2 for x in kp]
Mn=moment([(4,half),(1,km)])
def mixed_apply(M,u):return [(-1 if a==0 else 1)*sum(M[a][b]*u[b] for b in range(4)) for a in range(4)]
um_unscaled=[F(3),F(1),F(0),F(0)]
eq('old unit-normalizer squared',-um_unscaled[0]**2+um_unscaled[1]**2,-8)
eq('old eigenpair without radical',mixed_apply(M,um_unscaled),[-4*x for x in um_unscaled])
eq('new eigenpair',mixed_apply(Mn,[F(1),F(0),F(0),F(0)]),[-2,0,0,0])
J=[4*a+b for a,b in zip(kp,km)]
Jn=[4*a+b for a,b in zip(half,km)]
eq('current velocities',(J[1]/J[0],Jn[1]/Jn[0]),(F(3,5),F(1,3)))
eq('old and new moment velocities',(um_unscaled[1]/um_unscaled[0],F(0)),(F(1,3),F(0)))
eq('aggregate constants',(1/F(2)+1/F(4),3/F(2)+1/F(4)),(F(3,4),F(7,4)))
eq('normalized aggregates',(F(3,4)/2,F(7,4)/4),(F(3,8),F(7,16)))
t=F(1,2)
starts=[F(0),F(2)]; ends=[F(1),F(3)]
active=[j for j in range(2) if starts[j]<=t<=ends[j]]
eq('active support set',active,[0])
formal_inverse=t-2
eq('second inverse outside emission domain',0<=formal_inverse<=1,False)
eq('correct aggregate density on first window',sum(F(1) for j in active),F(1))
eq('unrestricted algebraic inverse extension gives wrong sum',sum(F(1) for j in range(2))!=F(1),True)
print(json.dumps({'status':'PASS','checks':checks,'check_count':len(checks),'support_defect':{'emission_intervals':['[0,1]','[0,1]'],'arrival_windows':['[0,1]','[2,3]'],'receiving_time':'1/2','active_streams':[1],'correct_rate':'1','invalid_formal_second_inverse':'-3/2'},'arithmetic':'fractions.Fraction exact'},indent=2))
