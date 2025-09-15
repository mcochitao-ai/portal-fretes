from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from fretes.models import UserProfile


class Command(BaseCommand):
    help = 'Cria um usuário gerente com permissões corretas'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Nome de usuário')
        parser.add_argument('email', type=str, help='Email do usuário')
        parser.add_argument('password', type=str, help='Senha do usuário')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']
        
        # Verificar se usuário já existe
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.ERROR(f'❌ Usuário {username} já existe!')
            )
            return
        
        # Criar usuário
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name='Gerente',
            last_name='Sistema'
        )
        
        # Configurar perfil como gerente com permissões corretas
        profile = user.userprofile
        profile.tipo_usuario = 'gerente'
        profile.tipo_acesso = 'completo'
        profile.is_master = False  # IMPORTANTE: Gerente NÃO é master
        profile.save()
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ Usuário gerente criado: {username}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'📋 Acesso: Apenas "Aprovar Cotações"')
        )
        self.stdout.write(
            self.style.SUCCESS(f'🔑 Login: {username} / {password}')
        )

