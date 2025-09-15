from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import connection
import os
import sys

class Command(BaseCommand):
    help = 'Debug completo do sistema no Render'

    def handle(self, *args, **options):
        self.stdout.write('🔍 DEBUG COMPLETO DO RENDER')
        self.stdout.write('=' * 80)
        
        # 1. Informações do ambiente
        self.stdout.write('\n🌍 AMBIENTE:')
        self.stdout.write(f'   Python: {sys.version}')
        self.stdout.write(f'   RENDER: {os.environ.get("RENDER", "NÃO")}')
        self.stdout.write(f'   PORT: {os.environ.get("PORT", "NÃO DEFINIDA")}')
        self.stdout.write(f'   DATABASE_URL: {os.environ.get("DATABASE_URL", "NÃO DEFINIDA")[:50]}...')
        
        # 2. Configurações Django
        self.stdout.write('\n⚙️ DJANGO:')
        from django.conf import settings
        self.stdout.write(f'   DEBUG: {settings.DEBUG}')
        self.stdout.write(f'   DATABASE: {settings.DATABASES["default"]["ENGINE"]}')
        self.stdout.write(f'   ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}')
        
        # 3. Teste de conexão com banco
        self.stdout.write('\n🗄️ BANCO DE DADOS:')
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                self.stdout.write(f'   ✅ Conectado! Tabelas: {len(tables)}')
                for table in tables:
                    self.stdout.write(f'      - {table[0]}')
        except Exception as e:
            self.stdout.write(f'   ❌ Erro na conexão: {e}')
        
        # 4. Verificar usuários
        self.stdout.write('\n👥 USUÁRIOS:')
        try:
            users = User.objects.all()
            self.stdout.write(f'   Total: {users.count()}')
            for user in users:
                status = '✅' if user.is_active else '❌'
                staff = '👑' if user.is_staff else '👤'
                self.stdout.write(f'   {status} {staff} {user.username}')
        except Exception as e:
            self.stdout.write(f'   ❌ Erro ao listar usuários: {e}')
        
        # 5. Teste específico do cochit0
        self.stdout.write('\n🔐 TESTE COCHIT0:')
        try:
            user = User.objects.get(username='cochit0')
            self.stdout.write(f'   ✅ Usuário encontrado: {user.username}')
            self.stdout.write(f'   📧 Email: {user.email}')
            self.stdout.write(f'   👑 Staff: {user.is_staff}')
            self.stdout.write(f'   🔧 Superuser: {user.is_superuser}')
            self.stdout.write(f'   ✅ Ativo: {user.is_active}')
            
            # Testar senha
            from django.contrib.auth import authenticate
            auth_user = authenticate(username='cochit0', password='123456')
            if auth_user:
                self.stdout.write('   ✅ Autenticação: SUCESSO!')
            else:
                self.stdout.write('   ❌ Autenticação: FALHOU!')
                
        except User.DoesNotExist:
            self.stdout.write('   ❌ Usuário cochit0 NÃO ENCONTRADO!')
        except Exception as e:
            self.stdout.write(f'   ❌ Erro: {e}')
        
        # 6. Verificar arquivos importantes
        self.stdout.write('\n📄 ARQUIVOS:')
        important_files = ['manage.py', 'requirements.txt', 'render.yaml']
        for file in important_files:
            if os.path.exists(file):
                self.stdout.write(f'   ✅ {file}')
            else:
                self.stdout.write(f'   ❌ {file} não encontrado')
        
        self.stdout.write('\n' + '=' * 80)
        self.stdout.write('🏁 DEBUG COMPLETO!')
