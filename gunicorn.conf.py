# Configuração do Gunicorn para otimizar performance no Render

import os

# Configurações básicas
bind = f"0.0.0.0:{os.environ.get('PORT', 8000)}"
workers = 2
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 2

# Configurações de performance
max_requests = 1000
max_requests_jitter = 100
preload_app = True

# Configurações de logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Configurações de segurança
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Configurações de processo
user = None
group = None
tmp_upload_dir = None

# Configurações de SSL (se necessário)
# keyfile = None
# certfile = None

# Configurações de proxy
forwarded_allow_ips = "*"
secure_scheme_headers = {
    'X-FORWARDED-PROTOCOL': 'ssl',
    'X-FORWARDED-PROTO': 'https',
    'X-FORWARDED-SSL': 'on'
}
