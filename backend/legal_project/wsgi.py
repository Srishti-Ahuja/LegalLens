import os
from django.core.wsgi import get_wsgi_application

os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'legal_project.settings')

application = get_wsgi_application()
