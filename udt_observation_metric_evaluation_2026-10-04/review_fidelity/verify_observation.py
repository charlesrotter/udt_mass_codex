"""Source-table transcription plus Decimal60 check; imports no parent code."""
from decimal import Decimal, localcontext
from pathlib import Path
import csv,hashlib,json,sys,platform
B=Path(__file__).resolve().parent
O=B.parent/'observation'
# Independently transcribed after directly viewing M1 PDF page4 render.
SOURCE=[
 ('UGC 3789','51.5','4.0','4.5','3319.9','0.8'),
 ('NGC 6264','132.1','17','21','10192.6','0.8'),
 ('NGC 6323','109.4','23','34','7801.5','1.5'),
 ('NGC 5765b','112.2','5.1','5.4','8525.7','0.7'),
 ('CGCG 074-064','87.6','7.2','7.9','7172.2','1.9'),
 ('NGC 4258','7.58','0.11','0.11','679.3','0.4'),
]
D=Decimal
with localcontext() as ctx:
 ctx.prec=60
 inputs=list(csv.DictReader((O/'MCP_TABLE1_INPUT.tsv').open(),delimiter='\t'))
 actual=list(csv.DictReader((O/'MCP_CONSTRAINTS.tsv').open(),delimiter='\t'))
 assert len(inputs)==len(actual)==len(SOURCE)==6
 assert [r['galaxy'] for r in inputs]==[r['galaxy'] for r in actual]==[r[0] for r in SOURCE]
 expected=[]; errors={}; limits={}
 for src,i,r in zip(SOURCE,inputs,actual):
  name,ds,dl,du,vs,ve=src
  for key,value in zip(['D_Mpc','D_minus_Mpc','D_plus_Mpc','v_opt_CMB_km_s','v_reported_minus_km_s','v_reported_plus_km_s'],[ds,dl,du,vs,ve,ve]):
   assert D(i[key])==D(value),(name,key)
  vel=D(vs); err=D(ve); c=D('299792.458')
  z=vel/c; zl=(vel-err)/c; zu=(vel+err)/c
  e={'D_Mpc':D(ds),'D_lower_Mpc':D(ds)-D(dl),'D_upper_Mpc':D(ds)+D(du),
     'z_opt_CMB':z,'z_lower':zl,'z_upper':zu,'Z_proxy':1+z,
     'ell_proxy':(1+z).ln(),'ell_lower':(1+zl).ln(),'ell_upper':(1+zu).ln()}
  for k,v in e.items():
   # Float64 output representation allowance, many orders below quoted data errors.
   tol=D('3e-15')*max(abs(v),D('1'))
   error=abs(D(r[k])-v)
   assert error<=tol,(name,k,str(error),str(tol))
   errors[k]=max(errors.get(k,D('0')),error);limits[k]=max(limits.get(k,D('0')),tol)
  assert e['D_lower_Mpc']>0 and 0<1+zl<1+z<1+zu
  assert e['ell_lower']<e['ell_proxy']<e['ell_upper']
  expected.append({'galaxy':name,**{k:str(v) for k,v in e.items()}})
 result={'status':'PASS_SIX_SOURCE_ROWS_AND_DECIMAL60_CONVERSIONS','rows':6,'numeric_columns_per_row':10,
   'max_abs_error_by_column':{k:str(v) for k,v in errors.items()},'max_tolerance_by_column':{k:str(v) for k,v in limits.items()},
   'method':'Decimal60 division/logarithm on independently visually transcribed source values; parent float/math implementation not imported',
   'source_interval':'M1 Table1 posterior16th/84th marginals; NGC4258 distance has statistical/systematic quadrature; not joint confidence',
   'source_sha256':hashlib.sha256((O/'primary/M1_Pesce_2001.09213v2.pdf').read_bytes()).hexdigest(),
   'parent_input_sha256':hashlib.sha256((O/'MCP_TABLE1_INPUT.tsv').read_bytes()).hexdigest(),
   'parent_output_sha256':hashlib.sha256((O/'MCP_CONSTRAINTS.tsv').read_bytes()).hexdigest(),
   'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'python':sys.version,'platform':platform.platform(),
   'limitations':'Same conventional transformation formula; independent numeric library/precision and source transcription. No original disk-data posterior recovery, joint test, empirical fit or UDT confirmation.'}
 (B/'INDEPENDENT_CONSTRAINTS.json').write_text(json.dumps(expected,indent=2)+'\n')
 (B/'OBSERVATION_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
