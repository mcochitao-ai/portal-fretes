from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from fretes.models import UserProfile

class Command(BaseCommand):
    help = 'Lista todos os usuários do sistema com suas credenciais e permissões'

    def handle(self, *args, **options):
        self.stdout.write('🔍 Listando todos os usuários do sistema...')
        self.stdout.write('=' * 60)
        
        users = User.objects.all().order_by('username')
        
        if not users.exists():
            self.stdout.write(self.style.WARNING('❌ Nenhum usuário encontrado no sistema!'))
            return
        
        for user in users:
            try:
                profile = user.userprofile
                tipo_usuario = profile.tipo_usuario
                is_master = profile.is_master
                tipo_acesso = profile.tipo_acesso
            except UserProfile.DoesNotExist:
                tipo_usuario = 'Sem perfil'
                is_master = False
                tipo_acesso = 'N/A'
            
            # Status do usuário
            status = []
            if user.is_active:
                status.append('✅ Ativo')
            else:
                status.append('❌ Inativo')
            
            if user.is_staff:
                status.append('👨‍💼 Staff')
            
            if user.is_superuser:
                status.append('🔑 Superuser')
            
            if is_master:
                status.append('👑 Master')
            
            status_str = ' | '.join(status)
            
            self.stdout.write(f'\n👤 Username: {user.username}')
            self.stdout.write(f'📧 Email: {user.email}')
            self.stdout.write(f'👨‍💼 Nome: {user.first_name} {user.last_name}')
            self.stdout.write(f'🏷️ Tipo: {tipo_usuario}')
            self.stdout.write(f'🔐 Acesso: {tipo_acesso}')
            self.stdout.write(f'📊 Status: {status_str}')
            self.stdout.write('-' * 40)
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('💡 Para acessar o Django Admin, use um usuário com "Staff" e "Superuser"')
        self.stdout.write('🔑 Usuários recomendados para admin:')
        
        admin_users = User.objects.filter(is_staff=True, is_superuser=True, is_active=True)
        for user in admin_users:
            self.stdout.write(f'   • {user.username} ({user.email})')
        
        if not admin_users.exists():
            self.stdout.write('   ❌ Nenhum usuário com permissões de admin encontrado!')
            self.stdout.write('   💡 Execute: python manage.py setup_producao')
