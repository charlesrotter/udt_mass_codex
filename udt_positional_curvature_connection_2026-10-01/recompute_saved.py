"""Independent exact rational reconstruction from saved coordinate tensor; no CAS."""
import ast,itertools,json,hashlib,platform
from pathlib import Path
from fractions import Fraction as F
b=Path('udt_positional_curvature_connection_2026-10-01');source=b/'checks/curvature_repaired.stdout'
doc=json.loads(source.read_text());eta=(-1,1,1,1);indices=list(itertools.product(range(4),repeat=4))
count=0

def evaluate(expr,env):
 def node(a):
  if isinstance(a,ast.Constant):return F(a.value)
  if isinstance(a,ast.Name):return env[a.id]
  if isinstance(a,ast.UnaryOp):return -node(a.operand) if isinstance(a.op,ast.USub) else node(a.operand)
  if isinstance(a,ast.BinOp):
   x,y=node(a.left),node(a.right)
   if isinstance(a.op,ast.Add):return x+y
   if isinstance(a.op,ast.Sub):return x-y
   if isinstance(a.op,ast.Mult):return x*y
   if isinstance(a.op,ast.Div):return x/y
   if isinstance(a.op,ast.Pow):assert y.denominator==1;return x**int(y)
  if isinstance(a,ast.Call) and isinstance(a.func,ast.Name) and a.func.id=='sin':
   assert len(a.args)==1 and isinstance(a.args[0],ast.Name) and a.args[0].id=='theta'
   return F(3,5)
  raise ValueError(ast.dump(a))
 return node(ast.parse(expr,mode='eval').body)

def eq(a,b,label):
 global count
 assert a==b,(label,str(a),str(b));count+=1

def build(k,sqrt_f):
 env={'mu':F(9,50),'r':F(1),'kappa':k};f=1-2*env['mu']-k
 eq(sqrt_f**2,f,'positive tetrad normalization');assert f>0
 e=(1/sqrt_f,sqrt_f,F(1),F(5,3));res={}
 for idx in indices:
  name=','.join(map(str,idx));z=evaluate(doc['coordinate_curvature'].get(name,'0'),env)
  for i in idx:z*=e[i]
  res[idx]=z
  eq(z,evaluate(doc['orthonormal_curvature'].get(name,'0'),env),'saved coordinate to orthonormal '+name)
 return res
k=F(7,25);A=build(k,F(3,5));A0=build(F(0),F(4,5));D={idx:A[idx]-A0[idx] for idx in indices}
B=lambda i,j,a,b:(eta[j]*eta[i] if j==a and i==b else 0)-(eta[i]*eta[j] if i==a and j==b else 0)
for idx in indices:eq(D[idx],k*B(*idx),'isotropic curvature difference')
Ric=[[sum(eta[i]*A[i,a,b,i] for i in range(4)) for b in range(4)] for a in range(4)]
for a,b_ in itertools.product(range(4),repeat=2):eq(Ric[a][b_],3*k*eta[a] if a==b_ else 0,'Ricci contraction')
eq(sum(eta[a]*Ric[a][a] for a in range(4)),12*k,'scalar contraction')
weyl_square=sum(F(eta[i]*eta[j]*eta[a]*eta[b_])*(A[i,j,a,b_]-k*B(i,j,a,b_))**2 for i,j,a,b_ in indices)
eq(weyl_square,48*F(9,50)**2,'retained nonzero Weyl square');assert weyl_square>0
U=(F(5,4),F(3,4),F(0),F(0));n=(F(0),F(0),F(1),F(0))
tide=sum(D[i,j,a,b_]*n[i]*U[j]*U[a]*n[b_] for i,j,a,b_ in indices)
eq(tide,-k,'boosted clock tide');eq(-tide/2,k/2,'first leading contrast');eq(-3*tide/2,3*k/2,'return leading contrast')
# Off-diagonal coordinate identification differs from the physical frame map.
raw={idx:evaluate(doc['coordinate_curvature'].get(','.join(map(str,idx)),'0'),{'mu':F(9,50),'r':F(1),'kappa':k})-evaluate(doc['coordinate_curvature'].get(','.join(map(str,idx)),'0'),{'mu':F(9,50),'r':F(1),'kappa':F(0)}) for idx in indices}
assert raw[(0,2,2,0)]!=D[(0,2,2,0)];count+=1
print(json.dumps({'status':'PASS','checks':count,'python':platform.python_version(),'method':'stdlib AST/Fraction; original saved coordinate tensor independently transformed with exact rational matched tetrads; no CAS or candidate curvature formulas used to create input','source':str(source),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'parameters':{'mu':'9/50','r':'1','kappa':'7/25','sin_theta':'3/5','sqrt_f':'3/5','sqrt_f0':'4/5'},'Ricci':[[str(z) for z in row] for row in Ric],'scalar':str(12*k),'retained_Weyl_square':str(weyl_square),'boosted_delta_tide':str(tide),'outgoing_L2_coefficient':str(-tide/2),'return_L2_coefficient':str(-3*tide/2),'limits':'Saved-artifact finite exact check, exposed to parent proof and source; not an independent derivation of coordinate curvature or continuum proof.'},indent=2))
