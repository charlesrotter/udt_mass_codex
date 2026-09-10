# NCI1 direct adversarial review and focused repair review

Date: 2026-09-10. Reviewer context: /root/pair_depth_source_review.
This file is written by that reviewer under the parent's explicit narrow authorization to create
only DIRECT_REVIEW.md. It preserves the initial direct verdict and its actual independent
calculations, then records the one focused same-premise repair review.

## 1. Initial direct review: original verdict and scope

Original verdict: VERIFIED-WITH-CAVEATS for the core conditional equivalence. No load-bearing
defect found. Two small example clarifications were required before the whole text could be
called fully precise.

The actual starting and ending hashes of the initial direct review were:

~~~
HEAD a62f3cc52b94b1029092227b5feda7b7ee154486
WORK_ORDER.md
689b21513fd8a3593f4c6891d7b39442e7f730f2d334459fbb35b1bf8ed78f05
INITIAL_CANDIDATE.md
a2769dd02500970475225939f0606ba212bdde6b6a54a3bebdd5023ced1385e1
~~~

The argument supports exactly the declared conclusion:

~~~
P iff there exists f>0 with f U conformal Killing
  iff sigma=0 and alpha=a_flat-H U_flat is exact.
~~~

The reviewer checked the argument, not merely its agreement with a familiar theorem:

- With delta=log(omega_B/omega_A) and f=exp(-Psi), endpoint differences are equivalent to
  conservation of f omega. The signs agree with G220's static and conformal controls.
- Differentiation along affine null geodesics gives the stated symmetric-tensor contraction.
  The candidate explicitly includes every local null direction and arbitrary short subsegments,
  so necessity is justified.
- The nine specified future-null directions force a general symmetric four-dimensional tensor
  to be proportional to the Lorentz metric. No Einstein equation enters.
- In a unit observer frame the conformal-Killing projections give b_0=H, b_i=a_i, zero shear,
  and psi=f H, where b=d log f. This is exactly b=a_flat-H U_flat; vorticity cancels.
- Closedness gives local primitives; global existence requires exactness. The period
  qualification and simply connected sufficient condition are correct. The differential is
  fixed, so connectedness gives uniqueness up to one additive constant.
- The source join preserves G216's comparison-clock/unit-clock distinction and G247's
  path-labelled chain semantics. The property concerns supplied (g,U), not a metric-only law,
  population selector, or new physical necessity.

### Original objections and smallest repairs

1. INITIAL_CANDIDATE.md lines143-147 conclude A_i=c_i A with positive constants but do not
   explicitly assume positive A_i. Smooth nonzero signed factors describe the same squared
   metric; mixed signs defeat that literal formulation. Declare A_i>0 as positive representatives,
   without restricting the metric class, or write abs(A_i)=c_i A.
2. Line134 should call -kappa n_x^2 the normalized slope
   (1/omega) d delta/d lambda, or declare source normalization omega_A=1.
   Equation(D) is correct; the abbreviated prose is ambiguous.

The malformed parentheses at line97 were noted as an optional notation cleanup: the final term
means U_(a (b-a)_{b)}. Its intended expression and the subsequent projections are unambiguous.
This editorial notation point was not required for acceptance.

### Direct obstruction arguments

For the shear example, opposite +/-e_x directions force the same scalar temporal derivative to
equal -kappa, while opposite +/-e_y directions force it to equal zero. Thus no scalar gradient
can match every direction at that event.

For the shear-free lapse example, the independent full-metric reconstruction below establishes
flatness, vanishing shear/expansion, and nonclosed alpha. The obstruction is also visible as
incompatible scalar derivatives: the necessary assignments would give partial_t Psi=0 and
partial_x Psi=-t/(1+t x), whose mixed derivatives disagree on the positive-lapse patch.

## 2. Exact independently executed commands and output

Both commands below ran in /home/udt-admin/udt_mass_codex. They imported SymPy, not the author's
implementation or outputs; they created no files. Each exited 0 with no stderr. Runtime:
Python3.10.12, SymPy1.13.1. These are the actual executed command bodies, not a retrospective
replacement. They supplement the direct argument and do not by themselves prove the global theorem.

### Command1: full four-metric flatness and observer obstructions

