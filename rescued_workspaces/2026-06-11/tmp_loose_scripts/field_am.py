import numpy as np
# Total angular momentum operator for charge-monopole:
# J = r x (p - eA) - q rhat,  with q = eg/4pi.  The extra -q*rhat is the field AM
# stored in E x B. J^2 eigenvalues = l(l+1), l=|q|,|q|+1,...  This is textbook
# (Wu-Yang / Saha / Jackson). The HALF-INTEGER J for q=1/2 is the famous
# "charge-monopole composite has half-integer angular momentum" (Saha 1936).
#
# KEY DISTINCTION for the statistics claim:
# Half-integer J  =/=>  Fermi statistics, by itself.
# Spin-statistics in 3+1D is a theorem for LOCAL relativistic QFT; a composite's
# statistics under EXCHANGE of two identical composites is a separate computation.
#
# Goldhaber 1976 / Hasenfratz-'t Hooft 1976 / Jackiw-Rebbi 1976: the dyon/monopole
# bound state becomes a FERMION only with extra structure. Let me tabulate the
# actual requirements.

print("""
SPIN-FROM-ISOSPIN REQUIREMENTS (literature):

Hasenfratz-'t Hooft 1976 & Jackiw-Rebbi 1976:
  - NON-ABELIAN 't Hooft-Polyakov monopole (SU(2) gauge)
  - matter in ISOSPIN-1/2 representation (isospinor)
  => bound state acquires half-integer ANGULAR MOMENTUM from isospin. (scalar isospinor!)

Goldhaber 1976 (+ Goldhaber-Wilczek): the STATISTICS upgrade.
  - To conclude the composite is a genuine FERMION (Fermi statistics under exchange)
    you need MORE than half-integer J: you need a spin-statistics argument for the
    composite, e.g. the Witten/Goldhaber/Wilczek analysis, dyon exchange,
    or the global SU(2) -> the well-definedness of the rep.
  - For an ABELIAN monopole + single charged field, two such composites and their
    exchange: the half-integer J does NOT automatically give Fermi statistics.
""")

# Numeric sanity: field AM magnitude eg/4pi = q. For q=1/2 the stored field AM is 1/2.
q=0.5
print(f"Stored EM field angular momentum |E x B integral| = q = {q}  (Saha/Thomson)")
print("This SHIFTS J to half-integer. It is real and well-established.")
print("It does NOT by itself make the SCALAR field a spin-1/2 Dirac FERMION.")
