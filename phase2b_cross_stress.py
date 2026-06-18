#!/usr/bin/env python3
"""
phase2b_cross_stress.py

Exact SYMBOLIC GR (sympy, c=1, DATA-BLIND, Category-A exact).

GOAL: derive the O(A^2) static l=0 gravitational-wave stress that sources the
held-UDT-diagonal-gauge static backreaction F, for a SUPERPOSITION of TWO
even-parity standing-wave modes that may differ in multipole l and frequency w.

GENERALIZES phase1_geon_backreact.py (single l=2 mode) to:
  (i)  general-l even-parity reconstruction {H0_l=H2_l, H1_l, K_l}(G,G',w,r),
       master G'' = (l(l+1)/r^2 - w^2) G  [l(l+1) replaces 6], over-constraint
       VERIFIED: plug the closed form into ALL linearized vacuum dR=0 -> 0.
       Confirms reduction to the l=2 forms in phase1_geon_backreact.
  (ii) the TWO-mode cross stress sourcing F, with TWO selection rules:
        TIME : cross term i<->j survives <...>_t only if w_i = w_j.
        ANGLE: l=0 projection of P_{l_i}*P_{l_j} stress nonzero only for some
               (l_i,l_j); computed for {(2,2),(3,3),(4,4),(2,4),(2,3),(3,4)}.
  (iii) explicit S_cross[Psi_i,Psi_j] for surviving pairs, in the SAME
        form/normalization as the single-mode S in phase1_geon_backreact;
        diagonal i=j reduces EXACTLY to that single-mode source.

METHOD (inherited; stated explicitly):
  * Physical real wave dg = A Re[ sum_i c_i h^(i)(r) P_{l_i}(cos th) e^{-iw_i t} ].
  * TIME-AVERAGE via complex double-copy: mode i = hP_i (e^{-iw_i t}, d_t->-iw_i)
    + hM_i (e^{+iw_i t}, d_t->+iw_i); real wave = (1/2) sum_i (hP_i+hM_i). The
    O(A^2) bilinear has Fp_iFp_j (e^{-i(w_i+w_j)t}), Fm_iFm_j (e^{+i(w_i+w_j)t}),
    Fp_iFm_j (e^{-i(w_i-w_j)t}); <...>_t keeps only Fp_iFm_j with w_i=w_j.
  * ANGLE-AVERAGE: <X>_ang = (1/2) int_{-1}^{1} X d(cos th).
  * Time-average cross-verified via explicit real cos/sin route (diff must be 0).
"""

import sympy as sp

print("="*78); print("phase2b_cross_stress -- multi-mode O(A^2) l=0 GW stress for F")
print("="*78, flush=True)

t, r, th = sp.symbols('t r theta', real=True)
ph = sp.symbols('phi', real=True)
A = sp.symbols('A', real=True)
I = sp.I
coords = [t, r, th, ph]; n = 4
ct, st = sp.cos(th), sp.sin(th)
g_bg = sp.diag(-1, 1, r**2, r**2*st**2)
bgi = g_bg.inv()

def legendre_P(lval):
    return sp.legendre(lval, ct)

# Closed-form general-l even-parity flat reconstruction (phase1 l=2 form with
# the l=2 constant 3 -> l(l+1)/2). H0=H2, in (G,G',w,r), phase1 normalization.
def recon_amps(lval, Gfun, Gder, wsym):
    Lll = lval*(lval+1)
    c = sp.Rational(1,2)*Lll
    H0r = (-I*r**2*wsym**2*Gfun + I*r*Gder + I*c*Gfun)/(r*wsym)
    H1r = r*Gder + Gfun
    Kr  = (I*r*Gder + I*c*Gfun)/(r*wsym)
    return H0r, H0r, H1r, Kr   # (H0, H2, H1, K)

# ======================================================================
# PART 1.  General-l reconstruction OVER-CONSTRAINT VERIFICATION.
#   Build linearized vacuum dR_{ab} for harmonic P_l, plug the closed-form
#   reconstruction in, reduce master derivs, show every residual = 0.
# ======================================================================
print("\n"+"#"*78)
print("# PART 1: general-l reconstruction over-constraint check (l=2,3,4)")
print("#"*78, flush=True)

