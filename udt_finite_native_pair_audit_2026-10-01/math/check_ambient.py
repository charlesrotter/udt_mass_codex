#!/usr/bin/env python3
"""Exact finite ambient checks, independent of the FNA1 parent implementation.

These are exact-arithmetic controls for the analytic argument, not a proof by
sampling or a physical admission test. Uses only Python standard-library Fraction.
"""
from fractions import Fraction as Q
import json

count = 0


def check(ok, label):
    global count
    count += 1
    if not ok:
        raise AssertionError(label)


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def scale(c, a):
    return tuple(c * x for x in a)


def sub(a, b):
    return add(a, scale(-1, b))


rows = []
for eps in (1, -1):
    metric = (-1, eps, 1, 1, 1)

    def dot(a, b):
        return sum(h * x * y for h, x, y in zip(metric, a, b))

    for t in (Q(1, 10), Q(1, 3), Q(1, 2), Q(2, 3), Q(9, 10)):
        # Positive curvature: (c,v)=(cos alpha,sin alpha).
        # Negative curvature: (c,v)=(cosh alpha,sinh alpha).
        c = (1 - eps * t*t) / (1 + eps * t*t)
        v = 2*t / (1 + eps * t*t)
        check(c*c + eps*v*v == 1 and c > 0 and v > 0, 'prepared circle/hyperbola')
        for k in (Q(1, 2), Q(1), Q(3, 2)):
            X = (Q(0), 1/k, Q(0), Q(0), Q(0))
            U = (Q(1), Q(0), Q(0), Q(0), Q(0))
            n = (Q(0), Q(0), Q(1), Q(0), Q(0))
            B0 = add(scale(c, X), scale(v/k, n))
            Y = add(scale(1/c, B0), scale(v/(k*c), U))
            UB = add(scale(eps*k*v/c, B0), scale(1/c, U))
            D = sub(Y, X)
            check(dot(X, X) == eps/k**2, 'source quadric')
            check(dot(B0, B0) == eps/k**2, 'prepared quadric')
            check(dot(Y, Y) == eps/k**2, 'receiver quadric')
            check(dot(UB, UB) == -1 and dot(Y, UB) == 0, 'receiver proper tangent')
            check(dot(D, D) == 0 and dot(X, D) == dot(Y, D) == 0, 'actual null chord')
            ell = -dot(U, D)
            K = scale(1/ell, D)
            omega_o = -dot(UB, K)
            p = 1/omega_o
            check(ell > 0 and omega_o > 0 and p == 1/c, 'independent clock contraction')
            check((p > 1) if eps == 1 else (0 < p < 1), 'sign discriminator')

            # Derivative of the actual family at fixed prepared worldlines.
            Dprime = sub(scale(p, UB), U)
            Aprimeprime = scale(eps*k*k, X)
            ellprime = -dot(Aprimeprime, D) - dot(U, Dprime)
            Kprime = sub(scale(1/ell, Dprime), scale(ellprime/ell, K))
            check(dot(K, Kprime) == 0, 'null family derivative')
            check(ellprime == p*p-1, 'affine span derivative')
            check(dot(Kprime, Kprime) == eps*k*k, 'null direction derivative norm')
            for a in (Q(1, 3), Q(1), Q(7, 2)):
                Js, Jr = scale(p, UB), scale(a, K)
                h00, h01, h11 = dot(Js, Js), dot(Js, Jr), dot(Jr, Jr)
                determinant = h00*h11-h01*h01
                beta = h01/h00
                L2 = h11-h01*h01/h00
                m = a
                check(h00 == -p*p and h01 == -a and h11 == 0, 'full germ')
                check(h00 < 0 and determinant == -a*a, 'rank and regularity')
                check(L2 == a*a/(p*p) and beta/m == 1/(p*p), 'shift/density normalization')
                check(determinant/(m*m) == -1, 'completed determinant')
                orthogonal_ruler = sub(Jr, scale(beta, Js))
                check(dot(orthogonal_ruler, Js) == 0, 'ruler orthogonality')
                check(dot(orthogonal_ruler, orthogonal_ruler) == L2, 'positive ruler norm')

            # Actual nearby immersion, no manufactured metric matrix.
            sigma = Q(1, 1000) / (k * (p + 1))
            F = add(Y, scale(sigma, K))
            Fs = add(scale(p, UB), scale(sigma, Kprime))
            check(dot(F, F) == eps/k**2, 'nearby ribbon on quadric')
            check(dot(F, Fs) == dot(F, K) == 0, 'nearby ribbon tangents')
            h00 = dot(Fs, Fs)
            check(h00 == -p*p + 2*eps*k*v*sigma/c + eps*k*k*sigma*sigma,
                  'nearby original-equation pullback')
            check(h00 < 0 and dot(Fs, K) == -1, 'nearby regularity')

            def transport(V):
                return sub(V, scale(eps*k*k*dot(V, D), add(X, scale(Q(1, 2), D))))

            screen1 = (Q(0), Q(0), Q(0), Q(1), Q(0))
            screen2 = (Q(0), Q(0), Q(0), Q(0), Q(1))
            ne = sub(K, U)
            no = sub(scale(1/omega_o, K), UB)
            source_frame = (U, ne, screen1, screen2)
            target_frame = (UB, no, screen1, screen2)
            eta = (-1, 1, 1, 1)
            for frame in (source_frame, target_frame):
                for i in range(4):
                    for j in range(4):
                        check(dot(frame[i], frame[j]) == (eta[i] if i == j else 0),
                              'proper endpoint tetrad')
            lam = [[eta[i]*dot(target_frame[i], transport(source_frame[j]))
                    for j in range(4)] for i in range(4)]
            gamma, S = (p+1/p)/2, (1/p-p)/2
            expected = [[gamma,S,0,0],[S,gamma,0,0],[0,0,1,0],[0,0,0,1]]
            check(lam == expected, 'full transported frame, including screen')
            for i in range(4):
                for j in range(4):
                    check(sum(eta[a]*lam[a][i]*lam[a][j] for a in range(4)) ==
                          (eta[i] if i == j else 0), 'Lorentz form')
            check(lam[0][0]+lam[0][1] == omega_o, 'actual null vector frequency')
            check(S/gamma == (1-p*p)/(1+p*p), 'projective signed component')
            check(gamma-S == p, 'direction-retaining clock readout')
            check(transport(K) == K, 'same actual null tangent transported')
            # Check the transport ODE at an interior point with full vectors.
            z = Q(2, 5)
            point = add(X, scale(z, D))
            for V in source_frame:
                Vz = sub(V, scale(eps*k*k*dot(V, D), add(scale(z, X), scale(z*z/2, D))))
                derivative = scale(-eps*k*k*dot(V, D), point)
                check(dot(Vz, point) == 0, 'transport tangent everywhere')
                check(dot(Vz, D) == dot(V, D), 'transport conserved contraction')
                check(derivative == scale(-eps*k*k*dot(Vz, D), point), 'ambient transport ODE')
            # A-centered primary chart domain is a separate condition.
            radius = v/(k*c)
            f = 1-eps*k*k*radius*radius
            if eps == 1:
                check((f > 0) == (v < c), 'primary chart horizon discriminator')
            else:
                check(f > 0, 'opposite curvature static chart')
            rows.append({'curvature_sign':eps,'k':str(k),'circle_parameter':str(t),
                         'p':str(p),'source_affine_span':str(ell),
                         'Gamma_transport':str(gamma),'signed_projective':str(S/gamma),
                         'A_static_first_reception_regular':f>0})

# Flat actual geometry: clocks (s,0) and (b,L), b=s+L, future K=(1,1).
L = Q(7, 3)
check(L > 0, 'flat finite initial separation')
flat_h = ((Q(-1),Q(-1)),(Q(-1),Q(0)))
check(flat_h[0][0]*flat_h[1][1]-flat_h[0][1]**2 == -1, 'flat full germ')
check((1-1)/(1+1) == 0, 'flat chi vanishes while flight remains finite')
print(json.dumps({'status':'PASS','kind':'exact_fraction_controls_not_sampling_proof',
                  'assertions':count,'spaceform_cases':len(rows),'flat_cases':1,
                  'rows':rows},indent=2))
