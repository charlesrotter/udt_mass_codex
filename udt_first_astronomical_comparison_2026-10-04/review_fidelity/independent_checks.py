"""ACP1 source-fidelity arithmetic; independent implementation, no parent imports.
Source numbers manually transcribed from primary PDF tables before execution.
CPU Decimal80; finite controls do not assert a physical metric realization.
"""
import decimal, hashlib, json, platform, resource, sys
from pathlib import Path
D=decimal.Decimal
decimal.getcontext().prec=80
resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
HERE=Path(__file__).resolve().parent
c=D('299792.458')
checks=[]
def check(name, ok, details=None):
    checks.append({'name':name,'pass':bool(ok),'details':details})
    if not ok: raise AssertionError(name)

def row(v):
    v=D(v); z=v/c; Z=1+z; phi=-Z.ln()
    chi=(1-Z*Z)/(1+Z*Z)
    ex=(2*phi).exp()
    check('chi rational vs exponential '+str(v),abs(chi-(ex-1)/(ex+1))<D('1e-75'))
    return {k:str(val) for k,val in {'v_km_s':v,'z':z,'Z':Z,'phi_clock':phi,'chi_clock':chi}.items()}
summary=[row(v) for v in ['7170.3','7172.2','7174.1']]
spots=[row(v) for v in ['6007.40','6009.41','6897.66','6899.68','7650.97','7652.97']]
check('CGCG barycentric center plus source offset',D('6908.9')+D('263.3')==D('7172.2'))
check('distance percentile endpoints',D('87.6')-D('7.2')==D('80.4') and D('87.6')+D('7.9')==D('95.5'))
check('phi and chi reverse positive-velocity ordering',all(D(summary[i]['phi_clock'])>D(summary[i+1]['phi_clock']) and D(summary[i]['chi_clock'])>D(summary[i+1]['chi_clock']) for i in range(2)))
areas=[]
for d in ['80.4','87.6','95.5']:
    area=D(d)**2
    areas.append({'D_Mpc':d,'abs_det_B_Mpc2_at_omega_o_1':str(area)})
    check('area roundtrip '+d,area.sqrt()==D(d))
for scale in ['0.125','1','8']:
    a=D(scale); d=D('87.6'); b11=d/a;b22=d/a
    check('affine determinant area '+scale,a*a*b11*b22==d*d)
# Equal area does not imply full spot map: an explicit one-axis angle.
d=D('87.6'); theta=[D('0.001'),D('0')]
image1=[d*theta[0],d*theta[1]]
image2=[2*d*theta[0],d*theta[1]/2]
check('same-area anisotropic map changes spot',d*d==(2*d)*(d/2) and image1!=image2)

# Evaluate reception-time slopes by constructing and INVERTING t(s), then
# finite-differencing V(t), separately from the candidate's chain-rule RHS.
# Z(s)=K(1+s)^2, alpha(s)=1+b*s. Positive on the tested neighborhood.
h=D('1e-20'); s=D('0.2'); drift=[]
for K in [D(1),D('1.023923884036468')] :
  for b in [D(0),D('0.1')]:
    t=K*((1+s)**3-1)/3
    def velocity_at_reception(tau):
      se=(1+3*tau/K)**(D(1)/D(3))-1
      return c*(K*(1+se)**2/(1+b*se)-1)
    actual=(velocity_at_reception(t+h)-velocity_at_reception(t-h))/(2*h)
    alpha=1+b*s
    expected=c*(2/((1+s)*alpha)-b/(alpha*alpha))
    error=abs(actual-expected)
    check('reception inverse finite derivative '+str(K)+' '+str(b),error < D('1e-30'),str(error))
    drift.append({'K':str(K),'alpha_slope':str(b),'actual':str(actual),'expected':str(expected),'absolute_error':str(error)})
# Fault catches: extra bulk division and missing source-cadence term.
base=D(drift[2]['expected']); wrong_bulk=base/D(drift[2]['K'])
check('catch extra bulk slowdown',abs(base-wrong_bulk)>D('1000'))
alpha=1+D('0.1')*s
wrong_alpha=c*2/((1+s)*alpha)
check('catch missing cadence term',abs(D(drift[1]['expected'])-wrong_alpha)>D('1000'))
# Printed six-row flags and uncertainties from Table4; not full data.
a=[D(x) for x in ['0.082','0.020','4.580','4.140','-0.106','0.285']]
sig=[D(x) for x in ['1.758','2.164','1.030','1.071','0.734','0.657']]
flags=[0,0,1,1,1,1]
# Deliberate arithmetic fixture residual=1 and positive floor=1. The quantity
# below is only the measured-acceleration contribution minus common log2pi.
terms=[1/(x*x+1)+(x*x+1).ln() for x in sig]
masked=sum(terms[j] for j in range(6) if flags[j]==1)
explicit=terms[2]+terms[3]+terms[4]+terms[5]
check('printed acceleration flags',sum(flags)==4 and masked==explicit)
check('catch treating modeled accelerations as data',sum(terms)-masked>0)
# Source p21 published count inconsistency is an observation, not a corrected fit.
check('p21 narrative arithmetic mismatch',4*(71+50+45)-20==644 and 644!=604 and 16+2*(71+50+45)+20==368 and 368!=348)

result={'reviewer':'/root/acp_fidelity','python':sys.version,'platform':platform.platform(),'decimal_precision':80,'implementation':'No parent code imported/read before run; manually transcribed primary source inputs.','finite_check_cases':len(checks),'summary_CMB':summary,'printed_spots_barycentric':spots,'areas':areas,'drift_controls':drift,'printed_acceleration_mask_nll_without_log2pi':str(masked),'checks':checks,'all_pass':all(x['pass'] for x in checks),'limits':['No full Table4 or full source likelihood','No posterior fit or source pipeline replay','No physical metric selected or implied by algebraic controls','No formal interval certificate','No registry/source grade upgrade']}
(HERE/'INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'all_pass':result['all_pass'],'finite_check_cases':len(checks),'summary_center':summary[1],'areas':areas,'max_drift_absolute_error':str(max(D(x['absolute_error']) for x in drift))},indent=2))
