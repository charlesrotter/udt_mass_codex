# G73 exact derivation — global-sky source sensitivity

Date: 2026-08-11

Primary landing:

`REGULAR_SKY_RESPONSE_SOURCE_INVERTIBLE__ROBUST_KALEIDOSCOPE_REQUIRES_GLOBAL_BRANCHING_SINGULARITY_OR_SOURCE_RESTRICTION`

This is a response-classification theorem. It is not a physical CMB source, sky, spectrum, or
prediction.

## 1. Correctly typed global question

Let `S_o` be a supplied observer sky and `S_s` a supplied source surface/sky. A single regular
query branch gives a map

```text
f:S_o -> S_s
```

and, after the G72 same-query screen transport is factored out, a pointwise response

```text
M(n)=U(n)^-1 D(n) in GL+(2).
```

For a scalar source `s`, the branch supplies a pullback `s_o(n)=s(f(n))`. For a source-screen
vector `v`, transported observer coordinates give

```text
v_o_tilde(n)=M(n) v(f(n)).                                  (1)
```

Equation (1) is conditional on the physical source actually having that tensor type. It is not a
TT or polarization law.

## 2. Regular one-to-one response retains the source exactly

If `f` is a diffeomorphism and every `M(n)` is invertible, then

```text
s(p)=s_o(f^-1(p)),
v(p)=M(f^-1(p))^-1 v_o_tilde(f^-1(p)).                       (2)
```

Thus the complete regular response can produce a visually complicated rearrangement, scale,
shear, and rotation while retaining all arbitrary source information. Geometry does not force two
distinct unrestricted sources to the same output.

This is an information statement, not a claim that geometry is visually unimportant. A complicated
invertible map can dominate the appearance of one particular realization while remaining exactly
reversible.

The symbolic check verifies the generic `2 x 2` inverse. An independent finite global witness uses
three source pixels, three invertible local blocks, and a nontrivial pixel permutation. Its full
`6 x 6` response has exact rank six and an exact inverse.

## 3. Strong shear can make directions geometry-dominated

Write the positive canonical response, ignoring common scale and rotation, as

```text
P=ell diag(exp(chi),exp(-chi)).                              (3)
```

For an input direction `v=(cos alpha,sin alpha)`, the output angle `beta` satisfies

```text
tan beta = exp(-2 chi) tan alpha.                            (4)
```

For input directions uniform modulo sign, the exact fraction lying within an unoriented cone
`epsilon` of the dominant output axis is

```text
F(chi,epsilon)=(2/pi) atan(exp(2 chi) tan epsilon).          (5)
```

For every fixed `epsilon>0`, `F -> 1` as `chi -> infinity`. Except for the exact minor-axis source
direction, a sufficiently strong shear aligns the normalized output with the geometric dominant
axis. That is a genuine geometry-dominated *directional* limit.

It does not erase source amplitude. In the limit the surviving leading amplitude is proportional
to the source magnitude times `|cos alpha|`; the exceptional minor-axis direction behaves
differently. No current branch/profile is shown here to realize `chi -> infinity`.

## 4. What a true kaleidoscope requires

There are two mathematically different repeated-image cases.

### 4.1 One source feature copied to several observer directions

If `f:S_o -> S_s` is noninjective, distinct observer directions can sample the same source point.
An exact discrete witness maps two source values to four observer values as

```text
(x1,x2) -> (x1,x2,x1,x2).                                   (6)
```

The source remains recoverable, but the geometry imposes exact repeated-image correlations. This
is the clean mathematical analogue of a kaleidoscope overwhelming the organization of an ordinary
source without manufacturing the source itself.

For a smooth self-map `S^2 -> S^2`, an everywhere regular local diffeomorphism is a covering map.
Because connected `S^2` is simply connected, a nontrivial multiple self-cover cannot remain regular
everywhere. A repeated whole-sky self-image therefore requires critical/branch points. This
statement is restricted to the `S^2` self-map case; different source topology or a partial sky must
be classified separately.

### 4.2 Several source/path branches arriving at one observer direction

The metric may return a branch-labelled family

```text
{M_i(n) v(p_i)}_i.                                          (7)
```

That set is not yet a single observable. Summing, averaging, choosing, phase-combining, or assigning
weights to its members requires an additional query/source/detector rule. No such owner is present
in G68--G72.

## 5. Caustic or fold limit

At `det(D)=0`, the G72 regular response leaves its domain. The exact rank-one witness

```text
diag(1,0)(x1,x2)=(x1,0)                                     (8)
```

shows how geometry can collapse one source direction. The remaining amplitude `x1` is still source
data. A caustic can therefore create strong geometric organization, but G72 supplies no rule for
continuing, regularizing, combining, or measuring the branches across it.

## 6. Complete G68 control replay

All 21 frozen maps are regular. Independent direct SVD gives

```text
max chi                         0.0023238059699749714
max singular-value ratio       1.0046584288394136
max anisotropy gain            0.46584288394135864 percent.
```

For the strongest row, equation (5) changes the fractions inside the preregistered unoriented
cones only from

```text
5 degrees:   0.0555555556 -> 0.0558130361
15 degrees:  0.1666666667 -> 0.1674078470
30 degrees:  0.3333333333 -> 0.3346160010.
```

So the registered stationary/equatorial G68 tile is weakly anisotropic, not strongly
kaleidoscopic. This says nothing about a complete sky near the positional-dilation asymptote; G68
does not sample that object.

G68 azimuthal carry `psi` remains distinct from relative image rotation and is not used in this
strength classification.

## 7. The user's two physical possibilities both survive

1. `UNIQUE_SOURCE_PLUS_UDT_RESPONSE`: the universe's actual nonhomogeneous mass/geometry field is
   decisive, while UDT remaps and distorts its appearance. This is fully compatible with the exact
   regular result.
2. `ROBUST_GEOMETRIC_KALEIDOSCOPE`: many ordinary sources acquire common repeated or highly aligned
   motifs because the global relation branches, folds, or becomes strongly anisotropic. This
   remains a live but unselected global possibility.
3. Intermediate regimes can preserve source-specific fine structure while geometry controls broad
   organization.

## 8. Exact boundary and next gate

No seed ensemble can resolve the fork before the complete global relation map is supplied. On a
regular bijective map, sampling more arbitrary seeds merely confirms exact invertibility. The next
metric-led calculation is therefore the branch/critical atlas of a complete symbolic-scale
observer-sky relation:

- determine where the sky map is one-to-one, multi-covering, set-valued, or singular;
- retain the complete angular sector and mixing;
- keep the global scale symbolic;
- do not use SNe, `X_max`, bootstrap, or CMB observations as selectors;
- introduce source ensembles only after the relation topology and physical readout type are owned.

The physical endpoint/profile/global scale, actual source distribution/statistics, detector rule,
and TT/TE/EE/BB map remain `OPEN_NO_OWNER`.
