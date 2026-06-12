# Key test: does U_dilaton(b) at LARGE b flatten to 3x the single-lump self-energy?
# If interaction vanishes at large b, U(b->inf) -> 3*U_self(single lump). 
# The reported drop 0.234->0.110 is HUGE (>50%). For a screened Yukawa interaction (mu~1, range~1)
# between lumps of radius ~7 at separation b<=4, the lumps still massively overlap (b<<rstar=6.99).
# So the "interaction" is dominated by OVERLAP reduction of frozen rigid lumps, NOT a field force.
# Let's compute 3x single-lump self energy and compare to the b-curve asymptote.
import numpy as np
print("Single lump radius (cavity rstar)=6.9875; separations b<=4 << 2*rstar=13.975")
print("=> lumps remain HEAVILY overlapping at all tested b. b=4 still deep overlap.")
print("U_S(0)=0.2340 is the FULLY-COINCIDENT 3-lump stack (3 lumps at same center).")
print("At b=0 all three sit on top of each other -> source amplitude 3x -> energy ~ 9x one lump (quadratic).")
print("As they separate, overlap integral S_a*D_b cross-terms drop. This is TRIVIAL overlap geometry.")
