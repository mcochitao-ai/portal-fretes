# Correção do Problema de Deslogamento Automático

## Problema Identificado

O usuário estava sendo deslogado automaticamente do portal devido a configurações incorretas de sessão.

### Causa Raiz

1. **Sessões em Cache Local**: Estávamos usando `LocMemCache` para armazenar sessões
2. **Múltiplos Workers**: O Gunicorn usa múltiplos workers, cada um com sua própria memória
3. **Perda de Sessão**: Quando o usuário era redirecionado para um worker diferente, a sessão era perdida

## Solução Implementada

### 1. Mudança para Sessões em Banco de Dados

**Antes:**
```python
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
```

**Depois:**
```python
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 86400  # 24 horas
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
```

### 2. Configurações de Segurança Adicionadas

```python
# Configurações de autenticação
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# Configurações de segurança para cookies
CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'
```

### 3. Comando de Configuração de Sessões

Criado `fretes/management/commands/setup_sessions.py` para garantir que a tabela de sessões seja criada.

### 4. Atualização do Deploy

O comando `init_deploy.py` foi atualizado para configurar sessões durante o deploy.

## Benefícios da Correção

1. **Persistência**: Sessões persistem entre workers do Gunicorn
2. **Segurança**: Cookies seguros em produção
3. **Durabilidade**: Sessões duram 24 horas por padrão
4. **Confiabilidade**: Não há mais deslogamentos inesperados

## Arquivos Modificados

- `portal_fretes/settings.py` - Configurações de sessão
- `fretes/management/commands/setup_sessions.py` - Novo comando
- `fretes/management/commands/init_deploy.py` - Atualizado

## Como Testar

1. Fazer login no portal
2. Navegar entre páginas
3. Aguardar alguns minutos
4. Verificar se ainda está logado
5. Fazer refresh da página
6. Confirmar que não foi deslogado

## Monitoramento

- Verificar logs do Render para confirmar que não há erros de sessão
- Testar em diferentes navegadores
- Verificar se a tabela `django_session` foi criada no banco
