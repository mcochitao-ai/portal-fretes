from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from fretes.models import UserProfile

class Command(BaseCommand):
    help = 'Cria usuário cochit0 no servidor'

    def handle(self, *args, **options):
        self.stdout.write('🔧 Criando usuário cochit0...')
        
        # Verificar se já existe
        if User.objects.filter(username='cochit0').exists():
            user = User.objects.get(username='cochit0')
            self.stdout.write('✅ Usuário cochit0 já existe')
            
            # Garantir permissões de admin
            if not user.is_staff or not user.is_superuser:
                user.is_staff = True
                user.is_superuser = True
                user.is_active = True
                user.save()
                self.stdout.write('✅ Permissões de admin configuradas para cochit0')
            else:
                self.stdout.write('✅ cochit0 já tem permissões de admin')
            
            # Verificar se tem perfil
            if hasattr(user, 'userprofile'):
                profile = user.userprofile
                if not profile.is_master:
                    profile.is_master = True
                    profile.tipo_usuario = 'master'
                    profile.save()
                    self.stdout.write('✅ Perfil cochit0 atualizado para master')
            else:
                UserProfile.objects.create(
                    user=user,
                    tipo_usuario='master',
                    is_master=True,
                    tipo_acesso='completo'
                )
                self.stdout.write('✅ Perfil master criado para cochit0')
        else:
            # Criar usuário cochit0
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
        
        # Verificar se admin existe
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_user(
                username='admin',
                email='admin@portalfretes.com',
                password='admin123',
                first_name='Administrador',
                last_name='Sistema',
                is_staff=True,
                is_superuser=True,
                is_active=True
            )
            
            UserProfile.objects.create(
                user=admin_user,
                tipo_usuario='master',
                is_master=True,
                tipo_acesso='completo'
            )
            
            self.stdout.write('✅ Usuário admin criado!')
            self.stdout.write('   Username: admin')
            self.stdout.write('   Password: admin123')
        else:
            self.stdout.write('✅ Usuário admin já existe')
        
        self.stdout.write('\n🎉 Usuários criados com sucesso!')
        self.stdout.write('Agora você pode fazer login com:')
        self.stdout.write('   - cochit0 / 1357')
        self.stdout.write('   - admin / admin123')
