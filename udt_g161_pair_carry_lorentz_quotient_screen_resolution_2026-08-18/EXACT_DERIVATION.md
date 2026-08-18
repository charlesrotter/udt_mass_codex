# G161 exact derivation — pair carry as a Lorentz quotient

Date: 2026-08-18

## Landing

`PAIR_FIRST_JET_IS_EXACT_LORENTZ_STABILIZER_QUOTIENT__POSITIVE_BPLUS2_IS_UNIQUE_TIME_ORIENTED_GAUGE_SECTION_ON_FUTURE_TIMELIKE_CLOCK_STRATUM__DISTANCE_SWEEP_FIXES_QUOTIENT_PATH_AND_FIRST_JET_NOT_VERTICAL_RAPIDITY__SCREEN_NORMAL_TRANSPORT_DOES_NOT_UNIVERSALLY_RESOLVE_TANGENT_BOOST__NORMAL_GAUGE_INVARIANT_EXTRINSIC_SIMPLE_CAUSAL_SPECTRUM_CONDITIONALLY_FIXES_PAIR_FLAG__DEGENERATE_NULL_AND_GLOBAL_STRATA_OPEN__PHYSICAL_CARRY_HISTORY_QUERY_AND_COMPLETION_OPEN`

This is preregistered outcome class 4.

## 1. Exact finite quotient

Let `h` be the regular Lorentzian pair metric in a supplied target pair frame and let a carry
`M in GL+(2)` act by

\[
\pi_h(M)=M^T hM.
\]

If two carries have the same pullback, define

\[
L=M_2M_1^{-1}.
\]

Then

\[
L^ThL-h
=M_1^{-T}\left(M_2^ThM_2-M_1^ThM_1\right)M_1^{-1}.
\]

Therefore

\[
\pi_h(M_1)=\pi_h(M_2)
\quad\Longleftrightarrow\quad
M_2=LM_1,\qquad L^ThL=h.
\]

Let

\[
\mathcal D_h=\{M\in GL^+(2):Me_0\text{ is future timelike}\}.
\]

After orientation and time orientation are fixed, each regular fiber is exactly one left
`SO+(h)` orbit. Thus the correctly typed quotient is

\[
SO^+(h)\backslash\mathcal D_h,
\]

or `SO+(1,1)\D_eta` after a target orthonormal pair frame identifies `h=eta`. This is not merely a
counterexample to faithful reconstruction: it is the complete finite classification of what the
pair metric forgets.

Dimensionally,

\[
\dim GL^+(2)-\dim SO^+(1,1)=4-1=3,
\]

which is exactly the number of independent entries of a Lorentzian `2 x 2` pair metric.

## 2. Exact first-jet quotient

At the identity of the stabilizer, an infinitesimal vertical rate `A` satisfies

\[
A^Th+hA=0.
\]

For `h=eta=diag(-1,1)` and

\[
A=\begin{pmatrix}a&b\\c&d\end{pmatrix},
\]

the condition is

\[
\begin{pmatrix}-2a&c-b\\c-b&2d\end{pmatrix}=0,
\]

so

\[
A=\omega
\begin{pmatrix}0&1\\1&0\end{pmatrix}.
\]

Thus a carry first jet `(M,dot M)` has eight local components, while the carried pair first jet
`(hbar,dot hbar)` has six. The two missing jet components are the finite rapidity and its rate.

More generally, let `h(lambda)` vary and let a smooth `L(lambda)` obey

\[
L(\lambda)^Th(\lambda)L(\lambda)=h(\lambda).
\]

For

\[
M'(\lambda)=L(\lambda)M(\lambda),
\]

one has identically

\[
M'^ThM'=M^ThM.
\]

Differentiating gives equality of the complete pair first jets. Repeating the differentiation
shows that an arbitrarily long smooth distance sweep, and indeed every derivative of its pair
metric, remains blind to a freely varying vertical rapidity whenever the lift remains regular.

The sweep is still informative: it fixes the complete quotient path and all of its metric-visible
derivatives. It does not fix a representative above that path.

## 3. The positive triangular carry is the unique quotient section

Work in a supplied future-oriented target orthonormal pair frame, so `h=eta`. Write

\[
M=\begin{pmatrix}p&q\\r&s\end{pmatrix},
\qquad \det M>0,
\]

and require its first column to be future timelike:

\[
p>0,\qquad p^2-r^2>0.
\]

Set

\[
a=\sqrt{p^2-r^2}>0
\]

and define

\[
\Lambda(M)=\frac1a
\begin{pmatrix}p&-r\\-r&p\end{pmatrix}.
\]

Then

\[
\Lambda^T\eta\Lambda=\eta,
\qquad \det\Lambda=1,
\]

and

\[
B=\Lambda M
=\begin{pmatrix}
a & \dfrac{pq-rs}{a}\\[2mm]
0 & \dfrac{ps-qr}{a}
\end{pmatrix}.
\]

