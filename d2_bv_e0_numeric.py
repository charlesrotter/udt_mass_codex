"""d2_bv_e0_numeric.py -- verifier's OWN recomputation of D2a's Sec.3/4 numbers
from the blind-verified E0 JSON (independent trapezoid integration; no reuse of
the deliverer's script). DO NOT COMMIT."""
import json
import numpy as np

d = json.load(open('microphysics_E0_ambient_tables.json'))['brackets']

print('%-12s %10s %10s %12s %10s %10s %10s | %9s %9s %9s | %8s %8s %8s | %9s %9s' % (
    'bracket', '|K|st1', '|K|max', 'x@max', 'ratio', 'Q/q@.5', 'relerrQ',
    'x@50%', 'x@99%', 'minrhop', 'L_rad', 'chi_c', 'chi_s', 'sgnchg', 'Qq05'))
for name, e in d.items():
    Z = e['Z']
    pr = e['profiles']
    r = np.array(pr['r']); phi = np.array(pr['phi']); phip = np.array(pr['phip'])
    rho = np.array(pr['rho']); rhop = np.array(pr['rhop'])
    rs = e['r_s']
    x = r / rs
    # flux column and my own source integration
    flux = Z * rho**2 * phip                      # = pi_phi_qflux
    src = 4.0 * np.exp(-2.0 * phi) * rhop**2      # the P source
    Q = np.concatenate([[0.0], np.cumsum(0.5 * (src[1:] + src[:-1]) * np.diff(r))])
    q = flux[-1]
    # rel err of reconstruction vs extracted flux column (where flux is non-tiny)
    mask = flux > 1e-6 * q
    relerr = np.max(np.abs(Q[mask] - flux[mask]) / flux[mask])
    Qq = Q / Q[-1]
    x50 = np.interp(0.50, Qq, x)
    x99 = np.interp(0.99, Qq, x)
    i05 = np.searchsorted(x, 0.5)
    Qq05 = np.interp(0.5, x, Qq)
    # |K| = 2 e^{-2phi} (rho'/rho)^2
    Kabs = 2.0 * np.exp(-2.0 * phi) * (rhop / rho)**2
    # station 1 of 6: r = rs/6
    r_st1 = rs / 6.0
    K_st1 = np.interp(r_st1, r, Kabs)
    imax = np.argmax(Kabs)
    # interior min |rho'| and sign changes (open interior: exclude folds)
    inner = (r > 0) & (r < rs)
    minrhop = np.min(np.abs(rhop[inner]))
    sgn = np.sign(rhop[inner])
    sgnchg = int(np.sum(sgn[1:] * sgn[:-1] < 0))
    # chi
    Lrad = np.trapz(np.exp(phi), r)
    chi_c = Lrad / rho[0]
    chi_s = Lrad / rho[-1]
    print('%-12s %10.2e %10.3f %12.4f %10.1e %10.1e %10.1e | %9.4f %9.4f %9.1e | %8.4f %8.4f %8.4f | %9d %9.1e' % (
        name, K_st1, Kabs[imax], x[imax], Kabs[imax] / K_st1, Qq05, relerr,
        x50, x99, minrhop, Lrad, chi_c, chi_s, sgnchg, Qq05))
    # cross-check q against banked
    assert abs(q - e['q']) / e['q'] < 1e-6, (q, e['q'])
print('\nD2a doc claims: |K|st1 5.3e-6/5.8e-7/3.4e-6/3.7e-7; max 0.708@.9939/0.183@.9981/'
      '0.473@.9942/0.096@.9979; ratio 1.3e5/3.2e5/1.4e5/2.6e5; Q/q@0.5 7.5e-4/7.4e-4/6.9e-4/8.2e-4;'
      ' x50 .9935/.9968/.9939/.9964; x99 .9987/.9996/.9989/.9995; Lrad 3.5637/2.6164/4.4839/3.4337')
