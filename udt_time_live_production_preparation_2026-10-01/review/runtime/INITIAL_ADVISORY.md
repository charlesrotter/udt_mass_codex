# TPP1 runtime and scope review intake

Actual separate context: `/root/tpp_runtime`, same inherited model. This review
attributes top-level startup, synchronization and unchanged full406 audit to the
parent. It independently read the work order and verified HEAD
`90d9bc49e2fed787d9068b0a50e13a62ac58021b`, branch `grok`, and no tracked changes.
Unrelated untracked names were inspected only through git status; protected
payloads were not opened. Review writes remain under this directory. CPU checks
are limited to180s/4GiB each; this reviewer uses no GPU.

Before the new implementation, reviewed the original immutable checkpoint
module, TDS1 worker, its guard/artifact reviewer and its covariant-momentum
Hamilton/RK45 clock reviewer. Reuse of the latter, if needed, will be explicit:
it is a distinct implementation from the producer ray integrator, not a newly
independent mathematical method or independent simulation.

The dyadic timestep design can reuse the existing checkpoint convention if
`step=tick` and every accepted time is exactly `1+tick*dt_min` to floating-point
representation. Steps must land on output-window, checkpoint and terminal ticks;
restart must reconstruct scheduling from signed inputs and the saved tick. Any
stateful adaptive controller would itself need saving. The present proposal uses
state-derived speed bounds, which can avoid that extra state.

Planned checks examine invalid and nonfinite inputs before GPU imports, cadence
and step-floor behavior, direct immutable metadata hashes, pause/resume and
signal restart arrays, explicit resource stops, selected independent null-ray
readouts, and whether the dispatch exceeds measured workload or scientific scope.
Incomplete and diagnostic records must remain ineligible for restart. A failed
output write must leave the prior committed checkpoint usable and give an
explicit output-limit reason. Passing any finite suite will not establish all
failure modes, nonlinear stability, native UDT field selection or a full census.

No substantive acceptance is issued at intake; the changed worker and actual
saved artifacts remain to be reviewed.
