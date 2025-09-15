from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from fretes.models import UserProfile
from django.db import transaction

class Command(BaseCommand):
    help = 'FORÇA criação do usuário cochit0'

    def handle(self, *args, **options):
        self.stdout.write('🚨 FORÇANDO CRIAÇÃO DO USUÁRIO COCHIT0...')
        self.stdout.write('=' * 60)
        
        with transaction.atomic():
            # Deletar usuário cochit0 se existir
            if User.objects.filter(username='cochit0').exists():
                User.objects.filter(username='cochit0').delete()
                self.stdout.write('🗑️ Usuário cochit0 antigo removido')
            
            # Criar usuário cochit0 do zero
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
            
            # Criar perfil master
            UserProfile.objects.create(
                user=user,
                tipo_usuario='master',
                is_master=True,
                tipo_acesso='completo'
            )
            
            self.stdout.write('✅ Usuário cochit0 criado com sucesso!')
            self.stdout.write('   Username: cochit0')
            self.stdout.write('   Password: 1357')
            self.stdout.write('   is_staff: True')
            self.stdout.write('   is_superuser: True')
            self.stdout.write('   is_active: True')
            
            # Verificar se foi criado corretamente
            user_check = User.objects.get(username='cochit0')
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
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('🎯 USUÁRIO COCHIT0 CRIADO COM SUCESSO!')
        self.stdout.write('Agora você pode fazer login com:')
        self.stdout.write('   Username: cochit0')
        self.stdout.write('   Password: 1357')
