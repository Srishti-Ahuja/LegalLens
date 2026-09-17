import os
import sys
# Force protobuf pure‑python implementation for Python 3.14+ compatibility
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'
# Prevent loading of compiled protobuf extensions that crash on Python 3.14
sys.modules.setdefault('google._upb._message', None)
sys.modules.setdefault('google.protobuf.pyext._message', None)
# Log that sitecustomize ran
with open('sitecustomize_loaded.log', 'w') as f:
    f.write('sitecustomize loaded\n')
