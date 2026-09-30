"""Post-exposure independent sphere integration and exact4:1 frame projections."""
import json
import platform
import sympy as s

identities={}
rejections={}
def eq(name,a,b=0):
    residual=s.simplify(a-b)
    assert residual == 0, (name,residual)
    identities[name]=str(residual)
def neq(name,a):
    residual=s.simplify(a)
    assert residual != 0, (name,residual)
    rejections[name]=str(residual)

z,phi,eps=s.symbols('z phi eps',real=True)
P=s.legendre(4,z)
F=1+eps*P
n=s.Matrix([s.sqrt(1-z*z)*s.cos(phi),s.sqrt(1-z*z)*s.sin(phi),z])
k=s.Matrix([1,*n])
def sphere(expr):
    return s.simplify(s.integrate(s.integrate(s.expand(expr),(phi,0,2*s.pi)),(z,-1,1)))

first=[sphere(F*k[i]) for i in range(4)]
second=s.zeros(4)
for i in range(4):
    eq('sphere-first-'+str(i),first[i],4*s.pi if i==0 else 0)
    for j in range(i,4):
        second[i,j]=second[j,i]=sphere(F*k[i]*k[j])
        target=4*s.pi if i==j==0 else (4*s.pi/3 if i==j else 0)
        eq('sphere-second-'+str(i)+str(j),second[i,j],target)
fourth_z=sphere(F*n[2]**4)/(4*s.pi)
fourth_x=sphere(F*n[0]**4)/(4*s.pi)
eq('axial-fourth-normalized',fourth_z,s.Rational(1,5)+eps*s.Rational(8,315))
eq('transverse-fourth-normalized',fourth_x,s.Rational(1,5)+eps*s.Rational(1,105))
eq('fourth-direction-contrast',fourth_z-fourth_x,eps/63)
neq('moment-isotropy-not-distribution-isotropy',fourth_z-fourth_x)
critical=s.solve(s.diff(P,z),z)
values=[s.simplify(P.subs(z,x)) for x in [-1,1,*critical]]
assert set(values)=={s.Integer(1),s.Rational(3,8),-s.Rational(3,7)},values
identities['complete-critical-values-on-compact-interval']=str(values)
eq('positive-factor-lower-bound-eps-positive',1+s.Rational(1,1)*(-s.Rational(3,7)),s.Rational(4,7))

G=s.diag(-1,1,1,1)
kp=s.Matrix([1,1,0,0]);km=s.Matrix([1,-1,0,0])
T=4*(G*kp)*(G*kp).T+(G*km)*(G*km).T
J=4*kp+km
UJ=J/s.sqrt(-(J.T*G*J)[0])
UM=s.Matrix([3,1,0,0])/(2*s.sqrt(2))
NJ=s.Matrix([3,5,0,0])/4
NM=s.Matrix([1,3,0,0])/(2*s.sqrt(2))
eq('J-norm',(UJ.T*G*UJ)[0],-1)
eq('M-norm',(UM.T*G*UM)[0],-1)
eq('J-current-frame-flux',(UJ.T*T*NJ)[0],3)
eq('M-rest-frame-flux',(UM.T*T*NM)[0],0)
eq('M-density',(UM.T*T*UM)[0],4)
eq('J-density',(UJ.T*T*UJ)[0],5)
neq('M-observer-not-J-observer',UJ[1]/UJ[0]-UM[1]/UM[0])
H=s.diag(2,2,0,0)
Mcov=G*second*G
recip=s.trace(G*Mcov*G*H)
eq('smooth-P4-DDR-positive',recip,32*s.pi/3)
neq('smooth-moment-isotropy-not-DDR',recip)

print(json.dumps({'status':'PASS','python':platform.python_version(),'sympy':s.__version__,
 'identities':identities,'nonidentities':rejections,
 'values':{'angular_first':str(first),'angular_second_contravariant':str(second),
 'normalized_axial_fourth':str(fourth_z),'normalized_transverse_fourth':str(fourth_x),
 'P4_critical_values':str(values),'UJ':str(UJ),'UM':str(UM)},
 'limits':'exact supplied controls, not a physical kinetic or clock-response derivation'},indent=2))
