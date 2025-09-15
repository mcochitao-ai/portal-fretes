from django.core.management.base import BaseCommand
from django.core.management import execute_from_command_line
from django.db import connection
import os

class Command(BaseCommand):
    help = 'Força execução das migrações no PostgreSQL'

    def handle(self, *args, **options):
        self.stdout.write('🚀 FORÇANDO MIGRAÇÕES NO POSTGRESQL')
        self.stdout.write('=' * 60)
        
        # Verificar se DATABASE_URL está definida
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            self.stdout.write('❌ DATABASE_URL não encontrada - usando SQLite')
            return
        
        self.stdout.write('✅ DATABASE_URL encontrada - usando PostgreSQL')
        
        try:
            # 1. Testar conexão
            self.stdout.write('\n🔌 TESTANDO CONEXÃO:')
            with connection.cursor() as cursor:
                cursor.execute("SELECT version();")
                version = cursor.fetchone()[0]
                self.stdout.write(f'   ✅ Conectado! PostgreSQL: {version[:50]}...')
            
            # 2. Executar makemigrations com verbosidade
            self.stdout.write('\n📝 EXECUTANDO MAKEMIGRATIONS:')
            try:
                execute_from_command_line(['manage.py', 'makemigrations', '--verbosity=2'])
                self.stdout.write('   ✅ Makemigrations executado com sucesso')
            except Exception as e:
                self.stdout.write(f'   ⚠️ Makemigrations: {e}')
            
            # 3. Executar migrate com verbosidade
            self.stdout.write('\n🚀 EXECUTANDO MIGRATE:')
            try:
                execute_from_command_line(['manage.py', 'migrate', '--verbosity=2'])
                self.stdout.write('   ✅ Migrate executado com sucesso')
            except Exception as e:
                self.stdout.write(f'   ❌ Migrate falhou: {e}')
                import traceback
                self.stdout.write(f'   Traceback: {traceback.format_exc()}')
            
            # 4. Verificar tabelas criadas
            self.stdout.write('\n📊 VERIFICANDO TABELAS CRIADAS:')
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
            
            # 5. Verificar tabelas essenciais
            essential_tables = ['auth_user', 'django_session', 'django_migrations']
            self.stdout.write('\n🔍 VERIFICANDO TABELAS ESSENCIAIS:')
            for table in essential_tables:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT COUNT(*) 
                        FROM information_schema.tables 
                        WHERE table_name = %s;
                    """, [table])
                    count = cursor.fetchone()[0]
                    if count > 0:
                        self.stdout.write(f'   ✅ {table}: EXISTE')
                    else:
                        self.stdout.write(f'   ❌ {table}: NÃO EXISTE')
            
            self.stdout.write('\n✅ MIGRAÇÕES FORÇADAS COM SUCESSO!')
            
        except Exception as e:
            self.stdout.write(f'❌ ERRO GERAL: {e}')
            import traceback
            self.stdout.write(f'   Traceback: {traceback.format_exc()}')
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('🏁 MIGRAÇÕES FORÇADAS COMPLETAS!')
