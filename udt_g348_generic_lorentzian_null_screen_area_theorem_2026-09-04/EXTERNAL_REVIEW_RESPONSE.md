# External review response — G348

Date: 2026-09-04  
Role: fresh zero-context adversarial mathematical-relativity, Lorentzian-geometry, Jacobi-field, symplectic-transport, caustic, and evidence-integrity review

## Scope and method

I treated the mounted intake as the only evidentiary source. Before inspecting payload content or executing a replay, I copied it with preserved layout and metadata to:

`/work/g348_external_review_sealedcopy.b2HR7U/intake`

All execution used that copy. I did not edit `/intake`, access a repository or protected package, browse the web, download anything, install anything, or use a network-capable program. A separate scratch reconstruction was placed outside the copied intake at `/work/g348_external_review_sealedcopy.b2HR7U/scratch_reconstruction.py`.

The bounded question is answered only for infinitesimal quotient-screen Jacobi geometry along a supplied regular affinely parametrized null geodesic of a supplied smooth four-dimensional Lorentzian metric. “Regular” concerns the metric and nonzero tangent; it does not exclude conjugate points.

## 1. Evidence authentication

The authentication results are:

- `REVIEW_SCOPE.json` SHA-256: `3f1dc71c37a2352c8ecda0b88fb826cd1707a5a0220403b8ec566f24854c10cf`.
- `REVIEW_MANIFEST.tsv` SHA-256: `e6558faf549f1fbf5df09fd947b0ff7bc1e1cbf707a795b06ef299cd73e7c8d2`.
- `REVIEW_MANIFEST.sha256` SHA-256: `ca5dbecc025ce59c80a1896632916f249bc4ccc66bb8a0257c72b353e053c8e4`.
- The digest declared inside `REVIEW_MANIFEST.sha256` exactly matches the manifest digest.
- The scope declares 33 payloads, contains 33 distinct paths, and the manifest has 33 distinct rows with the identical path set.
- The complete intake contains exactly 35 regular files: those 33 payloads plus `REVIEW_MANIFEST.tsv` and `REVIEW_MANIFEST.sha256`. There are no extra files, missing files, symlinks, or special files.
- Every registered byte count and every registered SHA-256 passes against `/intake` and independently against the preserved copy.
- All 35 source files and their copies are byte-identical.

This establishes exact internal consistency of the sealed intake against its supplied checksum chain. The hashes are unkeyed and have no external signature or independently supplied trust anchor, so they do not by themselves prove authorship or historical provenance. Likewise, `GIT_PREREGISTRATION_PROOF.txt` is a documentary transcript: the stated commit/push chronology cannot be independently checked under the explicit prohibition on repository access. That limitation is non-mathematical and is retained rather than silently promoted to stronger authentication.

## 2. Replay audit

Static inspection of all four Python executables found only standard-library imports. The three scientific replays import combinations of `json`, `math`, and `random`; the aggregate additionally uses `ast`, `hashlib`, `os`, `pathlib`, `subprocess`, and `sys`. No dynamic import, network client, package installer, shell downloader, or evidence-writing primitive occurs in the scientific replays. The aggregate invokes only the three local registered scripts with the active interpreter, `-B -S`, `PYTHONDONTWRITEBYTECODE=1`, and `UDT_NO_WRITE=1`.

The registered aggregate replay completed with exit status zero and reported `18/18` gates. Its underlying results were:

- production: `39542/39542` assertions;
- implementation-distinct verification: `9759/9759` assertions;
- hostile controls: `21/21` mutations reported caught.

I wrapped the aggregate with an independent digest of every regular file in the whole copied intake and every file in `/intake`. Both complete trees had identical byte digests before and after execution. No bytecode directory or other generated evidence artifact appeared.

The replay is regression support, not a proof of a universal theorem. The so-called hostile controls are especially weak as scientific evidence: `valid(candidate)` is literal equality with a frozen dictionary, so each one-field mutation is caught tautologically. The aggregate's phrase hooks are documentary integrity guards. The implementation-distinct route is genuinely different computational code, but it shares the same mathematical premise of a symmetric screen tide and is not premise-independent.