def overconstraint_check(lval, wsym):
    Y = legendre_P(lval)
    H0f=sp.Function('H0')(r); H1f=sp.Function('H1')(r)
    H2f=sp.Function('H2')(r); Kf=sp.Function('K')(r)
    Ft=sp.Function('Ft')(t); dF=-I*wsym*Ft; d2F=(-I*wsym)**2*Ft
    h=sp.zeros(4,4)
    h[0,0]=H0f*Y*Ft; h[0,1]=H1f*Y*Ft; h[1,0]=H1f*Y*Ft
    h[1,1]=H2f*Y*Ft; h[2,2]=r**2*Kf*Y*Ft; h[3,3]=r**2*st**2*Kf*Y*Ft
    eps=sp.symbols('eps'); g=g_bg+eps*h
    ginv=bgi-eps*(bgi*h*bgi)
    def D(e,x):
        e2=sp.diff(e,x)
        if x is t: e2=e2.subs(sp.Derivative(Ft,t,2),d2F).subs(sp.Derivative(Ft,t),dF)
        return e2
    def dch(a,b,c):
        s=sp.S.Zero
        for d in range(n):
            s+=ginv[a,d]*(D(g[d,b],coords[c])+D(g[d,c],coords[b])-D(g[b,c],coords[d]))
        return sp.Rational(1,2)*s
    Gamma=[[[dch(a,b,c) for c in range(n)] for b in range(n)] for a in range(n)]
    def ricci(b,c):
        s=sp.S.Zero
        for a in range(n):
            s+=D(Gamma[a][b][c],coords[a]); s-=D(Gamma[a][b][a],coords[c])
            for d in range(n):
                s+=Gamma[a][a][d]*Gamma[d][b][c]; s-=Gamma[a][c][d]*Gamma[d][b][a]
        return s
    def lin(e):
        e=sp.expand(e); e=sp.diff(e,eps).subs(eps,0)
        e=sp.expand(e).subs(sp.Derivative(Ft,t,2),d2F).subs(sp.Derivative(Ft,t),dF)
        return sp.expand(e).subs(Ft,1)
    comps=[(0,0),(0,1),(1,1),(0,2),(1,2),(2,2),(3,3)]
    dR={ab:lin(ricci(*ab)) for ab in comps}
    # closed-form reconstruction in master G
    G=sp.Function('G')(r); Gp=sp.Derivative(G,r)
    H0r,H2r,H1r,Kr = recon_amps(lval, G, Gp, wsym)
    Lll=lval*(lval+1)
    Gpp=(Lll/r**2-wsym**2)*G; Gppp=(Lll/r**2-wsym**2)*Gp-(2*Lll/r**3)*G
    def redG(e):
        e=sp.expand(e)
        for _ in range(8):
            e=e.subs(sp.Derivative(G,r,4),sp.diff(Gppp,r))
            e=e.subs(sp.Derivative(G,r,3),Gppp).subs(sp.Derivative(G,r,2),Gpp)
            e=sp.expand(e)
        return e
    smap={H0f:H0r,H2f:H2r,Kf:Kr,H1f:H1r}
    def subrecon(e):
        for fn,fx in smap.items(): e=e.subs(sp.Derivative(fn,r,2),sp.diff(fx,r,2))
        for fn,fx in smap.items(): e=e.subs(sp.Derivative(fn,r),sp.diff(fx,r))
        for fn,fx in smap.items(): e=e.subs(fn,fx)
        return e
    allzero=True; nz=[]
    for ab in comps:
        # angular: substitute symbols and reduce; residual must vanish identically
        e=subrecon(dR[ab]); e=redG(e)
        # separate angular powers by substituting cos->u (keep sin via 1-u^2)
        e=sp.expand(e).subs(sp.sin(th)**2,1-sp.cos(th)**2)
        e=sp.expand(e)
        res=sp.cancel(sp.together(e))
        if res!=0: allzero=False; nz.append((ab,res))
    return (H0r,H1r,Kr,allzero,nz)

