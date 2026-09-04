# G338 post-review evidence hardening

The fresh external review accepted the bounded G338 scientific result without a
required repair. It noted, as optional low-severity hardening, that the
package-only aggregate replay used an explicit source-absence fallback when
executed outside the repository.

After acceptance, `verify_package.py` was hardened so that an in-repository
replay authenticates each frozen source either from its current bytes or from
the preregistration commit `01e2110a`. The sealed-intake fallback remains
explicit because a review intake intentionally has neither the repository nor
its Git history. The repository-wide premise verifier now also executes the
aggregate verifier in no-write mode.

This is an evidence-path repair only. It does not change the metric, pair carry,
kernel, formulas, test tolerances, result artifacts, conclusion, or external
review response. The reviewer's other optional note—mechanizing the
source-metric-to-`G` bridge inside the independent script—remains deferred; the
reviewer independently rederived that bridge and did not require a repair.
