from django.core.management.base import BaseCommand
from django.core.management import execute_from_command_line
from django.db import connection
import os

class Command(BaseCommand):
    help = 'EMERGÊNCIA: Força migrações de qualquer forma'

    def handle(self, *args, **options):
        self.stdout.write('🚨 EMERGÊNCIA: FORÇANDO MIGRAÇÕES')
        self.stdout.write('=' * 80)
        
        try:
            # 1. Testar conexão
            self.stdout.write('\n🔌 TESTANDO CONEXÃO:')
            with connection.cursor() as cursor:
                cursor.execute("SELECT version();")
                version = cursor.fetchone()[0]
                self.stdout.write(f'   ✅ Conectado! PostgreSQL: {version[:50]}...')
            
            # 2. Executar makemigrations com --empty se necessário
            self.stdout.write('\n📝 EXECUTANDO MAKEMIGRATIONS:')
            try:
                execute_from_command_line(['manage.py', 'makemigrations', '--verbosity=2'])
                self.stdout.write('   ✅ Makemigrations executado')
            except Exception as e:
                self.stdout.write(f'   ⚠️ Makemigrations: {e}')
                # Tentar com --empty
                try:
                    execute_from_command_line(['manage.py', 'makemigrations', '--empty', '--verbosity=2'])
                    self.stdout.write('   ✅ Makemigrations --empty executado')
                except Exception as e2:
                    self.stdout.write(f'   ❌ Makemigrations --empty: {e2}')
            
            # 3. Executar migrate com --fake-initial
            self.stdout.write('\n🚀 EXECUTANDO MIGRATE:')
            try:
                execute_from_command_line(['manage.py', 'migrate', '--verbosity=2'])
                self.stdout.write('   ✅ Migrate executado')
            except Exception as e:
                self.stdout.write(f'   ⚠️ Migrate normal falhou: {e}')
                # Tentar com --fake-initial
                try:
                    execute_from_command_line(['manage.py', 'migrate', '--fake-initial', '--verbosity=2'])
                    self.stdout.write('   ✅ Migrate --fake-initial executado')
                except Exception as e2:
                    self.stdout.write(f'   ❌ Migrate --fake-initial: {e2}')
                    # Tentar com --run-syncdb
                    try:
                        execute_from_command_line(['manage.py', 'migrate', '--run-syncdb', '--verbosity=2'])
                        self.stdout.write('   ✅ Migrate --run-syncdb executado')
                    except Exception as e3:
                        self.stdout.write(f'   ❌ Migrate --run-syncdb: {e3}')
            
            # 4. Verificar tabelas essenciais
            self.stdout.write('\n🔍 VERIFICANDO TABELAS ESSENCIAIS:')
            essential_tables = ['django_session', 'auth_user', 'django_migrations']
            
            for table in essential_tables:
                try:
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
                except Exception as e:
                    self.stdout.write(f'   ❌ {table}: ERRO - {e}')
            
            # 5. Se django_session não existir, criar manualmente
            self.stdout.write('\n🔧 CRIANDO TABELA DJANGO_SESSION MANUALMENTE:')
            try:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS django_session (
                            session_key VARCHAR(40) NOT NULL PRIMARY KEY,
                            session_data TEXT NOT NULL,
                            expire_date TIMESTAMP WITH TIME ZONE NOT NULL
                        );
                    """)
                    self.stdout.write('   ✅ Tabela django_session criada manualmente')
            except Exception as e:
                self.stdout.write(f'   ❌ Erro ao criar django_session: {e}')
            
            # 6. Verificar todas as tabelas
            self.stdout.write('\n📊 TODAS AS TABELAS:')
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
            
            self.stdout.write('\n✅ EMERGÊNCIA CONCLUÍDA!')
            
        except Exception as e:
            self.stdout.write(f'❌ ERRO GERAL: {e}')
            import traceback
            self.stdout.write(f'   Traceback: {traceback.format_exc()}')
        
        self.stdout.write('\n' + '=' * 80)
        self.stdout.write('🏁 EMERGÊNCIA FINALIZADA!')