The recorded first production failure is legitimate and correctly preserved. Equality of the magnitudes of `sin(L)sinh(L)` at equal finite offsets about `pi` is not the definition of a simple zero because the nonvanishing `sinh(L)` factor is asymmetric. Replacing that diagnostic with a centered first derivative for the rank-one witness and a centered second derivative for the rank-zero witness is mathematically correct and does not alter the theorem. The first aggregate failure was only a line-wrapped literal phrase hook. The sealed material records both events, although, as above, their chronology is documentary rather than externally authenticated here.

## 3. Quotient screen and its connection

Let `k` be the nonzero affine null tangent. On `k^perp`, the radical of the restricted Lorentz metric is exactly `span(k)`. To see positivity directly, choose a unit timelike `u`, write `k=omega(u+s)` with `s` unit spacelike in `u^perp`, and write `X=a u+x`. Orthogonality to `k` gives `x·s=a`, hence

\[
g(X,X)=|x-as|^2.
\]

Equality holds precisely for `X` proportional to `k`. Thus

\[
Q=k^\perp/\operatorname{span}(k)
\]

is intrinsically a positive-definite rank-two metric bundle.

For a section represented by `X in k^perp`, define `D[X]=[nabla_k X]`. If `X` is replaced by `X+f k`, affine geodesicity gives

\[
\nabla_k(X+fk)=\nabla_kX+f'k,
\]

so the quotient class is unchanged. Differentiating `g(X,k)=0` shows `nabla_kX` remains in `k^perp`. Differentiating `g(X,Y)` proves metric compatibility. Therefore the Levi-Civita connection supplies the quotient carry canonically; no observer screen, Sachs basis, or independently supplied transport law is required. The affine hypothesis is load-bearing here: without `nabla_k k=0`, the displayed representative-independence would need reparametrization terms.

## 4. Curvature sign, tide, Jacobi equation, and symplectic transport

With the sealed convention

\[
R(X,Y)Z=\nabla_X\nabla_YZ-\nabla_Y\nabla_XZ-\nabla_{[X,Y]}Z,
\]

the transverse tide is `T[X]=[R(X,k)k]`. It is representative-independent because `R(k,k)=0`, lies in the quotient because its contraction with `k` vanishes, and is self-adjoint by the Riemann tensor pair symmetries.

For a commuting geodesic variation, torsion-freeness and `nabla_k k=0` give

\[
\nabla_k^2J=R(k,J)k=-R(J,k)k,
\]

so the quotient Jacobi equation is exactly

\[
D^2x+Tx=0.
\]

This confirms the sign used by the intake.

For two solutions, with canonical covectors `p=(Dx)^flat` and `r=(Dy)^flat`, differentiate

\[
\Omega((x,p),(y,r))=r(x)-p(y).
\]

Metric compatibility cancels the velocity terms, and self-adjointness of `T` cancels the curvature terms. Hence the Wronskian is conserved. The fundamental map on `Q plus Q*` is consequently symplectic. Standard uniqueness for the regular linear ODE gives existence and invertibility over the entire regular segment, including every conjugate endpoint, together with

\[
M_{20}=M_{21}M_{10},\qquad M_{01}=M_{10}^{-1}.
\]

The block inverse of a typed symplectic map gives

\[
B_{01}=-B_{10}^{*}.
\]

The star is the metric/canonical adjoint between the two endpoint quotient spaces; in parallel orthonormal frames it is transpose. Therefore the two absolute determinant densities agree under reversal. None of these statements needs a field equation or a special spacetime.

## 5. Adversarial crossing-order attack

Fix the source and metric-identify the initial covector with a vector. The Jacobi tensor satisfies

\[
B(\lambda_0)=0,\qquad DB(\lambda_0)=I,
\]

and its column Wronskians give

\[
B^*DB-(DB)^*B=0.
\]

At a conjugate value `lambda_*`, put `V=ker B(lambda_*)`. If a nonzero `v in V` also obeyed `DB v=0`, then the Jacobi field `B(lambda)v` would have zero position and derivative at `lambda_*`; ODE uniqueness would make it identically zero, contradicting its initial derivative `v`. Hence `DB|V` is injective.

