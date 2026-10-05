<a id="r16tsi"></a>

#### Timed records can calibrate the conditional scale — TSI1

The missing ruler in R13OJM need not be a known source size. A specified ideal
receiver-clock record can supply a scale. This is a conditional inverse result
for R8CPR's already supplied metric and histories, not native metric selection,
an astronomical measurement or an additional physically matched-GR prediction.
H has units inverse length; write ell_o=c_E t_o for receiver proper time in
length units, with t_o in seconds. The ordinary local clock stays ordinary.

Declare the records before inversion. T is the smooth arrival map of labeled
emitter proper-clock readings against calibrated receiver proper time, giving
Z=dell_o/dell_e. A stable source frequency can instead give Z up to a constant;
unknown time-dependent source frequency need not do so. A is the same source's
pointlike angular position against receiver time in a specified parallel
transported radial frame. Neither requires source size. U is only an untimed
ordered Z/angle curve, with no known length or calibrated time interval.
These are distinct conditional interfaces, not claims of available observations.

For the inherited fixed finite-E escaping receiver and strict limiting
|b_*|<a/sqrt(f(a)), put x=1/R and

    V=sqrt(H²+(E²-1)x²+2mx³),
    s=sqrt(1+H²b²-b²x²+2mb²x³),
    alpha=1/(Ex+V)+Vb²/(1+s),
    A=x alpha, F=(1-Omega b)/(sqrt(h) alpha), Z=F(x)/x.

The limiting incidence Jacobian I_infty(1-Omega b_*) is strictly positive.
Smooth tails and the implicit function theorem give smooth actual b(x), hence
positive smooth F near0; F(0)=H(1-Omega b_*)/[sqrt(h)sqrt(1+H²b_*²)].
This derivative control is essential; Z~constant R alone would not suffice.
Since dx/dell_o=-xV,

    dlog Z/dell_o = V(1-xF'/F) -> H,
    K := lim dlog Z/dt_o = c_E H,
    H=K/c_E,   1/H=c_E/K.                              (TSI1-T)

This ideal T record fixes H independently of m,a,E and regular b_*, without a
known ruler. It does not determine those remaining parameters or select the
metric. If |F'/F|<=B on a final interval, a finite error bound is

    |dlog Z/dell_o-H| <= |V-H|+VBx,
    |V-H| <= (|E²-1|x²+2mx³)/(V+H).

B and the onset interval depend on the branch. No uniform known observational
error bar is supplied. A finite difference of log Z divided by receiver elapsed
time averages the exact rate and inherits only a justified bound on that interval.
Agreement in finite samples is not a proof that an unknown source is in this tail.

The angular route is narrower. In outgoing EF coordinates the radial unit vector
e_r=(-1/(E+v),E,0,0) and equatorial e_phi=(0,0,0,1/R) are parallel transported
along the radial receiver. Future ray directions obey

    n_phi=b/alpha,
    n_r=[s/(E+v)-v b²/(R²(1+s))]/A,
    theta=atan2(n_phi,n_r), tan(theta_*)=H b_*.

The incoming sky direction is opposite; the sign/frame convention is fixed.
For the principal preparation b_*=0, actual incidence yields
b=Omega a x/H²+O(x²), theta=Omega a x/H+O(x²). Its nonzero leading coefficient
and smooth remainder give

    -dlog|theta|/dt_o -> c_E H.                          (TSI1-A)

This is a timed source-position track, not angular size. It requires the
specified preparation and angular reference. Generic limiting angle alone
determines only H b_*; arbitrary frame rotation/centroid motion can spoil the
inference. No universal angular logarithmic rate for all preparations is claimed.

The U record retains an exact scale degeneracy. Under m,a,R,b,u,t_e,ell_o,ell_e
multiplied by lambda and H,Omega divided by lambda, E is unchanged. Corresponding
incidences have identical h,s,v,A,Z and angles; U_integral scales by lambda,
P is invariant and I scales inversely. The metric pulls back to lambda²g;
OJM1's Jacobi factors and any unknown source size co-scale. Thus combined untimed
redshift/angular data do not fix this homothety. Timed records instead satisfy
Z_lambda(t)=Z(t/lambda) with corresponding origins, and rates scale by1/lambda.
A fixed receiver calibration is physical information, not a free relabeling.
This conditional family comparison is not an adopted native UDT scale symmetry.

There is an operational limit. The finite emitter-time endpoint admits only
finitely many pulses at fixed positive spacing in any finite remaining emission
interval. Such pulses cannot sample an infinite late derivative record. A
continuous ideal phase/map, or indefinitely refined sampling, needs a separate
physical-source/resolution assessment. If nu_o=nu_e/Z, the received logarithmic
frequency drift is dlog Z/dt_o-dlog nu_e/dt_o. Constant source normalization
cancels; arbitrary variability can mimic a finite record. Positive endpoint
frequency with bounded logarithmic derivative in emitter proper time makes
that contaminant decay as1/Z, but this regularity is an extra source condition,
not a derived material or astronomical fact. Angular tracking likewise needs
late visibility and resolving power. No practical detectability is established.

c_E supplies the conversion from measured K to a length. This added dimensional
timing record is exactly what the c_E/G_obs-only obstruction does not include.
G_obs allows the mass-dimension combination c_E³/(G_obs K), but it is not a
derived physical mass or an independent second constraint. A proposed
m=G_obs M/c_E² interface would need separate justification and independent M;
co-scaling a geometric mass or defining M from the measured K adds no datum.
MGC1's independently justified mass/density routes remain possible and open.
No physical X_max or observed Hubble parameter has been identified.

The [frozen candidate](udt_timing_scale_identifiability_2026-10-05/INITIAL_CANDIDATE.md)
owns the full argument and [work record](udt_timing_scale_identifiability_2026-10-05/WORK_RECORD.md)
records exact/finite checks, actual separate-context reviews, exposure and limits.
The positive change is a ruler-free conditional scale interface. The negative
result concerns untimed records; it does not extend to calibrated time histories.
Finite practical inversion, empirical source admission and native geometry
selection remain separate gates. The [return brief](udt_timing_scale_identifiability_2026-10-05/DECISION_BRIEF.md)
states the next bounded proposal without launching it.
