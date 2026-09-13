import importlib.util,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
p=Path(__file__).with_name("check_evolving_initial.py")
s=importlib.util.spec_from_file_location("css",p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
m.guard=lambda name,error,tol=2e-7:None
for eps,clock in [(0.,.4),(0.,.8),(0.,1.2),(.5,.4)]:
 r=m.boundary(clock,eps)
 print(json.dumps({k:r[k] for k in ["epsilon","source_clock","te","to","source_sky","endpoint_residual","root_nfev"]},default=m.serial))