Both diagonal entries are positive because `a>0` and `det M>0`. Hence `B` lies in positive
upper-triangular `B+(2)`.

For uniqueness, write a general future boost as

\[
\Lambda'=\begin{pmatrix}c&-u\\-u&c\end{pmatrix},
\qquad c^2-u^2=1,\quad c>0.
\]

The lower-left entry of `Lambda' M` vanishes exactly when

\[
-up+cr=0
\quad\Longrightarrow\quad
\frac uc=\frac rp.
\]

The timelike and future conditions give one and only one such boost. Therefore every orbit in the
regular future-clock stratum has a unique positive triangular representative.

This upgrades G160's statement. `B+(2)` is not merely a convenient physically restricted carry
class here. It is a canonical gauge section of the quotient after a target orthonormal pair frame,
time orientation, and pair orientation are supplied. It does **not** thereby become the physical
carry.

The section fails when the clock column is null (`a=0`), past-directed, or leaves the chosen
oriented component.

## 4. The terminal pair variables are quotient coordinates

Writing

\[
B=\begin{pmatrix}a&b\\0&d\end{pmatrix},
\qquad a,d>0,
\]

gives

\[
B^T\eta B
=\begin{pmatrix}
-a^2&-ab\\
-ab&d^2-b^2
\end{pmatrix}.
\]

Comparing with

\[
h=-T^2(d\tau+\beta\,d\sigma)^2+L^2d\sigma^2
\]

returns exactly

\[
T=a,\qquad \beta=\frac ba,\qquad L=d.
\]

Consequently `(T,beta,L)`, equivalently `(kappa,phi,beta)`, are the three quotient coordinates.
They are not three partial clues from which the fourth carry coordinate should normally be
recovered. The fourth coordinate is the Lorentz representative removed by the quotient.

## 5. Why screen and normal transport do not universally fix the boost

Consider flat product geometry with adapted metric

\[
g=\operatorname{diag}(-1,1,1,1)
\]

and pair plane `span(e0,e1)`, normal screen `span(e2,e3)`. The pair immersion is totally geodesic,
so

\[
II=0,\qquad D^\perp\text{ is flat},\qquad U^\perp_\gamma=I.
\]

For any tangent boost `L in SO+(1,1)`, the full adapted-frame change

\[
\mathcal L=\operatorname{diag}(L,I_2)
\]

preserves the complete metric, pair metric, screen metric, zero second fundamental form, normal
connection, and normal holonomy. Yet the tangent frame representative changes.

Thus no universal solder from the normal screen or its transport to tangent rapidity follows from
the complete metric identities. A complete coframe representative can record the rapidity, but
G159's live Lorentz covariance prevents treating that representative as physical without an
additional ownership statement.

## 6. Conditional extrinsic resolution

On a **supplied regular timelike pair immersion**, let `A_A` be its two shape operators in an
orthonormal normal frame. Define

\[
\mathcal C_{II}=\sum_{A=2}^{3}A_A^2.
\]

Under a normal rotation `R in O(2)`,

\[
A'_A=\sum_B R_{AB}A_B,
\]

so

\[
\sum_A(A'_A)^2
=\sum_{A,B,C}R_{AB}R_{AC}A_BA_C
=\sum_BA_B^2.
\]

Each shape operator is self-adjoint for the induced Lorentz metric, hence `C_II` is also
self-adjoint.

If `C_II` has two distinct real eigenvalues, its eigenlines are `h`-orthogonal. In Lorentzian
dimension two, two independent orthogonal eigenlines cannot be null; one is timelike and one is
spacelike. Time orientation chooses the future direction and pair orientation fixes the remaining
spatial sign. Therefore the simple-real-spectrum stratum supplies a canonical tangent flag and
removes the continuous boost ambiguity.

This is a sufficient conditional construction, not a universal law. It requires the pair immersion
that owns `II`, and it fails on explicit admitted strata:

- totally geodesic or umbilic data make `C_II` scalar;
- `C_II=[[5,5],[-5,-5]]` has zero discriminant and a null/Jordan flag;
- `C_II=[[0,36],[-36,0]]` has discriminant `-5184` and no real eigenflag;
- eigenvalue crossings can branch the flag along a sweep;
- global continuation and monodromy were not classified.

## 7. What was and was not derived

Derived within the bounded regular stratum:

1. the pair metric is the exact Lorentz-stabilizer quotient of the carry;
2. the pair first jet is the corresponding first-jet quotient;
3. the positive triangular representative is the unique time-oriented quotient section;
4. a full smooth separation sweep fixes the quotient curve, not vertical rapidity;
5. normal transport alone does not universally remove the tangent boost;
6. simple extrinsic spectrum conditionally supplies a canonical pair flag.

Not derived:

- that vertical rapidity is physically real rather than coframe gauge;
- that the triangular section is the physical carry;
- that every physical query supplies an immersion with simple extrinsic spectrum;
- behavior at null, singular, crossing, cut, or global strata;
- the physical history, query, carry, dynamics, `X_max`, or observational predictions.
