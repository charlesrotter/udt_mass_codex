# Numerical contract — preregistered before integration

Date: 2026-08-11

Parent preregistration commit: `ab9c5eec`

## Production method

- CPU `scipy.integrate.solve_ivp`, method `DOP853`;
- relative tolerance `1e-10`, absolute tolerance `1e-12`, maximum step `0.01`;
- metric derivatives by complex-step differentiation with step `1e-30`;
- geodesic endpoint derivative (`dexp`) by centered initial-velocity perturbations of size `1e-6`;
- path transport integrated segment by segment on the exact declared coordinate path.

## Independent method

- no production import;
- central finite-difference metric derivatives with step `2e-5`;
- fixed-step classical RK4 with `1,600` steps per unit affine/path parameter;
- centered endpoint derivative with velocity perturbation `2e-6`.

## Frozen sample universe

- R17: `lambda in {-1,0,1}`, nonzero twist `a=0.4`, perturbation
  `epsilon in {-0.12,0,+0.12}`;
- local complete time-live factorized coframe: `epsilon in {-0.15,-0.075,0,+0.075,+0.15}`;
- two initial causal classes per geometry: one unit timelike and one unit spacelike tangent built
  from the complete orthonormal frame;
- R17 paths: one Hopf-fiber loop and one small coordinate rectangle;
- local complete-coframe paths: two independent coordinate rectangles;
- no sample is discarded after inspection.

## Certification and classification thresholds

- endpoint-atlas direct/composite defect: `<=5e-10`;
- geodesic norm drift: `<=5e-8`;
- parallel-transport metric defect: `<=5e-8`;
- production/independent final-coordinate difference: `<=2e-4` in Euclidean chart norm;
- production/independent holonomy-matrix difference: `<=3e-4`;
- `dexp` is classified `NEAR_CONJUGATE_OR_NUMERICALLY_UNRESOLVED` when its smallest singular value
  at the registered affine endpoint is `<1e-5`; it is not discarded;
- a loop return is classified nonidentity when `||P-I||_F>1e-5`; identity is not preferred;
- Lorentzian/pair regularity is classified by inertia plus `h00<0` and `det(h)<0`, with a
  degeneracy warning when the smallest absolute eigenvalue or determinant magnitude is `<1e-8`.

Failure of a numerical threshold yields `NUMERIC_UNRESOLVED`, never a geometric or physical
negative. Passing these thresholds certifies only the declared numerical construction.
