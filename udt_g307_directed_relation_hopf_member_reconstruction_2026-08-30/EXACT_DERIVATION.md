# G307 exact derivation — directed relations reduce, but do not populate, the Hopf ambiguity

Date: 2026-08-30
Grade: `INTERNALLY_REPAIRED_AFTER_EXTERNAL_SCIENTIFIC_SUPPORT__FOLLOWUP_PENDING`

## Bounded landing

```text
SUPPLIED_DIRECTED_GERM_SELECTS_ONE_MEMBER_PER_CHIRAL_FAMILY
__SIGNED_TRANSVERSE_SCREEN_GERM_SELECTS_ONE_MEMBER_CONDITIONALLY
__ACTIVE_PREMISES_POPULATE_NEITHER__PHYSICAL_MEMBER_REMAINS_OPEN
```

This is preregistered candidate 2. It is a conditional reconstruction theorem on the positive
round G305/G306 completion. It does not change the metric or reciprocal kernel and does not add a
field equation, source, matter sector, scale, observation, or physical population.

## 1. Set-up

Identify the unit round three-sphere with the unit quaternions. Let `p` be a supplied point and
`v` a supplied ordered unit tangent at `p`, so

\[
|p|=|v|=1,\qquad \langle p,v\rangle=0.
\]

G306's two chiral families are the unit imaginary left- and right-multiplication fields

\[
V_L(q)=u_Lq,\qquad V_R(q)=qu_R,
\]

with `u_L` and `u_R` unit imaginary quaternions.

## 2. One member in each chirality

Requiring both fields to equal the supplied tangent at `p` gives

\[
u_Lp=v,\qquad pu_R=v.
\]

Quaternion inversion gives the unique solutions

\[
\boxed{u_L=v\bar p,\qquad u_R=\bar p v.}
\]

The maps from the imaginary quaternions to the tangent space,

\[
u\mapsto up,\qquad u\mapsto pu,
\]

are linear isometries. Hence each equation has exactly one solution in its respective chiral
`S2` family. A supplied `(p,v)` therefore reduces two continuous `S2` families to exactly two
members: one left and one right.

## 3. Why the route still cannot choose between them

Let `J_L` and `J_R` be the corresponding orthogonal complex structures. Both satisfy

\[
J_Lp=J_Rp=v,\qquad J_Lv=J_Rv=-p.
\]

They therefore agree on the entire oriented two-plane `span{p,v}`. The common great-circle route
and its tangent are

\[
q(\theta)=\cos\theta\,p+\sin\theta\,v,
\]

\[
\dot q(\theta)=\cos\theta\,v-\sin\theta\,p,
\]

and exactly

\[
J_Lq(\theta)=J_Rq(\theta)=\dot q(\theta).
\]

Thus the full one-dimensional route and metric frame carry along that route do not distinguish
chirality. The distinction is transverse, not longitudinal.

## 4. The smallest conditional discriminator

Choose an oriented orthonormal screen `(w,z)` complementary to `span{p,v}`, with
`(p,v,w,z)` positively oriented. The two complex structures act oppositely:

\[
J_Lw=z,\qquad J_Rw=-z,
\]

\[
J_Lz=-w,\qquad J_Rz=w.
\]

On a round sphere of radius `a`, the supplied Hopf field has transverse covariant derivative

\[
\nabla_wV_{L/R}=\pm\frac{z}{a}.
\]

Therefore one oriented signed transverse-screen first derivative selects exactly one of the two
remaining members. The magnitude `1/a` changes with radius; the discriminating sign does not.

This is conditional reconstruction from supplied data. It is not a theorem that the metric alone
chooses the sign or that active UDT premises populate a physical screen derivative.

## 5. Exact ownership ladder

| Supplied data | Geometric members remaining | Ownership conclusion |
|---|---:|---|
| round metric | two `S2` families | no member selected |
| point `p` | two `S2` families | no direction supplied |
| point plus ordered tangent `(p,v)` | two | one per chirality |
| complete one-dimensional route and metric carry | two | both induce the same route |
| oriented signed transverse-screen first jet | one | conditionally reconstructed |
| active-premise lawful physical population | none selected | `OPEN` |

G298–G300 already distinguish the rich metric-owned relation/control arena from a populated lawful
query family. G307 does not close that ownership boundary. It identifies the smallest local datum
that would close the G306 member ambiguity once a physical relation is supplied.

## 6. Evidence

- preregistered and pushed at `1bdfe7d2` before executable outcomes;
- 1,806 exact standard-library rational assertions across 36 oriented frames;
- all positive radii covered analytically, with five explicit scale controls;
- 32,000 implementation-independent checks over 1,000 random oriented frames, including direct
  reconstruction from `(p,v)` through independently built evaluation maps;
- maximum independent numerical error `4.1389114358025836e-13`;
- eight direct mathematical corruptions and fourteen semantic ownership mutations caught;
- current premise verifier passed after the result;
- metric and reciprocal kernel explicitly frozen and unchanged.

Fresh external review found no scientific defect and retained this exact landing, while requiring
evidence and replay repairs. R1--R4 now pass internally; repair-only follow-up remains pending.
Physical route/query/screen population, dynamics, history, mass, scale, observation, and physical
`X_max` remain open.
