from django.core.management.base import BaseCommand
from django.db import connection
from django.core.management import execute_from_command_line
import os

class Command(BaseCommand):
    help = 'Força configuração do PostgreSQL'

    def handle(self, *args, **options):
        self.stdout.write('🐘 FORÇANDO CONFIGURAÇÃO DO POSTGRESQL')
        self.stdout.write('=' * 60)
        
        # Mostrar ambiente
        self.stdout.write(f'🌍 Ambiente: {"RENDER" if os.environ.get("RENDER") else "LOCAL"}')
        self.stdout.write(f'🗄️ DATABASE_URL: {os.environ.get("DATABASE_URL", "NÃO DEFINIDA")[:50]}...')
        
        try:
            # 1. Verificar conexão
            self.stdout.write('\n🔌 TESTANDO CONEXÃO:')
            with connection.cursor() as cursor:
                cursor.execute("SELECT version();")
                version = cursor.fetchone()
                self.stdout.write(f'   ✅ Conectado! PostgreSQL: {version[0][:50]}...')
            
            # 2. Executar makemigrations
            self.stdout.write('\n📝 EXECUTANDO MAKEMIGRATIONS:')
            try:
                execute_from_command_line(['manage.py', 'makemigrations', '--verbosity=2'])
                self.stdout.write('   ✅ Makemigrations executado!')
            except Exception as e:
                self.stdout.write(f'   ⚠️ Makemigrations: {e}')
            
            # 3. Executar migrate
            self.stdout.write('\n🚀 EXECUTANDO MIGRATE:')
            try:
                execute_from_command_line(['manage.py', 'migrate', '--verbosity=2'])
                self.stdout.write('   ✅ Migrate executado!')
            except Exception as e:
                self.stdout.write(f'   ❌ Migrate falhou: {e}')
            
            # 4. Verificar tabelas
            self.stdout.write('\n📊 VERIFICANDO TABELAS:')
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    ORDER BY table_name;
                """)
                tables = cursor.fetchall()
                self.stdout.write(f'   📋 Total de tabelas: {len(tables)}')
                for table in tables:
                    self.stdout.write(f'      - {table[0]}')
            
            # 5. Verificar se auth_user existe
            self.stdout.write('\n👤 VERIFICANDO AUTH_USER:')
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM information_schema.tables 
                    WHERE table_name = 'auth_user';
                """)
                count = cursor.fetchone()[0]
                if count > 0:
                    self.stdout.write('   ✅ Tabela auth_user existe!')
                    
                    # Contar usuários
                    cursor.execute("SELECT COUNT(*) FROM auth_user;")
                    user_count = cursor.fetchone()[0]
                    self.stdout.write(f'   👥 Total de usuários: {user_count}')
                else:
                    self.stdout.write('   ❌ Tabela auth_user NÃO existe!')
                    
        except Exception as e:
            self.stdout.write(f'❌ Erro geral: {e}')
            import traceback
            self.stdout.write(f'   Traceback: {traceback.format_exc()}')
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('🏁 CONFIGURAÇÃO POSTGRESQL COMPLETA!')
