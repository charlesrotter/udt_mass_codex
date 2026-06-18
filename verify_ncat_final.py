# Finer-grid confirmation of corrected-L4 deep-cell HELD ratio + summary
import os; os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK","0")
import math, torch
torch.set_default_dtype(torch.float64); dev='cuda' if torch.cuda.is_available() else 'cpu'; PI=math.pi
exec(open('verify_ncat_recompute.py').read().split('if __name__')[0])
print("CORRECTED-L4 HELD deep-cell ratios (finer grids):")
for Nr,Nth in [(120,180),(160,260)]:
    C=Cell(Nr=Nr,Nth=Nth,p=0.4);E1=minimize_held(C,1,'correct')[0]
    r2=minimize_held(C,2,'correct')[0]/E1; r3=minimize_held(C,3,'correct')[0]/E1
    print(f"  Nr={Nr} Nth={Nth}: E2/E1={r2:.3f} E3/E1={r3:.3f}  -> E_k > k*E_1 ? {r2>2 and r3>3}")
