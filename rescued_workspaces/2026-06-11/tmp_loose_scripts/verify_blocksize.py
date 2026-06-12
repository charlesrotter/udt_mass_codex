# The block size = number of channels of one parity = (number of distinct |kappa| values) = |kappa_max| = 3.
# With kappa in {+-1,+-2,+-3}: 6 channels, parity splits 3/3. Block size = |kappa_max| = 3.
# The corpus EQUATES block size with (2l+1)=3 for l=1. But:
#   block size = |kappa_max| = 3   (from 6 channels / 2)
#   (2l+1) = 3                     (for l=1, the SELECTED orbital)
# These are equal (=3) but are DIFFERENT quantities that coincide at the Diophantine triple (1/2,1,3).
# Check: is block-size = (2l+1) an identity, or a coincidence at this triple?
# If kappa_max were 2 (channels +-1,+-2): block size=2, but l would still be... selected separately.
for kmax in [1,2,3,4]:
    nchan=2*kmax
    block=nchan//2  # = kmax
    print(f"|kappa_max|={kmax}: channels={nchan}, parity-block size={block} (= |kappa_max|)")
print()
print("So 'block size = N_c = 3' is block size = |kappa_max| = 3.")
print("Calling it (2l+1)=3 requires l=1, true at the triple, but the block size is set by |kappa_max|, not by l.")
