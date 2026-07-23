# Review disposition

Date: 2026-07-23

The first fresh adversarial review returned `PASS-WITH-CAVEATS`. Its six
required corrections were preregistered at commit `535f3c4` before any draft
result was changed.

The correction layer:

1. scopes `span{I,*}` to connected, orientation-preserving Lorentz symmetry
   and proves the full orientation-reversing commutant is scalar;
2. records `D` and `D^-1` as equally compatible inverse solderings with
   physical sector ownership open;
3. directly sources and replays the registered `dphi` causal census;
4. distinguishes independent local algebra from direct parsing/hash checking
   of frozen atlas classifications;
5. adds five exercised operator-level mutation catches; and
6. adds explicit full-`D` CSN and induced null two-form rank/nilpotence
   checks.

The fresh post-correction review returned `PASS`. It independently reproduced:

- the timelike and spacelike rank-three plus rank-three reduction;
- Hodge exchange, reciprocal inversion, and CSN invariance;
- the rank-one tangent and rank-two two-form null nilpotents;
- the connected/full Lorentz commutant distinction;
- failure of unequal complex chiral weights to descend to real geometry;
- the exact `3072/2304/768` frozen causal census;
- `37/37` production checks, `29/29` independent checks, `25/25` catches,
  `60/60` source hashes, and 30 unique object rows; and
- the repository baseline of 70 passed and one expected failure.

No required correction remains. Optional future work is not authority: a
separate audit may test whether any selected complete branch keeps `dphi`
everywhere nonzero and nonnull and supplies a global section or toric/Hopf
join.
