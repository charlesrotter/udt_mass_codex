# Historical canonical-geometry angular-method salvage audit

Date: 2026-07-28

Status: `VERIFIED-WITH-CAVEATS_SAME_CONTEXT_INDEPENDENT_IMPLEMENTATION`

## Result

The old lepton, quark, QCD, mixing, and nuclear “prediction” chains are **not restored**. Their
load-bearing steps use one or more of a posited round `S^2`/spinor carrier, imported Standard Model,
QCD, quantum, GR, nuclear, or Gaussian/Fock structure, empirical labels visible before the rule was
fixed, searched integer/`pi` combinations, or absent calculation sources. The arithmetic formulas
can be replayed; that does not make their physical interpretation native.

The audit did find one useful change of mathematical perspective. Section 18.6 of the old document
did not study only one angular scalar. It combined the complete rank-one rotation sector with the
rank-two symmetric-traceless sector and asked what algebra they generate. Its old physical jump to
QCD was invalid, but the **complete-operator-algebra method** is reusable.

The exact correction is:

- in real dimension three, rotations have dimension `3` and symmetric trace-free deformations have
  dimension `5`; together they close `sl(3,R)`, not intrinsically `su(3)`;
- `su(3)` appears only after an additional complex/Hermitian convention turns the symmetric
  generators into imaginary anti-Hermitian ones;
- the same construction exists in every dimension: `so(n) + Sym_0(n)` has dimension `n^2-1` and
  closes `sl(n,R)`.

Therefore `3+5=8` is generic `n=3` operator algebra, not unique evidence for QCD or a UDT force.

## Current metric cross-map

The method becomes relevant because current post-July metric work independently supplies the object
on which it acts. In the registered local positive two-screen regime:

```text
End(S) = R I + so(2) + Sym_0(2)
       = area + rotation + two shape/shear components.
```

The traceless basis

```text
R  = [[ 0,-1],[ 1, 0]]
S1 = [[ 1, 0],[ 0,-1]]
S2 = [[ 0, 1],[ 1, 0]]
```

obeys

```text
[R,S1]  =  2 S2
[R,S2]  = -2 S1
[S1,S2] = -2 R,
```

so it closes exactly as `sl(2,R)`. Adding the identity gives `gl(2,R)` as the complete local screen
endomorphism type.

This matches, without changing, four current results:

- the founded-pair audit leaves three self-adjoint screen components before an extra screen-rotation
  equivariance reduces them to one scalar `lambda`;
- the angular Jacobi audit has the exact area/shape/twist decomposition `B=A_rel I+J+W`;
- the finite quotient-lift audit has `K=S+wJ`, with a symmetric response plus screen rotation;
- the ensemble atlas observes screen/shift shear, twist, and nonlinear curvature interaction.

The perspective correction is consequently concrete: `lambda` is only the isotropic trace response
after an additional equivariance restriction. It is not the complete angular response. The two
trace-free shape modes and rotation must remain visible when mapping the complete metric solution
space.

## Historical census

The registered historical spans contain 23 distinct method families:

- 8 `EMPIRICAL_NUMEROLOGY`;
- 5 `IMPORTED_COMPARISON_ONLY`;
- 5 `PURE_MATH_REUSABLE_CONDITIONAL`;
- 2 `HISTORICAL_RESULT_ONLY`;
- 1 `NATIVE_METHOD_LEAD_REQUIRES_REDERIVATION`;
- 1 `MIXED_MULTIPLE_METHOD_CLASSES`; and
- 1 current bounded exact rederivation used for the cross-map.

The source spans name 45 calculation or evidence files. An independent all-object Git-history census
finds none of those 45 paths or basenames anywhere in this repository's Git history. Their absence
does not make every written equation false, but it prevents exact replay of the claimed computations
and requires the audit to use the document's own disclosed formulas and failures only.

Notable self-disclosures in the old document include:

- the Gaussian/Fock `pi` measure was a smuggled quantization import and retracted;
- the coefficient `84` was found by algebraic search, no native operator was known to produce it,
  and an explicit cubic candidate failed by parity;
- equal Diophantine dimensions were not shown to be isomorphic representations;
- quark coefficients were found by searching combinations; and
- spectrum-to-particle assignments carried density and look-elsewhere caveats.

These failures and caveats are retained rather than filtered out.

## What was learned

`OBSERVED`: the old work repeatedly obtained close numerical comparisons after using a large menu of
integer multiplicities, powers of `pi`, imported relations, labels, boundary choices, and searched
maps. Those comparisons are historical observations only.

`DERIVED` (bounded pure mathematics): the complete real angular endomorphism decomposition and its
commutator closure are exact.

`DERIVED` (bounded current metric type): current post-July reports already contain area, rotation,
shape, and pair/screen response objects on the positive screen. This derivation does not come from
the old document.

`LEAD`: use the complete screen-response algebra as the next metric-led mapping object, rather than
asking a scalar `lambda` to carry the whole angular sector.

`OPEN`: the metric-selected response coefficients, transport through complete finite cells, global
screen bundle, physical section, dynamics, action, source, carrier, matter interpretation, and any
particle or force map.

## Four evidence gates

1. **Preregistered:** yes; the base, candidate universe, outcomes, firewall, and catches were frozen
   before the method classification and exact algebra.
2. **Full or bounded:** full for the registered angular/ratio/hierarchy/multiplet/charge/spectrum/QCD/
   mass method spans and every filename found there; not a line-by-line adjudication of unrelated
   material in the 6,892-line document.
3. **Independent verification:** yes within the same context, using a separate standard-library
   implementation; no fresh adversarial agent was authorized, so the grade remains caveated.
4. **Premises audited:** yes; every physical input, carrier, imported structure, empirical target,
   algebraic choice, and present ownership claim is separated in the ledgers.

## Maximum conclusion

The complete-angular-operator method is salvaged, and the current two-screen decomposition sharpens
the comparison-versus-realization ownership map. No historical particle, mass, charge, QCD, force,
gauge, action, carrier, source, boundary, or prediction claim is restored.
