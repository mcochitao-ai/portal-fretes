from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from fretes.models import UserProfile


class Command(BaseCommand):
    help = 'Testa a criação de um novo usuário para verificar se recebe acesso limitado por padrão'

    def add_arguments(self, parser):
        parser.add_argument(
            '--usuario',
            type=str,
            default='teste_usuario',
            help='Nome do usuário de teste (padrão: teste_usuario)'
        )

    def handle(self, *args, **options):
        username = options['usuario']
        
        # Verificar se o usuário já existe
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'⚠️ Usuário "{username}" já existe!')
            )
            return
        
        # Criar novo usuário
        user = User.objects.create_user(
            username=username,
            email=f'{username}@teste.com',
            password='123456'
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ Usuário "{username}" criado com sucesso!')
        )
        
        # Verificar o perfil criado automaticamente
        try:
            profile = user.userprofile
            self.stdout.write(
                self.style.SUCCESS(
                    f'📋 Perfil criado automaticamente com acesso: {profile.get_tipo_acesso_display()}'
                )
            )
            
            if profile.tipo_acesso == 'limitado':
                self.stdout.write(
                    self.style.SUCCESS('✅ CONFIRMADO: Novo usuário recebe acesso LIMITADO por padrão!')
                )
            else:
                self.stdout.write(
                    self.style.ERROR('❌ ERRO: Novo usuário não recebeu acesso limitado!')
                )
                
        except UserProfile.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('❌ ERRO: Perfil não foi criado automaticamente!')
            )
        
        # Mostrar lista atualizada
        self.stdout.write('\n📋 Lista atual de usuários:')
        self.stdout.write('=' * 40)
        
        for user in User.objects.all().order_by('username'):
            try:
                profile = user.userprofile
                tipo = profile.get_tipo_acesso_display()
                if profile.tipo_acesso == 'completo':
                    icon = '🔧'
                else:
                    icon = '📋'
            except UserProfile.DoesNotExist:
                tipo = 'Não configurado'
                icon = '❓'
            
            self.stdout.write(f'{icon} {user.username:<20} - {tipo}')
