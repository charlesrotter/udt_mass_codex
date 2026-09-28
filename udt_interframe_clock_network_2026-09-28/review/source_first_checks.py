"""Independent source-first controls; no ICN1 author proof/code/results imported.

Question: necessary relay/radar relations and possible unsupported metric/scale joins.
Regime: regular future null legs and geodesic proper clocks on supplied metrics.
All geometric controls are free-and-explored, not admitted UDT solutions.
Exact rational/symbolic CPU algebra; c_E=1 only for coordinate units below.
No grid, tolerance, data fit, GPU, field equation, physical source or scale input.
Run via existing run_capture.py: 60s CPU/wall, 512MiB, threads=1.
Maximum result: scoped controls plus algebra; no universal geometry selection.
"""
import hashlib
import json
import pathlib
import platform
import subprocess
import sys

import sympy as S

ROOT = pathlib.Path(__file__).resolve().parents[2]
REVIEW = pathlib.Path(__file__).resolve().parent
checks = []


def eq(name, actual, expected=0):
    if actual == expected:
        residual = S.Integer(0)
    elif isinstance(actual, S.MatrixBase):
        residual = S.simplify((actual - expected).norm())
    else:
        residual = S.simplify(S.sympify(actual - expected).rewrite(S.exp))
    checks.append(dict(name=name, passed=residual == 0,
                       actual=str(actual), expected=str(expected), residual=str(residual)))
    if residual != 0:
        raise RuntimeError(name + ': ' + str(residual))


def differs(name, actual, incorrect):
    residual = S.simplify(actual - incorrect)
    checks.append(dict(name=name, passed=residual != 0,
                       actual=str(actual), incorrect=str(incorrect), residual=str(residual)))
    if residual == 0:
        raise RuntimeError('wrong formula passed: ' + name)


launch = json.loads((ROOT / 'udt_interframe_clock_network_2026-09-28/LAUNCH.json').read_text())
pins = {p: dict(expected=h, actual=hashlib.sha256((ROOT / p).read_bytes()).hexdigest())
        for p, h in launch['source_pins'].items()}
if not all(v['actual'] == v['expected'] for v in pins.values()):
    raise RuntimeError('source pin mismatch')
branch = subprocess.check_output(['git', 'branch', '--show-current'], cwd=ROOT, text=True).strip()
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
origin = subprocess.check_output(['git', 'rev-parse', 'origin/grok'], cwd=ROOT, text=True).strip()
if branch != 'grok' or head != launch['head'] or origin != launch['origin_grok']:
    raise RuntimeError('branch/head mismatch')

# Differentiate actual composed maps, retaining the intermediate event.
s, c = S.symbols('s c', positive=True)
F, G, H = [S.Function(v) for v in ['F', 'G', 'H']]
R = G(F(s))
P = S.diff(F(s), s) * S.Subs(S.diff(G(s), s), s, F(s))
eq('echo chain with actual return event', S.diff(R, s), P)
D, T = c * (R - s) / 2, (R + s) / 2
eq('radar rate', S.diff(D, s) / S.diff(T, s), c * (P - 1) / (P + 1))
q = S.symbols('q', positive=True)
eq('positive rate subluminal margin', 1 - ((q - 1) / (q + 1)) ** 2, 4*q/(q+1)**2)
eq('sum-depth kernel half argument', S.tanh(-S.log(q)/2), (1-q)/(1+q))
Rl = G(H(F(s)))
eq('latency chain', S.diff(Rl, s),
   S.Subs(S.diff(G(s), s), s, H(F(s))) *
   S.Subs(S.diff(H(s), s), s, F(s)) * S.diff(F(s), s))

# 1+1 inertial motion embedded in Lorentz4: A=(s,0), B=(gamma*b,L+gamma*v*b).
# Both proper-normalized geodesics. Positive x branch on the stated local domain.
L, b = S.symbols('L b', positive=True)
v, gamma = S.Rational(3, 5), S.Rational(5, 4)
eq('inertial proper normalization', gamma**2*(1-v**2), 1)
Bout = (s+L)/(gamma*(1-v))
Aback = L + gamma*(1+v)*b
echo = Aback.subs(b, Bout)
eq('outbound null incidence', gamma*Bout-s, L+gamma*v*Bout)
eq('return null incidence', Aback-gamma*b, L+gamma*v*b)
eq('inertial outward clock ratio', S.diff(Bout,s), 2)
eq('inertial return clock ratio', S.diff(Aback,b), 2)
eq('inertial echo slope', S.diff(echo,s), 4)
Ti, Di = (s+echo)/2, (echo-s)/2
eq('inertial radar position', Di, L+v*Ti)
eq('inertial radar velocity', S.diff(Di,s)/S.diff(Ti,s), v)
differs('causal return is not inverse slope', S.diff(Aback,b), 1/S.diff(Bout,s))
differs('same clock ratios permit distinct radar distances', Di.subs(L,2), Di.subs(L,1))

