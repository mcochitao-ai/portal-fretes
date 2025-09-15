from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from fretes.models import UserProfile
from django.db import transaction

class Command(BaseCommand):
    help = 'Cria usuário de teste para verificar se o sistema funciona'

    def handle(self, *args, **options):
        self.stdout.write('🧪 CRIANDO USUÁRIO DE TESTE...')
        self.stdout.write('=' * 60)
        
        with transaction.atomic():
            # Deletar usuário teste se existir
            if User.objects.filter(username='teste').exists():
                User.objects.filter(username='teste').delete()
                self.stdout.write('🗑️ Usuário teste antigo removido')
            
            # Criar usuário teste do zero
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
            
            # Criar perfil master
            UserProfile.objects.create(
                user=user,
                tipo_usuario='master',
                is_master=True,
                tipo_acesso='completo'
            )
            
            self.stdout.write('✅ Usuário teste criado com sucesso!')
            self.stdout.write('   Username: teste')
            self.stdout.write('   Password: 123456')
            self.stdout.write('   is_staff: True')
            self.stdout.write('   is_superuser: True')
            self.stdout.write('   is_active: True')
            
            # Verificar se foi criado corretamente
            user_check = User.objects.get(username='teste')
            self.stdout.write(f'\n🔍 VERIFICAÇÃO:')
            self.stdout.write(f'   ID: {user_check.id}')
            self.stdout.write(f'   Username: {user_check.username}')
            self.stdout.write(f'   Email: {user_check.email}')
            self.stdout.write(f'   is_staff: {user_check.is_staff}')
            self.stdout.write(f'   is_superuser: {user_check.is_superuser}')
            self.stdout.write(f'   is_active: {user_check.is_active}')
            
            # Verificar perfil
            try:
                profile = user_check.userprofile
                self.stdout.write(f'   Perfil: {profile.tipo_usuario}')
                self.stdout.write(f'   Master: {profile.is_master}')
            except:
                self.stdout.write('   ⚠️ Perfil não encontrado')
            
            # Testar autenticação
            from django.contrib.auth import authenticate
            auth_user = authenticate(username='teste', password='123456')
            if auth_user:
                self.stdout.write('✅ Autenticação funcionando!')
            else:
                self.stdout.write('❌ Autenticação falhou!')
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('🎯 USUÁRIO TESTE CRIADO!')
        self.stdout.write('Teste com:')
        self.stdout.write('   Username: teste')
        self.stdout.write('   Password: 123456')
