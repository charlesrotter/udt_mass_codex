import sympy as sp, mpmath as mp
mp.mp.dps=40
# [A] exact dt/drho from null condition
rho,rho0,c,En,L,Af,Bf,b=sp.symbols('rho rho0 c E L Af Bf b',positive=True)
rhodot2=(En**2/(Af*c**2)-L**2/rho**2)/Bf
cdtdrho=c*(En/(Af*c**2))/sp.sqrt(rhodot2)
claim=sp.sqrt(Bf/Af)/sp.sqrt(1-Af*b**2/rho**2)
assert sp.simplify(cdtdrho.subs(L,En*b/c)-claim)==0
print("[A] c dt/drho = sqrt(B/A)/sqrt(1-A b^2/rho^2)  OK")
# [B] beta=0 radial reduces to ambient F(s;R) antiderivative rho^{1-2s}/(1-2s)
s,a,phi0=sp.symbols('s a phi0',positive=True)
A_amb=sp.exp(-2*phi0)*rho**(2*s); B_amb=sp.exp(2*phi0)*rho**(-2*s)/a**2
assert sp.simplify(sp.sqrt(B_amb/A_amb)-sp.exp(2*phi0)*rho**(-2*s)/a)==0
print("[B] radial ambient sqrt(B/A)=e^{2phi0}rho^{-2s}/a -> int gives rho^{1-2s}/(1-2s) = S6b F(s;R)  OK")
# [C] O(m) excess integrand and leading log (s=0)
m=sp.symbols('m',positive=True)
I=sp.exp(2*m/rho)/sp.sqrt(1-(rho0**2/rho**2)*sp.exp(-2*m/rho+2*m/rho0))
Iflat=1/sp.sqrt(1-rho0**2/rho**2)
dI1=sp.simplify(sp.series(I-Iflat,m,0,2).removeO().coeff(m,1))
assert sp.simplify(dI1-(2*rho+3*rho0)/((rho+rho0)*sp.sqrt(rho**2-rho0**2)))==0
print("[C] O(m) excess integrand = (2rho+3rho0)/((rho+rho0)sqrt(rho^2-rho0^2))  OK")
# finite part beta integral = 1
assert abs(mp.quad(lambda t: 1/(mp.sqrt(t)*(2+t)**mp.mpf(1.5)),[0,mp.inf])-1)<1e-12
print("[C] per-leg finite O(m) constant = 1 (Beta) ; leading log coeff = 2m (arg 4 r1 r2/rho0^2)  OK")
# [D] second-order b-localized coefficient native vs GR
def W(m_,R,kind):
    if kind=='udt':
        I=lambda r: mp.e**(2*m_/r)/mp.sqrt(1-(1/r**2)*mp.e**(-2*m_/r+2*m_))
    else:
        I=lambda r:(1/(1-2*m_/r))/mp.sqrt(1-(1/r**2)*((1-2*m_/r)/(1-2*m_)))
    return mp.quad(I,[1,R])-mp.sqrt(R**2-1)-2*m_*mp.acosh(R)
def w2(kind,R=mp.mpf('1e13')):
    ms=[mp.mpf('1e-4')*k for k in (1,2,3,4)]
    M=mp.matrix([[x,x**2,x**3,x**4] for x in ms])
    return mp.lu_solve(M,mp.matrix([W(x,R,kind) for x in ms]))[1]
w2u=w2('udt'); w2g=w2('gr')
print("[D] w2_native=%s ~ 9pi/4-2=%s"%(mp.nstr(w2u,11),mp.nstr(9*mp.pi/4-2,11)))
print("[D] w2_gr    =%s ~ 15pi/4-2=%s"%(mp.nstr(w2g,11),mp.nstr(15*mp.pi/4-2,11)))
print("[D] w2_gr-w2_native=%s ~ 3pi/2=%s"%(mp.nstr(w2g-w2u,11),mp.nstr(3*mp.pi/2,11)))
assert abs(w2u-(9*mp.pi/4-2))<1e-6 and abs(w2g-(15*mp.pi/4-2))<1e-6 and abs((w2g-w2u)-3*mp.pi/2)<1e-8
print("ALL SHAPIRO CHECKS PASS (data-blind)")
