# Configuração de Email para Reset de Senha

Para que a funcionalidade de "esqueci a senha" funcione corretamente, você precisa configurar as seguintes variáveis de ambiente:

## Variáveis Necessárias

```bash
# Configurações de Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha-de-app
DEFAULT_FROM_EMAIL=noreply@portalfretes.com
```

## Configuração com Gmail

1. **Ative a verificação em duas etapas** na sua conta do Gmail
2. **Gere uma senha de app**:
   - Vá para Configurações da Conta do Google
   - Segurança > Verificação em duas etapas > Senhas de app
   - Gere uma nova senha de app para "Mail"
3. **Use a senha de app** como `EMAIL_HOST_PASSWORD`

## Configuração com Outros Provedores

### Outlook/Hotmail
```bash
EMAIL_HOST=smtp-mail.outlook.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
```

### Yahoo
```bash
EMAIL_HOST=smtp.mail.yahoo.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
```

## Testando a Configuração

Para testar se o email está funcionando, você pode usar o shell do Django:

```python
python manage.py shell
```

```python
from django.core.mail import send_mail
from django.conf import settings

send_mail(
    'Teste de Email',
    'Este é um email de teste.',
    settings.DEFAULT_FROM_EMAIL,
    ['seu-email@exemplo.com'],
    fail_silently=False,
)
```

## Funcionalidades Implementadas

✅ **Solicitar Reset de Senha**: `/forgot-password/`
✅ **Redefinir Senha**: `/reset-password/<token>/`
✅ **Link no Login**: "Esqueci a senha" na página de login
✅ **Validação de Token**: Tokens expiram em 24 horas
✅ **Mensagens de Feedback**: Sucesso e erro para o usuário
✅ **Interface Responsiva**: Design consistente com o resto do sistema

