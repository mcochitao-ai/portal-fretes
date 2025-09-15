from django.core.management.base import BaseCommand
from django.db import connection
from django.core.management import execute_from_command_line
import os

class Command(BaseCommand):
    help = 'Configura PostgreSQL corretamente'

    def handle(self, *args, **options):
        self.stdout.write('🐘 CONFIGURANDO POSTGRESQL CORRETAMENTE')
        self.stdout.write('=' * 60)
        
        # Verificar se DATABASE_URL está definida
        database_url = os.environ.get('DATABASE_URL')
        if database_url:
            self.stdout.write('✅ DATABASE_URL encontrada!')
            self.stdout.write(f'   URL: {database_url[:50]}...')
        else:
            self.stdout.write('❌ DATABASE_URL não encontrada - usando SQLite')
            return
        
        try:
            # 1. Testar conexão
            self.stdout.write('\n🔌 TESTANDO CONEXÃO:')
            with connection.cursor() as cursor:
                cursor.execute("SELECT version();")
                version = cursor.fetchone()[0]
                self.stdout.write(f'   ✅ Conectado! PostgreSQL: {version[:50]}...')
            
            # 2. Executar migrações
            self.stdout.write('\n📝 EXECUTANDO MIGRAÇÕES:')
            execute_from_command_line(['manage.py', 'makemigrations'])
            self.stdout.write('   ✅ Makemigrations executado')
            
            execute_from_command_line(['manage.py', 'migrate'])
            self.stdout.write('   ✅ Migrate executado')
            
            # 3. Verificar tabelas
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
            
            # 4. Verificar auth_user
            self.stdout.write('\n👤 VERIFICANDO AUTH_USER:')
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM auth_user;")
                count = cursor.fetchone()[0]
                self.stdout.write(f'   👥 Usuários na tabela auth_user: {count}')
            
            self.stdout.write('\n✅ POSTGRESQL CONFIGURADO COM SUCESSO!')
            
        except Exception as e:
            self.stdout.write(f'❌ ERRO: {e}')
            import traceback
            self.stdout.write(f'   Traceback: {traceback.format_exc()}')
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('🏁 CONFIGURAÇÃO POSTGRESQL COMPLETA!')