# Relay direction reset: endpoint Lorentz maps compose to I but real echo ratio is four.
LAB = S.Matrix([[gamma,-gamma*v],[-gamma*v,gamma]])
LBA = LAB.inv()
eq('flat endpoint frame carry composition', (LBA*LAB-S.eye(2)).norm(), 0)
out_ray_B = LAB*S.Matrix([1,1])
new_return_ray_A = LBA*S.Matrix([1,-1])
eq('outward null Doppler factor', out_ray_B[0], S.Rational(1,2))
eq('return null Doppler factor after ray reset', new_return_ray_A[0], S.Rational(1,2))
eq('relay product from separate rays', 1/(out_ray_B[0]*new_return_ray_A[0]), 4)
differs('unbroken-ray cocycle cannot replace relay product', 4, 1/(LBA*LAB*S.Matrix([1,1]))[0])

# A third stationary clock: direct and relayed paths have different arrival offsets.
direct = s+1  # A=(0,0), C=(0,1).
relayed = s+1+S.sqrt(2)  # A -> B=(1,0) -> C.
eq('third-clock direct and relay slopes may agree', S.diff(direct,s), S.diff(relayed,s))
differs('third-clock direct and relay arrival maps differ', relayed, direct)

# Time-dependent conformally flat supplied metric g=eta^2 diag(-1,1,1,1), eta>0.
# Fixed spatial-coordinate observers are geodesic; proper tau=eta^2/2.
eta, ell = S.symbols('eta ell', positive=True)
u = S.Matrix([1/eta,0,0,0])
metric = S.diag(-eta**2,eta**2,eta**2,eta**2)
eq('conformal observer unit normalization', (u.T*metric*u)[0], -1)
# Only Gamma^0_00 contributes to its acceleration, =1/eta; spatial Gamma^i_00=0.
eq('conformal observer time acceleration', u[0]*S.diff(u[0],eta)+(1/eta)*u[0]**2)
tau0, tau1, tau2 = eta**2/2, (eta+ell)**2/2, (eta+2*ell)**2/2
z1 = S.diff(tau1,eta)/S.diff(tau0,eta)
z2 = S.diff(tau2,eta)/S.diff(tau1,eta)
Pcon = S.diff(tau2,eta)/S.diff(tau0,eta)
eq('time-dependent actual-leg product', z1*z2, Pcon)
eq('conformal numerical pair slopes', (z1*z2).subs({eta:2,ell:1}), 2)
differs('wrong unevolved return evaluation', Pcon, z1*z1)
Dc, Tc = (tau2-tau0)/2, (tau2+tau0)/2
eq('conformal radar rate', S.diff(Dc,eta)/S.diff(Tc,eta), (Pcon-1)/(Pcon+1))
eq('conformal late radar distance divergent', S.limit(Dc,eta,S.oo), S.oo)
eq('conformal late echo slope tends to one', S.limit(Pcon,eta,S.oo), 1)

# c:[M,L,T]=(0,1,-1), G=(-1,3,-2). No monomial has pure length dimension.
dim = S.Matrix([[0,-1],[1,3],[-1,-2]])
eq('two calibration dimensions independent', dim.rank(), 2)
for target, vector in [('length',S.Matrix([0,1,0])),
                       ('time',S.Matrix([0,0,1])), ('mass',S.Matrix([1,0,0]))]:
    eq('no pure '+target+' from c and G', dim.row_join(vector).rank(), 3)
eq('G over c squared needs mass to make length', dim*S.Matrix([-2,1]), S.Matrix([-1,1,0]))

record = dict(stage='SOURCE_FIRST_BEFORE_ICN1_CANDIDATE_EXPOSURE',
              branch=branch, head=head, origin_grok=origin,
              python=sys.version, sympy=S.__version__, platform=platform.platform(),
              source_pins=pins, checks=checks, count=len(checks), passed=True,
              source_first_script_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest())
out = REVIEW / 'SOURCE_FIRST_CHECKS.json'
with out.open('x') as stream:
    json.dump(record, stream, indent=2)
    stream.write('\n')
print(json.dumps(dict(passed=True, check_count=len(checks), pins=len(pins), output=str(out))))
