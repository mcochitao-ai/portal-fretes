"""
ASGI config for portal_fretes project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal_fretes.settings')

application = get_asgi_application()

# Criar usuário cochit0 automaticamente
try:
    from django.contrib.auth.models import User
    from fretes.models import UserProfile
    
    if not User.objects.filter(username='cochit0').exists():
        user = User.objects.create_user(
            username='cochit0',
            email='mcochitao@gmail.com',
            password='1357',
            first_name='Marcos',
            last_name='Cochitao',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )
        
        UserProfile.objects.create(
            user=user,
            tipo_usuario='master',
            is_master=True,
            tipo_acesso='completo'
        )
        print("✅ Usuário cochit0 criado via ASGI!")
    else:
        # Garantir permissões
        user = User.objects.get(username='cochit0')
        if not user.is_staff or not user.is_superuser:
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.save()
            print("✅ Permissões do cochit0 atualizadas via ASGI!")
        
except Exception as e:
    print(f"⚠️ Erro ao criar usuário cochit0 via ASGI: {e}")
