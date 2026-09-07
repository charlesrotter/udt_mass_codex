"""Source-first reconstruction of FW1's fixed finite functional.

Full complex FFT translations, explicit Welch segments and determinant-derived
null row. No author FW2 imports and no observed samples at module definition.
"""
import numpy as np

FS = 4096
N = 98*FS
M = 90*FS
CROP = 4*FS
WFREQ = np.arange(4*FS//2+1)/4
FREQ = np.fft.fftfreq(N, 1/FS)
CORE_FREQ = np.arange(M//2+1)/90
KEEP = np.flatnonzero((CORE_FREQ >= 30) & (CORE_FREQ <= 500))
HANN = .5-.5*np.cos(2*np.pi*np.arange(M)/M)
WELCH_HANN = .5-.5*np.cos(2*np.pi*np.arange(4*FS)/(4*FS))
TAPER_ENERGY = np.dot(HANN, HANN)
WELCH_ENERGY = np.dot(WELCH_HANN, WELCH_HANN)

def nullrow(F):
    det = F[0, 0]*F[1, 1]-F[0, 1]*F[1, 0]
    return np.array([-(F[2, 0]*F[1, 1]-F[2, 1]*F[1, 0])/det,
                     -(F[0, 0]*F[2, 1]-F[0, 1]*F[2, 0])/det, 1.])

def shift(x, delay):
    coeff = np.fft.fft(x)
    coeff[[0, N//2]] = 0
    coeff *= np.exp(2j*np.pi*FREQ*delay)
    answer = np.fft.ifft(coeff)
    assert np.linalg.norm(answer.imag) <= 1e-12*max(np.linalg.norm(answer.real), 1e-100)
    return answer.real

def residual(channels, delays, b):
    result = np.zeros(M)
    for x, tau, coefficient in zip(channels, delays, b):
        result += coefficient*shift(x, tau)[CROP:-CROP]
    return result

def welch_manual(x):
    estimates = np.zeros(4*FS//2+1)
    count = 0
    for start in range(0, M-4*FS+1, 2*FS):
        segment = x[start:start+4*FS]
        z = np.fft.fft((segment-segment.mean())*WELCH_HANN)[:4*FS//2+1]
        power = (z.real*z.real+z.imag*z.imag)/(FS*WELCH_ENERGY)
        power[1:-1] *= 2
        estimates += power
        count += 1
    assert count == 44
    return estimates/count

def core_transform(x):
    return np.fft.fft(x*HANN)[KEEP]

def weighted_Q(z, interpolated_psd):
    return float(np.mean(2*(z.real*z.real+z.imag*z.imag)/(FS*TAPER_ENERGY*interpolated_psd)))

def waveform(family, phase):
    limits = ((30, 500), (30, 100), (100, 500))[family]
    bins = np.arange(limits[0]*98, limits[1]*98+1)
    rng = np.random.Generator(np.random.PCG64(352170817+1000*family+phase))
    z = rng.standard_normal(len(bins))+1j*rng.standard_normal(len(bins))
    coefficients = np.zeros(N, dtype=complex)
    coefficients[bins] = z
    coefficients[-bins] = z.conj()
    padded = np.fft.ifft(coefficients).real
    norm = np.sqrt(np.dot(padded[CROP:-CROP], padded[CROP:-CROP])/FS)
    assert norm > 0
    return padded/norm

def direct_bins(x, bins):
    # Independent dense summation anchors for final-window DFT.
    indices = np.arange(M)
    return np.array([np.sum(HANN*x*np.exp(-2j*np.pi*k*indices/M)) for k in bins])

