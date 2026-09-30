#!/usr/bin/env python3
"""Independent algebraic jet reconstruction, with no author solver imports."""
import hashlib
import json
from pathlib import Path
import platform
import resource
import sys
import time

resource.setrlimit(resource.RLIMIT_CPU, (180, 180))
resource.setrlimit(resource.RLIMIT_AS, (2 * 1024**3, 2 * 1024**3))
started = time.monotonic()
import sympy as s

out = Path(__file__).resolve().parent
t, A, E = s.symbols("t A E", positive=True)
Q, at, ax, Pt, Px, Qt, Qx = s.symbols("Q at ax Pt Px Qt Qx", real=True)
att, atx, axx, Ptt, Ptx, Pxx, Qtt, Qtx, Qxx = s.symbols(
    "att atx axx Ptt Ptx Pxx Qtt Qtx Qxx", real=True
)
jets = [
    {t: 1, A: 2*A*at, E: E*Pt, Q: Qt, at: att, ax: atx,
     Pt: Ptt, Px: Ptx, Qt: Qtt, Qx: Qtx},
    {A: 2*A*ax, E: E*Px, Q: Qx, at: atx, ax: axx,
     Pt: Ptx, Px: Pxx, Qt: Qtx, Qx: Qxx},
]

def clean(expr):
    return s.factor(s.cancel(expr))

def d(expr, coordinate):
    if coordinate > 1:
        return s.S.Zero
    return s.Add(*(s.diff(expr, var)*val for var, val in jets[coordinate].items()))

g = s.Matrix([[-A, 0, 0, 0], [0, A, 0, 0],
              [0, 0, t*E, t*E*Q],
              [0, 0, t*E*Q, t*(E*Q**2+1/E)]])
gi = s.Matrix([[-1/A, 0, 0, 0], [0, 1/A, 0, 0],
               [0, 0, (E*Q**2+1/E)/t, -E*Q/t],
               [0, 0, -E*Q/t, E/t]])
assert all(clean(v)==0 for v in g*gi-s.eye(4))
Gamma = [[[clean(sum(gi[c,h]*(d(g[h,b],a)+d(g[h,a],b)-d(g[a,b],h))
                    for h in range(4))/2)
           for b in range(4)] for a in range(4)] for c in range(4)]
Ric = s.zeros(4)
for a in range(4):
    for b in range(4):
        Ric[a,b] = clean(sum(d(Gamma[c][a][b],c)-d(Gamma[c][a][c],b)
            +sum(Gamma[c][c][h]*Gamma[h][a][b]-Gamma[c][b][h]*Gamma[h][a][c]
                 for h in range(4)) for c in range(4)))

EP = Ptt+Pt/t-Pxx-E**2*(Qt**2-Qx**2)
EQ = Qtt+Qt/t-Qxx+2*(Pt*Qt-Px*Qx)
expected = s.zeros(4)
expected[0,0] = -att+axx+at/t+1/(2*t**2)-(Pt**2+E**2*Qt**2)/2
expected[0,1] = expected[1,0] = ax/t-(Pt*Px+E**2*Qt*Qx)/2
expected[1,1] = att-axx+at/t-(Px**2+E**2*Qx**2)/2
expected[2,2] = t*E*EP/(2*A)
expected[2,3] = expected[3,2] = t*E*(Q*EP+EQ)/(2*A)
expected[3,3] = t*E*((Q**2-E**-2)*EP+2*Q*EQ)/(2*A)
component_matches = {f"R{a}{b}": clean(Ric[a,b]-expected[a,b])==0
                     for a in range(4) for b in range(4)}
assert all(component_matches.values()), component_matches

energy = t*(Pt**2+Px**2+E**2*(Qt**2+Qx**2))
momentum = 2*t*(Pt*Px+E**2*Qt*Qx)
pde = {Ptt:Pxx-Pt/t+E**2*(Qt**2-Qx**2),
       Qtt:Qxx-Qt/t-2*(Pt*Qt-Px*Qx)}
compatibility = clean((d(energy,1)-d(momentum,0)).subs(pde))
assert compatibility==0
wave_lambda = clean((d(energy,0)-d(momentum,1)).subs(pde))
assert clean(wave_lambda+Pt**2-Px**2+E**2*(Qt**2-Qx**2))==0

on_shell_a = {
    at:(energy-1/t)/4,
    ax:momentum/4,
    att:clean((d(energy,0)+1/t**2).subs(pde)/4),
    axx:d(momentum,1)/4,
}
ricci_on_shell = {f"R{a}{b}": clean(Ric[a,b].subs(on_shell_a).subs(pde))
                  for a in range(4) for b in range(4)}
assert all(v==0 for v in ricci_on_shell.values())

# Nonzero exact rational jets: controls against missing unpolarized terms.
sample = {t:s.Rational(3,2), A:s.Rational(7,5), E:s.Rational(5,4),
    Q:s.Rational(2,7), Pt:s.Rational(1,3), Px:s.Rational(-2,5),
    Qt:s.Rational(3,7), Qx:s.Rational(1,4), Ptx:s.Rational(-1,7),
    Pxx:s.Rational(2,9), Qtx:s.Rational(1,8), Qxx:s.Rational(-3,10)}
