"""
Arquivo temporário para compatibilidade com o deploy no Render.
Este arquivo redireciona para o WSGI correto do Django.
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

# Configura o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal_fretes.settings')

# Obtém a aplicação WSGI do Django
application = get_wsgi_application()

# Para compatibilidade com gunicorn app:app
app = application
