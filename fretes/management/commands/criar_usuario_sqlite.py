from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from fretes.models import UserProfile
from django.db import transaction

class Command(BaseCommand):
    help = 'Cria usuário no SQLite para garantir funcionamento'

    def handle(self, *args, **options):
        self.stdout.write('🔧 CRIANDO USUÁRIO NO SQLITE...')
        self.stdout.write('=' * 60)
        
        with transaction.atomic():
            # Deletar usuário teste se existir
            if User.objects.filter(username='teste').exists():
                User.objects.filter(username='teste').delete()
                self.stdout.write('🗑️ Usuário teste antigo removido')
            
            # Criar usuário teste
            user = User.objects.create_user(
                username='teste',
                email='teste@teste.com',
                password='123456',
                first_name='Usuario',
                last_name='Teste',
                is_staff=True,
                is_superuser=True,
                is_active=True
            )
            
            # Criar perfil
            UserProfile.objects.create(
                user=user,
                tipo_usuario='master',
                is_master=True,
                tipo_acesso='completo'
            )
            
            self.stdout.write('✅ Usuário teste criado no SQLite!')
            self.stdout.write('   Username: teste')
            self.stdout.write('   Password: 123456')
            
            # Verificar se foi criado
            user_check = User.objects.get(username='teste')
            self.stdout.write(f'   ID: {user_check.id}')
            self.stdout.write(f'   is_staff: {user_check.is_staff}')
            self.stdout.write(f'   is_superuser: {user_check.is_superuser}')
            self.stdout.write(f'   is_active: {user_check.is_active}')
            
            # Testar autenticação
            from django.contrib.auth import authenticate
            auth_user = authenticate(username='teste', password='123456')
            if auth_user:
                self.stdout.write('✅ Autenticação funcionando!')
            else:
                self.stdout.write('❌ Autenticação falhou!')
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('🎯 USUÁRIO CRIADO NO SQLITE!')
        self.stdout.write('Teste com:')
        self.stdout.write('   Username: teste')
        self.stdout.write('   Password: 123456')