~~~bash
python3 - <<'PY'
import sys
import sympy as s
print('Python',sys.version.split()[0], 'SymPy',s.__version__)
t,x,y,z,kappa=s.symbols('t x y z kappa', real=True)
q=(t,x,y,z); dim=4; N=1+t*x
g=s.diag(-N**2,1,1,1); gi=g.inv()
Ga=[[[s.simplify(sum(gi[a,d]*(s.diff(g[d,c],q[b])+s.diff(g[d,b],q[c])-s.diff(g[b,c],q[d])) for d in range(dim))/2) for c in range(dim)] for b in range(dim)] for a in range(dim)]
riemann=[]
for a in range(dim):
 for b in range(dim):
  for c in range(dim):
   for d in range(dim):
    value=s.simplify(s.diff(Ga[a][d][b],q[c])-s.diff(Ga[a][c][b],q[d])+sum(Ga[a][c][e]*Ga[e][d][b]-Ga[a][d][e]*Ga[e][c][b] for e in range(dim)))
    if value!=0: riemann.append((a,b,c,d,value))
print('control4_nonzero_Christoffel',[(a,b,c,Ga[a][b][c]) for a in range(dim) for b in range(dim) for c in range(dim) if Ga[a][b][c]!=0])
print('control4_all_256_Riemann_components_zero',not riemann,riemann)
U=s.Matrix([1/N,0,0,0]); Ul=g*U
DU=s.Matrix(dim,dim,lambda a,b:s.simplify(s.diff(Ul[b],q[a])-sum(Ga[c][a][b]*Ul[c] for c in range(dim))))
acc=s.simplify(DU.T*U); expansion=s.simplify(sum(gi[a,b]*DU[a,b] for a in range(dim) for b in range(dim)))
h=g+Ul*Ul.T; proj=s.eye(dim)+Ul*U.T
sigma=s.simplify(proj*(DU+DU.T)*proj.T/2-expansion*h/3)
alpha=s.simplify(acc-expansion*Ul/3)
dalpha=s.Matrix(dim,dim,lambda a,b:s.simplify(s.diff(alpha[b],q[a])-s.diff(alpha[a],q[b])))
print('control4_U_norm',s.simplify((U.T*g*U)[0]))
print('control4_acceleration_covector',list(acc),'expansion',expansion,'shear_zero',sigma==s.zeros(dim))
print('control4_alpha',list(alpha),'dalpha_01',dalpha[0,1])
eta=s.diag(-1,1,1,1); V=s.Matrix([s.cosh(kappa*x),s.sinh(kappa*x),0,0]); Vl=eta*V
DV=s.Matrix(dim,dim,lambda a,b:s.diff(Vl[b],q[a])); acc2=s.simplify(DV.T*V)
exp2=s.simplify(sum(eta[a,b]*DV[a,b] for a in range(dim) for b in range(dim)))
h2=eta+Vl*Vl.T; pr2=s.eye(dim)+Vl*V.T
sig2=s.simplify(pr2*(DV+DV.T)*pr2.T/2-exp2*h2/3)
print('control3_U_norm',s.simplify((V.T*eta*V)[0]))
print('control3_at_x0_acc',list(acc2.subs(x,0)),'expansion',exp2.subs(x,0),'shear_diagonal',list(sig2.subs(x,0).diagonal()))
nx,ny,nz=s.symbols('nx ny nz', real=True); ray=s.Matrix([1,nx,ny,nz])
print('control3_frequency_derivative_at_x0',s.simplify(-(ray.T*DV.subs(x,0)*ray)[0]))
assert not riemann
assert sigma==s.zeros(dim)
assert s.simplify(dalpha[0,1]-1/N**2)==0
assert sig2.subs(x,0)==s.diag(0,2*kappa/3,-kappa/3,-kappa/3)
assert s.simplify(-(ray.T*DV.subs(x,0)*ray)[0]+kappa*nx**2)==0
print('INDEPENDENT_DIRECT_CONTROLS_PASS')
PY
~~~

Complete stdout:

~~~
Python 3.10.12 SymPy 1.13.1
control4_nonzero_Christoffel [(0, 0, 0, x/(t*x + 1)), (0, 0, 1, t/(t*x + 1)), (0, 1, 0, t/(t*x + 1)), (1, 0, 0, t*(t*x + 1))]
control4_all_256_Riemann_components_zero True []
control4_U_norm -1
control4_acceleration_covector [0, t/(t*x + 1), 0, 0] expansion 0 shear_zero True
control4_alpha [0, t/(t*x + 1), 0, 0] dalpha_01 (t*x + 1)**(-2)
control3_U_norm -1
control3_at_x0_acc [0, 0, 0, 0] expansion kappa shear_diagonal [0, 2*kappa/3, -kappa/3, -kappa/3]
control3_frequency_derivative_at_x0 -kappa*nx**2
INDEPENDENT_DIRECT_CONTROLS_PASS
~~~

