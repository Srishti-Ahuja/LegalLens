import os
# Ensure protobuf uses pure‑python implementation on Python 3.14 and newer
os.environ.setdefault('PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION', 'python')
