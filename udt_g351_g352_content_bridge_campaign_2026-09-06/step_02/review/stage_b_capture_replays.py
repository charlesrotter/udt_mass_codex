#!/usr/bin/env python3
"""One-time review evidence capture; immutable input code, fresh output folder."""
import argparse, datetime, json, pathlib, resource, subprocess, time
parser=argparse.ArgumentParser()
parser.add_argument('--repo',type=pathlib.Path,required=True)
parser.add_argument('--output',type=pathlib.Path,required=True)
args=parser.parse_args()
repo=args.repo.resolve(); out=args.output.resolve()
here=pathlib.Path(__file__).resolve().parent
assert out.is_dir()
prefix='udt_g351_g352_content_bridge_campaign_2026-09-06/step_02'
records=[]
def run(name,command,cwd=repo,limited=False):
    def limits():
        resource.setrlimit(resource.RLIMIT_AS,(512*1024**2,512*1024**2))
        resource.setrlimit(resource.RLIMIT_CPU,(60,60))
    start=datetime.datetime.now(datetime.timezone.utc).isoformat(); t=time.monotonic()
    with (out/(name+'.stdout')).open('xb') as stdout,(out/(name+'.stderr')).open('xb') as stderr:
        p=subprocess.run(command,cwd=cwd,stdout=stdout,stderr=stderr,timeout=60,
                         preexec_fn=limits if limited else None)
    row={'name':name,'command':command,'cwd':str(cwd),'start_utc':start,
         'actual_exit':p.returncode,'wall_seconds':round(time.monotonic()-t,6)}
    records.append(row)
    return p.returncode

try:
    assert run('stage_b_candidate_auth',['sha256sum','--check',prefix+'/FROZEN_CANDIDATE_SHA256SUMS'])==0
    assert run('stage_b_source_auth',['sha256sum','--check',prefix+'/SOURCE_SHA256SUMS'])==0
    assert run('stage_b_frozen_diff',['git','diff','--exit-code','9aa8dc44b0a7afe92765960851b678e9b6f355fe','--',prefix])==0
    assert run('stage_b_stage_a_auth',['sha256sum','--check','STAGE_A_SHA256SUMS'],cwd=here)==0
    assert run('stage_b_independent',['/usr/bin/time','-v','python3','-B',str(here/'stage_b_independent_comparison.py'),'--repo',str(repo)],limited=True)==0
    assert run('stage_b_author_baseline',['/usr/bin/time','-v','python3','-B',prefix+'/check_naturality.py'],limited=True)==0
    assert (out/'stage_b_author_baseline.stdout').read_bytes()==(repo/prefix/'AUTHOR_RESULT.json').read_bytes()
    expected={'v_shift_sign':'full_translation_isometry','wrong_y_ode':'full_translation_isometry',
              'homothety_v_power':'full_proper_homothety','density_scale':'quotient_amount_area_weight',
              'component_as_scalar':'passive_null_boost_metric'}
    for mutation,guard in expected.items():
        name='stage_b_'+mutation
        rc=run(name,['/usr/bin/time','-v','python3','-B',prefix+'/check_naturality.py','--mutation',mutation],limited=True)
        assert rc==1 and 'AssertionError: '+guard in (out/(name+'.stderr')).read_text()
        records[-1]['expected_first_failing_guard']=guard
        records[-1]['matching_guard_observed']=True
    assert run('stage_b_final_git',['git','rev-parse','HEAD'])==0
finally:
    with (out/'STAGE_B_REPLAY_RESULTS.json').open('x') as f:
        json.dump({'records':records,'limits':{'address_space_MiB':512,'CPU_seconds':60,'wall_seconds':60,'one_math_child_at_a_time':True}},f,indent=2)
print(json.dumps(records,indent=2))