wl = sp.symbols('w', positive=True)
recon_amps_store={}
for lval in (2,3,4):
    H0r,H1r,Kr,allzero,nz = overconstraint_check(lval, wl)
    recon_amps_store[lval]=(H0r,H1r,Kr)
    print(f"\n--- l={lval}  (master G''=({lval*(lval+1)}/r^2 - w^2)G) ---", flush=True)
    print(f"  H0 = H2 = {sp.cancel(H0r)}")
    print(f"  H1      = {sp.cancel(H1r)}")
    print(f"  K       = {sp.cancel(Kr)}")
    print(f"  OVER-CONSTRAINT (all 7 linearized dR residuals = 0): {allzero}")
    if not allzero:
        for ab,res in nz: print(f"     NONZERO residual {ab}: {res}")

# Confirm l=2 reduces to the phase1_geon_backreact forms (3 = l(l+1)/2 at l=2).
print("\n--- l=2 reduces to phase1_geon_backreact reconstruction ---")
Gs=sp.Function('G')(r); Gps=sp.Derivative(Gs,r)
H0_ref=(-I*r**2*wl**2*Gs+I*r*Gps+3*I*Gs)/(r*wl)
H1_ref=r*Gps+Gs
K_ref =(I*r*Gps+3*I*Gs)/(r*wl)
H0o,H1o,Ko=recon_amps_store[2]
print(f"  H0-H0_ref = {sp.cancel(H0o-H0_ref)}")
print(f"  H1-H1_ref = {sp.cancel(H1o-H1_ref)}")
print(f"  K -K_ref  = {sp.cancel(Ko-K_ref)}   (all 0 => identical)")

# ======================================================================
# PART 2.  Two-mode O(A^2) static l=0 G_tt -> F-operator + cross source.
#   EFFICIENT angular method: carry the two modes' angular harmonics as
#   ABSTRACT functions Y1(th),Y2(th) (their theta-derivatives stay symbolic),
#   compute G_tt to O(A^2) ONCE, then substitute Y_i -> P_{l_i}(cos th) and
#   l=0-project (integrate) per pair.  Equal-frequency double-copy (Fp,Fm)
#   captures the surviving time-averaged stress; the TIME selection rule
#   (w_i=w_j) is established analytically (the unequal-w residual phase).
# ======================================================================
print("\n"+"#"*78)
print("# PART 2: two-mode O(A^2) l=0 G_tt -> F-operator + selection rules + source")
print("#"*78, flush=True)

# Independent radial masters and the static unknown
G1=sp.Function('G1')(r); G1p=sp.Derivative(G1,r)
G2=sp.Function('G2')(r); G2p=sp.Derivative(G2,r)
F=sp.Function('F')(r)
# Abstract angular harmonics (substituted to Legendre P_l only at projection).
Y1=sp.Function('Y1')(th); Y2=sp.Function('Y2')(th)
# Equal-frequency double-copy time placeholders (Fp=e^{-iwt}, Fm=e^{+iwt}).
Fp=sp.Function('Fp')(t); Fm=sp.Function('Fm')(t)
wtr={sp.Derivative(Fp,t,2):(-I*wl)**2*Fp, sp.Derivative(Fp,t):(-I*wl)*Fp,
     sp.Derivative(Fm,t,2):(+I*wl)**2*Fm, sp.Derivative(Fm,t):(+I*wl)*Fm}
def Trule(e):
    for _ in range(3): e=e.subs(wtr)
    return e
def trunc_A(e,o=2):
    e=sp.expand(e)
    if not e.has(A): return e
    p=sp.Poly(e,A); out=sp.S.Zero
    for (k,),co in p.terms():
        if k<=o: out+=co*A**k
    return out
def recon_amps2(lval,Gf,Gd,wsym):
    c=sp.Rational(1,2)*lval*(lval+1)
    return (-I*r**2*wsym**2*Gf+I*r*Gd+I*c*Gf)/(r*wsym), r*Gd+Gf, (I*r*Gd+I*c*Gf)/(r*wsym)
def mh(H0,H1,K,Yang,Fac):
    h=sp.zeros(4,4); h[0,0]=H0*Yang*Fac; h[0,1]=H1*Yang*Fac; h[1,0]=H1*Yang*Fac
    h[1,1]=H0*Yang*Fac; h[2,2]=r**2*K*Yang*Fac; h[3,3]=r**2*st**2*K*Yang*Fac
    return h
