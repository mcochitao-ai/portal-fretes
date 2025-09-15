from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import connection
import os

class Command(BaseCommand):
    help = 'Status final do sistema'

    def handle(self, *args, **options):
        self.stdout.write('🎯 STATUS FINAL DO SISTEMA')
        self.stdout.write('=' * 80)
        
        # 1. Ambiente
        self.stdout.write('\n🌍 AMBIENTE:')
        self.stdout.write(f'   RENDER: {os.environ.get("RENDER", "NÃO")}')
        self.stdout.write(f'   DATABASE_URL: {"✅ DEFINIDA" if os.environ.get("DATABASE_URL") else "❌ NÃO DEFINIDA"}')
        
        # 2. Banco de dados
        self.stdout.write('\n🗄️ BANCO DE DADOS:')
        try:
            with connection.cursor() as cursor:
                # Verificar se é PostgreSQL
                cursor.execute("SELECT version();")
                version = cursor.fetchone()[0]
                if 'PostgreSQL' in version:
                    self.stdout.write(f'   ✅ PostgreSQL: {version[:50]}...')
                    
                    # Listar tabelas
                    cursor.execute("""
                        SELECT table_name 
                        FROM information_schema.tables 
                        WHERE table_schema = 'public' 
                        ORDER BY table_name;
                    """)
                    tables = cursor.fetchall()
                    self.stdout.write(f'   📋 Tabelas: {len(tables)}')
                    for table in tables:
                        self.stdout.write(f'      - {table[0]}')
                else:
                    self.stdout.write(f'   ✅ SQLite: {version[:50]}...')
        except Exception as e:
            self.stdout.write(f'   ❌ Erro: {e}')
        
        # 3. Usuários
        self.stdout.write('\n👥 USUÁRIOS:')
        try:
            users = User.objects.all()
            self.stdout.write(f'   Total: {users.count()}')
            for user in users:
                status = '✅' if user.is_active else '❌'
                staff = '👑' if user.is_staff else '👤'
                self.stdout.write(f'   {status} {staff} {user.username}')
        except Exception as e:
            self.stdout.write(f'   ❌ Erro: {e}')
        
        # 4. Teste de login
        self.stdout.write('\n🔐 TESTE DE LOGIN:')
        usuarios_teste = [
            ('admin', 'admin123'),
            ('cochit0', '123456'),
        ]
        
        for username, password in usuarios_teste:
            try:
                from django.contrib.auth import authenticate
                user = authenticate(username=username, password=password)
                if user:
                    self.stdout.write(f'   ✅ {username}: SUCESSO')
                else:
                    self.stdout.write(f'   ❌ {username}: FALHOU')
            except Exception as e:
                self.stdout.write(f'   ❌ {username}: ERRO - {e}')
        
        self.stdout.write('\n' + '=' * 80)
        self.stdout.write('🏁 STATUS FINAL COMPLETO!')
