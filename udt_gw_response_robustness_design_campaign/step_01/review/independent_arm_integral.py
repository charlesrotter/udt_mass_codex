"""Independent integral interpretation of cached arm-transfer definition."""
import cmath
import hashlib
import json
import math
import pathlib
import platform

ROOT=pathlib.Path("/tmp/udt-gw-response-docs-L3JgrF")
pins={"DetResponse.c":"2e1d5db56170607e655a866165905b5867d537200e90dceb77c81f8832259a40","LALSimulation.c":"a10f73a39029b86d4de7c46c11ad269b0ee17a9499dce52b9b42a0bbeb1cb619"}
for name,expected in pins.items():
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==expected
definition=(ROOT/"DetResponse.c").read_text()
caller=(ROOT/"LALSimulation.c").read_text()
assert "double Pibeta = LAL_PI * beta;" in definition
assert "double beta = f * armlen / LAL_C_SI;" in caller
assert "beta = pi f L / c" in definition
def sinc(x):
    return math.sin(x)/x if x else 1.
def formula(x,mu):
    return .5*(cmath.exp(1j*x*(1-mu))*sinc(x*(1+mu))+cmath.exp(-1j*x*(1+mu))*sinc(x*(1-mu)))
def integral(x,mu,n):
    # Equal mixture of uniforms over s in[-1,1], including degenerate interval.
    # Simpson quadrature is a finite independent anchor, not certified supremum.
    def integrand(s):
        return cmath.exp(1j*x*((1-mu)+(1+mu)*s))+cmath.exp(1j*x*(-(1+mu)+(1-mu)*s))
    result=integrand(-1)+integrand(1)
    for j in range(1,n):
        result+=(4 if j%2 else 2)*integrand(-1+2*j/n)
    return result*(2/n)/12
rows=[]
for x in [0.,.02,.1,1.,3.]:
    for mu in [-1.,-.6,0.,.3,1.]:
        f=formula(x,mu)
        i1=integral(x,mu,128)
        i2=integral(x,mu,256)
        err=abs(i2-f)
        assert err<1e-7
        assert abs(f)<=1+1e-14
        bound=min(2.,2*abs(x),abs(x*mu)+(2/3)*x*x*(1+mu*mu))
        assert abs(f-1)<=bound+1e-14
        if mu==0:
            assert abs(f-sinc(2*x))<1e-14
        rows.append({"x":x,"mu":mu,"source_real":f.real,"source_imag":f.imag,"integral_error_n128":abs(i1-f),"integral_error_n256":err,"defect":abs(f-1),"analytic_bound":bound})
f=500.;L=4000.;c=299792458.
x=math.pi*f*L/c
correct=formula(x,.6)
extra_pi=formula(math.pi*x,.6)
assert abs(correct-extra_pi)>1e-3
print(json.dumps({"python":platform.python_version(),"passed":True,"source_pins":pins,"interpretation":"Source convention beta=fL/c; x=pi*beta. Source comment includes an extra pi and cannot control caller convention.","rows":rows,"max_n256_error":max(row["integral_error_n256"] for row in rows),"extra_pi_mutation":{"f":f,"L":L,"mu":.6,"x":x,"correct":[correct.real,correct.imag],"wrong":[extra_pi.real,extra_pi.imag],"disagreement":abs(correct-extra_pi)}} ,sort_keys=True,indent=2))

