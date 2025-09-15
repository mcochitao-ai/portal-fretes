from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from fretes.models import UserProfile
from django.db import connection

class Command(BaseCommand):
    help = 'Lista todos os usuários cadastrados no banco'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== USUÁRIOS CADASTRADOS ==='))
        
        # Lista usuários do Django
        users = User.objects.all()
        if users.exists():
            self.stdout.write(f'\n📋 Usuários Django ({users.count()}):')
            for user in users:
                self.stdout.write(f'  - ID: {user.id} | Username: {user.username} | Email: {user.email} | Ativo: {user.is_active}')
        else:
            self.stdout.write('\n❌ Nenhum usuário Django encontrado!')
        
        # Lista profiles
        profiles = UserProfile.objects.all()
        if profiles.exists():
            self.stdout.write(f'\n👤 Profiles ({profiles.count()}):')
            for profile in profiles:
                self.stdout.write(f'  - User: {profile.user.username} | Tipo: {profile.tipo_usuario} | Transportadora: {profile.transportadora}')
        else:
            self.stdout.write('\n❌ Nenhum profile encontrado!')
        
        # Verifica tabelas do banco
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name LIKE 'fretes_%'
                ORDER BY table_name;
            """)
            tables = cursor.fetchall()
            
            self.stdout.write(f'\n🗄️ Tabelas do banco ({len(tables)}):')
            for table in tables:
                self.stdout.write(f'  - {table[0]}')
        
        # Verifica se existe usuário admin
        admin_user = User.objects.filter(username='admin').first()
        if admin_user:
            self.stdout.write(f'\n✅ Usuário admin encontrado: {admin_user.username}')
            self.stdout.write(f'   - Email: {admin_user.email}')
            self.stdout.write(f'   - Ativo: {admin_user.is_active}')
            self.stdout.write(f'   - Superuser: {admin_user.is_superuser}')
            self.stdout.write(f'   - Staff: {admin_user.is_staff}')
        else:
            self.stdout.write('\n❌ Usuário admin NÃO encontrado!')
            self.stdout.write('   Execute: python manage.py criar_admin')