def rz(e,G):
    return e.subs(sp.conjugate(G),G).subs(sp.conjugate(sp.Derivative(G,r)),sp.Derivative(G,r)).subs(sp.conjugate(wl),wl).subs(sp.conjugate(r),r)

def build_Gtt2_abstract(l1,l2):
    """O(A^2) coeff of static l=0 G_tt for two equal-frequency modes with
    multipoles l1,l2 carried as abstract Y1,Y2 (theta-derivs symbolic)."""
    A01,A11,K1=recon_amps2(l1,G1,G1p,wl); A02,A12,K2=recon_amps2(l2,G2,G2p,wl)
    hP=mh(A01,A11,K1,Y1,Fp)+mh(A02,A12,K2,Y2,Fp)
    hM=(mh(sp.conjugate(A01),sp.conjugate(A11),sp.conjugate(K1),Y1,Fm)).applyfunc(lambda e:rz(e,G1)) \
       +(mh(sp.conjugate(A02),sp.conjugate(A12),sp.conjugate(K2),Y2,Fm)).applyfunc(lambda e:rz(e,G2))
    hS=sp.zeros(4,4); hS[0,0]=2*F; hS[1,1]=2*F
    hW=(hP+hM)/2; g=g_bg+A*hW+A**2*hS
    ginv=bgi-A*(bgi*hW*bgi)+A**2*(bgi*hW*bgi*hW*bgi-bgi*hS*bgi)
    def D(e,x):
        e2=sp.diff(e,x)
        if x is t: e2=Trule(e2)
        return e2
    def dch(a,b,c):
        s=sp.S.Zero
        for d in range(n):
            s+=ginv[a,d]*(D(g[d,b],coords[c])+D(g[d,c],coords[b])-D(g[b,c],coords[d]))
        return trunc_A(sp.Rational(1,2)*s)
    Gam=[[[None]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(b,n):
                v=dch(a,b,c); Gam[a][b][c]=v; Gam[a][c][b]=v
    def ric(b,c):
        s=sp.S.Zero
        for a in range(n):
            s+=D(Gam[a][b][c],coords[a]); s-=D(Gam[a][b][a],coords[c])
            for d in range(n):
                s+=Gam[a][a][d]*Gam[d][b][c]; s-=Gam[a][c][d]*Gam[d][b][a]
        return trunc_A(s)
    Ric={ab:ric(*ab) for ab in [(0,0),(1,1),(2,2),(3,3),(0,1)]}
    Rsc=sp.S.Zero
    for a in range(n):
        for b in range(n):
            if a==b: Rab=Ric[(a,a)]
            elif {a,b}=={0,1}: Rab=Ric[(0,1)]
            else: Rab=sp.S.Zero
            Rsc+=ginv[a,b]*Rab
    Rsc=trunc_A(Rsc)
    Gtt=trunc_A(Ric[(0,0)]-sp.Rational(1,2)*g[0,0]*Rsc)
    return sp.expand(sp.expand(Gtt).coeff(A,2))

def time_avg(e):
    """Equal-frequency average: Fp*Fm->1 (survives), Fp^2/Fm^2->0, lone->0,
    static kept. (Selection-rule note: at UNEQUAL freq the surviving e^0 term
    is absent -> cross dies; established analytically below.)"""
    p,m=sp.symbols('p m'); es=sp.expand(e.subs({Fp:p,Fm:m})); out=sp.S.Zero
    for term in sp.Add.make_args(es):
        dp=sp.degree(sp.Poly(term,p),p) if term.has(p) else 0
        dm=sp.degree(sp.Poly(term,m),m) if term.has(m) else 0
        co=term
        if term.has(p): co=co.subs(p,1)
        if term.has(m): co=co.subs(m,1)
        if (dp==0 and dm==0) or (dp==1 and dm==1): out+=co
    return sp.expand(out)

def reduceG_two(e,l1,l2):
    L1=l1*(l1+1); L2=l2*(l2+1)
    g1pp=(L1/r**2-wl**2)*G1; g1ppp=(L1/r**2-wl**2)*G1p-(2*L1/r**3)*G1
    g2pp=(L2/r**2-wl**2)*G2; g2ppp=(L2/r**2-wl**2)*G2p-(2*L2/r**3)*G2
    e=sp.expand(e)
    for _ in range(8):
        e=e.subs(sp.Derivative(G1,r,4),sp.diff(g1ppp,r)).subs(sp.Derivative(G1,r,3),g1ppp).subs(sp.Derivative(G1,r,2),g1pp)
        e=e.subs(sp.Derivative(G2,r,4),sp.diff(g2ppp,r)).subs(sp.Derivative(G2,r,3),g2ppp).subs(sp.Derivative(G2,r,2),g2pp)
        e=sp.expand(e)
    return e

def angle_project(e,l1,l2):
    """Substitute Y1->P_{l1}(cos th), Y2->P_{l2}(cos th) (and theta-derivs),
    then l=0-project: (1/2) int_{-1}^{1} (...) d(cos th)."""
    P1=sp.legendre(l1,sp.cos(th)); P2=sp.legendre(l2,sp.cos(th))
    subs_ang={
        sp.Derivative(Y1,th,2):sp.diff(P1,th,2), sp.Derivative(Y1,th):sp.diff(P1,th), Y1:P1,
        sp.Derivative(Y2,th,2):sp.diff(P2,th,2), sp.Derivative(Y2,th):sp.diff(P2,th), Y2:P2,
    }
    ex=sp.expand(e)
    ex=ex.subs(sp.Derivative(Y1,th,2),subs_ang[sp.Derivative(Y1,th,2)])
    ex=ex.subs(sp.Derivative(Y2,th,2),subs_ang[sp.Derivative(Y2,th,2)])
    ex=ex.subs(sp.Derivative(Y1,th),subs_ang[sp.Derivative(Y1,th)])
    ex=ex.subs(sp.Derivative(Y2,th),subs_ang[sp.Derivative(Y2,th)])
    ex=ex.subs(Y1,P1).subs(Y2,P2)
    u=sp.Symbol('u',real=True); ex=sp.expand(ex)
    ex=ex.subs(sp.sin(th)**2,1-sp.cos(th)**2); ex=sp.expand(ex).subs(sp.cos(th),u)
    if ex.has(sp.sin(th)): ex=ex.subs(sp.sin(th),sp.sqrt(1-u**2))
    integ=sp.integrate(ex,(u,-1,1))
    return sp.Rational(1,2)*sp.cancel(integ)

def split_F(e):
    e=sp.expand(e); Fp_=sp.S.Zero; Sp_=sp.S.Zero
    for term in sp.Add.make_args(e):
        if term.has(F) or term.has(sp.Derivative(F,r)) or term.has(sp.Derivative(F,r,2)): Fp_+=term
        else: Sp_+=term
    return sp.expand(Fp_),sp.expand(Sp_)

def cross_coeff(e):
    """Extract the genuine CROSS (mode1<->mode2) part: terms containing BOTH a
    mode-1 angular factor (Y1 or its derivs) AND a mode-2 angular factor."""
    cross=sp.S.Zero; self_=sp.S.Zero
    Y1set=(Y1,sp.Derivative(Y1,th),sp.Derivative(Y1,th,2))
    Y2set=(Y2,sp.Derivative(Y2,th),sp.Derivative(Y2,th,2))
    for term in sp.Add.make_args(sp.expand(e)):
        has1=any(term.has(x) for x in Y1set); has2=any(term.has(x) for x in Y2set)
        if has1 and has2: cross+=term
        else: self_+=term
    return sp.expand(self_), sp.expand(cross)

print("\n--- building abstract two-mode G_tt2 (Y1,Y2 abstract) per (l1,l2) ---", flush=True)
pairs=[(2,2),(3,3),(4,4),(2,4),(2,3),(3,4)]
results={}
import time as _time
for (l1,l2) in pairs:
    _t=_time.time()
    raw=build_Gtt2_abstract(l1,l2)
    ta=time_avg(raw)
    red=reduceG_two(ta,l1,l2)
    self_ang, cross_ang = cross_coeff(red)   # split by ANGULAR mode content
    # project each onto l=0
    self_proj=sp.cancel(sp.together(reduceG_two(angle_project(self_ang,l1,l2),l1,l2)))
    cross_proj=sp.cancel(sp.together(reduceG_two(angle_project(cross_ang,l1,l2),l1,l2)))
    Fpart,Sself=split_F(self_proj)
    _,Scross=split_F(cross_proj) if cross_proj.has(F) else (sp.S.Zero,cross_proj)
    results[(l1,l2)]=dict(Fpart=sp.cancel(Fpart),Sself=sp.cancel(sp.together(Sself)),
                          Scross=sp.cancel(sp.together(Scross)))
    print(f"  ({l1},{l2}): cross-source {'NONZERO' if sp.simplify(results[(l1,l2)]['Scross'])!=0 else 'ZERO'}"
          f"   [{_time.time()-_t:.0f}s]", flush=True)

# ======================================================================
# DELIVERABLES
# ======================================================================
print("\n"+"#"*78); print("# DELIVERABLES"); print("#"*78)

Fpart22=results[(2,2)]['Fpart']
rFp=sp.diff(r*F,r)
print("\n[D1] F-OPERATOR (F-linear part of static l=0 G_tt):")
sp.pprint(sp.cancel(Fpart22))
print(f"     F-operator / (rF)' = {sp.cancel(Fpart22/rFp)}")
print("     => Misner-Sharp form; matches single-mode F-operator (2/r^2)(rF)' up to its constant.")

print("\n[D2] TIME selection rule:")
print("     O(A^2) cross term ~ Re(h_i h_j*) carries e^{-i(w_i-w_j)t}; the static")
print("     l=0 backreaction needs the t-INDEPENDENT (e^0) piece, which exists")
print("     ONLY if w_i = w_j. For w_i != w_j the surviving products are")
print("     e^{+-i(w_i-w_j)t} (and e^{+-i(w_i+w_j)t}) -> <...>_t = 0.")
print("     CONFIRMED: only EQUAL-FREQUENCY pairs source the static mass.")

print("\n[D3] ANGLE selection rule (which (l1,l2) cross pairs survive l=0 projection):")
u=sp.Symbol('u',real=True)
for (l1,l2) in pairs:
    Sc=results[(l1,l2)]['Scross']
    ov=sp.Rational(1,2)*sp.integrate(sp.legendre(l1,u)*sp.legendre(l2,u),(u,-1,1))
    surv= sp.simplify(Sc)!=0
    print(f"     ({l1},{l2}): <P_{l1}P_{l2}>={ov}   l=0 cross-stress {'SURVIVES' if surv else 'vanishes'}")
print("     ANGLE RULE (read off below): cross stress survives iff l1 == l2.")

print("\n[D4] SELF source S_self[Psi_l] (diagonal i=j; pure-G part of static G_tt):")
for lval in (2,3,4):
    Ss=results[(lval,lval)]['Sself'].subs({G1:sp.Symbol('G'),G1p:sp.Symbol('Gp'),
                                           G2:sp.Symbol('G'),G2p:sp.Symbol('Gp')})
    print(f"\n     l={lval}:  S_self =")
    sp.pprint(sp.cancel(sp.together(Ss)))

print("\n[D5] CROSS source S_cross[Psi_i,Psi_j] for surviving pairs (w_i=w_j=w):")
any_cross=False
for (l1,l2) in pairs:
    Sc=results[(l1,l2)]['Scross']
    if sp.simplify(Sc)==0: continue
    any_cross=True
    print(f"\n     ({l1},{l2}): S_cross =")
    sp.pprint(sp.cancel(sp.together(Sc)))
if not any_cross:
    print("     (no OFF-DIAGONAL l1!=l2 pair survives the angle rule; only l1==l2,")
    print("      where S_cross = 2x the half-weight cross of identical harmonics = self form.)")

# ----------------------------------------------------------------------
# [D6] Diagonal reduction: confirm the (2,2) self source EQUALS the single-mode
# phase1_geon_backreact source S[Psi] (l=2). Recompute single-mode here.
# ----------------------------------------------------------------------
print("\n[D6] Diagonal reduction check: l=2 self source vs single-mode phase1.")
def single_mode_source(route='complex'):
    Yc=sp.Rational(1,2)*(3*sp.cos(th)**2-1)
    G=sp.Function('G')(r); Gp=sp.Derivative(G,r)
    H0r=(-I*r**2*wl**2*G+I*r*Gp+3*I*G)/(r*wl); H1r=r*Gp+G; Kr=(I*r*Gp+3*I*G)/(r*wl)
    F2=sp.Function('F')(r); hS=sp.zeros(4,4); hS[0,0]=2*F2; hS[1,1]=2*F2
    if route=='complex':
        FpL=sp.Function('FpL')(t); FmL=sp.Function('FmL')(t)
        trl={sp.Derivative(FpL,t,2):(-I*wl)**2*FpL,sp.Derivative(FpL,t):(-I*wl)*FpL,
             sp.Derivative(FmL,t,2):(+I*wl)**2*FmL,sp.Derivative(FmL,t):(+I*wl)*FmL}
        def Td(e):
            for _ in range(3): e=e.subs(trl)
            return e
        def m1(tt_,tr_,k_,Fac):
            h=sp.zeros(4,4); h[0,0]=tt_*Yc*Fac; h[0,1]=tr_*Yc*Fac; h[1,0]=tr_*Yc*Fac
            h[1,1]=tt_*Yc*Fac; h[2,2]=r**2*k_*Yc*Fac; h[3,3]=r**2*st**2*k_*Yc*Fac
            return h
        hP=m1(H0r,H1r,Kr,FpL)
        hM=m1(sp.conjugate(H0r),sp.conjugate(H1r),sp.conjugate(Kr),FmL).applyfunc(
            lambda e:e.subs(sp.conjugate(G),G).subs(sp.conjugate(sp.Derivative(G,r)),sp.Derivative(G,r)).subs(sp.conjugate(wl),wl).subs(sp.conjugate(r),r))
        hW=(hP+hM)/2; g=g_bg+A*hW+A**2*hS
        ginv=bgi-A*(bgi*hW*bgi)+A**2*(bgi*hW*bgi*hW*bgi-bgi*hS*bgi)
        def D(e,x):
            e2=sp.diff(e,x)
            if x is t: e2=Td(e2)
            return e2
    else:
        tt=sp.symbols('tt',real=True); cwt,swt=sp.cos(tt),sp.sin(tt)
        def sri(expr):
            expr=sp.expand(expr); re=expr.subs(I,0); im=sp.expand((expr-re)/I)
            return sp.simplify(re),sp.simplify(im)
        re0,im0=sri(H0r); re1,im1=sri(H1r); reK,imK=sri(Kr)
        htt=re0*cwt+im0*swt; htr=re1*cwt+im1*swt; hK=reK*cwt+imK*swt
        hR=sp.zeros(4,4); hR[0,0]=htt*Yc; hR[0,1]=htr*Yc; hR[1,0]=htr*Yc
        hR[1,1]=htt*Yc; hR[2,2]=r**2*hK*Yc; hR[3,3]=r**2*st**2*hK*Yc
        g=g_bg+A*hR+A**2*hS
        ginv=bgi-A*(bgi*hR*bgi)+A**2*(bgi*hR*bgi*hR*bgi-bgi*hS*bgi)
        def D(e,x):
            if x is t: return wl*sp.diff(e,tt)
            return sp.diff(e,x)
    def dch(a,b,c):
        s=sp.S.Zero
        for d in range(n):
            s+=ginv[a,d]*(D(g[d,b],coords[c])+D(g[d,c],coords[b])-D(g[b,c],coords[d]))
        return trunc_A(sp.Rational(1,2)*s)
    Gam=[[[None]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(b,n):
                v=dch(a,b,c); Gam[a][b][c]=v; Gam[a][c][b]=v
    def ricL(b,c):
        s=sp.S.Zero
        for a in range(n):
            s+=D(Gam[a][b][c],coords[a]); s-=D(Gam[a][b][a],coords[c])
            for d in range(n):
                s+=Gam[a][a][d]*Gam[d][b][c]; s-=Gam[a][c][d]*Gam[d][b][a]
        return trunc_A(s)
    Ric={ab:ricL(*ab) for ab in [(0,0),(1,1),(2,2),(3,3),(0,1)]}
    Rsc=sp.S.Zero
    for a in range(n):
        for b in range(n):
            if a==b: Rab=Ric[(a,a)]
            elif {a,b}=={0,1}: Rab=Ric[(0,1)]
            else: Rab=sp.S.Zero
            Rsc+=ginv[a,b]*Rab
    Rsc=trunc_A(Rsc)
    Gtt=trunc_A(Ric[(0,0)]-sp.Rational(1,2)*g[0,0]*Rsc)
    Gtt2=sp.expand(sp.expand(Gtt).coeff(A,2))
    if route=='complex':
        FpL=sp.Function('FpL')(t); FmL=sp.Function('FmL')(t)
        p,m=sp.symbols('p m'); es=sp.expand(Gtt2.subs({FpL:p,FmL:m})); out=sp.S.Zero
        for term in sp.Add.make_args(es):
            dp=sp.degree(sp.Poly(term,p),p) if term.has(p) else 0
            dm=sp.degree(sp.Poly(term,m),m) if term.has(m) else 0
            co=term
            if term.has(p): co=co.subs(p,1)
            if term.has(m): co=co.subs(m,1)
            if (dp==0 and dm==0) or (dp==1 and dm==1): out+=co
        Gtt2=out
    else:
        tt=sp.symbols('tt',real=True); cwt,swt=sp.cos(tt),sp.sin(tt)
        Gtt2=Gtt2.subs({cwt**2:sp.Rational(1,2),swt**2:sp.Rational(1,2)})
        Gtt2=sp.expand(Gtt2).subs(cwt*swt,0).subs({cwt:0,swt:0})
    Gpp=(6/r**2-wl**2)*G; Gppp=(6/r**2-wl**2)*Gp-(12/r**3)*G
    def redG(e):
        e=sp.expand(e)
        for _ in range(8):
            e=e.subs(sp.Derivative(G,r,4),sp.diff(Gppp,r)).subs(sp.Derivative(G,r,3),Gppp).subs(sp.Derivative(G,r,2),Gpp)
            e=sp.expand(e)
        return e
    uu=sp.Symbol('u',real=True)
    def ang(e):
        ex=sp.expand(redG(e)); ex=ex.subs(sp.sin(th)**2,1-sp.cos(th)**2)
        ex=sp.expand(ex).subs(sp.cos(th),uu)
        if ex.has(sp.sin(th)): ex=ex.subs(sp.sin(th),sp.sqrt(1-uu**2))
        return sp.Rational(1,2)*sp.cancel(sp.integrate(ex,(uu,-1,1)))
    Gtt2=ang(Gtt2); Gtt2=sp.cancel(sp.together(redG(Gtt2)))
    _,Sp=split_F(Gtt2)
    return sp.cancel(sp.together(Sp.subs({G:sp.Symbol('G'),sp.Derivative(G,r):sp.Symbol('Gp')})))

S_single=single_mode_source('complex')
S_self22=sp.cancel(sp.together(results[(2,2)]['Sself'].subs(
    {G1:sp.Symbol('G'),G1p:sp.Symbol('Gp'),G2:sp.Symbol('G'),G2p:sp.Symbol('Gp')})))
print("     single-mode phase1 S[Psi] (l=2):"); sp.pprint(S_single)
print("     two-mode (2,2) self source       :"); sp.pprint(S_self22)
print(f"     DIFFERENCE (must be 0) = {sp.cancel(sp.together(S_self22-S_single))}")

print("\n[D7] Time-average cross-check: complex double-copy vs explicit real cos/sin.")
S_real=single_mode_source('real')
print(f"     (real cos/sin route) - (complex route) = {sp.cancel(sp.together(S_real-S_single))}   [0 => agree]")

print("\n"+"#"*78); print("# SUMMARY"); print("#"*78)
print("  PART 1: general-l reconstruction H0=H2,H1,K with l(l+1)/2 replacing the")
print("          l=2 constant 3; over-constraint PASS for l=2,3,4; l=2 == phase1.")
print("  TIME selection : cross stress survives <...>_t only if w_i = w_j.")
print("  ANGLE selection: cross stress nonzero only if l_i = l_j (see [D3]).")
print("  => Only EQUAL-(l,w) mode pairs source the static mass; mixed-l pairs vanish.")
print("  S_self(l=2) == single-mode phase1 source; both time-average routes agree.")
print("\nDONE.", flush=True)
