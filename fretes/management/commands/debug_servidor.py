from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection
from django.contrib.auth.models import User
from fretes.models import FreteRequest, UserProfile
import os

class Command(BaseCommand):
    help = 'Debug do servidor - verifica problemas que podem causar erro 500'

    def handle(self, *args, **options):
        self.stdout.write('🔍 Debug do servidor - verificando problemas...')
        self.stdout.write('=' * 60)
        
        # 1. Verificar configuração do banco
        self.stdout.write('\n📊 1. Configuração do banco:')
        db_config = settings.DATABASES['default']
        self.stdout.write(f'   Engine: {db_config["ENGINE"]}')
        self.stdout.write(f'   Name: {db_config["NAME"]}')
        
        database_url = os.environ.get('DATABASE_URL')
        if database_url:
            self.stdout.write(f'   DATABASE_URL: {database_url[:50]}...')
        else:
            self.stdout.write('   ❌ DATABASE_URL: Não definida')
        
        # 2. Testar conexão com banco
        self.stdout.write('\n🔌 2. Teste de conexão:')
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                if result:
                    self.stdout.write('   ✅ Conexão: OK')
                else:
                    self.stdout.write('   ❌ Conexão: FALHOU')
        except Exception as e:
            self.stdout.write(f'   ❌ Erro na conexão: {e}')
        
        # 3. Verificar se tabelas existem
        self.stdout.write('\n📋 3. Verificação de tabelas:')
        try:
            with connection.cursor() as cursor:
                # Verificar tabela de usuários
                cursor.execute("SELECT COUNT(*) FROM auth_user")
                user_count = cursor.fetchone()[0]
                self.stdout.write(f'   ✅ Tabela auth_user: {user_count} usuários')
                
                # Verificar tabela de fretes
                cursor.execute("SELECT COUNT(*) FROM fretes_freterequest")
                frete_count = cursor.fetchone()[0]
                self.stdout.write(f'   ✅ Tabela fretes_freterequest: {frete_count} fretes')
                
        except Exception as e:
            self.stdout.write(f'   ❌ Erro ao verificar tabelas: {e}')
        
        # 4. Verificar usuários
        self.stdout.write('\n👥 4. Verificação de usuários:')
        try:
            users = User.objects.all()
            self.stdout.write(f'   Total de usuários: {users.count()}')
            
            admin_users = User.objects.filter(is_staff=True, is_superuser=True)
            self.stdout.write(f'   Usuários admin: {admin_users.count()}')
            
            if admin_users.exists():
                for user in admin_users:
                    self.stdout.write(f'   - {user.username} (ativo: {user.is_active})')
            else:
                self.stdout.write('   ❌ Nenhum usuário admin encontrado!')
                
        except Exception as e:
            self.stdout.write(f'   ❌ Erro ao verificar usuários: {e}')
        
        # 5. Verificar configurações Django
        self.stdout.write('\n⚙️ 5. Configurações Django:')
        self.stdout.write(f'   DEBUG: {settings.DEBUG}')
        self.stdout.write(f'   ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}')
        self.stdout.write(f'   SECRET_KEY: {"Definida" if settings.SECRET_KEY else "Não definida"}')
        
        # 6. Verificar arquivos estáticos
        self.stdout.write('\n📁 6. Arquivos estáticos:')
        self.stdout.write(f'   STATIC_URL: {settings.STATIC_URL}')
        self.stdout.write(f'   STATIC_ROOT: {settings.STATIC_ROOT}')
        self.stdout.write(f'   MEDIA_URL: {settings.MEDIA_URL}')
        self.stdout.write(f'   MEDIA_ROOT: {settings.MEDIA_ROOT}')
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('💡 Se houver erros acima, eles podem causar Server Error 500')
        self.stdout.write('🔧 Verifique os logs do Render para mais detalhes')