### Command2: null-tensor lemma and independent conformal-Killing projections

~~~bash
python3 - <<'PY'
import sympy as s
p=s.symbols('s00 s01 s02 s03 s11 s12 s13 s22 s23 s33')
S=s.Matrix([[p[0],p[1],p[2],p[3]],[p[1],p[4],p[5],p[6]],[p[2],p[5],p[7],p[8]],[p[3],p[6],p[8],p[9]]])
nulls=[]
for i in range(1,4):
 for eps in [-1,1]:
  k=s.Matrix([1,0,0,0]); k[i]=eps; nulls.append(k)
for i in range(1,4):
 for j in range(i+1,4):
  k=s.Matrix([1,0,0,0]); k[i]=k[j]=s.sqrt(2)/2; nulls.append(k)
sol=s.linsolve([(k.T*S*k)[0] for k in nulls],p)
print('nine_future_null_tests_solution_for_S',sol)
H,a1,a2,a3,b0,b1,b2,b3,c=s.symbols('H a1 a2 a3 b0 b1 b2 b3 c')
s11,s22,s12,s13,s23,w12,w13,w23=s.symbols('sig11 sig22 sig12 sig13 sig23 w12 w13 w23')
D=s.Matrix([[0,a1,a2,a3],[0,H+s11,s12+w12,s13+w13],[0,s12-w12,H+s22,s23+w23],[0,s13-w13,s23-w23,H-s11-s22]])
Uflat=s.Matrix([-1,0,0,0]); b=s.Matrix([b0,b1,b2,b3])
T=(D+D.T+b*Uflat.T+Uflat*b.T)/2
res=s.linsolve(list(T-c*s.diag(-1,1,1,1)),(b0,b1,b2,b3,c,s11,s22,s12,s13,s23))
print('aligned_CKV_projection_solution',res)
print('vorticity_coefficients_drop_out',not any(T.has(w) for w in (w12,w13,w23)))
assert sol==s.FiniteSet((-p[9],0,0,0,p[9],0,0,p[9],0,p[9]))
assert res==s.FiniteSet((H,a1,a2,a3,H,0,0,0,0,0))
print('INDEPENDENT_NULL_TENSOR_AND_KINEMATIC_PROJECTIONS_PASS')
PY
~~~

Complete stdout:

~~~
nine_future_null_tests_solution_for_S {(-s33, 0, 0, 0, s33, 0, 0, s33, 0, s33)}
aligned_CKV_projection_solution {(H, a1, a2, a3, H, 0, 0, 0, 0, 0)}
vorticity_coefficients_drop_out True
INDEPENDENT_NULL_TENSOR_AND_KINEMATIC_PROJECTIONS_PASS
~~~

## 3. Independence, exposure and omitted checks

This is the same /root/pair_depth_source_review context that completed the source-first assessment,
not a second reviewer. Before completing the source stage, the reviewer had the question and source
list but no candidate proof or proposed result. Historical source verdicts were read at that stage.
The follow-up exposed the proposed criterion and examples; the reviewer then read the actual entire
frozen candidate and work order. The author check implementation, outputs and verdict were not read
or imported. Exact runtime model identity was not exposed; no different-model claim.

The direct review attempted to open https://arxiv.org/pdf/0802.3642v2 using the web tool; the fetch
failed with a cache error. A subsequent search returned the authors' arXiv abstract
https://arxiv.org/abs/0802.3642, which confirms the classical redshift-potential/conformal-vector/
shear-integrability attribution. Proposition numbering was not independently checked from the PDF.
The substantive review verdict rests on the direct argument and independent calculations above.
No parallax or physical-light conclusion was imported.

Not repeated: whole-premise verifier, source package replays, full source-manifest audit, numerical
sampling, global-topology examples, or exhaustive literature novelty assessment. Static/conformal
controls and the homogeneous corollary were checked analytically. No scientific grade changed;
the known G325 banking blocker remains. Original direct review made no file changes.

## 4. Focused same-premise repair review

Focused verdict: ACCEPT_REPAIR__VERIFIED_WITH_CAVEATS__CONDITIONAL_UNPROMOTED_APPLICATION.
The repaired candidate is INITIAL_CANDIDATE.md plus REPAIR.md. Its initial bytes are unchanged.
No load-bearing objection remains within the stated supplied smooth (g,U) class.

Files directly read and hashed at focused review:

