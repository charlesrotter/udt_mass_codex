"""Direct finite arrival maps, independent of the energy quadrature proof."""
import json
import platform
import numpy as np
import scipy
from scipy.integrate import solve_ivp

def run(rtol,atol,max_step,h):
    f=lambda r:1-r**4
    fp=lambda r:-4*r**3
    # y=(r,dr/dt,tau). Original coordinate-time timelike geodesic equation.
    def clock_rhs(t,y):
        r,v,tau=y; ff=f(r)
        return [v,-ff*fp(r)/2+3*fp(r)*v*v/(2*ff),np.sqrt(ff-v*v/ff)]
    clock=solve_ivp(clock_rhs,(0,0.75),[0.25,0.,0.],method='DOP853',
                    rtol=rtol,atol=atol,max_step=max_step,dense_output=True)
    assert clock.success
    def outgoing(s):
        def encounter(t,y):return y[0]-clock.sol(t)[0]
        encounter.terminal=True;encounter.direction=1
        ray=solve_ivp(lambda t,y:[f(y[0])],(s,0.75),[0.],method='DOP853',
                      events=encounter,rtol=rtol,atol=atol,max_step=max_step)
        assert ray.success and len(ray.t_events[0])==1
        t=float(ray.t_events[0][0]); r,v,tau=clock.sol(t)
        return dict(emission=s,arrival_t=t,arrival_r=float(r),arrival_tau=float(tau),
                    original_null_incidence_residual=float(ray.y_events[0][0,0]-r))
    outs=[outgoing(s) for s in (-h,0,h)]
    p_fd=(outs[2]['arrival_tau']-outs[0]['arrival_tau'])/(2*h)
    relay=outs[1]['arrival_t']
    def incoming(tstart):
        r,v,tau=clock.sol(tstart)
        def center(t,y):return y[0]
        center.terminal=True;center.direction=-1
        ray=solve_ivp(lambda t,y:[-f(y[0])],(tstart,1.5),[r],method='DOP853',
                      events=center,rtol=rtol,atol=atol,max_step=max_step)
        assert ray.success and len(ray.t_events[0])==1
        return dict(relay_t=float(tstart),relay_tau=float(tau),return_t=float(ray.t_events[0][0]),
                    original_return_incidence_residual=float(ray.y_events[0][0,0]))
    returns=[incoming(relay+x) for x in (-h,0,h)]
    q_fd=(returns[2]['return_t']-returns[0]['return_t'])/(returns[2]['relay_tau']-returns[0]['relay_tau'])
    rr,vv,tau=clock.sol(relay)
    proper_rate=np.sqrt(f(rr)-vv*vv/f(rr))
    E_from_trajectory=f(rr)/proper_rate
    v_proper=vv/proper_rate
    exact_E=np.sqrt(f(0.25))
    p_endpoint=exact_E+v_proper
    q_endpoint=1/(exact_E-v_proper)
    sample=clock.sol(np.linspace(0,0.75,101))
    rvals,vvals=sample[0],sample[1]
    rates=np.sqrt(1-rvals**4-vvals*vvals/(1-rvals**4))
    energy=(1-rvals**4)/rates
    normalization=-(1-rvals**4)/rates**2+(vvals/rates)**2/(1-rvals**4)+1
    return dict(rtol=rtol,atol=atol,max_step=max_step,h=h,
                outgoing=outs,returns=returns,p_fd=float(p_fd),q_fd=float(q_fd),
                p_endpoint=float(p_endpoint),q_endpoint=float(q_endpoint),
                p_difference=float(p_fd-p_endpoint),q_difference=float(q_fd-q_endpoint),
                energy_max_abs_residual=float(np.max(np.abs(energy-exact_E))),
                normalization_max_abs_residual=float(np.max(np.abs(normalization))),
                normalization_note='uses proper rate from metric and is algebraic; energy residual is independent trajectory diagnostic',
                E_from_trajectory=float(E_from_trajectory),v_proper=float(v_proper))

results=[run(1e-11,1e-13,0.002,1e-4),run(1e-12,1e-14,0.001,5e-5)]
for out in results:
    assert out['p_fd']>1 and out['q_fd']>1
    assert abs(out['p_difference'])<1e-7 and abs(out['q_difference'])<1e-7
    assert out['energy_max_abs_residual']<1e-10
print(json.dumps(dict(kind='float64 direct arrival-map diagnostic, not interval proof',
    python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,
    runs=results,p_change=results[1]['p_fd']-results[0]['p_fd'],
    q_change=results[1]['q_fd']-results[0]['q_fd'],all_assertions_passed=True),indent=2))