For `v in V` and arbitrary `w`, the Wronskian identity yields

\[
q(DBv,Bw)=q(Bv,DBw)=0.
\]

Thus `DB(V)` lies in `(im B)^perp`. Both spaces have dimension `dim ker B`, so this map is an isomorphism. This is exactly the missing kernel-to-cokernel transversality condition, not merely injectivity in the full target.

To expose the determinant order, let `m=dim ker B` and choose domain and target splittings adapted to `ker B`, `im B`, and its orthogonal complement. With `h=lambda-lambda_*`, the matrix has block form

\[
B(\lambda_*+h)=
\begin{pmatrix}
h\Gamma+O(h^2)&hE+O(h^2)\\
hF+O(h^2)&L+O(h)
\end{pmatrix},
\]

where `Gamma:ker B -> (im B)^perp` and `L` on the complementary directions are invertible. A Schur-complement expansion gives

\[
\det B(\lambda_*+h)=h^m\det(\Gamma)\det(L)+O(h^{m+1}).
\]

Therefore the zero order is exactly `m`. A higher-order rank-one zero would require `Gamma=0`; a degenerate rank-zero zero would require singular `DB`; both contradict the preceding uniqueness-plus-Wronskian argument. This proof applies to every smooth self-adjoint quotient tide, so a regular Lorentzian null-Jacobi counterexample cannot occur within the stated assumptions.

As an additional realization check, arbitrary smooth symmetric two-screen profiles can be realized locally, with the convention-adjusted sign, along the central null geodesic of a smooth Brinkmann plane-wave metric. Thus the constant-tide witnesses are genuine Lorentzian possibilities, not merely unrelated matrix ODEs. The separate scratch reconstruction confirmed the regular-crossing normal forms and found no higher-order branch.

## 6. Rank, caustic, coincidence, and negative-tide branches

All two-screen ranks are correctly retained:

- Rank two: the intrinsic absolute directional area is strictly positive. The signed determinant can be positive or negative and remains constant only on a connected interval without a crossing. The full phase map and the type-I chart are regular.
- Rank one: the area determinant is zero, its zero is simple, and the signed coefficient flips across the crossing. The full phase map remains regular, while `B^{-1}`, the type-I generator, and the finite inverse-determinant scalar do not exist there.
- Rank zero: the determinant has an exact double zero and no sign flip. The full phase map again remains regular. This includes but is not limited to coincidence.

The exact witness `T=diag(1,-1)` at affine length `pi` has `det B=sin(L)sinh(L)`, giving a noncoincident rank-one simple crossing. The witness `T=I` at `pi` has `B=0` and `det B=sin^2(L)`, giving a noncoincident rank-zero double crossing. At coincidence,

\[
B=(\lambda-\lambda_0)I+O((\lambda-\lambda_0)^3),
\]

because `B''(lambda_0)=-T B(lambda_0)=0`; it is the rank-zero, order-two identity-chart boundary. For `T=diag(-1,-4)`, both scalar Jacobi solutions are hyperbolic and `det B=sinh(L)sinh(2L)/2>0` for positive nonzero `L`, so the negative-tide nonconjugate branch is present.

A caustic is singular for the projection from initial slope to final position, not for the spacetime metric or the full symplectic transport. The intake maintains this distinction correctly.

## 7. Area, orientation, coordinate, affine, and observer typing

For a fixed-frequency projective null variation at source zero,

\[
p_0=\omega_0q_0\theta_0,\qquad x_1=B_{10}p_0.
\]

Taking the metric Jacobian between the source celestial tangent area and target quotient area gives

\[
\mathscr A_{1\leftarrow0}
=\omega_0^2|\det B_{10}|\sqrt{\det q_1\det q_0},
\]

and analogously in reverse with source frequency `omega_1`. The absolute value is the intrinsic unoriented metric area. A signed determinant requires independently supplied orientations at both endpoints. In two screen dimensions, compatible transported orientations give `det(-B*)=det B` under reversal. Reflecting exactly one endpoint orientation flips the signed coefficient and leaves the absolute area unchanged. A crossing of multiplicity `m` changes the signed coefficient by `(-1)^m`, so rank one flips and rank zero does not.