~~~
WORK_ORDER.md
689b21513fd8a3593f4c6891d7b39442e7f730f2d334459fbb35b1bf8ed78f05
INITIAL_CANDIDATE.md
a2769dd02500970475225939f0606ba212bdde6b6a54a3bebdd5023ced1385e1
REPAIR.md
38f0bf9512a426e23e76acba8bca71dcef36b0d1e126ce5f45eabbe269b98dc4
SOURCE_REVIEW.md (first focused-read version; enumeration correction noted below)
19a6bfa0d23876e8094a7329af4209e0e82a5a7af1be7f63f214769358758cf3
~~~

Repair1 correctly chooses positive smooth representatives A_i>0. A smooth nonzero representative
has constant sign on a connected interval; its absolute value is smooth and leaves the squared
metric and logarithmic derivative A_i'/A_i unchanged. The statement A_i=c_i A with c_i>0 is now
precise and imposes no additional physical restriction.

Repair2 correctly names the frequency-normalized slope and identifies the omega=1 special
normalization for the raw slope. This agrees with equation(D), the independent direct calculation,
and common affine rescaling. The optional line97 notation cleanup is not required for acceptance.

No recomputation was needed for these two wording/domain corrections: the original independently
executed calculations above already test the corrected expressions. Those original commands,
outputs and exposure history are preserved rather than relabelled as a fresh review.

REPAIR.md discloses the author's positive-exponential parametrization and omega=1 normalization.
This is new prose exposure in the repair stage only. The reviewer has still not read or imported
the actual author code or outputs and does not independently attest those implementation claims.

## 5. Source-stage record fidelity check

SOURCE_REVIEW.md preserves the original scientific findings, recommendation, no-novelty scope,
source-versus-proof exposure and omissions. The two hash transcriptions flagged by the parent now
match direct sha256sum:

~~~
G235 EXACT_DERIVATION.md
5bcc38c32ddef6fd88e6c8608305f3d3317defdd2263972392184416295c2955
G220 FRESH_ADVERSARIAL_REVIEW.md
8c0cdf0cbdff660f43f06d5bcc153837bd3d258810b99bc9bb9a7e6f0343e259
~~~

The focused reader caught an actual-read enumeration overstatement inherited from the reviewer's
own original source-stage summary: the registry row set was G339,G340,G341,G344,G345,G346,
not every row G339-G346. G342/G343 registry rows were not queried. This was reported to the parent
for correction in SOURCE_REVIEW.md. It is a review-log correction, not a scientific/candidate
repair. The exact derivation read list and substantive findings are unaffected.

Only DIRECT_REVIEW.md was created by this reviewer. Candidate, source science, registry, canon,
manuscript, protected paths and author code/output were not edited.

## 6. Focused documentation closeout

The parent corrected the actual-read enumeration and retained disclosure of its origin.
The reviewer reread SOURCE_REVIEW.md completely after that correction. It faithfully records
the source-stage findings and limits. The earlier source-record hash in section4 is historical;
the final reviewed source-record hash is:

~~~
SOURCE_REVIEW.md
134b2ee0a5d6e818cb5e5ab63008d63ff204a8cd2ea0572cbe188e41d1099b37
~~~

At the parent's additional explicit request, the reviewer read DECISION_BRIEF.md completely
for fidelity to the repaired candidate and this review:

~~~
DECISION_BRIEF.md
dbdf63c67378d0b3d907d2232a71b5e965f915ff1c6cfa23c92b632df7d540f1
~~~

Verdict: FIDELITY_ACCEPTED_WITH_RECORDED_SCOPE. Its scalar/CK/exactness equivalence is read,
as in its surrounding text and the controlling candidate, as an existence statement for Psi.
Its local closedness statement retains the preceding zero-shear condition. It preserves supplied
observer/metric dependence, the unpromoted mathematical-application status, the absence of a
physical adoption, the distinction between independent review and author regression, the actual
one-cycle repair, and the full365 banking boundary. No new scientific claim requires another
review cycle.

The brief's author24 check count, operational statements and preservation assertions are not
independently replayed by this fidelity review. The reviewer did not read author code/output,
CAMPAIGN_LOG.md, or the INDEX/roadmap edits. Their review or verification is not claimed here.
The independent argument, actual commands and outputs in sections1-2 remain the review evidence.

Final candidate verdict remains ACCEPT_REPAIR__VERIFIED_WITH_CAVEATS__
CONDITIONAL_UNPROMOTED_APPLICATION. No load-bearing objection remains; the optional line97
parenthesis cleanup is not an acceptance condition. No scientific promotion or new work is
authorized by this review.
