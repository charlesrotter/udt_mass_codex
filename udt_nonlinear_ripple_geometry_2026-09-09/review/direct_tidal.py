"""Direct review: full-metric Riemann using the independently built matrix connection.
Author candidate exposed; no author functions imported. Source-first files unchanged.
"""
import contextlib
import io
import itertools
import json
import runpy
from pathlib import Path
with contextlib.redirect_stdout(io.StringIO()):
    ns=runpy.run_path(str(Path(__file__).with_name('source_first_tensor.py')))
s,t,x,P,L,g,ch,b,A,N,rules=(ns[n] for n in
    ('s','t','x','P','L','g','ch','b','A','N','rules'))
coords=ns['coords']
pt,px=s.diff(P,t),s.diff(P,x)
invframe=[1/(b*s.sqrt(A)),1/s.sqrt(A),s.exp(-P/2)/s.sqrt(t),s.exp(P/2)/s.sqrt(t)]
def riemann(a,bb,c,d):
    up=s.diff(ch[a][d][bb],coords[c])-s.diff(ch[a][c][bb],coords[d])
    up+=sum(ch[a][c][v]*ch[v][d][bb]-ch[a][d][v]*ch[v][c][bb] for v in range(4))
    cov=g[a,a]*up
    val=cov*invframe[a]*invframe[bb]*invframe[c]*invframe[d]
    return s.simplify(s.powdenest(val,force=True))
def shell(v):
    return s.simplify(v.subs(rules,simultaneous=True))
E=s.diag(*(shell(riemann(i,0,i,0)) for i in range(1,4)))
Z=1/(N*N)
delta=s.simplify((E[1,1]-E[2,2])/Z)
expected=-b*b*s.diff(P,x,2)-pt/(4*t)+t*pt**3/4+3*b*b*t*pt*px**2/4
assert s.simplify(delta-expected)==0, ('full_Riemann_tidal',delta-expected)
assert s.simplify(s.trace(E))==0

# Exact electric tensor at the SE1 event, in the full orthonormal frame.
initial={L:0,P:0,pt:s.Rational(1,4),px:0,s.diff(P,x,2):0,t:1}
E1=E.subs(initial,simultaneous=True).applyfunc(s.simplify)
assert E1==s.diag(-s.Rational(5,12),s.Rational(5,32),s.Rational(25,96))
normalized=s.simplify(t*t*delta)
D1=normalized.subs(initial,simultaneous=True)
assert D1 == -s.Rational(15,256)

# Reconstruct the basis-conversion term from off-shell curvature and metric.
ep=s.symbols('ep',real=True)
f=s.Function('f')(t)
sub={P:ep*f*s.cos(x),L:0}
raw_yy=riemann(2,0,2,0)
raw_zz=riemann(3,0,3,0)
def vary(expr):
    return s.simplify(s.diff(expr.subs(sub).doit(),ep).subs(ep,0)/s.cos(x))
orth_coeff=vary((raw_yy-raw_zz)/2)
coord_coeff=vary((s.exp(P)*raw_yy-s.exp(-P)*raw_zz)/2)
basis_change=s.simplify(coord_coeff-orth_coeff)
assert basis_change==s.Rational(2,9)*f/t**s.Rational(3,2)
T=s.symbols('T',positive=True)
h=s.Function('h')(T)
dt_dT=s.Rational(4,3)*T**s.Rational(1,3)
ft=2*s.diff(h,T)/dt_dT
ftt=s.diff(ft,T)/dt_dT
convert={f:2*h,s.diff(f,t):ft,s.diff(f,t,2):ftt,t:T**s.Rational(4,3)}
orth_T=orth_coeff.subs(convert,simultaneous=True)
coord_T=coord_coeff.subs(convert,simultaneous=True)
ode=-s.diff(h,T)/T-T**s.Rational(2,3)*h
orth_on=s.simplify(orth_T.subs(s.diff(h,T,2),ode))
coord_on=s.simplify(coord_T.subs(s.diff(h,T,2),ode))
assert s.simplify(orth_on-(-s.diff(h,T)/(3*T)+T**s.Rational(2,3)*h))==0
assert s.simplify(coord_on-(-s.diff(h,T)/(3*T)+4*h/(9*T*T)+T**s.Rational(2,3)*h))==0

# All independent frame Riemann pair entries, including mixed tidal slots.
pairs=list(itertools.combinations(range(4),2))
scaled={}
for i,(a,bb) in enumerate(pairs):
    for c,d in pairs[i:]:
        value=s.simplify(shell(riemann(a,bb,c,d))*A)
        scaled[str((a,bb,c,d))]=str(value)
print(json.dumps(dict(result='PASS_DIRECT_FULL_RIEMANN_AND_BASIS',
    tidal_contrast_divided_by_Z=str(delta),initial_full_E=str(E1),
    initial_normalized_contrast=str(D1),basis_change=str(basis_change),
    G327_orthonormal=str(orth_on),G327_background_coordinate=str(coord_on),
    independent_frame_pairs_divided_by_inverse_A=scaled),indent=2))
