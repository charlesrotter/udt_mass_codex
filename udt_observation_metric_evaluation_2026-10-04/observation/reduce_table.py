"""Exploratory published marginal constraints; no cosmology or metric fit."""
from pathlib import Path
import csv, json, math, hashlib

B=Path(__file__).resolve().parent
# OBSERVED calibration in the optical-velocity convention, not physical speed inference.
C_E_KM_S=299792.458


def main():
    src=B/'MCP_TABLE1_INPUT.tsv'
    inputs=list(csv.DictReader(src.open(),delimiter='\t'))
    assert len(inputs)==6 and len({r['galaxy'] for r in inputs})==6
    rows=[]
    for raw in inputs:
        name=raw['galaxy'];r={k:float(v) for k,v in raw.items() if k!='galaxy'}
        dlo=r['D_Mpc']-r['D_minus_Mpc'];dhi=r['D_Mpc']+r['D_plus_Mpc']
        v=r['v_opt_CMB_km_s'];vlo=v-r['v_reported_minus_km_s'];vhi=v+r['v_reported_plus_km_s']
        assert 0<dlo<r['D_Mpc']<dhi and -C_E_KM_S<vlo<v<vhi
        zlo,z,zhi=[w/C_E_KM_S for w in [vlo,v,vhi]]
        elllo,ell,ellhi=[math.log1p(w) for w in [zlo,z,zhi]]
        assert elllo<ell<ellhi
        for zv,vv in zip([zlo,z,zhi],[vlo,v,vhi]):
            assert abs(zv*C_E_KM_S-vv)<1e-10
        rows.append(dict(galaxy=name,D_Mpc=r['D_Mpc'],D_lower_Mpc=dlo,D_upper_Mpc=dhi,
                         z_opt_CMB=z,z_lower=zlo,z_upper=zhi,Z_proxy=1+z,
                         ell_proxy=ell,ell_lower=elllo,ell_upper=ellhi,
                         interval_note='NGC4258 distance combines statistical/systematic errors in quadrature' if name=='NGC 4258' else 'source-reported marginal16th/84th posterior percentiles'))
    out=B/'MCP_CONSTRAINTS.tsv'
    with out.open('x',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
    record={'status':'PASS_EXPLORATORY_SOURCE_CONDITIONAL_CONVERSION','rows':6,
            'input_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),
            'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'c_E_km_s':C_E_KM_S,'z_median_range':[min(r['z_opt_CMB'] for r in rows),max(r['z_opt_CMB'] for r in rows)],
            'distance_median_range_Mpc':[min(r['D_Mpc'] for r in rows),max(r['D_Mpc'] for r in rows)],
            'distance_not_PS W_L':'D_A from conditional disk fitting; no conversion to initial proper L',
            'limits':'Published exposed marginal constraints only. No joint likelihood/covariance inference, positional attribution, native candidate fit, H0/peculiar-flow subtraction, metric evolution or global-asymptote constraint.'}
    with (B/'DIAGNOSTIC_RESULT.json').open('x') as f:json.dump(record,f,indent=2);f.write('\n')
    print(json.dumps(record,indent=2))


if __name__=='__main__':main()
