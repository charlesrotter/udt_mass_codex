#!/usr/bin/env python3
"""Exact anchors for the reviewed rank qualification, not an acquisition theorem."""
import json,sympy as s
x=s.symbols('xi_A',real=True);k1,k2=s.symbols('k1 k2',positive=True)
phi1=s.pi/2-k1*x;phi2=s.pi/2-k2*x
coeff=s.Matrix([[s.simplify(s.cos(k1*x+phi1)),s.simplify(s.cos(k2*x+phi2))]])
assert coeff==s.zeros(1,2) and coeff.rank()==0
registered=s.Matrix([[s.cos(s.Rational(21,40)),s.cos(s.Rational(21,20))]])
assert s.cos(s.Rational(21,40)).is_positive is True and registered.rank()==1
eta,Q=s.symbols('eta Q',real=True);c1,c2=registered[0,0],registered[0,1]
a1=(Q-c2*eta)/c1
assert s.simplify(c1*a1+c2*eta-Q)==0
print(json.dumps({'status':'PASS','all_node_rank':0,'all_node_amplitude_dimension':2,'nonzero_target_at_all_nodes':'INCOMPATIBLE','registered_rank':1,'registered_compatible_level_dimension':1,'initial_unqualified_claim':'REFUTED_BY_EXACT_KNOWN_PHASE_COUNTEREXAMPLE','corrected_claim':'rank one when at least one coefficient is nonzero; affine fibre dimension m-rank for compatible target','sympy':s.__version__},indent=2))
