import importlib.util, io, contextlib
spec=importlib.util.spec_from_file_location("d","/home/udt-admin/UDT_m_e/da_discharge_i_dirac.py")
m=importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(m)
h=m.h_tensor("m0")
print("import fast + functions live. spot checks:")
for kp in [-3,-4]:
    t1,t2=m.dirac_channel(kp,-1,h)
    print(f"  kappa=-1 -> {kp:+d}: t1={t1:.3e} t2={t2:.3e} -> {'OPEN' if abs(t1)>1e-12 or abs(t2)>1e-12 else 'forbidden'}")