sample.update({Ptt:pde[Ptt].subs(sample),Qtt:pde[Qtt].subs(sample)})
sample.update({var:clean(value.subs(pde).subs(sample)) for var,value in on_shell_a.items()})
sample[atx] = clean((d(energy,1)/4).subs(sample))
assert all(clean(v.subs(sample))==0 for v in Ric)
mutations = {}
for name, changed in [
    ("drop_P_nonlinearity", {Ptt:sample[Pxx]-sample[Pt]/sample[t]}),
    ("reverse_Q_coupling", {Qtt:sample[Qxx]-sample[Qt]/sample[t]
                              +2*(sample[Pt]*sample[Qt]-sample[Px]*sample[Qx])}),
    ("drop_Q_momentum", {ax:sample[t]*sample[Pt]*sample[Px]/2}),
    ("leave_lapse_at_background", {at:-1/(4*sample[t]),ax:0,
                                  att:1/(4*sample[t]**2),axx:0}),
]:
    values = {**sample, **changed}
    residuals = {f"R{a}{b}":str(clean(Ric[a,b].subs(values)))
                 for a in range(4) for b in range(4) if clean(Ric[a,b].subs(values))!=0}
    assert residuals, name
    mutations[name] = residuals

# Longitudinal null-geodesic tangent k=C/A (1,+1,0,0).
# Here A=N^2 and d/dlambda=(C/A)(d_t+d_x).
C = s.symbols("C", positive=True)
k = [C/A,C/A,s.S.Zero,s.S.Zero]
geodesic = [clean(sum(k[b]*d(k[a],b) for b in range(4))
             +sum(Gamma[a][b][c]*k[b]*k[c] for b in range(4) for c in range(4)))
             for a in range(4)]
assert all(v==0 for v in geodesic)
null = clean((s.Matrix(k).T*g*s.Matrix(k))[0])
assert null==0
omega = clean(-(g[0,0]/s.sqrt(A))*k[0])
assert clean(omega-C/s.sqrt(A))==0

# A genuinely unpolarized homogeneous analytic anchor: target-space geodesic.
tau, v, p0, q0 = s.symbols("tau v p0 q0", real=True)
Ph = p0+s.log(s.cosh(v*tau))
Qh = q0+s.exp(-p0)*s.tanh(v*tau)
homogeneous_identities = [
    s.diff(Ph,tau,2)-s.exp(2*Ph)*s.diff(Qh,tau)**2,
    s.diff(Qh,tau,2)+2*s.diff(Ph,tau)*s.diff(Qh,tau),
    s.diff(Ph,tau)**2+s.exp(2*Ph)*s.diff(Qh,tau)**2-v**2,
]
homogeneous_residuals = [s.simplify(s.trigsimp(h)) for h in homogeneous_identities]
assert all(h==0 for h in homogeneous_residuals)

pins = json.loads((out.parent.parent/"SOURCE_PINS.json").read_text())
pin_matches = {p:hashlib.sha256(Path(p).read_bytes()).hexdigest()==sha for p,sha in pins.items()}
# Central file may be edited during later parent integration. This records the actual snapshot.
result = {
    "verdict":"VERIFIED-WITH-CAVEATS",
    "scope":"Exact local Ricci reduction, constraints and longitudinal clock formula only",
    "model":"Parent-inherited model; exact identifier not exposed in reviewer context",
    "context":"Fresh scoped /root/ngd1_equations; expected equations and NE1 proof exposed",
    "implementation":"Independent SymPy algebraic-jet Levi-Civita/Ricci implementation; no author code imported",
    "python":sys.version,
    "sympy":s.__version__,"platform":platform.platform(),
    "symbols":{"A":"exp(2a)=exp(lambda/2)t^(-1/2)","E":"exp(P)","a":"lambda/4-log(t)/4"},
    "metric_determinant":str(clean(g.det())),
    "component_formula_matches":component_matches,
    "original_ricci_components":{f"R{a}{b}":str(Ric[a,b]) for a in range(4) for b in range(4)},
    "on_shell_original_ricci":{key:str(value) for key,value in ricci_on_shell.items()},
    "lambda_integrability":str(compatibility),
    "lambda_wave_equation":str(wave_lambda),
    "exact_rational_mutation_residuals":mutations,
    "longitudinal_null":str(null),
    "longitudinal_affine_geodesic_residuals":list(map(str,geodesic)),
    "longitudinal_frequency":str(omega),
    "longitudinal_clock_ratio":"N(t_e+d,x_o)/N(t_e,x_e), x_o-x_e=d>0 on chosen lift/winding",
    "homogeneous_anchor":{
        "tau":"log(t/t0)","P":"p0+log(cosh(v*tau))",
        "Q":"q0+exp(-p0)*tanh(v*tau)","lambda":"lambda0+v**2*tau",
        "exact_residuals":list(map(str,homogeneous_residuals))},
    "source_pin_matches_at_run":pin_matches,
    "limits":{"cpu_seconds":180,"address_space_bytes":2*1024**3,"gpu":"none"},
    "elapsed_seconds":time.monotonic()-started,
    "max_rss_kib":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    "omissions":["No author solver or grid results checked at this equation gate",
                 "No different-model/library or interval certificate claimed",
                 "No transverse ray or generic spacetime coverage",
                 "No native UDT equation adoption or physical clock protocol selection"]
}
(out/"EQUATION_CHECK.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({key:result[key] for key in ["verdict","scope","elapsed_seconds","max_rss_kib",
      "source_pin_matches_at_run","lambda_integrability","lambda_wave_equation",
      "longitudinal_affine_geodesic_residuals"]},indent=2))
