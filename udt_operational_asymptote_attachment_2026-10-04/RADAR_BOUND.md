# A lower bound for the original circular emitter's radar

The math reviewer independently supplied this source-first extension; the parent
rederives it here. It strengthens the radar distinction without replacing the
original circular source or presuming an echo for every phase.

Within the static region, every future causal curve obeys

    0 >= -f dt²+dr²/f+r²dOmega²,
    dt >= |dr|/f, since f>0 and future dt>0.

Suppose an actual outgoing/return signal pair joins the original circular clock
at radius a to a relay event at R<r_c and back. Each leg needs at least
integral_a^R dr/f in coordinate time; extra angular/radial motion cannot reduce
this bound. Along the source tau_e=sqrt(h)t, so its radar length is bounded by

    D_rad,circular = (tau_return-tau_emit)/2
                   >= sqrt(h) integral_a^R dr/f.

If such echoes remain available along R->r_c from below, this bound diverges
logarithmically because the outer root is simple. This is not a proof of an
echo or unique null return for every phase/radius. At/beyond r_c the candidate's
causal cone argument prohibits return to a altogether. Other receiver-origin
radar assignments involve different events and are not decided here.

The proper-clock factor is sqrt(h), distinct from sqrt(f(a)) for the separately
accelerated static-clock control. Both are lengths in c_E=1 units; restoring
seconds multiplies half of the proper-time interval by c_E. No new physical
relay/source mechanism or native distance convention is adopted.