Under arbitrary passive endpoint coordinates,

\[
x_i'=R_ix_i,\quad p_i'=R_i^{-T}p_i,\quad
B'=R_1BR_0^T,\quad q_i'=R_i^{-T}q_iR_i^{-1}.
\]

The determinant factors cancel exactly in the metric-area formula. Under a positive common affine rescaling `k -> a k`, canonical momentum and endpoint frequencies gain `a`, while `B` gains `a^{-1}` and its two-dimensional determinant gains `a^{-2}`. The directional areas and their ratio are therefore affine invariant.

For any finite future unit timelike observer `u`, every quotient class has a unique representative orthogonal to `u`. The change from observer `u` to `v` is

\[
I_{v\leftarrow u}X=X+\frac{g(X,v)}{\omega_v}k,
\]

which is a quotient-metric isometry. Differentiation of the normalized celestial direction gives

\[
\theta_v=\frac{\omega_u}{\omega_v}I_{v\leftarrow u}\theta_u,
\qquad
d\Omega_v=\left(\frac{\omega_u}{\omega_v}\right)^2d\Omega_u.
\]

Consequently independent endpoint observer replacements with `D_i=omega(v_i)/omega(u_i)` give

\[
\mathscr A'_{1\leftarrow0}=D_0^2\mathscr A_{1\leftarrow0},\qquad
\mathscr A'_{0\leftarrow1}=D_1^2\mathscr A_{0\leftarrow1}.
\]

Only the source factor appears in each direction: changing the target observer only changes the quotient representative by an isometry. The reversal ratio remains the square of the new endpoint frequency ratio. The domain correctly excludes null observers; finite timelike observers can approach that boundary but do not include it.

## 8. Inverse-G345 mean and chartwise stationary sewing

On the rank-two stratum, the intrinsic G345 quantity is

\[
\widehat\Delta_{10}
=\frac{1}{|\det B_{10}|\,\omega_1\omega_0
\sqrt{\det q_1\det q_0}}.
\]

Using reversal immediately gives

\[
\sqrt{\mathscr A_{1\leftarrow0}\mathscr A_{0\leftarrow1}}
=\widehat\Delta_{10}^{-1}.
\]

At rank loss, the two areas vanish while the finite inverse-determinant chart ceases to exist; only a limiting reciprocal can tend to zero. The report does not falsely assign a finite G345 scalar at the caustic.

For three endpoints, full symplectic composition is unconditional on rank. The type-I stationary formula instead requires the relevant `B_10`, `B_21`, and `B_20` blocks to be invertible. Only on such a chart,

\[
H_1=B_{21}^{-1}B_{20}B_{10}^{-1},\qquad
|\det B_{20}|=|\det H_1|\,|\det B_{21}|\,|\det B_{10}|.
\]

Including the intermediate metric/frequency normalization yields the stated directional-area sewing. If any required block is singular, the stationary type-I expression is unavailable; there is no global cancellation or bare multiplicative law. One must use full symplectic composition or a different generating chart. The sealed conclusion is correctly chartwise.

## 9. Scope and evidentiary conclusion

The direct derivation proves the generic result from the supplied smooth Lorentzian metric, its Levi-Civita connection, and the supplied regular affine null geodesic. The prior G343--G347 exact Taub/Kasner derivations are consistent comparison surfaces, not the proof of genericity. The numerical programs provide useful regression and implementation-diversity evidence but do not establish universality; universality comes from the quotient, curvature, Wronskian, ODE-uniqueness, and kernel-to-cokernel arguments above.

No mathematical repair is required. The nonblocking evidence caveats are limited to the absence of an external signature/trust anchor for the checksum chain, repository-independent verification of the documentary chronology, tautological hostile controls, and text-token gates that test wording rather than mathematics.

The result must not be widened. It says nothing about finite beams, geometric optics as a physical approximation, emission or detection, brightness, flux, luminosity, probability, observational distance, preferred observers, routes or populations, history, occupancy, stability, matter or mass, physical scale, `X_max`, or canon. It selects no metric, geodesic, endpoint, observer, or path population.

ACCEPT_G348_GENERIC_NULL_SCREEN_AREA_THEOREM
