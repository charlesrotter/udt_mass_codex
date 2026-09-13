from pathlib import Path
import json,csv,hashlib,math,datetime
ROOT=Path.cwd(); CSS=ROOT/"udt_conditional_signal_sequence_2026-09-12";LSB=ROOT/"udt_linked_stationary_signal_benchmark_2026-09-12"
paths=[CSS/"checks/evolving_repaired.stdout",CSS/"checks/routes.stdout",CSS/"CHECK_SUMMARY.json",LSB/"checks/benchmark.stdout",LSB/"BENCHMARK_TABLE.tsv"]
evolving=json.loads(paths[0].read_text());routes=json.loads(paths[1].read_text());summary=json.loads(paths[2].read_text());bench=json.loads(paths[3].read_text());table=list(csv.DictReader(paths[4].open(),delimiter="\t"))
assert evolving["status"]==routes["status"]==bench["status"]=="PASS"
for rel,h in summary["sources"].items():assert hashlib.sha256((CSS/rel).read_bytes()).hexdigest()==h
assert len(evolving["records"])==summary["full_cases"]==12
assert len(routes["records"])==summary["route_cases"]==10
assert len(evolving["checks"])==summary["parent_guard_count"]==1044
endpoint_max=max(c["error"] for c in evolving["checks"] if c["name"]=="original_endpoint")
assert endpoint_max==summary["max_scaled_errors"]["original_endpoint"]
main_max=max(v["endpoint_residual"] for v in evolving["records"])
assert main_max==summary["maximum_endpoint_residual"]
area_error=max(abs(abs(v["screen_map"][0][0]*v["screen_map"][1][1]-v["screen_map"][0][1]*v["screen_map"][1][0])-v["area"]) for v in evolving["records"])
assert area_error<1e-12
reciprocity=[]
for rev in evolving["reverse"]:
 v=next(v for v in evolving["records"] if v["epsilon"]==rev["epsilon"] and v["source_clock"]==rev["source_clock"])
 error=abs(v["area"]/rev["reverse_area"]-v["R"]**2)
 assert error<1e-12;reciprocity.append(error)
durations=[]
for stated in summary["events"]:
 records=sorted([v for v in evolving["records"] if v["epsilon"]==stated["epsilon"]],key=lambda v:v["source_clock"])
 duration=records[-1]["arrival_clock"]-records[0]["arrival_clock"]
 ds=records[-1]["source_clock"]-records[0]["source_clock"]
 first=records[0]["R"]
 error=first*ds-duration
 for actual,key in [(duration,"arrival_duration"),(duration/ds,"mean_R"),(first,"initial_R"),(error,"single_initial_pulse_duration_error"),(error/duration,"initial_pulse_relative_duration_error")]:assert abs(actual-stated[key])<1e-13
 durations.append({"epsilon":stated["epsilon"],"arrival_duration":duration,"mean_R":duration/ds,"initial_pulse_fractional_error":error/duration})
assert len(table)==len(bench["records"])==9
mapping={"turning_radius":"p","clock_R_A_B":"clock_R_A_B","chi_clock":"chi_clock","psi_B_radians":"psi_B","angle_contrast_radians":"angle_contrast","roundtrip_cE_over_L":"roundtrip_cE_over_L","time_contrast_cE_over_L":"time_contrast_cE_over_L"}
for row,saved in zip(table,bench["records"]):
 assert [float(row["supplied_a"]),float(row["supplied_b"])]==saved["supplied_coefficients"]
 for target,source in mapping.items():assert float(row[target])==saved[source]
print(json.dumps({"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"verdict":"PASS_SAVED_READOUT_TRANSCRIPTION","sources_sha256":{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},"css_main_endpoint_max":main_max,"css_all_endpoint_guard_max":endpoint_max,"css_area_manual_determinant_error":area_error,"css_actual_reverse_area_identity_errors":reciprocity,"css_event_readouts_recomputed_from_arrival_endpoints":durations,"lsb_table_rows_all_fields_exact":len(table),"scope":"Independent arithmetic/transcription on saved FLOAT64 records; no new trajectory, geodesic proof, interval certificate or observation."},indent=2))
