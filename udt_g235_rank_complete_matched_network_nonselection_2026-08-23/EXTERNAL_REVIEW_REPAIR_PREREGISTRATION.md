# G235 external-review repair preregistration

Date: 2026-08-23

The fresh sealed external review returned `G235_ACCEPTED_WITH_CAVEATS`. It found no scientific or
type error in the bounded `NO_CANDIDATE` result, but identified reproducibility weaknesses before
the package is banked. The following repairs are registered before modifying the evidence:

1. make a rebuilt sealed intake unambiguously self-contained by placing all frozen manifest sources
   below the package's own `SEALED_SOURCES/` directory and make `verify_package.py` resolve and
   containment-check that source root when present;
2. add a no-write mode to both executable derivations so a strict read-only reviewer can recompute
   their results without overwriting frozen evidence;
3. strengthen the independent replay to instantiate all six pair completions separately for every
   sampled member of each preregistered profile and to compare their six constructed clock entries;
4. replace the production script's tautological common-clock check with comparisons of the six
   actually constructed pair pullbacks;
5. add one exact two-chart overlap/reparameterization check to the production and independent
   evidence;
6. preserve the first external review verbatim, rebuild a fresh sealed intake, and request only a
   repair-follow-up verdict on these registered items and the unchanged bounded landing.

The candidate condition, twin profiles, separator, scientific landing, quantifier boundary, and
maximum conclusion may not change during these repairs.
