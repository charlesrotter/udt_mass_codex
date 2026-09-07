# Decision brief — completed, reviewed sensitivity limitation

The public three-detector data are accessible, but the chosen sensitivity
screen is not useful at its frozen target. One allowed background record
sets an exceptionally high threshold. The corrected synthetic tests cross
it only 5/168, 3/168 and 3/168 times across the three specified families,
versus the required 152/168. Even the largest predeclared amplitude gives
only 8/168 in each family. This is a negative result about this particular
procedure, not a verdict against interferometers or UDT.

FW1 and FW2 R1 are VERIFIED-WITH-CAVEATS at their exact narrowed scopes.
The campaign is complete after two reviewed steps, stopping at its declared
failed sensitivity gate. The reserved event window has not been opened.
No new constraint on geometric freedom has been obtained; no third step was
manufactured. There is no remaining runtime/access blocker for this return.

## What the result actually depends on

The admitted conditional wave/readout class permits two freely supplied
waveform functions. Under the chosen static, finite cyclic response,
three consistently delay-aligned channels leave one algebraic contrast
r=sum_i b_i d_i, with column b satisfying b^T F=0. Here d_i includes the
frozen zero-DC/Nyquist projection and cyclic delay alignment.
The statistic is Q=||Lr||^2, where L contains the fixed crop, Hann window,
frequency selection and PSD weights. Twelve background records fix the PSD;
the maximum Q over 21 other records fixes the threshold. No waveform template,
binary mechanism or physical-content law is selected.

The residual injection target is h_rss=1e-21 strain sqrt(second), normalized
over the 90-second core before Hann. Fractions use 21 backgrounds times 8 frozen
synthetic draws per family; they are not population power or confidence.
The extreme record has Q=31313.96 versus roughly 1 for the others. Its
decomposition is Virgo-channel-dominated; its physical cause is unresolved.
No record was deleted or threshold retuned. The finite identity does not
certify rotating, finite-arm or upstream physical signal preservation.

The metric supplies the conditional tidal relationship; conventional
interferometer/optical transfer, astrometry and error treatment are supplied
measurement assumptions. Sky/time/window are ordinary query data. Waveform
functions remain free. Calibration estimates are not hard joint bounds:
see the matched [O2 release](https://gwosc.org/o2_details/) and
[calibration records](https://dcc.ligo.org/T2100313/public).

## Decision and next bounded proposal

Recommend a background-robustness and response-error design gate, not another
event analysis: determine whether one defensible, prospectively frozen
contrast can tolerate background excursions while retaining a quantified
physical response/error interpretation. Use the exposed records as development
data only. Before any new confirmation data, freeze the statistic, exclusions,
target and uncertainty assumptions. A failure would park this procedure;
a success would justify a new, genuinely unused off-source validation—not
opening the event automatically. Exact proposed scope/budget/review/stops are
in [NEXT_WORK_ORDER.md](NEXT_WORK_ORDER.md). This proposal is NOT authorized.
Alternatively park this instrumental route and choose geometric/emergence work;
neither direction is blocked by this result or requires the other first.

Initial failed generators and reviews are preserved. Review found that rounded
frequency labels dropped an inclusive endpoint; one same-premise repair used
exact integer bins, without changing the frozen bands or decision rule.
The [FW2 review](step_02/review/FINAL_REVIEW.md) independently recomputed the
actual PSD, all reference values and all 504 target additions. The separate
contexts used different implementations; exact reviewer models are UNKNOWN,
and different-model, human-specialist and formal-verification axes UNTESTED.
Accepted grades, premises, canon and fixed-snapshot manuscript are unchanged.
GOCE stays PARKED, eligibility OPEN/UNRESOLVED, enquiry UNSENT. Backup
completeness and pre-reboot unsaved-state disposition remain UNVERIFIED.
