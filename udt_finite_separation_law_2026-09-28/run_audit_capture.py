"""Reuse the existing capture utility with only declared audit resource changes."""
import hashlib
import pathlib
import sys

root = pathlib.Path(__file__).resolve().parent.parent
source = root / 'udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py'
raw = source.read_bytes()
assert hashlib.sha256(raw).hexdigest() == '8ff5469ace76bdfc84188915242abbf3baff35516f9ee3f9ba4b1cbfeb2573ef'
code = raw.decode().replace('512 * 1024**2', '2048 * 1024**2')
code = code.replace('(60, 60)', '(900, 900)').replace('timeout=60', 'timeout=900')
code = code.replace('cpu_seconds=60', 'cpu_seconds=900')
exec(compile(code, str(source), 'exec'), {'__name__': '__main__', '__file__': str(source)})
