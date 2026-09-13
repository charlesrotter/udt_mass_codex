import ast,json,hashlib,datetime,sys
from pathlib import Path
p=Path(__file__).resolve().parent
source=p/'independent_connection_repaired.py';nodes=[]
for n in ast.parse(source.read_text()).body:
    if isinstance(n,ast.Try):break
    nodes.append(n)
ns={'__file__':str(source)};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(source),'exec'),ns)
for name in ('Q','J','frame_geometry','sqrt_at','vec','plus','scale','dot','connection','firstjet','exterior','equal','zero','nonzero','checks'):
    globals()[name]=ns[name]
u,v,x,y,H,g,gi,C,R,Ric,k,n,X,Y=frame_geometry((Q(1),Q(0),Q(1),Q(0)))
h=u-1;z1=h*h;z2=h;c=sqrt_at(1+2*(z1*z1+z2*z2),Q(1));nk=plus(n,k)
E1=plus(scale(z1,nk),plus(scale(1+2*z1*z1/(c+1),X),scale(2*z1*z2/(c+1),Y)))
E2=plus(scale(z2,nk),plus(scale(2*z1*z2/(c+1),X),scale(1+2*z2*z2/(c+1),Y)))
full=[plus(scale(c,nk),plus(scale(2*z1,X),scale(2*z2,Y))),plus(n,scale(-1,k)),E1,E2]
base=[nk,plus(n,scale(-1,k)),X,Y]
equal('offaxis_nodal_full_frame_same_event',full,base)
other=frame_geometry((Q(2),Q(0),Q(1),Q(0)));kk,nn,xx,yy=other[-4:]
wrong=[plus(nn,kk),plus(nn,scale(-1,kk)),xx,yy]
nonzero('catch_wrong_event_full_frame',[full[i][j]-wrong[i][j] for i in range(4) for j in range(4)])
a=u*u/3;b=-2*u**3/5
P1=plus(X,scale(a,n));P2=plus(Y,scale(b,n));m=plus(k,plus(plus(scale(a,X),scale(b,Y)),scale((a*a+b*b)/2,n)))
nullframe=[n,m,P1,P2]
equal('full_other_null_lift_Gram',[[dot(g,A,B) for B in nullframe] for A in nullframe],[[0,-1,0,0],[-1,0,0,0],[0,0,1,0],[0,0,0,1]])
P1=X;P2=plus(Y,scale(2*u**3,n));Nscaled=plus(n,scale(-1,k));z=2*u**3;cb=sqrt_at(1+2*z*z,Q(3));B1=X;B2=plus(scale(z,nk),scale(cb,Y))
equal('null_lift_Nscaled_projection',dot(g,Nscaled,P2),2*u**3)
zero('boost_Nscaled_projection',dot(g,Nscaled,B2))
nonzero('distinct_screen_planes',dot(g,Nscaled,P2)-dot(g,Nscaled,B2))
Ap=connection(g,C,P1,P2);Ab=connection(g,C,B1,B2);target=vec(-4*u*x,0,0,0)
equal('distinct_screen_same_full_potential',firstjet(Ap),firstjet(Ab))
equal('distinct_screen_target_potential',firstjet(Ap),firstjet(target))
equal('distinct_screen_same_curvature',exterior(Ap),exterior(Ab))
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'targeted off-axis nodal repair and supplemental distinct reductions on existing H0','code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'reused_reviewer_definitions_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'checks':checks,'count':len(checks),'passed':sum(c['pass'] for c in checks),'all_pass':all(c['pass'] for c in checks)}
with Path(sys.argv[1]).open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps(result));sys.exit(0 if result['all_pass'] else 1)
