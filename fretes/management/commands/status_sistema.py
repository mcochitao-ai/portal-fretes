from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import connection
import os

class Command(BaseCommand):
    help = 'Mostra status atual do sistema'

    def handle(self, *args, **options):
        self.stdout.write('🔍 STATUS ATUAL DO SISTEMA')
        self.stdout.write('=' * 60)
        
        # 1. Verificar banco de dados
        self.stdout.write('\n🗄️ BANCO DE DADOS:')
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                self.stdout.write(f'   ✅ Conectado! Tabelas: {len(tables)}')
                for table in tables:
                    self.stdout.write(f'      - {table[0]}')
        except Exception as e:
            self.stdout.write(f'   ❌ Erro: {e}')
        
        # 2. Verificar usuários
        self.stdout.write('\n👥 USUÁRIOS:')
        try:
            users = User.objects.all()
            self.stdout.write(f'   Total: {users.count()}')
            for user in users:
                status = '✅' if user.is_active else '❌'
                staff = '👑' if user.is_staff else '👤'
                self.stdout.write(f'   {status} {staff} {user.username} (ativo: {user.is_active}, staff: {user.is_staff})')
        except Exception as e:
            self.stdout.write(f'   ❌ Erro: {e}')
        
        # 3. Verificar configurações
        self.stdout.write('\n⚙️ CONFIGURAÇÕES:')
        from django.conf import settings
        self.stdout.write(f'   DEBUG: {settings.DEBUG}')
        self.stdout.write(f'   DATABASE: {settings.DATABASES["default"]["ENGINE"]}')
        self.stdout.write(f'   ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}')
        
        # 4. Verificar ambiente
        self.stdout.write('\n🌍 AMBIENTE:')
        self.stdout.write(f'   RENDER: {os.environ.get("RENDER", "NÃO")}')
        self.stdout.write(f'   PORT: {os.environ.get("PORT", "NÃO DEFINIDA")}')
        self.stdout.write(f'   PYTHON_VERSION: {os.environ.get("PYTHON_VERSION", "NÃO DEFINIDA")}')
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('🏁 STATUS COMPLETO!')
