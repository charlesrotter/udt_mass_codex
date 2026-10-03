# Independent hand extraction of the universal quartic coefficient

After candidate exposure I checked the quartic arrival algebra without importing
or rerunning the parent's arrival-series routine. This derives from the inspected
F2,F4,F6 interval polynomials, so it is a check of their consequences, not an
independent geometric derivation of those polynomials. Put e=L².

The first root is y=1-T e/6+O(e²). At x=0, dividing the endpoint derivatives by
their common2y factor gives

    p=1-T e/2+(T²/6-ab/6-bb/24)e²+O(e³).

For return x=2-4T e/3+O(e²), y=1-T e/6+O(e²). In the ratio -F_y/F_x,
write the numerator minus denominator as

    T(x+y)e-(partial_x F6+partial_y F6)e².

At(2,1), the last derivative sum is4aa+ab-bb/4; the denominator through
first order is -2+2T e/3. Hence

    q=1-3T e/2+(T²/4+2aa+ab/2-bb/8)e²+O(e³),
    log p=-T e/2+(T²/24-ab/6-bb/24)e²+O(e³),
    log q=-3T e/2+(-7T²/8+2aa+ab/2-bb/8)e²+O(e³).

For t=log p, log[p/(2-p²)]=3t+4t²+8t³+O(t⁴). At e² this leaves

    d4=2aa+ab-2T²=2|V|²+<V,W>.

The signs and actual later return are therefore independently checked at the
lowest nonzero generic order. Sixth-order generality still rests on the exact
finite interval algebra plus reviewed contractions, with independent direct
sphere-product validation of its numeric rational specializations.
