# CES1 producer check freeze

Question: validate the first variation of the frozen positive-rapidity ensemble
from original null interception and proper normalization. Exact SymPy arithmetic,
one CPU thread, 60 seconds/512 MiB; no floating point approximation or grid.
Abstract positive bump moments B0/B1 stand for the analytic smooth-bump integrals;
this script does not replace their support/regularity proof. The sign for all
allowed densities follows analytically, not by sampled rapidities.

Check the original interception equation to first order, proper-clock ratio,
FCV1 affine-ray numerator/denominator derivative, reciprocal trace/determinant,
zero-rapidity and matched-inverse-description controls. Reject deliberately
wrong dropped-motion, dropped-rate, dropped-denominator and reciprocal-factor
expressions. Same producer code is regression only; reviewers have independent
arguments and implementations. Preserve a failed execution and its exact code
before one bounded implementation repair. No alteration of physical preparation,
measure or contrast functional is authorized by an implementation failure.
