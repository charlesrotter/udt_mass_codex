import json,resource,signal,sys,time
requested=[]
def stop(s,f):requested.append(s)
signal.signal(signal.SIGTERM,stop)
print(json.dumps({'ready':True,'cpu_limit':resource.getrlimit(resource.RLIMIT_CPU),'as_limit':resource.getrlimit(resource.RLIMIT_AS)}),flush=True)
if sys.argv[1]=='delay':time.sleep(.25)
else:
    while not requested:time.sleep(.01)
print(json.dumps({'complete':True,'signals':requested}),flush=True)
raise SystemExit(75 if requested else 0)
