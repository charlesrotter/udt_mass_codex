# PE1 candidate — a recovered method, not a closed product dossier

Initial candidate, not promoted; direct adversarial review pending. Sources
and precise access/exposure limits: SOURCE_LEDGER.tsv and ACCESS_AND_EXPOSURE.md.

## Product identity: three different version labels

The audited target is ESA EGG_NOM_1B baseline `_0202`, not a Level-2 gravity
field model. P1 explicitly names that baseline. A named official item indexed
by web search provides a narrower cross-check: item
GO_CONS_EGG_NOM_1b_20091111T013534_20091111T030518_0202 has processor EGG_NOM
07.00, processing centre PDS001 and processing date06Feb2019. The direct
item endpoint has not yielded a live response here; this is cached official
metadata, not authenticated current payload/header bytes or a release census.
Its sensing date is metadata, not a selected test interval. Neither its
linked quality report nor observation download was opened.

The collection citation's Version1.0, filename baseline0202 and processor07.00
are distinct labels. P2's short official table lists4.08/5.02/5.04/5.06;
it does not establish a crosswalk to07.00. P3's retrieved handbook is
issue2rev0 dated25Jun2008 despite later catalogue publication metadata.
Do not silently make either source the2018 implementation authority.

## The missing algorithm note is now available

P4 is the actual approved ESA-EOPSM-GOCE-TN-3397 issue1.0,27Aug2018,
SHA2563ba0639bd03adb2d9cbea49af6840991b0d2c7dfea67dc6d40eed2e0a47e935f.
It was found through ESA's own current search and retrieved via normal public
access. Section1.1 explicitly ties its method to2018 L1b reprocessing.
Thus the previous missing-note access gap is CLOSED for this identified
document. Its relation to a particular deployed07.00 configuration remains
a provenance dependency; neither source alone supplies a byte-level crosswalk.

## What the processing graph actually uses

P4 Figure1 (printed11, layout inspected) separates red processing blocks
from green external calibration blocks. Its inputs include nominal EGG
accelerations; AUX_ICM_1b matrices; star-tracker quaternions/flags and CCD
temperatures; AUX_EGG_DB alignments/arm lengths; SST_PSO_2 reduced-dynamic
orbit/rotation information; and ITSG-Grace2014s model coefficients. The
new EGG_NOM_1b contains calibrated acceleration, attitude, angular rates
and gradients. Those outputs share upstream inputs: they are not independent
instruments merely because separately named.

Section6.1/Table9/Algorithm9 APPLY inverse-calibration, quadratic and angular
acceleration-coupling matrices whose ESTIMATION is an external block. The
text identifies star-tracker and gravity-model calibration, including science
and shaking data, but this note does not supply the full external estimation
objective/design/weights/constraints and actual parameter provenance. It
therefore does not say which proposed trace departures that fitting absorbs.
The two-sided interpolation endpoints for science calibration are manually
chosen using onboard events and observed data quality; they need not equal
shaking epochs. Linear interpolation of these matrices is not a declaration
that the final scalar nuisance is an additive affine drift.

Section6.2/Algorithm10 uses a moving median, data-dependent flags, neighbouring
marks and interpolation. Prose describes affected common/differential
accelerations, while the displayed replacement loop specifically assigns
differential acceleration. This audit does not silently resolve that broader
prose/code discrepancy or claim an actual deployed bug. Sections7.1–7.4
also use gap interpolation, integration, symmetric angular-rate filtering,
variable edge filters and endpoint trend fits. Actual filter controls,
segmentation and calibration estimation support are needed to close raw
support. A temporal gap or different processed row name alone is insufficient.
No universal guard-gap duration is certified.

Final Algorithm16 computes six gradients from calibrated accelerations,
angular rates and arm lengths. Its displayed diagonal assignments imply

    tr(V)=-2(ad14x/Lx+ad25y/Ly+ad36z/Lz+|omega|^2).

There is no explicit final assignment Vzz=-Vxx-Vyy or other pointwise trace
projection in that block. This is a fact about the written final stage,
NOT a claim of retained target response after upstream calibration. Filtering
angular-rate inputs is not automatically scalar DC removal or trace erasure.

## A document-normalization ambiguity, not a science repair

Equations6/7 define ad=(ai-aj)/2 and rd=(ri-rj)/2. Equation9 then puts
Rd=diag(Lx,Ly,Lz). At zero rotation, eq10 yields Vii=-adii/Li with these
definitions. Algorithm16 instead gives Vii=-2adii/Li. The layouts of both
pages were inspected. They cannot use the SAME L convention simultaneously.
The latter is consistent with FULL pair separations, as used explicitly
in reviewed TM1; the introductory L equals a half separation by eq7/9.

The exact diagnostic makes this concrete: V=(2,3,5), half separations(1,2,3),
ad=(-2,-6,-15). Eq10 returns(2,3,5); Algorithm16 fed those same L values
returns(4,6,10); feeding full separations(2,4,6) returns(2,3,5). All3
Fraction assertions pass; an actual changed-factor path fails its designated
assertion. This recomputes the printed convention comparison, not the actual
processor, and is not independent proof of the physical instrument.

No source is edited, no flight normalization error is established, and no
accepted TM1/G358 convention is repaired. A deployed baseline/channel mapping
would need source/configuration/header evidence to resolve this discrepancy.

## PE1 conclusion and what the next step may use

The source map is substantially more informative: exact2018 method recovered;
baseline0202 and a cached07.00 item identified; calibration and temporal-support
dependencies localized. We have NOT closed all document/raw-support gates.
Actual calibration estimator/parameter epochs/masks, processor configuration
crosswalk, baseline convention and nuisance/error support remain unverified.
Metadata navigation shows neither public availability nor absence of every
required raw/shaking auxiliary. No archive-dependent task was attempted.

A bounded PE2 may now assess whether the WRITTEN final-stage response and
identified processing classes suffice to apply TM2, and identify the exact
missing evidence if not. It cannot call the whole pipeline fixed linear,
adopt N=[1,t], set an error threshold, select records, fit observations or
declare a released product eligible. Nor may missing information be recast
as proof of no retained signal, a new physical-premise requirement, or UDT
failure. The admitted arena/interface status remains as in WORK_ORDER.md.

## Discovery and review exposure

Main independently read sources and identified the graph/normalization issues
before reviewer summary. Source-first reviewer sealed at17:27:06UTC, then sent
its summary before main's candidate byte-freeze, including the new07.00 item
lead. Main received and independently checked that cached primary metadata.
This is disclosed pre-freeze author exposure; it does not undo the reviewer's
actual source-first independence, but author/reviewer source discovery is not
fully independent. Main has not read the full source-first proof/report yet.
New candidate direct review remains necessary. Exact model identities UNKNOWN;
different-model, human-specialist and actual flight recomputation UNTESTED.
