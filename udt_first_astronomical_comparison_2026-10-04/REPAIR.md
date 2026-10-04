# ACP1 source-preserving precision repair

INITIAL_CANDIDATE.md and its freeze remain unchanged. This repair controls the
following four points; all other scoped constructions survive. The reviewers
raised these independently during their exposed passes. No source PDF, physical
premise or astronomical value is changed.

1. **Sky-map sign, section 4.** Fix B_eo as G348's observer-to-source reverse
   block using the same future-directed affine k, with both screen bases fixed.
   Since the observed sky direction is opposite to future propagation, the
   actual map is J=-omega_o B_eo. Equation (4) and all determinants, similarity
   conditions and affine scaling are unchanged. One may change a screen basis
   but must transform all source coordinates with it; no silent sign absorption
   in an already calibrated astrometric basis is permitted.

2. **Systemic clock ownership, section 6.** Published z0 is a fitted systemic
   parameter of the conventional disk model. The SMBH center is not supplied
   as a regular emitting proper clock. Thus -log(1+z0) and tanh[-log(1+z0)] are
   initially transformed summary parameters, called Phi_summary and chi_summary
   here. Identifying them with R6's actual clock leg additionally requires a
   specified regular reference clock/history, actual null branch and a
   consistent realization of the source de-redshifting/readout. The actual
   maser-spot ratios Z_j retain the direct R6 conditional interpretation when
   the stated line/readout hypotheses hold. No regular reference is invented
   at a black-hole singularity or inferred merely from the fitted z0 label.

3. **Monitoring estimator, section 1.** Replace the phrase 'fitted two-year
   slope' by 'fitted finite monitoring-window slope.' MCP XI section 3.2 fits
   nine consecutive monitoring epochs together, repeats initializations,
   selects and averages its best fits, and bins acceleration estimates into
   VLBI spectral channels. Its overall observing campaign duration is not
   the duration of each fitted feature history. A future replay needs that
   actual estimator and feature/epoch information.

4. **Statistical versus systematic intervals, section 6.** The printed
   [80.4,95.5] Mpc interval is the marginal statistical interval from the
   reported distance errors, not a complete uncertainty region. MCP XI Table 5
   separately reports model-choice systematic 1.5 Mpc for D and 1.7 km/s for its
   systemic optical velocity; its statistical velocity interval is asymmetric.
   MCP XIII's rounded CMB summary is retained as printed. These are related
   source products, not independent data. We retain the XI systematic separately
   and do not combine it into a fabricated joint or total confidence interval.

The complete machine-readable spot table was not retrieved within the bounded
access attempts. Its printed six-row illustration is not the full data. The
reviewer also found that MCP XI's p21 count narrative is not arithmetically
self-consistent as read; no total row/parameter count is used to manufacture
the missing data, and this observation does not establish an error in the
published distance fit. The forward likelihood remains a source-owned
conditional comparison, not a replay or empirical test performed here.

The parent finite checker initially completed its algebra but failed while
writing the output because a loop variable shadowed the package path. Its
original script, stdout, stderr, freeze and exit1 receipt are preserved. The
repair renames that variable and changes only the summary labels/systematic
metadata as required above; mathematical values and test choices are unchanged.
A new exact code freeze precedes the rerun. Initial printed PASS is not treated
as completion of a failed execution. Independent checkers do not import this code.
