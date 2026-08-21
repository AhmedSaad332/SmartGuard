import sys, os, importlib
print('cwd=', os.getcwd())
print('sys.path[0]=', sys.path[0])
print('sys.path[:5]=', sys.path[:5])
try:
    m = importlib.import_module('routers.video_stream_router')
    print('OK imported', m.__file__)
except Exception as e:
    import traceback
    traceback.print_exc()
    print('FAILED:', e)
