# Exact simplification repair before candidate freeze

The first check stopped on the product-metric divergence component
alpha*(sin(2*y)*tan(y)+cos(2*y)-1)/(r**4*sin(y)**2*tan(y)).
Its numerator is identically zero on a regular coordinate patch: substitute
sin(2y)=2sin(y)cos(y), tan(y)=sin(y)/cos(y), cos(2y)=1-2sin(y)^2.
The original simplify/trigsimp route did not reduce it. Preserve the original
code and comparisons_01 stdout/stderr/receipt. The repair changes only the zero
normalizer to expand trig functions and apply SymPy's fu trigonometric rules;
no equation, expected result, tolerance or resource cap changes. Removable
trigonometric denominators from simplification do not remove regular equator
points from the underlying smooth product metric.
