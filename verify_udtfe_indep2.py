import sympy as sp

r = sp.symbols('r', real=True)
c0 = sp.symbols('c0', positive=True)
phi = sp.Function('phi')(r)

# --- v_local for arbitrary diagonal, with positive N,L ---
N = sp.Function('N'); L = sp.Function('L')
Nr = sp.Symbol('Nv', positive=True); Lr = sp.Symbol('Lv', positive=True)
gtt = -Nr**2; grr = Lr**2
dr_dt = sp.sqrt(-gtt/grr)                      # coord null speed
v_loc = sp.sqrt(grr)*dr_dt/sp.sqrt(-gtt)       # proper-len/proper-time, c0=1 units
print("v_local arbitrary diagonal =", sp.simplify(v_loc), " (should be 1)")

# --- ATTACK #1: off-diagonal shift g_tr = s(r). Is local c still c0? ---
print("\n--- Off-diagonal shift attack ---")
s = sp.Symbol('s', real=True)   # constant shift sample; general s(r) handled by pointwise
n, l = sp.symbols('n l', positive=True)   # -gtt=n^2, grr=l^2 pointwise
# metric block [[-n^2, s],[s, l^2]] in (t,r). Null: ds^2=0
# -n^2 dt^2 + 2 s dt dr + l^2 dr^2 = 0  -> quadratic in (dr/dt)
u = sp.Symbol('u')  # dr/dt
nullq = -n**2 + 2*s*u + l**2*u**2
roots = sp.solve(nullq, u)
print("coord null dr/dt roots (two one-way speeds):")
for rt in roots: print("   ", sp.simplify(rt))
# The two one-way coordinate speeds differ (anisotropy). But locally measured?
# A STATIC observer 4-velocity along dt: u^mu=(1/sqrt(n^2),0). Its proper frame:
# orthonormal: e0 = (1/n) dt-dir; e1 must be orthogonal to e0 wrt metric.
# Build metric matrix, find local light speed via projecting null vector onto observer frame.
g = sp.Matrix([[-n**2, s],[s, l**2]])
# observer u: timelike, u = (a,0); normalize g(u,u)=-1 => -n^2 a^2=-1 => a=1/n
uo = sp.Matrix([1/n, 0])
# spatial direction e1 orthogonal to uo: g(uo,e1)=0 ; e1=(b,d)
b,d = sp.symbols('b d', real=True)
e1 = sp.Matrix([b,d])
orth = (uo.T*g*e1)[0]   # = -n^2*(1/n)*b + s*(1/n)*d ... compute
orth = sp.expand(orth)
# solve b in terms of d
bsol = sp.solve(orth, b)[0]
e1b = e1.subs(b, bsol)
norm1 = sp.simplify((e1b.T*g*e1b)[0])   # should be positive; normalize
e1n = e1b/sp.sqrt(norm1)
# A null vector k: k = uo + (1/clocal) * e1n_dir*clocal...
# Local light speed: decompose null k = E(uo + w) with w spatial unit, |w| measured =c_local.
# For any null k: g(k,k)=0. Write k = alpha*uo + beta*e1n (e1n unit spacelike, uo unit timelike orthonormal)
al, be = sp.symbols('al be', real=True)
k = al*uo + be*e1n
nullk = sp.simplify((k.T*g*k)[0])
print("g(k,k) in orthonormal observer frame =", nullk, " (=> -al^2+be^2)")
# => local speed = |be/al| from -al^2+be^2=0 => be/al=1 => c_local=1 (=c0) ALWAYS
print("=> local speed |be/al| from null cond -al^2+be^2=0  ==> 1 (constant) regardless of s")
