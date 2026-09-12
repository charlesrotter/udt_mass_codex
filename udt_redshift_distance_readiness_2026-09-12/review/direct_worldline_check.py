"""Independent Fraction/null-coordinate reconstruction of the parent witness.

No author/source-code imports. Integrate the normalized rapidity equations:
U^u=1/Z, U^v=Z, ds/du=1, hence d tau/ds=Z and dv/ds=Z^2.
Midpoint integration is exact for linear Z; Simpson is exact for quadratic Z^2.
The analytic proof, not these four finite controls, owns the general statement.
"""
from fractions import Fraction as Q
import json
import platform

rows=[]
for z0,eps,T,D in [(Q(2),Q(1,5),Q(1),Q(1)),
                   (Q(1),Q(0),Q(1),Q(1)),
                   (Q(2),Q(0),Q(2),Q(3)),
                   (Q(1),Q(1,5),Q(2),Q(3))]:
    zz=lambda ss:z0*(1+eps*ss/T)
    duration=T*zz(T/2)
    integrated_v=2*D+T*(zz(0)**2+4*zz(T/2)**2+zz(T)**2)/6
    # Candidate endpoint polynomial, evaluated independently of parent code.
    proposed_v=2*D+z0**2*(T+eps*T+eps**2*T/3)
    assert integrated_v==proposed_v
    t_end=(integrated_v+T)/2
    x_end=(integrated_v-T)/2
    assert t_end-T==x_end and x_end>=D>0
    nodes=[]
    for ss in [Q(0),T/2,T]:
        z=zz(ss)
        # Hyperbolic rapidity components expressed rationally via exp(eta)=z.
        Ut=(z+1/z)/2
        Ux=(z-1/z)/2
        norm=-Ut**2+Ux**2
        omega=Ut-Ux
        assert norm==-1 and omega==1/z and Ut>0
        assert z*omega==1
        nodes.append({'s':str(ss),'Z':str(z),'Ut':str(Ut),'Ux':str(Ux),
                      'norm':str(norm),'omega_o':str(omega)})
    relative=duration/(z0*T)-1
    assert relative==eps/2 and abs(relative)<=eps
    rows.append({'Z0':str(z0),'epsilon':str(eps),'T':str(T),'D':str(D),
                 'duration':str(duration),'initial_ratio_prediction':str(z0*T),
                 'relative_error':str(relative),'v_end':str(integrated_v),
                 't_end':str(t_end),'x_end':str(x_end),'nodes':nodes})
assert rows[0]['duration']=='11/5' and rows[0]['relative_error']=='1/10'
print(json.dumps({'python':platform.python_version(),'method':__doc__,
                  'arithmetic':'exact Fraction; no tolerances; four explicit controls',
                  'rows':rows,'status':'PASS'},indent=2))
