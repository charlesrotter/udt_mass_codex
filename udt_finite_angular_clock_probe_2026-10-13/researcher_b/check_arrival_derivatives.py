"""Same-worldline arrival derivative versus endpoint frequency ratios."""
import json
import numpy as np
from scipy.optimize import root
from original_clock_probe import ClockProbe

rows=[]
for epsilon,L in [(0.,.06),(-1e-5,.04)]:
    probe=ClockProbe(epsilon=epsilon,fine=True)
    for mu in [.13,.57,.91]:
        tp,xp,momenta,errors=probe.prepare(L,mu)
        reference=probe.one(L,mu)
        def bvel(ts):
            lapse,a,_,_=probe.geom(ts)
            gamma=np.sqrt(1+np.sum(momenta*momenta/(a*a),axis=-1))
            return lapse[:,None]*momenta/(a*a*gamma[:,None])
        def bpos(t):
            return xp+probe.integrate(bvel,tp,t)
        def rayvel(ts,q):
            lapse,a,_,_=probe.geom(ts)
            w=np.sqrt(np.sum(q*q/(a*a),axis=-1))
            return lapse[:,None]*q/(a*a*w[:,None])
        def clock_rate(ts,is_b):
            lapse,a,_,_=probe.geom(ts)
            gamma=np.sqrt(1+np.sum(momenta*momenta/(a*a),axis=-1)) if is_b else np.ones_like(ts)
            return (lapse/gamma)[:,None]
        def arrival(te,reverse):
            qref=reference['reverse_q' if reverse else 'outgoing_q']
            trref=reference['reverse_t' if reverse else 'outgoing_t']
            def residual(variables):
                angle,tr=variables
                q=np.array([np.cos(angle),np.sin(angle),0.])
                flight=probe.integrate(lambda ts:rayvel(ts,q),te,tr)
                return (bpos(te)+flight if reverse else flight-bpos(tr))[:2]
            sol=root(residual,[np.arctan2(qref[1],qref[0]),trref+(te-(tp if reverse else 1.))],
                     method='hybr',options={'xtol':1e-11})
            er=float(np.max(np.abs(residual(sol.x))))
            assert er<2e-12,er
            return float(sol.x[1]),er
        for reverse in [False,True]:
            te0=tp if reverse else 1.
            tr0=reference['reverse_t' if reverse else 'outgoing_t']
            freq=float(np.exp(reference['log_minus' if reverse else 'log_plus']))
            src_rate=float(clock_rate(np.array([te0]),reverse)[0,0])
            for step in [2e-4,1e-4]:
                vals=[]; residuals=[]
                for multiplier in [-2,-1,1,2]:
                    tr,er=arrival(te0+multiplier*step,reverse)
                    proper_increment=float(probe.integrate(lambda ts:clock_rate(ts,not reverse),tr0,tr)[0])
                    vals.append(proper_increment);residuals.append(er)
                derivative=(vals[0]-8*vals[1]+8*vals[2]-vals[3])/(12*step*src_rate)
                error=abs(derivative-freq)
                assert error<2e-8,(epsilon,L,mu,reverse,step,error)
                rows.append(dict(epsilon=epsilon,L=L,mu=mu,reverse_first=reverse,
                                 step=step,frequency_ratio=freq,arrival_derivative=derivative,
                                 absolute_difference=error,max_incidence_residual=max(residuals)))
print(json.dumps(dict(status='PASS_SAME_HISTORY_DERIVATIVE_CHECK',results=rows),indent=2))
