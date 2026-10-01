"""Finite geometric anchors for supplied space forms, not a native field selector.

Dimensionless k=1 normalizes units; the physical k remains free. No fitting or
field/ray campaign. Exact symbolic checks of embeddings, prepared clocks,
incidence derivatives and separate endpoint-frequency contractions.
"""
import json
import platform
import sympy as S

s,tau,a,L,rho,theta,az = S.symbols('s tau a L rho theta az',real=True)
w=S.symbols('w',positive=True)
checks=[]
def eq(name,got,want=0):
    residual=S.trigsimp(S.simplify(got-want))
    if residual!=0:raise AssertionError((name,residual))
    checks.append(name)
def dot(x,y,eta):return (x.T*eta*y)[0]
def vec(items):return S.Matrix(items)

# Full4D pullback and normal second fundamental form, both curvature signs.
spatial=vec([S.sin(theta)*S.cos(az),S.sin(theta)*S.sin(az),S.cos(theta)])
for sign in (1,-1):
    C=S.cos(rho) if sign==1 else S.cosh(rho)
    B=S.sin(rho) if sign==1 else S.sinh(rho)
    first=[C*S.sinh(s),C*S.cosh(s)] if sign==1 else [C*S.cos(s),C*S.sin(s)]
    X=vec(first+list(B*spatial))
    eta=S.diag(-1,sign,1,1,1)
    coords=[s,rho,theta,az]
    expected=S.diag(-C*C,1,B*B,B*B*S.sin(theta)**2)
    eq(f'quadric_{sign}',dot(X,X,eta),sign)
    for i,u in enumerate(coords):
        eq(f'normal_tangent_{sign}_{i}',dot(X,X.diff(u),eta))
        for j,v in enumerate(coords):
            eq(f'pullback_{sign}_{i}{j}',dot(X.diff(u),X.diff(v),eta),expected[i,j])
            eq(f'normal_second_form_{sign}_{i}{j}',dot(X.diff(u,v),X,eta),-expected[i,j])
    # Gaussian radial curvature computed from the lapse; full Gauss proof in text.
    eq(f'radial_section_curvature_{sign}',-S.diff(C,rho,2)/C,sign)

for sign in (1,-1):
    eta=S.diag(-1,sign,1)
    if sign==1:
        A=vec([S.sinh(s),S.cosh(s),0]);P=vec([0,S.cos(L),S.sin(L)])
        U=vec([1,0,0]);B=S.cosh(tau)*P+S.sinh(tau)*U
        F=S.cos(L)*S.cosh(s)*S.cosh(tau)-S.sinh(s)*S.sinh(tau)-1
        h=S.sqrt(1+w*w)
        # w=tan L>0; outgoing root cosh(tau)=h,sinh(tau)=w.
        root={S.sin(L):w/h,S.cos(L):1/h,S.sinh(tau):w,S.cosh(tau):h}
        Ar=vec([2*w/(1-w*w),(1+w*w)/(1-w*w),0])
        UAr=vec([(1+w*w)/(1-w*w),2*w/(1-w*w),0])
        q_expected=h/(1-w*w)
        returnroot={S.sinh(a):2*w/(1-w*w),S.cosh(a):(1+w*w)/(1-w*w)}
        p_function=1/S.cos(L);q_function=S.cos(L)/S.cos(2*L)
    else:
        A=vec([S.cos(s),S.sin(s),0]);P=vec([S.cosh(L),0,S.sinh(L)])
        U=vec([0,1,0]);B=S.cos(tau)*P+S.sin(tau)*U
        F=S.cosh(L)*S.cos(s)*S.cos(tau)+S.sin(s)*S.sin(tau)-1
        h=S.sqrt(1-w*w)
        # w=tanh L in(0,1); outgoing root cos(tau)=h,sin(tau)=w.
        root={S.sinh(L):w/h,S.cosh(L):1/h,S.sin(tau):w,S.cos(tau):h}
        Ar=vec([(1-w*w)/(1+w*w),2*w/(1+w*w),0])
        UAr=vec([-2*w/(1+w*w),(1-w*w)/(1+w*w),0])
        q_expected=h/(1+w*w)
        returnroot={S.sin(a):2*w/(1+w*w),S.cos(a):(1-w*w)/(1+w*w)}
        p_function=1/S.cosh(L);q_function=S.cosh(L)/S.cosh(2*L)
    A0=A.subs(s,0)
    eq(f'preparation_length_{sign}',dot(P.diff(L),P.diff(L),eta),1)
    eq(f'parallel_U_tangent_{sign}',dot(P,U,eta))
    eq(f'initial_clock_velocity_{sign}',(B.diff(tau).subs(tau,0)-U).norm()**2)
    eq(f'clock_A_unit_{sign}',dot(A.diff(s),A.diff(s),eta),-1)
    eq(f'clock_B_unit_{sign}',dot(B.diff(tau),B.diff(tau),eta),-1)
    for j in range(3):
        eq(f'clock_A_normal_acceleration_{sign}_{j}',A.diff(s,2)[j],sign*A[j])
        eq(f'clock_B_normal_acceleration_{sign}_{j}',B.diff(tau,2)[j],sign*B[j])
    eq(f'incidence_inner_product_{sign}',dot(A,B,eta),sign*(F+1))
    eq(f'first_emission_symmetry_{sign}',F.xreplace({s:tau,tau:s}),F)
    eq(f'outgoing_root_{sign}',F.subs(s,0).subs(root))
    p=S.cancel((-S.diff(F,s)/S.diff(F,tau)).subs(s,0).subs(root))
    eq(f'implicit_outgoing_slope_{sign}',p,h)
    Fret=F.subs(s,a)
    eq(f'return_root_{sign}',Fret.subs(root).subs(returnroot))
    q=S.cancel((-S.diff(Fret,tau)/S.diff(Fret,a)).subs(root).subs(returnroot))
    eq(f'implicit_return_slope_{sign}',q,q_expected)
    Br=B.subs(root);UBr=B.diff(tau).subs(root)
    kout=Br-A0;kin=Ar-Br
    eq(f'outgoing_null_chord_{sign}',dot(kout,kout,eta))
    eq(f'return_null_chord_{sign}',dot(kin,kin,eta))
    eq(f'endpoint_frequency_outgoing_{sign}',dot(kout,U,eta)/dot(kout,UBr,eta),p)
    eq(f'endpoint_frequency_return_{sign}',dot(kin,UBr,eta)/dot(kin,UAr,eta),q)
    eq(f'outgoing_log_series_{sign}',S.series(S.log(p_function),L,0,6).removeO(),sign*L**2/2+L**4/12)
    eq(f'return_log_series_{sign}',S.series(S.log(q_function),L,0,6).removeO(),3*sign*L**2/2+5*L**4/4)

# Flat regular branch and scalar typing checks.
eq('flat_arrival_derivative',S.diff(s+L,s),1)
eq('flat_echo_derivative',S.diff(tau+L,tau),1)
eq('positive_clock_kernel_typing',(S.cos(L)**2-1)/(S.cos(L)**2+1),-S.sin(L)**2/(1+S.cos(L)**2))
eq('first_leg_ratio_at_echo_limit',1/S.cos(S.pi/4),S.sqrt(2))

print(json.dumps({'status':'PASS','check_count':len(checks),'checks':checks,
 'python':platform.python_version(),'sympy':S.__version__,
 'scope':'Exact geometric algebra for supplied constant-curvature clocks; analytic branch/causal/domain arguments remain in the proof. No native selection, observational fit or finite-distance UDT prediction.'},indent=2))
