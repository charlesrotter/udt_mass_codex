"""Finite complex-covariance counterexample to the initial CO1 convention."""
import json
import platform

# Entries and every arithmetic intermediate below are exactly representable
# dyadic complex numbers. This is not a floating approximation to event data.
row = [-1j, 0j, 1+0j]  # F_T=I2, F_J=(i,0), residual row times d
C = [[1+0j,0j,0.5j], [0j,1+0j,0j], [-0.5j,0j,1+0j]]
proper = sum(row[i]*C[i][j]*row[j].conjugate() for i in range(3) for j in range(3))
wrong = sum(row[i].conjugate()*C[i][j]*row[j] for i in range(3) for j in range(3))
assert proper == 3 and wrong == 1 and proper != wrong
# C is Hermitian positive definite: the nontrivial block has eigenvalues1/2,3/2.
assert all(C[i][j] == C[j][i].conjugate() for i in range(3) for j in range(3))
assert C[0][0]*C[2][2]-C[0][2]*C[2][0] == 0.75
print(json.dumps({"python":platform.python_version(),
 "candidate_convention":"w=(-F_J F_T^-1,1), with row r=w d",
 "correct_row_covariance_w_C_wdagger":proper.real,
 "incorrect_column_covariance_using_unconjugated_entries":wrong.real,
 "positive_definite_covariance":True,
 "all_arithmetic_exactly_representable_dyadic_complex":True,
 "repair":"Declare row b=(-F_J F_T^-1,1), r=b d, Var(r)=b C b^dagger; or set column w=b^dagger."},indent=2))
