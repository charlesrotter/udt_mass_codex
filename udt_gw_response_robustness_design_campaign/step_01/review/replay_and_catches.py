"""Same-code replay and in-memory mutation catches, distinct from independent math."""
import contextlib
import hashlib
import io
import json
import pathlib
import platform
import traceback

P=pathlib.Path(__file__).resolve().parents[1]
script=P/"checks.py"
source=script.read_text()
assert hashlib.sha256(script.read_bytes()).hexdigest()=="0be202298d3d5c523f53443786e3776b66196f4f9e461fd61d4ef1c767aeb152"
def execute(text):
    output=io.StringIO()
    ns={"__name__":"__main__","__file__":str(script)}
    with contextlib.redirect_stdout(output):
        exec(compile(text,str(script),"exec"),ns)
    return output.getvalue(),ns
output,ns=execute(source)
saved=(P/"checks_run.stdout").read_text()
assert output==saved
expected=["amplitude_free_error","varying_response_commutes_with_common_filter","retained_band_bounds_windowed_signal","training_uniquely_fixes_distinct_holdout","extra_pi_convention"]
assert ns["caught"]==expected
# Independently force the five invalid assertions outside the producer reject helper.
wrong_assertions={
"amplitude_free_error":lambda:ns["leakage"]<=.01,
"varying_response_commutes_with_common_filter":lambda:ns["mixed"]==0,
"retained_band_bounds_windowed_signal":lambda:abs(ns["after"][2])<1e-14,
"training_uniquely_fixes_distinct_holdout":lambda:ns["radius"]==0,
"extra_pi_convention":lambda:abs(ns["transfer"](ns["x"],.6)-ns["transfer"](ns["math"].pi*ns["x"],.6))<1e-12}
catches=[]
for name,fn in wrong_assertions.items():
    try:
        assert fn(),name
    except AssertionError as e:
        catches.append({"name":name,"rejected":True,"exception":str(e)})
    else:
        raise AssertionError("independent execution failed to reject "+name)
mutations=[
("wrong_training_denominator","/ (1 - kappa)","/ (1 + kappa)"),
("wrong_interpolant_norm","exact_norm2 = float(v @ coeff)","exact_norm2 = float(v @ v)"),
("wrong_sharp_radius","radius = math.sqrt(p_norm2 * (hmax*hmax-h0_norm2))","radius = math.sqrt(hmax*hmax-h0_norm2)"),
("wrong_sinc_normalization","np.sinc(x*(1+mu)/np.pi)","np.sinc(x*(1+mu))")]
records=[]
for name,old,new in mutations:
    assert source.count(old)==1,name
    modified=source.replace(old,new)
    try:
        execute(modified)
    except AssertionError as error:
        frames=traceback.extract_tb(error.__traceback__)
        producer=[x for x in frames if x.filename==str(script)]
        records.append({"name":name,"rejected":True,"failed_line":producer[-1].lineno,"failed_expression":producer[-1].line,"message":str(error)})
    else:
        raise AssertionError("mutant survived: "+name)
print(json.dumps({"passed":True,"python":platform.python_version(),"replay_byte_identical":True,"replay_stdout_sha256":hashlib.sha256(output.encode()).hexdigest(),"original_five_defect_assertions_reexecuted":catches,"four_in_memory_producer_mutations":records,"files_changed_by_test":[],"evidence_type":"same-code regression and defect catches only; independent methods in separate reviewer scripts"},sort_keys=True,indent=2))

