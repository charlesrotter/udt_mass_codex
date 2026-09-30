#!/usr/bin/env python3
"""Independent exact NE1 replay from central R12's printed Bessel formula."""
import json
from pathlib import Path
import numpy as np
from scipy.special import jv, yv
from independent_numerics import file_hash


def main():
    package = Path(__file__).resolve().parents[2]
    result = {"source":"UDT_DEVELOPMENT.md R12; NE1 formula at parent startup HEAD",
              "source_sha256":file_hash(__file__), "runs":[]}
    for name in ("pilot_n32","pilot_n64","survey_n64","survey_n128",
                 "survey_n128_halfdt","survey_n256","challenge_n128","challenge_n256"):
        run = package/"runs"/name
        spec = json.loads((run/"metadata.json").read_text())["spec"]
        data = np.load(run/"fields.npz",allow_pickle=False)
        t,x,state = data["times"],data["x"],data["state"]
        k=.75
        a,b = -3*np.pi/4*yv(0,k),3*np.pi/4*jv(0,k)
        f=a*jv(0,k*t)+b*yv(0,k*t)
        ft=-k*(a*jv(1,k*t)+b*yv(1,k*t))
        ell=.5*t*t*(ft*ft+k*k*f*f)+.5*t*f*ft-9/8
        for i,case in enumerate(spec["cases"]):
            if not case["id"].startswith("ne1_e"):
                continue
            e=float(case["id"][5:])/100
            expected = np.zeros_like(state[:,i])
            expected[:,0]=e*f[:,None]*np.cos(k*x)
            expected[:,1]=e*ft[:,None]*np.cos(k*x)
            expected[:,4]=4*np.log(k)+e*e*(ell[:,None]+.5*(t*f*ft)[:,None]*np.cos(2*k*x))
            result["runs"].append({"run":name,"case":case["id"],
                "input_sha256":file_hash(run/"fields.npz"),
                "max_abs_error_by_component":np.max(abs(expected-state[:,i]),axis=(0,2)).tolist(),
                "max_abs_error":float(abs(expected-state[:,i]).max())})
    output=Path(__file__).with_name("NE1_EXACT.json")
    output.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    main()
