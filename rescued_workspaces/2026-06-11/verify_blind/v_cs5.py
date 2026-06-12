from v_engine import cstar
cs5 = cstar(1.0, 5, 0.10, 0.133, fstop=0.02, Tmax=160.0)
print(f"c*_5(gamma=1, abs 0.02) = {cs5:.6f}")
with open('cs5.out','w') as f: f.write(f"{cs5:.6f}\n")
